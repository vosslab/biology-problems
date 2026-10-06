"""Workload bands combining family size, branching, and tracing depth.

These are practical presets, not calibrated student difficulty scores. Teaching
acceptance is shared across levels; harder settings never relax the evidence.
Individual questions can overlap in difficulty despite different preset bands.
"""

# local repo modules
import pedigree_lib.family as family_model


# Structural controls are inclusive ranges; generations is a tuple of choices.
# Tune population together with total/founding couples, not population alone.
DIFFICULTY_SETTINGS = {
	'easy': dict(generations=(3,), people=(12, 15), seed_couples=(1, 1),
		couples=(3, 4), children=(1, 3), root_children=(2, 4)),
	'medium': dict(generations=(4, 5), people=(16, 22), seed_couples=(1, 2),
		couples=(4, 6), children=(1, 4), root_children=(2, 5)),
	'rigorous': dict(generations=(5,), people=(23, 26), seed_couples=(2, 3),
		couples=(6, 8), children=(1, 4), root_children=(2, 4)),
	'bonus': dict(generations=(6, 7), people=(60, 100), seed_couples=(3, 4),
		couples=(18, 26), children=(1, 5), root_children=(2, 5)),
}
MATCHING_SETTINGS = {
	'easy': dict(generations=(3,), people=(10, 11), seed_couples=(1, 1),
		couples=(2, 3), children=(1, 3), root_children=(2, 5)),
	'medium': dict(generations=(3,), people=(12, 15), seed_couples=(1, 2),
		couples=(3, 4), children=(1, 4), root_children=(2, 6)),
	'rigorous': dict(generations=(3, 4), people=(16, 18), seed_couples=(2, 3),
		couples=(4, 5), children=(1, 3), root_children=(2, 4)),
}

# Measured topology target for fresh bonus identification cases. Cached records
# and all other levels and question formats keep their current eligibility.
TERMINAL_FRONTIER_TRIAL_COUNTS = {
	'bonus': (9, 10),
}


#============================================
def difficulty_settings(level: str, matching: bool = False) -> dict:
	"""Return a copy of the constructor controls for a workload preset."""
	presets = MATCHING_SETTINGS if matching else DIFFICULTY_SETTINGS
	if level not in presets:
		raise ValueError(f'Unknown difficulty: {level}')
	result = dict(presets[level])
	return result


#============================================
def frontier_trial_counts(level: str, question_format: str) -> tuple[int, ...]:
	"""Return measured frontier sizes for bonus identification construction."""
	if question_format not in ('identify', 'select', 'match'):
		raise ValueError(f'Unknown question format: {question_format}')
	if question_format != 'identify':
		return ()
	result = TERMINAL_FRONTIER_TRIAL_COUNTS.get(level, ())
	return result


#============================================
def difficulty_limits(level: str, matching: bool = False) -> tuple[tuple[int, ...], int, int]:
	"""Return depth choices and size bounds from the shared constructor settings."""
	settings = difficulty_settings(level, matching)
	result = (settings['generations'], *settings['people'])
	return result


#============================================
def fits_difficulty(family: family_model.Family, level: str, matching: bool = False) -> bool:
	"""Filter accepted families using all structural controls in the generation preset."""
	settings = difficulty_settings(level, matching)
	ranks = family.generations()
	seeds = [u for u in family.unions if ranks[u.father] == ranks[u.mother] == 0]
	counts = dict(people=len(family.people), seed_couples=len(seeds), couples=len(family.unions))
	if max(ranks.values()) + 1 not in settings['generations']:
		return False
	if any(not settings[key][0] <= count <= settings[key][1] for key, count in counts.items()):
		return False
	for union in family.unions:
		low, high = settings['root_children'] if union in seeds else settings['children']
		if not low <= len(union.children) <= high:
			return False
	return True
