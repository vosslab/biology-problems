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
	main_couple: tuple[str, str] | None = None


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
def _parse_union_partner_token(token: str) -> tuple[str, str | None, str | None]:
	if len(token) > 1 and token[1] in ('m', 'f'):
		raise ValueError(f"Union partner '{token}' must omit sex (use minimal tokens).")
	return _parse_person_token(token, require_sex=False)


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
	founder_tokens = _scan_people_tokens(founder_segment, require_sex=True)
	if len(founder_tokens) < 2:
		raise ValueError("Founder segment must contain at least two people.")
	founder_ids: list[str] = []
	for person_id, sex, status in founder_tokens:
		_add_or_update_person(people, person_id, sex, status)
		founder_ids.append(person_id)
	main_couple = (founder_tokens[0][0], founder_tokens[1][0])

	for union_segment in segments[1:]:
		if ':' not in union_segment:
			raise ValueError(f"Union segment missing ':' -> '{union_segment}'.")
		parents_part, children_part = union_segment.split(':', 1)
		if children_part == '':
			raise ValueError(f"Union segment has no children -> '{union_segment}'.")
		if '-' not in parents_part:
			raise ValueError(f"Union segment missing '-' -> '{union_segment}'.")
		parent_a_str, parent_b_str = parents_part.split('-', 1)
		parent_a_id, parent_a_sex, parent_a_status = _parse_union_partner_token(parent_a_str)
		parent_b_id, parent_b_sex, parent_b_status = _parse_union_partner_token(parent_b_str)
		_add_or_update_person(people, parent_a_id, parent_a_sex, parent_a_status)
		_add_or_update_person(people, parent_b_id, parent_b_sex, parent_b_status)

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

	founder_id_set = set(founder_ids)
	for founder_id in founder_id_set:
		if founder_id in child_parent:
			raise ValueError(f"Founder '{founder_id}' appears as a child in a union.")

	progress = True
	while progress:
		progress = False
		for union in unions:
			parent_a = people[union.partner_a]
			parent_b = people[union.partner_b]
			if parent_a.sex is None and parent_b.sex is not None:
				parent_a.sex = 'female' if parent_b.sex == 'male' else 'male'
				progress = True
			if parent_b.sex is None and parent_a.sex is not None:
				parent_b.sex = 'female' if parent_a.sex == 'male' else 'male'
				progress = True

	for union in unions:
		parent_a = people[union.partner_a]
		parent_b = people[union.partner_b]
		if parent_a.sex is None or parent_b.sex is None:
			raise ValueError(f"Cannot infer sex for union '{union.partner_a}-{union.partner_b}'.")
		if parent_a.sex == parent_b.sex:
			raise ValueError(f"Union partners must be opposite sex in '{union.partner_a}-{union.partner_b}'.")

	normalized_unions: list[UnionIR] = []
	for union in unions:
		parent_a = people[union.partner_a]
		parent_b = people[union.partner_b]
		partner_a = union.partner_a
		partner_b = union.partner_b
		if parent_a.sex == 'female' and parent_b.sex == 'male':
			partner_a, partner_b = partner_b, partner_a
		normalized_unions.append(UnionIR(
			partner_a=partner_a,
			partner_b=partner_b,
			children=union.children,
		))
	unions = normalized_unions

	founder_partner_ids: set[str] = set()
	for union in unions:
		if union.partner_a in child_parent or union.partner_b in child_parent:
			continue
		founder_partner_ids.add(union.partner_a)
		founder_partner_ids.add(union.partner_b)

	if founder_id_set != founder_partner_ids:
		missing = sorted(founder_partner_ids - founder_id_set)
		extra = sorted(founder_id_set - founder_partner_ids)
		if missing:
			raise ValueError(f"Founder segment missing founder partners: {', '.join(missing)}.")
		if extra:
			raise ValueError(f"Founder segment includes non-founders: {', '.join(extra)}.")

	generations: dict[str, int] = {founder_id: 1 for founder_id in founder_id_set}
	progress = True
	while progress:
		progress = False
		for union in unions:
			parent_a = union.partner_a
			parent_b = union.partner_b
			gen_a = generations.get(parent_a)
			gen_b = generations.get(parent_b)
			if gen_a is not None and gen_b is None:
				generations[parent_b] = gen_a
				progress = True
			elif gen_b is not None and gen_a is None:
				generations[parent_a] = gen_b
				progress = True
			elif gen_a is not None and gen_b is not None and gen_a != gen_b:
				raise ValueError(f"Union partners must be same generation in '{parent_a}-{parent_b}'.")
			parent_gen = generations.get(parent_a) or generations.get(parent_b)
			if parent_gen is not None:
				for child_id in union.children:
					child_gen = generations.get(child_id)
					if child_gen is None:
						generations[child_id] = parent_gen + 1
						progress = True
					elif child_gen != parent_gen + 1:
						raise ValueError(f"Child '{child_id}' has inconsistent generation.")

	missing_generation = sorted(person_id for person_id in people if person_id not in generations)
	if missing_generation:
		raise ValueError(
			"Could not assign generation for: " + ', '.join(missing_generation)
		)

	main_union = None
	for union in unions:
		if {union.partner_a, union.partner_b} == set(main_couple):
			main_union = union
			break
	if main_union is None or not main_union.children:
		raise ValueError("Main couple must appear as a union with children.")

	return PedigreeGraphSpec(people=people, unions=unions, main_couple=main_couple)


