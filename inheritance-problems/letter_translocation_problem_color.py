#!/usr/bin/env python3

import os
import re
import sys
import copy
import random
import crcmod.predefined

def list2string(mylist, spacer=""):
	mystring = spacer.join(mylist)
	return mystring
	mystring = ""
	for letter in mylist:
		mystring += letter + spacer
	return mystring

def list2text(mylist):
	mystring = ""
	if len(mylist) > 2:
		sublist = mylist[:-1]
		for letter in sublist:
			mystring += letter+", "
		mystring += "and "+mylist[-1]
	elif len(mylist) == 2:
		mystring = mylist[0]+" and "+mylist[1]
	return mystring

num2word = {
	1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five',
	6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten',
	11: 'eleven', 12: 'twelve', 13: 'thirteen', 14: 'fourteen',
	15: 'fifteen', 16: 'sixteen', 17: 'seventeen', 18: 'eighteen', 19: 'nineteen',
	20: 'twenty',
}

def cutChromosome(chromolist, cut):
	chromosome_A = []
	chromosome_B = []
	count = 0
	for item in chromolist:
		count += 1
		if count <= cut:
			chromosome_A.append(item)
		else:
			chromosome_B.append(item)
	return chromosome_A, chromosome_B

#====================
def drawChromosomeCut(chromolist, cut):
	mystr = ""
	count = 0
	for item in chromolist:
		count += 1
		mystr += item
		if count == cut:
			mystr += "|"
	return mystr

#====================
def formatChromosome(chromosome_list, color):
	return colorHtmlText(list2string(chromosome_list, ""), color)

#====================
def colorHtmlText(raw_text, color):
	color_text = '<span style="color: {0}; display: inline-block; margin-left: -2px; margin-right: -2px;">{1}</span>'.format(color, raw_text)
	return color_text

#====================
def makeAllPossibleTranslocations(chromosome1_A, chromosome1_B, chromosome2_A, chromosome2_B):
	possible_translocation_choice_pairs = []
	#original1 = formatChromosome(chromosome1_A, 'DarkRed') + formatChromosome(chromosome1_B, 'OrangeRed') 
	#original2 = formatChromosome(chromosome2_A, 'DarkBlue') + formatChromosome(chromosome2_B, 'DarkGreen')
	#choice_pair = (original1, original2)
	#choice_pairs.append(choice_pair)

	choice1 = formatChromosome(chromosome1_A, 'DarkRed') + formatChromosome(chromosome2_B, 'DarkGreen')
	choice2 = formatChromosome(chromosome2_B[::-1], 'DarkGreen') + formatChromosome(chromosome1_A[::-1], 'DarkRed')
	choice_pair = (choice1, choice2)
	possible_translocation_choice_pairs.append(choice_pair)

	choice1 = formatChromosome(chromosome1_A, 'DarkRed') + formatChromosome(chromosome2_A[::-1], 'DarkBlue')
	choice2 = formatChromosome(chromosome2_A, 'DarkBlue') + formatChromosome(chromosome1_A[::-1], 'DarkRed')
	choice_pair = (choice1, choice2)
	possible_translocation_choice_pairs.append(choice_pair)
	
	choice1 = formatChromosome(chromosome1_B[::-1], 'OrangeRed') + formatChromosome(chromosome2_B, 'DarkGreen')
	choice2 = formatChromosome(chromosome2_B[::-1], 'DarkGreen') + formatChromosome(chromosome1_B, 'OrangeRed')
	choice_pair = (choice1, choice2)
	possible_translocation_choice_pairs.append(choice_pair)
	
	choice1 = formatChromosome(chromosome1_B[::-1], 'OrangeRed') + formatChromosome(chromosome2_A[::-1], 'DarkBlue')
	choice2 = formatChromosome(chromosome2_A, 'DarkBlue') + formatChromosome(chromosome1_B, 'OrangeRed')
	choice_pair = (choice1, choice2)
	possible_translocation_choice_pairs.append(choice_pair)
	return possible_translocation_choice_pairs

