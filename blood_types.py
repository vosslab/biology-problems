#!/usr/bin/env python

import math
import random

"""
<table style="border-collapse: collapse; border: 1px; border-color: black;">
<tbody>
<tr>
<td><span style="font-size: 100px; color: red;">●</span></td>
<td> </td>
<td>
<table style="border-collapse: collapse; border: 0px; border-color: white;">
<tbody>
<tr>
<td style="border-color: white;"><span style="font-size: 20px; color: darkred;">●</span></td>
<td style="border-color: white;"> </td>
<td style="border-color: white;"> </td>
</tr>
<tr>
<td style="border-color: white;"> </td>
<td style="border-color: white;"> </td>
<td style="border-color: white;"><span style="font-size: 20px; color: darkred;">●</span></td>
</tr>
<tr>
<td style="border-color: white;"><span style="font-size: 20px; color: darkred;">●</span></td>
<td style="border-color: white;"> </td>
<td style="border-color: white;"> </td>
</tr>
<tr>
<td style="border-color: white;"> </td>
<td style="border-color: white;"> </td>
<td style="border-color: white;"><span style="font-size: 20px; color: darkred;">●</span></td>
</tr>
</tbody>
</table>
</td>
<td> </td>
<td><span style="font-size: 100px; color: red;">●</span></td>
<td> </td>
</tr>
<tr>
<td> A antigen</td>
<td> </td>
<td> B antigen</td>
<td> </td>
<td> D antigen</td>
</tr>
</tbody>
</table>
"""

code2type = {
	'111':	'O-',
	'011':	'A-',
	'101':	'B-',
	'001':	'AB-',
	'110':	'O+',
	'010':	'A+',
	'100':	'B+',
	'000':	'AB+',
}

image_map = {
	'1111':	'https://blackboard.roosevelt.edu/courses/1/DZ.202110/assessment/f32af4a2a23346db8be715e65e318070/type-001.jpg.jpg',
	'1110':	'https://blackboard.roosevelt.edu/courses/1/DZ.202110/assessment/f7bc2b94ee7841b6bddd95ec41ad1898/type-002.jpg.jpg',
	'1101':	'https://blackboard.roosevelt.edu/courses/1/DZ.202110/assessment/78c31a20904d4845a3e26e22ebfab351/type-003.jpg.jpg',
	'1100':	'https://blackboard.roosevelt.edu/courses/1/DZ.202110/assessment/4aae814e94c34de5b7ac27b28d66ad9e/type-004.jpg.jpg',
	'1011':	'https://blackboard.roosevelt.edu/courses/1/DZ.202110/assessment/dc670c986139491492a9c93b35f5c5fa/type-005.jpg.jpg',
	'1010':	'https://blackboard.roosevelt.edu/courses/1/DZ.202110/assessment/ab104aea9b8d49908b0219b763218fc1/type-006.jpg.jpg',
	'1001':	'https://blackboard.roosevelt.edu/courses/1/DZ.202110/assessment/3c2cef5262a346a09bda64056a2cd963/type-007.jpg.jpg',
	'1000':	'https://blackboard.roosevelt.edu/courses/1/DZ.202110/assessment/32b575cc52c94d43b90a87e5656e7a53/type-008.jpg.jpg',
	'0111':	'https://blackboard.roosevelt.edu/courses/1/DZ.202110/assessment/be798d30298b4c05a35accde21755060/type-009.jpg.jpg',
	'0110':	'https://blackboard.roosevelt.edu/courses/1/DZ.202110/assessment/123a073f39d5402f91d31128ca856656/type-010.jpg.jpg',
	'0101':	'https://blackboard.roosevelt.edu/courses/1/DZ.202110/assessment/203f08400f4547ada6e6bcdcd1c2d2ea/type-011.jpg.jpg',
	'0100':	'https://blackboard.roosevelt.edu/courses/1/DZ.202110/assessment/6895a61442ca4cf69f8adcd5d81d5ebe/type-012.jpg.jpg',
	'0011':	'https://blackboard.roosevelt.edu/courses/1/DZ.202110/assessment/e83517f2a6d84003bbab4c7f70d75d3a/type-013.jpg.jpg',
	'0010':	'https://blackboard.roosevelt.edu/courses/1/DZ.202110/assessment/be5dc8646e8a4ac9817a0c2d54e6f996/type-014.jpg.jpg',
	'0001':	'https://blackboard.roosevelt.edu/courses/1/DZ.202110/assessment/d9470c3d9aae4ee1b82960874740a38b/type-015.jpg.jpg',
	'0000':	'https://blackboard.roosevelt.edu/courses/1/DZ.202110/assessment/024944166fb84fcb8848eb5cf1e5c413/type-016.jpg.jpg',
}

def getInvertCode(bcode):
	invert = bcode
	invert = invert.replace('0', '2')
	invert = invert.replace('1', '0')
	invert = invert.replace('2', '1')
	return invert

def flipPlace(bcode, place=3):
	newcode = bcode[:place-1]
	newcode += getInvertCode(bcode[place-1])
	newcode += bcode[place:]
	return newcode

def getWrongChoices(bcode):
	invert = getInvertCode(bcode)
	choices = []
	choices.append(bcode+'1')
	choices.append(bcode+'0')
	choices.append(invert+'1')
	choices.append(invert+'0')
	extras = []
	for choice in choices:
		extras.append(flipPlace(choice, 3))
	random.shuffle(extras)
	#choices.extend(extras)
	choices.append(extras.pop())
	choices.append(extras.pop())
	random.shuffle(choices)
	return choices

def code2display(bcode):
	display_txt = bcode
	display_txt = display_txt.replace("0", "%")
	display_txt = display_txt.replace("1", "O")
	return display_txt

if __name__ == '__main__':
	bcodes = list(code2type.keys())
	N = 0
	letters = "ABCDEFG"
	for bcode in bcodes:
		N += 1
		answer = bcode+"1"
		choices = getWrongChoices(bcode)
		question = "{0}. ".format(N)
		question += "What will the results of a blood test look like for a person "
		question += "with <b>{0} blood type</b>?".format(code2type[bcode])
		print(question)
		i = 0
		for choice in choices:
			prefix = ""
			if choice == answer:
				prefix = '*'
			ltr = letters[i]
			imgfile = image_map[choice]
			display_txt = code2display(choice)
			choice_txt = "<p><img src='{0}' /></p><p>image of blood type result, looks like {1}</p>".format(imgfile, display_txt)
			print("{0}{1}. {2}".format(prefix, ltr, choice_txt))
			i += 1
		print("")
