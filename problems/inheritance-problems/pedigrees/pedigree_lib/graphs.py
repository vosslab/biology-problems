"""On-demand NetworkX snapshots of authoritative pedigree relationships."""

# PIP3 modules
import networkx

# local repo modules
import pedigree_lib.family as family_model


#============================================
def to_networkx(family: family_model.Family,
		observations: dict[str, family_model.Observation] | None = None) -> networkx.Graph:
	"""Derive an independent graph snapshot with person/union nodes and role edges.

	Without observations, labels encode topology only. With observations, person
	labels include sex and visible status; hidden genotypes are never read.
	Callers may mutate the returned graph without changing the source family or
	any other snapshot. The family remains the only relationship authority.
	"""
	if observations is None:
		family.generations()
	else:
		family_model.validate_observations(family, observations)
	graph = networkx.Graph()
	for person in family.people:
		label = 'person'
		if observations is not None:
			obs = observations[person.id]
			label = repr(('person', person.sex, obs.affected, obs.carrier))
		graph.add_node(('person', person.id), label=label)
	for index, union in enumerate(family.unions):
		node = ('union', index)
		graph.add_node(node, label='union')
		for pid in (union.father, union.mother):
			graph.add_edge(node, ('person', pid), role='parent')
		for pid in union.children:
			graph.add_edge(node, ('person', pid), role='child')
	return graph


#============================================
def components(family: family_model.Family) -> list[set[str]]:
	"""Return connected person-ID sets, ordered by their first person in the family.

	Union nodes participate in connectivity but are omitted from the returned sets.
	Isolated people form single-person components.
	"""
	graph = to_networkx(family)
	result = [{pid for kind, pid in nodes if kind == 'person'}
		for nodes in networkx.connected_components(graph)]
	return result
