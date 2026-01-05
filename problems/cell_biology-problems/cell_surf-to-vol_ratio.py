#!/usr/bin/env python3

import random

import bptools

debug = False

color_wheel = bptools.default_color_wheel(4)
#print(color_wheel)

#======================================
#======================================
def averageRand(n=3):
	sumr = 0.0
	for i in range(n):
		sumr += random.random()
	return sumr/float(n)

#======================================
#======================================
def processCell(cell):
	cell['surf'] = round(cell['surf'], 2)
	cell['vol'] = round(cell['vol'], 2)
	cell['ratio'] = round(cell['surf']/cell['vol'],2)
	return cell

#======================================
#======================================
def makeCells():
	base_volume = 15 * averageRand(5)
	#======================================
	big_volume = {
		'answer': False,
		'vol': base_volume * (2 + averageRand(5)),
		'surf': (3*(4 + averageRand(5))*base_volume)**(2/3.),
		'desc': 'the largest volume to allow wastes to easily diffuse through the plasma membrane.',
		}
	processCell(big_volume)
	#======================================
	big_surface = {
		'answer': False,
		'vol': base_volume * (1 + averageRand(5)),
		'surf': (4*(4 + averageRand(5))*base_volume)**(2/3.),
		'desc': 'the largest surface area which will enable it to eliminate all of its wastes quickly.',
		}
	processCell(big_surface)
	#======================================
	ideal_ratio = {
		'answer': True,
		'vol': base_volume,
		'surf': (16*base_volume)**(2/3.),
		'desc': 'the highest surface area-to-volume ratio which facilitates the exchange of materials between a cell and its environment.',
		}
	processCell(ideal_ratio)
	#======================================
	small_volume = {
		'answer': False,
		'vol': base_volume * averageRand(8),
		'surf': base_volume * averageRand(8),
		'desc': 'the smallest volume and will not produce as much waste as the other cells.',
		}
	if small_volume['vol'] > small_volume['surf']:
		a = small_volume['vol']
		small_volume['vol'] = small_volume['surf']
		small_volume['surf'] = a
	processCell(small_volume)
	#======================================
	cells = [big_volume, big_surface, ideal_ratio, small_volume]

	volume_list = []
	surf_list = []
	ratio_list = []
	for cell in cells:
		volume_list.append(cell['vol'])
		surf_list.append(cell['surf'])
		ratio_list.append(cell['ratio'])
	if big_volume['vol'] != max(volume_list):
		print('fail big volume')
		return None
	if small_volume['vol'] != min(volume_list):
		print('fail small volume')
		return None
	if ideal_ratio['ratio'] != max(ratio_list):
		print('fail ideal ratio')
		return None
	if big_surface['surf'] != max(surf_list):
		print('fail big surface')
		return None
	if min(ratio_list) < 1.0:
		print('fail too small ratio')
		return None

	if debug is True:
		print('big_volume ', big_volume)
		print('big_surface', big_surface)
		print('ideal_ratio', ideal_ratio)
		print('small_volum', small_volume)

	return cells

#======================================
#======================================
def makeTable(cells):
	center_style = 'style="text-align: center; background-color: #ced4d9; vertical-align: middle; border-style: solid; border-width: 1px;"'
	table = '<table border="2px" cellpadding="10" cellspacing="10" style="border-collapse: collapse; border-color: #000000; border-style: solid;">'
	table += ' <tr><th {0}><i>name</i></th>'.format(center_style)
	table += '  <th {0}>Volume<br/>(&mu;m<sup>3</sup>)</th> '.format(center_style)
	table += '  <th {0}>Surface area<br/>(&mu;m<sup>2</sup>)</th> '.format(center_style)
	table += '  <th {0}>SA-to-V<br/>ratio</th> '.format(center_style)
	table += ' </tr> '
	num = 1
	more_style = 'vertical-align: middle; border-style: solid; border-width: 2px; border-color: #000000;'

	for cell in cells:
		table += '<tr>'
		table += ' <td style="{1}"><strong><span style="color: #{0};">Cell {2:d}</span></strong></td>'.format(
			color_wheel[num-1], more_style, num)
		table += ' <td style="text-align: right; {0}">{1:.1f}</td>'.format(more_style, cell['vol'])
		table += ' <td style="text-align: right; {0}">{1:.1f}</td>'.format(more_style, cell['surf'])
		table += ' <td style="text-align: right; {0}">{1:.1f}</td>'.format(more_style, cell['ratio'])
		table += '</tr>'
		num += 1
	table += '</table><br/>'
	return table

#======================================
#======================================
def makeChoices(cells):
	choices_list = []
	#answer
	num = 1
	transitions = ['because it has', 'as it has', 'with', 'having',
		'characterized by', 'given it has']
	random.shuffle(transitions)
	for cell in cells:
		choice_text = '<strong><span style="color: #{0}">Cell {1:d}</span></strong> '.format(
			color_wheel[num-1], num)
		choice_text += transitions.pop() + " "
		choice_text += cell['desc']
		#=====================
		choices_list.append(choice_text)
		if cell['answer'] is True:
			answer = choice_text
		num += 1
	return choices_list, answer

#======================================
#======================================
def write_question(N, args):
	cells = None
	while cells is None:
		cells = makeCells()
	random.shuffle(cells)

	table = makeTable(cells)
	choices_list, answer = makeChoices(cells)

	question = '<span style="font-size: 13pt;">'
	question += 'Which one of the following cells will be able to eliminate waste most efficiently? and why?'
	question += '</span>'

	question_text = table+question
	bb_question = bptools.formatBB_MC_Question(N, question_text, choices_list, answer)
	return bb_question

#======================================
#======================================
#======================================
#======================================
def parse_arguments():
	parser = bptools.make_arg_parser(description='Generate surface area to volume questions.')
	args = parser.parse_args()
	return args

#======================================
#======================================
def main():
	args = parse_arguments()
	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)


#======================================
#======================================
if __name__ == "__main__":
	main()


#======================================
#======================================
