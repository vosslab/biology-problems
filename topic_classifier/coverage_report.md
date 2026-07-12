# Multi-Subject Assignment Coverage Report

Date: 2026-07-12  
Runtime: `/opt/homebrew/opt/python@3.12/bin/python3.12` (Python 3.12.13)

## Frozen inventory

- 178 generator scripts
- 98 YAML banks
- 276 total frozen sources
- Inventory artifact: `topic_classifier/frozen_inventory.csv`
- The discovery result was stable across the unassigned reports and two
  consecutive validator runs.

Generator discovery uses `script_runner_lib.discover_generator_scripts()`.
YAML discovery covers `problems/multiple_choice_statements/*/*.yml` and
`problems/matching_sets/*/*.yml`.

For task-CSV purposes, a YAML concrete variant is the normalized
`(YMCS|YMATCH marker, input path)` pair. The task schema cannot address an
individual entry inside a bank; each bank was reviewed for coherent scope, and
no mixed bank requiring a source split was found.

## Curated result

- 414 non-empty assignment rows
- 0 uncovered generators
- 0 uncovered YAML banks
- 0 invalid subjects or chapters
- 0 chapter-routing failures
- Existing repeated identical rows preserved because they can intentionally
  control question frequency
- 0 source variants assigned to conflicting chapters in the same subject
- 159 additive assignments
  recorded in `topic_classifier/curation_change_report.csv`
- 0 unresolved ambiguity records

## Commands

```bash
source source_me.sh && /opt/homebrew/opt/python@3.12/bin/python3.12 \
  topic_classifier/validate_task_files.py -t topic_classifier/task_files \
  -i topic_classifier/frozen_inventory.csv

source source_me.sh && /opt/homebrew/opt/python@3.12/bin/python3.12 \
  topic_classifier/find_unassigned_scripts.py -t topic_classifier/task_files \
  -o /tmp/unassigned_scripts_after_manual.csv -l 0

source source_me.sh && /opt/homebrew/opt/python@3.12/bin/python3.12 \
  topic_classifier/find_unassigned_yaml.py -t topic_classifier/task_files \
  -o /tmp/unassigned_yaml_after_manual.csv -l 0
```

Existing JSONL and comparison artifacts were consulted only as supporting
evidence. No new automated subject or chapter classifications were generated.
Every baseline task-file row was preserved byte-for-byte; the website diff is
strictly additive.
