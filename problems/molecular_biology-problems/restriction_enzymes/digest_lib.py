"""Shared command-line, enzyme, and digest-evaluation helpers."""

import html

import bptools
import restrictlib


#============================================
def make_digest_parser(description: str):
	"""Return a parser with the options common to restriction-digest generators."""
	parser = bptools.make_arg_parser(description=description)
	parser = bptools.add_difficulty_args(parser)
	parser.add_argument(
		'-n', '--length', type=int, default=None,
		help='Length of the DNA molecule in kb.'
	)
	return parser


#============================================
def choose_distinct_enzyme_names() -> tuple[str, str]:
	"""Select two short restriction-enzyme names with distinct initial letters."""
	enzymes = restrictlib.get_enzyme_list()
	first_enzyme = restrictlib.random_enzyme_one_end(enzymes)
	second_enzyme = restrictlib.random_enzyme_one_end(
		enzymes, badletter=first_enzyme.__name__[0]
	)
	enzyme_names = (first_enzyme.__name__, second_enzyme.__name__)
	return enzyme_names


#============================================
def enzyme_context_paragraph(first_html: str, first_name: str, second_html: str,
		second_name: str) -> str:
	"""Return a short source paragraph for two enzymes, used as the question opening."""
	first_organism = restrictlib.get_web_data(
		restrictlib.enzyme_name_to_class(first_name)
	)['Organism']
	second_organism = restrictlib.get_web_data(
		restrictlib.enzyme_name_to_class(second_name)
	)['Organism']
	paragraph = (
		'<p>Restriction enzymes are proteins that cut DNA at specific sequences. '
		+ first_html + ' is derived from ' + html.escape(first_organism, quote=True)
		+ ', and ' + second_html + ' is derived from '
		+ html.escape(second_organism, quote=True)
		+ '. Both enzymes are labeled on the map.</p>'
	)
	return paragraph


#============================================
def linear_fragment_list(length: int, sites: list[int]) -> list[int]:
	"""Return fragment lengths including both physical end pieces."""
	sorted_sites = sorted(sites)
	fragments = [sorted_sites[0]]
	for index in range(len(sorted_sites) - 1):
		fragments.append(sorted_sites[index + 1] - sorted_sites[index])
	fragments.append(length - sorted_sites[-1])
	return fragments


#============================================
def linear_strand_list(length: int, sites: list[int]) -> list[int]:
	"""Return only intervals between consecutive sites; ends are not gel bands."""
	sorted_sites = sorted(sites)
	fragments = []
	for index in range(len(sorted_sites) - 1):
		fragments.append(sorted_sites[index + 1] - sorted_sites[index])
	return fragments


#============================================
def circular_fragment_list(length: int, sites: list[int]) -> list[int]:
	"""Return circular intervals including wraparound; 0 and length are one coordinate."""
	normalized_sites = []
	for site in sites:
		if site == length:
			site = 0
		if site not in normalized_sites:
			normalized_sites.append(site)
	sorted_sites = sorted(normalized_sites)
	fragments = []
	for index in range(len(sorted_sites) - 1):
		fragments.append(sorted_sites[index + 1] - sorted_sites[index])
	fragments.append(length - sorted_sites[-1] + sorted_sites[0])
	return fragments


#============================================
def digest_fragments(topology: str, length: int, sites: list[int]) -> list[int]:
	"""Return fragment lengths for one enzyme under the question DNA type."""
	if topology == 'fragment':
		fragments = linear_fragment_list(length, sites)
	elif topology == 'strand':
		fragments = linear_strand_list(length, sites)
	elif topology == 'circular':
		fragments = circular_fragment_list(length, sites)
	else:
		raise ValueError(f'Unknown digest topology: {topology}')
	return fragments


#============================================
def shared_correct_fraction(correct_bands: set[int], distractor_bands: set[int]) -> float:
	"""Return the fraction of correct distinct bands that also appear in the distractor."""
	overlap = correct_bands.intersection(distractor_bands)
	fraction = len(overlap) / len(correct_bands)
	return fraction


#============================================
def map_is_acceptable(topology: str, length: int, selected_sites: list[int],
		distractor_sites: list[int], difficulty: str) -> bool:
	"""Return True when the map meets validity and the requested difficulty."""
	correct_fragments = digest_fragments(topology, length, selected_sites)
	# Strand questions drop the two outside pieces for the selected enzyme only.
	if topology == 'strand':
		distractor_fragments = linear_fragment_list(length, distractor_sites)
	else:
		distractor_fragments = digest_fragments(topology, length, distractor_sites)
	correct_bands = set(correct_fragments)
	distractor_bands = set(distractor_fragments)
	if len(correct_bands) < 2:
		acceptable = False
		return acceptable
	fraction = shared_correct_fraction(correct_bands, distractor_bands)
	if fraction > 0.5:
		acceptable = False
		return acceptable
	# Co-migration is a selected-enzyme property.
	co_migration = len(correct_fragments) > len(correct_bands)
	if difficulty in ('easy', 'medium') and co_migration is True:
		acceptable = False
		return acceptable
	if difficulty == 'rigorous' and co_migration is False:
		acceptable = False
		return acceptable
	if topology == 'strand':
		fragment_reading = set(linear_fragment_list(length, selected_sites))
		if fragment_reading == correct_bands:
			acceptable = False
			return acceptable
	acceptable = True
	return acceptable
