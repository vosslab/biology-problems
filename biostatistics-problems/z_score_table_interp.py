#!/usr/bin/env python3

# Standard Library
import random
import sys

# Local repo modules
import bptools

#==============
def get_question_text(question_type: str) -> str:
	"""
	Returns the text of the biodiversity question.
	"""
	return (
		"Ecologists assess biodiversity across four Chicago-area villages by calculating "
		"Z-scores for plant diversity, insect diversity, and bird diversity. Based on the "
		"data provided below, which village shows the "
		f"<strong>{question_type.upper()}</strong> level of biodiversity overall?"
	)

#==============
def select_villages(num_requested) -> list:
	"""
	Randomly selects four distinct village names from a predefined list of Chicago-area villages.

	Returns:
		list: Four unique village names.
	"""
	chicago_villages = [
		"Oak Lawn",          "Palatine",           "Naperville",        "Arlington Heights",
		"Aurora",            "Wheaton",            "Skokie",            "Berwyn",
		"Elmhurst",          "Des Plaines",        "Evanston",          "Schaumburg",
		"Orland Park",       "Tinley Park",        "Hoffman Estates",   "Mount Prospect",
		"Bolingbrook",       "Downers Grove",      "Glenview",          "Lombard",
		"Buffalo Grove",     "Highland Park",      "Bartlett",          "Crystal Lake",
		"St. Charles",       "Algonquin",          "Park Ridge",        "Plainfield",
		"Streamwood",        "Elk Grove",          "Northbrook",        "Carol Stream",
		"Hinsdale",          "Wilmette",           "Addison",           "Roselle",
		"Lake Forest",       "Bensenville",        "Lisle",             "Woodridge",
		"Morton Grove",      "Villa Park",
	]

	return random.sample(chicago_villages, num_requested)

#==============
def generate_unique_z_scores(count: int) -> list:
	"""
	Generates a list of unique Z-scores with no duplicate rounded values. Ensures a balanced
	distribution of positive and negative values, and removes extreme values.

	Args:
		count (int): The number of unique Z-scores to generate.

	Returns:
		list: A sorted list of unique Z-scores with unrounded values.
	"""
	# Initialize lists and sets to store Z-scores and track unique rounded values
	z_scores = []
	rounded_values_included = set()

	# Extra settings to control distribution
	num_scores_needed = count + 4  # Extra scores for trimming outliers
	stdev = 3.8  # Standard deviation for Z-score generation
	precision = 0.3  # Precision for rounding control
	num_neg = 0  # Counter for negative numbers
	num_pos = 0  # Counter for positive numbers
	loop_count = 0  # Loop counter to prevent infinite loops

	# Check value: ensure that the precision allows enough unique rounded values
	if stdev * 0.8 * 2 / precision <= num_scores_needed:
		print("Error: precision is too high relative to stdev and count. "
			"Not enough unique values can be generated.")
		sys.exit(1)

	# Generate unique Z-scores with balanced positive and negative values
	while len(z_scores) < num_scores_needed:
		loop_count += 1
		if loop_count > 1000:
			print(f"Error: parameter settings (stdev={stdev}, precision={precision}) caused an infinite loop.")
			sys.exit(1)

		# Generate a Z-score using a normal distribution
		number = random.gauss(0.0, stdev)
		rounded = int(round(number / precision))  # Scale to enforce unique rounded values

		# Balance positive and negative numbers to avoid heavy skew
		if num_neg - num_pos > 3 and number < 0:
			number *= -1.0
		if num_pos - num_neg > 3 and number > 0:
			number *= -1.0

		# Ignore extreme values beyond 80% of the standard deviation range
		if abs(number) > stdev * 0.8:
			continue

		# Add the number if its rounded form is unique
		if rounded not in rounded_values_included:
			z_scores.append(number)
			rounded_values_included.add(rounded)

			# Update positive/negative counters
			if number < 0:
				num_neg += 1
			else:
				num_pos += 1

	# Sort Z-scores and remove the highest and lowest values to reduce extremes
	z_scores.sort()
	print("Sorted Z-scores for assignment:")
	for value in z_scores:
		print(f"{value:.3f}")

	# Remove two smallest and two largest values to get a controlled range
	z_scores.pop(0)  # Smallest value
	z_scores.pop(0)  # Second smallest value
	z_scores.pop(-1)  # Largest value
	z_scores.pop(-1)  # Second largest value

	return z_scores

