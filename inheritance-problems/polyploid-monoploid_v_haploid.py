#!/usr/bin/env python3

import random

"""
82. A certain plant is found to be an octoploid (8n) with 40 chromosomes, what are the monoploid (m) and haploid (h) numbers? Note: 40/8 = 5 and 40/2 = 20.
A. m=5; h=5
B. m=5; h=20
C. m=20; h=5
D. m=20; h=20
"""

"""
Specific terms are triploid (3 sets), tetraploid (4 sets), pentaploid (5 sets), hexaploid (6 sets), heptaploid[2] or septaploid[3] (7 sets), octoploid (8 sets), nonaploid (9 sets), decaploid (10 sets), undecaploid (11 sets), dodecaploid (12 sets), tridecaploid (13 sets), tetradecaploid (14 sets), etc.[29][30][31][32] Some higher ploidies include hexadecaploid (16 sets), dotriacontaploid (32 sets), and tetrahexacontaploid (64 sets)
"""

import bptools

ploidies = [4, 6, 8, 10, 12, 14, 16]
polyploid_names = {
	3: 'a triploid',
	4: 'a tetraploid',
	5: 'a pentaploid',
	6: 'a hexaploid',
	7: 'a heptaploid',
	8: 'an octaploid',
	9: 'a nonaploid',
	10: 'a decaploid',
	11: 'a undecaploid',
	12: 'a dodecaploid',
	13: 'a tridecaploid',
	14: 'a tetradecaploid',
	15: 'a pentadecaploid',
	16: 'a hexadecaploid',
	17: 'a heptadecaploid',
	18: 'an octadecaploid',
	32: 'a dotriacontaploid',
	64: 'a tetrahexacontaploid'
}
monoploid_sizes = [4, 5, 6, 7, 8, 9, 10, 11]

#=====================
def write_question_batch(N: int, args) -> list[str]:
	questions = []
	question_num = N
	for ploidy in ploidies:
		for monoploid in monoploid_sizes:
			total_chromosomes = monoploid * ploidy
			haploid = total_chromosomes // 2
			if haploid == monoploid:
				continue
			question = ""
			question += "<p>A certain plant is found to be "
			question += polyploid_names[ploidy] + ' '
			question += '({0}n) '.format(ploidy)
			question += "with {0} chromosomes in total.</p>".format(total_chromosomes)
			question += '<h5>What are the monoploid (m) and haploid (h) numbers for this plant?</h5>'
			if random.random() < 0.5:
				question += "<p><i>Note: {0}/{1} = {2} and {0}/2 = {3}</i></p>".format(total_chromosomes, ploidy, monoploid, haploid)
			else:
				question += "<p><i>Note: {0}/2 = {3} and {0}/{1} = {2}</i></p>".format(total_chromosomes, ploidy, monoploid, haploid)

			choices = []
			answer = '<p>monoploid, m = {0} and haploid, h = {1}</p>'.format(monoploid, haploid)
			choices.append(answer)
			wrong = '<p>monoploid, m = {0} and haploid, h = {1}</p>'.format(haploid, monoploid)
			choices.append(wrong)
			wrong = '<p>monoploid, m = {0} and haploid, h = {1}</p>'.format(monoploid, monoploid)
			choices.append(wrong)
			wrong = '<p>monoploid, m = {0} and haploid, h = {1}</p>'.format(haploid, haploid)
			choices.append(wrong)
			wrong = '<p>monoploid, m = {0} and haploid, h = {1}</p>'.format(total_chromosomes, monoploid)
			choices.append(wrong)
			wrong = '<p>monoploid, m = {0} and haploid, h = {1}</p>'.format(total_chromosomes, haploid)
			choices.append(wrong)

			random.shuffle(choices)
			complete_question = bptools.formatBB_MC_Question(question_num, question, choices, answer)
			questions.append(complete_question)
			question_num += 1
	return questions

#=====================
def parse_arguments():
	parser = bptools.make_arg_parser(
		description="Generate monoploid vs haploid questions.",
		batch=True
	)
	args = parser.parse_args()
	return args

#=====================
def main():
	args = parse_arguments()
	outfile = bptools.make_outfile()
	questions = bptools.collect_question_batches(write_question_batch, args)
	bptools.write_questions_to_file(questions, outfile)

#=====================
if __name__ == '__main__':
	main()
