#!/usr/bin/env python3
# ^^ Specifies the Python3 environment to use for script execution

# Import built-in Python modules
# Provides functions to generate random numbers and selections
import random
import copy

# Import external modules (pip-installed)
import PIL.ImageColor

# Import local modules from the project
# Provides custom functions, such as question formatting and other utilities
import bptools
import hybridcrosslib


# Dark label colors remain readable on white; swatches retain the table colors.
COLOR_NAME_HEX = {
	'red': 'b22222',
	'orange': '9a4600',
	'yellow': '756000',
	'blue': '2455a4',
	'green': '246b32',
	'brown': '804020',
	'tan': '805b20',
	'pink': '9f3d67',
	'white': '595959',
	'light blue': '28658a',
	'redish pink': 'a34334',
	'purple': '753a80',
}


#===================
def styled_color(color_name: str) -> str:
	"""
	Returns an HTML-styled version of a color name.
	"""
	common_color_name = hybridcrosslib.color_translate.get(color_name, color_name)
	label = bptools.colorHTMLText(common_color_name, COLOR_NAME_HEX[common_color_name])
	# Printable exam text preserves hex colors, not CSS color names.
	swatch_hex = '#{:02x}{:02x}{:02x}'.format(*PIL.ImageColor.getrgb(color_name))
	return (
		f'<strong>{label} '
		f'(<span style="color: {swatch_hex}; font-size: 1.8em;">&#x25A0;</span>)</strong>'
	)

#===================
#===================
#===================
def make_question_content(gene_type, color_set):
	"""
	Generates the descriptive question text for a gene dominance problem.

	Args:
		gene_type (str): Type of dominance ('complete dominance', 'incomplete dominance', 'codominance')
		color_set (list[str]): List of three color names [dominant, intermediate, recessive]

	Returns:
		str: HTML string for the question body
	"""
	# Create styled versions of the color names
	color1_text = styled_color(color_set[0])
	color2_text = styled_color(color_set[1])
	color3_text = styled_color(color_set[2])

	# Start question
	question = '<p>Two organisms were crossed in a monohybrid experiment. '

	if gene_type == 'complete dominance':
		question += (
			f'The offspring showed three {color1_text} and one {color3_text} phenotype.</p>'
		)

	else:
		truebreeds = [color1_text, color3_text]
		random.shuffle(truebreeds)

		question += f'The offspring phenotypes included {truebreeds[0]} and {truebreeds[1]}'

		if gene_type == 'incomplete dominance':
			question += f', along with an intermediate {color2_text} phenotype.</p>'

		elif gene_type == 'codominance':
			question += (
				f', along with a speckled combination of {truebreeds[0]} and {truebreeds[1]}.</p>'
			)

	# Final prompt
	question += '<p><strong>What type of dominance best explains these results?</strong></p>'
	return question

#===================
#===================
def get_question_text(gene_type, color_set, letter):
	"""
	gene types

	0: 'complete dominance',
	1: 'incomplete dominance',
	2: 'codominance',
	"""
	gene_table = hybridcrosslib.createSingleGeneTable(gene_type, letter, color_set, 'Gene 1')

	# write the question content
	question_content = make_question_content(gene_type, color_set)

	question_text = ''
	question_text += gene_table
	question_text += " <br/> "
	question_text += question_content

	return question_text


#===================
#===================
def write_question(N: int, args) -> None:
	"""
	Creates a formatted MC question about gene type interpretation.

	Args:
		gene_letter (str): Label (e.g., A, B, C).
		gene_type (str): Gene dominance type.
		color_set (list[str]): Three-color phenotype set.

	Returns:
		str: Formatted multiple choice question
	"""
	# Build question text
	gene_letter = random.choice(hybridcrosslib.gene_letters)
	gene_type = random.choice(hybridcrosslib.single_gene_types)
	color_set = random.choice(hybridcrosslib.get_three_color_sets())
	question_text = get_question_text(gene_type, color_set, gene_letter)

	# Create shuffled list of choices
	all_gene_types = copy.copy(hybridcrosslib.single_gene_types)
	all_gene_types += ['epistasis', 'X-linked recessive']
	random.shuffle(all_gene_types)

	# Create choice text list
	choices_list = [f"The gene shows {gtype}" for gtype in all_gene_types]
	answer_text = f"The gene shows {gene_type}"

	# Format with bptools
	complete_question = bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)

	# Write to file
	return complete_question

#===========================================================
#===========================================================
# This function handles the parsing of command-line arguments.
def parse_arguments():
	"""
	Parses command-line arguments for the script.

	Returns:
		argparse.Namespace: Parsed arguments with attributes `duplicates`,
		`num_choices`, and `question_type`.
	"""
	# Create an argument parser with a description of the script's functionality
	parser = bptools.make_arg_parser(description="Generate questions.")

	# Parse the provided command-line arguments and return them
	args = parser.parse_args()
	return args

#===========================================================
#===========================================================
# This function serves as the entry point for generating and saving questions.
def main():
	"""
	Main function that orchestrates question generation and file output.
	"""

	# Parse arguments from the command line
	args = parse_arguments()

	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)

#===========================================================
#===========================================================
# This block ensures the script runs only when executed directly
if __name__ == '__main__':
	# Call the main function to run the program
	main()

## THE END
