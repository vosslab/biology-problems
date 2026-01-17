#!/usr/bin/env python3
# ^^ Specifies the Python3 environment to use for script execution

# Import built-in Python modules
# Provides functions for interacting with the operating system
# Provides functions to generate random numbers and selections
import random
# Provides tools to parse command-line arguments
import itertools

# Import external modules (pip-installed)
# No external modules are used here currently

# Import local modules from the project
# Provides custom functions, such as question formatting and other utilities
import bptools

chartext = "ABCDEFGHJKMPQRSTWXYZ"
chartext = "ABCDEFGHIJKLMOPQRSTUVWXYZ"
charlist = list(chartext)

def color_html(text, rgb_color):
	html = ''
	html += f'<span style="color: {rgb_color}; ">'
	html += text
	html += '</span>'
	return html

telomere_symbols = ['&#x2738;', '&#x2738;'] # 8 pointed stars
telomere_symbols = ['&#x25C0;', '&#x25B6;'] # triangles

#============================================
#============================================
class Fragment():
	"""
	Chromosome fragment defined as a contiguous A..Z run in forward order.
	"""
	def __init__(self, sequence: str, telomere: str, break_point: str,
		rgb_color: str = 'black') -> None:
		# Validate sequence
		if not isinstance(sequence, str):
			raise ValueError("Sequence must be a string")
		if len(sequence) < 3:
			raise ValueError("Sequence length must be at least 3")

		self.sequence = min(sequence, sequence[::-1])

		if self.sequence not in chartext:
			raise ValueError("Sequence must be a contiguous A..Z substring")

		# Validate ends
		ends = (self.sequence[0], self.sequence[-1])

		if telomere == break_point:
			raise ValueError("Telomere and break point must be different")

		if len(telomere) != 1 or telomere not in ends:
			raise ValueError("Telomere must be one of the end letters")

		if len(break_point) != 1 or break_point not in ends:
			raise ValueError("Break point must be one of the end letters")

		self.telomere = telomere
		self.break_point = break_point
		self.rgb_color = rgb_color

	#============================================
	def html_formatted(self, telomere_first: bool = True, show_details: bool = False) -> str:
		"""
		Return HTML for the fragment. If show_details, mark telomere with '**'.
		"""
		html = ''
		html += '<span style="font-family: monospace; font-size: 1.2em; '
		html += 'display: inline-block; margin-left: 1px; margin-right: 1px;">'

		if telomere_first is True and self.sequence[-1] == self.telomere:
			local_sequence = self.sequence[::-1]
		elif telomere_first is False and self.sequence[0] == self.telomere:
			local_sequence = self.sequence[::-1]
		else:
			local_sequence = self.sequence

		if show_details and telomere_first is True:
			html += telomere_symbols[0]

		html += color_html(local_sequence, self.rgb_color)

		if show_details and telomere_first is False:
			html += telomere_symbols[1]

		html += '</span>'
		return html

	#============================================
	def text_formatted(self, telomere_first: bool = True, show_details: bool = False) -> str:
		"""
		Return HTML for the fragment. If show_details, mark telomere with '**'.
		"""
		text = ''
		if telomere_first is True and self.sequence[-1] == self.telomere:
			local_sequence = self.sequence[::-1]
		elif telomere_first is False and self.sequence[0] == self.telomere:
			local_sequence = self.sequence[::-1]
		else:
			local_sequence = self.sequence
		if show_details and telomere_first is True:
			text += '**'
		text += local_sequence
		if show_details and telomere_first is False:
			text += '**'
		return text

	#============================================
	def __lt__(self, other: object) -> bool:
		"""
		Order by start letter only. Sequences do not overlap by design.
		"""
		if not isinstance(other, Fragment):
			return NotImplemented
		return self.sequence[0] < other.sequence[0]

	#============================================
	def __gt__(self, other: object) -> bool:
		"""
		Inverse of __lt__.
		"""
		if not isinstance(other, Fragment):
			return NotImplemented
		return other.__lt__(self)

	#============================================
	# Add a hash that matches __eq__ (ignore rgb_color)
	def __hash__(self) -> int:
		"""
		Hash on identity fields so Fragment can be used in a set or as dict key.

		Returns:
			int: Hash of (sequence, telomere, break_point).
		"""
		return hash((self.sequence, self.telomere, self.break_point))

	#============================================
	def __eq__(self, other: object) -> bool:
		if not isinstance(other, Fragment):
			return False
		if self.sequence != other.sequence:
			return False
		if self.telomere != other.telomere:
			return False
		if self.break_point != other.break_point:
			return False
		return True

