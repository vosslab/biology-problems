#!/usr/bin/env python

import os
import sys
import random
import argparse

import seqlib

#==========================
#==========================
def makeInverseGeneticCode():
	inverse_genetic_code = {}
	for codon,amino_acid in seqlib.genetic_code.items():
		inverse_genetic_code[amino_acid] = inverse_genetic_code.get(amino_acid, []) + [codon,]
	return inverse_genetic_code

#==========================
#==========================
def makeRandomPeptide(peptide_length):
	peptide_sequence = 'M'
	nucleotide_sequence = "AUG"

	inverse_genetic_code = makeInverseGeneticCode()
	amino_acid_list = list(inverse_genetic_code.keys())
	#remove stop codon
	amino_acid_list.remove('_')
	amino_acid_list.sort()

	for i in range(peptide_length-1):
		amino_acid = random.choice(amino_acid_list)
		peptide_sequence += amino_acid
		codon = random.choice(inverse_genetic_code[amino_acid])
		nucleotide_sequence += codon

	print("nucleotide_sequence = ",nucleotide_sequence)
	peptide_sequence_calc = seqlib.translate(nucleotide_sequence)
	print("peptide_sequence = ", peptide_sequence)
	print("peptide_sequence_calc = ", peptide_sequence_calc)

	return peptide_sequence, nucleotide_sequence


#==========================
#==========================
def readWordleList():
	f = open('real_wordles.txt', 'r')

#==========================
#==========================
def makeWordlePeptide(peptide_length):
	wordle_list = readWordleList()
	peptide_sequence = 'M'
	nucleotide_sequence = "AUG"

	inverse_genetic_code = makeInverseGeneticCode()
	amino_acid_list = list(inverse_genetic_code.keys())
	#remove stop codon
	amino_acid_list.remove('_')
	amino_acid_list.sort()

	for i in range(peptide_length-1):
		amino_acid = random.choice(amino_acid_list)
		peptide_sequence += amino_acid
		codon = random.choice(inverse_genetic_code[amino_acid])
		nucleotide_sequence += codon

	print("nucleotide_sequence = ",nucleotide_sequence)
	peptide_sequence_calc = seqlib.translate(nucleotide_sequence)
	print("peptide_sequence = ", peptide_sequence)
	print("peptide_sequence_calc = ", peptide_sequence_calc)

	return peptide_sequence, nucleotide_sequence


#==========================
#==========================
def makeCompleteQuestion(N, peptide_length):
	peptide_sequence, nucleotide_sequence = makeRandomPeptide(peptide_length)

#==========================
#==========================
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-n', '--peptide-length', type=int, dest='peptide_length',
		help='length of the peptide to translate', default=10)
	parser.add_argument('-q', '--num-questions', type=int, dest='num_questions',
		help='number of questions to create', default=24)
	args = parser.parse_args()

	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	for i in range(args.num_questions):
		N = i+1
		bbformat = makeCompleteQuestion(N, args.peptide_length)
		f.write(bbformat)
		f.write('\n')
	f.close()
	proc = subprocess.Popen("open temp.html", shell=True)
	bptools.print_histogram()
