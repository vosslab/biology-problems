#General Toosl for These Problems
import os
import re
import sys
import copy
import yaml
import random
import colorsys
import subprocess
import num2words #pip
import crcmod.predefined #pip

#anticheating measures
use_nocopy_script = False
use_insert_hidden_terms = True
use_add_no_click_div = True
noPrint = True
noCopy = True
noScreenshot = False
autoBlur = True

hidden_term_bank = None
answer_histogram = {}
question_count = 0
crc16_dict = {}

#=======================
def test():
	sys.stderr.write("good job")

#==========================
#==========================
#==========================
def number_to_ordinal(integer):
	return num2words.num2words(integer, to='ordinal', lang='en_US')
assert number_to_ordinal(3) == 'third'
#==========================
def number_to_cardinal(integer):
	return num2words.num2words(integer, to='cardinal', lang='en_US')
assert number_to_cardinal(3) == 'three'

#==========================
#==========================
#==========================
# special loader with duplicate key checking
class UniqueKeyLoader(yaml.SafeLoader):
	def construct_mapping(self, node, deep=False):
		mapping = {}
		for key_node, value_node in node.value:
			key = self.construct_object(key_node, deep=deep)
			if isinstance(key, str):
				if mapping.get(key) is True:
					print("DUPLICATE KEY: ", key)
					raise AssertionError("DUPLICATE KEY: ", key)
				mapping[key] = True
			else:
				raise NotImplementedError
		return super().construct_mapping(node, deep)

#=======================
def readYamlFile(yaml_file):
	print("Processing file: ", yaml_file)
	yaml.allow_duplicate_keys = False
	yaml_file_pointer = open(yaml_file, 'r')
	#data = UniqueKeyLoader(yaml_pointer)
	#help(data)
	yaml_text = yaml_file_pointer.read()
	data = yaml.load(yaml_text, Loader=UniqueKeyLoader)
	#data = yaml.safe_load(yaml_pointer)
	yaml_file_pointer.close()
	return data

#==========================
#==========================
#==========================
def get_git_root(path=None):
	"""Return the absolute path of the repository root."""
	if path is None:
		# Use the path of the script
		path = os.path.dirname(os.path.abspath(__file__))
	try:
		base = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], cwd=path, universal_newlines=True).strip()
		return base
	except subprocess.CalledProcessError:
		# Not inside a git repository
		return None

#==========================
def load_hidden_term_bank():
	git_root = get_git_root()
	data_file_path = os.path.join(git_root, 'data/all_short_words.txt')
	with open(data_file_path, 'r') as file:
		terms = file.readlines()
	return [term.strip() for term in terms]

#==========================
def insert_hidden_terms(text_content):
	if use_insert_hidden_terms is False:
		return text_content

	global hidden_term_bank
	if hidden_term_bank is None:
		hidden_term_bank = load_hidden_term_bank()

	# Separate table, code and non-table/non-code content
	parts = re.split(r'(<table>.*?</table>|<code>.*?</code>)', text_content, flags=re.DOTALL)

	# Process each part
	new_parts = []
	for part in parts:
		if part.startswith('<table>') or part.startswith('<code>'):
			# Keep table and code content unchanged
			new_parts.append(part)
		else:  # Apply the modified logic to non-table parts
			# Replace spaces adjacent to words with '@'
			#part = re.sub(r'([a-z]) +(?![^<>]*>)', r'\1@', part)
			part = re.sub(r'([a-z]) +([a-z])(?![^<>]*>)', r'\1@\2', part)
			#part = re.sub(r'([A-Za-z]) +(?![^<>]*>)', r'\1@', part)
			#part = re.sub(r' +([A-Za-z])(?![^<>]*>)', r'@\1', part)
			words = part.split('@')
			new_words = []
			for word in words:
				new_words.append(word)
				hidden_term = random.choice(hidden_term_bank)
				new_words.append(f"<span style='font-size: 1px; color: white;'>{hidden_term}</span>")
			new_parts.append(''.join(new_words))
	return ''.join(new_parts)

#========================================
def html_monospace(txt, use_nbsp=True):
	local_txt = copy.copy(txt)
	if use_nbsp is True:
		local_txt = local_txt.replace(' ', '&nbsp;')
	return f"<span style='font-family: monospace;'>{local_txt}</span>"
	#return f"<span style=\"font-family: 'andale mono', 'courier new', courier, monospace;\">{local_txt}</span>"
	#return f"<span style='font-family: 'andale mono', 'courier new', courier, monospace;'><code>{txt}</code></span>"

