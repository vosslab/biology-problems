#!/usr/bin/env python

phenotypes = ['O', 'A', 'B', 'AB',]
genotypes = ['OO', 'AO', 'BO', 'AB',]
pmap = {
	'O': 'OO',
	'A': 'AO',
	'B': 'BO',
	'AB': 'AB',
}
gmap = {
	'OO': 'O',
	'AO': 'A',
	'AA': 'A',
	'BO': 'B',
	'BB': 'B',
	'AB': 'AB',
}


if __name__ == '__main__':
	for p1 in phenotypes:
		for p2 in phenotypes:
			question += "If a female with type {0} blood marries a male with type {1} blood, ".format(p1, p2)
			question += "which of the following possible blood types could their children have? "
			question += "Check all that apply."
			print(question)
			break
