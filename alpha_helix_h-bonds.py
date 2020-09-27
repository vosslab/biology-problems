#!/usr/bin/env python


import random


if __name__ == '__main__':
	amino_acid = random.randint(6,9)
	charlist = list("ABCDEFGHJKMPQRSTWXYZ")

	shift = 4
	answer = "{0:d} and {1:d}".format(amino_acid-shift,amino_acid+shift)
	choices = []
	choices.append(answer)

	for shift in (2,3,5):
		choice = "{0:d} and {1:d}".format(amino_acid-shift,amino_acid+shift)
		choices.append(choice)

	extra_choices = []
	for shift in (1,6,7,8):
		if shift >= amino_acid:
			continue
		choice = "{0:d} and {1:d}".format(amino_acid-shift,amino_acid+shift)
		extra_choices.append(choice)
	random.shuffle(extra_choices)
	choices.append(extra_choices.pop())
	random.shuffle(choices)
	
	question = "12. "
	question += "In a long &alpha;-helix, amino acid <b>number {0}</b> would form a hydrogen bond with which two other amino acids?".format(amino_acid)
	print(question)
	for i in range(5):
		prefix = ""
		ltr = charlist[i]
		choice = choices[i]
		if choice == answer:
			prefix = "*"
		print("{0}{1}. {2}".format(prefix, ltr, choice))

