#!/usr/bin/env python

import sys
import restrictlib


if __name__ == '__main__':
	if len(sys.argv) >= 2:
		multiple_choice = True
	else:
		multiple_choice = False

	enzymes = restrictlib.get_enzyme_list()
	enzyme_class = restrictlib.random_enzyme_with_overhang(enzymes)
	name = restrictlib.html_monospace(enzyme_class.__name__)
	cut_description = restrictlib.html_monospace(restrictlib.format_enzyme(enzyme_class))

	question = "12. The restriction enzyme <b>{0}</b> cuts the sequence: {1}. ".format(name, cut_description)
	if multiple_choice is False:
		question += "What is the sequence (in the 5' to 3' direction) of the "
	else:
		question += "Which one of the following sequences is the "
	question += "single-stranded nucleotide overhang region after cleavage? "
	print(question)
	
	answer = enzyme_class.ovhgseq
	if multiple_choice is False:
		print("A. {0}".format(answer))
		print("B. 5'-{0}-3'".format(answer))
		sys.exit(0)

	choices = []


	#A. 5'-TGCA-3' B. 5'-CTGCA-3' C. 5'-TGCAG-3' D. 5'-ACGT-3'
