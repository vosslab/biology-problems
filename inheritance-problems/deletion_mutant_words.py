#!/usr/bin/env python3

import os
import math
import time
import random
import argparse

import bptools
import deletionlib


#==========================================================
#==========================================================
def get_anagrams_for_word(query_word: str, wordlist_path: str = None) -> list[str]:
	"""
	Find all anagrams of a given word in a word list file.
	"""
	if wordlist_path is None:
		git_path = bptools.get_git_root()
		large_file = "enable2k.txt"
		wordlist_path = os.path.join(git_path, "data", large_file)

	target = query_word.strip()
	if not target:
		return []

	target_norm = target.lower()
	target_len = len(target_norm)
	target_key = ''.join(sorted(target_norm))

	anagrams: list[str] = []

	with open(wordlist_path, 'r', encoding='ascii') as handle:
		for line in handle:
			word = line.strip().lower()
			if not word or word.startswith('#'):
				continue

			if len(word) != target_len:
				continue

			key = ''.join(sorted(word))
			if key == target_key:
				anagrams.append(word)

	return anagrams

#==========================================================
#==========================================================
def find_anagram_words(wordlist_path: str, min_anagrams: int, word_length: int, first_letter: bool = False) -> list:
	"""
	Find words of a given length that have at least a given number of anagrams.
	"""
	anagram_groups: dict = {}
	with open(wordlist_path, 'r', encoding='ascii') as handle:
		for line in handle:
			word = line.strip()
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
	gene_order_word = random.choice(word_bank)
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
	git_path = bptools.get_git_root()
	small_file = "SCOWL-words_with_friends-intersection.txt"
	small_path = os.path.join(git_path, "data", small_file)
	#large_file = "words_with_friends_dictionary.txt"
	large_file = "enable2k.txt"
	large_path = os.path.join(git_path, "data", large_file)

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
def generate_mc_distractors(answer_gene_order: list[str], num_choices: int):
	"""
	Generates multiple-choice distractors for a gene order question.

	Args:
		answer_gene_order (list[str]): The correct order of genes.
		num_choices (int): The total number of multiple-choice options, including the correct answer.

	Returns:
		tuple[list[str], str]: A list of formatted multiple-choice options and the correct answer.
	"""

	answer_word = ''.join(answer_gene_order)
	anagrams = get_anagrams_for_word(answer_word)
	if 0 < len(anagrams) < 10:
		print(f"ANAGRAMS: {', '.join(anagrams)}")
	first_letter = answer_gene_order[0]
	good_anagrams = []
	for anagram in anagrams:
		if anagram.startswith(first_letter):
			good_anagrams.append(anagram)
	if 0 < len(good_anagrams) < 10:
		print(f"GOOD ANAGRAMS: {', '.join(good_anagrams)}")
	print(f"Found {len(anagrams)} anagrams and {len(good_anagrams)} good anagrams for our gene word {answer_word}.\n\n")

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
	question = deletionlib.write_question_text(answer_gene_order, deletions_list, deletion_colors)

	# Combine the question and table (if available) into the question text
	question_text = background + table + question + steps

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
	parser = argparse.ArgumentParser(description="Generate questions.")

	parser.add_argument(
		'-d', '--duplicates', metavar='#', type=int, dest='duplicates',
		help='Number of duplicate runs to do or number of questions to create', default=1
	)
	parser.add_argument(
		'-c', '--num_choices', metavar='#', type=int, default=5,
		help="Number of choices to create."
	)

	# Argument to specify the number of genes to delete on the chromosome
	parser.add_argument(
		'-g', '--num-genes', metavar='#', type=int, dest='num_genes',
		help='number of deleted genes on the chromosome', default=5)

	# Create a mutually exclusive group for question type and make it required
	question_group = parser.add_mutually_exclusive_group(required=True)
	question_group.add_argument(
		'-t', '--type', dest='question_type', type=str, choices=('fib', 'mc'),
		help='Set the question type: fib (numeric) or mc (multiple choice)'
	)
	question_group.add_argument(
		'-m', '--mc', dest='question_type', action='store_const', const='mc',
		help='Set question type to multiple choice'
	)
	question_group.add_argument(
		'-f', '--fib', dest='question_type', action='store_const', const='fib',
		help='Set question type to fill-in-the-blank (fib)'
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
if __name__ == '__main__':
	# Parse arguments from the command line
	args = parse_arguments()

	# Setup output file name
	script_name = os.path.splitext(os.path.basename(__file__))[0]
	outfile = (
		f'bbq-{script_name}'
		f'-{args.num_genes:02d}_genes'
		f'-words'
		f'-{args.question_type.upper()}'
		'-questions.txt'
	)
	print(f'Writing to file: {outfile}')

	# Open the output file and generate questions
	with open(outfile, 'w') as f:
		N = 1  # Question number counter
		for _ in range(args.duplicates):
			# Generate and write each question
			complete_question = write_question(N, args)
			if complete_question is not None:
				N += 1
				f.write(complete_question)

	print(f'Wrote to file: {outfile}')
	if args.question_type == 'mc':
		bptools.print_histogram()

