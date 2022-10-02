#!/usr/bin/env python3


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

print(overo_table+'\n')
print(overo_text+'\n')
print(leopard_table+'\n')
print(leopard_text+'\n')
print(merge_table+'\n')
print(merge_text+'\n')
print(question_text+'\n')
