"""Bounded terminal-child additions, retaining all existing acceptance gates."""

import dataclasses
import random

import pedigree_lib.difficulty as difficulty
import pedigree_lib.family as family_model
import pedigree_lib.generation_features as generation_features
import pedigree_lib.inheritance as inheritance
import pedigree_lib.questions as questions


#============================================
def polish(original: questions.AcceptedCase, rng: random.Random, level: str,
		matching: bool = False) -> questions.AcceptedCase:
	"""Try at most two additions; return the original object if none qualifies.

	Existing people, genotypes, observations, and parentage remain unchanged.
	Every addition must reduce shrink, preserve progression and width, and keep
	the same teaching evidence, compatible modes, answer, and difficulty band.
	"""
	current = original
	for _ in range(2):
		case = current.case
		rows = generation_features.counts(case.family)
		before_shrink = generation_features.shrink(rows)
		if before_shrink == 0 or len(case.family.people) >= difficulty.difficulty_settings(level, matching)['people'][1]:
			break
		ranks = case.family.generations()
		options = []
		for index, union in enumerate(case.family.unions):
			row = ranks[union.father] + 1
			if row < 2 or rows[row] >= rows[row - 1]:
				continue
			for sex in ('male', 'female'):
				for genotype in inheritance.transmissions(current.assessment.answer,
						case.genotypes[union.father], case.genotypes[union.mother], sex):
					options.append((index, sex, genotype))
		rng.shuffle(options)
		# Layout places fathers left of mothers unless reflected; retain that orientation.
		x = {symbol.person: symbol.x for symbol in current.diagram.symbols}
		first = case.family.unions[0]
		mirror = x[first.father] > x[first.mother]
		pid = f'p{len(case.family.people) + 1}'
		while pid in case.family.members():
			pid += '_'
		for index, sex, genotype in options:
			unions = list(case.family.unions)
			unions[index] = dataclasses.replace(unions[index], children=unions[index].children + (pid,))
			family = family_model.Family(case.family.people + (family_model.Person(pid, sex),), tuple(unions))
			if not difficulty.fits_difficulty(family, level, matching):
				continue
			observations = dict(case.observations)
			observations[pid] = family_model.Observation(inheritance.phenotype(current.assessment.answer, genotype))
			genotypes = dict(case.genotypes)
			genotypes[pid] = genotype
			candidate = dataclasses.replace(case, family=family, observations=observations, genotypes=genotypes)
			accepted, reasons = questions.evaluate(candidate, mirror=mirror)
			if accepted is None:
				continue
			old, new = original.assessment, accepted.assessment
			if new.answer != old.answer or new.evidence != old.evidence or any(
					new.compatibility[mode].compatible != old.compatibility[mode].compatible for mode in inheritance.MODES):
				continue
			after = generation_features.counts(family)
			if (accepted.diagram.width > current.diagram.width
					or generation_features.shrink(after) >= before_shrink
					or generation_features.progression(after) < generation_features.progression(rows)):
				continue
			current = dataclasses.replace(accepted, attempts=original.attempts, rejections=original.rejections)
			break
		else:
			break
	return current
