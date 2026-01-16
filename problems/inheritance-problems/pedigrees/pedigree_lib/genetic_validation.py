
# Local repo modules
import validation


#===============================
def _has_recessive_key(
	individuals: dict,
	couples: list,
) -> bool:
	for couple in couples:
		parent_a = individuals.get(couple.partner_a)
		parent_b = individuals.get(couple.partner_b)
		if parent_a is None or parent_b is None:
			continue
		if parent_a.phenotype != 'unaffected' or parent_b.phenotype != 'unaffected':
			continue
		for child_id in couple.children:
			child = individuals.get(child_id)
			if child is not None and child.phenotype == 'affected':
				return True
	return False


#===============================
def _has_dominant_key(
	individuals: dict,
	couples: list,
) -> bool:
	for couple in couples:
		parent_a = individuals.get(couple.partner_a)
		parent_b = individuals.get(couple.partner_b)
		if parent_a is None or parent_b is None:
			continue
		if parent_a.phenotype != 'affected' or parent_b.phenotype != 'affected':
			continue
		for child_id in couple.children:
			child = individuals.get(child_id)
			if child is not None and child.phenotype == 'unaffected':
				return True
	return False


#===============================
def _iter_children(couples: list):
	for couple in couples:
		for child_id in couple.children:
			yield couple, child_id


#===============================
def _get_parents(
	individuals: dict,
	couple,
) -> tuple:
	parent_a = individuals.get(couple.partner_a)
	parent_b = individuals.get(couple.partner_b)
	if parent_a is None or parent_b is None:
		return None, None
	if parent_a.sex == 'male' and parent_b.sex == 'female':
		return parent_a, parent_b
	if parent_a.sex == 'female' and parent_b.sex == 'male':
		return parent_b, parent_a
	return None, None


#===============================
def _any_carrier(individuals: dict) -> bool:
	return any(person.phenotype == 'carrier' for person in individuals.values())


#===============================
def validate_x_linked_recessive_constraints(
	individuals: dict,
	couples: list,
	carriers_visible: bool | None = None,
) -> list:
	errors: list = []
	if carriers_visible is None:
		carriers_visible = _any_carrier(individuals)

	for person_id, person in individuals.items():
		if person.sex == 'male' and person.phenotype == 'carrier':
			errors.append(f"{person_id}: male carrier in XLR mode.")

	for couple, child_id in _iter_children(couples):
		father, mother = _get_parents(individuals, couple)
		child = individuals.get(child_id)
		if father is None or mother is None or child is None:
			continue

		if father.phenotype == 'affected' and child.sex == 'male' and child.phenotype == 'affected':
			errors.append(f"{child_id}: affected male with affected father (XLR).")

		if child.sex == 'female' and child.phenotype == 'affected' and father.phenotype != 'affected':
			errors.append(f"{child_id}: affected female without affected father (XLR).")

		if carriers_visible and child.phenotype == 'affected':
			if child.sex == 'male':
				if mother.phenotype not in ('carrier', 'affected'):
					errors.append(f"{child_id}: affected male with non-carrier mother (XLR).")
			elif child.sex == 'female':
				if mother.phenotype not in ('carrier', 'affected'):
					errors.append(f"{child_id}: affected female with non-carrier mother (XLR).")
		if carriers_visible:
			if father.phenotype == 'affected' and child.sex == 'female' and child.phenotype == 'unaffected':
				errors.append(f"{child_id}: unaffected female with affected father (XLR).")
			if mother.phenotype == 'affected' and child.phenotype == 'unaffected':
				errors.append(f"{child_id}: unaffected child with affected mother (XLR).")

	return errors


