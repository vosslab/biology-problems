#!/usr/bin/env python3

import random

import bptools

base_colors = ['violet', 'indigo', 'blue', 'green', 'yellow', 'orange', 'red']

wavelengths = (410, 430, 460, 530, 580, 600, 700,)

html_colors = ('#9d159d', '#4a0080', '#000080', '#006600', '#b3b300', '#e63900', '#990000')

leaf_colors = {
	'reddish yellow':     ('red', 'orange', 'yellow',),
	'orangeish yellow':   ('orange', 'yellow',),
	'yellowish green':    ('yellow', 'green',),
	'yellowish blue':     ('yellow', 'green', 'blue',),
	'greenish blue':      ('green', 'blue',),
	'blue and violet':    ('blue', 'violet',),
}

#==================================
def colorHtml(color_name):
	color_id = base_colors.index(color_name)
	wavelength = wavelengths[color_id]
	color_code = html_colors[color_id]
	return f'<span style="color: {color_code}"><strong>{color_name}</strong> ({wavelength:d} nm)</span>'

#==================================
def writeChoice(name1, name2):
	return f"{colorHtml(name1)} and {colorHtml(name2)} "

#==================================
def colorDescription(leaf_color):
	mycolors = leaf_color.split(' ')
	and_text = None
	if len(mycolors) == 2:
		color1, color2 = mycolors
	elif len(mycolors) == 3:
		color1, and_text, color2 = mycolors
	color1true = color1.replace('dish', '')
	color1true = color1true.replace('ish', '')
	color_index1 = base_colors.index(color1true)
	color_index2 = base_colors.index(color2)
	html_text = f'<strong><span style="color: {html_colors[color_index1]}">{color1}</span> '
	if and_text is not None:
		html_text += 'and '
	html_text += f'<span style="color: {html_colors[color_index2]}">{color2}</span></strong>'
	return html_text

#==================================
#==================================
#==================================
def build_question(leaf_color):
	color_desc = colorDescription(leaf_color)
	question = ""
	question += f"<p>A plant with unique photosynthetic pigments has leaves that appear {color_desc}.</p>"
	question += "<p>Which one of the following wavelengths of visible light "
	question += "would most effectively be absorbed by this pigment?</p>"

	wrong_colors = leaf_colors[leaf_color]
	good_color_map = [True] * len(base_colors)
	for color in wrong_colors:
		color_index = base_colors.index(color)
		if color_index - 1 > 0:
			good_color_map[color_index - 1] = False
		good_color_map[color_index] = False
		if color_index + 1 < len(good_color_map):
			good_color_map[color_index + 1] = False

	answer_colors = []
	for i, v in enumerate(good_color_map):
		if v is True:
			answer_colors.append(base_colors[i])

	indices = random.sample(range(len(answer_colors)), 2)
	indices.sort()
	a1 = answer_colors[indices[0]]
	a2 = answer_colors[indices[1]]
	answer = writeChoice(a1, a2)

	choices_list = []
	for i in range(10):
		names = [random.choice(answer_colors), random.choice(wrong_colors)]
		random.shuffle(names)
		wrong_choice = writeChoice(names[0], names[1])
		choices_list.append(wrong_choice)
	choices_list = list(set(choices_list))
	random.shuffle(choices_list)
	choices_list = choices_list[:3]
	choices_list.append(answer)
	random.shuffle(choices_list)
	return question, choices_list, answer

#==================================
def write_question(N: int, args) -> str:
	leaf_color = random.choice(list(leaf_colors.keys()))
	question_text, choices_list, answer = build_question(leaf_color)
	return bptools.formatBB_MC_Question(N, question_text, choices_list, answer)

#==================================
def parse_arguments():
	parser = bptools.make_arg_parser(description="Generate photosynthetic light pigment questions.")
	args = parser.parse_args()
	return args

#==================================
def main():
	args = parse_arguments()
	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)

if __name__ == '__main__':
	main()
