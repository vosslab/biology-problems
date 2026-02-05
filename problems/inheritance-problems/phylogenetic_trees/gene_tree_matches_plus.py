#!/usr/bin/env python3

import copy
import time
import random
#local
import bptools
bptools.allow_no_click_div = False
bptools.allow_insert_hidden_terms = False

from treelib import tools
from treelib import lookup

debug = False

cache_all_treecode_cls_list = []

### TODO
# get most dissimilar in find SAME for quesiton and answer
# get most dissimilar in find DIFFERENT for quesiton and wrong choices

#===========================================================
#===========================================================
#===========================================================
#===========================================================
def generate_treecodes_lists(ordered_taxa, num_choices):
	"""
	Generate two lists of tree codes:
	1. A list of tree codes representing "same" phylogenetic trees.
	2. A list of tree codes representing "different" phylogenetic trees.
	"""
	# Determine the number of leaves from the length of the ordered taxa
	num_leaves = len(ordered_taxa)

	#===========================================
	# Generate the "same" tree codes list
	#===========================================
	# Step 1: Get a random base tree code for the given number of leaves
	same_base_treecode_cls = lookup.get_random_base_tree_code_for_leaf_count(num_leaves)
	if debug:
		same_base_treecode_cls.print_ascii_tree()

	# Step 2: Generate all inner-node permutations of the base tree code
	same_treecode_cls_list = lookup.get_all_inner_node_permutations_from_tree_code(same_base_treecode_cls)

	# Step 3: Limit the list to the desired number of choices
	same_treecode_cls_list = same_treecode_cls_list[:num_choices]

	# Debug: Print the tree codes in the "same" list
	if debug:
		for i, treecode_cls in enumerate(same_treecode_cls_list):
			print(f'SAME {i+1}: {treecode_cls.tree_code_str}')

	# Step 4: Replace the taxa in each tree code with the ordered taxa
	same_replaced_treecode_cls_list = []
	for i, treecode_cls in enumerate(same_treecode_cls_list):
		replaced_treecode_cls = lookup.replace_taxa_letters(treecode_cls, ordered_taxa)
		same_replaced_treecode_cls_list.append(replaced_treecode_cls)

	#===========================================
	# Generate all unique tree codes
	#===========================================
	global cache_all_treecode_cls_list
	if len(cache_all_treecode_cls_list) == 0:
		# If the cache is empty, generate all tree codes
		if debug:
			print("calculating all_permuted_tree_codes")

		all_treecode_cls_list = lookup.get_all_taxa_permuted_tree_codes_for_leaf_count(num_leaves)

		if debug:
			print("shuffling all_permuted_tree_codes")

		random.shuffle(all_treecode_cls_list)

		# Remove duplicate tree codes
		purge_start = time.time()
		if debug:
			print("purging duplicates")
		unique_treecode_cls_list = list(set(all_treecode_cls_list))

		# Debug: Measure the time taken to purge duplicates
		if time.time() - purge_start > 10:
			if debug:
				print(f"done purging duplicates in {time.time() - purge_start:.1f} seconds")
				print(f"unique {len(unique_treecode_cls_list)} treecodes, down from all {len(all_treecode_cls_list)}")

		# Cache the unique tree codes for future use
		cache_all_treecode_cls_list = copy.copy(unique_treecode_cls_list)
	else:
		# Load the cached unique tree codes
		if debug:
			print("loading unique_treecode_cls_list")
		unique_treecode_cls_list = copy.copy(cache_all_treecode_cls_list)

	#===========================================
	# Generate the "different" tree codes list
	#===========================================
	# Step 1: Sort the unique tree codes by similarity to the base tree code
	sorted_treecode_cls_list = lookup.sort_treecodes_by_taxa_distances(unique_treecode_cls_list, same_base_treecode_cls)
	if debug:
		print(f"sorted {len(sorted_treecode_cls_list)} treecodes, down from unique {len(unique_treecode_cls_list)}")

	# Step 2: Replace taxa in the sorted tree codes and generate permutations
	diff_replaced_treecode_cls_list = []
	for i, treecode_cls in enumerate(sorted_treecode_cls_list[:num_choices]):
		# Generate a random inner-node permutation for the tree code
		permuted_treecode_cls = lookup.get_random_inner_node_permutation_from_tree_code(treecode_cls)

		# Debug: Print the "different" tree codes
		if debug:
			print(f'DIFF {i+1}: {permuted_treecode_cls.tree_code_str}')

		# Replace the taxa with the ordered taxa
		replaced_treecode_cls = lookup.replace_taxa_letters(permuted_treecode_cls, ordered_taxa)
		diff_replaced_treecode_cls_list.append(replaced_treecode_cls)

	# Return both the "same" and "different" lists
	return same_replaced_treecode_cls_list, diff_replaced_treecode_cls_list