#===============================
def validate_x_linked_dominant_constraints(
	individuals: dict,
	couples: list,
) -> list:
	errors: list = []
	if _any_carrier(individuals):
		errors.append("XLD invalid: carrier phenotype present.")
		return errors

	for couple, child_id in _iter_children(couples):
		father, mother = _get_parents(individuals, couple)
		child = individuals.get(child_id)
		if father is None or mother is None or child is None:
			continue

		if father.phenotype == 'affected' and child.sex == 'male' and child.phenotype == 'affected':
			errors.append(f"{child_id}: affected male with affected father (XLD).")

		if father.phenotype == 'affected' and child.sex == 'female' and child.phenotype != 'affected':
			errors.append(f"{child_id}: unaffected female with affected father (XLD).")

		if child.sex == 'male' and child.phenotype == 'affected' and mother.phenotype != 'affected':
			errors.append(f"{child_id}: affected male with unaffected mother (XLD).")

		if (
			child.sex == 'female'
			and child.phenotype == 'affected'
			and father.phenotype != 'affected'
			and mother.phenotype != 'affected'
		):
			errors.append(f"{child_id}: affected female with unaffected parents (XLD).")

	return errors


#===============================
def validate_y_linked_constraints(
	individuals: dict,
	couples: list,
) -> list:
	errors: list = []
	for person_id, person in individuals.items():
		if person.phenotype == 'carrier':
			errors.append(f"{person_id}: carrier phenotype in Y-linked mode.")
		if person.sex == 'female' and person.phenotype == 'affected':
			errors.append(f"{person_id}: affected female in Y-linked mode.")

	for couple, child_id in _iter_children(couples):
		father, _ = _get_parents(individuals, couple)
		child = individuals.get(child_id)
		if father is None or child is None:
			continue
		if child.sex != 'male':
			continue
		if father.phenotype == 'affected' and child.phenotype != 'affected':
			errors.append(f"{child_id}: unaffected son of affected father (YL).")
		if father.phenotype != 'affected' and child.phenotype == 'affected':
			errors.append(f"{child_id}: affected son of unaffected father (YL).")

	return errors


#===============================
def validate_mode_keys(
	individuals: dict,
	couples: list,
	mode: str,
) -> list:
	"""
	Validate key evidence patterns for specific inheritance modes.

	Args:
		individuals (dict): Parsed individuals.
		couples (list): Parsed couples with children.
		mode (str): Inheritance mode.

	Returns:
		list: Validation errors.
	"""
	errors: list = []
	mode_value = mode.strip().lower()

	if mode_value in ('autosomal recessive', 'ar'):
		if not _has_recessive_key(individuals, couples):
			errors.append("Missing key: unaffected parents with affected child (AR).")

	if mode_value in ('autosomal dominant', 'ad'):
		if not _has_dominant_key(individuals, couples):
			errors.append("Missing key: affected parents with unaffected child (AD).")

	return errors


#===============================
def validate_mode_constraints(
	individuals: dict,
	couples: list,
	mode: str,
	carriers_visible: bool | None = None,
) -> list:
	"""
	Validate hard inheritance constraints for specific inheritance modes.
	"""
	mode_value = mode.strip().lower()

	if mode_value in ('x-linked recessive', 'xlr', 'xr'):
		return validate_x_linked_recessive_constraints(
			individuals,
			couples,
			carriers_visible=carriers_visible,
		)
	if mode_value in ('x-linked dominant', 'xld', 'xd'):
		return validate_x_linked_dominant_constraints(individuals, couples)
	if mode_value in ('y-linked', 'yl'):
		return validate_y_linked_constraints(individuals, couples)
	return []


#===============================
def validate_mode_keys_from_code(code_string: str, mode: str) -> list:
	"""
	Validate key evidence patterns for a code string.

	Args:
		code_string (str): Pedigree code string.
		mode (str): Inheritance mode.

	Returns:
		list: Validation errors.
	"""
	errors = validation.validate_code_string(code_string)
	if errors:
		return errors
	import mode_validate
	individuals, couples, _ = mode_validate.parse_pedigree_graph(code_string)
	return validate_mode_keys(individuals, couples, mode)


#===============================
def validate_mode_constraints_from_code(
	code_string: str,
	mode: str,
	carriers_visible: bool | None = None,
) -> list:
	"""
	Validate hard inheritance constraints for a code string.
	"""
	errors = validation.validate_code_string(code_string)
	if errors:
		return errors
	import mode_validate
	individuals, couples, detected_carriers = mode_validate.parse_pedigree_graph(code_string)
	carrier_flag = detected_carriers if carriers_visible is None else carriers_visible
	return validate_mode_constraints(individuals, couples, mode, carriers_visible=carrier_flag)


## THE END
