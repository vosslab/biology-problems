#!/usr/bin/env python3

# Local repo modules
import graph_spec


#===============================
AUTOSOMAL_DOMINANT = 'autosomal dominant'
AUTOSOMAL_RECESSIVE = 'autosomal recessive'
X_LINKED_DOMINANT = 'x-linked dominant'
X_LINKED_RECESSIVE = 'x-linked recessive'
Y_LINKED = 'y-linked'
NONE_MODE = 'none'
AUTOSOMAL_ALLELES = ('A', 'a')
X_LINKED_DOMINANT_ALLELES = ('D', 'd')
X_LINKED_RECESSIVE_ALLELES = ('X', 'x')


#===============================
def _phenotype_from_status(status: str | None) -> str:
	if status == 'infected':
		return 'affected'
	if status == 'carrier':
		return 'carrier'
	return 'unaffected'


#===============================
def _carriers_visible(people: dict) -> bool:
	return any(person.status == 'carrier' for person in people.values())


#===============================
def _canonical_pair(
	allele_a: str,
	allele_b: str,
	allele_order: tuple,
) -> tuple:
	if allele_a == allele_b:
		return (allele_a, allele_b)
	order_map = {
		allele_order[0]: 0,
		allele_order[1]: 1,
	}
	if order_map[allele_a] <= order_map[allele_b]:
		return (allele_a, allele_b)
	return (allele_b, allele_a)


#===============================
def _autosomal_child_genotypes(
	parent_a: tuple,
	parent_b: tuple,
) -> set:
	alleles_a = parent_a
	alleles_b = parent_b
	children: set = set()
	for allele_a in alleles_a:
		for allele_b in alleles_b:
			children.add(_canonical_pair(allele_a, allele_b, AUTOSOMAL_ALLELES))
	return children


#===============================
def _autosomal_parent_possible(
	parent_genotype: tuple,
	other_parent_domain: list,
	children_domains: list,
) -> bool:
	for child_domain in children_domains:
		match_found = False
		for other_genotype in other_parent_domain:
			if child_domain & _autosomal_child_genotypes(parent_genotype, other_genotype):
				match_found = True
				break
		if not match_found:
			return False
	return True


#===============================
def _propagate_autosomal(
	unions: list,
	domains: dict,
) -> bool:
	changed = True
	while changed:
		changed = False
		for union in unions:
			parent_a = union.partner_a
			parent_b = union.partner_b
			parent_a_domain = domains[parent_a]
			parent_b_domain = domains[parent_b]

			for child_id in union.children:
				child_domain = domains[child_id]
				possible_child: set = set()
				for genotype_a in parent_a_domain:
					for genotype_b in parent_b_domain:
						possible_child.update(_autosomal_child_genotypes(genotype_a, genotype_b))
				new_child_domain = child_domain & possible_child
				if not new_child_domain:
					return False
				if new_child_domain != child_domain:
					domains[child_id] = new_child_domain
					changed = True

			children_domains = [domains[child_id] for child_id in union.children]
			new_parent_a = {
				genotype for genotype in parent_a_domain
				if _autosomal_parent_possible(genotype, parent_b_domain, children_domains)
			}
			if not new_parent_a:
				return False
			if new_parent_a != parent_a_domain:
				domains[parent_a] = new_parent_a
				parent_a_domain = new_parent_a
				changed = True

			new_parent_b = {
				genotype for genotype in parent_b_domain
				if _autosomal_parent_possible(genotype, parent_a_domain, children_domains)
			}
			if not new_parent_b:
				return False
			if new_parent_b != parent_b_domain:
				domains[parent_b] = new_parent_b
				changed = True

	return True


#===============================
def _solve_autosomal(
	unions: list,
	domains: dict,
) -> bool:
	if not _propagate_autosomal(unions, domains):
		return False
	unsolved = [person_id for person_id, domain in domains.items() if len(domain) > 1]
	if not unsolved:
		return True
	person_id = min(unsolved, key=lambda pid: len(domains[pid]))
	for genotype in sorted(domains[person_id]):
		next_domains = {pid: set(values) for pid, values in domains.items()}
		next_domains[person_id] = {genotype}
		if _solve_autosomal(unions, next_domains):
			return True
	return False


#===============================
def _x_linked_child_genotypes(
	father_genotype: tuple,
	mother_genotype: tuple,
	child_sex: str,
	allele_order: tuple,
) -> set:
	father_allele = father_genotype[0]
	mother_alleles = mother_genotype
	if child_sex == 'male':
		return {(allele,) for allele in mother_alleles}
	children: set = set()
	for allele in mother_alleles:
		children.add(_canonical_pair(father_allele, allele, allele_order))
	return children


