#!/usr/bin/env python3

import copy
import math
import random
import textwrap
import time

import bptools


#==========================================================
#==========================================================
def generate_background_for_deletions(num_genes: int, table: bool) -> str:
	"""
	Generates a background explanation about using deletion mutants to determine the order of genes.

	Args:
		num_genes (int): The number of genes involved in the problem.
		table (bool): Whether additional information about polytene chromosomes is included.

	Returns:
		str: The background explanation as an HTML string.
	"""
	# Convert the number of genes to cardinal text
	cardinal_text = bptools.number_to_cardinal(num_genes)

	# Start with a header
	background_text = '<h4>Using Deletion Mutants to Determine Gene Order</h4>'

	# General introduction about deletion mutants
	background_text += (
		f'<p>Deletion mutants are an essential tool in genetics for uncovering the order of '
		f'{cardinal_text} ({num_genes}) genes on a chromosome. Deletions remove specific regions of '
		f'the chromosome, allowing researchers to observe the effects of the missing genes '
		f'on the phenotype of the organism. This approach is particularly useful for identifying the '
		f'locations of recessive genes, which are only revealed when the corresponding wildtype copies '
		f'are absent.</p>'
	)

	# Context-specific explanation of the test cross with deletion mutants
	background_text += (
		f'<p>In a test cross involving deletion mutants, one parent carries a full-length wildtype chromosome and '
		f'a second chromosome with a deletion, while the other parent is homozygous recessive for all '
		f'{cardinal_text} genes. Offspring inheriting the full-length wildtype chromosome display the dominant phenotype '
		f'for all {cardinal_text} genes in the test cross. '
		f'However, offspring inheriting the chromosome with the deletion will display some recessive traits. '
		'These recessive traits uncover the missing genes in the deleted region. '
		f'By analyzing which genes are uncovered in a series of different '
		f'deletion mutants, the linear order of the genes can be determined.</p>'
	)

	# Expand explanation with polytene chromosomes if table=True
	if table:
		background_text += (
			'<p>In organisms such as <i>Drosophila melanogaster</i>, polytene chromosomes from the salivary '
			'glands provide a physical map for studying deletions. Polytene chromosomes are giant chromosomes '
			'with distinct banding patterns, allowing researchers to directly visualize which regions of the '
			'chromosome are deleted. This visual representation complements the genetic data obtained from test '
			'crosses.</p>'
		)

	# Conclude with the problem's goal
	background_text += (
		f'<p>For this problem, deletion mutants have been generated for a chromosome containing '
		f'{cardinal_text} genes. Your goal is to analyze the phenotypic data resulting from these deletions '
		f'and determine the correct linear order of the genes.</p>'
	)

	return background_text

#===========================================================
#===========================================================
def get_deletion_mutant_steps() -> str:
	"""
	Returns the HTML formatted step-by-step instructions for solving deletion mutant problems.

	Returns:
		str: HTML formatted string with step-by-step instructions.
	"""
	steps = '<h6>Step-by-Step Instructions for Solving Deletion Mutant Problems</h6>'
	steps += '<ul>'
	steps += ' <li>Step 1: Simplify the information.</li>'
	steps += '   <ul><li>List the genes and deletions provided in the question.</li>'
	steps += '   <li>Organize the deletions in a clear table or list format for easier analysis.</li></ul>'
	steps += ' <li>Step 2: Create a template for the gene order.</li>'
	steps += '   <ul><li>Start with placeholders for each gene (e.g., _ _ _ _).</li>'
	steps += '   <li>Insert known genes based on hints (e.g., the first or last gene).</li></ul>'
	steps += ' <li>Step 3: Identify deletions containing the first gene.</li>'
	steps += '   <ul><li>Analyze deletions that include the first gene to determine its neighbors.</li>'
	steps += '   <li>Use deletions that overlap to narrow down adjacent genes.</li></ul>'
	steps += ' <li>Step 4: Analyze deletions containing the next genes.</li>'
	steps += '   <ul><li>Look for deletions that include specific pairs of genes.</li>'
	steps += '   <li>Identify deletions that exclude certain genes to resolve ambiguities.</li></ul>'
	steps += ' <li>Step 5: Verify the answer using all of the listed deletions.</li>'
	steps += '   <ul><li>Deletion questions can be hard to solve, but once you have an answer, it is easy to check if it is correct!</li>'
	steps += '   <li>Go through each deletion and confirm that the proposed gene order matches the genes included in that deletion.</li>'
	steps += '   <li>If any deletion is inconsistent with the proposed order, your answer is wrong.</li></ul>'
	steps += '</ul>'

	return steps

