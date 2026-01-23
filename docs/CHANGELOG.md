# Changelog

## 2026-01-23
- Converted [problems/biochemistry-problems/which_hydrophobic-simple.py](../problems/biochemistry-problems/which_hydrophobic-simple.py) to self-contained PGML format as [problems/biochemistry-problems/which_hydrophobic-simple.pgml](../problems/biochemistry-problems/which_hydrophobic-simple.pgml).
- Fixed `NchooseK` undefined error in [problems/biochemistry-problems/which_hydrophobic-simple.pgml](../problems/biochemistry-problems/which_hydrophobic-simple.pgml) by adding `PGchoicemacros.pl` to the loadMacros list.
- Added concise two-sentence `BEGIN_PGML_HINT` to [problems/biochemistry-problems/which_hydrophobic-simple.pgml](../problems/biochemistry-problems/which_hydrophobic-simple.pgml) explaining that hydrophobic compounds are mostly carbon and hydrogen.
- Updated [source_me.sh](../source_me.sh) to add PGML linter (`pgml-lint`) to the environment setup, making it available as a shell function after sourcing the script.
- Enhanced [webwork_lib.py](../webwork_lib.py) to automatically populate OPL header fields (Date, Author, Institution) with default values when not specified in YAML files, affecting both [problems/multiple_choice_statements/yaml_mc_statements_to_pgml.py](../problems/multiple_choice_statements/yaml_mc_statements_to_pgml.py) and [problems/matching_sets/yaml_match_to_pgml.py](../problems/matching_sets/yaml_match_to_pgml.py).
- Fixed potential unbound variable bug in [webwork_lib.py](../webwork_lib.py) KEYWORDS handling by moving keyword_blob append inside the else block.
- Improved [devel/commit_changelog.py](../devel/commit_changelog.py) to generate descriptive commit messages that include the first change and count remaining changes instead of just "docs: update changelog for DATE".
- Created [devel/add_dbsubject_to_yaml.py](../devel/add_dbsubject_to_yaml.py) script to automatically add `dbsubject` metadata to YAML files based on folder location.
- Added `dbsubject` field to 51 YAML files in [problems/matching_sets/](../problems/matching_sets/) and 47 YAML files in [problems/multiple_choice_statements/](../problems/multiple_choice_statements/) using folder-based subject mapping (biochemistry→Biochemistry, inheritance→Genetics, laboratory→Laboratory Techniques, etc.).

## 2026-01-22
- Resolved merge conflicts in [docs/CODE_ARCHITECTURE.md](docs/CODE_ARCHITECTURE.md) and [docs/FILE_STRUCTURE.md](docs/FILE_STRUCTURE.md) to align test/tool references with the current repo layout.
- Standardized lxml etree imports in gene mapping and treelib HTML validation helpers after merge resolution.
- Removed legacy [problems/multiple_choice_statements/yaml_to_pg.py](../problems/multiple_choice_statements/yaml_to_pg.py) during conflict cleanup to match the current PGML workflow.
