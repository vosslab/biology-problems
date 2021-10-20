#!/usr/bin/env python

import os
import sys
import random
import gellib

### ugly code, but works

def isFather(child, mother, male):
	#check if the male is the father
	#print("father check", child - mother - male)
	if len(child - mother - male) == 0:
		return True
	return False

def haveBaby(mother, father, num_males=3):
	diffs = father - mother
	print(diffs)
	if len(diffs) < 2:
		sys.exit(1)
	child = set()
	for i in mother:
		if random.random() < 0.5:
			child.add(i)
	for i in father:
		if random.random() < 0.4:
			child.add(i)
	for i in range(num_males):
		child.add(random.choice(list(diffs)))
	return child

if __name__ == '__main__':
	gel = gellib.GelClassHtml()
	gel.setTextColumn("Mother")
	"""
	num_males = 5 #min 3
	total_bands = 12
	min_bands = 4
	max_band_percent = 0.5
	"""

	"""
	num_males = 5 #min 3
	total_bands = 18
	min_bands = 10
	max_band_percent = 0.65
	"""
	num_males = 9 #min 3
	total_bands = 32
	min_bands = 14
	max_band_percent = 0.8

	band_tree = gel.createBandTree(total_bands)
	subsize = random.randint(min_bands, int(total_bands*max_band_percent)) 
	mother = gel.getRandomSubSet(total_bands, subsize)
	mother.add(0)
	allbands = set(range(total_bands))
	notmother = allbands - mother
	males = []
	subsize = random.randint(min_bands, int(total_bands*max_band_percent)) 
	father = gel.getRandomSubSet(total_bands, subsize)
	father.add(random.choice(list(notmother)))
	father.add(random.choice(list(notmother)))
	bothparents = father.intersection(mother)
	if len(bothparents) > 2:
		father.remove(random.choice(list(bothparents)))
	males.append(father)

	child = haveBaby(mother, father, num_males)
	musthave = child - mother
	print("mother", sorted(mother))
	print("child ", sorted(child))
	print("father", sorted(father))
	print("musthv", sorted(musthave))
	ignore = mother.intersection(child)
	print("ignore", sorted(ignore))

	if len(musthave) < num_males-1:
		#start over
		print("not enough band difference")
		sys.exit(1)
	# add a male with 1 band missing
	while len(males) < num_males:
		male = father.copy()
		male.remove(random.choice(list(musthave)))
		if male in males:
			musthave2 = male.intersection(musthave)
			male.remove(random.choice(list(musthave2)))
		if not male in males:
			males.append(male)
	for male in males:
		male.add(random.choice(list(allbands)))

	table = ""
	table += gel.tableWidths()
	#table += gel.drawLane(list(allbands), "allbands")
	table += gel.blankLane()
	table += gel.drawLane(sorted(mother), "Mother")
	table += gel.drawLane(sorted(child), "Child")
	random.shuffle(males)
	random.shuffle(males)
	dadcount = 0
	answer = None
	for i in range(len(males)):
		male = males[i]
		isfather = isFather(child, mother, male)
		if isfather:
			dadcount += 1
			answer = i
		#print(("Male #%d: %s -- %s"%(i+1, str(sorted(male)), isfather)))
		table += gel.drawLane(male, "Male %d"%(i+1))
	if dadcount != 1:
		print("wrong number of fathers")
		sys.exit(1)
	table += gel.blankLane()
	#table += gel.drawLane(musthave, "musthave")
	#table += gel.drawLane(ignore, "ignore")
	table += "</table>"

	#gel.saveImage("males.png")
	#print("open males.png")
	question = "<h6>Based on the DNA gel profile above, who is the father of the child?</h6>"
	full_question = "<p>Who is the father of the child?</p> {0} {1}".format(table, question)
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'a')
	f.write("MC\t")
	f.write(full_question+"\t")
	print("complete\n\n")
	print(question)
	charlist = "ABCDEFGHIJKLMN"
	for i in range(len(males)):
		letter = charlist[i]
		choice = "Male &num;{0:d}\t".format(i+1)
		if i == answer:
			choice += "Correct\t"
		else:
			choice += "Incorrect\t"
		print(choice)
		f.write(choice)
	f.write("\n")
	f.close()
	print("")
