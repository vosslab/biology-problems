#!/usr/bin/env python3
# ^^ Specifies the Python3 environment to use for script execution

import sys
import random
import copy

# Import external modules (pip-installed)
# No external modules are used here currently

# Import local modules from the project
# Provides custom functions, such as question formatting and other utilities
import bptools
import seqlib


def complement(seq):
	newseq = copy.copy(seq)
	newseq = newseq.replace('A', 'x')
	newseq = newseq.replace('T', 'A')
	newseq = newseq.replace('x', 'T')
	newseq = newseq.replace('G', 'x')
	newseq = newseq.replace('C', 'G')
	newseq = newseq.replace('x', 'C')
	return newseq
	#return newseq[::-1]

def flip(seq):
	newseq = copy.copy(seq)
	return newseq[::-1]

def oneLetter(choice):
	if choice[1] == choice[2]:
		question = complement(choice[2])+"NNN"
	else:
		question = "NNN"+complement(choice[0])
	return question

def threeLetters(choice):
	if random.random() < 0.5:
		question = "NNN"+flip(complement(choice))
	else:
		question = flip(complement(choice))+"NNN"
	return question

def fiveLetters(choice):
	if random.random() < 0.5:
		question = "NNN"+flip(complement(choice))
	else:
		question = flip(complement(choice))+"NNN"
	nt = random.choice(list(choice))
	compl = complement(nt)
	question = nt + question + compl
	return question


def write_question(N):
	nt1 = random.choice(('A', 'C', 'T', 'G'))
	nt2 = complement(nt1)

	matching_list = []
	matching_list.append(nt1+nt1+nt2)
	matching_list.append(nt1+nt2+nt2)
	matching_list.append(nt2+nt2+nt1)
	matching_list.append(nt2+nt1+nt1)
	random.shuffle(matching_list)

	answers_list = []
	unusedchoices = copy.copy(matching_list)

	match1 = unusedchoices.pop(0)
	answer1 = oneLetter(match1)
	answers_list.append(answer1)

	match2 = unusedchoices.pop(0)
	answer2 = threeLetters(match2)
	answers_list.append(answer2)

	match3 = unusedchoices.pop(0)
	answer3 = fiveLetters(match3)
	answers_list.append(answer3)

	match4 = unusedchoices.pop(0)
	r = random.randint(1,3)
	if r == 1:
		answer4 = oneLetter(match4)
	elif r == 2:
		answer4 = threeLetters(match4)
	elif r == 3:
		answer4 = fiveLetters(match4)
	else:
		sys.exit(1)
	answers_list.append(answer4)

	answers_table_list = []
	for answer in answers_list:
		if len(answer) == 6:
			answer_table = seqlib.Single_Strand_Table(answer, fivetothree=True, separate=3)
		else:
			answer_table = seqlib.Single_Strand_Table(answer, fivetothree=True, separate=4)
		answers_table_list.append(answer_table)

	matching_table_list = []
	for match in matching_list:
		match_table = seqlib.Single_Strand_Table_No_Primes(match, separate=4)
		matching_table_list.append(match_table)

	question_text = ''
	question_text += "<p>The following numbered sequences only contains half of a palindromic sequence.</p> "
	question_text += "<p>Match the correct lettered sequence that would finish and replace "
	question_text += "the '<strong>N</strong>'s in the sequence to make them palindromes.</p> "
	question_text += "<p>Letters will be used exactly once.</p> "

	bbformat = bptools.formatBB_MAT_Question(N, question_text, answers_table_list, matching_table_list)
	return bbformat

def write_question_wrapper(N, args):
	return write_question(N)


#===========================================================
def parse_arguments():
	parser = bptools.make_arg_parser(description="Generate palindrome matching questions.")
	args = parser.parse_args()
	return args


#===========================================================
def main():
	args = parse_arguments()
	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question_wrapper, args, outfile)

#===========================================================
#===========================================================
# This block ensures the script runs only when executed directly
if __name__ == '__main__':
	# Call the main function to run the program
	main()

## THE END
