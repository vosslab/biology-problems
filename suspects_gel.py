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
	draw1 = ImageDraw.Draw(pil_img, "RGB")
	miny = (row-1)*height + 10
	maxx = (row)*height
	xshift = 150
	fnt = ImageFont.truetype('/Users/vosslab/Library/Fonts/LiberationSansNarrow-Regular.ttf', 36)
	draw1.text((10, miny+height/4.), text, font=fnt, fill="black")
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
	max_band_width = 4
	min_gap = 3
	max_gap = 8
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

def isKiller(blood, victim, suspect):
	#check if the suspect is the killer
	if blood - victim == suspect - victim:
		return True
	return False

if __name__ == '__main__':
	print("hello world")
	#structure
	num_suspects = 4 #min 3
	total_bands = 13
	min_bands = 5
	max_band_percent = 0.6

	#each lane of the gel will be represented by a row in a numpy array
	## step 1 -- generate band library
	band_tree = createBandTree(total_bands)
	subsize = random.randint(min_bands, int(total_bands*max_band_percent)) 
	victim = getRandomSubSet(total_bands, subsize)
	victim.add(0)
	suspects = []
	for i in range(num_suspects-2):
		subsize = random.randint(min_bands, int(total_bands*max_band_percent)) 
		suspect = getRandomSubSet(total_bands, subsize)
		suspects.append(suspect)
	print suspects

	img1 = Image.new("RGB", (1024,1024), (212,212,212))

	allbands = set(range(total_bands))
	killer = random.choice(suspects)
	blood = victim.union(killer)
	print victim
	print blood
	print killer
	canthave = allbands - blood
	musthave = blood - victim
	ignore = victim.intersection(killer)

	if len(musthave) < 2:
		#start over
		sys.exit(1)
	if len(canthave) < 2:
		#start over
		sys.exit(1)
	# add a suspect with 1 band missing
	suspect = killer.copy()
	suspect.add(random.choice(list(canthave)))
	suspects.append(suspect)
	# add a suspect with 1 band extra
	suspect = killer.copy()
	suspect.remove(random.choice(list(musthave)))
	suspects.append(suspect)
	row = 1
	drawLane(indexToSubSet(band_tree, victim), img1, row, "victim")
	row += 1
	drawLane(indexToSubSet(band_tree, blood), img1, row, "blood")
	random.shuffle(suspects)
	random.shuffle(suspects)
	killcount = 0
	for i in range(len(suspects)):
		suspect = suspects[i]
		iskiller = isKiller(blood, victim, suspect)
		if iskiller:
			killcount += 1
		print("Suspect #%d: %s"%(i+1, iskiller))
		row += 1
		drawLane(indexToSubSet(band_tree, suspect), img1, row, "suspect %d"%(i+1))
	if killcount != 1:
		"wrong number of killers"
		sys.exit(1)
	row += 1
	drawLane(indexToSubSet(band_tree, canthave), img1, row, "canthave")
	row += 1
	drawLane(indexToSubSet(band_tree, musthave), img1, row, "musthave")
	img1.save("suspects.png", "PNG")
	print("open suspects.png")
