#!/usr/bin/env python3

import random
import bptools

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

#======================================
#======================================
def write_question(N, macro, answer):
	question = "<p><b>{0}</b> ".format(macro)
	if macro.endswith('s'):
		question += "are "
	else:
		question += "is "
	question += "most appropriately associated with this macromolecular category.</p>"
	choices_list = list(choices)
	random.shuffle(choices_list)
	complete_question = bptools.formatBB_MC_Question(N, question, choices_list, answer)
	return complete_question

#======================================
#======================================
def write_question_batch(N, args):
	questions = []
	for item in carbs:
		questions.append(write_question(N, item, 'Carbohydrates'))
		N += 1
	for item in lipids:
		questions.append(write_question(N, item, 'Lipids'))
		N += 1
	for item in protein:
		questions.append(write_question(N, item, 'Proteins'))
		N += 1
	for item in nucleic_acids:
		questions.append(write_question(N, item, 'Nucleic acids'))
		N += 1
	return questions

#======================================
#======================================
def parse_arguments():
	parser = bptools.make_arg_parser(batch=True)
	args = parser.parse_args()
	return args

#======================================
#======================================
def main():
	args = parse_arguments()
	outfile = bptools.make_outfile()
	questions = bptools.collect_question_batches(write_question_batch, args)
	bptools.write_questions_to_file(questions, outfile)

if __name__ == '__main__':
	main()
