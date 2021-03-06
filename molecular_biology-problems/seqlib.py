import sys
import copy
import random

arbitrary_codes = {
	'A': ('A'),
	'B': ('C', 'G', 'T',), # not A
	'C': ('C'),
	'D': ('A', 'G', 'T',), # not C
	'G': ('G'),
	'H': ('A', 'C', 'T',), # not G
	'K': ('G', 'T',),
	'M': ('A', 'C',),
	'N': ('A', 'C', 'G', 'T',),
	'R': ('A', 'G',), # purine
	'S': ('C', 'G',), # strong
	'T': ('T'),
	'V': ('A', 'C', 'G',), # not T
	'W': ('A', 'T',), # weak
	'Y': ('C', 'T',), # pyrimidine
}
inverse_arbitrary_codes = {
	('A',): 'A',
	('C', 'G', 'T'): 'B',
	('C',): 'C',
	('A', 'G', 'T'): 'D',
	('G',): 'G',
	('A', 'C', 'T'): 'H',
	('G', 'T'): 'K',
	('A', 'C'): 'M',
	('A', 'C', 'G', 'T'): 'N',
	('A', 'G'): 'R',
	('C', 'G'): 'S',
	('T',): 'T',
	('A', 'C', 'G'): 'V',
	('A', 'T'): 'W',
	('C', 'T'): 'Y'
}

genetic_code = {
	'UUU':'F', 'UCU':'S', 'UAU':'Y', 'UGU':'C',
	'UUC':'F', 'UCC':'S', 'UAC':'Y', 'UGC':'C',
	'UUA':'L', 'UCA':'S', 'UAA':'_', 'UGA':'_',
	'UUG':'L', 'UCG':'S', 'UAG':'_', 'UGG':'W',
	
	'CUU':'L', 'CCU':'P', 'CAU':'H', 'CGU':'R',
	'CUC':'L', 'CCC':'P', 'CAC':'H', 'CGC':'R',
	'CUA':'L', 'CCA':'P', 'CAA':'Q', 'CGA':'R',
	'CUG':'L', 'CCG':'P', 'CAG':'Q', 'CGG':'R',
	
	'AUU':'I', 'ACU':'T', 'AAU':'N', 'AGU':'S',
	'AUC':'I', 'ACC':'T', 'AAC':'N', 'AGC':'S',
	'AUA':'I', 'ACA':'T', 'AAA':'K', 'AGA':'R',
	'AUG':'M', 'ACG':'T', 'AAG':'K', 'AGG':'R',
	
	'GUU':'V', 'GCU':'A', 'GAU':'D', 'GGU':'G',
	'GUC':'V', 'GCC':'A', 'GAC':'D', 'GGC':'G',
	'GUA':'V', 'GCA':'A', 'GAA':'E', 'GGA':'G',
	'GUG':'V', 'GCG':'A', 'GAG':'E', 'GGG':'G',
}

#==========================
def colorNucleotideBackground(nt):
	colormap = {
		'A': '#e6ffe6', #A is green
		'C': '#e6f3ff', #C is blue
		'T': '#ffe6e6', #T is red
		'G': '#f2f2f2', #G is black
		'U': '#f3e6ff', #U is purple
	}
	if colormap.get(nt, None) is None:
		return ''
	bgcolorcode = ' bgcolor="{0}"'.format(colormap[nt])
	return bgcolorcode

#==========================
def colorNucleotideForeground(nt):
	colormap = {
		'A': '#004d00', #A is green
		'C': '#003566', #C is blue
		'T': '#6e1212', #T is red
		'G': '#2a2000', #G is black
		'U': '#420080', #U is purple
	}
	code = "<span style='color: {0};'>{1}</span>"
	if colormap.get(nt, None) is None:
		return nt
	return code.format(colormap[nt], nt)

#==========================
def DNA_Table(top_sequence, bottom_sequence=None, left_primes=True, right_primes=True):
	table = '<!-- {0} --> '.format(''.join(top_sequence))
	table += ' <table style="border-collapse: collapse; border: 1px solid silver;"> '
	#===========
	table += ' <tr>'
	if left_primes is True:
		table += '<td>5&prime;&ndash;</td>'
	else:
		table += '<td>&ndash;</td>'
	table += makeHtmlTDRow(top_sequence)
	if right_primes is True:
		table += '<td>&ndash;3&prime;</td>'
	else:
		table += '<td>&ndash;</td>'
	table += '</tr> '
	#===========
	if bottom_sequence is None:
		bottom_sequence = complement(top_sequence)
	table += ' <tr>'
	if left_primes is True:
		table += '<td>3&prime;&ndash;</td>'
	else:
		table += '<td>&ndash;</td>'
	table += makeHtmlTDRow(bottom_sequence)
	if right_primes is True:
		table += '<td>&ndash;5&prime;</td>'
	else:
		table += '<td>&ndash;</td>'
	table += '</tr> '
	#===========
	table += '</table> '
	return table

#=====================
#=====================
def Single_Strand_Table(ss_sequence_str, fivetothree=True, separate=3):
	table = '<!-- {0} --> '.format(''.join(ss_sequence_str))
	table += '&nbsp;<table style="border-collapse: collapse; border: 0px; display:inline-table"> '
	table += ' <tr>'
	if fivetothree is True:
		table += '<td>5&prime;&ndash;</td>'
	else:
		table += '<td>3&prime;&ndash;</td>'
	ss_sequence_list = list(ss_sequence_str)
	table += makeHtmlTDRow(ss_sequence_list, separate)
	if fivetothree is True:
		table += '<td>&ndash;3&prime;</td>'
	else:
		table += '<td>&ndash;5&prime;</td>'
	table += '</tr> '
	table += '</table> '
	return table

