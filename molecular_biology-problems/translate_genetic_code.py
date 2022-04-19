#!/usr/bin/env python

import os
import re
import sys
import random
import argparse
import subprocess

import seqlib
import bptools

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
	bad_letters = list('BJOUXZ')
	f = open('real_wordles.txt', 'r')
	wordle_list = []
	total_words = 0
	for line in f:
		sline = line.strip().upper()
		if len(sline) != 5:
			continue
		total_words += 1
		skip = False
		for ltr in bad_letters:
			if ltr in sline:
				skip = True
		if skip is True:
			continue
		wordle_list.append(sline.upper())
	print("read {0} of {1} valid words from file.".format(len(wordle_list), total_words))
	return wordle_list

#==========================
#==========================
def makeWordlePeptide(peptide_length):
	wordle_list = readWordleList()

	m_wordle_list = []
	for word in wordle_list:
		if word.startswith('M'):
			m_wordle_list.append(word)
	print("read {0} of {1} valid words that start with 'M'.".format(len(m_wordle_list), len(wordle_list)))

	m_word1 = random.choice(m_wordle_list)
	peptide_sequence = m_word1

	more_wordles_to_add = peptide_length//5 - 1
	for i in range(more_wordles_to_add):
		word = random.choice(wordle_list)
		peptide_sequence += word
	nucleotide_sequence = "AUG"

	inverse_genetic_code = makeInverseGeneticCode()

	for i,amino_acid in enumerate(list(peptide_sequence)):
		if i == 0:
			if amino_acid != 'M':
				print("protein fail")
				sys.exit(1)
			nucleotide_sequence = "AUG"
			continue
		try:
			codon = random.choice(inverse_genetic_code[amino_acid])
		except KeyError:
			print("peptide_sequence = ", peptide_sequence)
			print("amino_acid = ", amino_acid)
			sys.exit(1)
		nucleotide_sequence += codon

	print("nucleotide_sequence = ",nucleotide_sequence)
	peptide_sequence_calc = seqlib.translate(nucleotide_sequence)
	print("peptide_sequence = ", peptide_sequence)
	print("peptide_sequence_calc = ", peptide_sequence_calc)

	return peptide_sequence, nucleotide_sequence


#==========================
#==========================
def readGeneticCode():
	genetic_code_html_table = ''
	f = open('genetic_code.html', 'r')
	for line in f:
		# no newlines for blackboard upload
		sline = line.strip()
		req = re.search('\>([AGCU]{3})\<', sline)
		if req:
			nt_sequence = req.groups()[0]
			nt_table = seqlib.Single_Strand_Table_No_Primes(nt_sequence)
			sline = re.sub(nt_sequence, nt_table, sline)
		genetic_code_html_table += sline
	return genetic_code_html_table

#==========================
#==========================
def makeCompleteQuestion(N, peptide_length, extra=False):
	if peptide_length % 5 == 0:
		print("using wordle sequence")
		wordle = True
		peptide_sequence, nucleotide_sequence = makeWordlePeptide(peptide_length)
	else:
		print("using random sequence")
		wordle = False
		peptide_sequence, nucleotide_sequence = makeRandomPeptide(peptide_length)

	#add a stop codon
	stop_codons = ('UAA', 'UAG', 'UGA')
	nucleotide_sequence += random.choice(stop_codons)

	if extra is True:
		print("using extra mode")
		n = random.choice( (2,4,5,7,8) )
		front_nts = 'AUG'
		while 'AUG' in front_nts:
			front_nts = seqlib.transcribe(seqlib.makeSequence(n))
		n = random.randint(2, 7)
		back_nts = 'AUG'
		while 'AUG' in back_nts:
			back_nts = seqlib.transcribe(seqlib.makeSequence(n))
		nucleotide_sequence = front_nts + nucleotide_sequence + back_nts

	question = ''
	genetic_code_html_table = readGeneticCode()
	question += genetic_code_html_table
	question += '<p>Using the Genetic Code table above, '
	question += 'translate the following {0} nucleotide mRNA sequence '.format(len(nucleotide_sequence))
	question += 'into the single-letter peptide code.</p>'
	if extra is True:
		nt_table = seqlib.Single_Strand_Table(nucleotide_sequence, separate=4)
	else:
		nt_table = seqlib.Single_Strand_Table(nucleotide_sequence, separate=3)
	question += nt_table
	question += '<p>Note:<ul>'
	if extra is True:
		question += '<li>Remember that translation begins at a particular mRNA sequence.</li>'
	if wordle is True:
		wordle_count = peptide_length // 5
		if wordle_count == 1:
			question += '<li>Your answer will spell a five-letter word'.format(wordle_count)
			question += ' that is also a valid Wordle&trade; answer.</li>'
		elif wordle_count >= 2:
			question += '<li>Your answer will spell a combination of {0} five-letter words'.format(wordle_count)
			question += ' (that are also valid Wordle&trade; answers).</li>'
		else:
			print(error)
			sys.exit(1)
	else:
		question += '<li>Your answer will be a random string of {0} amino acid letters.</li>'.format(peptide_length)
	question += '<li>Enter your answer in the blank with no punctuation, only letters.</li>'
	question += '</ul></p>'
	f = open('temp.html', 'w')
	f.write(question)
	f.close()
	#print(question)

	sep3 = seqlib.insertCommas(peptide_sequence, separate=3)
	sep5 = seqlib.insertCommas(peptide_sequence, separate=5)
	answers_list = [peptide_sequence, sep3, sep5]

	bbformat = bptools.formatBB_FIB_Question(N, question, answers_list)

	return bbformat

#==========================
#==========================
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-n', '--peptide-length', type=int, dest='peptide_length',
		help='length of the peptide to translate', default=10)
	parser.add_argument('-q', '--num-questions', type=int, dest='num_questions',
		help='number of questions to create', default=24)
	parser.add_argument('-X', '--extra', dest='extra', action='store_true',
		help='add extra nts to front and back of mRNA', default=False)
	args = parser.parse_args()

	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	for i in range(args.num_questions):
		N = i+1
		bbformat = makeCompleteQuestion(N, args.peptide_length, args.extra)
		f.write(bbformat)
		f.write('\n')
	f.close()
	proc = subprocess.Popen("sleep 1; open temp.html", shell=True)
	bptools.print_histogram()
