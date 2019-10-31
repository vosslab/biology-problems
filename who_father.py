#!/usr/bin/env python

import sys
import random
import gellib

### ugly code, but works

def isFather(child, mother, male):
	#check if the male is the father
	print "father check", child - mother - male
	if len(child - mother - male) == 0:
		return True
	return False

def haveBaby(mother, father, num_males=3):
	diffs = father - mother
	print diffs
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
	gel = gellib.GelClass()
	gel.setTextColumn("Mother")

	num_males = 5 #min 3
	total_bands = 18
	min_bands = 10
	max_band_percent = 0.65
	"""
	num_males = 9 #min 3
	total_bands = 32
	min_bands = 14
	max_band_percent = 0.8
	"""

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
	print "mother", sorted(mother)
	print "child ", sorted(child)
	print "father", sorted(father)
	print "musthv", sorted(musthave)
	ignore = mother.intersection(child)
	print "ignore", sorted(ignore)

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

	gel.drawLane(allbands, "allbands")
	gel.blankLane()
	gel.drawLane(mother, "Mother")
	gel.drawLane(child, "Child")
	random.shuffle(males)
	random.shuffle(males)
	dadcount = 0
	for i in range(len(males)):
		male = males[i]
		isfather = isFather(child, mother, male)
		if isfather:
			dadcount += 1
		print("Male #%d: %s -- %s"%(i+1, str(sorted(male)), isfather))
		gel.drawLane(male, "Male %d"%(i+1))
	if dadcount != 1:
		print("wrong number of fathers")
		sys.exit(1)
	gel.blankLane()
	gel.drawLane(musthave, "musthave")
	gel.drawLane(ignore, "ignore")
	gel.saveImage("males.png")
	print("open males.png")
