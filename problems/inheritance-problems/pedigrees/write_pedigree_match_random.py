#!/usr/bin/env python3

"""
Pedigree matching question generator using randomly generated pedigrees.

This script generates matching questions where students must identify the
inheritance mode of randomly generated pedigree diagrams. Unlike the template-
based version (write_pedigree_match.py), this version uses the pedigree
skeleton and inheritance assignment engines to create novel pedigrees.
"""

# Standard Library
import os
import sys
import random

# Add pedigree_lib to path for local imports
pedigree_lib_path = os.path.join(os.path.dirname(__file__), 'pedigree_lib')
if pedigree_lib_path not in sys.path:
	sys.path.insert(0, pedigree_lib_path)

# Local repo modules
import bptools
import pedigree_lib.html_output
import pedigree_lib.code_definitions
import pedigree_lib.graph_parse as graph_parse
import pedigree_lib.mode_validate as mode_validate
import pedigree_lib.genetic_validation as genetic_validation

# Constants for inheritance modes
INHERITANCE_MODES = [
	'autosomal dominant',
	'autosomal recessive',
	'x-linked dominant',
	'x-linked recessive',
	'y-linked',
]

# Short names for display
MODE_SHORT_NAMES = {
	'autosomal dominant': 'autosomal dominant',
	'autosomal recessive': 'autosomal recessive',
	'x-linked dominant': 'x-linked dominant',
	'x-linked recessive': 'x-linked recessive',
	'y-linked': 'y-linked',
}

#=======================
def generate_valid_pedigree(
	mode: str,
	rng: random.Random,
	generations: int = 3,
	min_children: int = 2,
	max_children: int = 4,
	max_attempts: int = 100,
	show_carriers: bool = False,
	require_key_evidence: bool = False,
) -> str | None:
	"""
	Generate a random pedigree code string that is valid for the given mode.

	The function repeatedly generates pedigrees until one passes validation.

	Args:
		mode (str): Inheritance mode (e.g., 'autosomal dominant').
		rng (random.Random): Random number generator for reproducibility.
		generations (int): Number of generations (default 3).
		min_children (int): Minimum children per couple (default 2).
		max_children (int): Maximum children per couple (default 4).
		max_attempts (int): Maximum generation attempts before giving up.
		show_carriers (bool): Whether to show carrier status (for AR, XR).
		require_key_evidence (bool): Whether to require key diagnostic patterns.

	Returns:
		str | None: Valid pedigree code string, or None if generation failed.
	"""
	for _ in range(max_attempts):
		try:
			# Generate a random pedigree graph
			graph = graph_parse.generate_pedigree_graph(
				mode=mode,
				generations=generations,
				starting_couples=1,
				rng=rng,
				min_children=min_children,
				max_children=max_children,
				marry_in_rate=0.6,
				show_carriers=show_carriers,
			)

			# Render to code string
			code_string = graph_parse.render_graph_to_code(graph, show_carriers=show_carriers)

			# Validate the code string syntax
			import pedigree_lib.validation as validation
			syntax_errors = validation.validate_code_string(code_string)
			if syntax_errors:
				continue

			# Validate mode constraints (hard constraints that must pass)
			mode_errors = mode_validate.validate_mode_from_code(code_string, mode)
			if mode_errors:
				continue

			# Parse to get individual counts
			individuals, couples, _ = mode_validate.parse_pedigree_graph(code_string)

			# Check for key evidence patterns (optional, for stricter pedagogical quality)
			if require_key_evidence:
				key_errors = genetic_validation.validate_mode_keys(individuals, couples, mode)
				if key_errors:
					continue

			# Check minimum affected count (at least 1 for most modes)
			affected_count = sum(1 for ind in individuals.values() if ind.phenotype == 'affected')
			min_affected = 1
			# Y-linked needs affected males to be meaningful
			if mode == 'y-linked':
				min_affected = 1
			# For dominant/recessive, we want at least 1 affected
			if affected_count < min_affected:
				continue

			return code_string

		except (ValueError, KeyError, IndexError):
			# Generation or validation failed, try again
			continue

	return None