#==========================================================
#==========================================================
def color_deletion_name(deletion_text: str, deletion_key_str: str, deletion_colors: dict) -> str:
	"""
	Applies a unique color to a deletion's text based on its key.

	Args:
		deletion_text (str): The text to be colored (e.g., "Del #3: A, B, and C").
		deletion_key_str (str): The string key for the deletion (e.g., "ABC").
		deletion_colors (dict): A dictionary mapping deletion keys to colors.

	Returns:
		str: The HTML-formatted string with the appropriate color applied.
	"""
	# Wrap the text in a span with the corresponding color
	return f'<span style="color: #{deletion_colors[deletion_key_str]}; font-weight: bold;">{deletion_text}</span>'

#==========================================================
#==========================================================
def make_html_table(gene_order, deletions_list, deletion_colors):
	CELL_W = 60
	ROW_H = 25

	table = ''
	table += '<table style="border-collapse: collapse; border: 2px solid black; '
	width = CELL_W * (len(gene_order) + 1)
	height = ROW_H * (len(deletions_list) + 1)
	#table += f'width: {width}px; height: {height}px;'
	table += '">'
	table += '<tr><th> </th>'

	# Header for gene labels, gene order is unknown so just numbers
	for i in range(len(gene_order)):
		table += f'<th style="text-align: center; width: {CELL_W}px;">Gene {i+1}</th>'
	table += '</tr>'

	# Rows for deletions
	for i, deletion in enumerate(deletions_list):
		# Generate a deletion key string (e.g., "ABC")
		deletion_key_str = ''.join(sorted(deletion))

		# Row header for each deletion
		colored_deletion_name = color_deletion_name(f"Del #{i+1}", deletion_key_str, deletion_colors)
		table += f'<tr><th style="text-align: center;">{colored_deletion_name}</th>'

		for gene in gene_order:
			bg = deletion_colors[deletion_key_str] if gene in deletion else "EEEEEE"
			table += f'<td style="background-color: #{bg}; height: {ROW_H}px;">&nbsp;</td>'

		table += '</tr>'
	table += '</table>'
	return table

#==========================================================
#==========================================================
def list2text(mylist: list[str]) -> str:
	"""
	Converts a list of strings into a human-readable text format with an Oxford comma.

	If the list has more than two elements, it adds commas between elements and inserts
	"and" before the last element, ensuring an Oxford comma is included. For a list of
	exactly two elements, it joins them with "and". For an empty list or a single element,
	it returns an empty string or the single element respectively.

	Args:
		mylist (list[str]): A list of strings to convert into human-readable text.

	Returns:
		str: The human-readable string representation of the list.
	"""
	# Handle lists with more than two elements (include an Oxford comma)
	if len(mylist) > 2:
		return f"{', '.join(mylist[:-1])}, and {mylist[-1]}"

	# Handle lists with exactly two elements
	elif len(mylist) == 2:
		return f"{mylist[0]} and {mylist[1]}"

	# Return an empty string for empty lists
	elif len(mylist) == 0:
		return ""

	# For a single element, return the element itself
	else:
		return mylist[0]
#====================
# Assertions to verify correctness
assert list2text(list('abcd')) == "a, b, c, and d", \
	"Failed test case with more than 2 elements (Oxford comma required)"
assert list2text(['x', 'y']) == "x and y", \
	"Failed test case with exactly 2 elements"
assert list2text(['z']) == "z", \
	"Failed test case with a single element"
assert list2text([]) == "", \
	"Failed test case with an empty list"

