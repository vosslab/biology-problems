#!/usr/bin/env python

import sys
import seqlib
import random
import restrictlib

#================================================
def makeFillInBlankQuestion(enzyme_class, question_number=12):
	name = restrictlib.html_monospace(enzyme_class.__name__)
	cut_description = restrictlib.html_monospace(restrictlib.format_enzyme(enzyme_class))

	question = "blank {0}. ".format(question_number)
	question += "The restriction enzyme <b>{0}</b> cuts the sequence: {1}. ".format(name, cut_description)
	question += "What is the sequence (in the 5' to 3' direction) of the "
	question += "single-stranded nucleotide overhang region after cleavage? "
	print(question)

	answer = enzyme_class.ovhgseq
	print("A. {0}".format(answer))
	print("B. 5'-{0}-3'".format(answer))
	return


#================================================
def makeMultipleChoiceQuestion(enzyme_class, question_number=13):
	charlist = list("ABCDEFGHJKMPQRSTWXYZ")
	name = restrictlib.html_monospace(enzyme_class.__name__)
	cut_description = restrictlib.html_monospace(restrictlib.format_enzyme(enzyme_class))
	
	question = "{0}. ".format(question_number)
	question += "The restriction enzyme <b>{0}</b> cuts the sequence: {1}. ".format(name, cut_description)
	question += "Which one of the following sequences is the "
	question += "single-stranded nucleotide overhang region after cleavage? "

	#A. 5'-TGCA-3' B. 5'-CTGCA-3' C. 5'-TGCAG-3' D. 5'-ACGT-3'
	choices = []
	#print(enzyme_class.ovhgseq)
	#print(enzyme_class.site)
	#print(enzyme_class.elucidate())

	shift = (len(enzyme_class.site) - len(enzyme_class.ovhgseq))//2
	#print(shift)

	answer = ("5'-{0}-3'".format(enzyme_class.ovhgseq))
	choices.append(answer)

	inverse = ("5'-{0}-3'".format(seqlib.flip(enzyme_class.ovhgseq)))
	choices.append(inverse)

	expanded1 = ("5'-{0}-3'".format(enzyme_class.site[shift:]))
	choices.append(expanded1)

	expanded2 = ("5'-{0}-3'".format(enzyme_class.site[:-shift]))
	choices.append(expanded2)

	expandflip1 = ("5'-{0}-3'".format(seqlib.flip(enzyme_class.site[shift:])))
	choices.append(expandflip1)

	expandflip2 = ("5'-{0}-3'".format(seqlib.flip(enzyme_class.site[:-shift])))
	choices.append(expandflip2)

	#print(choices)
	choices = list(set(choices))
	#print(choices)
	if len(choices) > 5:
		a = choices.pop()
		if a == answer:
			choices.pop()
			choices.append(answer)
	try:
		choices.remove("5'--3'")
	except ValueError:
		pass

	#print(choices)
	random.shuffle(choices)
	#print(choices)

	if len(choices) <= 3:
		return None

	print(question)
	for i in range(len(choices)):
		ltr = charlist[i]
		choice = choices[i]
		prefix = ""
		if choice == answer:
			prefix = "*"
		print("{0}{1}. {2}".format(prefix, ltr, choice))


if __name__ == '__main__':
	if len(sys.argv) >= 2:
		multiple_choice = True
	else:
		multiple_choice = False

	enzymes = restrictlib.get_enzyme_list()
	#print(len(enzymes))
	#enzyme_class = restrictlib.random_enzyme_with_overhang(enzymes)

	random.shuffle(enzymes)
	
	question_number = 1
	for enzyme_name in enzymes:
		enzyme_class = restrictlib.enzyme_name_to_class(enzyme_name)
		overhang = enzyme_class.overhang()
		if not overhang.endswith('overhang'):
			continue
		if multiple_choice is False:
			makeFillInBlankQuestion(enzyme_class, question_number)
		else:
			makeMultipleChoiceQuestion(enzyme_class, question_number)
		question_number += 1
		#sys.exit(1)
		print("")



