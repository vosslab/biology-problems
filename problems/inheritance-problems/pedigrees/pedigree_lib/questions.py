"""One acceptance pipeline for authored and procedural homework cases."""

# Standard Library
import random
import pathlib
import collections
import dataclasses

# local repo modules
import pedigree_lib.layout as layout
import pedigree_lib.policy as policy
import pedigree_lib.sources as sources
import pedigree_lib.inheritance as inheritance
import pedigree_lib.graphs as graphs
import pedigree_lib.family as family_model


#============================================
class GenerationFailure(RuntimeError):
	"""The bounded candidate budget was exhausted; reasons accompany the failure."""


#============================================
@dataclasses.dataclass(frozen=True)
class AcceptedCase:
	case: sources.Case
	assessment: policy.Assessment
	diagram: layout.Diagram
	attempts: int = 1
	rejections: dict[str, int] = dataclasses.field(default_factory=dict)


#============================================
def evaluate(case: sources.Case, mirror: bool = False) -> tuple[AcceptedCase | None, tuple]:
	"""Apply the shared biological, teaching, and geometry gates.

	Args:
		case: Authored or simulated case to assess.
		mirror: Reflect the accepted drawing horizontally.

	Returns:
		Accepted case and empty reasons, or None and rejection reasons.

	Raises:
		ValueError: Invalid family or observation data; programming errors propagate.
	"""
	assessment = policy.assess(case.family, case.observations)
	# Hidden carrier genotypes must obey the same rule even when not forced by the drawing.
	if case.genotypes:
		carriers = sorted(pid for pid in family_model.later_spouses(case.family)
			if case.observations[pid].affected is False and case.genotypes[pid] == (0, 1))
		if carriers:
			return None, ('Unaffected later spouses cannot be carriers: ' + ', '.join(carriers),)
	if assessment.answer is None:
		return None, assessment.reasons
	diagram = layout.lay_out(case.family, mirror)
	errors = layout.layout_errors(diagram)
	if errors:
		return None, errors
	result = AcceptedCase(case, assessment, diagram)
	return result, ()


#============================================
def generate_case(mode: str, rng: random.Random, max_attempts: int = 5000,
		min_people: int = 11, max_people: int = 16,
		show_carriers: bool = False, generations: int = 4, *, seed_couples: int = 1,
		couples: tuple[int, int] | None = None, children: tuple[int, int] = (1, 4),
		root_children: tuple[int, int] | None = None) -> AcceptedCase:
	"""Search a bounded number of candidates for the requested teaching answer.

	Args:
		mode: Required inheritance mode.
		rng: Explicit generator for all procedural choices.
		max_attempts: Candidate budget before explicit failure.
		min_people: Inclusive minimum family size.
		max_people: Inclusive maximum family size.
		show_carriers: Reveal unaffected heterozygotes when true.
		generations: Required family depth, from three to five.
		seed_couples: Number of founding couples in generation one.
		couples: Inclusive total-couple bounds; None uses constructor defaults.
		children: Inclusive offspring bounds for non-seed unions.
		root_children: Inclusive offspring bounds for seed unions; None uses depth defaults.

	Returns:
		Accepted case with attempt count and prior rejection counts.

	Raises:
		GenerationFailure: No suitable case within the budget.
		ValueError: Invalid mode or infeasible size bounds.
	"""
	rejections = collections.Counter()
	for attempt in range(1, max_attempts + 1):
		case = sources.simulate_case(mode, rng, min_people, max_people, show_carriers, generations,
			seed_couples=seed_couples, couples=couples, children=children, root_children=root_children)
		accepted, reasons = evaluate(case, mirror=rng.choice((True, False)))
		if accepted is not None:
			if accepted.assessment.answer == mode:
				return dataclasses.replace(accepted, attempts=attempt, rejections=dict(rejections))
			reasons = ('Teaching evidence favors another mode',)
		rejections.update(reasons)
	raise GenerationFailure(f'No suitable {mode} case after {max_attempts} attempts: {dict(rejections)}')