#==========================================================
#==========================================================
def write_question_text(gene_order, deletions_list, deletion_colors):
	"""
	Writes the question about gene order based on the original list and deletions.
	"""
	### write question
	#Genes a, b, c, d, e, and f are closely linked in a chromosome, but their order is unknown.
	#Four deletions in the region are found to uncover recessive alleles of the genes as follows:
	#Deletion 1 uncovers a, d, and f; Deletion?2 uncovers d, e, and f; Deletion?3 uncovers c, d, and e;
	#Deletion 4 uncovers b and c. Which one of the following is the correct order for the genes?

	# Create a sorted copy of the original gene list
	sorted_gene_order = sorted(copy.copy(gene_order))
	sorted_gene_order_str = list2text(sorted_gene_order)

	# Number of genes and deletions (in words and digits)
	num_genes_int = len(gene_order)
	num_genes_word = f"{bptools.number_to_cardinal(num_genes_int)} ({num_genes_int})"
	num_deletions_int = len(deletions_list)
	num_deletions_word = f"{bptools.number_to_cardinal(num_deletions_int)} ({num_deletions_int})"

	# Start building the question text
	question = ""

	# Main description
	question += (
		f"<p>There are {num_genes_word} genes, "
		f"{sorted_gene_order_str}, closely linked in a single chromosome. However, "
		"their order is unknown. "
	)
	question += (
		f"In the region, {num_deletions_word} deletions have been identified. "
		"These deletions uncover recessive alleles of the genes as follows:</p><ul>"
	)

	# Add details for each deletion
	for i, deletion in enumerate(deletions_list):
		# Generate a deletion key string (e.g., "ABC")
		deletion_key_str = ''.join(sorted(deletion))
		deletions_word_str = list2text(deletion)

		# Colorize the deletion description
		colored_deletion = color_deletion_name(
			f"Deletion #{i+1}: <strong>{deletions_word_str}</strong>",
			deletion_key_str,
			deletion_colors
		)
		question += f"<li>{colored_deletion}</li>"

	# Add the final question and hints
	question += (
		f"</ul> <p>What is the correct order of the "
		f"{num_genes_word} genes?</p> "
	)
	question += (
		f"<p><strong>Hint 1</strong>: The first gene at start of the chromosome is "
		f"<strong>gene {gene_order[0]}</strong>.</p> "
	)
	question += (
		f"<p><strong>Hint 2</strong>: Enter your answer in the blank using only "
		f"{num_genes_word} letters, or one comma every three (3) letters. Do not include "
		"extra commas or spaces in your answer.</p>"
	)

	# Check for invalid newlines in the question
	if '\n' in question:
		raise ValueError("New lines are not allowed")

	return question

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
	answer_gene_order = ensure_most_alphabetical(gene_order)

	# Step 5: Generate deletions until all pairs are covered
	deletions_list = generate_deletions(gene_order)

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
def ensure_most_alphabetical(itemlist: list[str]) -> list[str]:
	"""
	Reverses the itemlist if the first element is greater than the last,
	to ensure the list is in its "most alphabetical" form.

	Args:
		itemlist (list[str]): A list of gene identifiers.

	Returns:
		list[str]: The adjusted list.
	"""
	if itemlist[0] > itemlist[-1]:
		itemlist.reverse()
	return copy.copy(itemlist)

#==========================================================
#==========================================================
def generate_deletions(gene_order: list[str]) -> list[list[str]]:
	"""
	Generates a list of deletions such that:
	1. All possible neighboring pairs of genes are covered.
	2. All possible split pairs (pairs split by deletions) are included.

	Args:
		gene_order (list[str]): The original list of genes in their current order.

	Returns:
		list[list[str]]: A list of deletions, where each deletion is a sublist of genes.
	"""
	# Number of genes in the gene order
	num_genes = len(gene_order)

	# Total number of neighboring gene pairs to be covered
	required_gene_pairs = num_genes - 1

	# Minimum and maximum sizes for deletions
	min_deletion_size = 2
	upper_limit = int(math.sqrt(num_genes)*2) + 1
	upper_limit = max(5, upper_limit)
	max_deletion_size = min(num_genes - 1, upper_limit)

	# Dictionaries to track progress
	split_gene_pairs = {}  # Tracks pairs of genes split by deletions
	used_gene_pairs = {}   # Tracks neighboring pairs of genes within deletions
	deletions_list = []    # List to store all generated deletions

	# Iteration counter to avoid infinite loops (can be useful for debugging)
	iterations = 0

	# Generate deletions until all required pairs are covered
	while len(split_gene_pairs) < required_gene_pairs or len(used_gene_pairs) < required_gene_pairs:
		iterations += 1

		# Decide the size of the deletion
		if random.random() < 0.1:  # 10% chance to use any size within range
			deletion_size = random.randint(min_deletion_size, max_deletion_size)
		elif num_genes > 4 and random.random() < 0.7:  # 70% chance for larger deletions
			deletion_size = random.randint(min_deletion_size + 2, max_deletion_size)
		else:  # Default case for medium-sized deletions
			deletion_size = random.randint(min_deletion_size + 1, max_deletion_size)

		# Choose a random starting point for the deletion
		deletion_start = random.randint(0, num_genes - deletion_size)

		# Extract the genes for the current deletion
		deletion = gene_order[deletion_start:deletion_start + deletion_size]

		# Call the function
		new_pairs = add_new_pairs(
			gene_order, deletion_start, deletion_size, split_gene_pairs, used_gene_pairs
		)

		# Sort the deletion to ensure consistent order
		deletion.sort()

		# Add the deletion to the list if it adds new information and is not a duplicate
		if new_pairs > 0 and deletion not in deletions_list:
			deletions_list.append(deletion)
			print(f"New Deletion #{len(deletions_list)}: {deletion}")

	# Print summary of results
	print("")
	print(f"Total neighboring gene pairs used: {len(used_gene_pairs)}")
	print(f"Total split gene pairs included: {len(split_gene_pairs)}\n")

	return deletions_list

