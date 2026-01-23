# Changelog

## 2026-01-23
- Converted [problems/biochemistry-problems/which_hydrophobic-simple.py](../problems/biochemistry-problems/which_hydrophobic-simple.py) to self-contained PGML format as [problems/biochemistry-problems/which_hydrophobic-simple.pgml](../problems/biochemistry-problems/which_hydrophobic-simple.pgml).
- Fixed `NchooseK` undefined error in [problems/biochemistry-problems/which_hydrophobic-simple.pgml](../problems/biochemistry-problems/which_hydrophobic-simple.pgml) by adding `PGchoicemacros.pl` to the loadMacros list.
- Added concise two-sentence `BEGIN_PGML_HINT` to [problems/biochemistry-problems/which_hydrophobic-simple.pgml](../problems/biochemistry-problems/which_hydrophobic-simple.pgml) explaining that hydrophobic compounds are mostly carbon and hydrogen.
- Updated [source_me.sh](../source_me.sh) to add PGML linter (`pgml-lint`) to the environment setup, making it available as a shell function after sourcing the script.

## 2026-01-22
- Resolved merge conflicts in [docs/CODE_ARCHITECTURE.md](docs/CODE_ARCHITECTURE.md) and [docs/FILE_STRUCTURE.md](docs/FILE_STRUCTURE.md) to align test/tool references with the current repo layout.
- Standardized lxml etree imports in gene mapping and treelib HTML validation helpers after merge resolution.
- Removed legacy [problems/multiple_choice_statements/yaml_to_pg.py](../problems/multiple_choice_statements/yaml_to_pg.py) during conflict cleanup to match the current PGML workflow.
