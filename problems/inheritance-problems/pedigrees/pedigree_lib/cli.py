"""Shared homework CLI and export adapter; the three command names stay stable."""

# Standard Library
import json
import random
import pathlib
import argparse
import functools

# local repo modules
import bptools
import pedigree_lib.questions as questions
import pedigree_lib.svg_output as svg_output
import pedigree_lib.html_output as html_output
import pedigree_lib.inheritance as inheritance

LEGEND = ('<p>Squares: males; circles: females; filled symbols: affected; '
	'half-filled symbols: unaffected carriers. Assume complete penetrance and no new mutations.</p>')


#============================================
def parse_arguments(default_source: str) -> argparse.Namespace:
	"""Parse the shared pedigree command options.

	Args:
		default_source: authored or procedural default for the calling command.

	Returns:
		Parsed bptools and pedigree options; argparse exits on invalid combinations.
	"""
	parser = bptools.make_arg_parser(description='Generate pedigree inheritance homework.')
	parser.add_argument('-s', '--seed', dest='seed', type=int, default=None,
		help='Reproduce a verification run; normal runs use fresh randomness.')
	parser.add_argument('-f', '--source', dest='source', choices=('authored', 'procedural'),
		default=default_source, help='Choose the family source.')
	parser.add_argument('-y', '--yaml', dest='yaml', type=pathlib.Path, default=None,
		help='Authored people-and-unions YAML bank.')
	parser.add_argument('-r', '--review-dir', dest='review_dir', type=pathlib.Path, default=None,
		help='Save editable SVGs and instructor evidence alongside the questions.')
	args = parser.parse_args()
	if args.yaml is not None and args.source != 'authored':
		parser.error('--yaml requires --source authored')
	return args


#============================================
def write_question(N: int, args: argparse.Namespace, rng: random.Random,
		bank: list | None, matching: bool) -> object:
	"""Format an accepted MC or matching item for bptools.

	Args:
		N: Question number assigned by the shared collector.
		args: Parsed CLI options, including optional instructor review output.
		rng: Shared generator for case selection and presentation.
		bank: Accepted authored cases, or None for procedural generation.
		matching: Select matching instead of multiple choice.

	Returns:
		Formatted bptools question item.

	Raises:
		questions.GenerationFailure: No suitable case or presentation is available.
	"""
	if matching:
		cases = questions.matching_set(rng, bank)
	else:
		case = questions.present(rng.choice(bank), rng) if bank is not None else \
			questions.generate_case(rng.choice(inheritance.MODES), rng)
		cases = [case]
	drawings = [html_output.render_html(case.diagram, case.case.observations) for case in cases]
	if args.review_dir is not None:
		_save_review(N, args.review_dir, cases)
	if matching:
		prompt = '<p>Match each pedigree to its most likely inheritance pattern. Use each pattern once.</p>'
		item = bptools.formatBB_MAT_Question(N, prompt + LEGEND, drawings,
			[case.assessment.answer for case in cases])
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
		report.append(dict(svg=name, answer=assessment.answer,
			evidence=assessment.evidence[assessment.answer],
			compatible_modes=[mode for mode, result in assessment.compatibility.items() if result.compatible],
			attempts=case.attempts, rejections=case.rejections))
	(directory / f'question_{number:03d}_review.json').write_text(
		json.dumps(report, indent=2) + '\n', encoding='utf-8')


#============================================
def run(args: argparse.Namespace, matching: bool) -> None:
	"""Generate and export questions through the shared collector.

	Args:
		args: Parsed CLI options.
		matching: Select matching instead of multiple choice.

	Raises:
		ValueError: An authored bank fails acceptance.
		questions.GenerationFailure: Procedural or presentation search is exhausted.
	"""
	rng = random.Random(args.seed)
	# bptools/QTI own final choice obfuscation; seed their legacy RNG for byte reproducibility.
	random.seed(args.seed)
	bank = questions.authored_cases(args.yaml) if args.source == 'authored' else None
	writer = functools.partial(write_question, rng=rng, bank=bank, matching=matching)
	bptools.collect_and_write_questions(writer, args, bptools.make_outfile())
