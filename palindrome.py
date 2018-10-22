#!/usr/bin/env python

import sys
import copy
import random

def complement(seq):
	newseq = copy.copy(seq)
	newseq = newseq.replace('A', 'x')
	newseq = newseq.replace('T', 'A')
	newseq = newseq.replace('x', 'T')
	newseq = newseq.replace('G', 'x')
	newseq = newseq.replace('C', 'G')
	newseq = newseq.replace('x', 'C')
	return newseq[::-1]

def oneLetter(choice):
	if choice[1] == choice[2]:
		question = complement(choice[2])+"NNN"
	else:
		question = "NNN"+complement(choice[0])
	return question

def threeLetters(choice):
	if random.random() < 0.5:
		question = "NNN"+complement(choice)
	else:
		question = complement(choice)+"NNN"
	return question

def fiveLetters(choice):
	if random.random() < 0.5:
		question = "NNN"+complement(choice)
	else:
		question = complement(choice)+"NNN"
	nt = random.choice(list(choice))
	compl = complement(nt)
	question = nt + question + compl
	return question


if __name__ == '__main__':
	nt1 = random.choice(('A', 'C', 'T', 'G'))
	nt2 = complement(nt1)
	print("letters used: %s and %s"%(nt1, nt2))

	choices = []
	choices.append(nt1+nt1+nt2)
	choices.append(nt1+nt2+nt2)
	choices.append(nt2+nt2+nt1)
	choices.append(nt2+nt1+nt1)
	print(choices)
	random.shuffle(choices)

	questions = []
	unusedchoices = copy.copy(choices)
	
	choice = unusedchoices.pop()
	question = oneLetter(choice)
	print("%s -> %s"%(choice, question))
	questions.append(question)
	
	choice = unusedchoices.pop()
	question = threeLetters(choice)
	print("%s -> %s"%(choice, question))
	questions.append(question)

	choice = unusedchoices.pop()
	question = fiveLetters(choice)
	print("%s -> %s"%(choice, question))
	questions.append(question)
	
	choice = unusedchoices.pop()
	r = random.random()
	if r < 0.333:
		question = oneLetter(choice)
	elif r < 0.667:
		question = threeLetters(choice)
	else:
		question = fiveLetters(choice)
	print("%s -> %s"%(choice, question))
	print("")

	questions.append(question)

	print("Questions XX-XX. "
			+"The following numbered sequences only contains half of a palindromic sequence. "
			+"Match the correct lettered seqeuence that would finish and replace the 'N's in the sequence to make them palindromes. "
			+"Letters will be used exactly once.")

	random.shuffle(choices)
	letters = "ABCDE"
	for i in range(len(choices)):
		l = letters[i]
		c = choices[i]
		sys.stderr.write("%s. %s\t"%(l, c))
	print("")
	random.shuffle(questions)
	for i in range(len(questions)):
		q = questions[i]
		sys.stderr.write("_ XX. 5'-%s-3'"%(q))
		if i % 2 == 1:
			sys.stderr.write("\n")
		else:
			sys.stderr.write("\t")