#============================================
def authored_cases(path: str | pathlib.Path | None = None,
		student: bool = False) -> list[AcceptedCase]:
	"""Load and accept every example in an authored bank.

	Args:
		path: YAML bank path, or None for the bundled examples.
		student: Keep connected, answerable cases with carrier status hidden.

	Returns:
		Accepted cases with expectations checked after visible-evidence assessment.

	Raises:
		ValueError: An authored case is invalid, unsuitable, or disagrees with its expectation.
	"""
	if path is None:
		path = pathlib.Path(__file__).parent.parent / 'authored_cases.yml'
	result = []
	for case in sources.load_cases(path):
		if student:
			if len(graphs.components(case.family)) != 1:
				continue
			observations = {pid: dataclasses.replace(obs, carrier=False)
				for pid, obs in case.observations.items()}
			case = dataclasses.replace(case, observations=observations)
		accepted, reasons = evaluate(case)
		if accepted is None:
			if student:
				continue
			raise ValueError(f'Unsuitable authored case {case.metadata}: {reasons}')
		if 'expected_mode' in case.metadata and case.metadata['expected_mode'] != accepted.assessment.answer:
			raise ValueError(f'Authored expectation disagrees with visible evidence: {case.metadata}')
		result.append(accepted)
	if student and not result:
		raise ValueError('No connected authored cases are answerable with carrier status hidden')
	return result


#============================================
def present(case: AcceptedCase, rng: random.Random) -> AcceptedCase:
	"""Vary sibling order and reflection without changing biological state.

	Args:
		case: Previously accepted authored case; explicit sibling hints prevent shuffling.
		rng: Generator for presentation choices.

	Returns:
		A readable accepted presentation; reflection may reverse hinted order.

	Raises:
		GenerationFailure: No readable presentation within the bounded search.
	"""
	for _ in range(100):
		unions = []
		for index, union in enumerate(case.case.family.unions):
			children = list(union.children)
			if index not in case.case.ordered_unions:
				rng.shuffle(children)
			unions.append(dataclasses.replace(union, children=tuple(children)))
		family = dataclasses.replace(case.case.family, unions=tuple(unions))
		candidate = dataclasses.replace(case.case, family=family)
		accepted, _ = evaluate(candidate, rng.choice((True, False)))
		if accepted is not None:
			return accepted
	raise GenerationFailure('No readable presentation of authored family after 100 attempts')


#============================================
def matching_set(rng: random.Random, authored: list[AcceptedCase] | None = None,
		generations: int = 3, min_people: int | None = None,
		max_people: int | None = None, *, seed_couples: int = 1,
		couples: tuple[int, int] | None = None, children: tuple[int, int] = (1, 4),
		root_children: tuple[int, int] | None = None) -> list[AcceptedCase]:
	"""Assemble independently accepted cases with comparable complexity.

	Args:
		rng: Generator for selection, simulation, and ordering.
		authored: Accepted bank, or None to generate procedural cases.
		generations: Shared depth for all diagrams in this set.
		min_people: Inclusive size minimum; None uses the standard depth-specific bound.
		max_people: Inclusive size maximum; None uses the standard depth-specific bound.
		seed_couples: Procedural founding-couple count, shared across the set.
		couples: Procedural total-couple bounds; None uses constructor defaults.
		children: Procedural offspring bounds for non-seed unions.
		root_children: Procedural offspring bounds for seed unions; None uses depth defaults.

	Returns:
		Shuffled cases using every mode once, with equal depth and comparable sizes.

	Raises:
		GenerationFailure: A suitable case is unavailable for any mode.
	"""
	default_min, default_max = (12, 15) if generations == 3 else (16, 22)
	if min_people is None:
		min_people = default_min
	if max_people is None:
		max_people = default_max
	result = []
	for mode in inheritance.MODES:
		if authored is None:
			case = generate_case(mode, rng, min_people=min_people, max_people=max_people,
				generations=generations, seed_couples=seed_couples, couples=couples,
				children=children, root_children=root_children)
		else:
			candidates = [item for item in authored if item.assessment.answer == mode
				and min_people <= len(item.case.family.people) <= max_people
				and max(item.case.family.generations().values()) == generations - 1]
			if not candidates:
				raise GenerationFailure(f'No comparable authored case for {mode}')
			case = present(rng.choice(candidates), rng)
		result.append(case)
	rng.shuffle(result)
	return result
