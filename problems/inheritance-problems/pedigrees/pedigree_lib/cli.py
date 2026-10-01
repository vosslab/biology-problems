"""Shared homework CLI and export adapter; all three question formats share one pipeline."""

# Standard Library
import json
import random
import pathlib
import argparse
import functools
import dataclasses
import collections.abc

# local repo modules
import bptools
import pedigree_lib.questions as questions
import pedigree_lib.svg_output as svg_output
import pedigree_lib.html_output as html_output
import pedigree_lib.inheritance as inheritance
import pedigree_lib.similarity as similarity
import pedigree_lib.ranking as ranking
import pedigree_lib.scenarios as scenarios

LEGEND = ('<p>Squares: males; circles: females; filled symbols: affected; '
	'empty symbols: unaffected. Assume complete penetrance and no new mutations.</p>')


#============================================
def parse_arguments() -> argparse.Namespace:
	"""Parse the shared pedigree command options.

	Returns:
		Parsed bptools and pedigree options; argparse exits on invalid combinations.
	"""
	parser = bptools.make_arg_parser(description='Generate pedigree inheritance homework. '
		'Difficulty combines family size, branching, and tracing depth; '
		'all levels use the same inheritance-evidence checks.')
	parser.add_argument('-s', '--seed', dest='seed', type=int, default=None,
		help='Reproduce a verification run; normal runs use fresh randomness.')
	parser.add_argument('-r', '--review-dir', dest='review_dir', type=pathlib.Path, default=None,
		help='Save editable SVGs and instructor evidence alongside the questions.')
	difficulty = parser.add_mutually_exclusive_group()
	for level in ('easy', 'medium', 'rigorous'):
		difficulty.add_argument(f'--{level}', dest='difficulty', action='store_const', const=level,
			help=f'Use {level} structural workload (default: medium).')
	difficulty.add_argument('--bonus', dest='difficulty', action='store_const', const='bonus',
		help='Use a 30-40-person family; only supported by write_pedigree_to_pattern.py.')
	parser.set_defaults(difficulty='medium')
	args = parser.parse_args()
	return args


#============================================
def write_question(N: int, args: argparse.Namespace, rng: random.Random,
		scenario_iter: collections.abc.Iterator[tuple], question_format: str) -> object:
	"""Format an accepted MC or matching item for bptools.

	Args:
		N: Question number assigned by the shared collector.
		args: Parsed CLI options, including optional instructor review output.
		rng: Shared generator for case selection and presentation.
		scenario_iter: Prepared scenarios; each call consumes one, including collector retries.
		question_format: identify, select, or match.

	Returns:
		Formatted bptools question item, or None when the finite pool is exhausted.
	"""
	scenario = next(scenario_iter, None)
	if scenario is None:
		return None
	cases = list(scenario)
	rng.shuffle(cases)
	drawings = [html_output.render_html(case.diagram, case.case.observations) for case in cases]
	if args.review_dir is not None:
		_save_review(N, args.review_dir, cases)
	if question_format == 'match':
		prompt = '<p>Match each pedigree to its most likely inheritance pattern. Use each pattern once.</p>'
		item = bptools.formatBB_MAT_Question(N, prompt + LEGEND, drawings,
			[case.assessment.answer for case in cases])
	elif question_format == 'select':
		index = rng.randrange(len(cases))
		mode = cases[index].assessment.answer
		prompt = f'<p>Which pedigree most likely demonstrates <strong>{mode}</strong> inheritance?</p>'
		item = bptools.formatBB_MC_Question(N, prompt + LEGEND, drawings, drawings[index])
	else:
		prompt = '<p>Which inheritance pattern is most likely demonstrated by this pedigree?</p>'
		choices = list(inheritance.MODES)
		rng.shuffle(choices)
		item = bptools.formatBB_MC_Question(N, drawings[0] + prompt + LEGEND,
			choices, cases[0].assessment.answer)
	return item


#============================================
def _save_review(number: int, directory: pathlib.Path, cases: list) -> None:
	directory.mkdir(parents=True, exist_ok=True)
	report = []
	for index, case in enumerate(cases, 1):
		name = f'question_{number:03d}_case_{index:02d}.svg'
		(directory / name).write_text(svg_output.render_svg(case.diagram, case.case.observations),
			encoding='utf-8')
		assessment = case.assessment
		complexity = similarity.complexity(case.case.family)
		report.append(dict(svg=name, answer=assessment.answer,
			ranking_score=ranking.score(case),
			complexity=dataclasses.asdict(complexity), complexity_sort_key=complexity.sort_key(),
			evidence=assessment.evidence[assessment.answer],
			compatible_modes=[mode for mode, result in assessment.compatibility.items() if result.compatible],
			attempts=case.attempts, rejections=case.rejections))
	(directory / f'question_{number:03d}_review.json').write_text(
		json.dumps(report, indent=2) + '\n', encoding='utf-8')
	if len(cases) > 1:
		comparisons = similarity.pairwise([case.case for case in cases])
		(directory / f'question_{number:03d}_similarity.json').write_text(
			json.dumps(comparisons, indent=2) + '\n', encoding='utf-8')


#============================================
def run(args: argparse.Namespace, question_format: str) -> None:
	"""Generate and export questions through the shared collector.

	Args:
		args: Parsed CLI options.
		question_format: identify, select, or match.

	Raises:
		questions.GenerationFailure: Procedural search or the scenario pool is exhausted.
	"""
	rng = random.Random(args.seed)
	# bptools/QTI own final choice obfuscation; seed their legacy RNG for byte reproducibility.
	random.seed(args.seed)
	requested = args.duplicates
	if args.max_questions is not None:
		requested = min(requested, args.max_questions)
	prepared = []
	if requested > 0:
		print('Preparing 5,000 valid pedigree candidates...')
		prepared = scenarios.build(rng, args.difficulty, question_format)
		print(f'Prepared {len(prepared)} complete {question_format} scenarios.')
		if requested > len(prepared):
			raise questions.GenerationFailure(f'Requested {requested} questions, but the pool has '
				f'only {len(prepared)} complete {question_format} scenarios')
	# Select the best eligible scenarios, then randomize question order. Keep reserves for
	# collector duplicate rejection; retries consume new entries even when N stays unchanged.
	selected = prepared[:requested]
	rng.shuffle(selected)
	scenario_iter = iter(selected + prepared[requested:])
	writer = functools.partial(write_question, rng=rng, scenario_iter=scenario_iter,
		question_format=question_format)
	bptools.collect_and_write_questions(writer, args, bptools.make_outfile())
