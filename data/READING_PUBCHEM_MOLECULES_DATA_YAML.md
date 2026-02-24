# Reading pubchem_molecules_data.yml

This guide explains how to read and use:

- `data/pubchem_molecules_data.yml`

This YAML file is a local PubChem cache used by the PubChem generators in:

- `problems/biochemistry-problems/PUBCHEM/`

The most important reader/writer is:

- `problems/biochemistry-problems/PUBCHEM/pubchemlib.py`

## What this file contains

`pubchem_molecules_data.yml` has three top-level keys:

- `cid_to_data`: map of PubChem CID -> molecule data dictionary
- `name_to_cid`: map of normalized molecule name -> PubChem CID
- `time_stamp`: unix epoch seconds when cache was last saved

Example shape:

```yaml
cid_to_data:
  750:
    Abbreviation: glycine
    CID: 750
    Full name: glycine
    Partition coefficient: -3.2
    Molecular formula: C2H5NO2
    Molecular weight: 75.07
    SMILES: C(C(=O)O)N
name_to_cid:
  glycine: 750
time_stamp: 1770126222
```

## Molecule record fields

Each `cid_to_data` entry is expected by `PubChemLib` to have exactly 7 keys:

- `Abbreviation`
- `CID`
- `Full name`
- `Partition coefficient`
- `Molecular formula`
- `Molecular weight`
- `SMILES`

In `pubchemlib.py`, this is enforced by `expected_molecule_data_keys = 7` before returning cached records.

## Recommended way to read data in programs

Prefer using `PubChemLib` instead of manual YAML parsing. It handles:

- name normalization (`lower().strip()`)
- CID lookup cache (`name_to_cid`)
- molecule data cache (`cid_to_data`)
- API fallback and cache persistence

Example:

```python
#!/usr/bin/env python3

import pubchemlib

pcl = pubchemlib.PubChemLib()
try:
	mol = pcl.get_molecule_data_dict("glycine")
	if mol is None:
		print("not found")
	else:
		print(mol["CID"], mol["Molecular formula"], mol["SMILES"])
finally:
	pcl.close()
```

## Direct YAML reading (when you do not want API calls)

If you only need offline reads, parse YAML directly.

```python
#!/usr/bin/env python3

import yaml

with open("data/pubchem_molecules_data.yml", "r") as f:
	pubchem_data = yaml.safe_load(f)

cid_to_data = pubchem_data.get("cid_to_data", {})
name_to_cid = pubchem_data.get("name_to_cid", {})

name = "glycine".lower().strip()
cid = name_to_cid.get(name)
if cid is None:
	print("name not in cache")
else:
	mol_data = cid_to_data.get(cid)
	if mol_data is None:
		print("cid not in cache map")
	else:
		print(mol_data["Full name"], mol_data["Molecular weight"])
```

This is the same lookup pattern used in:

- `problems/biochemistry-problems/PUBCHEM/MACROMOLECULE_CATEGORIZE/generate_macromolecule_id_pgml.py`

## Important details and gotchas

- Use lowercase trimmed names when reading `name_to_cid`.
- Some names are synonyms pointing to the same CID.
- `Partition coefficient` can be `null` for some molecules.
- `time_stamp` is cache metadata, not molecule metadata.
- Keep key names exact (including spaces and capitalization) when reading records.

## When the cache updates

`PubChemLib` updates this file when new lookups are fetched from PubChem and `close()` is called. The write path is controlled by:

- `bptools.get_repo_data_path("pubchem_molecules_data.yml")`

So scripts in different folders still write to the same shared repo cache.
