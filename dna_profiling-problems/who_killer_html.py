#!/usr/bin/env python3

import os
import sys
import random

import gellib
import bptools

def isKiller(blood, victim, suspect):
	#check if the suspect is the killer
	if blood - victim == suspect - victim:
		return True
	return False

def writeQuestion(N):
	#structure
	gel = gellib.GelClassHtml()
	gel.setTextColumn("Suspect 5")

	num_suspects = 5 #min 3
	total_bands = 18
	min_bands = 12
	max_band_percent = 0.7
	"""
	num_suspects = 9 #min 3
	total_bands = 24
	min_bands = 14
	max_band_percent = 0.6
	"""
	"""
	num_suspects = 5 #min 3
	total_bands = 12
	min_bands = 2
	max_band_percent = 0.7
	"""

	band_tree = gel.createBandTree(total_bands)
	subsize = random.randint(min_bands, int(total_bands*max_band_percent))
	victim = gel.getRandomSubSet(total_bands, subsize)
	victim.add(0)
	suspects = []
	for i in range(num_suspects-2):
		subsize = random.randint(min_bands, int(total_bands*max_band_percent))
		suspect = gel.getRandomSubSet(total_bands, subsize)
		suspects.append(suspect)
	print(suspects)

	allbands = set(range(total_bands))
	killer = random.choice(suspects)
	blood = victim.union(killer)
	print(victim)
	print(blood)
	print(killer)
	canthave = allbands - blood
	musthave = blood - victim
	ignore = victim.intersection(killer)

	if len(musthave) < 2:
		#start over
		#sys.exit(1)
		print('too few musthave lanes')
		return None
	if len(canthave) < 2:
		#start over
		#sys.exit(1)
		print('too few canthave lanes')
		return None

	# add a suspect with 1 band extra
	suspect = killer.copy()
	suspect.add(random.choice(list(canthave)))
	suspects.append(suspect)

	# add a suspect with 1 band missing
	suspect = killer.copy()
	suspect.remove(random.choice(list(musthave)))
	suspects.append(suspect)

	for suspect in suspects:
		suspect.add(random.choice(list(victim)))

	table = ""
	table += gel.tableWidths()
	#table += gel.drawLane(allbands, "allbands")
	table += gel.blankLane()
	table += gel.drawLane(victim, "Victim")
	table += gel.drawLane(blood, "Blood")
	random.shuffle(suspects)
	random.shuffle(suspects)

	question = "<h6>Based on the DNA gel profile above, which suspect left blood at the crime scene?</h6>"

	killcount = 0
	choice = ""
	for i in range(len(suspects)):
		suspect = suspects[i]
		table += gel.drawLane(suspect, "Suspect &num;{0:d}".format(i+1))
		iskiller = isKiller(blood, victim, suspect)
		if iskiller:
			killer_num = i
			killcount += 1
	if killcount != 1:
		"wrong number of killers"
		return None
	table += gel.blankLane()
	#table += gel.drawLane(canthave, "canthave")
	#table += gel.drawLane(musthave, "musthave")
	table += "</table> "
	full_question = "<p>Who is the killer?</p> {0} {1}".format(table, question)

	choices_list = []
	answer_string = ''
	for i in range(len(suspects)):
		choice = "Suspect &num;{0}".format(i+1)
		choices_list.append(choice)
		if i == killer_num:
			answer_string = choice
	bb_question = bptools.formatBB_MC_Question(N, full_question, choices_list, answer_string)
	return bb_question


if __name__ == '__main__':
	duplicates = 199
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	for i in range(duplicates):
		N = i + 1
		bb_question = writeQuestion(N)
		if bb_question is None:
			continue
		f.write(bb_question)
	f.write("\n")
	f.close()
	bptools.print_histogram()