#===============================
def _x_linked_parent_possible(
	parent_is_father: bool,
	parent_domain: list,
	other_parent_domain: list,
	children: list,
	allele_order: tuple,
) -> set:
	valid: set = set()
	for genotype in parent_domain:
		ok = True
		for child_sex, child_domain in children:
			match_found = False
			for other_genotype in other_parent_domain:
				if parent_is_father:
					possible = _x_linked_child_genotypes(
						genotype,
						other_genotype,
						child_sex,
						allele_order,
					)
				else:
					possible = _x_linked_child_genotypes(
						other_genotype,
						genotype,
						child_sex,
						allele_order,
					)
				if child_domain & possible:
					match_found = True
					break
			if not match_found:
				ok = False
				break
		if ok:
			valid.add(genotype)
	return valid


#===============================
def _propagate_x_linked(
	pedigree: graph_spec.PedigreeGraphSpec,
	domains: dict,
	allele_order: tuple,
) -> bool:
	changed = True
	while changed:
		changed = False
		for union in pedigree.unions:
			parent_a = union.partner_a
			parent_b = union.partner_b
			parent_a_sex = pedigree.people[parent_a].sex
			if parent_a_sex == 'male':
				father_id = parent_a
				mother_id = parent_b
			else:
				father_id = parent_b
				mother_id = parent_a
			father_domain = domains[father_id]
			mother_domain = domains[mother_id]

			for child_id in union.children:
				child_sex = pedigree.people[child_id].sex
				child_domain = domains[child_id]
				possible_child: set = set()
				for father_genotype in father_domain:
					for mother_genotype in mother_domain:
						possible_child.update(_x_linked_child_genotypes(
							father_genotype,
							mother_genotype,
							child_sex,
							allele_order,
						))
				new_child_domain = child_domain & possible_child
				if not new_child_domain:
					return False
				if new_child_domain != child_domain:
					domains[child_id] = new_child_domain
					changed = True

				parent_children = [(pedigree.people[child_id].sex, domains[child_id]) for child_id in union.children]
				new_father = _x_linked_parent_possible(
					True,
				father_domain,
				mother_domain,
				parent_children,
				allele_order,
			)
			if not new_father:
				return False
			if new_father != father_domain:
				domains[father_id] = new_father
				father_domain = new_father
				changed = True

			new_mother = _x_linked_parent_possible(
				False,
				mother_domain,
				father_domain,
				parent_children,
				allele_order,
			)
			if not new_mother:
				return False
			if new_mother != mother_domain:
				domains[mother_id] = new_mother
				changed = True

	return True


#===============================
def _solve_x_linked(
	pedigree: graph_spec.PedigreeGraphSpec,
	domains: dict,
	allele_order: tuple,
) -> bool:
	if not _propagate_x_linked(pedigree, domains, allele_order):
		return False
	unsolved = [person_id for person_id, domain in domains.items() if len(domain) > 1]
	if not unsolved:
		return True
	person_id = min(unsolved, key=lambda pid: len(domains[pid]))
	for genotype in sorted(domains[person_id]):
		next_domains = {pid: set(values) for pid, values in domains.items()}
		next_domains[person_id] = {genotype}
		if _solve_x_linked(pedigree, next_domains, allele_order):
			return True
	return False


#===============================
def _autosomal_domains(
	pedigree: graph_spec.PedigreeGraphSpec,
	mode: str,
	carriers_visible: bool,
) -> dict | None:
	domains: dict = {}
	heterozygous = _canonical_pair(AUTOSOMAL_ALLELES[0], AUTOSOMAL_ALLELES[1], AUTOSOMAL_ALLELES)
	for person_id, person in pedigree.people.items():
		phenotype = _phenotype_from_status(person.status)
		if mode == AUTOSOMAL_DOMINANT:
			if phenotype == 'carrier':
				return None
			if phenotype == 'affected':
				domain = {(AUTOSOMAL_ALLELES[0], AUTOSOMAL_ALLELES[0]), heterozygous}
			else:
				domain = {(AUTOSOMAL_ALLELES[1], AUTOSOMAL_ALLELES[1])}
		else:
			if phenotype == 'affected':
				domain = {(AUTOSOMAL_ALLELES[1], AUTOSOMAL_ALLELES[1])}
			elif phenotype == 'carrier':
				domain = {heterozygous}
			else:
				if carriers_visible:
					domain = {(AUTOSOMAL_ALLELES[0], AUTOSOMAL_ALLELES[0])}
				else:
					domain = {
						(AUTOSOMAL_ALLELES[0], AUTOSOMAL_ALLELES[0]),
						heterozygous,
					}
		domains[person_id] = domain
	return domains