#==========================
def insert_hidden_terms_old(text_content):
	if use_insert_hidden_terms is False:
		return text_content
	global hidden_term_bank
	if hidden_term_bank is None:
		hidden_term_bank = load_hidden_term_bank()
	# Replace spaces outside HTML tags with '@'
	text_content = re.sub(r'( +)(?![^<>]*>)', '@', text_content)
	words = text_content.split('@')
	new_words = []
	for word in words:
		new_words.append(word)
		hidden_term = random.choice(hidden_term_bank)
		new_words.append(f"<span style='font-size: 1px; color: white;'>{hidden_term}</span>")
	return ''.join(new_words)

#==========================
#==========================
#==========================

#=======================
#=======================

base_replacement_rule_dict = {
	' not ': ' <strong>NOT</strong> ', #BOLD BLACK
	' Not ': ' <strong>NOT</strong> ', #BOLD BLACK
	' NOT ': ' <strong>NOT</strong> ', #BOLD BLACK
	' false ': ' <span style="color: #ba372a;"><strong>FALSE</strong></span> ', #BOLD RED
	' False ': ' <span style="color: #ba372a;"><strong>FALSE</strong></span> ', #BOLD RED
	' FALSE ': ' <span style="color: #ba372a;"><strong>FALSE</strong></span> ', #BOLD RED
	' true ': ' <span style="color: #169179;"><strong>TRUE</strong></span> ', #BOLD GREEN
	' True ': ' <span style="color: #169179;"><strong>TRUE</strong></span> ', #BOLD GREEN
	' TRUE ': ' <span style="color: #169179;"><strong>TRUE</strong></span> ', #BOLD GREEN
	'  ': ' ',
}

#=======================
def applyReplacementRulesToText(text_string, replacement_rule_dict):
	if replacement_rule_dict is None:
		print("no replacement rules found")
		replacement_rule_dict = base_replacement_rule_dict
	else:
		#replacement_rule_dict = {**base_replacement_rule_dict, **replacement_rule_dict}
		replacement_rule_dict |= base_replacement_rule_dict
	for find_text, replace_text in replacement_rule_dict.items():
		text_string = text_string.replace(find_text, replace_text)
	return text_string

#=======================
def applyReplacementRulesToList(list_of_text_strings, replacement_rule_dict):
	if replacement_rule_dict is None:
		print("no replacement rules found")
		replacement_rule_dict = base_replacement_rule_dict
	else:
		#replacement_rule_dict = {**base_replacement_rule_dict, **replacement_rule_dict}
		replacement_rule_dict |= base_replacement_rule_dict
	new_list_of_text_strings = []
	for string_text in list_of_text_strings:
		for find_text,replace_text in replacement_rule_dict.items():
			string_text = string_text.replace(find_text,replace_text)
		new_list_of_text_strings.append(string_text)
	return new_list_of_text_strings

#==========================
#==========================
#==========================

#==========================
def colorHTMLText(text, hex_code):
	return f'<span style="color: #{hex_code};">{text}</span>'

#==========================
fixed_color_wheel = (
	'e60000',  # RED
	'e65400',  # DARK ORANGE
	'e69100',  # LIGHT ORANGE
	'b3b300',  # DARK YELLOW
	'59b300',  # LIME GREEN
	'009900',  # GREEN
	'00b38f',  # TEAL
	'00b3b3',  # CYAN
	'0a9bf5',  # SKY BLUE
	'0039e6',  # BLUE
	'004d99',  # NAVY
	'7b12a1',  # PURPLE
	'b30077',  # MAGENTA
	'cc0066'   # PINK
)

#==========================
def default_color_wheel(num_colors, random_shift=True):
	# Calculate the step size for selecting colors
	step = len(fixed_color_wheel) / num_colors
	# Generate the list of indices to select colors from the fixed color wheel
	indices = [round(step * i) for i in range(num_colors)]

	# Apply a random shift to the selected indices if specified
	if random_shift:
		shift = random.randint(0, len(fixed_color_wheel) - 1)
		indices = [(i + shift) % len(fixed_color_wheel) for i in indices]

	# Select the colors based on the generated indices
	selected_colors = [fixed_color_wheel[i] for i in indices]
	return selected_colors