#============================================
#============================================
class Chromosome:
	"""
	Two joined fragments that form a chromosome.
	"""
	def __init__(self, fragment_A: Fragment, fragment_B: Fragment,
		telomere_A_improper: bool = False, telomere_B_improper: bool = False) -> None:
		if fragment_A == fragment_B:
			raise ValueError("Fragments cannot be the same")

		if set(fragment_A.sequence) & set(fragment_B.sequence):
			raise ValueError("Fragments cannot overlap")

		if fragment_A < fragment_B:
			self.fragment1 = fragment_A
			self.telomere1_improper = telomere_A_improper
			self.fragment2 = fragment_B
			self.telomere2_improper = telomere_B_improper
		else:
			self.fragment1 = fragment_B
			self.telomere1_improper = telomere_B_improper
			self.fragment2 = fragment_A
			self.telomere2_improper = telomere_A_improper

	#============================================
	def whole_chromosome(self) -> str:
		"""
		Return HTML for the chromosome as the two colored fragments.
		"""
		html = ''
		html += self.fragment1.html_formatted(
			telomere_first=not self.telomere1_improper,
			show_details=True
		)
		html += self.fragment2.html_formatted(
			telomere_first=self.telomere2_improper,
			show_details=True
		)
		return html

	#============================================
	def show_break(self) -> str:
		"""
		Return HTML for the chromosome as the two colored fragments.
		"""
		html = ''
		html += '<span style="font-family: monospace; font-size: 1.2em; '
		html += 'display: inline-block; margin-left: 1px; margin-right: 1px;">'
		if self.telomere1_improper:
			gene1 = self.fragment1.telomere
		else:
			gene1 = self.fragment1.break_point
		html += color_html(gene1, self.fragment1.rgb_color)
		html += '<strong>&#x23D0;</strong>'
		if self.telomere2_improper:
			gene2 = self.fragment2.telomere
		else:
			gene2 = self.fragment2.break_point
		html += color_html(gene2, self.fragment2.rgb_color)
		html += '</span>'
		return html

	#============================================
	def html_formatted(self, show_details: bool = False) -> str:
		"""
		Return HTML for the chromosome as the two colored fragments.
		"""
		html = ''
		html += self.fragment1.html_formatted(
			telomere_first=not self.telomere1_improper,
			show_details=show_details
		)
		html += '<strong>&#x2261;</strong>'
		html += self.fragment2.html_formatted(
			telomere_first=self.telomere2_improper,
			show_details=show_details
		)
		return html

	#============================================
	def __str__(self) -> str:
		"""
		Return text string for print() and str().
		"""
		text = '  '
		text += self.fragment1.text_formatted(
			telomere_first=not self.telomere1_improper,
			show_details=True
		)
		text += '|'
		text += self.fragment2.text_formatted(
			telomere_first=self.telomere2_improper,
			show_details=True
		)
		return text

	#============================================
	# Mirror __str__ so the REPL shows the same HTML
	def __repr__(self) -> str:
		"""
		Return HTML string for repr().
		"""
		return self.__str__()
# Simple assertion tests
a = Fragment('ABC', 'A', 'C')
d = Fragment('DEF', 'D', 'F')
proper = Chromosome(a, d)
improper = Chromosome(a, d, telomere_A_improper=True, telomere_B_improper=True)
assert '|' in str(proper)
assert '|' in str(improper)

#===========================================================
# Fixed color per segment
SEGMENT_COLORS = [
	"DarkRed",
	"OrangeRed",
	"DarkBlue",
	"DarkGreen",
]

#====================
def alloc_multinomial(balls: int, buckets: int) -> list:
	"""
	Allocate balls into buckets by independent random throws.

	Args:
		balls (int): Number of balls to throw.
		buckets (int): Number of destination buckets.

	Returns:
		list: Length-buckets counts that sum to balls.
	"""
	# Choose one bucket index for each ball
	choices = random.choices(range(buckets), k=balls)
	# Start all bucket counts at zero
	ball_counts = [0] * buckets
	# Tally how many balls landed in each bucket
	for idx in choices:
		ball_counts[idx] += 1
	# Return counts per bucket
	return ball_counts

# Simple assertion test for the function: 'alloc_multinomial'
_result = alloc_multinomial(9, 5)
assert len(_result) == 5 and sum(_result) == 9

