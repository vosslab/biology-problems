
import sys

# Define the set of letters to be used and their associated colors
all_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
all_colors = [
	'#d40000', #RED
	'#b74300', #DARK ORANGE
	'#935d00', #LIGHT ORANGE
	'#6c6c00', #DARK YELLOW
	'#3b7600', #LIME GREEN
	'#007a00', #GREEN
	'#00775f', #TEAL
	'#007576', #CYAN
	'#076dad', #SKY BLUE
	'#003fff', #BLUE
	'#0067cc', #NAVY
	'#a719db', #PURPLE
	'#c80085', #MAGENTA
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

	# Initialize the HTML table (avoid colspan-heavy layouts which render as extra columns in text previews)
	metabolic_table = "<table border='0' style='border-collapse: collapse;'>"

	# Row for enzyme labels (aligned above the arrows)
	metabolic_table += "<tr>"
	for i in range(len(letters) - 1):
		metabolic_table += "<td>&nbsp;</td>"
		metabolic_table += ("<td style='font-size: 75%; text-align:center; vertical-align: bottom;'>"
			f"enzyme {i+1}</td>")
	metabolic_table += "<td>&nbsp;</td></tr>"

	# Row for molecules and arrows
	metabolic_table += "<tr>"
	for i in range(len(letters) - 1):
		metabolic_table += f"<td style='font-size: 150%; text-align:center; padding: 0 6px;'>{letters[i]}</td>"
		metabolic_table += "<td style='text-align:center; padding: 0 6px;'>&xrarr;</td>"
	metabolic_table += f"<td style='font-size: 150%; text-align:center; padding: 0 6px;'>{letters[-1]}</td>"
	metabolic_table += "</tr></table>"

	return metabolic_table