#==============
def generate_z_scores(villages: list) -> dict:
	"""
	Generates random Z-scores for each village based on specific criteria to simulate biodiversity.

	Each village receives three Z-scores for different categories (e.g., plant, insect, bird diversity),
	with values assigned to meet the following criteria:
		- Highest Overall Z-score: Represents the village with the highest biodiversity.
		- Lowest Overall Z-score: Represents the village with the lowest biodiversity.
		- Mid-range Overall with Highest Individual Z-score: A distractor with one high individual value.
		- Mid-range Overall with Lowest Individual Z-score: A distractor with one low individual value.

	Args:
		villages (list): List of four village names selected for the question.

	Returns:
		dict: Dictionary where each key is a village name and each value is a list of three Z-scores.
	"""
	# Generate a sorted list of unique, unrounded Z-scores
	num_scores_needed = (len(villages) * 3)
	z_score_source_list = generate_unique_z_scores(num_scores_needed)

	# Assign Z-scores to each village based on the specified criteria.
	# Each village will receive three Z-scores selected from different positions in the sorted list.
	# This helps to ensure diversity in scores while controlling overall and individual values.

	z_scores = {}

	# Highest Overall Z-score:
	# This village has the highest cumulative Z-score by selecting higher values from the sorted list.
	z_scores[villages[0]] = [
		z_score_source_list[10],
		z_score_source_list[9],
		z_score_source_list[7],
	]

	# Lowest Overall Z-score:
	# This village has the lowest cumulative Z-score by selecting lower values from the sorted list.
	z_scores[villages[1]] = [
		z_score_source_list[1],
		z_score_source_list[2],
		z_score_source_list[4],
	]

	# Mid-range Overall with High Individual Z-score:
	# This village has a mid-range cumulative score but includes one very high individual score.
	z_scores[villages[2]] = [
		z_score_source_list[11],
		z_score_source_list[6],
		z_score_source_list[3],
	]

	# Mid-range Overall with Low Individual Z-score:
	# This village has a mid-range cumulative score but includes one very low individual score.
	z_scores[villages[3]] = [
		z_score_source_list[0],
		z_score_source_list[5],
		z_score_source_list[8],
	]

	# Shuffle the Z-scores within each village's list
	for village in villages:
		random.shuffle(z_scores[village])

	# Validate the assigned Z-scores to ensure they match the intended outcomes
	if not validate_z_scores(villages, z_scores):
		print("Error: Generated Z-scores do not match intended criteria.")
		sys.exit(1)

	return z_scores


#==============
def print_z_score_data(villages: list, z_scores: dict):
	"""
	Prints all Z-score data in a nicely formatted table with aligned columns.

	Args:
		villages (list): List of village names.
		z_scores (dict): Dictionary where each key is a village name and each value is a list of three Z-scores.
	"""
	# Calculate total Z-scores for each village
	totals = {village: sum(z_scores[village]) for village in villages}

	print("\n=== Z-score Data Overview ===")
	print(f"{'Village':<20} {'Plant Z-score':>15} {'Insect Z-score':>15} {'Bird Z-score':>15} {'Total Z-score':>15}")
	print("-" * 80)

	for village in villages:
		plant, insect, bird = [f"{score:>7.2f}" for score in z_scores[village]]
		total = f"{totals[village]:>7.2f}"
		print(f"{village:<20} {plant:>15} {insect:>15} {bird:>15} {total:>15}")

	print("-" * 100)

#==============
def validate_z_scores(villages: list, z_scores: dict) -> bool:
	"""
	Validates the generated Z-scores to ensure they meet the specific criteria for each village.

	Args:
		villages (list): List of four village names.
		z_scores (dict): Dictionary where each key is a village name and each value is a list of three Z-scores.

	Returns:
		bool: True if all validation checks pass, False otherwise.
	"""
	# Print all Z-score data in a formatted table
	print_z_score_data(villages, z_scores)

	# Calculate total Z-scores for each village
	totals = {village: sum(scores) for village, scores in z_scores.items()}

	# Sort villages by total Z-score to identify highest and lowest cumulative score villages
	villages_sorted_by_total = sorted(villages, key=lambda v: totals[v])
	lowest_cumulative_score_village = villages_sorted_by_total[0]
	highest_cumulative_score_village = villages_sorted_by_total[-1]

	# Identify individual max and min Z-scores for each village
	individual_max_scores = {village: max(scores) for village, scores in z_scores.items()}
	individual_min_scores = {village: min(scores) for village, scores in z_scores.items()}

	# Determine the village with the highest and lowest individual Z-scores
	highest_individual_score_village = max(individual_max_scores, key=individual_max_scores.get)
	highest_individual_score = individual_max_scores[highest_individual_score_village]

	lowest_individual_score_village = min(individual_min_scores, key=individual_min_scores.get)
	lowest_individual_score = individual_min_scores[lowest_individual_score_village]

	# Improved debug output for readability
	print("\n=== Validation Debug Output ===")

	print(f"\nHighest Cumulative Z-score Village: {highest_cumulative_score_village}")
	print(f"  Total = {totals[highest_cumulative_score_village]:.2f}, Scores = {[f'{score:.2f}' for score in z_scores[highest_cumulative_score_village]]}")

	print(f"\nLowest Cumulative Z-score Village: {lowest_cumulative_score_village}")
	print(f"  Total = {totals[lowest_cumulative_score_village]:.2f}, Scores = {[f'{score:.2f}' for score in z_scores[lowest_cumulative_score_village]]}")

	print(f"\nHighest Village Individual Score: {highest_individual_score_village}")
	print(f"  Highest individual Z-score = {highest_individual_score:.2f}, Scores = {[f'{score:.2f}' for score in z_scores[highest_individual_score_village]]}")

	print(f"\nLowest Village Individual Score: {lowest_individual_score_village}")
	print(f"  Lowest individual Z-score = {lowest_individual_score:.2f}, Scores = {[f'{score:.2f}' for score in z_scores[lowest_individual_score_village]]}")

	# Final check: Ensure each criterion is assigned to a different village
	if len(set([
		highest_cumulative_score_village,
		lowest_cumulative_score_village,
		highest_individual_score_village,
		lowest_individual_score_village
	])) != 4:
		print("\nValidation failed: Each criterion should be assigned to a different village.")
		return False

	print("\nValidation successful: Generated Z-scores meet all criteria.")
	return True