#==========================================================
#==========================================================
def add_new_pairs(
	gene_order: list[str], start: int, size: int,
	split_gene_pairs: dict, used_gene_pairs: dict
) -> int:
	"""
	Adds both split pairs (pairs split by a deletion) and neighboring pairs (within the deletion)
	to their respective dictionaries, and tracks how many new pairs were added.

	Args:
		gene_order (list[str]): The original list of genes.
		start (int): The starting index of the deletion.
		size (int): The size of the deletion.
		split_gene_pairs (dict): Dictionary tracking pairs split by deletions.
		used_gene_pairs (dict): Dictionary tracking neighboring pairs used in deletions.

	Returns:
		int: The total number of new pairs (split + neighboring) added to the dictionaries.
	"""
	new_pairs = 0

	# Step 1: Add split gene pairs (pairs split by this deletion)
	# Check the pair before the deletion
	if start > 0:  # Ensure we don't go out of bounds
		pair = gene_order[start - 1] + gene_order[start]
		if pair not in split_gene_pairs:
			split_gene_pairs[pair] = True
			new_pairs += 1

	# Check the pair after the deletion
	if start + size < len(gene_order):  # Ensure we don't go out of bounds
		pair = gene_order[start + size - 1] + gene_order[start + size]
		if pair not in split_gene_pairs:
			split_gene_pairs[pair] = True
			new_pairs += 1

	# Step 2: Add neighboring pairs within the deletion
	deletion = gene_order[start:start + size]
	for i in range(len(deletion) - 1):
		pair = deletion[i] + deletion[i + 1]
		if pair not in used_gene_pairs:
			used_gene_pairs[pair] = True
			new_pairs += 1

	return new_pairs

#==========================================================
#==========================================================
def insertCommas(my_str: str, separate: int = 3) -> str:
	"""
	Inserts commas into a string after every specified number of characters.

	Args:
		my_str (str): The string to modify.
		separate (int): The number of characters between each comma. Default is 3.

	Returns:
		str: The modified string with commas inserted.
	"""
	# Use textwrap.wrap to split the string into chunks of `separate` length
	chunks = textwrap.wrap(my_str, separate)
	# Join the chunks with commas
	return ','.join(chunks)
assert insertCommas('ABCDEF', 2) == "AB,CD,EF"
assert insertCommas('ABCDE', 3) == "ABC,DE"

#==========================================================
#==========================================================
def generate_fib_answer_variations(gene_order: list[str]) -> list[str]:
	"""
	Generates various answer formats based on the original list of genes.

	Args:
		gene_order (list[str]): The original list of genes.

	Returns:
		list[str]: A sorted list of unique answer variations.
	"""
	# Generate the base answer by joining the original list of genes
	base_answer = ''.join(gene_order)

	# Generate various base versions
	base_versions = [
		base_answer,                        # Original gene order
		','.join(gene_order),               # Comma-separated
		insertCommas(base_answer, 3),       # Chunks of 3
		insertCommas(base_answer[::-1], 3)  # Chunks of 3 in reverse order
	]

	# Add the reversed versions of each base version
	all_variations = base_versions[:]
	for version in base_versions:
		all_variations.append(version[::-1])

	# Deduplicate and sort the results
	return sorted(set(all_variations))