#=====================
#=====================
def Single_Strand_Table_No_Primes(ss_sequence_str, separate=3):
	table = '<!-- {0} --> '.format(''.join(ss_sequence_str))
	table += '&nbsp;<table style="border-collapse: collapse; border: 0px; display:inline-table"> '
	table += ' <tr>'
	ss_sequence_list = list(ss_sequence_str)
	table += makeHtmlTDRow(ss_sequence_list, separate)
	table += '</tr> '
	table += '</table> '
	return table

#=====================
#=====================
def Primer_Table(primer):
	return Single_Strand_Table(transcribe(primer), fivetothree=True)

#==========================
def makeHtmlTable(sequence_list, separate=3):
	table = '<!-- {0} --> '.format(''.join(sequence_list))
	table += '<table style="border-collapse: collapse; border: 1px solid silver;"> '
	for j in range(len(sequence_list)):
		table += ' <tr>'
		table += makeHtmlTDRow(sequence_list[j], separate)
		table += '</tr> '
	table += '</table> '
	return table

#==========================
def makeHtmlTDRow(sequence, separate=3):
	htmlrow = ""
	#print(sequence)
	for i in range(len(sequence)):
		if i > 0 and i % separate == 0:
			htmlrow += "<td>&nbsp;,&nbsp;</td> "
		nt = sequence[i]
		htmlrow += "<td {1}>&nbsp;{0}&nbsp;</td> ".format(
			colorNucleotideForeground(nt),
			colorNucleotideBackground(nt))
	return htmlrow

#==========================
def insertCommas(my_str, separate=3):
	new_str = ''
	for i in range(0, len(my_str), separate):
		new_str += my_str[i:i+separate] + ','
	return new_str[:-1]

#=========================
def complement(seq):
	newseq = copy.copy(seq)
	newseq = newseq.replace('A', 'x')
	newseq = newseq.replace('T', 'A')
	newseq = newseq.replace('x', 'T')
	newseq = newseq.replace('G', 'x')
	newseq = newseq.replace('C', 'G')
	newseq = newseq.replace('x', 'C')
	return newseq

#=========================
def flip(seq):
	newseq = copy.copy(seq)
	return newseq[::-1]

#=========================
def makeSequence(seqlen=10):
	if seqlen <= 3:
		## too many checks
		seq = _makeSequence(seqlen)
		return seq
	endloop = False
	half = int(seqlen//2)
	while not endloop:
		endloop = True
		seq = _makeSequence(seqlen)
		compl = complement(seq)

		# several criteria for bad sequences
		if seq == flip(seq):
			endloop = False
		elif seq == compl:
			endloop = False
		elif seq == flip(compl):
			endloop = False

		elif seq[:half] == seq[-half:]:
			endloop = False
		elif compl[:half] == compl[-half:]:
			endloop = False
		elif seq[:half] == compl[-half:]:
			endloop = False
		elif compl[:half] == seq[-half:]:
			endloop = False

		elif not 'T' in seq:
			endloop = False
		elif not 'A' in seq:
			endloop = False

		elif seq[:half] == flip(seq[-half:]):
			endloop = False
		elif compl[:half] == flip(compl[-half:]):
			endloop = False
		elif seq[:half] == flip(compl[-half:]):
			endloop = False
		elif compl[:half] == flip(seq[-half:]):
			endloop = False

		elif seq[:half] == flip(seq[:half]):
			endloop = False
		elif compl[:half] == flip(compl[:half]):
			endloop = False
		elif seq[:half] == flip(compl[:half]):
			endloop = False
		elif compl[:half] == flip(seq[:half]):
			endloop = False

		elif seq[-half:] == flip(seq[-half:]):
			endloop = False
		elif compl[-half:] == flip(compl[-half:]):
			endloop = False
		elif seq[-half:] == flip(compl[-half:]):
			endloop = False
		elif compl[-half:] == flip(seq[-half:]):
			endloop = False

		if endloop is True:
			newseq = copy.copy(seq)
			newseq = newseq.replace('T', 'A')
			if 'AAAA' in newseq:
				endloop = False
			newseq = newseq.replace('C', 'G')
			if 'GGGG' in newseq:
				endloop = False			

	return seq

#========================================
def sequenceSimilarityScore(seq1, seq2):
	min_length = min(len(seq1), len(seq2))
	score = 0
	for i in range(min_length):
		if seq1[i] == seq2[i]:
			score += 1
	return score

#========================================
def html_monospace(txt):
	return "<span style='font-family: 'andale mono', 'courier new', courier, monospace;'>{0}</span>".format(txt)

#=========================
def _makeSequence(seqlen=10):
	seq = ""
	letters = list('AGCT')
	for i in range(seqlen-1):
		seq += random.choice(letters)
	#last letter must not match the first
	letters.remove(seq[0])
	letters.remove(complement(seq[0]))
	seq += random.choice(letters)
	return seq

#=========================
def transcribe(dna):
	#assumes dna sequence is the non-template/coding strand
	rna = copy.copy(dna)
	rna = rna.replace('T', 'U')
	return rna

#=========================
def translate(rna):
	#assumes rna sequence is the mRNA and starts at the first letter
	codons = [rna[i:i+3] for i in range(0, len(rna), 3)]
	peptide = ''
	for codon in codons:
		amino_acid = genetic_code.get(codon.upper())
		if amino_acid is None:
			print("Unknown amino_acid: {0}".format(amino_acid))
			sys.exit(1)
		peptide += amino_acid
	return peptide

