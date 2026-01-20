
CHROMOSOME_LENGTHS = {
	1: (125, 124),
	2: (93, 149),
	3: (91, 107),
	4: (50, 140),
	5: (48, 133),
	6: (61, 110),
	7: (60, 99),
	8: (46, 101),
	9: (49, 92),
	10: (40, 95),
	11: (54, 81),
	12: (36, 98),
	13: (18, 97),
	14: (17, 90),
	15: (19, 84),
	16: (37, 54),
	17: (24, 57),
	18: (17, 61),
	19: (27, 33),
	20: (28, 36),
	21: (13, 35),
	22: (15, 37),
}

ACROCENTRIC_CHROMOSOMES = [13, 14, 15, 21, 22]

COLOR_SCALES = {
	'red': ['coral', 'lightsalmon', 'crimson'],
	'blue': ['deepskyblue', 'lightskyblue', 'royalblue'],
}


#======================================
def merge_tables(table_list):
	table = ''
	table += '<table style="border-collapse: collapse; border: 0px solid white;">'
	for chromo_table in table_list:
		table += '<tr>'
		table += '  <td align="left">{0}</td>'.format(chromo_table)
		table += '</tr>'
	table += '</table>'
	return table


#======================================
def draw_meiosis_chromosome(chromosome1, color='red', scale=2.4, centromere_width=32):
	table = ''
	table += '<table style="border-collapse: collapse; border: 0px solid white; height: 30px">'
	distance = CHROMOSOME_LENGTHS[chromosome1]
	table += '<colgroup width="{0}"></colgroup>'.format(distance[0] * scale - centromere_width / 2)
	table += '<colgroup width="{0}"></colgroup>'.format(centromere_width)
	table += '<colgroup width="{0}"></colgroup>'.format(distance[1] * scale - centromere_width / 2)
	table += '<tr>'
	table += f'<td bgcolor="{COLOR_SCALES[color][2]}" style="border: 2px solid black;" align="center"><span style="font-size: small"></span></td>'
	table += f'<td bgcolor="{COLOR_SCALES[color][1]}" style="border: 4px solid black;" align="center">{chromosome1}</td>'
	table += f'<td bgcolor="{COLOR_SCALES[color][2]}" style="border: 2px solid black;" align="center"><span style="font-size: large"></span></td>'
	table += '</tr>'
	table += '</table>'
	return table


#======================================
def draw_translocated_chromosome(chromosome1, chromosome2, color1='red', color2='blue', scale_main=2.4, scale_trans=1.2, centromere_width=32):
	table = ''
	table += '<table style="border-collapse: collapse; border: 0px solid white; height: 30px">'
	distance1 = CHROMOSOME_LENGTHS[chromosome1]
	distance2 = CHROMOSOME_LENGTHS[chromosome2]
	table += '<colgroup width="{0}"></colgroup>'.format(distance1[0] * scale_main - centromere_width / 2)
	table += '<colgroup width="{0}"></colgroup>'.format(centromere_width)
	table += '<colgroup width="{0}"></colgroup>'.format(distance1[1] * scale_trans - centromere_width / 4)
	table += '<colgroup width="{0}"></colgroup>'.format(distance2[1] * scale_trans - centromere_width / 4)
	table += '<tr>'
	table += f'<td bgcolor="{COLOR_SCALES[color1][2]}" style="border: 2px solid black;" align="center"><span style="font-size: large"></span></td>'
	table += f'<td bgcolor="{COLOR_SCALES[color1][1]}" style="border: 4px solid black;" align="center">{chromosome1}</td>'
	table += f'<td bgcolor="{COLOR_SCALES[color1][2]}" style="border: 2px solid black; border-right: 1px dashed black" align="center"><span style="font-size: large"></span></td>'
	table += f'<td bgcolor="{COLOR_SCALES[color2][2]}" style="border: 2px solid black; border-left: 1px dashed black" align="center"><span style="font-size: large"></span></td>'
	table += '</tr>'
	table += '</table>'
	return table


#======================================
def draw_robertsonian_chromosome(chromosome1, chromosome2, color1='coral', color2='deepskyblue', scale=3, centromere_width=24):
	table = ''
	table += '<table style="border-collapse: collapse; border: 0px solid white; height: 30px">'
	distance1 = CHROMOSOME_LENGTHS[chromosome1]
	distance2 = CHROMOSOME_LENGTHS[chromosome2]
	table += '<colgroup width="{0}"></colgroup>'.format(distance1[1] * scale - centromere_width / 2)
	table += '<colgroup width="{0}"></colgroup>'.format(centromere_width)
	table += '<colgroup width="{0}"></colgroup>'.format(distance2[1] * scale - centromere_width / 2)
	table += '<tr>'
	table += '<td bgcolor="{1}"  style="border: 2px solid black;" align="center"><span style="font-size: small">{0}q</span></td>'.format(
		chromosome1, color1
	)
	table += '<td bgcolor="SlateGray" style="border: 4px solid black;"></td>'
	table += '<td bgcolor="{1}"   style="border: 2px solid black;" align="center"><span style="font-size: small">{0}q</span></td>'.format(
		chromosome2, color2
	)
	table += '</tr>'
	table += '</table>'
	return table


#======================================
def draw_robertsonian_single_chromosome(chromosome1, color='coral', scale=3, centromere_width=24):
	table = ''
	table += '<table style="border-collapse: collapse; border: 0px solid white; height: 30px">'
	distance = CHROMOSOME_LENGTHS[chromosome1]
	table += '<colgroup width="{0}"></colgroup>'.format(distance[0] * scale - centromere_width / 2)
	table += '<colgroup width="{0}"></colgroup>'.format(centromere_width)
	table += '<colgroup width="{0}"></colgroup>'.format(distance[1] * scale - centromere_width / 2)
	table += '<tr>'
	table += '<td bgcolor="{1}"  style="border: 2px solid black;" align="center"><span style="font-size: small">{0}p</span></td>'.format(
		chromosome1, color
	)
	table += '<td bgcolor="SlateGray" style="border: 4px solid black;"></td>'
	table += '<td bgcolor="{1}"   style="border: 2px solid black;" align="center"><span style="font-size: small">{0}q</span></td>'.format(
		chromosome1, color
	)
	table += '</tr>'
	table += '</table>'
	return table
