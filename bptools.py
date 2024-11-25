#General Toosl for These Problems
import os
import re
import sys
import copy
import math
import yaml
import random
import colorsys
import subprocess
import num2words #pip
import crcmod.predefined #pip

import xml.etree.ElementTree as ET

#anticheating measures
use_nocopy_script = False
use_insert_hidden_terms = True
hidden_term_density = 0.7
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
	"""
	Convert a number to its ordinal representation.
	Args:
		integer (int): A positive integer to be converted.
	Returns:
		str: The ordinal representation of the number in English.
	"""
	return num2words.num2words(integer, to='ordinal', lang='en_US')
assert number_to_ordinal(3) == 'third'
#==========================
def number_to_cardinal(integer):
	"""
	Convert a number to its cardinal representation.
	Args:
		integer (int): A positive integer to be converted.
	Returns:
		str: The cardinal representation of the number in English.
	"""
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

#===========================================================
#===========================================================

import xml.etree.ElementTree as ET

def is_valid_html(html_str: str) -> bool:
	"""
	Validates if the input HTML string is well-formed by removing entities
	and wrapping the content in a root element for XML parsing.

	Args:
	html_str (str): The HTML string to validate.

	Returns:
	bool: True if the HTML is well-formed, False otherwise.
	"""
	html_str = html_str.replace('<', '\n<')
	try:
		# Remove HTML entities by finding '&' followed by alphanumerics or '#' and a semicolon
		cleaned_html = re.sub(r'&[#a-zA-Z0-9]+;', '', html_str)
		# Wrap in a root tag for XML parsing as XML requires a single root element
		wrapped_html = f"<root>{cleaned_html}</root>"
		# Parse the cleaned and wrapped HTML with XML parser
		ET.fromstring(wrapped_html)
		return True
	except ET.ParseError as e:
		# Print the error message for debugging
		if len(html_str) > 80:
			print(f"Parse error: {e}")
		#print(html_str)
		return False

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
				if random.random() < hidden_term_density:
					hidden_term = random.choice(hidden_term_bank)
					new_words.append(f"<span style='font-size: 1px; color: white;'>{hidden_term}</span>")
				else:
					new_words.append(" ")
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
def append_clear_font_space_to_text(string_text):
	return f'<span style="font-family: sans-serif; letter-spacing: 1px;">{string_text}</span>'

#=======================
def append_clear_font_space_to_list(list_of_text_strings):
	new_list_of_text_strings = []
	for string_text in list_of_text_strings:
		new_string_text = append_clear_font_space_to_text(string_text)
		new_list_of_text_strings.append(new_string_text)
	return new_list_of_text_strings

#=======================
def applyReplacementRulesToText(text_string, replacement_rule_dict):
	if not isinstance(text_string, str):
		raise TypeError(f"value is not string: {text_string}")
	if replacement_rule_dict is None:
		print("no replacement rules found")
		replacement_rule_dict = base_replacement_rule_dict
	else:
		#replacement_rule_dict = {**base_replacement_rule_dict, **replacement_rule_dict}
		replacement_rule_dict |= base_replacement_rule_dict
	for find_text, replace_text in replacement_rule_dict.items():
		if not replace_text.startswith('<strong>'):
			replace_text = f'<strong>{replace_text}</strong>'
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
	for text_string in list_of_text_strings:
		if not isinstance(text_string, str):
			raise TypeError(f"value is not string: {text_string}")
		for find_text, replace_text in replacement_rule_dict.items():
			if not replace_text.startswith('<strong>'):
				replace_text = f'<strong>{replace_text}</strong>'
			text_string = text_string.replace(find_text, replace_text)
		new_list_of_text_strings.append(text_string)
	return new_list_of_text_strings

#==========================
#==========================
#==========================

#==========================
def colorHTMLText(text, hex_code):
	return f'<span style="color: #{hex_code};">{text}</span>'