#===============================
def validate_pedigree_graph_spec(spec_string: str) -> list[str]:
	"""
	Validate a pedigree graph spec string.

	Args:
		spec_string (str): Pedigree graph spec string.

	Returns:
		list[str]: Validation error messages (empty means valid).
	"""
	try:
		parse_pedigree_graph_spec(spec_string)
	except Exception as exc:
		return [str(exc)]
	return []


#===============================
def is_valid_pedigree_graph_spec(spec_string: str) -> bool:
	"""
	Check whether a pedigree graph spec string is valid.

	Args:
		spec_string (str): Pedigree graph spec string.

	Returns:
		bool: True if valid, otherwise False.
	"""
	errors = validate_pedigree_graph_spec(spec_string)
	return len(errors) == 0


#===============================
def format_pedigree_graph_spec(pedigree: PedigreeGraphSpec) -> str:
	"""
	Serialize a pedigree graph spec to a compact string.
	"""
	def format_person(person: IndividualIR, include_sex: bool = True) -> str:
		if person.sex is None:
			raise ValueError(f"Person '{person.person_id}' missing sex.")
		sex_char = 'm' if person.sex == 'male' else 'f'
		status_char = ''
		if person.status == 'infected':
			status_char = 'i'
		elif person.status == 'carrier':
			status_char = 'c'
		if include_sex:
			return f"{person.person_id}{sex_char}{status_char}"
		if status_char:
			return f"{person.person_id}{status_char}"
		return f"{person.person_id}"

	child_ids = set()
	for union in pedigree.unions:
		child_ids.update(union.children)

	founder_id_set: set[str] = set()
	for union in pedigree.unions:
		if union.partner_a in child_ids or union.partner_b in child_ids:
			continue
		founder_id_set.add(union.partner_a)
		founder_id_set.add(union.partner_b)
	founder_ids = sorted(founder_id_set)
	if not founder_ids:
		founder_ids = sorted(pedigree.people)

	main_couple = pedigree.main_couple
	if main_couple is None and len(founder_ids) >= 2:
		main_couple = (founder_ids[0], founder_ids[1])

	ordered_founders: list[str] = []
	if main_couple is not None:
		for founder_id in main_couple:
			if founder_id in founder_ids and founder_id not in ordered_founders:
				ordered_founders.append(founder_id)
	for founder_id in founder_ids:
		if founder_id not in ordered_founders:
			ordered_founders.append(founder_id)

	founder_tokens = [
		format_person(pedigree.people[founder_id], include_sex=True)
		for founder_id in ordered_founders
	]
	segments = [f"F:{''.join(founder_tokens)}"]

	for union in pedigree.unions:
		parent_a = pedigree.people[union.partner_a]
		parent_b = pedigree.people[union.partner_b]
		parent_a_token = format_person(parent_a, include_sex=False)
		parent_b_token = format_person(parent_b, include_sex=False)
		if parent_a.sex == 'female' and parent_b.sex == 'male':
			parent_a_token, parent_b_token = parent_b_token, parent_a_token
		children_tokens = [
			format_person(pedigree.people[child_id], include_sex=True)
			for child_id in union.children
		]
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
