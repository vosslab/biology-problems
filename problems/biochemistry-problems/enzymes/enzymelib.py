import sys
import random

#======================================
def makeEnzymeHTMLTable(enzyme_tree):
	tc_style = 'align="center" style="vert-align: middle; border: solid black 1px"'
	#pH_style = 'align="left" style="vert-align: middle; border: solid black 1px"'
	table = '<table border="0" style="border-collapse: collapse; border: white solid 0px; width: 400px;"'
	table += '>'
	table += '<tr>'
	table += '  <th {0}>Enzyme</th>'.format(tc_style)
	table += '  <th {0}>Effective<br/>Temperature<br/>Range (&deg;C)</th>'.format(tc_style)
	table += '  <th {0}>Optimum<br/>pH</th>'.format(tc_style)
	table += '</tr>'
	for enzyme_dict in enzyme_tree:
		table += '<tr>'
		table += '  <td {0}>{1}</td>'.format(tc_style, enzyme_dict['name'])
		table += '  <td {0}>{1}&ndash;{2}</td>'.format(tc_style, enzyme_dict['temp1'], enzyme_dict['temp2'])
		table += '  <td {0}>{1:.1f}&nbsp;</td>'.format(tc_style, enzyme_dict['optim_pH'])
		table += '</tr>'
	table += '</table>  '
	return table

#======================================
def makeEnzymeTree(N):
	pH_values   = list(range( 1, 11, 1))
	temp_values = list(range(15, 76, 5))
	temp_jumps = [8, 10, 10, 12, 15, 18]
	enzyme_names = list('ABCD')

	enzyme_tree = []
	for i, ename in enumerate(enzyme_names):

		random.shuffle(pH_values)
		pH = pH_values.pop()
		try:
			pH_values.remove(pH+1)
		except ValueError:
			pass
		try:
			pH_values.remove(pH-1)
		except ValueError:
			pass

		random.shuffle(temp_values)
		random.shuffle(temp_jumps)
		try:
			temp1 = temp_values.pop()
			jump = temp_jumps.pop()

		except IndexError:
			if ename != 'D':
				print("this is bad")
				sys.exit(1)
			temp1 = 10
			#print(N, "force temp = 10")
			jump = 7
		temp2 = temp1 + jump
		if temp2 > 85:
			temp2 = 85
		for t in range(temp1-5, temp2+2, 5):
			try:
				temp_values.remove(t)
			except ValueError:
				pass

		enzyme_dict = {
			'name': ename,
			'optim_pH': pH,
			'temp1': temp1,
			'temp2': temp2,
			}
		enzyme_tree.append(enzyme_dict)
	return enzyme_tree
