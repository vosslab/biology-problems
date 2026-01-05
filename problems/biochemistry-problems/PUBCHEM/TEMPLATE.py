#!/usr/bin/env python3

# external python/pip modules
import os
import random
import argparse

# local repo modules
import bptools

#======================================
#======================================
def get_question_text():
	return "This is a hard question?"

#======================================
#======================================
def generate_choices(num_choices) -> (list, str):
	# Define possible choices and wrong choices
	choices_list = [
		'competitive inhibitor',
		'non-competitive inhibitor',
		]
	answer_text = random.choice(choices_list)
	wrong_choices_list = [
		'molecular stopper',
		'metabolic blocker',
		]
	random.shuffle(wrong_choices_list)
	choices_list.extend(wrong_choices_list[:1])

	# Shuffle choices for presentation
	random.shuffle(choices_list)

	return choices_list, answer_text

#======================================
#======================================
def generate_complete_question(N: int, num_choices: int) -> str:

	# Add more to the question based on the given letters
	question_text = get_question_text()

	# Choices and answers
	choices_list, answer_text = generate_choices(num_choices)

	# Complete the question formatting
	complete_question = bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)
	return complete_question

#======================================
#======================================
def main():
	# Define argparse for command-line options
	parser = argparse.ArgumentParser(description="Generate questions.")
	parser.add_argument('-d', '--duplicates', type=int, default=95, help="Number of questions to create.")
	parser.add_argument('-n', '--num_choices', type=int, default=5, help="Number of choices to create.")
	args = parser.parse_args()

	# Output file setup
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print(f'writing to file: {outfile}')

	# Create and write questions to the output file
	with open(outfile, 'w') as file:
		N = 0
		for d in range(args.duplicates):
			N += 1
			bbformat = generate_complete_question(N, args.num_choices)
			if bbformat is None:
				N -= 1
				continue
			file.write(bbformat)
	bptools.print_histogram()
	print(f'saved {N} questions to {outfile}')


#======================================
#======================================
if __name__ == '__main__':
	main()