#====================
def makeAllImpossibleTranslocations(chromosome1_A, chromosome1_B, chromosome2_A, chromosome2_B):
	impossible_translocation_choices = []
	#original1 = formatChromosome(chromosome1_A, 'DarkRed') + formatChromosome(chromosome1_B, 'OrangeRed') 
	#original2 = formatChromosome(chromosome2_A, 'DarkBlue') + formatChromosome(chromosome2_B, 'DarkGreen')
	#choice_pair = (original1, original2)
	#choice_pairs.append(choice_pair)

	#choice1 = formatChromosome(chromosome1_A, 'DarkRed') + formatChromosome(chromosome2_B, 'DarkGreen')
	#choice2 = formatChromosome(chromosome2_B[::-1], 'DarkGreen') + formatChromosome(chromosome1_A[::-1], 'DarkRed')
	choice1 = formatChromosome(chromosome1_A[::-1], 'DarkRed') + formatChromosome(chromosome2_B, 'DarkGreen')
	choice2 = formatChromosome(chromosome2_B, 'DarkGreen') + formatChromosome(chromosome1_A[::-1], 'DarkRed')
	choice3 = formatChromosome(chromosome1_A, 'DarkRed') + formatChromosome(chromosome2_B[::-1], 'DarkGreen')
	choice4 = formatChromosome(chromosome2_B[::-1], 'DarkGreen') + formatChromosome(chromosome1_A, 'DarkRed')
	choice5 = formatChromosome(chromosome1_A[::-1], 'DarkRed') + formatChromosome(chromosome2_B[::-1], 'DarkGreen')
	choice6 = formatChromosome(chromosome2_B[::-1], 'DarkGreen') + formatChromosome(chromosome1_A[::-1], 'DarkRed')
	impossible_translocation_choices += [choice1, choice2, choice3, choice4, choice5, choice6]

	#choice1 = formatChromosome(chromosome1_A, 'DarkRed') + formatChromosome(chromosome2_A[::-1], 'DarkBlue')
	#choice2 = formatChromosome(chromosome2_A, 'DarkBlue') + formatChromosome(chromosome1_A[::-1], 'DarkRed')
	choice1 = formatChromosome(chromosome1_A[::-1], 'DarkRed') + formatChromosome(chromosome2_A[::-1], 'DarkBlue')
	choice2 = formatChromosome(chromosome2_A, 'DarkBlue') + formatChromosome(chromosome1_A, 'DarkRed')
	choice3 = formatChromosome(chromosome1_A, 'DarkRed') + formatChromosome(chromosome2_A, 'DarkBlue')
	choice4 = formatChromosome(chromosome2_A[::-1], 'DarkBlue') + formatChromosome(chromosome1_A[::-1], 'DarkRed')
	choice5 = formatChromosome(chromosome1_A[::-1], 'DarkRed') + formatChromosome(chromosome2_A, 'DarkBlue')
	choice6 = formatChromosome(chromosome2_A[::-1], 'DarkBlue') + formatChromosome(chromosome1_A, 'DarkRed')
	impossible_translocation_choices += [choice1, choice2, choice3, choice4, choice5, choice6]
	
	#choice1 = formatChromosome(chromosome1_B[::-1], 'OrangeRed') + formatChromosome(chromosome2_B, 'DarkGreen')
	#choice2 = formatChromosome(chromosome2_B[::-1], 'DarkGreen') + formatChromosome(chromosome1_B, 'OrangeRed')
	choice1 = formatChromosome(chromosome1_B, 'OrangeRed') + formatChromosome(chromosome2_B, 'DarkGreen')
	choice2 = formatChromosome(chromosome2_B[::-1], 'DarkGreen') + formatChromosome(chromosome1_B[::-1], 'OrangeRed')
	choice3 = formatChromosome(chromosome1_B[::-1], 'OrangeRed') + formatChromosome(chromosome2_B[::-1], 'DarkGreen')
	choice4 = formatChromosome(chromosome2_B, 'DarkGreen') + formatChromosome(chromosome1_B, 'OrangeRed')
	choice5 = formatChromosome(chromosome1_B, 'OrangeRed') + formatChromosome(chromosome2_B[::-1], 'DarkGreen')
	choice6 = formatChromosome(chromosome2_B, 'DarkGreen') + formatChromosome(chromosome1_B[::-1], 'OrangeRed')
	impossible_translocation_choices += [choice1, choice2, choice3, choice4, choice5, choice6]

	
	#choice1 = formatChromosome(chromosome1_B[::-1], 'OrangeRed') + formatChromosome(chromosome2_A[::-1], 'DarkBlue')
	#choice2 = formatChromosome(chromosome2_A, 'DarkBlue') + formatChromosome(chromosome1_B, 'OrangeRed')
	choice1 = formatChromosome(chromosome1_B, 'OrangeRed') + formatChromosome(chromosome2_A[::-1], 'DarkBlue')
	choice2 = formatChromosome(chromosome2_A, 'DarkBlue') + formatChromosome(chromosome1_B[::-1], 'OrangeRed')
	choice3 = formatChromosome(chromosome1_B[::-1], 'OrangeRed') + formatChromosome(chromosome2_A, 'DarkBlue')
	choice4 = formatChromosome(chromosome2_A[::-1], 'DarkBlue') + formatChromosome(chromosome1_B, 'OrangeRed')
	choice5 = formatChromosome(chromosome1_B, 'OrangeRed') + formatChromosome(chromosome2_A, 'DarkBlue')
	choice6 = formatChromosome(chromosome2_A[::-1], 'DarkBlue') + formatChromosome(chromosome1_B[::-1], 'OrangeRed')
	impossible_translocation_choices += [choice1, choice2, choice3, choice4, choice5, choice6]

	return impossible_translocation_choices

