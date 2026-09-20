
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


def test_circular_digest_calculates_wraparound_band_sizes():
	circular_digest = import_from_repo_path(
		"problems/molecular_biology-problems/restriction_enzymes/circular_digest.py"
	)
	fragment_sizes = circular_digest.get_circular_fragment_sizes(12, [2, 7])
	assert fragment_sizes == [5, 7]
	assert circular_digest.get_circular_fragment_sizes(12, [0, 5]) == [5, 7]


def test_circular_digest_origin_is_top_center():
	circular_digest = import_from_repo_path(
		"problems/molecular_biology-problems/restriction_enzymes/circular_digest.py"
	)
	x_position, y_position, angle_deg, region = circular_digest.get_perimeter_point(0, 10)
	assert region == 'top'
	assert abs(x_position - (circular_digest.MAP_LEFT + circular_digest.MAP_WIDTH / 2)) < 1
	assert abs(y_position - (circular_digest.MAP_TOP + circular_digest.DNA_STROKE / 2)) < 1
	assert abs(angle_deg - 270) < 1


def test_circular_digest_uses_full_perimeter_for_coordinates():
	circular_digest = import_from_repo_path(
		"problems/molecular_biology-problems/restriction_enzymes/circular_digest.py"
	)
	expected = 0.2 * circular_digest.perimeter_length()
	x_position, y_position, _angle_deg, _region = circular_digest.get_perimeter_point(2, 10)
	mapped_x, mapped_y, _mapped_angle, _mapped_region = circular_digest.point_at_distance(expected)
	assert abs(x_position - mapped_x) < 1
	assert abs(y_position - mapped_y) < 1
	straight_only = 2 * (circular_digest.MAP_WIDTH - 2 * circular_digest.MAP_RADIUS)
	straight_only += 2 * (circular_digest.MAP_HEIGHT - 2 * circular_digest.MAP_RADIUS)
	wrong_x, wrong_y, _wrong_angle, _wrong_region = circular_digest.point_at_distance(0.2 * straight_only)
	assert abs(x_position - wrong_x) > 5 or abs(y_position - wrong_y) > 5


def test_circular_digest_enzyme_sites_are_straight_edge_integers():
	circular_digest = import_from_repo_path(
		"problems/molecular_biology-problems/restriction_enzymes/circular_digest.py"
	)
	for length, selected_count in ((10, 2), (12, 3), (16, 3)):
		eligible = [
			site for site in range(1, length)
			if circular_digest.is_enzyme_eligible(site, length)
		]
		assert len(eligible) >= selected_count + 1
		for site in range(1, length):
			_x_position, _y_position, _angle_deg, region = circular_digest.get_perimeter_point(
				site, length
			)
			if circular_digest.is_enzyme_eligible(site, length):
				assert region in circular_digest.STRAIGHT_REGIONS
			if region not in circular_digest.STRAIGHT_REGIONS:
				assert circular_digest.is_enzyme_eligible(site, length) is False


def test_circular_digest_places_distractor_enzyme_at_zero():
	circular_digest = import_from_repo_path(
		"problems/molecular_biology-problems/restriction_enzymes/circular_digest.py"
	)
	for length, selected_count, difficulty in (
			(10, 2, 'easy'), (12, 3, 'medium'), (16, 3, 'rigorous')
			):
		for _ in range(20):
			selected_sites, distractor_sites = circular_digest.choose_sites(
				length, selected_count, difficulty
			)
			assert 0 not in selected_sites
			assert distractor_sites[0] == 0
			assert len(selected_sites) == selected_count
			assert len(distractor_sites) == 2
			for site in selected_sites + [value for value in distractor_sites if value != 0]:
				assert circular_digest.is_enzyme_eligible(site, length) is True
			selected_bands = set(
				circular_digest.get_circular_fragment_sizes(length, selected_sites)
			)
			distractor_bands = set(
				circular_digest.get_circular_fragment_sizes(length, distractor_sites)
			)
			overlap = selected_bands.intersection(distractor_bands)
			assert len(overlap) / len(selected_bands) <= 0.5


def test_digest_lib_uses_the_three_topology_formulas():
	digest_lib = import_from_repo_path(
		"problems/molecular_biology-problems/restriction_enzymes/digest_lib.py"
	)
	length = 10
	sites = [2, 6]
	assert digest_lib.linear_fragment_list(length, sites) == [2, 4, 4]
	assert digest_lib.linear_strand_list(length, sites) == [4]
	assert digest_lib.circular_fragment_list(length, sites) == [4, 6]
	assert digest_lib.shared_correct_fraction({2, 4, 6}, {2, 8}) == 1 / 3
	assert digest_lib.map_is_acceptable('circular', 10, [2, 6], [0, 5], 'easy') is True
	assert digest_lib.map_is_acceptable('circular', 10, [2, 6], [0, 4], 'easy') is False
	# Strand answers drop selected end pieces; distractor overlap still uses those ends.
	selected_strand = digest_lib.linear_strand_list(10, [2, 6])
	distractor_on_strand = digest_lib.linear_fragment_list(10, [4])
	assert selected_strand == [4]
	assert distractor_on_strand == [4, 6]
