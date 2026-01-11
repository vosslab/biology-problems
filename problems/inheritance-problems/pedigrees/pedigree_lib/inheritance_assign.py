#!/usr/bin/env python3

# Standard Library
import random

# Local repo modules
from graph_parse import PedigreeGraph


#===============================
def _assign_autosomal_dominant(graph: PedigreeGraph, rng: random.Random) -> None:
	founders = [ind for ind in graph.individuals.values() if ind.generation == 1]
	affected_founder = rng.choice(founders)
	affected_founder.phenotype = 'affected'
	for couple in graph.couples:
		parent_a = graph.individuals[couple.partner_a]
		parent_b = graph.individuals[couple.partner_b]
		for child_id in couple.children:
			child = graph.individuals[child_id]
			inherit_a = parent_a.phenotype == 'affected' and rng.random() < 0.5
			inherit_b = parent_b.phenotype == 'affected' and rng.random() < 0.5
			child.phenotype = 'affected' if (inherit_a or inherit_b) else 'unaffected'


#===============================
def _assign_autosomal_recessive(graph: PedigreeGraph, rng: random.Random, show_carriers: bool) -> None:
	"""
	Assign phenotypes for autosomal recessive inheritance.

	Both founders are made carriers to ensure affected offspring are possible.
	When both parents are carriers, children have 25% affected, 50% carrier, 25% normal.
	Carrier status is tracked internally and converted to display format at the end.
	"""
	# Track carrier status internally (separate from phenotype)
	is_carrier: dict[str, bool] = {}

	# Make both founders carriers to guarantee affected children are possible
	for ind in graph.individuals.values():
		if ind.generation == 1:
			is_carrier[ind.id] = True
			ind.phenotype = 'unaffected'

	# Assign marry-in spouses as carriers with high probability
	for ind in graph.individuals.values():
		if ind.generation > 1 and ind.father_id is None and ind.mother_id is None:
			# This is a marry-in spouse
			is_carrier[ind.id] = rng.random() < 0.7
			ind.phenotype = 'unaffected'

	# Process couples in generation order
	for couple in sorted(graph.couples, key=lambda c: c.generation):
		parent_a = graph.individuals[couple.partner_a]
		parent_b = graph.individuals[couple.partner_b]
		parent_a_carrier = is_carrier.get(parent_a.id, False) or parent_a.phenotype == 'affected'
		parent_b_carrier = is_carrier.get(parent_b.id, False) or parent_b.phenotype == 'affected'

		for child_id in couple.children:
			child = graph.individuals[child_id]
			if parent_a_carrier and parent_b_carrier:
				# Both carriers: 25% affected, 50% carrier, 25% normal
				roll = rng.random()
				if roll < 0.25:
					child.phenotype = 'affected'
					is_carrier[child.id] = False
				elif roll < 0.75:
					is_carrier[child.id] = True
					child.phenotype = 'unaffected'
				else:
					is_carrier[child.id] = False
					child.phenotype = 'unaffected'
			elif parent_a_carrier or parent_b_carrier:
				# One carrier: 50% carrier, 50% normal
				is_carrier[child.id] = rng.random() < 0.5
				child.phenotype = 'unaffected'
			else:
				is_carrier[child.id] = False
				child.phenotype = 'unaffected'

	# Convert carrier status to display format if show_carriers is True
	if show_carriers:
		for ind_id, carrier in is_carrier.items():
			ind = graph.individuals[ind_id]
			if carrier and ind.phenotype == 'unaffected':
				ind.phenotype = 'carrier'