#===========================================================
#===========================================================
def min_difference(numbers: list) -> int:
	"""
	Find the minimum difference between any two consecutive integers in a sorted list.

	Parameters
	----------
	numbers : list
		A list of integers.

	Returns
	-------
	int
		The smallest difference found between any two consecutive integers.
	"""
	if isinstance(numbers, tuple):
		numbers = list(numbers)
	# Sort the list in place
	numbers.sort()
	# Calculate differences using list comprehension
	differences = [numbers[i+1] - numbers[i] for i in range(len(numbers) - 1)]
	# Return the smallest difference
	return min(differences)
assert min_difference([40, 41]) == 1
assert min_difference([30, 15, 36]) == 6
assert min_difference([84, 25, 24, 37]) == 1
assert min_difference([84, 30, 30, 42, 56, 72]) == 0

#==========================
dark_color_wheel = {
	'red': 'b30000',
	'orange': 'b34100',
	'brown': '663300',
	'gold': 'b37100',
	'yellow': '999900',
	'olive green': '465927',
	'lime green': '4d9900',
	'green': '008000',
	'teal': '008066',
	'cyan': '008080',
	'sky blue': '076cab',
	'blue': '002db3',
	'navy': '004080',
	'purple': '690f8a',
	'magenta': '800055',
	'pink': '99004d'
}

light_color_wheel = {
	'red': 'ffcccc',
	'orange': 'ffd9cc',
	'brown': 'ffe6cc',
	'gold': 'ffebcc',
	'yellow': 'ffffcc',
	'olive green': 'eaefdc',
	'lime green': 'd9ffcc',
	'green': 'ccffcc',
	'teal': 'ccffe6',
	'cyan': 'ccffff',
	'sky blue': 'ccf2ff',
	'blue': 'ccd9ff',
	'navy': 'ccccff',
	'purple': 'e6ccff',
	'magenta': 'ffccf2',
	'pink': 'ffccff'
}

extra_light_color_wheel = {
	'red': 'ffe6e6',
	'orange': 'ffece6',
	'brown': 'fff3e6',
	'gold': 'fff9e5',
	'yellow': 'ffffe6',
	'olive green': 'f5f7ee',
	'lime green': 'ecffe6',
	'green': 'e6ffe6',
	'teal': 'e6fff3',
	'cyan': 'e6ffff',
	'sky blue': 'e6f9ff',
	'blue': 'e6ecff',
	'navy': 'e6e6ff',
	'purple': 'f3e6ff',
	'magenta': 'ffe6f9',
	'pink': 'ffe6ff'
}

"""dark_color_wheel = (
	'b30000',  # RED
	'663300',  # BROWN
	'b34100',  # DARK ORANGE
	'b37100',  # LIGHT ORANGE
	'999900',  # DARK YELLOW
	'465927',  # OLIVE GREEN
	'4d9900',  # LIME GREEN
	'008000',  # GREEN
	'008066',  # TEAL
	'008080',  # CYAN
	'076cab',  # SKY BLUE
	'002db3',  # BLUE
	'004080',  # NAVY
	'690f8a',  # PURPLE
	'800055',  # MAGENTA
	'99004d'   # PINK
)

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
)"""

