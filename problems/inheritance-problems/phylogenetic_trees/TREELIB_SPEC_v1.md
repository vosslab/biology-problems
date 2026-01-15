# TREELIB_SPEC_v1

This document defines the stable, external formats used by treelib:

1) tree_code strings (the compact phylogenetic tree encoding)
2) tree common names (human-readable identifiers for base shapes)

Internal classes (for example TreeCode and GeneTreeOutput) are implementation details
and are not part of this spec.

## 1) tree_code string (v1)

### Purpose
tree_code is a compact, fully parenthesized encoding of a rooted binary gene tree
with explicit internal node identifiers.

### Syntax
A tree_code is composed only of parentheses, taxa letters, and internal node digits.

Informal grammar:

- tree := "(" tree node tree ")" | taxon
- taxon := [A-Za-z] (single character)
- node := [1-9] (single digit)

Example:

((a1b)3(c2d))

### Core invariants
- tree_code must start with "(" and end with ")".
- Only parentheses, letters, and digits are allowed in v1.
- For n taxa, there are exactly n-1 internal nodes.
- Internal node identifiers are unique, consecutive digits "1" to "n-1".
- Taxa identifiers are unique letters.

### Base mode
Base tree codes are the canonical shapes stored in treelib.definitions.

Rules for base mode:
- Taxa are lowercase letters.
- Taxa are consecutive starting at "a" and appear in sorted order.
- Base codes are alpha-sorted (see below).

### Replacement mode
Replacement tree codes allow any single-letter alphabetic taxa (upper or lower case),
not necessarily consecutive. Replacement mode still uses the same node rules and
full parentheses.

### Alpha-sorted canonical form
treelib uses a local canonical rule for codes that have single-letter taxa adjacent
to a node:

For any internal node number N, if the immediate left and right characters are
letters, the left letter must be < the right letter.

tools.sort_alpha_for_gene_tree(tree_code) enforces this local rule.

## 2) Common names for base codes

treelib.definitions.code_library maps a common name to a base tree_code.

Naming convention:
- Prefix is the number of leaves (for example "5", "6", "7").
- Suffix is a shape label (for example "comb", "balanced", "giraffe", "twohead").
- Some shapes have numeric suffixes when multiple edge-labeled variants exist
  (for example "6balanced1", "6balanced2").

Lookup rules:
- lookup.get_tree_code_from_common_name(name) returns the base tree_code.
- lookup.get_common_name_from_tree_code(code) normalizes taxa and, for small trees,
  checks inner-node permutations to find the base name.

Library scope:
- For 2 to 6 leaves, the library contains all edge-labeled trees (Euler numbers).
- For 7+ leaves, the library contains one base code per tree type
  (Wedderburn-Etherington counts).

## 3) Taxa replacement format

tools.replace_taxa_letters(tree_code, ordered_taxa) replaces the default taxa
letters with a specified ordered list or tuple.

- ordered_taxa must have the same length as the number of leaves.
- Multi-character taxa are wrapped as |NAME| to avoid replacement collisions.

Example:

Base:
(((a1b)2c)3d)

Replacement taxa:
("W", "X", "Y", "Z")

Output:
(((W1X)2Y)3Z)

Note: pipe-wrapped multi-character taxa are intended for display and downstream
logic, not for validate_tree_code (which only accepts letters, digits, and
parentheses).

## 4) Distance map semantics

tools.generate_taxa_distance_map(tree_code) returns a dictionary mapping each
ordered taxon pair to the internal node number that connects them.

- For a pair (taxon1, taxon2), the distance is the highest internal node number
  between the two taxa in the tree_code string.
- Distances are integers from 1 to n-1.

Example:

tree_code: ((a1b)2c)

distance_map:
{("a", "b"): 1, ("a", "c"): 2, ("b", "c"): 2}
