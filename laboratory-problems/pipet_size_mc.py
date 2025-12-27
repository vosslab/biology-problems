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
		
	digits = [0,0,0]
	digits[2] = rawdigits % 10
	digits[1] = (rawdigits % 100) // 10
	digits[0] = (rawdigits % 1000) // 100
	print(digits)
	
	pipetstr = ''
	pipetstr += '<table border="0"><tbody><tr><td style="vertical-align: middle;"><strong>{0}</strong>'.format(pipet.upper())
	pipetstr += '</td><td style="vertical-align: middle;"><table border="1"><tbody>'
	pipetstr += '<tr><td align="center"><span style="color: {0};">&nbsp;<strong>{1}</strong></span></td></tr>'.format(colors[0], digits[0])
	pipetstr += '<tr><td align="center"><span style="color: {0};">&nbsp;<strong>{1}</strong></span></td></tr>'.format(colors[1], digits[1])
	pipetstr += '<tr><td align="center"><span style="color: {0};"><strong>{1}</strong></span></td></tr>'.format(colors[2], digits[2])
	pipetstr += '</tbody></table></td></tr></tbody></table>'
	return pipetstr
	
##=========================
def get_raw_digits(volume, pipet):
	rawdigits = int(volume * pipet_volume_multiplier[pipet])
	return rawdigits
	
##=========================
def question_text(volume):
	# <p>Which pipet and setting would you use to pipet 230 &mu;L using only one step?</p>
	if volume > 10:
		question = "Which pipet and setting would you use to pipet {0:.0f} &mu;L using only one step?".format(volume)
	else:
		question = "Which pipet and setting would you use to pipet {0:.1f} &mu;L using only one step?".format(volume)
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
def write_question_batch(start_num: int, args) -> list:
	questions = []
	remaining = None
	if args.max_questions is not None:
		remaining = args.max_questions - (start_num - 1)
		if remaining <= 0:
			return questions
	N = start_num
	for pipet in pipet_choices:
		volume = get_volume(pipet)
		rawdigits = get_raw_digits(volume, pipet)
		question = question_text(volume)
		choices = get_wrong_choices(volume, pipet)
		choices_list = []
		for choice in choices:
			if choice['pipet'] == pipet and choice['rawdigits'] == rawdigits:
				answer = choice['text']
			choices_list.append(choice['text'])
		bb_format = bptools.formatBB_MC_Question(N, question, choices_list, answer)
		questions.append(bb_format)
		N += 1
		if remaining is not None and len(questions) >= remaining:
			return questions
	return questions

def parse_arguments():
	parser = bptools.make_arg_parser(
		description="Generate pipet size questions.",
		batch=True
	)
	args = parser.parse_args()
	return args

def main():
	args = parse_arguments()
	outfile = bptools.make_outfile(None)
	questions = bptools.collect_question_batches(write_question_batch, args)
	bptools.write_questions_to_file(questions, outfile)

if __name__ == '__main__':
	main()

			


	
	
	
	
