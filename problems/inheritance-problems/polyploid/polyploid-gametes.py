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
	answer = f'{gametes} chromosomes'
	choice_dict[gametes] = answer
	#===========
	number = ploidy
	wrong = f'{number} chromosomes'
	choice_dict[number] = wrong
	#===========
	number = ploidy*2
	wrong = f'{number} chromosomes'
	choice_dict[number] = wrong
	#===========
	number = ploidy // 2
	wrong = f'{number} chromosomes'
	choice_dict[number] = wrong
	#===========
	number = monoploid
	wrong = f'{number} chromosomes'
	choice_dict[number] = wrong
	#===========
	number = monoploid*2
	wrong = f'{number} chromosomes'
	choice_dict[number] = wrong
	#===========
	number = gametes // 2
	wrong = f'{number} chromosomes'
	choice_dict[number] = wrong
	#===========
	number = total_chromosomes
	wrong = f'{number} chromosomes'
	choice_dict[number] = wrong
	#===========
	number = total_chromosomes * 2
	wrong = f'{number} chromosomes'
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
	question += f"<p>A {polyploid_names[ploidy]} plant species is found to be "
	question += f'{ploidy}n = {total_chromosomes} chromosomes.</p> '
	question += '<h5>How many chromosomes would present in the gametes of this species?</h5>'
	if random.random() < 0.5:
		question += f"<p><i>Note: {total_chromosomes}/{ploidy} = {monoploid} and {total_chromosomes}/2 = {gametes}</i></p>"
	else:
		question += f"<p><i>Note: {total_chromosomes}/2 = {gametes} and {total_chromosomes}/{ploidy} = {monoploid}</i></p>"

	bb_question = bptools.formatBB_MC_Question(N, question, choices_list, answer)
	return bb_question

def write_question(N: int, args) -> str:
	max_tries = 100
	for _ in range(max_tries):
		ploidy = random.choice(ploidies)
		monoploid = random.choice(monoploid_sizes)
		bb_question = makeQuestion(N, ploidy, monoploid)
		if bb_question is not None:
			return bb_question
	return None

def parse_arguments():
	parser = bptools.make_arg_parser(description="Generate polyploid gamete questions.")
	args = parser.parse_args()
	return args

def main():
	args = parse_arguments()
	outfile = bptools.make_outfile(None)
	bptools.collect_and_write_questions(write_question, args, outfile)

if __name__ == '__main__':
	main()
