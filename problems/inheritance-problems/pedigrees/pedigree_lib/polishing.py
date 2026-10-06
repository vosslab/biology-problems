"""Bounded terminal-child additions, retaining all existing acceptance gates."""

import dataclasses
import random

import pedigree_lib.difficulty as difficulty
import pedigree_lib.family as family_model
import pedigree_lib.generation_features as generation_features
import pedigree_lib.inheritance as inheritance
import pedigree_lib.questions as questions
import pedigree_lib.ranking as ranking
import pedigree_lib.layout as layout


#============================================
def polish(original: questions.AcceptedCase, rng: random.Random, level: str,
		matching: bool = False) -> questions.AcceptedCase:
	"""Choose up to two structural improvements, then sample each child once.

	Existing people, genotypes, observations, and parentage remain unchanged.
	Every addition must reduce shrink, preserve progression and width, and keep
	the same teaching evidence, compatible modes, answer, and difficulty band.
	Choose placement before sampling genotype; never optimize affected outcomes.
	"""
	current = original
	for _ in range(2):
		case = current.case
		rows = generation_features.counts(case.family)
		before_shrink = generation_features.shrink(rows)
		if before_shrink == 0:
			break
		settings = difficulty.difficulty_settings(level, matching)
		if len(case.family.people) >= settings['people'][1]:
			break
		before_progression = generation_features.progression(rows)
		ranks = case.family.generations()
		options = [index for index, union in enumerate(case.family.unions)
			if ranks[union.father] + 1 >= 2
			and rows[ranks[union.father] + 1] < rows[ranks[union.father]]]
		rng.shuffle(options)
		sex = rng.choice(('male', 'female'))
		# Layout places fathers left of mothers unless reflected; retain that orientation.
		x = {symbol.person: symbol.x for symbol in current.diagram.symbols}
		first = case.family.unions[0]
		mirror = x[first.father] > x[first.mother]
		pid = f'p{len(case.family.people) + 1}'
		while pid in case.family.members():
			pid += '_'
		best = None
		best_score = ranking.structure_score(case.family, current.diagram)
		generation_eligibility = {}
		for index in options:
			union = case.family.unions[index]
			child_generation = ranks[union.father] + 1
			if len(union.children) >= settings['children'][1]:
				continue
			if child_generation not in generation_eligibility:
				proposed_rows = rows.copy()
				proposed_rows[child_generation] += 1
				generation_eligibility[child_generation] = (
					generation_features.shrink(proposed_rows) < before_shrink
					and generation_features.progression(proposed_rows) >= before_progression)
			if not generation_eligibility[child_generation]:
				continue
			unions = list(case.family.unions)
			unions[index] = dataclasses.replace(union, children=union.children + (pid,))
			family = family_model.Family(case.family.people + (family_model.Person(pid, sex),), tuple(unions))
			if not difficulty.fits_difficulty(family, level, matching):
				continue
			diagram = layout.lay_out(family, mirror=mirror)
			if layout.layout_errors(diagram) or diagram.width > current.diagram.width:
				continue
			candidate_score = ranking.structure_score(family, diagram)
			if candidate_score > best_score:
				best = (family, index)
				best_score = candidate_score
		if best is None:
			break
		family, index = best
		union = case.family.unions[index]
		# Repeated gamete combinations retain their Mendelian sampling weight.
		genotype = rng.choice(inheritance.transmissions(current.assessment.answer,
			case.genotypes[union.father], case.genotypes[union.mother], sex))
		observations = dict(case.observations)
		observations[pid] = family_model.Observation(inheritance.phenotype(current.assessment.answer, genotype))
		genotypes = dict(case.genotypes)
		genotypes[pid] = genotype
		candidate = dataclasses.replace(case, family=family, observations=observations, genotypes=genotypes)
		accepted, reasons = questions.evaluate(candidate, mirror=mirror)
		# A failed biological/teaching check stops polishing, without rerolling the child.
		if accepted is None:
			break
		old, new = original.assessment, accepted.assessment
		# Each mode has one teaching profile; its trailing diagnostic counts may change.
		if new.answer != old.answer or any(
				bool(new.evidence[mode]) != bool(old.evidence[mode])
				or new.compatibility[mode].compatible != old.compatibility[mode].compatible
				for mode in inheritance.MODES):
			break
		current = dataclasses.replace(accepted, attempts=original.attempts, rejections=original.rejections)
	return current