#===============================
def _x_linked_domains(
	pedigree: graph_spec.PedigreeGraphSpec,
	mode: str,
	carriers_visible: bool,
) -> dict | None:
	domains: dict = {}
	if mode == X_LINKED_RECESSIVE:
		alleles = X_LINKED_RECESSIVE_ALLELES
	else:
		alleles = X_LINKED_DOMINANT_ALLELES
	heterozygous = _canonical_pair(alleles[0], alleles[1], alleles)
	for person_id, person in pedigree.people.items():
		if person.sex is None:
			return None
		phenotype = _phenotype_from_status(person.status)
		if mode == X_LINKED_RECESSIVE:
			if person.sex == 'male':
				if phenotype == 'carrier':
					return None
				domain = {(alleles[1],)} if phenotype == 'affected' else {(alleles[0],)}
			else:
				if phenotype == 'affected':
					domain = {(alleles[1], alleles[1])}
				elif phenotype == 'carrier':
					domain = {heterozygous}
				else:
					if carriers_visible:
						domain = {(alleles[0], alleles[0])}
					else:
						domain = {(alleles[0], alleles[0]), heterozygous}
		else:
			if phenotype == 'carrier':
				return None
			if person.sex == 'male':
				domain = {(alleles[0],)} if phenotype == 'affected' else {(alleles[1],)}
			else:
				if phenotype == 'affected':
					domain = {(alleles[0], alleles[0]), heterozygous}
				else:
					domain = {(alleles[1], alleles[1])}
		domains[person_id] = domain
	return domains


#===============================
def _check_y_linked(pedigree: graph_spec.PedigreeGraphSpec) -> bool:
	for person in pedigree.people.values():
		phenotype = _phenotype_from_status(person.status)
		if phenotype == 'carrier':
			return False
		if person.sex == 'female' and phenotype == 'affected':
			return False

		for union in pedigree.unions:
			parent_a = union.partner_a
			parent_b = union.partner_b
			parent_a_sex = pedigree.people[parent_a].sex
			if parent_a_sex == 'male':
				father_id = parent_a
			else:
				father_id = parent_b
		father_status = _phenotype_from_status(pedigree.people[father_id].status)
		for child_id in union.children:
			child = pedigree.people[child_id]
			if child.sex != 'male':
				continue
			child_status = _phenotype_from_status(child.status)
			if father_status == 'affected' and child_status != 'affected':
				return False
			if father_status != 'affected' and child_status == 'affected':
				return False

	return True


#===============================
def _is_mode_possible(pedigree: graph_spec.PedigreeGraphSpec, mode: str) -> bool:
	carriers_visible = _carriers_visible(pedigree.people)
	if carriers_visible and mode not in (AUTOSOMAL_RECESSIVE, X_LINKED_RECESSIVE):
		return False

	if mode in (AUTOSOMAL_DOMINANT, AUTOSOMAL_RECESSIVE):
		domains = _autosomal_domains(pedigree, mode, carriers_visible)
		if domains is None:
			return False
		return _solve_autosomal(pedigree.unions, domains)

	if mode in (X_LINKED_DOMINANT, X_LINKED_RECESSIVE):
		domains = _x_linked_domains(pedigree, mode, carriers_visible)
		if domains is None:
			return False
		allele_order = (
			X_LINKED_DOMINANT_ALLELES
			if mode == X_LINKED_DOMINANT
			else X_LINKED_RECESSIVE_ALLELES
		)
		return _solve_x_linked(pedigree, domains, allele_order)

	if mode == Y_LINKED:
		return _check_y_linked(pedigree)

	return False


#===============================
def possible_modes(pedigree: graph_spec.PedigreeGraphSpec) -> list:
	"""
	Return all inheritance modes consistent with a pedigree graph spec.
	"""
	order = [
		AUTOSOMAL_DOMINANT,
		AUTOSOMAL_RECESSIVE,
		X_LINKED_DOMINANT,
		X_LINKED_RECESSIVE,
		Y_LINKED,
	]
	matches = [mode for mode in order if _is_mode_possible(pedigree, mode)]
	if not matches:
		return [NONE_MODE]
	return matches


#===============================
def possible_modes_from_spec(spec_string: str) -> list:
	"""
	Parse and evaluate a pedigree graph spec string.
	"""
	pedigree = graph_spec.parse_pedigree_graph_spec(spec_string)
	return possible_modes(pedigree)


#===============================
if __name__ == '__main__':
	sample = 'F:AmBfCmDfEfGfHmIf;A-B:CmDfEf;C-G:HmIf'
	print(possible_modes_from_spec(sample))

## THE END