#=======================
def getCrc16_FromString(mystr):
	crc16 = crcmod.predefined.Crc('xmodem')
	crc16.update(mystr.encode('ascii'))
	return crc16.hexdigest().lower()

#=====================
def makeQuestionPretty(question):
	pretty_question = copy.copy(question)
	#print(len(pretty_question))
	pretty_question = re.sub('\<table.+\<\/table\>', '[]\n', pretty_question)
	#print(len(pretty_question))
	pretty_question = re.sub('\<\/p\>\s*\<p\>', '\n', pretty_question)
	#print(len(pretty_question))
	return pretty_question

#=====================
def formatBB_MC_Question(N, question, choices_list, answer):
	bb_question = ''

	number = "{0}. ".format(N)
	crc16 = getCrc16_FromString(question)
	bb_question += 'MC\t<p>{0}. {1}</p> {2}'.format(N, crc16, question)
	pretty_question = makeQuestionPretty(question)
	print('{0}. {1} -- {2}'.format(N, crc16, pretty_question))

	letters = 'ABCDEFGH'
	for i, choice in enumerate(choices_list):
		bb_question += '\t{0}.  {1}&nbsp; '.format(letters[i], choice)
		if choice == answer:
			prefix = 'x'
			bb_question += '\tCorrect'
		else:
			prefix = ' '
			bb_question += '\tIncorrect'
		print("- [{0}] {1}. {2}".format(prefix, letters[i], choice))
	print("")
	return bb_question + '\n'

#====================
def makePossibleChoiceList(possible_choice_pairs):
	possible_choices = []
	for i in range(len(possible_choice_pairs)):
		choice = random.choice(possible_choice_pairs[i])
		possible_choices.append(choice)
	return possible_choices