#===========================================================
#===========================================================
def get_background_statement() -> str:
	"""
	Returns a short paragraph on the importance of phylogenetic trees in genetics research.
	"""
	return (
		"<p><b>Phylogenetic trees</b> are fundamental tools in genetics research, "
		"enabling scientists to visualize evolutionary relationships "
		"among species, gene sequences, or populations. "
		"By tracing shared ancestry, these trees can provide valuable insights into genetic biodiversity. "
		"Applications of phylogenetic trees include tracking disease evolution, "
		"identifying conserved genetic sequences, and understanding speciation processes. "
		"Phylogenetic trees are indispensable for both theoretical and applied genetics.</p>"
	)

#===========================================================
#===========================================================
def find_diff_question(N, num_choices, same_treecode_cls_list, diff_treecode_cls_list, include_hint=False):
	"""
	Generate a question asking students to identify the different phylogenetic tree.
	"""
	# Ensure there are enough tree codes to form the question
	if len(same_treecode_cls_list) < num_choices:
		print("Not enough same tree codes for the find different question")
		return None

	# Randomly select a tree code to use as the reference tree for the question
	random.shuffle(same_treecode_cls_list)
	same_treecode_cls = same_treecode_cls_list.pop()  # The reference tree code for the question

	header = '<h2>Find the <span style="color: #ba372a;"><strong>DIFFERENT</strong></span> tree</h2>'

	# Include a background statement to provide context
	background_statement = get_background_statement()

	# Build the question statement introducing the reference tree
	question_statement = f'<p>The tree diagram below is a phylogenetic tree with {same_treecode_cls.num_leaves} leaves. '
	question_statement += 'This phylogenetic tree is affectionately named: '
	question_statement += f'"<i>{same_treecode_cls.tree_common_name}</i>".</p>'
	question_statement += same_treecode_cls.get_html_table()
	question_statement += '<p></p>'
	question_statement += f'<p>Among the {bptools.number_to_cardinal(num_choices)} phylogenetic trees displayed below, '
	question_statement += 'all but one have the same structure and '
	question_statement += 'represent the same evolutionary relationships as the tree above.</p>'
	question_statement += '<p>Your task is to identify the single '
	question_statement += '<span style="color: #ba372a;">different</span> phylogenetic tree '
	question_statement += 'that does NOT share the same structure or relationships as the reference tree above.</p>'
	question_statement += '<p></p>'
	question_statement += '<p>Which one of the following phylogenetic trees represents a '
	question_statement += '<span style="color: #ba372a;"><strong>DIFFERENT</strong></span> phylogenetic tree?</p>'

	hint_text = ""
	if include_hint:
		hint_text = (
			"<p><i>Hint: trees can be rotated at internal nodes without changing their meaning. "
			"Focus on branching order, not left/right orientation.</i></p>"
		)

	# Randomly select the correct "different" answer tree
	random.shuffle(diff_treecode_cls_list)
	answer_treecode_cls = diff_treecode_cls_list.pop()  # The "different" tree code

	# Initialize the list of HTML representations for the multiple-choice options
	html_choices_list = []

	# Add incorrect "same" choices (trees with the same structure)
	random.shuffle(same_treecode_cls_list)
	for treecode_cls in same_treecode_cls_list[:num_choices - 1]:
		html_treecode_table = treecode_cls.get_html_table(caption=False)
		html_choices_list.append(html_treecode_table)

	# Add the correct "different" choice
	answer_html_table = answer_treecode_cls.get_html_table(caption=False)
	html_choices_list.append(answer_html_table)

	# Remove duplicates from the choices and shuffle them for randomness
	html_choices_list = list(set(html_choices_list))
	random.shuffle(html_choices_list)

	# Combine the background, question statement, and choices into the full question
	full_statement = header + background_statement + question_statement + hint_text
	complete_question = bptools.formatBB_MC_Question(N, full_statement, html_choices_list, answer_html_table)

	# Print a debug message to indicate the question generation is complete
	print(f"Q{N} find_diff_question() is complete for {num_choices} choices")

	return complete_question

