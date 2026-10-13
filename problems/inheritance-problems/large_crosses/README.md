# Shared cross questions

`unique_counts.py` is the common executable. It asks about one parent's gametes,
offspring genotypes, or offspring phenotypes. The three mode flags are mutually
exclusive. Shared calculations and rendering live in `unique_counts_lib.py`;
`cross_table.py` supplies the existing blank worksheet tables.

From the repository root, create the two parents once:

```bash
source source_me.sh
cross_script=problems/inheritance-problems/large_crosses/unique_counts.py
python3 "$cross_script" --num-genes 4 --save-scenario cross.json
```

Then generate four questions from those exact parents:

```bash
python3 "$cross_script" --scenario cross.json --gametes --parent 1 --hint -c 5 -d 1
python3 "$cross_script" --scenario cross.json --gametes --parent 2 --hint -c 5 -d 1
python3 "$cross_script" --scenario cross.json --genotypes --hint -c 5 -d 1
python3 "$cross_script" --scenario cross.json --phenotypes --hint -c 5 -d 1
```

`--scenario` also accepts `-y` for the exam task runner's input column. The file
contains a `parents` list with two objects, each holding a plain-text `name` and
a `name_color` in `#RRGGBB` format, plus a `genotype` list such as
`["Aa", "BB", "Cc", "dd"]`. Both parents must use the
same loci in the same order. Gene count comes from the file when it is supplied;
`--num-genes` only controls newly generated scenarios. Answers are calculated
from the genotypes, not stored in JSON.

Name colors are selected once when the scenario is created, stored with each
parent, and reused in every question and worksheet. They can be edited in JSON.
Existing scenario files need a `name_color` field added to each parent, for example:

```json
{
  "parents": [
    {"name": "Eunbi", "name_color": "#9A4600", "genotype": ["Aa", "BB", "Cc", "dd"]},
    {"name": "Irena", "name_color": "#006B5E", "genotype": ["aa", "Bb", "Cc", "Dd"]}
  ]
}
```

Outcome terms have fixed colors: gametes dark green (`#006400`), genotypes dark
blue (`#003366`), and phenotypes dark orange (`#9A4600`). These apply to question
stems, hints, and worksheet labels.

Saving refuses to overwrite an existing scenario. Reading never changes the
parents; distractors can vary between runs. Without `--scenario`, each question
draws fresh parents. `--parent` applies only to gamete questions and defaults to 1.
Keep each generated question's heading and table when importing; instructors can
consolidate repeated material during layout review.

The existing `unique_gametes.py`, `unique_cross_genotypes.py`, and
`unique_cross_phenotypes.py` paths remain as thin homework entry points. They
call the same implementation and retain their original default gene counts.