# Lighter color wheel for background colors in HTML tables
light_color_wheel = (
	'ffcccc',  # Light Red
	'ffd9cc',  # Light Dark Orange
	'ffebcc',  # Light Light Orange
	'ffffcc',  # Light Dark Yellow
	'd9ffcc',  # Light Lime Green
	'ccffcc',  # Light Green
	'ccffe6',  # Light Teal
	'ccffff',  # Light Cyan
	'ccf2ff',  # Light Sky Blue
	'ccd9ff',  # Light Blue
	'ccccff',  # Light Navy
	'e6ccff',  # Light Purple
	'ffccf2',  # Light Magenta
	'ffccff',  # Light Pink
)

# Lighter color wheel for background colors in HTML tables
extra_light_color_wheel = (
	'ffe6e6',  # Light Red
	'ffece6',  # Light Orange
	'fff5e6',  # Light Light Orange
	'ffffe6',  # Light Yellow
	'ecffe6',  # Light Lime Green
	'e6ffe6',  # Light Green
	'e6fff3',  # Light Teal
	'e6ffff',  # Light Cyan
	'e6f9ff',  # Light Sky Blue
	'e6ecff',  # Light Blue
	'e6e6ff',  # Light Navy
	'f3e6ff',  # Light Purple
	'ffe6f9',  # Light Magenta
	'ffe6ff',  # Light Pink
)

def default_light_color_wheel(num_colors, random_shift=True, extra_light=False):
	if extra_light is True:
		color_wheel = extra_light_color_wheel
	else:
		color_wheel = light_color_wheel

	# Calculate the step size for selecting colors
	step = len(color_wheel) / num_colors
	# Generate the list of indices to select colors from the light color wheel
	indices = [round(step * i) for i in range(num_colors)]

	# Apply a random shift to the selected indices if specified
	if random_shift:
		shift = random.randint(0, len(color_wheel) - 1)
		indices = [(i + shift) % len(color_wheel) for i in indices]

	# Select the colors based on the generated indices
	selected_colors = [color_wheel[i] for i in indices]
	return selected_colors

def light_and_dark_color_wheel(num_colors, random_shift=True, extra_light=False):
	if extra_light is True:
		color_wheel = extra_light_color_wheel
	else:
		color_wheel = light_color_wheel

	# Calculate the step size for selecting colors
	step = len(color_wheel) / num_colors
	# Generate the list of indices to select colors from the light color wheel
	indices = [round(step * i) for i in range(num_colors)]

	# Apply a random shift to the selected indices if specified
	if random_shift:
		shift = random.randint(0, len(color_wheel) - 1)
		indices = [(i + shift) % len(color_wheel) for i in indices]

	# Select the colors based on the generated indices
	selected_light_colors = [color_wheel[i] for i in indices]
	selected_dark_colors = [fixed_color_wheel[i] for i in indices]
	return selected_light_colors, selected_dark_colors

# Assume the fixed_color_wheel and light_color_wheel lists are defined elsewhere in this file, as shown above

def write_html_color_table(filename):
	with open(filename, 'w') as f:
		# Start the HTML document
		f.write("<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><title>Color Table</title>"
				"<style>table {width: 100%; border-collapse: collapse;} th {background-color: #333; color: white; padding: 10px;}"
				"td {padding: 10px; text-align: center;} .light-bg {font-weight: bold;} .dark-text {background-color: white;}"
				"</style></head><body><table border='1'><tr><th>Color Name</th><th>Light Color (Background)</th>"
				"<th>Fixed Color (Text)</th></tr>")

		# Generate table rows
		for i in range(len(light_color_wheel)):
			fixed_index = i % len(fixed_color_wheel)  # Loop back if necessary
			f.write(f"<tr><td>Color {i+1}</td><td class='light-bg' style='background-color:#{light_color_wheel[i]};'>Text</td>"
					f"<td class='dark-text' style='color:#{fixed_color_wheel[fixed_index]};'>Text</td></tr>")

		# End the HTML document
		f.write("</table></body></html>")

#==========================
def default_color_wheel_calc(num_colors=4):
	degree_step = int(360 / float(num_colors))
	r,g,b = (255, 0, 0)
	color_wheel = make_color_wheel(r,g,b, degree_step)
	return color_wheel