#====================
def make_chromosomes(min_chromosome_size: int, min_fragment_size: int):
	"""
	Create two chromosomes as contiguous runs with a gap between them.
	Splits slack characters across five buckets to place and size runs.

	Args:
		min_chromosome_size (int): Minimum size for each chromosome run.

	Returns:
		tuple: (chromosome1: Chromosome, chromosome2: Chromosome)
	"""
	# Compute the minimal layout requirement
	base_total = 2 * min_chromosome_size + 1
	# Compute how many characters remain to distribute
	free = len(chartext) - base_total

	# Allocate the free characters across five buckets
	# Buckets: leftpad, extra_len1, extra_gap, extra_len2, rightpad
	alloc = alloc_multinomial(free, 5)
	# Unpack bucket sizes
	leftpad, extra1, gap_extra, extra2, _rightpad = alloc

	# Compute chromosome 1 final length
	len1 = min_chromosome_size + extra1
	# Compute mandatory gap size (at least one)
	gap = 1 + gap_extra
	# Compute chromosome 2 final length
	len2 = min_chromosome_size + extra2

	# Compute start index of chromosome 1
	start1 = leftpad
	# Compute end index of chromosome 1
	end1 = start1 + len1
	# Compute start index of chromosome 2
	start2 = end1 + gap
	# Compute end index of chromosome 2
	end2 = start2 + len2

	# Slice out chromosome 1 sequence
	chromosome1_seq = chartext[start1:end1]
	# Slice out chromosome 2 sequence
	chromosome2_seq = chartext[start2:end2]

	# Compute sizes for cut placement
	chromosome1_size = len(chromosome1_seq)
	chromosome2_size = len(chromosome2_seq)

	# Choose a valid internal cut for chromosome 1
	chromosome1_cut = random.randint(
		min_fragment_size, chromosome1_size - min_fragment_size
	)
	# Choose a valid internal cut for chromosome 2
	chromosome2_cut = random.randint(
		min_fragment_size, chromosome2_size - min_fragment_size
	)

	# Split chromosome 1 into A then B
	chromosome1_A = chromosome1_seq[:chromosome1_cut]
	chromosome1_B = chromosome1_seq[chromosome1_cut:]
	# Split chromosome 2 into A then B
	chromosome2_A = chromosome2_seq[:chromosome2_cut]
	chromosome2_B = chromosome2_seq[chromosome2_cut:]

	# Create fragment 1A with telomere at the left end
	fragment1_A = Fragment(
		chromosome1_A, telomere=chromosome1_A[0], break_point=chromosome1_A[-1], rgb_color=SEGMENT_COLORS[0],
	)
	# Create fragment 1B with telomere at the right end
	fragment1_B = Fragment(
		chromosome1_B, telomere=chromosome1_B[-1], break_point=chromosome1_B[0], rgb_color=SEGMENT_COLORS[1],
	)
	# Create fragment 2A with telomere at the left end
	fragment2_A = Fragment(
		chromosome2_A, telomere=chromosome2_A[0], break_point=chromosome2_A[-1], rgb_color=SEGMENT_COLORS[2],
	)
	# Create fragment 2B with telomere at the right end
	fragment2_B = Fragment(
		chromosome2_B, telomere=chromosome2_B[-1], break_point=chromosome2_B[0], rgb_color=SEGMENT_COLORS[3],
	)

	# Assemble chromosome 1 from its two fragments
	chromosome1 = Chromosome(fragment1_A, fragment1_B)
	# Assemble chromosome 2 from its two fragments
	chromosome2 = Chromosome(fragment2_A, fragment2_B)

	# Return the pair of chromosomes
	return chromosome1, chromosome2

#===========================================================
def make_all_possible_translocations(chromosome1, chromosome2):
	"""
	Build the four cross-chromosome derivatives:
	(fragment from chromosome1) + (fragment from chromosome2).
	"""
	translocated_chromosomes_list = []
	for fragment_A in (chromosome1.fragment1, chromosome1.fragment2):
		for fragment_B in (chromosome2.fragment1, chromosome2.fragment2):
			new_chromosome = Chromosome(fragment_A, fragment_B)
			translocated_chromosomes_list.append(new_chromosome)
	if len(translocated_chromosomes_list) != 4:
		raise ValueError("Expected exactly four derivatives")
	return translocated_chromosomes_list

#===========================================================
def make_all_improper_translocations(chromosome1, chromosome2):
	"""
	Build the four cross-chromosome derivatives:
	(fragment from chromosome1) + (fragment from chromosome2).
	"""
	all_fragments = [chromosome1.fragment1, chromosome1.fragment2, chromosome2.fragment1, chromosome2.fragment2]
	improper_chromosomes_list = []
	for fragment_A, fragment_B in itertools.combinations(all_fragments, 2):
		new_chromosome1 = Chromosome(fragment_A, fragment_B, telomere_A_improper=False, telomere_B_improper=True)
		new_chromosome2 = Chromosome(fragment_A, fragment_B, telomere_A_improper=True, telomere_B_improper=False)
		new_chromosome3 = Chromosome(fragment_A, fragment_B, telomere_A_improper=True, telomere_B_improper=True)
		improper_chromosomes_list.append(new_chromosome1)
		improper_chromosomes_list.append(new_chromosome2)
		improper_chromosomes_list.append(new_chromosome3)
	if len(improper_chromosomes_list) != 18:
		raise ValueError("Expected exactly eighteen derivatives")
	return improper_chromosomes_list

