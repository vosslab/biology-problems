import copy
import random

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

	return seq

#=========================
def _makeSequence(seqlen=10):
	seq = ""
	for i in range(seqlen):
		seq += random.choice('AGCT')
	return seq

#=========================
def transcribe(dna):
	#assumes dna sequence is the non-template/coding strand
	rna = copy.copy(dna)
	rna = rna.replace('T', 'U')
	return rna

