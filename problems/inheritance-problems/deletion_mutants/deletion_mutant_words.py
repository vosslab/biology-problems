#!/usr/bin/env python3
# ^^ Specifies the Python3 environment to use for script execution

# Import built-in Python modules
import time
import random
import math

# Import external modules (pip-installed)
# No external modules are used here currently

# Import local modules from the project
# Provides custom functions, such as question formatting and other utilities
import bptools
import deletionlib

#==========================================================
#==========================================================
def get_anagrams_for_word(query_word: str, wordlist_path: str = None) -> set[str]:
	"""
	Find all anagrams of a given word in a word list file.

	Args:
		query_word (str): The word to find anagrams for.
		wordlist_path (str, optional): Path to the wordlist file.
			Defaults to 'enable2k.txt' under data directory.

	Returns:
		set[str]: Unique uppercase anagrams of the given word.
	"""
	# Determine default word list path
	if wordlist_path is None:
		large_file = "enable2k.txt"
		wordlist_path = bptools.get_repo_data_path(large_file)

	# Normalize the query word
	target = query_word.strip().upper()
	if not target:
		return set()

	target_len = len(target)
	target_key = ''.join(sorted(target))

	# Collect anagrams in a set for uniqueness
	anagram_set: set[str] = set()

	with open(wordlist_path, 'r', encoding='ascii') as handle:
		for line in handle:
			word = line.strip().upper()
			if not word or word.startswith('#'):
				continue
			if len(word) != target_len:
				continue
			if ''.join(sorted(word)) == target_key:
				anagram_set.add(word)

	return anagram_set

#==========================================================
#==========================================================
def find_anagram_words(wordlist_path: str, min_anagrams: int, word_length: int, first_letter: bool = False) -> list:
	"""
	Find words of a given length that have at least a given number of anagrams.
	"""
	anagram_groups: dict = {}
	with open(wordlist_path, 'r', encoding='ascii') as handle:
		for line in handle:
			word = line.strip().upper()
			if not word or word.startswith('#'):
				continue
			if len(word) != word_length:
				continue
			# skip words that have repeated letters
			if len(set(word)) != word_length:
				continue
			if first_letter is True:
				key = word[0] + ''.join(sorted(word[1:]))
			else:
				key = ''.join(sorted(word))
			if key not in anagram_groups:
				anagram_groups[key] = []
			anagram_groups[key].append(word)
	result_words: list = []
	for key in anagram_groups:
		group = anagram_groups[key]
		if len(group) - 1 >= min_anagrams:
			for word in group:
				result_words.append(word)
	return result_words

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
	answer_gene_order = generate_gene_list(num_genes)

	# Step 5: Generate deletions until all pairs are covered
	deletions_list = deletionlib.generate_deletions(answer_gene_order)

	return answer_gene_order, deletions_list

#==========================================================
#==========================================================
def generate_gene_list(num_genes: int) -> list[str]:
	"""
	Generates a list of genes of the specified size that forms a word
	Args:
		num_genes (int): The number of genes to include in the list.

	Returns:
		list[str]: A shuffled list of unique gene identifiers.
	"""
	min_word_bank_size = 10
	word_bank = get_gene_word_bank(num_genes, min_word_bank_size)
	print(f"Final word bank size of {len(word_bank)} words.\n")
	gene_order_word = random.choice(word_bank).upper()
	gene_list = list(gene_order_word)
	return gene_list

#==========================================================
#==========================================================
def get_gene_word_bank(num_genes: int, min_word_bank_size: int) -> list[str]:
	"""
	Build a word bank of candidate gene order words.

	Each word has length num_genes and has at least a minimum number
	of anagrams in the source word lists.

	Args:
		num_genes:
			Length of each candidate word.
		min_word_bank_size:
			Minimum number of candidate words required.

	Returns:
		A list of candidate words.

	Raises:
		ValueError:
			If no suitable word bank can be constructed.
	"""
	small_file = "SCOWL-words_with_friends-intersection.txt"
	small_path = bptools.get_repo_data_path(small_file)
	#large_file = "words_with_friends_dictionary.txt"
	large_file = "enable2k.txt"
	large_path = bptools.get_repo_data_path(large_file)

	for min_anagrams in (5, 4, 3, 2):
		print(
			f"DEBUG get_gene_word_bank: trying SMALL list, "
			f"min_anagrams={min_anagrams}, num_genes={num_genes}"
		)
		found_words = find_anagram_words(small_path, min_anagrams, num_genes, first_letter=True)
		print(
			f"DEBUG get_gene_word_bank: SMALL list, "
			f"min_anagrams={min_anagrams}, found_words={len(found_words)}"
		)
		if len(found_words) >= min_word_bank_size:
			print(
				f"DEBUG get_gene_word_bank: using SMALL list, "
				f"min_anagrams={min_anagrams}"
			)
			return found_words
		found_words = find_anagram_words(small_path, min_anagrams+1, num_genes, first_letter=False)
		print(
			f"DEBUG get_gene_word_bank: SMALL list, "
			f"min_anagrams={min_anagrams}, found_words={len(found_words)}"
		)
		if len(found_words) >= min_word_bank_size:
			print(
				f"DEBUG get_gene_word_bank: using SMALL list, "
				f"min_anagrams={min_anagrams}"
			)
			return found_words

	for min_anagrams in (4, 3, 2, 1, 0):
		print(
			f"DEBUG get_gene_word_bank: trying LARGE list, "
			f"min_anagrams={min_anagrams}, num_genes={num_genes}"
		)
		found_words = find_anagram_words(large_path, min_anagrams, num_genes)
		print(
			f"DEBUG get_gene_word_bank: LARGE list, "
			f"min_anagrams={min_anagrams}, found_words={len(found_words)}"
		)
		if len(found_words) >= min_word_bank_size:
			print(
				f"DEBUG get_gene_word_bank: using LARGE list, "
				f"min_anagrams={min_anagrams}"
			)
			return found_words

	raise ValueError("Could not find enough candidate words for gene list")