#===========================================================
#===========================================================
# This function generates multiple answer choices for a question.
def generate_choices(chromosome1, chromosome2) -> (list, str):
	"""
	Generates a list of answer choices along with the correct answer.
	"""
	choices_list = []
	translocated_chromosomes_list = make_all_possible_translocations(chromosome1, chromosome2)
	random.shuffle(translocated_chromosomes_list)
	print("Translocated chromosomes")
	for tchr in translocated_chromosomes_list:
		choices_list.append(tchr.html_formatted(show_details=False))
		print(tchr)

	improper_chromosomes_list = make_all_improper_translocations(chromosome1, chromosome2)
	print(f"Made {len(improper_chromosomes_list)} improper chromosomes")
	random.shuffle(improper_chromosomes_list)
	print("Improper chromosomes")
	for imchr in improper_chromosomes_list:
		print(imchr)

	wrong_choice = random.choice(improper_chromosomes_list)
	answer_text = wrong_choice.html_formatted(show_details=False)
	choices_list.append(answer_text)

	random.shuffle(choices_list)
	# Return the list of choices and the correct answer
	return choices_list, answer_text

#===========================================================
#===========================================================
# This function generates and returns the main question text.
def get_question_text(chromosome1, chromosome2) -> str:
	"""
	Generates and returns the main text for the question.
	"""
	question_text = ''

	# Short background on reciprocal translocation
	question_text += "<p>"
	question_text += "In a reciprocal translocation, two nonhomologous chromosomes each break "
	question_text += "once and exchange their terminal fragments. Gene order within each "
	question_text += "fragment is preserved; only the junctions change."
	question_text += "</p>"

	question_text += "<p>Two chromosomes with the gene sequences  "
	question_text += chromosome1.whole_chromosome()
	question_text += "  and  "
	question_text += chromosome2.whole_chromosome()
	question_text += "  undergo a reciprocal translocation after breaks between  "
	question_text += chromosome1.show_break()
	question_text += "  and  "
	question_text += chromosome2.show_break()
	question_text += ", where the symbols: "
	question_text += " and ".join(telomere_symbols)
	question_text += " represent the telomeres. </p>"

	question_text += "<p>Which one of the following is <strong>NOT</strong> a possible product of this translocation?</p>"

	# Return the complete question text
	return question_text

#===========================================================
def write_question(N, args):
	#this is a BIG function
	chromosome1, chromosome2 = make_chromosomes(args.min_chromosome_size, args.min_fragment_size)
	print("Original chromosomes")
	print(chromosome1)
	print(chromosome2)

	question_text = get_question_text(chromosome1, chromosome2)
	choices_list, answer_text = generate_choices(chromosome1, chromosome2)

	bb_format = bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)
	return bb_format


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

	# Add an argument to specify the number of answer choices for each question
	parser.add_argument(
		'-n', '--min-size', '--min-chromosome-size', type=int, default=7, dest='min_chromosome_size',
		help="Minimum size of chromosomes."
	)

	# Add an argument to specify the number of answer choices for each question
	parser.add_argument(
		'-f', '--min-fragment-size', type=int, default=3, dest='min_fragment_size',
		help="Minimum size of fragments."
	)

	# Parse the provided command-line arguments and return them
	args = parser.parse_args()

	if args.min_fragment_size < 2:
		raise ValueError("Sorry, you must have at least 2 genes per fragment")
	if args.min_chromosome_size < 2 * args.min_fragment_size:
		raise ValueError(f"Sorry, chromosomes min={args.min_chromosome_size} must be at least twice as long as fragments min={args.min_fragment_size}")
	if args.min_fragment_size > 5:
		raise ValueError("Sorry, you cant have a minimum bigger than 5 genes per fragment")
	if args.min_chromosome_size > 9:
		raise ValueError("Sorry, you cant have a minimum bigger than 9 genes per chromosome")
	return args

#===========================================================
#===========================================================
# This function serves as the entry point for generating and saving questions.
def main():
	"""
	Main function that orchestrates question generation and file output.

	Workflow:
	1. Parse command-line arguments.
	2. Generate the output filename using script name and args.
	3. Generate formatted questions using write_question().
	4. Shuffle and trim the list if exceeding max_questions.
	5. Write all formatted questions to output file.
	6. Print stats and status.
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
