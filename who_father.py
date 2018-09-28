#!/usr/bin/env python

import sys
import numpy
import random
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

### ugly code, but works

def drawLane(band_tree, pil_img, row=1, text=""):
	factor = 5
	height = 70
	rowgap = 15
	draw1 = ImageDraw.Draw(pil_img, "RGB")
	miny = (row-1)*height + rowgap
	maxx = (row)*height
	xshift = 150
	fnt = ImageFont.truetype('/Users/vosslab/Library/Fonts/LiberationSansNarrow-Regular.ttf', 36)
	draw1.text((rowgap, miny+height/4.), text, font=fnt, fill="black")
	for band_dict in band_tree:
		start = xshift+band_dict['start']*factor
		end = start + band_dict['width']*factor
		draw1.rectangle(((start, miny), (end, maxx)), fill="blue", outline="black")	

def getRandomSubSet(setsize, subsize):
	subindex = random.sample(xrange(setsize), subsize)
	return set(subindex)

def indexToSubSet(mylist, indices):
	newlist = []
	for i in indices:
		newlist.append(mylist[i])
	return newlist

def createBandTree(total_bands=12):
	min_band_width = 2
	max_band_width = 6
	min_gap = 2
	max_gap = 6
	band_tree = []
	start_point = 2
	for i in range(total_bands):
		width = random.randint(min_band_width, max_band_width+1)
		gap = random.randint(min_gap, max_gap+1)
		start_point += gap
		band_dict = {
			'width': width,
			'start': start_point,
		}
		start_point += width
		band_tree.append(band_dict)
	return band_tree

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
	print("hello world")
	#structure
	num_males = 4 #min 3
	total_bands = 15
	min_bands = 6
	max_band_percent = 0.65

	#each lane of the gel will be represented by a row in a numpy array
	## step 1 -- generate band library
	band_tree = createBandTree(total_bands)
	subsize = random.randint(min_bands, int(total_bands*max_band_percent)) 
	mother = getRandomSubSet(total_bands, subsize)
	mother.add(0)
	allbands = set(range(total_bands))
	notmother = allbands - mother
	males = []
	subsize = random.randint(min_bands, int(total_bands*max_band_percent)) 
	father = getRandomSubSet(total_bands, subsize)
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


	img1 = Image.new("RGB", (1024,1024), (212,212,212))

	row = 1
	drawLane(indexToSubSet(band_tree, allbands), img1, row, "allbands")
	row += 1
	drawLane(indexToSubSet(band_tree, mother), img1, row, "mother")
	row += 1
	drawLane(indexToSubSet(band_tree, child), img1, row, "child")
	random.shuffle(males)
	random.shuffle(males)
	dadcount = 0
	for i in range(len(males)):
		male = males[i]
		isfather = isFather(child, mother, male)
		if isfather:
			dadcount += 1
		print("Male #%d: %s -- %s"%(i+1, str(sorted(male)), isfather))
		row += 1
		drawLane(indexToSubSet(band_tree, male), img1, row, "male %d"%(i+1))
	if dadcount != 1:
		print("wrong number of fathers")
		sys.exit(1)
	row += 1
	drawLane(indexToSubSet(band_tree, musthave), img1, row, "musthave")
	row += 1
	drawLane(indexToSubSet(band_tree, ignore), img1, row, "ignore")
	img1.save("males.png", "PNG")
	print("open males.png")
