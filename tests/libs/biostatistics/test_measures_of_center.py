"""Protect worked answers and the calculator-free median-change contract."""

# Standard Library
import re
import random
import argparse
import statistics

# PIP3 modules
import pytest

# Local test helpers
from lib_test_utils import import_from_repo_path


@pytest.mark.parametrize("values", [[2, 2, 4, 6, 16], [1, 3, 6, 9, 9]])
def test_worked_answers_agree_with_independent_statistics(values: list[int]) -> None:
	mod = import_from_repo_path("problems/biostatistics-problems/measures_of_center.py")
	choices = mod.matching_choices(values)
	results = [float(choice.rsplit("=", 1)[-1].strip()) for choice in choices]
	expected = [statistics.mean(values), statistics.median(values),
		statistics.mode(values), (min(values) + max(values)) / 2]
	assert results == expected
	assert len(set(results)) == len(results)
	assert choices[0].startswith("(" + " + ".join(str(value) for value in values) + ")")
	assert choices[3].startswith(f"({min(values)} + {max(values)}) / 2 = ")


def test_increasing_unique_maximum_preserves_the_median() -> None:
	mod = import_from_repo_path("problems/biostatistics-problems/measures_of_center.py")
	state = random.getstate()
	try:
		random.seed(318)
		item = mod.write_question(1, argparse.Namespace(kind="median_change"))
	finally:
		random.setstate(state)
	data_text = re.search(r"compare their tips: (.*?)\.", item.question_text)[1]
	values = [int(value) for value in re.findall(r"\$(\d+)", data_text)]
	old_max, extra_tip, new_max = map(int, re.search(
		r"earned \$(\d+) receives another \$(\d+).*?total to \$(\d+)",
		item.question_text).groups())
	assert old_max + extra_tip == new_max
	mean, median = map(float, re.search(
		r"mean is \$(\d+(?:\.\d+)?) per server, and the median is \$(\d+)",
		item.question_text).groups())
	assert mean == statistics.mean(values)
	assert median == statistics.median(values)
	changed = values[:-1] + [new_max]
	assert old_max == max(values) and values.count(old_max) == 1
	assert new_max > old_max
	assert statistics.median(changed) == statistics.median(values)
	assert item.answer_text == "Does not change"
