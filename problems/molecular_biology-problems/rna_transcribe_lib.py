"""Core RNA transcription sequence, prompt, and answer generation.

Prime questions respect antiparallel strands. Directionless questions ask for
RNA bases aligned left-to-right with the template, without testing direction.
For example, template 3'-ATGCCG-5' yields RNA 5'-UACGGC-3'; AUGCCG and
CGGCAU are wrong answers when displayed 5' to 3'.
"""

# Standard Library
import random

# local repo modules
import seqlib
import bptools


#============================================
def transcribe_sequence(sequence: str, strand: str, fivetothree: bool) -> str:
	"""Return RNA in the 5' to 3' direction for a displayed DNA strand."""
	if strand == 'template':
		coding_sequence = seqlib.complement(sequence)
		if fivetothree:
			coding_sequence = seqlib.flip(coding_sequence)
	elif strand == 'coding':
		coding_sequence = sequence if fivetothree else seqlib.flip(sequence)
	else:
		raise ValueError(f'Unknown DNA strand: {strand}')
	answer = seqlib.transcribe(coding_sequence)
	return answer


#============================================
def fib_answers(answer: str, prime: bool) -> list[str]:
	"""Accept plain or comma-grouped RNA, with optional prime notation."""
	answers = [answer, seqlib.insertCommas(answer)]
	if prime:
		for sequence in list(answers):
			answers.append(f"5'-{sequence}-3'")
			answers.append(f'5&prime;-{sequence}-3&prime;')
	answers = list(dict.fromkeys(answers))
	return answers


#============================================
def get_question_text(sequence: str, strand: str, fivetothree: bool,
		question_type: str, direction_mode: str) -> str:
	"""Build a strand table and student-facing transcription instructions."""
	if direction_mode == 'prime':
		question = seqlib.Single_Strand_Table(sequence, fivetothree=fivetothree)
	else:
		question = seqlib.Single_Strand_Table_No_Primes(sequence)
	strand_label = 'template' if strand == 'template' else 'non-template/coding'
	if question_type == 'mc':
		question += '<p>Which sequence is the mRNA product produced from transcription '
	else:
		question += '<p>Enter the mRNA sequence produced from transcription '
	question += f'of the DNA {strand_label} strand above.</p>'
	if direction_mode == 'directionless':
		question += '<p>Direction is not tested. Write the RNA bases aligned '
		question += 'left-to-right with the DNA template shown above.</p>'
	elif question_type == 'mc':
		question += '<p>Hint: pay close attention to the 5&prime; and 3&prime; directions!</p>'
	else:
		question += '<p>Write your RNA sequence in the 5&prime; to 3&prime; direction.</p>'
	if question_type == 'fib':
		question += '<p><i>You may include a comma every 3 letters. '
		question += 'Do not add extra commas or spaces.</i></p>'
		if direction_mode == 'directionless':
			question += '<p>Enter only the RNA bases, without direction labels.</p>'
	return question


#============================================
def generate_choices(sequence: str, answer: str, num_choices: int) -> list[str]:
	"""Mix orientation/base-pairing mistakes with one correct RNA sequence."""
	half = len(sequence) // 2
	complement = seqlib.complement(sequence)
	candidates = [
		seqlib.transcribe(sequence),
		seqlib.transcribe(seqlib.flip(sequence)),
		seqlib.transcribe(complement),
		seqlib.transcribe(seqlib.flip(complement)),
		seqlib.transcribe(sequence[:half] + complement[half:]),
		seqlib.transcribe(complement[:half] + sequence[half:]),
	]
	wrong_choices = list(dict.fromkeys(choice for choice in candidates if choice != answer))
	# Short sequences can collapse orientation distractors; use single-base mistakes.
	if len(wrong_choices) < num_choices - 1:
		for index in range(len(answer)):
			for base in 'ACGU':
				candidate = answer[:index] + base + answer[index + 1:]
				if candidate != answer and candidate not in wrong_choices:
					wrong_choices.append(candidate)
	random.shuffle(wrong_choices)
	choices = wrong_choices[:num_choices - 1] + [answer]
	random.shuffle(choices)
	return choices


#============================================
def generate_question(N: int, sequence_len: int, question_type: str,
		direction_mode: str, num_choices: int = 5) -> object:
	"""Generate one randomized MC or FIB transcription item."""
	if question_type not in ('mc', 'fib') or direction_mode not in ('directionless', 'prime'):
		raise ValueError('Unknown question format or direction mode')
	if sequence_len < 2 or (question_type == 'mc' and not 2 <= num_choices <= 5):
		raise ValueError('Use a sequence length of at least 2 and 2 to 5 MC choices')
	sequence = seqlib.makeSequence(sequence_len)
	strand = 'template'
	fivetothree = False
	if direction_mode == 'prime':
		fivetothree = random.choice([True, False])
		if question_type == 'fib':
			strand = random.choice(['template', 'coding'])
	answer = transcribe_sequence(sequence, strand, fivetothree)
	question = get_question_text(sequence, strand, fivetothree, question_type, direction_mode)
	if question_type == 'fib':
		answers = fib_answers(answer, prime=direction_mode == 'prime')
		item = bptools.formatBB_FIB_Question(N, question, answers)
	else:
		choices = generate_choices(sequence, answer, num_choices)
		choice_tables = []
		choice_fivetothree = random.choice([True, False])
		for choice in choices:
			if direction_mode == 'prime':
				display = choice if choice_fivetothree else seqlib.flip(choice)
				table = seqlib.Single_Strand_Table(display, fivetothree=choice_fivetothree)
			else:
				table = seqlib.Single_Strand_Table_No_Primes(choice)
			choice_tables.append(table)
			if choice == answer:
				answer_table = table
		item = bptools.formatBB_MC_Question(N, question, choice_tables, answer_table)
	return item