#==========================
#==========================
def get_indices_for_color_wheel(num_colors, color_wheel_length):
	"""
	Selects `num_colors` indices from a circular list of `color_wheel_length` items while ensuring
	that the selected indices are evenly spaced or satisfy other constraints depending on edge cases.

	Args:
		num_colors (int): The number of colors (indices) to select.
		color_wheel_length (int): The total length of the color wheel.

	Returns:
		list[int]: A sorted list of selected indices satisfying the constraints.

	Raises:
		ValueError: If `num_colors` is too large to satisfy the minimum distance requirement
		or if further indices cannot be selected under the constraints.

	Notes:
		- If `num_colors` exceeds `color_wheel_length`, the indices wrap around to repeat.
		- If `num_colors` is greater than half of `color_wheel_length`, random selection is used.
		- For smaller cases, a minimum spacing (`min_distance`) is enforced to distribute indices evenly.
		- The `color_wheel_length` is treated as circular, so wrap-around is handled.
	"""

	# Edge Case 1: If the number of colors exceeds the length of the color wheel
	# Wrap around by repeating indices in a circular fashion
	if num_colors > color_wheel_length:
		selected_indices = [i % color_wheel_length for i in range(num_colors)]
		return selected_indices

	# Edge Case 2: If there are many colors relative to the color wheel length
	# Use random selection without enforcing `min_distance` because spacing constraints aren't realistic
	if num_colors > color_wheel_length // 2 - 1:
		all_indices = list(range(color_wheel_length))
		random.shuffle(all_indices)  # Shuffle to randomize the selection
		selected_indices = all_indices[:num_colors]
		return sorted(selected_indices)

	# General Case: Calculate minimum spacing between indices
	# Ensure indices are approximately evenly distributed around the color wheel
	min_distance = int(math.floor(color_wheel_length / (num_colors + 1)))

	# Check if the desired number of colors can be selected given the `min_distance`
	if num_colors > color_wheel_length // min_distance:
		raise ValueError("num_colors too large to satisfy min_distance requirement")

	# Initialize an empty list for selected indices and create a list of all available indices
	selected_indices = []  # Stores the final selected indices
	available_indices = list(range(color_wheel_length))  # Indices that can still be selected

	# Select the required number of indices (`num_colors`)
	for _ in range(num_colors):
		# If no indices are available, raise an error
		if not available_indices:
			raise ValueError("Cannot select further colors within min_distance constraints")

		# Randomly choose an index from the available indices
		index = random.choice(available_indices)

		# Add the chosen index to the list of selected indices
		selected_indices.append(index)

		# Remove indices too close to the chosen index
		# The range includes indices `min_distance` away in both directions (wrap-around accounted for)
		for offset in range(-min_distance + 1, min_distance):
			idx_to_remove = (index + offset) % color_wheel_length  # Handle circular wrap-around
			if idx_to_remove in available_indices:
				available_indices.remove(idx_to_remove)

	# Sort the selected indices for consistency
	selected_indices = sorted(selected_indices)

	# Check if the selected indices actually meet the `min_distance` constraint
	# If not, raise an error as a safety check
	if num_colors > 1 and min_difference(selected_indices) < min_distance:
		raise ValueError(f'min_difference {min_difference(selected_indices)} < min_distance {min_distance}')

	return selected_indices

#==========================
def default_color_wheel(num_colors, color_wheel=dark_color_wheel):
	color_wheel_length = len(color_wheel)
	print(f"num_colors = {num_colors}; color_wheel_length = {color_wheel_length}")
	selected_indices = get_indices_for_color_wheel(num_colors, color_wheel_length)

	# Select the colors based on the generated indices
	color_wheel_keys = list(color_wheel.keys())
	selected_keys = [color_wheel_keys[i] for i in selected_indices]
	selected_colors_rgb = [color_wheel[i] for i in selected_keys]
	return selected_colors_rgb


#==========================
def default_color_wheel2(num_colors, random_shift=True):
	# Calculate the step size for selecting colors
	step = len(dark_color_wheel) / num_colors
	# Generate the list of indices to select colors from the fixed color wheel
	indices = [round(step * i) for i in range(num_colors)]

	# Apply a random shift to the selected indices if specified
	if random_shift:
		shift = random.randint(0, len(dark_color_wheel) - 1)
		indices = [(i + shift) % len(dark_color_wheel) for i in indices]

	# Select the colors based on the generated indices
	selected_colors = [dark_color_wheel[i] for i in indices]
	return selected_colors

#==========================
def light_and_dark_color_wheel(num_colors, dark_color_wheel=dark_color_wheel, light_color_wheel=light_color_wheel):
	color_wheel_length = min(len(dark_color_wheel), len(light_color_wheel))
	selected_indices = get_indices_for_color_wheel(num_colors, color_wheel_length)

	# Select the colors based on the generated indices
	dark_color_wheel_keys = list(dark_color_wheel.keys())
	dark_selected_keys = [dark_color_wheel_keys[i] for i in selected_indices]
	dark_selected_colors_rgb = [dark_color_wheel[i] for i in dark_selected_keys]
	light_color_wheel_keys = list(light_color_wheel.keys())
	light_selected_keys = [light_color_wheel_keys[i] for i in selected_indices]
	light_selected_colors_rgb = [light_color_wheel[i] for i in light_selected_keys]
	return light_selected_colors_rgb, dark_selected_colors_rgb


