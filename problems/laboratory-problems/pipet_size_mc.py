#!/usr/bin/env python3

import random
import bptools

###

# <table border="0"><tbody><tr><td style="vertical-align: middle;">P10</td><td style="vertical-align: middle;"><table border="1"><tbody><tr><td align="center"><span style="color: black;">0</span></td></tr><tr><td align="center"><span style="color: black;">2</span></td></tr><tr><td align="center"><span style="color: red;">3</span></td></tr></tbody></table></td></tr></tbody></table>

##=========================
pipet_choices = ['P10', 'P100', 'P1000']

##=========================
pipet_volume_multiplier = {
	'P10': 10,
	'P100': 1,
	'P1000': 0.1,
}

##=========================
pipet_volume_range = {
	'P10': [3,10],
	'P100': [30,100],
	'P1000': [300,1000],
}

##=========================
pipet_colors = {
	'P10': ['black', 'black', 'red',],
	'P100': ['black', 'black', 'black',],
	'P1000': ['red', 'black', 'black',],
}

##=========================
pipet_bg_colors = {
	'P10': '#f0f0f0',
	'P100': '#fff6d6',
	'P1000': '#dfefff',
}

##=========================
def get_volume(pipet):
	minvol, maxvol = pipet_volume_range[pipet]
	rawvolume = (maxvol - minvol)*random.random() + minvol
	volume = round(rawvolume, 1)
	if volume > 10:
		volume -= volume % 1
	if volume > 100:
		volume -= volume % 10
	rawdigits = get_raw_digits(volume, pipet)
	if rawdigits % 10 == 0:
		volume = get_volume(pipet)
	return volume

##=========================
def pipetstr(pipet, rawdigits):
	colors = pipet_colors[pipet]
	bg_color = pipet_bg_colors[pipet]

	digits = [0,0,0]
	digits[2] = rawdigits % 10
	digits[1] = (rawdigits % 100) // 10
	digits[0] = (rawdigits % 1000) // 100

	pipetstr = ''
	pipetstr += "<table border='0' cellpadding='0' cellspacing='6'><tbody><tr>"
	pipetstr += "<td style='vertical-align: middle;'>"
	pipetstr += (
		f"<span style='display: inline-block; width: 52px; height: 52px; "
		f"line-height: 52px; border-radius: 50%; border: 1px solid #333; "
		f"text-align: center; background-color: {bg_color}; "
		f"font-family: Arial, sans-serif; font-weight: bold;'>"
		f"{pipet.upper()}</span>"
	)
	pipetstr += "</td><td style='vertical-align: middle;'>"
	pipetstr += (
		f"<table border='0' cellpadding='2' cellspacing='0' "
		f"style='border-collapse: separate; border-spacing: 0; "
		f"border-radius: 10px 10px 6px 6px; overflow: hidden; "
		f"background-color: {bg_color}; border: 1px solid #333;'>"
		"<tbody>"
	)
	pipetstr += f"<tr><td align='center'><span style='color: {colors[0]};'>&nbsp;<strong>{digits[0]}</strong></span></td></tr>"
	pipetstr += f"<tr><td align='center'><span style='color: {colors[1]};'>&nbsp;<strong>{digits[1]}</strong></span></td></tr>"
	pipetstr += f"<tr><td align='center'><span style='color: {colors[2]};'><strong>{digits[2]}</strong></span></td></tr>"
	pipetstr += '</tbody></table></td></tr></tbody></table>'
	return pipetstr

##=========================
def get_raw_digits(volume, pipet):
	rawdigits = int(volume * pipet_volume_multiplier[pipet])
	return rawdigits

##=========================
def question_text(volume):
	# <p>Which pipet and setting would you use to pipet 230 &mu;L using only one step?</p>
	volume_text = f"<span style='font-family: monospace;'>{volume:.1f} &mu;L</span>"
	if volume > 10:
		volume_text = f"<span style='font-family: monospace;'>{volume:.0f} &mu;L</span>"
		question = "Which pipet and setting would you use to pipet {0} using only one step?".format(volume_text)
	else:
		question = "Which pipet and setting would you use to pipet {0} using only one step?".format(volume_text)
	return question

##=========================
def get_wrong_choices(volume, pipet):
	#if volume < 10:
	#	volume2 = volume * 100
	#elif volume < 100:
	#	volume2 = volume * 10
	#else:
	#	volume2 = volume // 10
	choices = []
	rawdigits1 = get_raw_digits(volume, pipet)
	if rawdigits1 < 100:
		rawdigits2 = get_raw_digits(volume*10, pipet)
	else:
		rawdigits2 = get_raw_digits(volume//10, pipet)

	for pipet in pipet_choices:
		for value in (rawdigits1, rawdigits2):
			choice_text = pipetstr(pipet, value)
			choice = {'text': choice_text, 'pipet': pipet, 'rawdigits': value,}
			choices.append(choice)
	return choices


##=========================
def write_question(N: int, args) -> str:
	pipet = random.choice(pipet_choices)
	volume = get_volume(pipet)
	rawdigits = get_raw_digits(volume, pipet)
	question = question_text(volume)
	choices = get_wrong_choices(volume, pipet)
	choices_list = []
	answer = None
	for choice in choices:
		if choice['pipet'] == pipet and choice['rawdigits'] == rawdigits:
			answer = choice['text']
		choices_list.append(choice['text'])
	if answer is None:
		return None
	bbf = bptools.formatBB_MC_Question(N, question, choices_list, answer)
	return bbf

def parse_arguments():
	parser = bptools.make_arg_parser(
		description="Generate pipet size questions."
	)
	args = parser.parse_args()
	return args

def main():
	args = parse_arguments()
	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)

if __name__ == '__main__':
	main()







