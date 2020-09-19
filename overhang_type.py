#!/usr/bin/env python

import sys
import random
import restrictlib

def writeQuestion(enzyme_class, overhang_type):
	name = restrictlib.html_monospace(enzyme_class.__name__)
	cut_description = restrictlib.html_monospace(restrictlib.format_enzyme(enzyme_class))
	question = "11. The restriction enzyme <b>{0}</b> cuts the sequence: {1}. ".format(name, cut_description)
	question += "Which one of the following is the "
	question += "correct name for the type of cut this enzyme produces? "

	overhang = enzyme_class.overhang()

	answer = None
	choices = []
	if overhang_type is True:
		answer = overhang
		choices.append("5' overhang")
		choices.append("3' overhang")
		choices.append("blunt")
	else:
		if overhang.endswith("overhang"):
			answer = "sticky end"
		elif overhang == "blunt":
			answer = "blunt end"
		choices.append("overhang end")
		choices.append("hanger end")
		choices.append("blunt end")
		choices.append("straight edge")
		choices.append("sticky end")
	
	if answer is None:
		print("ERROR")
		print("ERROR")
		print("ERROR")
		sys.exit(1)

	print(question)
	
	#============================
	random.shuffle(choices)
	charlist = "ABCDE"
	for i in range(len(choices)):
		choice_msg = choices[i]
		letter = charlist[i]
		prefix = ""
		if choice_msg == answer:
			prefix = "*"
		print("{0}{1}. {2}".format(prefix, letter, choice_msg))




if __name__ == '__main__':

	if len(sys.argv) >= 2:
		overhang_type = False
	else:
		#just the name
		overhang_type = True

	enzymes = restrictlib.get_enzyme_list()
	enzyme_class = restrictlib.random_enzyme(enzymes)
	writeQuestion(enzyme_class, overhang_type)





	#A. 5'-TGCA-3' B. 5'-CTGCA-3' C. 5'-TGCAG-3' D. 5'-ACGT-3'