#==========================
def light_and_dark_color_wheel2(num_colors, random_shift=True, extra_light=False):
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
	selected_dark_colors = [dark_color_wheel[i] for i in indices]
	return selected_light_colors, selected_dark_colors


def write_html_color_table(filename):
	with open(filename, 'w') as f:
		# Start the HTML document
		f.write("<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><title>Color Table</title>"
				"<style>table {width: 100%; border-collapse: collapse;} th {background-color: #333; color: white; padding: 10px;}"
				"td {padding: 10px; text-align: center;} .light-bg {font-weight: bold;} .dark-text {background-color: white;}"
				"</style></head><body><table border='1'><tr><th>Color Name</th><th>Light Color (Background)</th>"
				"<th>Fixed Color (Text)</th></tr>")
		# Generate table rows
		for i in range(len(dark_color_wheel)):
			light_index = i % len(light_color_wheel)  # Loop back if necessary
			f.write(f"<tr><td>Color {i+1}</td><td class='light-bg' style='background-color:#{light_color_wheel[light_index]};'>Text</td>"
					f"<td class='dark-text' style='color:#{dark_color_wheel[i]};'>Text</td></tr>")

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
def generate_gene_letters(
	num_genes: int,
	shift: int = -1,
	clear: bool = False,
) -> str:
	"""
	Generate a string of unique gene letters based on deterministic or random selection.

	Args:
		num_genes (int): The number of unique gene letters to generate.
		shift (int, optional): The starting index for deterministic selection. If -1, randomization is used. Defaults to -1.
		clear (bool, optional): If True, uses the `clear_alphabet` (removes ambiguous characters).
		                        Defaults to False, which uses the full alphabet.

	Returns:
		str: A string containing `num_genes` unique letters.
	"""
	# Define alphabets
	full_alphabet = "abcdefghijklmnopqrstuvwxyz"
	ambiguous_letters = "giloqsuvz"  # Ambiguous or easily confused letters
	clear_alphabet = ''.join(sorted(set(full_alphabet) - set(ambiguous_letters)))

	# Select alphabet based on the `clear` flag
	alphabet = clear_alphabet if clear else full_alphabet

	# Validate input
	if num_genes > len(alphabet):
		raise ValueError(f"num_genes ({num_genes}) cannot exceed the length of the alphabet ({len(alphabet)}).")

	if shift >= 0:
		# Generate a deterministic sequence with a valid shift
		shift = shift % (len(alphabet) - num_genes + 1)
		return alphabet[shift:shift + num_genes]
	else:
		# Generate random unique letters
		return ''.join(sorted(random.sample(alphabet, num_genes)))
