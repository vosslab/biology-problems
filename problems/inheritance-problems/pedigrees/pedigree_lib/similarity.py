"""Graph-based pedigree similarity, independent of labels and drawing coordinates."""

# Standard Library
import collections
import dataclasses
import itertools

# PIP3 modules
import networkx

# local repo modules
import pedigree_lib.family as family_model
import pedigree_lib.sources as sources
import pedigree_lib.graphs as graphs


#============================================
@dataclasses.dataclass(frozen=True)
class Similarity:
	structure: float
	visible: float
	same_structure: bool
	same_visible: bool


#============================================
@dataclasses.dataclass(frozen=True)
class Complexity:
	people: int
	unions: int
	generations: int
	founder_couples: int
	joining_unions: int
	max_sibship: int
	components: int
	cycle_rank: int
	diameter: int

	def sort_key(self) -> tuple[int, ...]:
		"""Order by depth, unions, joined branches, cycles, then people; not exam difficulty."""
		return (self.generations, self.unions, self.joining_unions, self.cycle_rank, self.people)


#============================================
def complexity(family: family_model.Family) -> Complexity:
	"""Measure structure, including multi-founder families and shared ancestry.

	Cycle rank is E - V + C on the incidence graph, not a count of biological
	ancestry cycles. Diameter is the largest component's longest shortest path,
	measured in person-union edges. Isolated people have diameter zero.
	"""
	graph = graphs.to_networkx(family)
	components = list(networkx.connected_components(graph))
	parents = family.parentage()
	ranks = family.generations()
	result = Complexity(people=len(family.people), unions=len(family.unions),
		generations=max(ranks.values()) + 1,
		founder_couples=sum(u.father not in parents and u.mother not in parents for u in family.unions),
		joining_unions=sum(u.father in parents and u.mother in parents for u in family.unions),
		max_sibship=max((len(u.children) for u in family.unions), default=0),
		components=len(components),
		cycle_rank=graph.number_of_edges() - graph.number_of_nodes() + len(components),
		diameter=max(networkx.diameter(graph.subgraph(nodes)) for nodes in components))
	return result


#============================================
def _features(graph: networkx.Graph) -> collections.Counter:
	"""Count neighborhood labels at radii zero through three incidence edges."""
	hashes = networkx.weisfeiler_lehman_subgraph_hashes(graph,
		node_attr='label', edge_attr='role', iterations=3, include_initial_labels=True)
	result = collections.Counter((radius, label)
		for labels in hashes.values() for radius, label in enumerate(labels))
	return result


#============================================
def _compare_graphs(left: tuple, right: tuple) -> tuple[float, bool]:
	left_graph, a = left
	right_graph, b = right
	# Multiset Jaccard: shared neighborhood occurrences divided by all occurrences.
	score = sum((a & b).values()) / sum((a | b).values())
	identical = False
	if score == 1.0:
		identical = networkx.is_isomorphic(left_graph, right_graph,
			node_match=networkx.algorithms.isomorphism.categorical_node_match('label', None),
			edge_match=networkx.algorithms.isomorphism.categorical_edge_match('role', None))
	return score, identical


#============================================
def compare(left: sources.Case, right: sources.Case) -> Similarity:
	"""Compare topology and visible patterns on a zero-to-one similarity scale.

	Topology ignores sex and phenotype. Visible comparison includes sex, affected
	status, and disclosed carrier status; neither comparison reads hidden genotypes.
	IDs, labels, ordering, reflection, and coordinates have no influence. Scores are
	approximate neighborhood overlap, not inheritance confidence or exact edit distance.
	Only the same_* flags establish graph isomorphism; a score of one alone does not.

	Raises:
		ValueError: Invalid family or incomplete/invalid observations.
	"""
	result = _compare_prepared(_prepare(left), _prepare(right))
	return result


#============================================
def _prepare(case: sources.Case) -> tuple:
	"""Snapshot graphs and neighborhood counts once for reuse within an operation."""
	structure = graphs.to_networkx(case.family)
	visible = graphs.to_networkx(case.family, case.observations)
	result = ((structure, _features(structure)), (visible, _features(visible)))
	return result


#============================================
def _compare_prepared(left: tuple, right: tuple) -> Similarity:
	structure, same_structure = _compare_graphs(left[0], right[0])
	visible, same_visible = _compare_graphs(left[1], right[1])
	result = Similarity(structure, visible, same_structure, same_visible)
	return result


#============================================
def pairwise(cases: list[sources.Case]) -> list[dict]:
	"""Compare each pair once, reusing graphs/features within this call only.

	Indices are one-based. Subsequent calls rebuild snapshots so observation
	edits cannot leave stale visible labels. No cache survives the operation.
	"""
	result = []
	if len(cases) < 2:
		return result
	prepared = [_prepare(case) for case in cases]
	for (i, left), (j, right) in itertools.combinations(enumerate(prepared, 1), 2):
		result.append(dict(left=i, right=j, **dataclasses.asdict(_compare_prepared(left, right))))
	return result