#===========================================================
#===========================================================
def find_same_question(N, num_choices, same_treecode_cls_list, diff_treecode_cls_list, include_hint=False):
	"""
	Generate a question asking students to identify the same phylogenetic tree.
	"""
	# Ensure there are enough tree codes to create the question
	if len(diff_treecode_cls_list) < num_choices:
		print("Not enough different tree codes for the find same question")
		return None

	# Randomly select the primary tree code for the question
	random.shuffle(same_treecode_cls_list)
	same_treecode_cls = same_treecode_cls_list.pop()  # The main tree for the question
	answer_treecode_cls = same_treecode_cls_list.pop()  # Correct answer among the choices

	header = '<h2>Find the <span style="color: #169179;"><strong>SAME</strong></span> tree</h2>'

	# Include a background statement on phylogenetic trees
	background_statement = get_background_statement()

	# Build the question statement introducing the phylogenetic tree
	question_statement = f'<p>The tree diagram below is a phylogenetic tree with {same_treecode_cls.num_leaves} leaves. '
	question_statement += 'This phylogenetic tree is affectionately called: '
	question_statement += f'"<i>{same_treecode_cls.tree_common_name}</i>".</p>'
	question_statement += same_treecode_cls.get_html_table()
	question_statement += '<p></p>'
	question_statement += '<p></p><p>Several phylogenetic trees are shown below, '
	question_statement += 'but only one has the SAME structure and '
	question_statement += 'represents the same relationships as the phylogenetic tree above.</p>'
	question_statement += '<p>Your task is to identify the single '
	question_statement += '<span style="color: #169179;">same</span> phylogenetic tree '
	question_statement += 'that shares the same structure and relationships as the reference tree above.</p>'
	question_statement += '<p></p>'
	question_statement += '<p>Which one of the following phylogenetic trees represents the '
	question_statement += '<span style="color: #169179;"><strong>SAME</strong></span> '
	question_statement += 'tree relationships or is equivalent to the phylogenetic tree above?</p>'

	hint_text = ""
	if include_hint:
		hint_text = (
			"<p><i>Hint: trees are equivalent if internal nodes can be rotated to match. "
			"Ignore the exact left/right placement of taxa.</i></p>"
		)

	# Initialize the list of HTML representations for the multiple-choice options
	html_choices_list = []
	# Add the incorrect choices (trees with different structures)
	random.shuffle(same_treecode_cls_list)
	for treecode_cls in diff_treecode_cls_list[:num_choices - 1]:
		html_treecode_table = treecode_cls.get_html_table(caption=False)
		html_choices_list.append(html_treecode_table)
	# Add the correct choice (answer)
	answer_html_table = answer_treecode_cls.get_html_table(caption=False)
	html_choices_list.append(answer_html_table)
	# Remove duplicates from the choices and shuffle them for randomness
	html_choices_list = list(set(html_choices_list))
	random.shuffle(html_choices_list)

	# Combine the background, question statement, and choices into the full question
	full_statement = header + background_statement + question_statement + hint_text
	complete_question = bptools.formatBB_MC_Question(N, full_statement, html_choices_list, answer_html_table)

	# Print a debug message and return the complete question
	print(f"Q{N} find_same_question() is complete for {num_choices} choices")
	return complete_question

