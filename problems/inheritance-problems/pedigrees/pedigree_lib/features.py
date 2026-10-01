"""Topology measurements only: no phenotype, teaching policy, or drawing inputs."""

import collections
import dataclasses
import statistics

import networkx

import pedigree_lib.family as family_model
import pedigree_lib.graphs as graphs
import pedigree_lib.similarity as similarity


#============================================
def measure(family: family_model.Family) -> dict:
	"""Measure degree distribution, branching, and balance on authoritative parentage.

	A continuing child has offspring of their own. A branch point has at least
	two continuing children. Balance averages smallest/largest descendant counts
	at those branch points (zero when none exist). Descendants are distinct people,
	so shared ancestry does not double-count a person within a branch.
	"""
	graph = graphs.to_networkx(family)
	ancestry = networkx.DiGraph()
	ancestry.add_nodes_from(p.id for p in family.people)
	for union in family.unions:
		ancestry.add_edges_from((parent, child)
			for parent in (union.father, union.mother) for child in union.children)
	balances = []
	continuing = []
	for union in family.unions:
		branches = [len(networkx.descendants(ancestry, child)) for child in union.children
			if ancestry.out_degree(child) > 0]
		continuing.append(len(branches))
		if len(branches) >= 2:
			balances.append(min(branches) / max(branches))
	result = dataclasses.asdict(similarity.complexity(family))
	result.update(
		degree_counts=dict(sorted(collections.Counter(dict(graph.degree()).values()).items())),
		branch_points=len(balances),
		continuing_children=sum(continuing),
		branch_balance=statistics.mean(balances) if balances else 0.0,
		sibship_variance=statistics.pvariance([len(u.children) for u in family.unions])
			if family.unions else 0.0)
	return result
