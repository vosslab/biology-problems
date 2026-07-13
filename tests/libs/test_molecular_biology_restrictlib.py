
import datetime

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


def test_restrictlib_uses_fresh_cached_web_data(monkeypatch, tmp_path):
	restrictlib = import_from_repo_path(
		"problems/molecular_biology-problems/restriction_enzymes/restrictlib.py"
	)
	enzyme_class = restrictlib.enzyme_name_to_class("EcoRI")
	now = datetime.datetime.now(datetime.timezone.utc)
	restrictlib.WEB_DATA_CACHE_PATH = str(tmp_path / "restriction_cache.yml")
	restrictlib.WEB_DATA_CACHE = {
		"schema_version": 1,
		"max_age_days": restrictlib.WEB_DATA_CACHE_MAX_AGE.days,
		"enzymes": {
			"EcoRI": {
				"fetched_at": now.isoformat(timespec="seconds"),
				"data": {"Organism": "Escherichia coli RY13"},
			},
		},
	}
	def fail_fetch(enzyme):
		raise AssertionError(f"unexpected web request for {enzyme}")

	monkeypatch.setattr(restrictlib, "fetch_web_data", fail_fetch)
	data = restrictlib.get_web_data(enzyme_class)
	assert data["Organism"] == "Escherichia coli RY13"
