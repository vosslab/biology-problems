"""Build valid pedigree pools once, then consume ranked, comparable scenarios."""

import collections
import dataclasses
import random

import pedigree_lib.difficulty as difficulty
import pedigree_lib.inheritance as inheritance
import pedigree_lib.questions as questions
import pedigree_lib.polishing as polishing
import pedigree_lib.ranking as ranking
import pedigree_lib.sources as sources


#============================================
def generate_candidate(mode: str, rng: random.Random, level: str,
		matching: bool = False) -> questions.AcceptedCase:
	"""Resample preset construction choices on rejection, retaining every acceptance gate."""
	settings = difficulty.difficulty_settings(level, matching)
	construction = [(depth, seeds) for depth in settings['generations']
		for seeds in range(settings['seed_couples'][0], settings['seed_couples'][1] + 1)
		if sources.minimum_couples(depth, seeds) <= settings['couples'][1]]
	rejections = collections.Counter()
	for attempt in range(1, 5001):
		depth, seeds = rng.choice(construction)
		case = sources.simulate_case(mode, rng,
			min_people=settings['people'][0], max_people=settings['people'][1],
			generations=depth, seed_couples=seeds, couples=settings['couples'],
			children=settings['children'], root_children=settings['root_children'])
		accepted, reasons = questions.evaluate(case, mirror=rng.choice((False, True)))
		if accepted is not None:
			if accepted.assessment.answer == mode:
				return dataclasses.replace(accepted, attempts=attempt, rejections=dict(rejections))
			reasons = ('Teaching evidence favors another mode',)
		rejections.update(reasons)
	raise questions.GenerationFailure(f'No suitable {mode} case in {level} after 5000 attempts: '
		f'{dict(rejections)}')


#============================================
def generate_pool(rng: random.Random, level: str, matching: bool = False,
		count: int = 5000) -> list[questions.AcceptedCase]:
	"""Generate accepted candidates, polish within the preset, then recheck difficulty."""
	pool = []
	for _ in range(count):
		case = generate_candidate(rng.choice(inheritance.MODES), rng, level, matching)
		pool.append(polishing.polish(case, rng, level, matching))
	# Preset filtering stays independent of aesthetics and uses the existing authority.
	result = [case for case in pool if difficulty.fits_difficulty(case.case.family, level, matching)]
	return result


#============================================
def comparable_key(case: questions.AcceptedCase) -> tuple[int, int]:
	"""Keep depth and founding-family count equal within multi-diagram questions."""
	ranks = case.case.family.generations()
	founders = sum(ranks[u.father] == ranks[u.mother] == 0 for u in case.case.family.unions)
	result = (max(ranks.values()) + 1, founders)
	return result


#============================================
def assemble(pool: list[questions.AcceptedCase], question_format: str) -> list[tuple]:
	"""Consume eligible entries in supplied order, without reusing a pool entry.

	Selection and matching each require all five modes with comparable depth/founders.
	Incomplete groups remain unused rather than relaxing those requirements.
	"""
	if question_format == 'identify':
		return [(case,) for case in pool]
	if question_format not in ('select', 'match'):
		raise ValueError(f'Unknown question format: {question_format}')
	groups = collections.defaultdict(lambda: collections.defaultdict(collections.deque))
	for index, case in enumerate(pool):
		groups[comparable_key(case)][case.assessment.answer].append(index)
	used = set()
	result = []
	for index, case in enumerate(pool):
		if index in used:
			continue
		group = groups[comparable_key(case)]
		if not all(group[mode] for mode in inheritance.MODES):
			continue
		indices = [group[mode].popleft() for mode in inheritance.MODES]
		used.update(indices)
		result.append(tuple(pool[i] for i in indices))
	return result


#============================================
def build(rng: random.Random, level: str, question_format: str,
		pool_size: int = 5000) -> list[tuple]:
	"""Build once for bptools; removing the sort restores generation order."""
	if question_format not in ('identify', 'select', 'match'):
		raise ValueError(f'Unknown question format: {question_format}')
	if level == 'bonus' and question_format != 'identify':
		raise ValueError('--bonus requires write_pedigree_to_pattern.py (one pedigree per question)')
	pool = generate_pool(rng, level, question_format == 'match', pool_size)
	pool.sort(key=ranking.score, reverse=True)
	result = assemble(pool, question_format)
	if not result:
		raise questions.GenerationFailure(f'No complete {question_format} scenarios fit {level}')
	return result
