#!/usr/bin/env python3
# ^^ Specifies the Python3 environment to use for script execution

# Import built-in Python modules
import math
import time
import random

# Import external modules (pip-installed)
# No external modules are used here currently

# Import local modules from the project
# Provides custom functions, such as question formatting and other utilities
import bptools
import deletionlib

#==========================================================
#==========================================================
def make_deletions(num_genes: int):
	"""
	Generates a random list of genes and a set of gene deletions such that:
	1. Every gene pair is included in at least one deletion.
	2. All possible split gene pairs (pairs split by deletions) are represented.

	Args:
		num_genes (int): The number of genes to include in the original list.

	Returns:
		tuple: A tuple containing:
			- gene_order (list[str]): The original ordered list of genes.
			- deletions_list (list[list[str]]): A list of deletions (each deletion is a sublist of genes).
	"""
	# Step 1: Generate and shuffle the list of genes
	gene_order = generate_gene_list(num_genes)

	# Step 2: Ensure the list is "most alphabetical"
	answer_gene_order = deletionlib.ensure_most_alphabetical(gene_order)

	# Step 5: Generate deletions until all pairs are covered
	deletions_list = deletionlib.generate_deletions(gene_order)

	return answer_gene_order, deletions_list


#==========================================================
#==========================================================
def generate_gene_list(num_genes: int, shuffle: bool=True) -> list[str]:
	"""
	Generates a shuffled list of genes of the specified size.

	Args:
		num_genes (int): The number of genes to include in the list.

	Returns:
		list[str]: A shuffled list of unique gene identifiers.
	"""
	charlist = list("ABCDEFGHJKMPQRSTWXYZ")
	if shuffle is True:
		random.shuffle(charlist)
	itemlist = charlist[:num_genes]
	#always shuffle the genes
	random.shuffle(itemlist)
	return itemlist

#==========================================================
#==========================================================
def generate_mc_distractors(answer_gene_order: list[str], num_choices: int):
	"""
	Generates multiple-choice distractors for a gene order question.

	Args:
		answer_gene_order (list[str]): The correct order of genes.
		num_choices (int): The total number of multiple-choice options, including the correct answer.

	Returns:
		tuple[list[str], str]: A list of formatted multiple-choice options and the correct answer.
	"""

	# Generate permutations starting with a random order from the current choices_set
	choices_set = set([tuple(answer_gene_order),])
	max_attempts = 1000 # Limit the number of attempts to prevent infinite loops
	attempts = 0

	while len(choices_set) < num_choices and attempts < max_attempts:
		# Start with a random choice from the existing set
		base_gene_order = list(random.choice(list(choices_set)))
		choice_gene_order = base_gene_order[:]

		# Introduce controlled randomness by swapping adjacent genes
		index1 = random.randint(2, len(base_gene_order) - 1)  # Avoid the first gene
		index2 = index1 - 1
		choice_gene_order[index1], choice_gene_order[index2] = choice_gene_order[index2], choice_gene_order[index1]

		# Add the modified order to the set
		choices_set.add(tuple(choice_gene_order))
		attempts += 1

	if len(choices_set) < num_choices:
		num_genes = len(answer_gene_order)
		# Fixing the first gene, permute the rest
		max_choices = math.factorial(num_genes - 1)
		raise ValueError(f"Only able to generate of {len(choices_set)} of {num_choices} choices with {num_genes} genes after {attempts} attempts. Maximum possible is {max_choices}.")

	# Generate the correct answer text
	answer_text = deletionlib.format_choice(answer_gene_order)

	# Convert the set of tuples to a list of formatted strings
	choices_list = [deletionlib.format_choice(list(choice)) for choice in choices_set]

	# Deduplicate and sort the results for consistent output
	choices_list = sorted(set(choices_list))

	return choices_list, answer_text
cl, a = generate_mc_distractors(list("ABCD"), 6)
assert len(cl) == 6
assert a == deletionlib.format_choice(list("ABCD"))
cl, a = generate_mc_distractors(list("ABCDE"), 8)
assert len(cl) == 8, f"Expected 8 choices, got {len(cl)}."
assert a == deletionlib.format_choice(list("ABCDE")), "Expected correct answer not obtained"