#=======================
def generate_pedigree_set(
	rng: random.Random,
	generations: int = 3,
	show_carriers: bool = False,
) -> dict[str, str] | None:
	"""
	Generate a complete set of pedigrees, one for each inheritance mode.

	Args:
		rng (random.Random): Random number generator.
		generations (int): Number of generations per pedigree.
		show_carriers (bool): Whether to show carrier status.

	Returns:
		dict[str, str] | None: Mapping of mode to code string, or None if failed.
	"""
	pedigrees: dict[str, str] = {}

	for mode in INHERITANCE_MODES:
		code_string = generate_valid_pedigree(
			mode=mode,
			rng=rng,
			generations=generations,
			show_carriers=show_carriers,
		)
		if code_string is None:
			return None
		pedigrees[mode] = code_string

	return pedigrees


#=======================
def matchingQuestionSet(start_num: int = 1, max_questions: int | None = None) -> list[str]:
	"""
	Generate a batch of pedigree matching questions with random pedigrees.

	Args:
		start_num (int): Starting question number.
		max_questions (int | None): Maximum number of questions to generate.

	Returns:
		list[str]: List of formatted Blackboard questions.
	"""
	bb_output_format_list: list[str] = []
	question_text = "<p>Match the following pedigrees to their most likely inheritance type.</p> "
	question_text += "<p>Note: <i>each inheritance type will only be used ONCE.</i></p> "

	choices_list = [
		'autosomal dominant',
		'autosomal recessive',
		'x-linked dominant',
		'x-linked recessive',
		'y-linked',
	]

	N = start_num - 1
	attempt_count = 0
	max_total_attempts = (max_questions or 99) * 10

	while attempt_count < max_total_attempts:
		if max_questions is not None and N >= start_num - 1 + max_questions:
			break

		attempt_count += 1
		rng = random.Random()

		# Generate a complete set of pedigrees
		pedigrees = generate_pedigree_set(rng, generations=3, show_carriers=False)
		if pedigrees is None:
			continue

		# Optionally mirror each pedigree
		prompts_list: list[str] = []
		for mode in INHERITANCE_MODES:
			code_string = pedigrees[mode]
			if random.random() < 0.5:
				code_string = pedigree_lib.code_definitions.mirror_pedigree(code_string)
			html_code = pedigree_lib.html_output.translateCode(code_string)
			prompts_list.append(html_code)

		N += 1
		bb_output_format = bptools.formatBB_MAT_Question(N, question_text, prompts_list, choices_list)
		bb_output_format_list.append(bb_output_format)

	return bb_output_format_list


#=======================
def write_question_batch(N: int, args) -> list[str]:
	"""
	Wrapper for batch question generation.

	Args:
		N (int): Starting question number.
		args: Parsed command-line arguments.

	Returns:
		list[str]: List of formatted questions.
	"""
	return matchingQuestionSet(N, args.max_questions)


#===========================================================
#===========================================================
def parse_arguments():
	"""
	Parses command-line arguments for the script.

	Returns:
		argparse.Namespace: Parsed arguments.
	"""
	parser = bptools.make_arg_parser(
		description="Generate pedigree matching questions with randomly generated pedigrees.",
		batch=True,
	)
	args = parser.parse_args()
	return args


#===========================================================
#===========================================================
def main():
	"""
	Main function that orchestrates question generation and file output.

	Workflow:
	1. Parse command-line arguments.
	2. Generate the output filename using script name and args.
	3. Generate formatted questions using random pedigree generation.
	4. Shuffle and trim the list if exceeding max_questions.
	5. Write all formatted questions to output file.
	6. Print stats and status.
	"""
	# Parse arguments from the command line
	args = parse_arguments()

	outfile = bptools.make_outfile()
	questions = bptools.collect_question_batches(write_question_batch, args)
	bptools.write_questions_to_file(questions, outfile)


#===========================================================
#===========================================================
if __name__ == '__main__':
	main()

## THE END
