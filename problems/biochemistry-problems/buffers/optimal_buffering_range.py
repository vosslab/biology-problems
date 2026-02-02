#!/usr/bin/env python3

# built-in python modules
import random

# external pip modules

# local repo modules
import bptools
import bufferslib

#======================================
#======================================
def get_question_text(buffer_dict) -> str:
	"""
	Generates and returns the main text for the question.

	This function is responsible for creating the base question text.
	Currently, it returns a generic placeholder string, but in a real
	application, this could involve generating a dynamic question based
	on various inputs or parameters.

	Returns:
		str: A string containing the main question text.
	"""
	question_text = ""
	question_text += ('<p><strong>' + buffer_dict['acid_name'].capitalize()
		+ '</strong> and its conjugate base, ' + buffer_dict['base_name']
		+ ', ' + buffer_dict['description'] + '.</p> ')
	question_text += ('<p>' + buffer_dict['acid_name'].capitalize() + ' is ' + buffer_dict['protic_name']
		+ ' with '+bufferslib.pKa_list_to_words(buffer_dict['pKa_list'])+'.</p> ')
	question_text += "<p>Which one of the following pH values falls outside the optimal buffering range"
	question_text += f"of {buffer_dict['acid_name'].capitalize()}?</p>"
	return question_text

#======================================
#======================================
def get_buffer_list() -> list:
	"""
	Build and return the list of buffer dictionaries.

	Returns:
		list: List of buffer dictionaries.
	"""
	buffer_list = []
	buffer_list += list(bufferslib.triprotic.values())
	buffer_list += list(bufferslib.tetraprotic.values())
	return buffer_list

#======================================
#======================================
def pH_to_color_span(ph_value, use_gray=False):
	"""
	Convert a pH value to a colored HTML <span> element based on a gradient.

	- pH < 7: From dark red (1.0) to black or gray (7.0).
	- pH > 7: From black or gray (7.0) to dark blue (13.0).
	"""
	# Clamp the pH value between 1.0 and 13.0
	#ph_value = max(1.0, min(13.0, ph_value))

	min_color = 28  # Minimum value for r and b
	max_color = 128  # Maximum value for r and b
	g = min_color  # Green stays constant

	# Calculate RGB values
	if ph_value < 7.0:
		# Transition from red (128, 28, 28) to black/gray (28, 28, 28)
		b = min_color  # Blue stays at the minimum
		t = (ph_value - 1.0) / (7.0 - 1.0)  # Scale factor for interpolation
		r = int((max_color - min_color) * (1 - t) + min_color)  # Red decreases
	else:
		# Transition from black/gray (28, 28, 28) to blue (28, 28, 128)
		r = min_color  # Red stays at the minimum
		t = (ph_value - 7.0) / (13.0 - 7.0)  # Scale factor for interpolation
		b = int((max_color - min_color) * t + min_color)  # Blue increases

	# Convert RGB to hex color
	color_hex = f"#{r:02x}{g:02x}{b:02x}"

	# Return the HTML span element with the color
	return f'pH <span style="color: {color_hex}">{ph_value:.1f}</span>'


#======================================
#======================================
def random_float_not_near(number_list, lower_bound=2.0, upper_bound=12.0, min_distance=1.2, max_attempts=1000):
	for _ in range(max_attempts):
		# Generate a random float in the given range
		candidate = round(random.uniform(lower_bound, upper_bound),1)

		# Check if the candidate is far enough from all values in the list
		if all(abs(candidate - value) >= min_distance for value in number_list):
			return candidate

	raise ValueError(f"Could not find a suitable float after {max_attempts} attempts.")

#======================================
#======================================
def generate_choices(buffer_dict, num_choices: int) -> (list, str):
	"""
	Generates a list of answer choices along with the correct answer.

	Defines a fixed set of choices for multiple-choice questions.
	This function randomly selects a correct answer from a predefined
	list of correct choices, then adds a few incorrect choices from
	another list to fill out the choices list. The number of choices
	is constrained by `num_choices`.

	Args:
		num_choices (int): The total number of answer choices to generate.

	Returns:
		tuple: A tuple containing:
			- list: A list of answer choices (mixed correct and incorrect).
			- str: The correct answer text.
	"""
	# Define possible correct choices and incorrect choices
	#print(buffer_dict.keys())
	pka_list = buffer_dict['pKa_list']
	choices_list = []
	answer_value = random_float_not_near(pka_list)
	answer_text = pH_to_color_span(answer_value)
	used_texts = {answer_text}

	candidates = []
	for pka in pka_list:
		candidates.append(pka + random.random())
		candidates.append(pka - random.random())
	random.shuffle(candidates)
	for candidate in candidates:
		if len(choices_list) >= num_choices - 1:
			break
		choice_text = pH_to_color_span(candidate)
		if choice_text in used_texts:
			continue
		used_texts.add(choice_text)
		choices_list.append(candidate)

	attempts = 0
	while len(choices_list) < num_choices - 1:
		attempts += 1
		if attempts > 1000:
			raise ValueError("Could not build a unique set of pH choices.")
		pka = random.choice(pka_list)
		candidate = pka + random.uniform(-0.9, 0.9)
		choice_text = pH_to_color_span(candidate)
		if choice_text in used_texts:
			continue
		used_texts.add(choice_text)
		choices_list.append(candidate)

	choices_list.append(answer_value)
	choices_list.sort()
	choices_text_list = [pH_to_color_span(choice_value) for choice_value in choices_list]
	answer_text = pH_to_color_span(answer_value)

	return choices_text_list, answer_text

#======================================
#======================================
def write_question(N: int, args) -> str:
	"""
	Creates a complete formatted question for output.

	This function combines the question text and choices generated by
	other functions into a formatted question string. The formatting
	is handled by a helper function from the `bptools` module.

	Args:
		N (int): The question number, used for labeling the question.
		args (argparse.Namespace): Parsed arguments with num_choices.

	Returns:
		str: A formatted question string suitable for output, containing
		the question text, answer choices, and correct answer.
	"""
	buffer_list = get_buffer_list()
	buffer_dict = random.choice(buffer_list)
	buffer_dict = bufferslib.expand_buffer_dict(buffer_dict)

	question_text = get_question_text(buffer_dict)
	choices_list, answer_text = generate_choices(buffer_dict, args.num_choices)

	# Format the complete question with the specified module function
	complete_question = bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)
	return complete_question

#=====================
def parse_arguments():
	"""
	Parses command-line arguments for the script.

	Defines and handles all arguments for the script, including:
	- `duplicates`: The number of questions to generate.
	- `num_choices`: The number of answer choices for each question.

	Returns:
		argparse.Namespace: Parsed arguments with attributes `duplicates`
		and `num_choices`.
	"""
	parser = bptools.make_arg_parser(description="Generate questions.")
	parser = bptools.add_choice_args(parser, default=5)

	args = parser.parse_args()
	return args

#======================================
#======================================
def main():
	"""
	Main function that orchestrates question generation and file output.
	"""
	args = parse_arguments()
	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)

if __name__ == '__main__':
	main()

#======================================
#======================================
if __name__ == '__main__':
	main()

## THE END
