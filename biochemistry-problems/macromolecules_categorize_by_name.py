#!/usr/bin/env python

import os
import random

carbs = [
	"glycogen",
	"chitin",
	"cellulose",
	"starch",
	"amylopectin",
	"amylose",
	"sucrose",
	"lactose",
	"maltose",
	"glucose",
	"fructose",
	"galactose",
	"monosaccharides",
	"disaccharides",
	"polysaccharides",
	"aldose",
	"ketose",
	"triose",
	"pentose",
	"hexose",
	"glycosidic linkage",
	"&alpha;-glycosidic linkage",
	"&beta;-glycosidic linkage",
	"C<sub>6</sub>H<sub>12</sub>O<sub>6</sub>",
	"dietary fiber",
	"exoskeleton of arthropods",
	"strong and flexible surgical thread",
	"tough cell wall in plants",
]

lipids = [
	"fatty acids",
	"fat",
	"oil",
	"wax",
	"butter",
	"do not dissolve well in water",
	"almost all hydrophobic",
	"olive oil",
	"highest energy content",
	"glycerol and fatty acids",
	"made of long hydrocarbons",
	"does not form long polymers",
	"phospholipids",
	"detergents",
	"steroids",
	"ester linkage",
	"triglycerides",
	"triacylglycerol",
	"saturated fatty acids",
	"unsaturated fatty acids",
	"has no hydrogen bonds",
	"cholesterol",
	"testosterone",
	"estrogen",
	"cortisone",
	"&omega;-3",
	"margarine",
	"hydrogenation",
	"long-term food reserves"
]

protein = [
	"&alpha;-helix",
	"&beta;-strand",
	"&beta;-pleated sheet",
	"alanine",
	"cysteine",
	"phenylalanine",
	"glycine",
	"histidine",
	"isoleucine",
	"lysine",
	"leucine",
	"methionine",
	"asparagine",
	"proline",
	"glutamine",
	"arginine",
	"serine",
	"threonine",
	"valine",
	"tyrosine",
	"peptide bonds",
	"collagen",
	"often contains sulfur atoms",
	"hemoglobin",
	"speed up chemical reactions",
	"enzymes",
	"polypeptides",
	"amino acids",
	"side chains",
	"&alpha;-carbon or C<sub>&alpha;</sub>",
	"primary structure",
	"secondary structure",
	"tertiary structure",
	"quaternary structure",
	"disulfide bridge",
	"hydrophobic core",
	"denaturation",
	"native structure",
	"chaperonins",
]

nucleic_acids = [
	"polymer is connected by phosphates",
	"backbone of sugar-phosphate units",
	"ATP",
	"adenine",
	"cytosine",
	"guanine",
	"thymine",
	"uracil",
	"DNA",
	"RNA",
	"nucleotides",
	"nucleosides",
	"nucleobases",
	"nitrogenous bases"
	"polynucleotides",
	"pyrimidines",
	"purines",
	"deoxyribose backbone",
	"double stranded helix",
	"antiparallel helix",
	"5&prime; &rarr; 3&prime;"
	"base pair",
	"messenger RNA",
	"transfer RNA",
	"ribosomal RNA",
]

"""
1. <b>glycogen</b> is most appropriately associated with this macromolecular category.
A. Nucleic acids
B. Lipids
*C. Carbohydrates
D. Proteins
"""


choices = [
	'Nucleic acids',
	'Lipids',
	'Carbohydrates',
	'Proteins',
]

def writeQuestion(macro, answer):
	question = "MC\t"
	question += "<b>{0}</b> ".format(macro)
	if macro.endswith('s'):
		question += "are "
	else:
		question += "is "
	question += "is most appropriately associated with this macromolecular category."
	random.shuffle(choices)
	for choice in choices:
		question += '\t' + choice
		if choice == answer:
			question += '\tCorrect'
		else:
			question += '\tIncorrect'
	return question
	
	
	
if __name__ == '__main__':
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	for item in carbs:
		complete_question = writeQuestion(item, 'Carbohydrates')
		f.write(complete_question+'\n')
	for item in lipids:
		complete_question = writeQuestion(item, 'Lipids')
		f.write(complete_question+'\n')
	for item in protein:
		complete_question = writeQuestion(item, 'Proteins')		
		f.write(complete_question+'\n')
	for item in nucleic_acids:
		complete_question = writeQuestion(item, 'Nucleic acids')
		f.write(complete_question+'\n')
	f.close()
	
	
	