#==========================================================
#==========================================================
def generate_mc_distractors(answer_gene_order: list[str], num_choices: int):
	"""
	Generates multiple-choice distractors for a gene order question.

	Args:
		answer_gene_order (list[str]): The correct order of genes.
		num_choices (int): Total number of choices including the correct answer.

	Returns:
		tuple[list[str], str]: Formatted choice list and the correct answer.
	"""

	# Combine gene letters into a single word
	answer_word = ''.join(answer_gene_order).upper()

	# Find all anagrams for this word
	anagram_set = get_anagrams_for_word(answer_word)
	anagram_set.discard(answer_word)

	# Debug print for short anagram lists
	if 0 < len(anagram_set) < 15:
		print(f"ANAGRAMS: {', '.join(sorted(anagram_set))}")

	# Separate anagrams that share the same first letter
	first_letter = answer_gene_order[0].upper()
	good_anagrams = []
	other_anagrams = []
	for anagram in sorted(anagram_set):
		if anagram.startswith(first_letter):
			good_anagrams.append(anagram)
		else:
			other_anagrams.append(anagram)

	# Debug print for short good-anagram lists
	if 0 < len(good_anagrams) < 15:
		print(f"GOOD ANAGRAMS: {', '.join(good_anagrams)}")

	# Summary diagnostic output
	print(
		f"Found {len(anagram_set)} anagrams and {len(good_anagrams)} good anagrams "
		f"for {answer_word}.\n"
	)

	# Generate formatted correct answer text
	answer_formatted_text = deletionlib.format_choice(answer_gene_order)

	# Collect all formatted choices
	choices_list: list[str] = []

	# Fill the distractor choices from similar (good) anagrams
	for word in good_anagrams:
		formatted_choice_text = deletionlib.format_choice(list(word))
		choices_list.append(formatted_choice_text)
		if len(choices_list) == num_choices - 1:
			break

	# Fill remaining slots from other anagrams if needed
	if len(choices_list) < num_choices - 1:
		for word in other_anagrams:
			formatted_choice_text = deletionlib.format_choice(list(word))
			choices_list.append(formatted_choice_text)
			if len(choices_list) == num_choices - 1:
				break

	# Add the correct answer to the choice list
	choices_list.append(answer_formatted_text)

	# Deduplicate and sort for consistent output
	choices_list = sorted(set(choices_list))

	# Return the final set of choices and the correct answer
	return choices_list, answer_formatted_text

# Simple words with clear anagrams
# "stop" -> stop, post, spot, tops, opts, pots
cl, a = generate_mc_distractors(list("STOP"), 6)
assert len(cl) == 6, f"Expected 6 choices, got {len(cl)}"
assert a == deletionlib.format_choice(list("STOP")), "Answer formatting mismatch"
assert a in cl, "Correct answer not present"
assert len(cl) == len(set(cl)), "Duplicate choices found"

# "stone" -> stone, tones, seton, onset, steno, etons
cl, a = generate_mc_distractors(list("STONE"), 6)
assert len(cl) == 6, f"Expected 6 choices, got {len(cl)}"
assert a in cl, "Correct answer missing from choice list"

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
				deletion_colors, True, args.first_letter)

	# Combine the question and table into the question text
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
	outfile = bptools.make_outfile(
		None,
		f"{args.num_genes:02d}_genes",
		args.question_type.upper()
	)
	bptools.collect_and_write_questions(write_question, args, outfile)

#==========================================================
def parse_arguments():
	parser = bptools.make_arg_parser(description="Generate deletion mutant word questions.")
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
