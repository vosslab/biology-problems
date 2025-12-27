#!/usr/bin/env python3

import copy
import random

import bptools

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

def write_question(N: int, args) -> str:
	#============================
	question_text = "Based on only their molecular formula, "
	question_text += "which one of the following compounds is most likely a lipid?"

	newlipids = {}
	newlipids.update(lipids)
	create_new_entries(newlipids)
	answer_key = random.choice(list(newlipids.keys()))

	hydrophillics = {}
	hydrophillics.update(sugars)
	hydrophillics.update(nucleobases)
	hydrophillics.update(nucleotides)
	hydrophillics.update(amino_acids)
	create_new_entries(hydrophillics)

	choices = [answer_key]
	wrong_keys = random.sample(list(hydrophillics.keys()), 4)
	choices.extend(wrong_keys)

	complete_dict = {}
	complete_dict.update(hydrophillics)
	complete_dict.update(newlipids)

	random.shuffle(choices)

	choices_list = []
	for choice_key in choices:
		molecule_string = dict2html(complete_dict[choice_key])
		choices_list.append(molecule_string)
	answer_text = dict2html(complete_dict[answer_key])

	complete_question = bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)
	return complete_question

#==================================================
def parse_arguments():
	"""
	Parse command-line arguments.
	"""
	parser = bptools.make_arg_parser(description="Generate lipid identification questions.")
	args = parser.parse_args()
	return args

#==================================================
def main():
	args = parse_arguments()
	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)

#==================================================
if __name__ == '__main__':
	main()