#====================
def makeChromosomes():
	if len(sys.argv) >= 2:
		min_size = int(sys.argv[1])
	else:
		min_size = 6
	if min_size < 4:
		print("Sorry, you must have at least 4 genes for this program")
		sys.exit(1)
	if min_size > 9:
		print("Sorry, you cant have a minimum bigger than 9 genes per chromosome for this program")
		sys.exit(1)

	print(("Minimum chromosome size: %d"%(min_size)))

	charlist = list("ABCDEFGHJKMPQRSTWXYZ")

	chromosome1_size = random.randint(min_size, 10)
	chromosome1 = charlist[:chromosome1_size]

	chromosome2_size = random.randint(min_size, len(charlist)-chromosome1_size-1)
	chromosome2_shift = random.randint(chromosome1_size+1, len(charlist)-chromosome2_size)
	chromosome2 = charlist[chromosome2_shift:chromosome2_shift+chromosome2_size]

	chromosome1_cut = random.randint(2, chromosome1_size-2)
	chromosome2_cut = random.randint(3, chromosome2_size-3)
	#print chromosome1_cut, chromosome2_cut

	print(list2string(chromosome1), chromosome1_cut, chromosome1_size)
	print(list2string(chromosome2), chromosome2_cut, chromosome2_size)
	print(drawChromosomeCut(chromosome1, chromosome1_cut))
	print(drawChromosomeCut(chromosome2, chromosome2_cut))

	chromosome1_A, chromosome1_B = cutChromosome(chromosome1, chromosome1_cut)
	chromosome2_A, chromosome2_B = cutChromosome(chromosome2, chromosome2_cut)

	#this should not happen, but it does
	if len(chromosome1_A) <= 1:
		print("ERROR")
		return None
	if len(chromosome1_B) <= 1:
		print("ERROR")
		return None
	if len(chromosome2_A) <= 1:
		print("ERROR")
		return None
	if len(chromosome2_B) <= 1:
		print("ERROR")
		return None
	len_set = set([len(chromosome1_A),  len(chromosome1_B), len(chromosome2_A), len(chromosome2_B) ])
	if len(len_set) < 4:
		print("Chromosomes have matching lengths")
		return None
	return (chromosome1_A, chromosome1_B, chromosome2_A, chromosome2_B)

#====================
def makeQuestion(N):
	#this is a BIG function
	chromosome_tuple = None
	while chromosome_tuple is None:
		chromosome_tuple = makeChromosomes()

	chromosome1_A, chromosome1_B, chromosome2_A, chromosome2_B = chromosome_tuple

	possible_choice_pairs = makeAllPossibleTranslocations(chromosome1_A, chromosome1_B, chromosome2_A, chromosome2_B)
	possible_choices = makePossibleChoiceList(possible_choice_pairs)
	random.shuffle(possible_choices)
	popped = possible_choices.pop()
	
	impossible_translocation_choices = makeAllImpossibleTranslocations(chromosome1_A, chromosome1_B, chromosome2_A, chromosome2_B)
	random.shuffle(impossible_translocation_choices)
	random.shuffle(impossible_translocation_choices)
	answer_choice = ''
	while len(answer_choice) != len(popped):
		answer_choice = impossible_translocation_choices.pop()

	possible_choices.append(answer_choice)
	random.shuffle(possible_choices)

	bar = "<strong>|</strong>"

	question = ''
	question += ("Two chromosomes with the gene sequences  ")
	question += formatChromosome(chromosome1_A, 'DarkRed') + formatChromosome(chromosome1_B, 'OrangeRed') 
	question += ("  and  ")
	question += formatChromosome(chromosome2_A, 'DarkBlue') + formatChromosome(chromosome2_B, 'DarkGreen') 
	question += ("  undergo a reciprocal translocation after breaks between  ")
	question += colorHtmlText(chromosome1_A[-1], 'DarkRed') + bar + colorHtmlText(chromosome1_B[0], 'OrangeRed') 
	question += ("  and  ")
	question += colorHtmlText(chromosome2_A[-1], 'DarkBlue') + bar + colorHtmlText(chromosome2_B[0], 'DarkGreen') 
	question += (" . Which one of the following is <strong>NOT</strong> a possible product of this translocation?&nbsp; ")

	#blackboard = "MC\t"
	#blackboard += question
	#print(question)
	
	blackboard = formatBB_MC_Question(N, question, possible_choices, answer_choice)
	return blackboard

if __name__ == "__main__":
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')	
	duplicates = 199
	for i in range(duplicates):
		blackboard = makeQuestion(i+1)
		if blackboard is not None:
			f.write(blackboard)
		else:
			#continue
			sys.exit(1)
	f.close()
