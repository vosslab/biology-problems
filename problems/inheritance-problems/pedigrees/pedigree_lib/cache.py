"""Local compact JSONL pedigree bank; drawing geometry is rebuilt on demand."""

import fcntl
import json
import pathlib
import random
import time
import contextlib
import collections.abc

import pedigree_lib.difficulty as difficulty
import pedigree_lib.family as family_model
import pedigree_lib.inheritance as inheritance
import pedigree_lib.questions as questions
import pedigree_lib.sources as sources

DEFAULT_DIRECTORY = pathlib.Path(__file__).resolve().parents[4] / 'output_pedigree_cache'
MAX_AGE_SECONDS = 24 * 60 * 60
MODES = dict(zip(('AD', 'AR', 'XD', 'XR', 'Y'), inheritance.MODES))


#============================================
def path_for_level(level: str, directory: pathlib.Path = DEFAULT_DIRECTORY) -> pathlib.Path:
	"""Keep each difficulty in its own independently expiring bank."""
	if level not in difficulty.DIFFICULTY_SETTINGS:
		raise ValueError(f'Unknown pedigree cache level: {level}')
	path = directory / f'pedigree_cache_{level}.jsonl'
	return path


#============================================
def record_key(record: dict) -> str:
	"""Identify exact records independently of JSON whitespace and dictionary order."""
	key = json.dumps(record, sort_keys=True, separators=(',', ':'))
	return key


#============================================
def encode(accepted: questions.AcceptedCase) -> dict:
	"""Store relationships and biological state without labels or geometry."""
	case = accepted.case
	indices = {person.id: index for index, person in enumerate(case.family.people)}
	mode = accepted.assessment.answer
	code = next(code for code, name in MODES.items() if name == mode)
	record = dict(mode=code,
		sex=''.join(person.sex[0] for person in case.family.people),
		affected=[indices[p.id] for p in case.family.people if case.observations[p.id].affected],
		carriers=[indices[p.id] for p in case.family.people
			if mode.endswith('recessive') and case.genotypes[p.id] == (0, 1)],
		families=[[indices[u.father], indices[u.mother], [indices[c] for c in u.children]]
			for u in case.family.unions])
	return record


#============================================
def decode(record: dict, level: str, matching: bool | None = None) -> sources.Case | None:
	"""Validate a compact record and recover a genotype witness, hiding carriers.

	Malformed records raise ValueError. Biologically incompatible records return None.
	Carrier lists constrain hidden genotypes, never the student-visible assessment.
	"""
	if not isinstance(record, dict) or set(record) != {
			'mode', 'sex', 'affected', 'carriers', 'families'}:
		raise ValueError('Pedigree cache records require mode, sex, affected, carriers, families')
	if level not in difficulty.DIFFICULTY_SETTINGS or record['mode'] not in MODES:
		raise ValueError('Unknown pedigree cache level or mode')
	sex = record['sex']
	if not isinstance(sex, str) or not sex or any(value not in 'mf' for value in sex):
		raise ValueError('Pedigree cache sex must be a nonempty string of m/f characters')
	for key in ('affected', 'carriers'):
		values = record[key]
		if (not isinstance(values, list)
				or any(type(index) is not int or not 0 <= index < len(sex) for index in values)
				or len(set(values)) != len(values)):
			raise ValueError(f'Invalid pedigree cache {key} indices')
	if set(record['affected']) & set(record['carriers']):
		raise ValueError('Pedigree carriers must be unaffected')
	mode = MODES[record['mode']]
	if record['carriers'] and not mode.endswith('recessive'):
		raise ValueError('Carrier status requires recessive inheritance')
	if not isinstance(record['families'], list):
		raise ValueError('Pedigree cache families must be a list')
	unions = []
	for row in record['families']:
		if not isinstance(row, list) or len(row) != 3 or not isinstance(row[2], list):
			raise ValueError('Each cached family requires father, mother, and children')
		if any(type(index) is not int or not 0 <= index < len(sex)
				for index in (row[0], row[1], *row[2])):
			raise ValueError('Invalid pedigree cache family indices')
		unions.append(family_model.Union(str(row[0]), str(row[1]), tuple(map(str, row[2]))))
	people = tuple(family_model.Person(str(i), 'male' if value == 'm' else 'female')
		for i, value in enumerate(sex))
	family = family_model.Family(people, tuple(unions))
	if matching is not None and not difficulty.fits_difficulty(family, level, matching):
		return None
	visible = {str(i): family_model.Observation(i in record['affected']) for i in range(len(sex))}
	carriers = frozenset(map(str, record['carriers']))
	if carriers & family_model.later_spouses(family):
		return None
	hidden = {pid: family_model.Observation(obs.affected, pid in carriers)
		for pid, obs in visible.items()}
	noncarriers = frozenset(pid for pid, obs in visible.items() if not obs.affected and pid not in carriers)
	witness = inheritance.analyze(family, hidden, mode, noncarrier_ids=noncarriers)
	if not witness.compatible:
		return None
	result = sources.Case(family, visible, witness.witness)
	return result


#============================================
@contextlib.contextmanager
def _locked(path: pathlib.Path) -> collections.abc.Iterator[None]:
	"""Use a stable lock file so deleting an expired bank cannot strand writers."""
	path.parent.mkdir(parents=True, exist_ok=True)
	with path.with_suffix(path.suffix + '.lock').open('a', encoding='utf-8') as lock:
		fcntl.flock(lock, fcntl.LOCK_EX)
		yield


#============================================
def _expire(path: pathlib.Path) -> None:
	"""Remove an expired bank while its separate lock is held."""
	if path.is_file() and time.time() - path.stat().st_mtime >= MAX_AGE_SECONDS:
		path.unlink()
		print(f'Deleted pedigree cache older than 24 hours: {path}')


#============================================
def read_records(path: pathlib.Path, fresh_only: bool = False) -> list[dict]:
	"""Read a locked snapshot, optionally deleting banks last updated 24 hours ago."""
	with _locked(path):
		if fresh_only:
			_expire(path)
		if not path.is_file():
			return []
		with path.open(encoding='utf-8') as stream:
			records = [json.loads(line) for line in stream if line.strip()]
	return records


#============================================
def append(path: pathlib.Path, pool: list[questions.AcceptedCase]) -> int:
	"""Append novel records to a current bank, recreating it if expired."""
	added = 0
	with _locked(path):
		_expire(path)
		with path.open('a+', encoding='utf-8') as stream:
			stream.seek(0)
			known = {record_key(json.loads(line)) for line in stream if line.strip()}
			for accepted in pool:
				record = encode(accepted)
				key = record_key(record)
				if key in known:
					continue
				stream.write(key + '\n')
				known.add(key)
				added += 1
	return added


#============================================
def candidates(path: pathlib.Path, rng: random.Random, level: str,
		matching: bool = False) -> collections.abc.Iterator[questions.AcceptedCase]:
	"""Randomly read distinct eligible entries, rechecking current acceptance rules."""
	records = read_records(path, fresh_only=True)
	rng.shuffle(records)
	seen = set()
	for record in records:
		key = record_key(record)
		if key in seen:
			continue
		seen.add(key)
		case = decode(record, level, matching)
		if case is None:
			continue
		accepted, reasons = questions.evaluate(case, mirror=rng.choice((False, True)))
		if accepted is not None and accepted.assessment.answer == MODES[record['mode']]:
			yield accepted
