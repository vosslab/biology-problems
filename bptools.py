#General Toosl for These Problems
import re
import sys
import copy
import yaml
import colorsys
import crcmod.predefined

answer_histogram = {}

#=======================
def test():
	sys.stderr.write("good job")

#==========================
#==========================
#==========================
# special loader with duplicate key checking
class UniqueKeyLoader(yaml.SafeLoader):
	def construct_mapping(self, node, deep=False):
		mapping = []
		for key_node, value_node in node.value:
			key = self.construct_object(key_node, deep=deep)
			if key in mapping:
				print("DUPLICATE KEY: ", key)
				raise AssertionError("DUPLICATE KEY: ", key)
			mapping.append(key)
		return super().construct_mapping(node, deep)

#=======================
def readYamlFile(yaml_file):
	print("Processing file: ", yaml_file)
	yaml.allow_duplicate_keys = False
	yaml_pointer = open(yaml_file, 'r')
	#data = UniqueKeyLoader(yaml_pointer)
	#help(data)
	yaml_text = yaml_pointer.read()
	data = yaml.load(yaml_text, Loader=UniqueKeyLoader)
	#data = yaml.safe_load(yaml_pointer)
	yaml_pointer.close()
	return data

#==========================
#==========================
#==========================
def make_color_wheel(r, g, b, degree_step=40): # Assumption: r, g, b in [0, 255]
	r, g, b = map(lambda x: x/255., [r, g, b]) # Convert to [0, 1]
	#print(r, g, b)
	hue, l, s = colorsys.rgb_to_hls(r, g, b)     # RGB -> HLS
	#print(hue, l, s)
	wheel = []
	for deg in range(0, 359, degree_step):
		hue_i = (hue*360. + float(deg))/360.
		#print(hue_i, l, s)
		ryb_percent_color = colorsys.hls_to_rgb(hue_i, l, s)
		#print(ryb_percent_color)
		rgb_percent_color = _ryb_to_rgb(*ryb_percent_color)
		rgb_color = tuple(map(lambda x: int(round(x*255)), rgb_percent_color))
		hexcolor = '%02x%02x%02x' % rgb_color
		wheel.append(hexcolor)
	return wheel

#==========================
def _cubic(t, a, b):
	weight = t * t * (3 - 2*t)
	return a + weight * (b - a)

#==========================
def _ryb_to_rgb(r, y, b): # Assumption: r, y, b in [0, 1]
	# red
	x0, x1 = _cubic(b, 1.0, 0.163), _cubic(b, 1.0, 0.0)
	x2, x3 = _cubic(b, 1.0, 0.5), _cubic(b, 1.0, 0.2)
	y0, y1 = _cubic(y, x0, x1), _cubic(y, x2, x3)
	red = _cubic(r, y0, y1)
	# green
	x0, x1 = _cubic(b, 1.0, 0.373), _cubic(b, 1.0, 0.66)
	x2, x3 = _cubic(b, 0., 0.), _cubic(b, 0.5, 0.094)
	y0, y1 = _cubic(y, x0, x1), _cubic(y, x2, x3)
	green = _cubic(r, y0, y1)
	# blue
	x0, x1 = _cubic(b, 1.0, 0.6), _cubic(b, 0.0, 0.2)
	x2, x3 = _cubic(b, 0.0, 0.5), _cubic(b, 0.0, 0.0)
	y0, y1 = _cubic(y, x0, x1), _cubic(y, x2, x3)
	blue = _cubic(r, y0, y1)
	# return
	return (red, green, blue)

#=====================
#=====================
#=====================
def getGeneLetters(length, shift=0):
	all_lowercase = "abcdefghijklmnopqrstuvwxyz"
	lowercase =     "abcdefghjkmnpqrstuwxyz"
	shift = shift % (len(lowercase) - length + 1)
	gene_string = lowercase[shift:shift+length]
	gene_list = list(gene_string)
	return gene_list

#==========================
#==========================
#==========================
def getCrc16_FromString(mystr):
	crc16 = crcmod.predefined.Crc('xmodem')
	crc16.update(mystr.encode('ascii'))
	return crc16.hexdigest().lower()

#==========================
def makeQuestionPretty(question):
	pretty_question = copy.copy(question)
	#print(len(pretty_question))
	pretty_question = re.sub('\<table .+\<\/table\>', '[TABLE]\n', pretty_question)
	pretty_question = re.sub('\<table .*\<\/table\>', '[TABLE]\n', pretty_question)
	if 'table' in pretty_question:
		print("MISSED A TABLE")
		print(pretty_question)
		#sys.exit(1)
		pass
	#print(len(pretty_question))
	pretty_question = re.sub('&nbsp;', ' ', pretty_question)
	pretty_question = re.sub('h[0-9]\>', 'p>', pretty_question)
	pretty_question = re.sub('<br/>', '\n', pretty_question)
	pretty_question = re.sub('<span [^>]*>', ' ', pretty_question)
	pretty_question = re.sub('</span>', '', pretty_question)
	pretty_question = re.sub('\<hr\/\>', '', pretty_question)
	pretty_question = re.sub('\<\/p\>\s*\<p\>', '\n', pretty_question)
	pretty_question = re.sub('\<p\>\s*\<\/p\>', '\n', pretty_question)
	pretty_question = re.sub('\n\<\/p\>', '', pretty_question)
	pretty_question = re.sub('\n\<p\>', '\n', pretty_question)
	pretty_question = re.sub('\n\n', '\n', pretty_question)

	#print(len(pretty_question))
	return pretty_question

