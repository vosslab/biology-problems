#!/usr/bin/env python

import math
import random

#NUM TAB question_text TAB answer TAB [optional]tolerance

#=========================
def get_values(p=None):
	if p is None:
		p = get_good_p()
	q = round(1-p, 2)
	#hw
	p2 = round(p**2, 4)
	q2 = round(q**2, 4)
	twopq = round(2*p*q,4)
	sum = p2 + twopq + q2
	#print(p, q)
	#print(p2, twopq, q2, sum)
	return p, q, p2, twopq, q2

#=========================
def get_good_p():
	max_p = 0.99
	min_p = 0.4
	r = random.random()
	r *= (max_p-min_p)
	r += min_p
	#alleles
	p = round(r, 2)
	return p

def add_note():
	note_text = ''
	note_text += '<p>Note: Do not use a percentage, if the answer is 42.3%, use 0.423 on the blank. '
	note_text += 'Your answer will be greater than zero and less than one.</p>'
	return note_text

#=========================
def make_interesting_fraction(n, d=10000):
	#assume out of 10000
	# given numerator, n and denominator, d
	n = int(n)
	gcd = math.gcd(n, d)
	numerator = n // gcd
	denominator = d // gcd
	if denominator <= 100:
		factor = random.choice([7,11,13])
		numerator *= factor
		denominator *= factor
	elif denominator <= 400:
		factor = random.choice([3,7])
		numerator *= factor
		denominator *= factor
	if (numerator*1e4/denominator - n*1e4/d) > 0.1:
		print("something went wrong")
		sys.exit(1)
	return numerator, denominator

#=========================
def makeType2aQuestion(p):
	p, q, p2, twopq, q2 = get_values(p)
	if random.random() < 0.5:
		#get p
		phenotype = 'dominant'
		answer = p
	else:
		#get p
		phenotype = 'recessive'
		answer = q
	numerator, denominator = make_interesting_fraction(q2*1e4, 10000)

	question_text = ''
	question_text += 'Genetic disorder occurs {0:d} in {1:d} births. '.format(numerator, denominator)
	question_text += 'What is the expected frequency of the <b>{0}</b> allele '.format(phenotype)
	question_text += 'according to the Hardy-Weinberg model? '
	question_text += add_note()

	blackboard_text = 'NUM\t'
	blackboard_text += question_text+'\t'
	blackboard_text += '{0:.2f}\t'.format(answer)
	blackboard_text += '0.009\n'
	return blackboard_text

#=========================
def makeType2bQuestion(p):
	p, q, p2, twopq, q2 = get_values(p)
	if random.random() < 0.5:
		#get p
		phenotype = 'dominant'
		answer = p
	else:
		#get p
		phenotype = 'recessive'
		answer = q
	dominant_count = int((1.0 - q2)*1e4)
	numerator, denominator = make_interesting_fraction(dominant_count, 10000)

	question_text = ''
	question_text += 'In a small village, {0:d} out of {1:d} people '.format(numerator, denominator)
	question_text += 'have the dominant phenotype '
	question_text += 'and do NOT have a rare recessive disorder. '
	question_text += 'What is the expected frequency of the <b>{0}</b> allele '.format(phenotype)
	question_text += 'according to the Hardy-Weinberg model? '
	question_text += add_note()

	blackboard_text = 'NUM\t'
	blackboard_text += question_text+'\t'
	blackboard_text += '{0:.2f}\t'.format(answer)
	blackboard_text += '0.009\n'
	return blackboard_text

#=========================
def makeQuestion(type, p):
	if type == '2a':
		blackboard_text = makeType2aQuestion(p)
	elif type == '2b':
		blackboard_text = makeType2bQuestion(p)
	return blackboard_text

#=========================
#=========================
if __name__ == '__main__':
	type = '2a'
	#p = get_good_p()

	filename = 'bbq-hardy_weinberg-type_{0}.txt'.format(type)
	f = open(filename, 'w')
	count = 0
	for rawp in range(40, 100, 1):
		p = rawp/100.
		blackboard_text = makeQuestion(type, p)
		count += 1
		print(count, blackboard_text)
	print("wrote", count, "questions to", filename)
	f.close()
