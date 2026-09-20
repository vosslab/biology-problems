
from bs4 import BeautifulSoup

from lib_test_utils import import_from_repo_path


def test_restrictlib_good_ending_and_strict_sequence():
	restrictlib = import_from_repo_path(
		"problems/molecular_biology-problems/restriction_enzymes/restrictlib.py"
	)
	assert restrictlib.check_for_good_ending("EcoRI") is True
	assert restrictlib.check_for_good_ending("Eco_mut1") is True
	assert restrictlib.check_for_good_ending("Eco_3") is True
	assert restrictlib.check_for_good_ending("Eco") is False

	enzyme_class = restrictlib.enzyme_name_to_class("EcoRI")
	assert restrictlib.has_strict_sequence(enzyme_class) is True


def test_restrictlib_parses_labeled_web_fields():
	restrictlib = import_from_repo_path(
		"problems/molecular_biology-problems/restriction_enzymes/restrictlib.py"
	)
	html = b"""
		<font><b>Organism: </b><a><i>Escherichia</i> <i>coli</i> RY13</a><br/>
		<b>Growth Temperature: </b>37 degrees<br/></font>
	"""
	data = restrictlib._parse_web_data(html, "https://example.test/EcoRI")
	assert data["Organism"] == "Escherichia coli RY13"
	assert data["Growth Temperature"] == "37 degrees"


def test_linear_digest_table_rows_have_explicit_cells_for_terminal_rendering():
	linear_digest = import_from_repo_path(
		"problems/molecular_biology-problems/restriction_enzymes/linear_digest.py"
	)
	table = BeautifulSoup(linear_digest.makeTable(4, {1: "EcoRI"}), "html.parser")
	cell_counts = [len(row.find_all("td", recursive=False)) for row in table.find_all("tr")]
	assert cell_counts == [12, 12, 12, 12]


def test_circular_digest_calculates_wraparound_band_sizes():
	circular_digest = import_from_repo_path(
		"problems/molecular_biology-problems/restriction_enzymes/circular_digest.py"
	)
	fragment_sizes = circular_digest.get_circular_fragment_sizes(12, [2, 7])
	assert fragment_sizes == [5, 7]
