#!/usr/bin/env python3

import os
import re
import sys
import glob
import html
import random
import xmltodict

import bptools

#===============================
def XML2dict(filename):
	fileptr = open(filename, "r")
	raw_xml_content = fileptr.read()
	raw_xml_content = re.sub('\n', '', raw_xml_content)
	xml_dict = xmltodict.parse(raw_xml_content)
	return xml_dict, raw_xml_content

#===============================
def processQuestion(N, filename):
	xmldict, raw_xml_content = XML2dict(filename)
	raw_xml_content = re.sub('<span[^>]*>', '', raw_xml_content)
	raw_xml_content = re.sub('</span>', '', raw_xml_content)
	raw_xml_content = re.sub('&#xa0;', ' ', raw_xml_content)

	#print(raw_xml_content)

	#ANSWER ID
	answer_text_id = xmldict['assessmentItem']['responseDeclaration']['correctResponse']['value']
	#print(answer_text_id)
	m = re.search('answer_([0-9]+)', answer_text_id)
	answer_index = int(m.groups()[0]) - 1
	#question_text = ''.join(xmldict['assessmentItem']['itemBody'])
	
	#QUESTION
	m = re.search('<itemBody><div>(.+)</div><choiceInteraction ', raw_xml_content)
	#print(m)
	question_text = m.groups()[0]
	if '<img ' in question_text:
		return None
	question_text_data = question_text.encode('ascii', 'xmlcharrefreplace')
	question_text = question_text_data.decode('ascii')
	#print(question_text)
	
	#CHOICES
	choices_list = []
	m = re.search('<choiceInteraction [^>]*>(.*)</choiceInteraction>', raw_xml_content)
	choice_content = m.groups()[0]
	#print(choice_content)
	simpleChoices = choice_content.split('</simpleChoice>')
	#print(simpleChoices)
	for i, data in enumerate(simpleChoices):
		if len(data) == 0:
			continue
		m = re.search('<simpleChoice identifier="answer_{0}" fixed="true">([^"]*)'.format(i+1), data)
		if m is None:
			break
		choice_text = m.groups()[0].strip()
		if '<img ' in choice_text:
			return None
		choice_text_data = choice_text.encode('ascii', 'xmlcharrefreplace')
		choice_text = choice_text_data.decode('ascii')
		choices_list.append(choice_text)
	if len(choices_list) <= 1:
		return None
	#print(choices_list)
	try:
		answer_text = choices_list[answer_index]
	except IndexError:
		print(choices_list)
		print(answer_index)
		sys.exit(1)
	#print(answer_text)
	random.shuffle(choices_list)
	return question_text, choices_list, answer_text

#===============================
#===============================
if __name__ == '__main__':
	filename = None
	if len(sys.argv) == 1 and os.path.isdir('qti21'):
		filenames = glob.glob('qti21/assessmen*.xml')
		filenames.sort()
	elif len(sys.argv) >= 2:
		filenames = [sys.argv[1], ]
	else:
		print("Usage: {0} <file.xml>".format(os.path.basename(__file__)))
	if not os.path.isfile(filenames[0]):
		print("Usage: {0} <file.xml>".format(os.path.basename(__file__)))

	N = 0
	skip_list = []
	f = open('readable_questions.txt', 'w')
	for filename in filenames:
		print(filename)
		N += 1
		N = int(filename[-9:-4])
		formatted_question = processQuestion(N, filename)
		if formatted_question is not None:
			f.write(formatted_question)
		else:
			skip_list.append(filename)
	f.close()
	print(skip_list)
	bptools.print_histogram()
