#!/usr/bin/env python3

import random

import bptools

"""
77. The tetraploid number of a species is 4n = 16. How many chromosomes would present in the gametes of this species?
A. 3
B. 4
C. 6
D. 8
E. 16
"""

"""
Specific terms are triploid (3 sets), tetraploid (4 sets), pentaploid (5 sets),
hexaploid (6 sets), heptaploid[2] or septaploid[3] (7 sets), octoploid (8 sets),
nonaploid (9 sets), decaploid (10 sets), undecaploid (11 sets), dodecaploid (12 sets),
tridecaploid (13 sets), tetradecaploid (14 sets), etc.[29][30][31][32]

Some higher ploidies include hexadecaploid (16 sets), dotriacontaploid (32 sets), and tetrahexacontaploid (64 sets)
"""

ploidies = [4, 6, 8, 10, 12, 14, 16]
polyploid_names = {
	4: 'a tetraploid',
	6: 'a hexaploid',
	8: 'an octaploid',
	10: 'a decaploid',
	12: 'a dodecaploid',
	14: 'a tetradecaploid',
	16: 'a hexadecaploid',
	18: 'an octadecaploid',
	32: 'a dotriacontaploid',
	64: 'a tetrahexacontaploid'
}
monoploid_sizes = [4, 5, 6, 7, 8, 9, 10, 11]

def makeQuestion(N, ploidy, monoploid):
	total_chromosomes = monoploid * ploidy
	if total_chromosomes % 2 == 1:
		#odd number -> bad things
		return None
	gametes = total_chromosomes // 2
	if gametes == monoploid:
		return None

	choice_dict = {}
	answer = '{0} chromosomes'.format(gametes)
	choice_dict[gametes] = answer
	#===========
	number = ploidy
	wrong = '{0} chromosomes'.format(number)
	choice_dict[number] = wrong
	#===========
	number = ploidy*2
	wrong = '{0} chromosomes'.format(number)
	choice_dict[number] = wrong
	#===========
	number = ploidy // 2
	wrong = '{0} chromosomes'.format(number)
	choice_dict[number] = wrong
	#===========
	number = monoploid
	wrong = '{0} chromosomes'.format(number)
	choice_dict[number] = wrong
	#===========
	number = monoploid*2
	wrong = '{0} chromosomes'.format(number)
	choice_dict[number] = wrong
	#===========
	number = gametes // 2
	wrong = '{0} chromosomes'.format(number)
	choice_dict[number] = wrong
	#===========
	number = total_chromosomes
	wrong = '{0} chromosomes'.format(number)
	choice_dict[number] = wrong
	#===========
	number = total_chromosomes * 2
	wrong = '{0} chromosomes'.format(number)
	choice_dict[number] = wrong

	numbers = list(choice_dict.keys())
	while len(numbers) > 5:
		random.shuffle(numbers)
		num = numbers.pop()
		if num == gametes:
			numbers.append(num)
		else:
			del choice_dict[num]
	numbers.sort()
	choices_list = []
	for n in numbers:
		choices_list.append(choice_dict[n])

	question = ""
	question += "<p>A {0} plant species is found to be ".format(polyploid_names[ploidy])
	question += '{0}n = {1} chromosomes.</p> '.format(ploidy, total_chromosomes)
	question += '<h5>How many chromosomes would present in the gametes of this species?</h5>'
	if random.random() < 0.5:
		question += "<p><i>Note: {0}/{1} = {2} and {0}/2 = {3}</i></p>".format(total_chromosomes, ploidy, monoploid, gametes)
	else:
		question += "<p><i>Note: {0}/2 = {3} and {0}/{1} = {2}</i></p>".format(total_chromosomes, ploidy, monoploid, gametes)

	bb_question = bptools.formatBB_MC_Question(N, question, choices_list, answer)
	return bb_question

def write_question_batch(start_num: int, args) -> list:
	questions = []
	remaining = None
	if args.max_questions is not None:
		remaining = args.max_questions - (start_num - 1)
		if remaining <= 0:
			return questions
	N = start_num
	for ploidy in ploidies:
		for monoploid in monoploid_sizes:
			bb_question = makeQuestion(N, ploidy, monoploid)
			if bb_question is None:
				continue
			questions.append(bb_question)
			N += 1
			if remaining is not None and len(questions) >= remaining:
				return questions
	return questions

def parse_arguments():
	parser = bptools.make_arg_parser(
		description="Generate polyploid gamete questions.",
		batch=True
	)
	args = parser.parse_args()
	return args

def main():
	args = parse_arguments()
	outfile = bptools.make_outfile(None)
	questions = bptools.collect_question_batches(write_question_batch, args)
	bptools.write_questions_to_file(questions, outfile)

if __name__ == '__main__':
	main()
