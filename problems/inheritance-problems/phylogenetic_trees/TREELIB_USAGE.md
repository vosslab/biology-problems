# TREELIB_USAGE

This guide shows how to use treelib to generate, label, compare, and render
phylogenetic tree codes in the inheritance problem generators.

## Quick start

Create a TreeCode from a base tree code and render it:

```python
from treelib import lookup

treecode_cls = lookup.get_random_base_tree_code_for_leaf_count(5)
treecode_cls.print_ascii_tree()
html_table = treecode_cls.get_html_table()
```

## Replace taxa labels

Replace the default taxa letters with a chosen order:

```python
from treelib import lookup

treecode_cls = lookup.get_random_base_tree_code_for_leaf_count(4)
ordered_taxa = ("A", "B", "C", "D")
replaced = lookup.replace_taxa_letters(treecode_cls, ordered_taxa)
html_table = replaced.get_html_table(caption=False)
```

Notes:
- ordered_taxa must match the number of leaves.
- Multi-character taxa are wrapped as |NAME|. This is intended for display and
  downstream logic, not for validate_tree_code.

## Tree permutations

Generate permutations of a base tree:

```python
from treelib import lookup

base = lookup.get_random_base_tree_code_for_leaf_count(5)
inner_node_perms = lookup.get_all_inner_node_permutations_from_tree_code(base)
random_perm = lookup.get_random_inner_node_permutation_from_tree_code(base)
```

Performance notes:
- lookup.get_all_permuted_tree_codes_for_leaf_count and
  lookup.get_all_taxa_permuted_tree_codes_for_leaf_count grow quickly.
- permute.get_all_permutations_from_tree_code raises an error above 8 leaves.

## Similarity and sorting

Sort candidate trees by similarity to an answer tree:

```python
from treelib import lookup

all_base = lookup.get_all_base_tree_codes_for_leaf_count(5)
answer = all_base[0]
sorted_list = lookup.sort_treecodes_by_taxa_distances(all_base[1:], answer)
```

The similarity score is based on the taxa distance map (see TREELIB_SPEC_v1).

## Rendering details

TreeCode.get_html_table returns a single-line HTML table. The validation step
rejects HTML containing newlines, so do not insert "\n" into the output.

If you need direct rendering control, use GeneTreeOutput:

```python
from treelib import output

tree_code_str = "((a1b)2c)"
renderer = output.GeneTreeOutput()
html_table = renderer.get_html_from_tree_code(tree_code_str)
```

## Import side effects

Importing treelib.lookup builds the base tree maps and prints a short summary to
stdout. If you need a quiet import, delay loading lookup until needed.

## Generator entry points

The treelib code is used by these generators:
- gene_tree_choice_plus.py (distance matrix to tree choice)
- gene_tree_matches_plus.py (find same or different tree)

Run them with --help to see current CLI flags:

```
python3 problems/inheritance-problems/phylogenetic_trees/gene_tree_choice_plus.py --help
python3 problems/inheritance-problems/phylogenetic_trees/gene_tree_matches_plus.py --help
```
