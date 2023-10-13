
import sys

# Define the set of letters to be used and their associated colors
all_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
all_colors = [
	'#e60000', #RED
	'#e65400', #DARK ORANGE
	'#e69100', #LIGHT ORANGE
	'#b3b300', #DARK YELLOW
	'#59b300', #LIME GREEN
	'#009900', #GREEN
	'#00b38f', #TEAL
	'#00b3b3', #CYAN
	'#0a9bf5', #SKY BLUE
	'#0039e6', #BLUE
	'#004d99', #NAVY
	'#7b12a1', #PURPLE
	'#b30077', #MAGENTA
	'#cc0066', #PINK
]

#======================================
#======================================
def get_letters(num_letters=6, shift=0):
	"""Fetch a list of HTML-formatted letters with a given color.

	Args:
		num_letters (int): The number of letters to get.
		shift (int): The index to start from for letter and color.

	Returns:
		html_letters (list): List of HTML formatted letters with color.
	"""

	# Determine the starting index for fetching letters and colors
	letter_index = shift % (len(all_letters) - num_letters)

	# Extract letters and colors based on the calculated index
	letters = list(all_letters[letter_index:letter_index+num_letters])
	local_colors = all_colors + all_colors  # Double the list to handle rollover
	color_index = shift % len(all_colors)
	colors = local_colors[color_index:color_index+num_letters]

	# Format letters as HTML with color
	html_letters = []
	for i, ltr in enumerate(letters):
		clr = colors[i]
		html_text = '<strong><span style="color: {0}">{1}</span></strong>'.format(clr, ltr)
		html_letters.append(html_text)

	return html_letters

#======================================
#======================================
def generate_metabolic_pathway(num_letters, shift=0):
	"""Generate an HTML table showing a metabolic pathway.

	Args:
		num_letters (int): Number of molecules (letters) in the pathway.
		shift (int): Index to start from for letter and color selection.

	Returns:
		metabolic_table (str): HTML-formatted table representing the metabolic pathway.
	"""

	# Validate the number of molecules
	if num_letters < 3:
		print('Not enough molecules provided for the pathway.')
		sys.exit(1)

	# Fetch HTML-formatted letters
	letters = get_letters(num_letters, shift)

	# Initialize the HTML table
	metabolic_table = '<table border="0" style="border-collapse: collapse;">'

	# Create the row for enzymes
	metabolic_table += '<tr><td colspan=2></td>'  # Leading empty cells
	for i in range(len(letters) - 1):
		metabolic_table += f'<td style="font-size: 50%; text-align:center; vertical-align: bottom;" colspan=3>enzyme {i+1}</td>'
		metabolic_table += '<td></td>'  # Trailing empty cell
	metabolic_table += '<td></td></tr>'  # Trailing empty cell

	# Create the row for molecules and arrows
	metabolic_table += '<tr>'
	for i in range(len(letters) - 1):
		metabolic_table += f'<td style="font-size: 125%; text-align:center;" colspan=3>{letters[i]}</td>'
		metabolic_table += '<td style="text-align:center; vertical-align:top;">&nbsp;&xrarr;&nbsp;</td>'
	# Add the last molecule
	metabolic_table += f'<td style="font-size: 125%; text-align:center;" colspan=3>{letters[-1]}</td></tr>'

	# Create a row for spacing (to separate rows visually)
	metabolic_table += '<tr>'
	for i in range(len(letters)*4-1):
		metabolic_table += "<td><span style='font-size: 1px; color: white;'>&nbsp;</span></td>"
	metabolic_table += '</tr></table>'

	return metabolic_table
