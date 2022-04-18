#!/usr/bin/env python

import os
import sys
import argparse

import seqlib


#==========================
#==========================
def makeCompleteQuestion(N, peptide_length):
	peptide_sequence = 'M'
	nucleotide_sequence = "AUG"
	seqlen = (peptide_length - 1) * 3
	dna = seqlib.makeSequence(seqlen)
	rna = seqlib.transcribe(dna)
	nucleotide_sequence += rna
	print(nucleotide_sequence)
	peptide_sequence = seqlib.translate(nucleotide_sequence)
	print(peptide_sequence)
	sys.exit(1)








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
