#General Toosl for These Problems
import re
import sys
import copy
import crcmod.predefined


#=======================
def test():
	sys.stderr.write("good job")


#=======================
def getCrc16_FromString(mystr):
	crc16 = crcmod.predefined.Crc('xmodem')
	crc16.update(mystr.encode('ascii'))
	return crc16.hexdigest().lower()

#=====================
def makeQuestionPretty(question):
	pretty_question = copy.copy(question)
	#print(len(pretty_question))
	pretty_question = re.sub('\<table.+\<\/table\>', '[TABLE]\n', pretty_question)
	#print(len(pretty_question))
	pretty_question = re.sub('\<\/p\>\s*\<p\>', '\n', pretty_question)
	#print(len(pretty_question))
	return pretty_question

#=====================
def formatBB_MC_Question(N, question, choices_list, answer):
	bb_question = ''

	#number = "{0}. ".format(N)
	crc16 = getCrc16_FromString(question)
	bb_question += 'MC\t<p>{0}. {1}</p> {2}'.format(N, crc16, question)
	pretty_question = makeQuestionPretty(question)
	print('{0}. {1} -- {2}'.format(N, crc16, pretty_question))

	answer_count = 0

	letters = 'ABCDEFGH'
	for i, choice in enumerate(choices_list):
		bb_question += '\t{0}.  {1}&nbsp; '.format(letters[i], choice)
		if choice == answer:
			prefix = 'x'
			bb_question += '\tCorrect'
			answer_count += 1
		else:
			prefix = ' '
			bb_question += '\tIncorrect'
		print("- [{0}] {1}. {2}".format(prefix, letters[i], makeQuestionPretty(choice)))
	print("")
	if answer_count != 1:
		print("Wrong answer count {0}".format(answer_count))
		sys.exit(1)
	return bb_question + '\n'