#===========================================================
#===========================================================
def write_question(N, args):
	"""
	Generate a phylogenetic question based on the specified mode.
	"""
	if args.question_type != 'mc':
		raise ValueError("Only multiple-choice format is supported.")
	# Generate a sorted list of gene letters based on the number of leaves
	sorted_taxa = sorted(bptools.generate_gene_letters(args.num_leaves))

	# Generate all permutations of the sorted taxa letters, ensuring combination safety
	all_taxa_permutations = tools.get_comb_safe_taxa_permutations(sorted_taxa)

	# Randomize the order of permutations
	random.shuffle(all_taxa_permutations)

	# Select one specific taxa order for constructing the distance matrix
	ordered_taxa = all_taxa_permutations.pop()
	if debug:
		print('ordered_taxa=', ordered_taxa)

	# Generate lists of TreeCode objects for "same" and "different" trees
	same_treecode_cls_list, diff_treecode_cls_list = generate_treecodes_lists(ordered_taxa, args.num_choices)

	# Generate a question based on the specified mode ('same' or 'diff')
	if args.mode == 'same':
		# Find a "same" question where the student identifies the identical tree
		complete_question = find_same_question(
			N,
			args.num_choices,
			same_treecode_cls_list,
			diff_treecode_cls_list,
			include_hint=args.hint
		)
	else:
		# Find a "different" question where the student identifies the different tree
		complete_question = find_diff_question(
			N,
			args.num_choices,
			same_treecode_cls_list,
			diff_treecode_cls_list,
			include_hint=args.hint
		)

	# Return the formatted question
	return complete_question

#===========================================================
#===========================================================
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
	parser = bptools.make_arg_parser(description="Generate phylogenetic tree matching questions.")
	parser = bptools.add_choice_args(parser, default=5)
	parser = bptools.add_hint_args(parser)
	parser = bptools.add_question_format_args(
		parser,
		types_list=['mc'],
		required=False,
		default='mc'
	)
	parser.add_argument(
		'-l', '--leaves', '--num_leaves', type=int, dest='num_leaves',
		help='number of leaves in the gene tree', default=5)

	# MODE: same vs different (required, mutually exclusive shortcuts allowed)
	mode_group = parser.add_mutually_exclusive_group(required=True)
	mode_group.add_argument("--mode", dest="mode", type=str,
		choices=("same", "different"),
		help="Question mode: same or different")
	mode_group.add_argument("-S", "--same", dest="mode", action="store_const", const="same",
		help="Question mode: find same")
	mode_group.add_argument("-D", "--different", dest="mode", action="store_const", const="different",
		help="Question mode: find different")

	# DIFFICULTY: easy < medium < rigorous
	# Use one argument with choices, plus optional shortcuts if you want
	parser.add_argument("--difficulty", dest="difficulty", type=str,
		choices=("easy", "medium", "rigorous"), default="medium",
		help="Difficulty: easy, medium, or rigorous")

	# Optional difficulty shortcuts
	diff_group = parser.add_mutually_exclusive_group()
	diff_group.add_argument("-E", "--easy",      dest="difficulty", action="store_const", const="easy",
		help="Set difficulty to easy")
	diff_group.add_argument("-M", "--medium",    dest="difficulty", action="store_const", const="medium",
		help="Set difficulty to medium")
	diff_group.add_argument("-R", "--rigorous",  dest="difficulty", action="store_const", const="rigorous",
		help="Set difficulty to rigorous")
	parser.set_defaults(difficulty=None)

	args = parser.parse_args()

	if args.difficulty == "easy":
		args.num_choices = 5
		if args.mode == "same":
			args.num_leaves = 5
		elif args.mode == "different":
			args.num_leaves = 6
	elif args.difficulty == "medium":
		args.num_choices = 6
		if args.mode == "same":
			args.num_leaves = 6
		elif args.mode == "different":
			args.num_leaves = 7
	elif args.difficulty == "rigorous":
		args.num_choices = 8
		args.num_leaves = 8

	if args.num_leaves < 3:
		raise ValueError("Program requires a minimum of three (3) leaves to work")

	if args.num_leaves > 8:
		raise ValueError("Program not tested beyond eight (8) leaves")

	return args

#===========================================================
#===========================================================
def main():
	"""
	Main function that orchestrates question generation and file output.
	"""

	# Parse arguments from the command line
	args = parse_arguments()

	# Define output file name
	hint_mode = 'with_hint' if args.hint else 'no_hint'
	if args.difficulty is not None:
		difficulty_suffix = f"{args.difficulty.upper()}_level"
	else:
		difficulty_suffix = f"{args.num_leaves}_leaves-{args.num_choices}_choices"
	outfile = bptools.make_outfile(args.question_type.upper(),
		hint_mode,
		f"{args.mode.upper()}_mode",
		difficulty_suffix
	)

	# Collect and write questions using shared helper
	bptools.collect_and_write_questions(write_question, args, outfile)

#===========================================================
#===========================================================
if __name__ == '__main__':
	main()

## THE END