#===============================
def _assign_x_linked_recessive(graph: PedigreeGraph, rng: random.Random, show_carriers: bool) -> None:
	"""
	Assign phenotypes for X-linked recessive inheritance.

	Carrier females pass to 50% of sons (affected) and 50% of daughters (carrier).
	Affected males pass carrier status to all daughters.
	Carrier status is tracked internally and converted to display format at the end.
	"""
	# Track carrier status internally for females
	is_carrier: dict[str, bool] = {}

	# Initialize founders - make founder female a carrier to ensure affected offspring
	for ind in graph.individuals.values():
		if ind.generation == 1:
			if ind.sex == 'female':
				# High chance of being carrier to produce affected sons
				is_carrier[ind.id] = True
				ind.phenotype = 'unaffected'
			elif ind.sex == 'male':
				# Small chance founder male is affected
				if rng.random() < 0.15:
					ind.phenotype = 'affected'
				else:
					ind.phenotype = 'unaffected'

	# Assign marry-in spouses
	for ind in graph.individuals.values():
		if ind.generation > 1 and ind.father_id is None and ind.mother_id is None:
			if ind.sex == 'female':
				is_carrier[ind.id] = rng.random() < 0.3
			ind.phenotype = 'unaffected'

	# Process couples in generation order
	for couple in sorted(graph.couples, key=lambda c: c.generation):
		father = graph.individuals[couple.partner_a]
		mother = graph.individuals[couple.partner_b]
		mother_carrier = is_carrier.get(mother.id, False) or mother.phenotype == 'affected'

		for child_id in couple.children:
			child = graph.individuals[child_id]
			if child.sex == 'male':
				# Sons: 50% affected if mother is carrier
				if mother_carrier and rng.random() < 0.5:
					child.phenotype = 'affected'
				else:
					child.phenotype = 'unaffected'
			else:
				# Daughters
				if father.phenotype == 'affected':
					# Father affected -> daughter is at least carrier
					if mother_carrier and rng.random() < 0.5:
						child.phenotype = 'affected'
						is_carrier[child.id] = False
					else:
						is_carrier[child.id] = True
						child.phenotype = 'unaffected'
				elif mother_carrier and rng.random() < 0.5:
					# Mother carrier -> 50% daughter is carrier
					is_carrier[child.id] = True
					child.phenotype = 'unaffected'
				else:
					is_carrier[child.id] = False
					child.phenotype = 'unaffected'

	# Convert carrier status to display format if show_carriers is True
	if show_carriers:
		for ind_id, carrier in is_carrier.items():
			ind = graph.individuals[ind_id]
			if carrier and ind.phenotype == 'unaffected':
				ind.phenotype = 'carrier'


#===============================
def _assign_y_linked(graph: PedigreeGraph, rng: random.Random) -> None:
	founder_males = [ind for ind in graph.individuals.values() if ind.generation == 1 and ind.sex == 'male']
	if founder_males:
		rng.choice(founder_males).phenotype = 'affected'
	for couple in graph.couples:
		father = graph.individuals[couple.partner_a]
		for child_id in couple.children:
			child = graph.individuals[child_id]
			if child.sex == 'male' and father.phenotype == 'affected':
				child.phenotype = 'affected'


#===============================
def _assign_x_linked_dominant(graph: PedigreeGraph, rng: random.Random) -> None:
	"""
	Assign phenotypes for X-linked dominant inheritance.

	X-linked dominant: affected males pass to all daughters, affected mothers
	pass to ~50% of children. No father-to-son transmission.
	"""
	# Start with one affected founder (prefer female for more transmission)
	founders = [ind for ind in graph.individuals.values() if ind.generation == 1]
	founder_females = [ind for ind in founders if ind.sex == 'female']
	founder_males = [ind for ind in founders if ind.sex == 'male']

	# Prefer female founder as affected (more offspring get trait)
	if founder_females and rng.random() < 0.7:
		affected_founder = rng.choice(founder_females)
	elif founder_males:
		affected_founder = rng.choice(founder_males)
	else:
		affected_founder = rng.choice(founders)
	affected_founder.phenotype = 'affected'

	# Process couples in generation order
	for couple in sorted(graph.couples, key=lambda c: c.generation):
		father = graph.individuals[couple.partner_a]
		mother = graph.individuals[couple.partner_b]
		for child_id in couple.children:
			child = graph.individuals[child_id]
			# Father passes X to daughters only
			if father.phenotype == 'affected' and child.sex == 'female':
				child.phenotype = 'affected'
			# Mother passes X to all children with 50% chance
			elif mother.phenotype == 'affected' and rng.random() < 0.5:
				child.phenotype = 'affected'
			else:
				child.phenotype = 'unaffected'


#===============================
def assign_phenotypes(graph: PedigreeGraph, mode: str, rng: random.Random, show_carriers: bool) -> None:
	mode_value = mode.strip().lower()
	if mode_value in ('autosomal dominant', 'ad'):
		_assign_autosomal_dominant(graph, rng)
	elif mode_value in ('autosomal recessive', 'ar'):
		_assign_autosomal_recessive(graph, rng, show_carriers)
	elif mode_value in ('x-linked dominant', 'xd'):
		_assign_x_linked_dominant(graph, rng)
	elif mode_value in ('x-linked recessive', 'xr'):
		_assign_x_linked_recessive(graph, rng, show_carriers)
	elif mode_value in ('y-linked', 'yl'):
		_assign_y_linked(graph, rng)


#===============================
if __name__ == '__main__':
	default_rng = random.Random(7)
	print(default_rng.random())

## THE END
