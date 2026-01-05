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
	for ind in graph.individuals.values():
		if ind.generation == 1:
			if rng.random() < 0.6:
				ind.phenotype = 'carrier' if show_carriers else 'unaffected'
			else:
				ind.phenotype = 'unaffected'
	for couple in graph.couples:
		parent_a = graph.individuals[couple.partner_a]
		parent_b = graph.individuals[couple.partner_b]
		for child_id in couple.children:
			child = graph.individuals[child_id]
			parent_a_carrier = parent_a.phenotype in ('carrier', 'affected')
			parent_b_carrier = parent_b.phenotype in ('carrier', 'affected')
			if parent_a_carrier and parent_b_carrier and rng.random() < 0.25:
				child.phenotype = 'affected'
			elif parent_a_carrier or parent_b_carrier:
				child.phenotype = 'carrier' if show_carriers else 'unaffected'
			else:
				child.phenotype = 'unaffected'


#===============================
def _assign_x_linked_recessive(graph: PedigreeGraph, rng: random.Random, show_carriers: bool) -> None:
	for ind in graph.individuals.values():
		if ind.generation == 1:
			if ind.sex == 'female' and rng.random() < 0.4:
				ind.phenotype = 'carrier' if show_carriers else 'unaffected'
			elif ind.sex == 'male' and rng.random() < 0.2:
				ind.phenotype = 'affected'
	for couple in graph.couples:
		mother = graph.individuals[couple.partner_b]
		father = graph.individuals[couple.partner_a]
		for child_id in couple.children:
			child = graph.individuals[child_id]
			if child.sex == 'male':
				if mother.phenotype in ('carrier', 'affected') and rng.random() < 0.5:
					child.phenotype = 'affected'
				else:
					child.phenotype = 'unaffected'
			else:
				if father.phenotype == 'affected' and mother.phenotype in ('carrier', 'affected'):
					child.phenotype = 'affected' if rng.random() < 0.5 else ('carrier' if show_carriers else 'unaffected')
				elif mother.phenotype in ('carrier', 'affected') and rng.random() < 0.5:
					child.phenotype = 'carrier' if show_carriers else 'unaffected'
				else:
					child.phenotype = 'unaffected'


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
def assign_phenotypes(graph: PedigreeGraph, mode: str, rng: random.Random, show_carriers: bool) -> None:
	mode_value = mode.strip().lower()
	if mode_value in ('autosomal dominant', 'ad'):
		_assign_autosomal_dominant(graph, rng)
	elif mode_value in ('autosomal recessive', 'ar'):
		_assign_autosomal_recessive(graph, rng, show_carriers)
	elif mode_value in ('x-linked recessive', 'xr'):
		_assign_x_linked_recessive(graph, rng, show_carriers)
	elif mode_value in ('y-linked', 'yl'):
		_assign_y_linked(graph, rng)


#===============================
if __name__ == '__main__':
	default_rng = random.Random(7)
	print(default_rng.random())

## THE END
