#!/usr/bin/env python3

import random

import bptools
overo_text = (
	"<p>In the American Paint Horse, the Overo gene, Ov, produces a white splotch pattern on the coat. "
	+"The overo phenotype is seen only when a horse has one Ov copy, Ovov. "
	+"Horses with two Ov copies, OvOv, suffer from overo lethal white syndrome (OLWS) and die soon after birth. "
	+"These foals are called white overo because they are completely white before they die. "
	+"Horses with no Ov copies are solid colored, ovov.</p>"
)

overo_table = """
<table border="1" style="border-collapse: collapse; width: 200px; height: 120px;">
<tbody>
<tr style="">
<th style="background-color: #ffdb99;" align="center">genotype</th>
<th style="background-color: #ffdb99;" align="center">phenotype</th>
</tr>
<tr style="">
<td style="" align="center">Ov Ov</td>
<td style="" align="center">white overo</td>
</tr>
<tr style="">
<td style="" align="center">Ov ov</td>
<td style="" align="center">overo</td>
</tr>
<tr style="">
<td style="" align="center">ov ov</td>
<td style="" align="center">solid</td>
</tr>
</tbody>
</table>
"""

leopard_text = (
	"<p>In Appaloosa horse breeds, the Leopard complex gene, Lp, shows incomplete dominance "
	+"and controls white spotting. "
	+"One Lp allele, Lplp, produces the leopard phenotype, in which there are spots everywhere. "
	+"Two Lp alleles, LpLp, produce the fewspot phenotype, "
	+"in which the horse is mostly white with colored spots.</p>"
)

leopard_table = """
<table border="1" style="border-collapse: collapse; width: 200px; height: 120px;">
<tbody>
<tr style="">
<th style="background-color: lightblue;" align="center">genotype</th>
<th style="background-color: lightblue;" align="center">phenotype</th>
</tr>
<tr style="">
<td style="" align="center">Lp Lp</td>
<td style="" align="center">fewspot</td>
</tr>
<tr style="">
<td style="" align="center">Lp lp</td>
<td style="" align="center">leopard</td>
</tr>
<tr style="">
<td style="" align="center">lp lp</td>
<td style="" align="center">solid</td>
</tr>
</tbody>
</table>
"""

merge_text = (
	"<p>A crossbred horse that is both overo and leopard is called pintaloosa, "
	+"and these horses are spotted with splotches. "
	+"A horse that is both overo and fewspot is considered fewspot "
	+"because the white areas from Lp is indistinguishable from the white from Ov.</p>"
)

merge_table = """
<table border="1" style="border-collapse: collapse; width: 450px; height: 160px;">
<tbody>
<tr style="">
<th style="background-color: lightgray;" align="center" colspan=2 rowspan=2>merged<br/>phenotypes</th>
<th style="background-color: lightblue;" align="center" colspan=3>leopard gene</th>
</tr>
<tr style="">
<th style="background-color: lightgray;" align="center">fewspot</th>
<th style="background-color: lightgray;" align="center">leopard</th>
<th style="background-color: lightgray;" align="center">solid</th>
</tr>
<tr style="">
<th style="background-color: #ffdb99; width: 20%;" align="center" rowspan=3>overo<br/>gene</th>
<th style="background-color: lightgray; width: 20%;" align="center">white overo</th>
<td style=" width: 20%;" align="center">white</td>
<td style=" width: 20%;" align="center">white</td>
<td style=" width: 20%;" align="center">white</td>
</tr>
<tr style="">
<th style="background-color: lightgray;" align="center">overo</th>
<td style="" align="center">fewspot</td>
<td style="" align="center">pintaloosa</td>
<td style="" align="center">overo</td>
</tr>
<tr style="">
<th style="background-color: lightgray;" align="center">solid</th>
<td style="" align="center">fewspot</td>
<td style="" align="center">leopard</td>
<td style="" align="center">solid</td>
</tr>
</tbody>
</table>
"""

question_text = (
	"<p>Suppose that 16 pairs of pintaloosa horses have one offspring per pair. "
	+"How many of each phenotype would be expected? "
	+"Determine the number out of 16 expected for each phenotype. "
	+"Only count phenotypes for offspring expected to live past one week of age.</p>"
)

phenotype_counts = {
	"fewspot": 3,
	"pintaloosa": 4,
	"overo": 2,
	"leopard": 2,
	"solid": 1,
}

#======================================
def write_question(N: int, args) -> str:
	phenotype = random.choice(list(phenotype_counts.keys()))
	answer_count = phenotype_counts[phenotype]

	full_text = ""
	full_text += overo_text + overo_table
	full_text += leopard_text + leopard_table
	full_text += merge_text + merge_table
	full_text += question_text
	full_text += (
		f"<p><strong>How many {phenotype} offspring</strong> are expected "
		f"out of 16?</p>"
	)

	choices = []
	answer_text = f"{answer_count} of 16"
	choices.append(answer_text)

	other_counts = [i for i in range(0, 17) if i != answer_count]
	random.shuffle(other_counts)
	for count in other_counts:
		if len(choices) >= args.num_choices:
			break
		choices.append(f"{count} of 16")

	random.shuffle(choices)
	complete_question = bptools.formatBB_MC_Question(N, full_text, choices, answer_text)
	return complete_question

#======================================
def parse_arguments():
	parser = bptools.make_arg_parser(description="Generate horse phenotype questions.")
	parser = bptools.add_choice_args(parser, default=5)
	args = parser.parse_args()
	return args

#======================================
def main():
	args = parse_arguments()
	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)

if __name__ == '__main__':
	main()
