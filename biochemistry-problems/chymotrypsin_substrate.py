#!/usr/bin/env python3

import os
import random

#The main substrates of chymotrypsin are peptide bonds in which the amino acid N-terminal to the bond is a
#tryptophan, tyrosine, phenylalanine, or leucine
# cuts after large hydrophobic amino acid

"""
54. Given the following peptide sequence, Arg-Glu-Gly-Lys-Pro-Phe-Ser-Ala, at which peptide bond location will chymotrypsin most likely cleave first?
A. Ser-Ala
B. Phe-Ser
C. Pro-Phe
D. Lys-Pro
E. Gly-Lys
"""

#cut_aminos = ['Leu', 'Met', 'Phe', 'Trp', 'Tyr', ]
cut_aminos = ['Leu', 'Phe', 'Trp', 'Tyr', ]
reg_aminos = ['Ala', 'Asn', 'Ser', 'Glu', 'Asp', 'Gln', 'Thr', 'Gly', 'Cys', ]
bad_aminos = ['Pro', 'His', 'Arg', 'Lys', 'Met', 'Iso', 'Val', ]


def makeSubstrate(length):
	cut_amino_acid = random.choice(cut_aminos)
	cut_location = random.randint(2, length-2)
	substrate = []
	for i in range(length):
		if i == cut_location:
			aa = cut_amino_acid
		else:
			aa = random.choice(reg_aminos)
		substrate.append(aa)
	return substrate, cut_amino_acid, cut_location


def makeQuestion(length):
	substrate, cut_amino_acid, cut_location = makeSubstrate(length)
	peptide = 'NH<sub>3</sub><sup>+</sup>&mdash;' + '&mdash;'.join(substrate) + '&mdash;COO<sup>&ndash;</sup>'
	question = "Given the following peptide sequence, <b>{0}</b>, at which peptide bond location will chymotrypsin most likely cleave first?".format(peptide)
	print(question)
	choices = []
	# cuts after large hydrophobic amino acid
	answer = substrate[cut_location] + "&mdash;" + substrate[cut_location+1]
	choices.append(answer)
	wrong1 =substrate[cut_location-1] + "&mdash;" + substrate[cut_location]
	choices.append(wrong1)
	wrong_list = []
	for i in range(length-1):
		if i == cut_location or i == cut_location-1:
			continue
		wrong = substrate[i] + "&mdash;" + substrate[i+1]
		wrong_list.append(wrong)
	random.shuffle(wrong_list)
	for i in range(3):
		wrong = wrong_list[i]
		choices.append(wrong)
	random.shuffle(choices)
	print(choices)
	return question, answer, choices


def questionString(question, answer, choices):
	complete_text = "MC\t{0}".format(question)
	for choice in choices:
		if choice == answer:
			status = "Correct"
		else:
			status = "Incorrect"
		complete_text += "\t{0}\t{1}".format(choice, status)
	return complete_text

if __name__ == '__main__':
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	question_count = 99
	for i in range(question_count):
		length = random.randint(7,11)
		question, answer, choices = makeQuestion(length)
		complete_text = questionString(question, answer, choices)
		f.write("{0}\n".format(complete_text))
	f.close()