#==========================
def make_color_wheel(r, g, b, degree_step=40): # Assumption: r, g, b in [0, 255]
	r, g, b = map(lambda x: x/255., [r, g, b]) # Convert to [0, 1]
	#print('rgb: {0:.2f}, {1:.2f}, {2:.2f}'.format(r, g, b))
	hue, l, s = colorsys.rgb_to_hls(r, g, b)     # RGB -> HLS
	#print('hsl: {0:.2f}, {1:.2f}, {2:.2f}'.format(hue, s, l))
	wheel = []
	for deg in range(0, 359, degree_step):
		#print('--')
		hue_i = (hue*360. + float(deg))/360.
		#print(hue_i, l, s)
		#print('hsl: {0:.2f}, {1:.2f}, {2:.2f}'.format(hue_i, s, l))
		ryb_percent_color = colorsys.hls_to_rgb(hue_i, l, s)
		#print(ryb_percent_color)
		#print('ryb: {0:.2f}, {1:.2f}, {2:.2f}'.format(
		#	ryb_percent_color[0], ryb_percent_color[1], ryb_percent_color[2],))
		rgb_percent_color = _ryb_to_rgb(*ryb_percent_color)
		#print('rgb: {0:.2f}, {1:.2f}, {2:.2f}'.format(
		#	rgb_percent_color[0], rgb_percent_color[1], rgb_percent_color[2],))
		### this does not work
		rgb_color = tuple(map(lambda x: int(round(x*255)), rgb_percent_color))
		### this is worse
		#rgb_color = tuple(map(lambda x: int(round(x*255)), ryb_percent_color))
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
def getGeneLetters(length, shift=0, upper=False):
	#all_lowercase = "abcdefghijklmnopqrstuvwxyz"
	lowercase =     "abcdefghjkmnpqrstuwxyz"
	shift = shift % (len(lowercase) - length + 1)
	gene_string = lowercase[shift:shift+length]
	if upper is True:
		gene_string = gene_string.upper()
	gene_list = list(gene_string)
	return gene_list

#==========================
#==========================
#==========================
def checkAscii(mystr):
	#destructive function
	mystr = mystr.replace('. ', '\n')
	mystr = mystr.replace(', ', '\n')
	mystr = mystr.replace('<p>', '\n')
	mystr = mystr.replace('</p>', '\n')
	mystr = mystr.replace('<br/>', '\n')
	mystr = mystr.replace('\n\n', '\n')
	for i,line in enumerate(mystr.split('\n')):
		for j,c in enumerate(list(line)):
			try:
				c.encode('ascii', errors='strict')
			except UnicodeEncodeError:
				print(line)
				print(i, j, c)
				print("^ is not ascii")
				sys.exit(1)
	return True

#==========================
def getCrc16_FromString(mystr):
	crc16 = crcmod.predefined.Crc('xmodem')
	try:
		crc16.update(mystr.encode('ascii', errors='strict'))
	except UnicodeEncodeError:
		checkAscii(mystr)
		sys.exit(1)
	return crc16.hexdigest().lower()

#==========================
def makeQuestionPretty(question):
	pretty_question = copy.copy(question)
	#print(len(pretty_question))
	pretty_question = re.sub('\<table .+\<\/table\>', '\n[TABLE]\n', pretty_question)
	pretty_question = re.sub('\<table .*\<\/table\>', '\n[TABLE]\n', pretty_question)
	if '<table' in pretty_question or '</table' in pretty_question:
		print("MISSED A TABLE")
		print(pretty_question)
		sys.exit(1)
		pass
	#print(len(pretty_question))
	pretty_question = re.sub('&nbsp;', ' ', pretty_question)
	pretty_question = re.sub('h[0-9]\>', 'p>', pretty_question)
	pretty_question = re.sub('<br/>', '\n', pretty_question)
	pretty_question = re.sub('<li>', '\n* ', pretty_question)
	pretty_question = re.sub('<span [^>]*>', ' ', pretty_question)
	pretty_question = re.sub('<\/?strong>', ' ', pretty_question)
	pretty_question = re.sub('</span>', '', pretty_question)
	pretty_question = re.sub('\<hr\/\>', '', pretty_question)
	pretty_question = re.sub('\<\/p\>\s*\<p\>', '\n', pretty_question)
	pretty_question = re.sub('\<p\>\s*\<\/p\>', '\n', pretty_question)
	pretty_question = re.sub('\n\<\/p\>', '', pretty_question)
	pretty_question = re.sub('\n\<p\>', '\n', pretty_question)
	pretty_question = re.sub('\n\n', '\n', pretty_question)
	pretty_question = re.sub('  *', ' ', pretty_question)

	#print(len(pretty_question))
	return pretty_question

#==========================
def generate_js_function():
	#global use_nocopy_script
	if use_nocopy_script is False:
		return ''
	return jsdelivr_js_function()
	#return pdfanticopy_js_function()


