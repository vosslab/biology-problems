#!/usr/bin/env python3

# Standard Library
import dataclasses


#===============================
@dataclasses.dataclass
class IndividualIR:
	person_id: str
	sex: str | None
	status: str | None = None


#===============================
@dataclasses.dataclass
class UnionIR:
	partner_a: str
	partner_b: str
	children: list[str]


#===============================
@dataclasses.dataclass
class PedigreeGraphSpec:
	people: dict[str, IndividualIR]
	unions: list[UnionIR]


#===============================
def _parse_person_token(token: str, require_sex: bool) -> tuple[str, str | None, str | None]:
	if not token:
		raise ValueError('Empty person token.')
	person_id = token[0]
	if not person_id.isalpha() or not person_id.isupper():
		raise ValueError(f"Invalid person id '{person_id}'.")
	sex = None
	status = None
	if len(token) > 1:
		sex_char = token[1]
		if sex_char in ('m', 'f'):
			sex = 'male' if sex_char == 'm' else 'female'
			if len(token) > 2:
				status_char = token[2]
				if status_char not in ('i', 'c'):
					raise ValueError(f"Invalid status '{status_char}' in token '{token}'.")
				status = 'infected' if status_char == 'i' else 'carrier'
				if len(token) > 3:
					raise ValueError(f"Unexpected trailing characters in token '{token}'.")
		elif sex_char in ('i', 'c'):
			status = 'infected' if sex_char == 'i' else 'carrier'
			if len(token) > 2:
				raise ValueError(f"Unexpected trailing characters in token '{token}'.")
		else:
			raise ValueError(f"Invalid token '{token}'.")
	if require_sex and sex is None:
		raise ValueError(f"Missing sex for token '{token}'.")
	return person_id, sex, status


#===============================
def _scan_people_tokens(segment: str, require_sex: bool) -> list[tuple[str, str | None, str | None]]:
	if not segment:
		return []
	results: list[tuple[str, str | None, str | None]] = []
	idx = 0
	while idx < len(segment):
		char = segment[idx]
		if not char.isalpha() or not char.isupper():
			raise ValueError(f"Unexpected character '{char}' in segment '{segment}'.")
		token = char
		idx += 1
		if idx < len(segment) and segment[idx] in ('m', 'f', 'i', 'c'):
			token += segment[idx]
			idx += 1
			if token[-1] in ('m', 'f') and idx < len(segment) and segment[idx] in ('i', 'c'):
				token += segment[idx]
				idx += 1
		person_id, sex, status = _parse_person_token(token, require_sex)
		results.append((person_id, sex, status))
	return results


#===============================
def _add_or_update_person(people: dict[str, IndividualIR], person_id: str, sex: str | None, status: str | None) -> None:
	if person_id in people:
		person = people[person_id]
		if sex is not None and person.sex is not None and sex != person.sex:
			raise ValueError(f"Sex mismatch for '{person_id}'.")
		if person.sex is None and sex is not None:
			person.sex = sex
		if status is not None:
			person.status = status
		return
	people[person_id] = IndividualIR(person_id=person_id, sex=sex, status=status)


#===============================
def parse_pedigree_graph_spec(spec_string: str) -> PedigreeGraphSpec:
	"""
	Parse a pedigree graph spec string into individuals and unions.
	"""
	if not spec_string:
		raise ValueError('Empty pedigree graph spec string.')
	segments = [segment for segment in spec_string.split(';') if segment]
	if not segments:
		raise ValueError('Spec string has no segments.')
	if not segments[0].startswith('F:'):
		raise ValueError("Spec string must start with 'F:' segment.")

	people: dict[str, IndividualIR] = {}
	unions: list[UnionIR] = []
	child_parent: dict[str, str] = {}

	founder_segment = segments[0][2:]
	for person_id, sex, status in _scan_people_tokens(founder_segment, require_sex=True):
		_add_or_update_person(people, person_id, sex, status)

	for union_segment in segments[1:]:
		if ':' not in union_segment:
			raise ValueError(f"Union segment missing ':' -> '{union_segment}'.")
		parents_part, children_part = union_segment.split(':', 1)
		if '-' not in parents_part:
			raise ValueError(f"Union segment missing '-' -> '{union_segment}'.")
		parent_a_str, parent_b_str = parents_part.split('-', 1)
		parent_a_id, parent_a_sex, parent_a_status = _parse_person_token(parent_a_str, require_sex=False)
		parent_b_id, parent_b_sex, parent_b_status = _parse_person_token(parent_b_str, require_sex=False)
		_add_or_update_person(people, parent_a_id, parent_a_sex, parent_a_status)
		_add_or_update_person(people, parent_b_id, parent_b_sex, parent_b_status)

		parent_a = people[parent_a_id]
		parent_b = people[parent_b_id]
		if parent_a.sex is None and parent_b.sex is not None:
			parent_a.sex = 'female' if parent_b.sex == 'male' else 'male'
		if parent_b.sex is None and parent_a.sex is not None:
			parent_b.sex = 'female' if parent_a.sex == 'male' else 'male'
		if parent_a.sex is None or parent_b.sex is None:
			raise ValueError(f"Cannot infer sex for union '{union_segment}'.")
		if parent_a.sex == parent_b.sex:
			raise ValueError(f"Union partners must be opposite sex in '{union_segment}'.")

		children_tokens = _scan_people_tokens(children_part, require_sex=True)
		children_ids: list[str] = []
		for child_id, child_sex, child_status in children_tokens:
			_add_or_update_person(people, child_id, child_sex, child_status)
			if child_id in child_parent:
				raise ValueError(f"Child '{child_id}' appears in multiple unions.")
			child_parent[child_id] = parent_a_id
			children_ids.append(child_id)

		unions.append(UnionIR(
			partner_a=parent_a_id,
			partner_b=parent_b_id,
			children=children_ids,
		))

	return PedigreeGraphSpec(people=people, unions=unions)


#===============================
def format_pedigree_graph_spec(pedigree: PedigreeGraphSpec) -> str:
	"""
	Serialize a pedigree graph spec to a compact string.
	"""
	def format_person(person: IndividualIR) -> str:
		if person.sex is None:
			raise ValueError(f"Person '{person.person_id}' missing sex.")
		sex_char = 'm' if person.sex == 'male' else 'f'
		status_char = ''
		if person.status == 'infected':
			status_char = 'i'
		elif person.status == 'carrier':
			status_char = 'c'
		return f"{person.person_id}{sex_char}{status_char}"

	people_tokens = [format_person(pedigree.people[person_id]) for person_id in sorted(pedigree.people)]
	segments = [f"F:{''.join(people_tokens)}"]
	for union in pedigree.unions:
		parent_a = pedigree.people[union.partner_a]
		parent_b = pedigree.people[union.partner_b]
		parent_a_token = format_person(parent_a)
		parent_b_token = format_person(parent_b)
		children_tokens = [format_person(pedigree.people[child_id]) for child_id in union.children]
		segments.append(f"{parent_a_token}-{parent_b_token}:{''.join(children_tokens)}")
	return ';'.join(segments)


#===============================
def hash_pedigree_graph_spec(spec_string: str) -> str:
	"""
	Return a stable hash for a pedigree graph spec string.
	"""
	import hashlib
	digest = hashlib.sha256(spec_string.strip().encode('utf-8')).hexdigest()
	return digest


#===============================
if __name__ == '__main__':
	sample = 'F:AmBfCmDfEfGfHmIf;A-B:CmDfEf;C-G:HmIf'
	parsed = parse_pedigree_graph_spec(sample)
	print(format_pedigree_graph_spec(parsed))

## THE END
