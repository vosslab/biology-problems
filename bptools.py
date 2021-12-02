#General Toosl for These Problems
import re
import sys
import copy
import crcmod.predefined

answer_histogram = {}

#=======================
def test():
	sys.stderr.write("good job")

#=====================
def getGeneLetters(length, shift=0):
	all_lowercase = "abcdefghijklmnopqrstuvwxyz"
	lowercase =     "abcdefghjkmnpqrstuwxyz"
	shift = shift % (len(lowercase) - length + 1)
	gene_string = lowercase[shift:shift+length]
	gene_list = list(gene_string)
	return gene_list

#=======================
def getCrc16_FromString(mystr):
	crc16 = crcmod.predefined.Crc('xmodem')
	crc16.update(mystr.encode('ascii'))
	return crc16.hexdigest().lower()

#=====================
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
	pretty_question = re.sub('\<hr\/\>', '', pretty_question)
	pretty_question = re.sub('\<\/p\>\s*\<p\>', '\n', pretty_question)
	pretty_question = re.sub('\<p\>\s*\<\/p\>', '\n', pretty_question)
	pretty_question = re.sub('\n\<\/p\>', '', pretty_question)	
	pretty_question = re.sub('\n\<p\>', '\n', pretty_question)	
	pretty_question = re.sub('\n\n', '\n', pretty_question)

	#print(len(pretty_question))
	return pretty_question

#=====================
def formatBB_MC_Question(N, question, choices_list, answer):
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
def print_histogram():
	sys.stderr.write("=== Answer Choice Histogram ===\n")
	keys = list(answer_histogram.keys())
	keys.sort()
	for key in keys:
		sys.stderr.write("{0}: {1},  ".format(key, answer_histogram[key]))
	sys.stderr.write("\n")


