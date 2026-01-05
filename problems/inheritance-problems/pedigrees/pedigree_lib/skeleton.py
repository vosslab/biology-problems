#!/usr/bin/env python3

# Standard Library
import random

# Local repo modules
from graph_parse import Couple, Individual, PedigreeGraph, _new_id


#===============================
def _make_founder_couples(starting_couples: int, rng: random.Random) -> tuple[dict[str, Individual], list[Couple]]:
	individuals: dict[str, Individual] = {}
	couples: list[Couple] = []
	person_counter = 1
	couple_counter = 1
	for _ in range(starting_couples):
		male_id = _new_id('M', person_counter)
		person_counter += 1
		female_id = _new_id('F', person_counter)
		person_counter += 1
		individuals[male_id] = Individual(
			id=male_id,
			sex='male',
			phenotype='unaffected',
			generation=1,
		)
		individuals[female_id] = Individual(
			id=female_id,
			sex='female',
			phenotype='unaffected',
			generation=1,
		)
		couple_id = _new_id('C', couple_counter)
		couple_counter += 1
		couples.append(Couple(
			id=couple_id,
			partner_a=male_id,
			partner_b=female_id,
			generation=1,
			children=[],
		))
	return individuals, couples


#===============================
def _add_children(
	individuals: dict[str, Individual],
	couples: list[Couple],
	generation: int,
	person_counter: int,
	rng: random.Random,
	min_children: int,
	max_children: int,
) -> tuple[list[str], int]:
	children_ids: list[str] = []
	for couple in [c for c in couples if c.generation == generation]:
		num_children = rng.randint(min_children, max_children)
		for _ in range(num_children):
			sex = rng.choice(['male', 'female'])
			child_id = _new_id('P', person_counter)
			person_counter += 1
			individuals[child_id] = Individual(
				id=child_id,
				sex=sex,
				phenotype='unaffected',
				generation=generation + 1,
				father_id=couple.partner_a,
				mother_id=couple.partner_b,
			)
			couple.children.append(child_id)
			children_ids.append(child_id)
	return children_ids, person_counter


#===============================
def _pair_children(
	individuals: dict[str, Individual],
	children_ids: list[str],
	generation: int,
	person_counter: int,
	couple_counter: int,
	rng: random.Random,
	marry_in_rate: float,
) -> tuple[list[Couple], int, int]:
	new_couples: list[Couple] = []
	for child_id in children_ids:
		if rng.random() > marry_in_rate:
			continue
		child = individuals[child_id]
		spouse_sex = 'female' if child.sex == 'male' else 'male'
		spouse_id = _new_id('S', person_counter)
		person_counter += 1
		individuals[spouse_id] = Individual(
			id=spouse_id,
			sex=spouse_sex,
			phenotype='unaffected',
			generation=generation,
		)
		couple_id = _new_id('C', couple_counter)
		couple_counter += 1
		if child.sex == 'male':
			partner_a = child_id
			partner_b = spouse_id
		else:
			partner_a = spouse_id
			partner_b = child_id
		new_couples.append(Couple(
			id=couple_id,
			partner_a=partner_a,
			partner_b=partner_b,
			generation=generation,
			children=[],
		))
	return new_couples, person_counter, couple_counter


#===============================
def generate_skeleton_graph(
	generations: int = 4,
	starting_couples: int = 1,
	rng: random.Random | None = None,
	min_children: int = 2,
	max_children: int = 4,
	marry_in_rate: float = 0.7,
) -> PedigreeGraph:
	"""
	Generate a pedigree graph skeleton with randomized structure.
	"""
	if rng is None:
		rng = random.Random()

	individuals, couples = _make_founder_couples(starting_couples, rng)
	person_counter = len(individuals) + 1
	couple_counter = len(couples) + 1
	for gen in range(1, generations):
		children_ids, person_counter = _add_children(
			individuals,
			couples,
			gen,
			person_counter,
			rng,
			min_children,
			max_children,
		)
		if gen + 1 > generations:
			continue
		new_couples, person_counter, couple_counter = _pair_children(
			individuals,
			children_ids,
			gen + 1,
			person_counter,
			couple_counter,
			rng,
			marry_in_rate,
		)
		couples.extend(new_couples)

	graph = PedigreeGraph(
		individuals=individuals,
		couples=couples,
		generations=generations,
		starting_couples=starting_couples,
	)
	return graph


#===============================
def generate_basic_three_gen_graph(
	rng: random.Random | None = None,
	min_children: int = 2,
	max_children: int = 4,
	min_grandchildren: int = 1,
	max_grandchildren: int = 3,
	couples_to_pair: int = 2,
) -> PedigreeGraph:
	"""
	Generate a simple three-generation pedigree for layout smoke tests.
	"""
	if rng is None:
		rng = random.Random()

	individuals, couples = _make_founder_couples(1, rng)
	person_counter = len(individuals) + 1
	couple_counter = len(couples) + 1

	children_ids, person_counter = _add_children(
		individuals,
		couples,
		1,
		person_counter,
		rng,
		min_children,
		max_children,
	)

	children_sorted = sorted(children_ids)
	pair_count = max(1, min(couples_to_pair, len(children_sorted)))
	selected_children = children_sorted[:pair_count]

	new_couples: list[Couple] = []
	for child_id in selected_children:
		child = individuals[child_id]
		spouse_sex = 'female' if child.sex == 'male' else 'male'
		spouse_id = _new_id('S', person_counter)
		person_counter += 1
		individuals[spouse_id] = Individual(
			id=spouse_id,
			sex=spouse_sex,
			phenotype='unaffected',
			generation=2,
		)
		couple_id = _new_id('C', couple_counter)
		couple_counter += 1
		if child.sex == 'male':
			partner_a = child_id
			partner_b = spouse_id
		else:
			partner_a = spouse_id
			partner_b = child_id
		new_couples.append(Couple(
			id=couple_id,
			partner_a=partner_a,
			partner_b=partner_b,
			generation=2,
			children=[],
		))
	couples.extend(new_couples)

	_add_children(
		individuals,
		couples,
		2,
		person_counter,
		rng,
		min_grandchildren,
		max_grandchildren,
	)

	graph = PedigreeGraph(
		individuals=individuals,
		couples=couples,
		generations=3,
		starting_couples=1,
	)
	return graph


#===============================
if __name__ == '__main__':
	default_rng = random.Random(7)
	graph = generate_skeleton_graph(rng=default_rng)
	print(len(graph.individuals), len(graph.couples))

## THE END
