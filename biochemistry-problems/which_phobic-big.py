#!/usr/bin/env python3

import os
import copy
import random

lipids = {
	'DHA':	{'C':22,'H':32,'O':2},
	'cholesterol':	{'C':27,'H':46,'O':1},
	'EPA':	{'C':20,'H':30,'O':2},
	'palmate':	{'C':16,'H':31,'O':2},
	'oleate':	{'C':18,'H':33,'O':2},
	'stearate':	{'C':18,'H':35,'O':2},
	'testosterone':	{'C':19,'H':28,'O':2},
	'phosphatidate': {'C':35,'H':67,'O':8,'P':1},
	'cephalin': {'C':28,'H':38,'N':2,'O':4},
	'phosphatidylinositol': {'C':47,'H':83,'O':13,'P':2},
	'phosphatidylcholine': {'C':44,'H':84,'N':1,'O':8,'P':1},
}

sugars = {
	'ribose':	{'C':5,'H':10,'O':5,},
	'deoxyribose':	{'C':5,'H':10,'O':4,},
	'glucose':	{'C':6,'H':12,'O':12,},
	'sucrose':	{'C':12,'H':22,'O':11},
	'maltotriose':	{'C':18,'H':32,'O':16},
}
nucleobases = {
	'adenine':	{'C':5,'H':5,'N':5,},
	'cytosine':	{'C':4,'H':5,'N':3,'O':1},
	'guanine':	{'C':5,'H':5,'N':5,'O':1},
	'thymine':	{'C':5,'H':6,'N':2,'O':2},
	'uracil':	{'C':4,'H':4,'N':2,'O':2},
}
nucleotides = {
	'adenosine':	{'C':10,'H':14,'N':5,'O':7,'P':1},
	'cytidine':	{'C':9,'H':14,'N':3,'O':8,'P':1},
	'guanosine':	{'C':10,'H':14,'N':5,'O':8,'P':1},
	'thymidine':	{'C':10,'H':13,'N':2,'O':8,'P':1},
	'uridine':	{'C':9,'H':13,'N':2,'O':9,'P':1},
}
amino_acids = {
	'alanine':	{'C':3,'H':7,'N':1,'O':2},
	'arginine':	{'C':6,'H':14,'N':4,'O':2},
	'asparagine':	{'C':4,'H':8,'N':2,'O':2},
	'aspartate':	{'C':4,'H':7,'N':1,'O':4},
	'cysteine':	{'C':3,'H':7,'N':1,'O':2,'S':1},
	'glutamine':	{'C':5,'H':10,'N':2,'O':3},
	'glutamate':	{'C':5,'H':9,'N':1,'O':4},
	'histidine':	{'C':6,'H':9,'N':3,'O':2},
	'lysine':	{'C':6,'H':14,'N':2,'O':2},
	'methionine':	{'C':5,'H':11,'N':1,'O':2,'S':1},
	'proline':	{'C':5,'H':9,'N':1,'O':2},
	'serine':	{'C':3,'H':7,'N':1,'O':3},
	'threonine':	{'C':4,'H':9,'N':1,'O':3},
}

def dict2html(moldict):
	molstring = ''
	for element in moldict:
		if moldict[element] <= 0:
			continue
		molstring += element
		if moldict[element] > 1:
			molstring += '<sub>{0}</sub>'.format(moldict[element])
	return molstring


def condensation(m1dict, m2dict):
	merge_dict = copy.copy(m1dict)
	for key in m2dict:
		merge_dict[key] = merge_dict.get(key,0) + m2dict[key]
	merge_dict['H'] = merge_dict.get('H',2) - 2
	merge_dict['O'] = merge_dict.get('O',1) - 1
	return merge_dict

def create_new_entries(mol_dict):
	keys = list(mol_dict.keys())
	random.shuffle(keys)
	for k1 in keys:
		for k2 in keys:
			m1dict = mol_dict[k1]
			m2dict = mol_dict[k2]
			merge_dict = condensation(m1dict, m2dict)
			mol_dict[k1+'-'+k2] = merge_dict
	return mol_dict


def writeQuestion():
	#============================
	question_txt = "Based on only their molecular formula, "
	question_txt += "which one of the following compounds is most likely a lipid?"
	print("01. "+question_txt)

	letters = "ABCDEFG"
	complete_question = 'MC\t'
	complete_question += question_txt

	newlipids = {}
	newlipids.update(lipids)
	preadd = len(newlipids)
	hydrophillics = create_new_entries(newlipids)
	postadd = len(newlipids)
	print("Created {0} new entries {1} -> {2}".format(postadd-preadd, preadd, postadd))
	answer_key = random.choice(list(newlipids.keys()))
	print(answer_key)

	hydrophillics = {}
	hydrophillics.update(sugars)
	hydrophillics.update(nucleobases)
	hydrophillics.update(nucleotides)
	hydrophillics.update(amino_acids)
	preadd = len(hydrophillics)
	hydrophillics = create_new_entries(hydrophillics)
	postadd = len(hydrophillics)
	print("Created {0} new entries {1} -> {2}".format(postadd-preadd, preadd, postadd))

	choices = []
	choices.append(answer_key)
	for i in range(4):
		wrong = random.choice(list(hydrophillics.keys()))
		choices.append(wrong)

	complete_dict = {}
	complete_dict.update(hydrophillics)
	complete_dict.update(newlipids)

	random.shuffle(choices)

	for i,choice_key in enumerate(choices):
		molecule_string  = dict2html(complete_dict[choice_key])
		complete_question += '\t'+molecule_string
		if choice_key == answer_key:
			prefix = '*'
			complete_question += '\tCorrect'
		else:
			prefix = ''
			complete_question += '\tIncorrect'
		print("{0}{1}. {2} -- {3}".format(prefix, letters[i], choice_key, molecule_string))
	complete_question += '\n'
	print("")
	return complete_question


if __name__ == '__main__':

	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	duplicates = 95

	for d in range(duplicates):
		complete_question = writeQuestion()
		f.write(complete_question)
	f.close()