#==========================
def pdfanticopy_js_function():
	# Using Python f-string to include global variables in the JavaScript code
	js_code = f'<script>var noPrint={str(noPrint).lower()};var noCopy={str(noCopy).lower()};var noScreenshot={str(noScreenshot).lower()};var autoBlur={str(autoBlur).lower()};</script>'
	js_code += '<script type="text/javascript" '
	js_code += 'src="https://pdfanticopy.com/noprint.js"'
	js_code += '></script>'
	return js_code

#==========================
def jsdelivr_js_function():
	# Similar technique is applied here, variables are inserted dynamically
	js_code = f'<script>var noPrint={str(noPrint).lower()};var noCopy={str(noCopy).lower()};var noScreenshot={str(noScreenshot).lower()};var autoBlur={str(autoBlur).lower()};</script>'
	js_code += '<script type="text/javascript" '
	js_code += 'src="https://cdn.jsdelivr.net/gh/vosslab/biology-problems@main/javascript/noprint.js"'
	js_code += '></script>'
	return js_code

#==========================
def add_no_click_div(text):
	#global use_add_no_click_div
	if use_add_no_click_div is False:
		return text
	number = random.randint(1000,9999)
	output  = f'<div id="drv_{number}" '
	output += 'oncopy="return false;" onpaste="return false;" oncut="return false;" '
	output += 'oncontextmenu="return false;" onmousedown="return false;" onselectstart="return false;" '
	output += '>'
	output += text
	output += '</div>'
	return output

#==========================
def QuestionHeader(question, N, big_question=None, crc16=None):
	global crc16_dict
	#global use_nocopy_script
	if crc16 is None:
		if big_question is not None:
			crc16 = getCrc16_FromString(big_question)
		else:
			crc16 = getCrc16_FromString(question)
	if crc16_dict.get(crc16) == 1:
		print('crc16 first hash collision', crc16)
		crc16_dict[crc16] += 1
	elif crc16_dict.get(crc16) == 3:
		global question_count
		print('crc16 third hash collision', crc16, 'after question #', question_count)
		crc16_dict[crc16] += 1
	else:
		crc16_dict[crc16] = 1
	#header = '<p>{0:03d}. {1}</p> {2}'.format(N, crc16, question)
	pretty_question = makeQuestionPretty(question)
	print('{0:03d}. {1} -- {2}'.format(N, crc16, pretty_question))
	noisy_question = insert_hidden_terms(question)
	text = '<p>{0}</p> {1}'.format(crc16, noisy_question)
	header = ''
	if use_nocopy_script is True:
		js_function_string = generate_js_function()
		header += js_function_string
	header += add_no_click_div(text)
	return header

#==========================
def ChoiceHeader(choice_text):
	noisy_choice_text = insert_hidden_terms(choice_text)
	output = add_no_click_div(noisy_choice_text)
	return output

#==========================
#==========================
#==========================
def formatBB_MC_Question(N, question, choices_list, answer):
	global question_count
	if len(choices_list) <= 1:
		print("not enough choices to choose from, you need two choices for multiple choice")
		print("answer=", answer)
		print("choices_list=", choices_list)
		sys.exit(1)

	bb_question = ''
	#number = "{0}. ".format(N)

	bb_question += 'MC\t'
	big_question = question + ' '.join(choices_list) + answer
	bb_question += QuestionHeader(question, N, big_question)

	answer_count = 0

	letters = 'ABCDEFGHJKMNPQRSTUWXYZ'
	for i, choice_text in enumerate(choices_list):
		labeled_choice_text = '{0}.  {1}&nbsp; '.format(letters[i], choice_text)
		noisy_choice_text = ChoiceHeader(labeled_choice_text)
		bb_question += '\t'+noisy_choice_text
		if choice_text == answer:
			prefix = 'x'
			bb_question += '\tCorrect'
			answer_count += 1
			answer_histogram[letters[i]] = answer_histogram.get(letters[i], 0) + 1
		else:
			prefix = ' '
			bb_question += '\tIncorrect'
		print("- [{0}] {1}. {2}".format(prefix, letters[i], makeQuestionPretty(choice_text)))
	print("")
	if answer_count != 1:
		print("Too many or few answers count {0}".format(answer_count))
		sys.exit(1)
	question_count += 1
	return bb_question + '\n'

