#!/usr/bin/env python3
"""Calculator-free measures-of-center matching and median-change questions.

Authoring contract: MAT applies four measures to ordered data; MC analyzes how
changing an extreme observation affects the median. Each instance randomly draws
small integer data. Matching choices show completed arithmetic, following the
"Show the setup" exemplar in docs/QUESTION_EXEMPLARS.md. Confusions are mean vs.
midrange and median vs. mode. MC errors transfer the change in the mean or an
extreme value to the median. Collection applies the shared anti-cheat defaults.

Example: 2, 2, 4, 6, 16 -> mean 6, median 4, mode 2, midrange 9. Replacing 16
with 26 leaves the median unchanged. BBQ matching preserves four matched choices;
it cannot carry an additional unused answer. No student calculation is required.
"""

# Standard Library
import random
import argparse
import fractions

# Local repo modules
import bptools
from qti_package_maker.assessment_items import item_types


DATA_TEMPLATES = ((2, 2, 4, 6, 16), (1, 3, 6, 9, 9))
MEASURES = ("Mean", "Median", "Mode", "Midrange")


#============================================
def generate_dataset(kind: str) -> list[int]:
	"""Draw five ordered observations with four distinct measures of center."""
	# A unique maximum keeps "the largest value changes" unambiguous in MC items.
	template = DATA_TEMPLATES[0] if kind == "median_change" else random.choice(DATA_TEMPLATES)
	scale = random.randint(1, 3)
	offset = random.randint(0, 12)
	values = [scale * value + offset for value in template]
	return values


#============================================
def format_value(value: fractions.Fraction) -> str:
	"""Show whole numbers or exact tenths/halves for these five-value datasets."""
	if value.denominator == 1:
		text = str(value.numerator)
	else:
		text = f"{float(value):.1f}"
	return text


#============================================
def dataset_text(values: list[int]) -> str:
	"""Format the data as a compact, ordered line."""
	text = ", ".join(str(value) for value in values)
	return text


#============================================
def matching_choices(values: list[int]) -> list[str]:
	"""Return worked answers in the same order as MEASURES."""
	mean = fractions.Fraction(sum(values), len(values))
	median = values[len(values) // 2]
	mode = max(set(values), key=values.count)
	midrange = fractions.Fraction(values[0] + values[-1], 2)
	addition = " + ".join(str(value) for value in values)
	choices = [
		f"({addition}) / {len(values)} = {format_value(mean)}",
		str(median),
		str(mode),
		f"({values[0]} + {values[-1]}) / 2 = {format_value(midrange)}",
	]
	return choices


#============================================
def get_question_text(values: list[int], kind: str, new_maximum: int | None = None) -> str:
	"""Put the data before the matching instruction or median-change question."""
	if kind == "matching":
		text = f"<p>Data: {bptools.html_monospace(dataset_text(values), use_nbsp=False)}</p>"
		text += "<p>Match each of the following measures of center with their "
		text += "corresponding values. Each choice is used exactly once.</p>"
	else:
		mean = format_value(fractions.Fraction(sum(values), len(values)))
		median = values[len(values) // 2]
		tips = ", ".join(f"${value}" for value in values[:-1])
		tips += f", and ${values[-1]}"
		extra_tip = new_maximum - values[-1]
		text = f"<p>Five servers are closing up for the night and compare their tips: {tips}. "
		text += f"The mean is ${mean} per server, and the median is ${median}.</p>"
		text += f"<p>The server who earned ${values[-1]} receives another ${extra_tip} tip "
		text += f"from their last table, raising their total to ${new_maximum}. "
		text += "The other four totals stay the same. "
		text += "How does this change the median amount earned?</p>"
	return text


#============================================
def write_question(N: int, args: argparse.Namespace) -> item_types.BaseItem:
	"""Draw an instance and return a native bptools assessment item."""
	values = generate_dataset(args.kind)
	if args.kind == "matching":
		question = get_question_text(values, args.kind)
		choices = matching_choices(values)
		# Shuffle pairs together; the matching formatter preserves their association.
		order = random.sample(range(len(MEASURES)), len(MEASURES))
		prompts = [MEASURES[index] for index in order]
		matches = [choices[index] for index in order]
		item = bptools.formatBB_MAT_Question(N, question, prompts, matches)
	else:
		new_maximum = values[-1] + random.randint(5, 20)
		question = get_question_text(values, args.kind, new_maximum)
		# Error: treats the move away from the middle as lowering the middle.
		# Error: transfers the increase in the mean/midrange to the median.
		# Keep the directional ladder in its natural order.
		choices = ["Decreases", "Does not change", "Increases"]
		item = bptools.formatBB_MC_Question(N, question, choices, "Does not change")
	return item


#============================================
def parse_arguments() -> argparse.Namespace:
	"""Use shared output options and select one of the two question families."""
	parser = bptools.make_arg_parser(description=__doc__.split("\n", 1)[0])
	group = parser.add_mutually_exclusive_group()
	group.add_argument("-m", "--matching", dest="kind", action="store_const",
		const="matching", help="Match four measures to completed calculations (default).")
	group.add_argument("-C", "--median-change", dest="kind", action="store_const",
		const="median_change", help="Ask how increasing the maximum affects the median.")
	parser.set_defaults(kind="matching")
	args = parser.parse_args()
	return args


#============================================
def main() -> None:
	"""Generate BBQ output and the optional shared preview/export formats."""
	args = parse_arguments()
	outfile = bptools.make_outfile(args.kind)
	bptools.collect_and_write_questions(write_question, args, outfile)


if __name__ == "__main__":
	main()