#==========================================================
#==========================================================
def format_choice(gene_list: list[str]) -> str:
	"""
	Formats a gene order into a readable multiple-choice option with a monospace font for the gene sequence.

	Args:
		gene_list (list[str]): A list of genes in a specific order.

	Returns:
		str: A formatted choice string combining the gene sequence and gene description.
	"""
	# Monospace font using <span>
	gene_sequence = "<strong><span style='font-family: monospace;'>"
	if len(gene_list) >= 10:
		gene_sequence += f"{insertCommas(''.join(gene_list), 4)}</span></strong>"
	else:
		gene_sequence += f"{''.join(gene_list)}</span></strong>"
	gene_sequence += f":&nbsp;&nbsp; <i>gene order of {list2text(gene_list)}</i>"
	return gene_sequence

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
	answer_text = format_choice(answer_gene_order)

	# Convert the set of tuples to a list of formatted strings
	choices_list = [format_choice(list(choice)) for choice in choices_set]

	# Deduplicate and sort the results for consistent output
	choices_list = sorted(set(choices_list))

	return choices_list, answer_text
cl, a = generate_mc_distractors(list("ABCD"), 6)
assert len(cl) == 6
assert a == format_choice(list("ABCD"))
cl, a = generate_mc_distractors(list("ABCDE"), 8)
assert len(cl) == 8, f"Expected 8 choices, got {len(cl)}."
assert a == format_choice(list("ABCDE")), "Expected correct answer not obtained"

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
	background = generate_background_for_deletions(args.num_genes, args.table)
	steps = get_deletion_mutant_steps()

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

	# Generate an HTML table if the table option is enabled
	if args.table is True:
		print("Making TABLE")
		table = make_html_table(answer_gene_order, deletions_list, deletion_colors)
	else:
		print("Skipping TABLE")
		table = ''

	# Create the question text based on the original and deleted genes
	print('write_question_text()')
	question = write_question_text(answer_gene_order, deletions_list, deletion_colors)

	# Combine the question and table (if available) into the question text
	question_text = background + table + question + steps

	# Format the question and answer into the final output structure
	if args.question_type == 'fib':
		# Collect all possible answer variations
		print('generate_fib_answer_variations()')
		answers_list = generate_fib_answer_variations(answer_gene_order)
		complete_question = bptools.formatBB_FIB_Question(N, question_text, answers_list)
	else:
		# Collect all possible distractor variations
		print('generate_mc_distractors()')
		choices_list, answer_text = generate_mc_distractors(answer_gene_order, args.num_choices)
		complete_question = bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)

	return complete_question

#=====================
def parse_arguments():
	"""
	Parses command-line arguments for the script.

	Defines and handles all arguments for the script, including:
	- `duplicates`: The number of questions to generate.
	- `num_choices`: The number of answer choices for each question.
	- `question_type`: Type of question (numeric or multiple choice).

	Returns:
		argparse.Namespace: Parsed arguments with attributes `duplicates`,
		`num_choices`, and `question_type`.
	"""
	# Initialize argument parser for command-line options
	parser = bptools.make_arg_parser(description="Generate questions.")
	parser = bptools.add_choice_args(parser, default=5)

	# Argument to specify the number of genes to delete on the chromosome
	parser.add_argument(
		'-g', '--num-genes', metavar='#', type=int, dest='num_genes',
		help='number of deleted genes on the chromosome', default=5)

	# Create a mutually exclusive group for enabling or disabling table display
	table_group = parser.add_mutually_exclusive_group()
	table_group.add_argument(
		'-T', '--table', dest='table', action='store_true',
		help='Enable table display in the output'
	)
	table_group.add_argument(
		'-F', '--free', '--no-table', dest='table', action='store_false',
		help='Disable table display in the output'
	)
	# Set the default behavior for the `table` argument (enabled by default)
	parser.set_defaults(table=True)

	# Create a mutually exclusive group for question type and make it required
	parser = bptools.add_question_format_args(
		parser,
		types_list=['fib', 'mc'],
		required=False,
		default='mc'
	)

	args = parser.parse_args()

	# Validate the number of genes, ensuring it's within the acceptable range
	if args.num_genes < 4:
		raise ValueError("Sorry, you must have at least 4 genes for this program")
	if args.num_genes > 20:
		raise ValueError("Sorry, you can have at most 20 genes for this program")

	max_choices = math.factorial(args.num_genes - 1)  # Fixing the first gene, permute the rest
	if args.num_choices > max_choices:
		raise ValueError(
			f"Cannot generate {args.num_choices} choices with {args.num_genes} genes. Maximum possible is {max_choices}."
		)

	return args

#==========================
# Main program execution starts here
#==========================
def main():
	args = parse_arguments()
	table_str = "TABLE" if args.table else "FREE"
	outfile = bptools.make_outfile(
		None,
		f"{args.num_genes:02d}_genes",
		table_str,
		args.question_type.upper()
	)
	bptools.collect_and_write_questions(write_question, args, outfile)

if __name__ == '__main__':
	main()