#==============
#==============
def format_html_table(villages: list, z_scores: dict, totals: dict) -> str:
	"""
	Formats the Z-scores into an HTML-like table with alternating row colors and enhanced styling.

	Args:
		villages (list): List of village names.
		z_scores (dict): Dictionary of Z-scores for each village.
		totals (dict): Dictionary of total Z-scores for each village.

	Returns:
		str: Formatted HTML-like table as a string.
	"""
	# Define reusable style variables for header and cells
	header_style = (
		"padding: 10px; border: 1px solid #ddd; background-color: #e6e6e6;"
		"text-align: center; font-weight: bold;"
	)
	cell_style = "padding: 8px; border: 1px solid #ddd; text-align: center;"
	village_cell_style = "padding: 8px; border: 1px solid #ddd; text-align: left; font-weight: bold;"

	# Start the HTML table with general styling
	html = (
		"<table border='1' style='border-collapse: collapse; font-family: Arial, sans-serif;'>"
		"<tr style='height: 50px;'>"
		f"<th style='{header_style}'>Village</th>"
		f"<th style='{header_style}'>Plant<br/>Z-Score</th>"
		f"<th style='{header_style}'>Insect<br/>Z-Score</th>"
		f"<th style='{header_style}'>Bird<br/>Z-Score</th>"
		f"<th style='{header_style}'>Total<br/>Z-Score</th>"
		"</tr>"
	)

	# Loop through each village to populate rows with alternating background colors
	for i, village in enumerate(villages):
		plant, insect, bird = z_scores[village]
		total_score = totals[village]

		# Set background color for alternating rows
		row_bg_color = "#ffffe0" if i % 2 == 1 else "#ffffff"  # Light yellow for odd rows, light gray for even rows

		# Add row with data and styling
		html += (
			f"<tr style='background-color: {row_bg_color}; height: 45px;'>"
			f"<td style='{village_cell_style}'>{village}</td>"
			f"<td style='{cell_style}'>{plant:.2f}</td>"
			f"<td style='{cell_style}'>{insect:.2f}</td>"
			f"<td style='{cell_style}'>{bird:.2f}</td>"
			f"<td style='{cell_style} font-weight: bold;'>{total_score:.2f}</td>"
			"</tr>"
		)

	html += "</table>"
	html = html.replace('\n', ' ')
	return html


#==============
def sum_z_scores(z_scores: list) -> float:
	"""
	Calculates the total Z-score for a village by summing its individual Z-scores.

	Args:
		z_scores (list): List of individual Z-scores for a village.

	Returns:
		float: Total Z-score rounded to one decimal place.
	"""
	return round(sum(z_scores), 1)

#==============
def generate_choices(villages: list, z_scores: dict, totals: dict, question_type: str) -> (list, str):
	"""
	Generates answer choices based on village Z-scores.

	Args:
		villages (list): List of village names.
		z_scores (dict): Z-scores for each village.
		totals (dict): Total Z-scores for each village.

	Returns:
		tuple: (list of choices, correct answer text)
	"""
	# Find the village with the highest total Z-score
	if question_type == "highest":
		correct_village = max(totals, key=totals.get)
	elif question_type == "lowest":
		correct_village = min(totals, key=totals.get)
	else:
		sys.exit(1)
	choices = villages[:]
	#random.shuffle(choices)
	choices.sort()
	return choices, correct_village

#==============
def write_question(N: int, args) -> str:
	"""
	Creates a formatted multiple-choice question.

	Args:
		N (int): Question number.
		num_choices (int): Number of answer choices.

	Returns:
		str: Formatted question string.
	"""
	question_type = random.choice(("highest", "lowest"))
	villages = select_villages(args.num_choices)
	random.shuffle(villages)
	z_scores = generate_z_scores(villages)
	totals = {village: sum_z_scores(z_scores[village]) for village in villages}
	question_text = get_question_text(question_type)

	villages.sort()
	choices, answer_text = generate_choices(villages, z_scores, totals, question_type)

	# Format the question with Z-score data
	question_table = format_html_table(villages, z_scores, totals)
	complete_question = bptools.formatBB_MC_Question(N, question_text + question_table, choices, answer_text)
	return complete_question

#==============
def main():
	parser = bptools.make_arg_parser(description="Generate biodiversity questions.")
	parser = bptools.add_choice_args(parser, default=4)
	args = parser.parse_args()

	outfile = bptools.make_outfile(None)
	bptools.collect_and_write_questions(write_question, args, outfile)

#==============
if __name__ == '__main__':
	main()
