#!/usr/bin/env python

import sys
import random
import gellib

def isKiller(blood, victim, suspect):
	#check if the suspect is the killer
	if blood - victim == suspect - victim:
		return True
	return False

if __name__ == '__main__':
	#structure
	gel = gellib.GelClass()
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

	band_tree = gel.createBandTree(total_bands)
	subsize = random.randint(min_bands, int(total_bands*max_band_percent)) 
	victim = gel.getRandomSubSet(total_bands, subsize)
	victim.add(0)
	suspects = []
	for i in range(num_suspects-2):
		subsize = random.randint(min_bands, int(total_bands*max_band_percent)) 
		suspect = gel.getRandomSubSet(total_bands, subsize)
		suspects.append(suspect)
	print suspects


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

	gel.drawLane(allbands, "allbands")
	gel.blankLane()
	gel.drawLane(victim, "Victim")
	gel.drawLane(blood, "Blood")
	random.shuffle(suspects)
	random.shuffle(suspects)
	killcount = 0
	for i in range(len(suspects)):
		suspect = suspects[i]
		iskiller = isKiller(blood, victim, suspect)
		if iskiller:
			killcount += 1
		print("Suspect #%d: %s"%(i+1, iskiller))
		gel.drawLane(suspect, "Suspect %d"%(i+1))
	if killcount != 1:
		"wrong number of killers"
		sys.exit(1)
	gel.blankLane()
	gel.drawLane(canthave, "canthave")
	gel.drawLane(musthave, "musthave")
	gel.saveImage("suspects.png")
	print("open suspects.png")
