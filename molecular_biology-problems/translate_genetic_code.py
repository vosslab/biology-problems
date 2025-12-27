#!/usr/bin/env python3

import os
import re
import random
import functools

import bptools
import seqlib

#==========================
@functools.lru_cache
def make_inverse_genetic_code():
	inverse_genetic_code = {}
	for codon, amino_acid in seqlib.genetic_code.items():
		inverse_genetic_code[amino_acid] = inverse_genetic_code.get(amino_acid, []) + [codon]
	return inverse_genetic_code

#==========================
@functools.lru_cache
def read_wordle_list():
	bad_letters = list("BJOUXZ")
	wordle_file = bptools.get_repo_data_path("real_wordles.txt")
	wordle_list = []
	with open(wordle_file, "r") as f:
		for line in f:
			word = line.strip().upper()
			if len(word) != 5:
				continue
			if any(letter in word for letter in bad_letters):
				continue
			wordle_list.append(word)
	return wordle_list

#==========================
def make_random_peptide(peptide_length):
	peptide_sequence = "M"
	nucleotide_sequence = "AUG"

	inverse_genetic_code = make_inverse_genetic_code()
	amino_acid_list = list(inverse_genetic_code.keys())
	amino_acid_list.remove("_")
	amino_acid_list.sort()

	for _ in range(peptide_length - 1):
		amino_acid = random.choice(amino_acid_list)
		peptide_sequence += amino_acid
		codon = random.choice(inverse_genetic_code[amino_acid])
		nucleotide_sequence += codon

	return peptide_sequence, nucleotide_sequence

#==========================
def make_wordle_peptide(peptide_length):
	wordle_list = read_wordle_list()
	m_wordle_list = [word for word in wordle_list if word.startswith("M")]
	if len(m_wordle_list) == 0:
		return make_random_peptide(peptide_length)

	peptide_sequence = random.choice(m_wordle_list)
	more_wordles_to_add = peptide_length // 5 - 1
	for _ in range(more_wordles_to_add):
		peptide_sequence += random.choice(wordle_list)
	nucleotide_sequence = "AUG"

	inverse_genetic_code = make_inverse_genetic_code()
	for i, amino_acid in enumerate(list(peptide_sequence)):
		if i == 0:
			continue
		codon = random.choice(inverse_genetic_code[amino_acid])
		nucleotide_sequence += codon

	return peptide_sequence, nucleotide_sequence

#==========================
@functools.lru_cache
def read_genetic_code():
	genetic_code_html_table = ""
	code_path = os.path.join(os.path.dirname(__file__), "genetic_code.html")
	with open(code_path, "r") as f:
		for line in f:
			sline = line.strip()
			match = re.search(r">([AGCU]{3})<", sline)
			if match:
				nt_sequence = match.groups()[0]
				nt_table = seqlib.Single_Strand_Table_No_Primes(nt_sequence)
				sline = re.sub(nt_sequence, nt_table, sline)
			genetic_code_html_table += sline
	return genetic_code_html_table

#==========================
def make_complete_question(N, peptide_length, extra=False):
	if peptide_length % 5 == 0:
		wordle = True
		peptide_sequence, nucleotide_sequence = make_wordle_peptide(peptide_length)
	else:
		wordle = False
		peptide_sequence, nucleotide_sequence = make_random_peptide(peptide_length)

	stop_codons = ("UAA", "UAG", "UGA")
	nucleotide_sequence += random.choice(stop_codons)

	if extra is True:
		n = random.choice((2, 4, 5, 7, 8))
		front_nts = "AUG"
		while "AUG" in front_nts:
			front_nts = seqlib.transcribe(seqlib.makeSequence(n))
		n = random.randint(2, 7)
		back_nts = "AUG"
		while "AUG" in back_nts:
			back_nts = seqlib.transcribe(seqlib.makeSequence(n))
		nucleotide_sequence = front_nts + nucleotide_sequence + back_nts

	question = ""
	question += read_genetic_code()
	question += "<p>Using the Genetic Code table above, "
	question += f"translate the following {len(nucleotide_sequence)} nucleotide mRNA sequence "
	question += "into the single-letter peptide code.</p>"
	if extra is True:
		nt_table = seqlib.Single_Strand_Table(nucleotide_sequence, separate=4)
	else:
		nt_table = seqlib.Single_Strand_Table(nucleotide_sequence, separate=3)
	question += nt_table
	question += "<p>Note:<ul>"
	if extra is True:
		question += "<li>Remember that translation begins at a particular mRNA sequence.</li>"
	if wordle is True:
		wordle_count = peptide_length // 5
		if wordle_count == 1:
			question += "<li>Your answer will spell a five-letter word"
			question += " that is also a valid Wordle&trade; answer.</li>"
		else:
			question += f"<li>Your answer will spell a combination of {wordle_count} five-letter words"
			question += " (that are also valid Wordle&trade; answers).</li>"
	else:
		question += f"<li>Your answer will be a random string of {peptide_length} amino acid letters.</li>"
	question += "<li>Enter your answer in the blank with no punctuation, only letters.</li>"
	question += "</ul></p>"

	sep3 = seqlib.insertCommas(peptide_sequence, separate=3)
	sep5 = seqlib.insertCommas(peptide_sequence, separate=5)
	answers_list = [peptide_sequence, sep3, sep5]

	return bptools.formatBB_FIB_Question(N, question, answers_list)

#==========================
def write_question(N, args):
	return make_complete_question(N, args.peptide_length, args.extra)

#==========================
def parse_arguments():
	parser = bptools.make_arg_parser(description="Generate genetic code translation questions.")
	parser.add_argument(
		"-n",
		"--peptide-length",
		type=int,
		dest="peptide_length",
		help="Length of the peptide to translate.",
		default=10,
	)
	parser.add_argument(
		"-X",
		"--extra",
		dest="extra",
		action="store_true",
		help="Add extra nts to front and back of mRNA.",
		default=False,
	)
	args = parser.parse_args()
	return args

#==========================
def main():
	args = parse_arguments()
	outfile = bptools.make_outfile(None, f"{args.peptide_length}_aa", "extra" if args.extra else None)
	bptools.collect_and_write_questions(write_question, args, outfile)

#==========================
if __name__ == "__main__":
	main()
