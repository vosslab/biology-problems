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
	if assessment.answer is None:
		return None, assessment.reasons
	diagram = layout.lay_out(case.family, mirror)
	errors = layout.layout_errors(diagram)
	if errors:
		return None, errors
	result = AcceptedCase(case, assessment, diagram)
	return result, ()


#============================================
def generate_case(mode: str, rng: random.Random, max_attempts: int = 500,
		min_people: int = 11, max_people: int = 16,
		show_carriers: bool = False) -> AcceptedCase:
	"""Search a bounded number of candidates for the requested teaching answer.

	Args:
		mode: Required inheritance mode.
		rng: Explicit generator for all procedural choices.
		max_attempts: Candidate budget before explicit failure.
		min_people: Inclusive minimum family size.
		max_people: Inclusive maximum family size.
		show_carriers: Reveal unaffected heterozygotes when true.

	Returns:
		Accepted case with attempt count and prior rejection counts.

	Raises:
		GenerationFailure: No suitable case within the budget.
		ValueError: Invalid mode or infeasible size bounds.
	"""
	rejections = collections.Counter()
	for attempt in range(1, max_attempts + 1):
		case = sources.simulate_case(mode, rng, min_people, max_people, show_carriers)
		accepted, reasons = evaluate(case, mirror=rng.choice((True, False)))
		if accepted is not None:
			if accepted.assessment.answer == mode:
				return dataclasses.replace(accepted, attempts=attempt, rejections=dict(rejections))
			reasons = ('Teaching evidence favors another mode',)
		rejections.update(reasons)
	raise GenerationFailure(f'No suitable {mode} case after {max_attempts} attempts: {dict(rejections)}')


#============================================
def authored_cases(path: str | pathlib.Path | None = None) -> list[AcceptedCase]:
	"""Load and accept every example in an authored bank.

	Args:
		path: YAML bank path, or None for the bundled examples.

	Returns:
		Accepted cases with expectations checked after visible-evidence assessment.

	Raises:
		ValueError: An authored case is invalid, unsuitable, or disagrees with its expectation.
	"""
	if path is None:
		path = pathlib.Path(__file__).parent.parent / 'authored_cases.yml'
	result = []
	for case in sources.load_cases(path):
		accepted, reasons = evaluate(case)
		if accepted is None:
			raise ValueError(f'Unsuitable authored case {case.metadata}: {reasons}')
		if 'expected_mode' in case.metadata and case.metadata['expected_mode'] != accepted.assessment.answer:
			raise ValueError(f'Authored expectation disagrees with visible evidence: {case.metadata}')
		result.append(accepted)
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
def matching_set(rng: random.Random, authored: list[AcceptedCase] | None = None) -> list[AcceptedCase]:
	"""Assemble independently accepted cases with comparable complexity.

	Args:
		rng: Generator for selection, simulation, and ordering.
		authored: Accepted bank, or None to generate procedural cases.

	Returns:
		Shuffled cases using every mode once, with 12-15 people over three or four generations.

	Raises:
		GenerationFailure: A suitable case is unavailable for any mode.
	"""
	result = []
	for mode in inheritance.MODES:
		if authored is None:
			case = generate_case(mode, rng, min_people=12, max_people=15)
		else:
			candidates = [item for item in authored if item.assessment.answer == mode
				and 12 <= len(item.case.family.people) <= 15
				and 2 <= max(item.case.family.generations().values()) <= 3]
			if not candidates:
				raise GenerationFailure(f'No comparable authored case for {mode}')
			case = present(rng.choice(candidates), rng)
		result.append(case)
	rng.shuffle(result)
	return result