#=====================
def formatBB_MA_Question(N, question, choices_list, answers_list):
	global question_count
	if len(choices_list) <= 1:
		print("not enough choices to choose from, you need two choices for multiple choice")
		print("answers_list=", answers_list)
		print("choices_list=", choices_list)
		sys.exit(1)

	bb_question = ''
	#number = "{0}. ".format(N)
	bb_question += 'MA\t'
	big_question = question + ' '.join(choices_list) + ' '.join(answers_list)
	bb_question += QuestionHeader(question, N, big_question)

	answer_count = 0

	letters = 'ABCDEFGHJKMNPQRSTUWXYZ'
	for i, choice_text in enumerate(choices_list):
		labeled_choice_text = '{0}.  {1}&nbsp; '.format(letters[i], choice_text)
		noisy_choice_text = ChoiceHeader(labeled_choice_text)
		bb_question += '\t'+noisy_choice_text
		if choice_text in answers_list:
			prefix = 'x'
			bb_question += '\tCorrect'
			answer_count += 1
			answer_histogram[letters[i]] = answer_histogram.get(letters[i], 0) + 1
		else:
			prefix = ' '
			bb_question += '\tIncorrect'
		print("- [{0}] {1}. {2}".format(prefix, letters[i], makeQuestionPretty(choice_text)))
	print("")
	if answer_count == 0:
		print("No answer count {0}".format(answer_count))
		sys.exit(1)
	question_count += 1
	return bb_question + '\n'

#=====================
def formatBB_FIB_Question(N, question, answers_list):
	global question_count
	#fill in the black = FIB
	#FIB TAB question text TAB answer text TAB answer two text
	bb_question = ''

	#number = "{0}. ".format(N)
	bb_question += 'FIB\t'
	big_question = question + ' '.join(answers_list)
	bb_question += QuestionHeader(question, N, big_question)

	for i, answer in enumerate(answers_list):
		bb_question += '\t{0}'.format(answer)
		print("- {0}".format(makeQuestionPretty(answer)))
	print("")
	question_count += 1
	return bb_question + '\n'

#=====================
def formatBB_NUM_Question(N, question, answer, tolerance, tol_message=True):
	global question_count
	#NUM TAB question text TAB answer TAB [optional]tolerance
	bb_question = ''

	#number = "{0}. ".format(N)
	bb_question += 'NUM\t'
	if tol_message is True:
		question += f'<p><i>Answers need to be within {tolerance/answer*100:.1f}&percnt;'
		question += 'of the actual value to be correct.</i></p> '
	big_question = question + str(answer)
	bb_question += QuestionHeader(question, N, big_question)

	bb_question += '\t{0:.8f}'.format(answer)
	print("=== {0:.3f}".format(answer))
	bb_question += '\t{0:.8f}'.format(tolerance)
	print("+/- {0:.3f}".format(tolerance))
	print("")
	question_count += 1
	return bb_question + '\n'

#=====================
def formatBB_MAT_Question(N, question, answers_list, matching_list):
	#MAT TAB question text TAB answer text TAB matching text TAB answer two text TAB matching two text
	global question_count
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
	full_quesiton = question + ' '.join(answers_list) + ' '.join(matching_list)
	crc16 = getCrc16_FromString(full_quesiton)
	bb_question += 'MAT\t'
	bb_question += QuestionHeader(question, N, crc16)

	num_items = min(len(answers_list), len(matching_list))
	letters = 'ABCDEFGHJKMNPQRSTUWXYZ'
	for i in range(num_items):
		answer_text = answers_list[i]
		noisy_answer_text = ChoiceHeader(answer_text)
		match_text = matching_list[i]
		noisy_match_text = ChoiceHeader(match_text)
		bb_question += '\t{0}&nbsp;\t{1}&nbsp;'.format(noisy_answer_text, noisy_match_text)
		print("- {0}. {1} == {2}".format(letters[i], makeQuestionPretty(answer_text), makeQuestionPretty(match_text)))
	print("")
	question_count += 1
	return bb_question + '\n'

#==========================
#==========================
#==========================
def print_histogram():
	global question_count
	sys.stderr.write("=== Answer Choice Histogram ===\n")
	keys = list(answer_histogram.keys())
	keys.sort()
	total_answers = 0
	for key in keys:
		total_answers += answer_histogram[key]
		sys.stderr.write("{0}: {1},  ".format(key, answer_histogram[key]))
	sys.stderr.write("\n")
	sys.stderr.write("Total Questions = {0:d}; Total Answers = {1:d}\n".format(question_count, total_answers))
