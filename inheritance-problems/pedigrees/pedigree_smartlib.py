#!/usr/bin/env python3

# Standard Library
import dataclasses
import random

# Local repo modules
import pedigree_code_lib
import pedigree_code_strings


#===============================
@dataclasses.dataclass
class PedigreeTemplate:
	mode: str
	code: str
	generations: int
	skeleton_id: str | None = None
	notes: str | None = None


#===============================
MODE_ALIASES = {
	'ad': 'autosomal dominant',
	'ar': 'autosomal recessive',
	'xd': 'x-linked dominant',
	'xr': 'x-linked recessive',
	'yl': 'y-linked',
}

VALID_MODES = (
	'autosomal dominant',
	'autosomal recessive',
	'x-linked dominant',
	'x-linked recessive',
	'y-linked',
)


#===============================
def normalize_mode(mode: str) -> str:
	"""
	Normalize a user-supplied mode to the canonical name.

	Args:
		mode (str): Mode input (aliases allowed).

	Returns:
		str: Canonical mode name.
	"""
	mode_clean = mode.strip().lower()
	mode_value = MODE_ALIASES.get(mode_clean, mode_clean)
	if mode_value not in VALID_MODES:
		raise ValueError(f"Unknown mode '{mode}'. Choose from: {', '.join(VALID_MODES)}")
	return mode_value


#===============================
#===============================
def build_templates() -> list[PedigreeTemplate]:
	"""
	Build PedigreeTemplate objects from the static code string lists.

	Returns:
		list[PedigreeTemplate]: Templates with derived generation counts.
	"""
	templates: list[PedigreeTemplate] = []
	mode_lists = {
		'autosomal dominant': pedigree_code_strings.autosomal_dominant,
		'autosomal recessive': pedigree_code_strings.autosomal_recessive,
		'x-linked dominant': pedigree_code_strings.x_linked_dominant,
		'x-linked recessive': pedigree_code_strings.x_linked_recessive,
		'y-linked': pedigree_code_strings.y_linked,
	}
	for mode_name, code_list in mode_lists.items():
		for code in code_list:
			generations = pedigree_code_lib.count_generations(code)
			template = PedigreeTemplate(
				mode=mode_name,
				code=code,
				generations=generations,
				skeleton_id=None,
				notes=None,
			)
			templates.append(template)
	return templates


#===============================
PEDIGREE_TEMPLATES = build_templates()


#===============================
def get_templates(mode: str | None = None, generations: int | None = None) -> list[PedigreeTemplate]:
	"""
	Fetch templates filtered by mode and optional generation count.

	Args:
		mode (str | None): Inheritance mode to match.
		generations (int | None): Generation count to match.

	Returns:
		list[PedigreeTemplate]: Filtered templates.
	"""
	templates = PEDIGREE_TEMPLATES
	if mode is not None:
		mode_value = normalize_mode(mode)
		templates = [template for template in templates if template.mode == mode_value]
	if generations is not None:
		templates = [template for template in templates if template.generations == generations]
	return templates


#===============================
def choose_template(mode: str, generations: int | None = None, rng: random.Random | None = None) -> PedigreeTemplate:
	"""
	Choose a pedigree template for a given mode and generation count.

	Args:
		mode (str): Inheritance mode.
		generations (int | None): Desired generation count.
		rng (random.Random | None): Optional RNG for deterministic selection.

	Returns:
		PedigreeTemplate: Selected template.
	"""
	candidates = get_templates(mode, generations)
	if not candidates:
		available = sorted({template.generations for template in get_templates(mode)})
		available_text = ", ".join(str(value) for value in available) or "none"
		raise ValueError(
			f"No templates for mode '{mode}' with generations={generations}. "
			f"Available generations: {available_text}"
		)
	if rng is None:
		rng = random.Random()
	template = rng.choice(candidates)
	return template


#===============================
def make_pedigree_code(
	mode: str,
	generations: int | None = 4,
	allow_mirror: bool = True,
	rng: random.Random | None = None,
) -> str:
	"""
	Select a template and return the pedigree code string.

	Args:
		mode (str): Inheritance mode.
		generations (int | None): Desired generation count (default 4).
		allow_mirror (bool): Whether to mirror the pedigree randomly.
		rng (random.Random | None): Optional RNG for deterministic selection.

	Returns:
		str: Pedigree code string.
	"""
	if rng is None:
		rng = random.Random()
	template = choose_template(mode, generations, rng)
	code_string = template.code
	if allow_mirror and rng.random() < 0.5:
		code_string = pedigree_code_lib.mirror_pedigree(code_string)
	return code_string


#===============================
#===============================
def make_matching_set_codes(
	modes: list[str],
	generations: int | None = 4,
	allow_mirror: bool = True,
	rng: random.Random | None = None,
) -> list[str]:
	"""
	Make a list of pedigree code strings for matching questions.

	Args:
		modes (list[str]): Inheritance modes to include (one per panel).
		generations (int | None): Desired generation count (default 4).
		allow_mirror (bool): Whether to mirror each pedigree randomly.
		rng (random.Random | None): Optional RNG for deterministic selection.

	Returns:
		list[str]: Code strings for each pedigree panel.
	"""
	if rng is None:
		rng = random.Random()
	code_strings: list[str] = []
	for mode in modes:
		code_string = make_pedigree_code(mode, generations, allow_mirror, rng)
		code_strings.append(code_string)
	return code_strings


#===============================
#===============================
if __name__ == '__main__':
	default_rng = random.Random(7)
	code_string = make_pedigree_code('x-linked recessive', generations=4, rng=default_rng)
	print(code_string)

## THE END