#=====================
# Tests
assert generate_gene_letters(5, 3) == "defgh"  # Deterministic with full alphabet
assert generate_gene_letters(5, 3, clear=True) == "defhj"  # Deterministic with clear alphabet
assert len(generate_gene_letters(5)) == 5  # Random with full alphabet

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
	pretty_question = re.sub(r'\<table .+\<\/table\>', '\n[TABLE]\n', pretty_question)
	pretty_question = re.sub(r'\<table .*\<\/table\>', '\n[TABLE]\n', pretty_question)
	if '<table' in pretty_question or '</table' in pretty_question:
		print("MISSED A TABLE")
		print(pretty_question)
		sys.exit(1)
		pass
	#print(len(pretty_question))
	pretty_question = re.sub('&nbsp;', ' ', pretty_question)
	pretty_question = re.sub(r'h[0-9]\>', 'p>', pretty_question)
	pretty_question = re.sub('<br/>', '\n', pretty_question)
	pretty_question = re.sub('<li>', '\n* ', pretty_question)
	pretty_question = re.sub('<span [^>]*>', ' ', pretty_question)
	pretty_question = re.sub(r'<\/?strong>', ' ', pretty_question)
	pretty_question = re.sub('</span>', '', pretty_question)
	pretty_question = re.sub(r'\<hr\/\>', '', pretty_question)
	pretty_question = re.sub(r'\<\/p\>\s*\<p\>', '\n', pretty_question)
	pretty_question = re.sub(r'\<p\>\s*\<\/p\>', '\n', pretty_question)
	pretty_question = re.sub(r'\n\<\/p\>', '', pretty_question)
	pretty_question = re.sub(r'\n\<p\>', '\n', pretty_question)
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
def formatQTI_MC_Question_Simple(N, question, choices_list, answer):
	# Set up the QTI namespace
	QTI_NS = "http://www.imsglobal.org/xsd/imsqti_v2p1"
	ET.register_namespace('', QTI_NS)

	# Create the root element
	assessmentItem = ET.Element("{%s}assessmentItem" % QTI_NS, {
		"identifier": f"MCQ{N}",
		"adaptive": "false",
		"timeDependent": "false"
	})

	# Correct response setup
	responseDeclaration = ET.SubElement(assessmentItem, "responseDeclaration", {
		"identifier": "RESPONSE",
		"cardinality": "single",
		"baseType": "identifier"
	})
	correctResponse = ET.SubElement(responseDeclaration, "correctResponse")
	correctValue = ET.SubElement(correctResponse, "value")
	correctValue.text = str(choices_list.index(answer))

	# Question stem setup
	itemBody = ET.SubElement(assessmentItem, "itemBody")
	choiceInteraction = ET.SubElement(itemBody, "choiceInteraction", {
		"responseIdentifier": "RESPONSE",
		"shuffle": "true",
		"maxChoices": "1"
	})
	prompt = ET.SubElement(choiceInteraction, "prompt")
	prompt.text = question

	# Choices setup
	for choice in choices_list:
		simpleChoice = ET.SubElement(choiceInteraction, "simpleChoice", {
			"identifier": str(choices_list.index(choice))
		})
		simpleChoice.text = choice

	# Convert the ElementTree to a string
	return ET.tostring(assessmentItem, encoding='unicode')

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
	use_add_no_click_div = False
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

#===========================================================
#===========================================================
def formatBB_FIB_PLUS_Question(N: int, question: str, answer_map: dict) -> str:
	global question_count
	use_add_no_click_div = False
	#FIB_PLUS TAB question text TAB variable1 TAB answer1 TAB answer2 TAB TAB variable2 TAB answer3
	bb_question = ''
	bb_question += 'FIB_PLUS\t'
	bb_question += QuestionHeader(question, N)
	keys_list = sorted(answer_map.keys())
	for key in keys_list:
		value_list = answer_map[key]
		print(f"- KEY [{key}] -> {value_list}")
		bb_question += f'\t{key}'
		for value in value_list:
			bb_question += f'\t{value}'
		bb_question += '\t'
	bb_question += '\n'
	return bb_question

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

#=====================
def formatBB_ORD_Question(N, question_text, ordered_answers_list):
	#ORD TAB question text TAB answer text TAB answer two text
	global question_count
	if len(ordered_answers_list) <= 2:
		print("not enough answers to choose from, you need three answers for an ordering problem")
		print("answers_list=", ordered_answers_list)
		sys.exit(1)

	bb_question = ''
	#number = "{0}. ".format(N)
	bb_question += 'ORD\t'
	big_question = question_text + ' '.join(ordered_answers_list)
	bb_question += QuestionHeader(question_text, N, big_question)

	for i, answer_text in enumerate(ordered_answers_list):
		noisy_answer_text = ChoiceHeader(answer_text)
		bb_question += '\t'+noisy_answer_text
		print(f"- [{i+1}] {makeQuestionPretty(answer_text)}")
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