#==========================================================
#==========================================================
def write_question(N: int, args) -> str:
	"""
	Creates a single formatted question with various answer formats and tables.

	Args:
		N (int): The question number.
		num_genes (int): The total number of genes to work with.
		num_choices (int): The number of multiple-choice options.

	Returns:
		str: A formatted question ready to be written to the output file.
	"""
	background = deletionlib.generate_background_for_deletions(args.num_genes)
	steps = deletionlib.get_deletion_mutant_steps()

	# Generate the original list of genes and the set of deleted genes
	answer_gene_order, deletions_list = make_deletions(args.num_genes)

	# Shuffle the deleted genes randomly for question variability
	random.shuffle(deletions_list)

	# Assign colors to genes using the dark_color_wheel
	color_wheel = None
	while color_wheel is None:
		try:
			color_wheel = bptools.default_color_wheel(len(deletions_list))
		except ValueError:
			print("COLOR WHEEL FAIL")
			time.sleep(0.5)

	deletion_colors = {''.join(deletion): color_wheel[i] for i, deletion in enumerate(deletions_list)}

	print("Making TABLE")
	table = deletionlib.make_html_table(answer_gene_order, deletions_list, deletion_colors)

	# Create the question text based on the original and deleted genes
	print('write_question_text()')
	question = deletionlib.write_question_text(answer_gene_order, deletions_list,
				deletion_colors, False, args.first_letter)

	# Combine the question and table (if available) into the question text
	question_text = background + steps + table + question

	# Format the question and answer into the final output structure
	if args.question_type == 'fib':
		# Collect all possible answer variations
		print('generate_fib_answer_variations()')
		answers_list = deletionlib.generate_fib_answer_variations(answer_gene_order)
		complete_question = bptools.formatBB_FIB_Question(N, question_text, answers_list)
	else:
		# Collect all possible distractor variations
		print('generate_mc_distractors()')
		choices_list, answer_text = generate_mc_distractors(answer_gene_order, args.num_choices)
		complete_question = bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)

	return complete_question


#==========================================================
#==========================================================
def apply_difficulty_defaults(args):
	presets = {
		'easy': {
			'num_genes': 4,
			'num_choices': 5,
			'first_letter': True,
		},
		'medium': {
			'num_genes': 5,
			'num_choices': 5,
			'first_letter': False,
		},
		'rigorous': {
			'num_genes': 6,
			'num_choices': 6,
			'first_letter': False,
		},
	}
	preset = presets.get(args.difficulty, presets['medium'])

	if args.num_genes is None:
		args.num_genes = preset['num_genes']
	if args.num_choices is None:
		args.num_choices = preset['num_choices']
	if args.first_letter is None:
		args.first_letter = preset['first_letter']

	return args

#==========================================================
#==========================================================
def main() -> None:
	"""
	Main function that orchestrates question generation and file output.

	Workflow:
	1. Parse command line arguments.
	2. Build output filename from script name and args.
	3. Generate formatted questions with write_question().
	4. Shuffle and trim to max_questions.
	5. Write all questions to the output file.
	6. Print stats and status.
	"""
	args = parse_arguments()
	outfile = bptools.make_outfile(f"{args.num_genes:02d}_genes",
		args.question_type.upper()
	)
	bptools.collect_and_write_questions(write_question, args, outfile)

#==========================================================
def parse_arguments():
	parser = bptools.make_arg_parser(description="Generate deletion mutant questions.")
	parser = bptools.add_choice_args(parser, default=None)
	parser = bptools.add_difficulty_args(parser)
	parser.add_argument(
		'-g', '--num-genes', metavar='#', type=int, dest='num_genes',
		help='number of deleted genes on the chromosome', default=None
	)
	parser.add_argument(
		'-F', '--first-letter', dest='first_letter', action='store_true',
		help='give a hint about the first letter in the gene sequence'
	)
	parser.add_argument(
		'-N', '--no-first-letter', dest='first_letter', action='store_false',
		help='do not give a hint about the first letter in the gene sequence'
	)
	parser.set_defaults(first_letter=None)
	parser = bptools.add_question_format_args(
		parser,
		types_list=['fib', 'mc'],
		required=False,
		default='mc'
	)
	args = parser.parse_args()
	args = apply_difficulty_defaults(args)

	if args.num_genes < 4:
		raise ValueError("Sorry, you must have at least 4 genes for this program")
	if args.num_genes > 20:
		raise ValueError("Sorry, you can have at most 20 genes for this program")

	max_choices = math.factorial(args.num_genes - 1)
	if args.num_choices > max_choices:
		raise ValueError(
			f"Cannot generate {args.num_choices} choices with {args.num_genes} genes. "
			f"Maximum possible is {max_choices}."
		)
	return args

#==========================================================
#==========================================================
if __name__ == '__main__':
	main()
