#!/usr/bin/env python3

"""
Pedigree matching question generator using randomly generated pedigrees.

This script generates matching questions where students must identify the
inheritance mode of randomly generated pedigree diagrams. Unlike the template-
based version (write_pedigree_match.py), this version uses the pedigree
skeleton and inheritance assignment engines to create novel pedigrees.

Each question generates fresh random pedigrees on-demand.
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
import pedigree_lib.validation as validation
import pedigree_lib.graph_parse as graph_parse
import pedigree_lib.mode_validate as mode_validate

# Constants for inheritance modes
INHERITANCE_MODES = [
	'autosomal dominant',
	'autosomal recessive',
	'x-linked dominant',
	'x-linked recessive',
	'y-linked',
]

#=======================
def count_individuals(code_string: str) -> int:
	"""Count the number of individuals in a pedigree code string."""
	individuals, _, _ = mode_validate.parse_pedigree_graph(code_string)
	return len(individuals)


#=======================
def generate_valid_pedigree(
	mode: str,
	generations: int = 3,
	min_children: int = 2,
	max_children: int = 4,
	max_attempts: int = 100,
	show_carriers: bool = False,
	min_individuals: int | None = None,
	max_individuals: int | None = None,
) -> str | None:
	"""
	Generate a random pedigree code string that is valid for the given mode.

	Args:
		mode (str): Inheritance mode (e.g., 'autosomal dominant').
		generations (int): Number of generations (default 3).
		min_children (int): Minimum children per couple (default 2).
		max_children (int): Maximum children per couple (default 4).
		max_attempts (int): Maximum generation attempts before giving up.
		show_carriers (bool): Whether to show carrier status (for AR, XR).
		min_individuals (int | None): Minimum number of individuals (optional).
		max_individuals (int | None): Maximum number of individuals (optional).

	Returns:
		str | None: Valid pedigree code string, or None if generation failed.
	"""
	for _ in range(max_attempts):
		try:
			rng = random.Random()

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
			syntax_errors = validation.validate_code_string(code_string)
			if syntax_errors:
				continue

			# Validate mode constraints (hard constraints that must pass)
			mode_errors = mode_validate.validate_mode_from_code(code_string, mode)
			if mode_errors:
				continue

			# Parse to get individual counts
			individuals, couples, _ = mode_validate.parse_pedigree_graph(code_string)

			# Check individual count constraints
			num_individuals = len(individuals)
			if min_individuals is not None and num_individuals < min_individuals:
				continue
			if max_individuals is not None and num_individuals > max_individuals:
				continue

			# Check minimum affected count (at least 1 for most modes)
			affected_count = sum(1 for ind in individuals.values() if ind.phenotype == 'affected')
			if affected_count < 1:
				continue

			# Reject pedigrees with childless couples (invalid per spec)
			has_childless_couple = any(not couple.children for couple in couples)
			if has_childless_couple:
				continue

			return code_string

		except (ValueError, KeyError, IndexError):
			# Generation or validation failed, try again
			continue

	return None


#=======================
def generate_pedigree_set(
	generations: int = 3,
	show_carriers: bool = False,
	min_individuals: int = 8,
	max_individuals: int = 14,
	max_size_spread: int = 4,
	max_set_attempts: int = 20,
) -> dict[str, str] | None:
	"""
	Generate a complete set of pedigrees with similar complexity.

	All pedigrees in the set will have individual counts within a constrained
	range to ensure fair comparison in matching questions.

	Args:
		generations (int): Number of generations per pedigree.
		show_carriers (bool): Whether to show carrier status.
		min_individuals (int): Minimum individuals per pedigree (default 8).
		max_individuals (int): Maximum individuals per pedigree (default 14).
		max_size_spread (int): Maximum difference between largest and smallest
			pedigree in the set (default 4).
		max_set_attempts (int): Maximum attempts to generate a balanced set.

	Returns:
		dict[str, str] | None: Mapping of mode to code string, or None if failed.
	"""
	for _ in range(max_set_attempts):
		pedigrees: dict[str, str] = {}
		sizes: dict[str, int] = {}

		# Generate a pedigree for each mode within the size constraints
		for mode in INHERITANCE_MODES:
			code_string = generate_valid_pedigree(
				mode=mode,
				generations=generations,
				show_carriers=show_carriers,
				min_individuals=min_individuals,
				max_individuals=max_individuals,
			)
			if code_string is None:
				break  # Failed to generate for this mode, retry whole set
			pedigrees[mode] = code_string
			sizes[mode] = count_individuals(code_string)

		# Check if we got all modes
		if len(pedigrees) != len(INHERITANCE_MODES):
			continue

		# Check if the size spread is acceptable
		size_values = list(sizes.values())
		spread = max(size_values) - min(size_values)
		if spread <= max_size_spread:
			return pedigrees

		# Size spread too large, try again

	return None


#=======================
def write_question(N: int, args) -> str | None:
	"""
	Generate a single pedigree matching question with fresh random pedigrees.

	Args:
		N (int): Question number (1-based).
		args: Parsed command-line arguments.

	Returns:
		str | None: Formatted Blackboard MAT question, or None if generation failed.
	"""
	# Generate a fresh set of pedigrees for this question
	pedigree_set = generate_pedigree_set(generations=3, show_carriers=False)
	if pedigree_set is None:
		return None

	question_text = "<p>Match the following pedigrees to their most likely inheritance type.</p> "
	question_text += "<p>Note: <i>each inheritance type will only be used ONCE.</i></p> "

	choices_list = [
		'autosomal dominant',
		'autosomal recessive',
		'x-linked dominant',
		'x-linked recessive',
		'y-linked',
	]

	# Build prompts list with optional mirroring
	prompts_list: list[str] = []
	for mode in INHERITANCE_MODES:
		code_string = pedigree_set[mode]
		# Randomly mirror each pedigree for visual variety
		if random.random() < 0.5:
			code_string = pedigree_lib.code_definitions.mirror_pedigree(code_string)
		html_code = pedigree_lib.html_output.translateCode(code_string)
		prompts_list.append(html_code)

	bb_output_format = bptools.formatBB_MAT_Question(N, question_text, prompts_list, choices_list)
	return bb_output_format


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
	)
	args = parser.parse_args()
	return args


#===========================================================
#===========================================================
def main():
	"""
	Main function that orchestrates question generation and file output.
	"""
	args = parse_arguments()
	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)


#===========================================================
#===========================================================
if __name__ == '__main__':
	main()

## THE END