#==========================
#==========================
#==========================
def formatBB_MC_Question(N, question, choices_list, answer):
	if len(choices_list) <= 1:
		print("not enough choices to choose from, you need two choices for multiple choice")
		print("answer=", answer)
		print("choices_list=", choices_list)
		sys.exit(1)

	bb_question = ''
	#number = "{0}. ".format(N)
	crc16 = getCrc16_FromString(question)
	bb_question += 'MC\t<p>{0:03d}. {1}</p> {2}'.format(N, crc16, question)
	pretty_question = makeQuestionPretty(question)
	print('{0:03d}. {1} -- {2}'.format(N, crc16, pretty_question))

	answer_count = 0

	letters = 'ABCDEFGHJKMNPQRSTUWXYZ'
	for i, choice in enumerate(choices_list):
		bb_question += '\t{0}.  {1}&nbsp; '.format(letters[i], choice)
		if choice == answer:
			prefix = 'x'
			bb_question += '\tCorrect'
			answer_count += 1
			answer_histogram[letters[i]] = answer_histogram.get(letters[i], 0) + 1
		else:
			prefix = ' '
			bb_question += '\tIncorrect'
		print("- [{0}] {1}. {2}".format(prefix, letters[i], makeQuestionPretty(choice)))
	print("")
	if answer_count != 1:
		print("Too many or few answers count {0}".format(answer_count))
		sys.exit(1)
	return bb_question + '\n'

#=====================
def formatBB_MA_Question(N, question, choices_list, answers_list):
	if len(choices_list) <= 1:
		print("not enough choices to choose from, you need two choices for multiple choice")
		print("answers_list=", answers_list)
		print("choices_list=", choices_list)
		sys.exit(1)

	bb_question = ''
	#number = "{0}. ".format(N)
	crc16 = getCrc16_FromString(question)
	bb_question += 'MA\t<p>{0:03d}. {1}</p> {2}'.format(N, crc16, question)
	pretty_question = makeQuestionPretty(question)
	print('{0:03d}. {1} -- {2}'.format(N, crc16, pretty_question))

	answer_count = 0

	letters = 'ABCDEFGHJKMNPQRSTUWXYZ'
	for i, choice in enumerate(choices_list):
		bb_question += '\t{0}.  {1}&nbsp; '.format(letters[i], choice)
		if choice in answers_list:
			prefix = 'x'
			bb_question += '\tCorrect'
			answer_count += 1
			answer_histogram[letters[i]] = answer_histogram.get(letters[i], 0) + 1
		else:
			prefix = ' '
			bb_question += '\tIncorrect'
		print("- [{0}] {1}. {2}".format(prefix, letters[i], makeQuestionPretty(choice)))
	print("")
	if answer_count == 0:
		print("No answer count {0}".format(answer_count))
		sys.exit(1)
	return bb_question + '\n'

#=====================
def formatBB_FIB_Question(N, question, answers_list):
	#fill in the black = FIB
	#FIB TAB question text TAB answer text TAB answer two text
	bb_question = ''

	#number = "{0}. ".format(N)
	crc16 = getCrc16_FromString(question)
	bb_question += 'FIB\t<p>{0:03d}. {1}</p> {2}'.format(N, crc16, question)
	pretty_question = makeQuestionPretty(question)
	print('{0:03d}. {1} -- {2}'.format(N, crc16, pretty_question))

	for i, answer in enumerate(answers_list):
		bb_question += '\t{0}'.format(answer)
		print("- {0}".format(makeQuestionPretty(answer)))
	print("")
	return bb_question + '\n'

#=====================
def formatBB_NUM_Question(N, question, answer, tolerance):
	#NUM TAB question text TAB answer TAB [optional]tolerance
	bb_question = ''

	#number = "{0}. ".format(N)
	crc16 = getCrc16_FromString(question)
	bb_question += 'NUM\t<p>{0:03d}. {1}</p> {2}'.format(N, crc16, question)
	pretty_question = makeQuestionPretty(question)
	print('{0:03d}. {1} -- {2}'.format(N, crc16, pretty_question))

	bb_question += '\t{0:.8f}'.format(answer)
	print("=== {0:.3f}".format(answer))
	bb_question += '\t{0:.8f}'.format(tolerance)
	print("+/- {0:.3f}".format(tolerance))
	print("")
	return bb_question + '\n'

#=====================
def formatBB_MAT_Question(N, question, answers_list, matching_list):
	#MAT TAB question text TAB answer text TAB matching text TAB answer two text TAB matching two text
	bb_question = ''

	if len(answers_list) > len(set(answers_list)):
		print(answers_list)
		print("Duplicate answers")
		sys.exit(1)
	if len(matching_list) > len(set(matching_list)):
		print(matching_list)
		print("Duplicate matches")
		sys.exit(1)

	#number = "{0}. ".format(N)
	crc16 = getCrc16_FromString(question + ''.join(answers_list) + ''.join(matching_list))
	bb_question += 'MAT\t<p>{0:03d}. {1}</p> {2}'.format(N, crc16, question)
	pretty_question = makeQuestionPretty(question)
	print('{0:03d}. {1} -- {2}'.format(N, crc16, pretty_question))

	num_items = min(len(answers_list), len(matching_list))
	letters = 'ABCDEFGHJKMNPQRSTUWXYZ'
	for i in range(num_items):
		answer = answers_list[i]
		match = matching_list[i]
		bb_question += '\t{0}&nbsp;\t{1}&nbsp;'.format(answer, match)
		print("- {0}. {1} == {2}".format(letters[i], makeQuestionPretty(answer), makeQuestionPretty(match)))
	print("")
	return bb_question + '\n'

#==========================
#==========================
#==========================
def print_histogram():
	sys.stderr.write("=== Answer Choice Histogram ===\n")
	keys = list(answer_histogram.keys())
	keys.sort()
	for key in keys:
		sys.stderr.write("{0}: {1},  ".format(key, answer_histogram[key]))
	sys.stderr.write("\n")


