# TREELIB_TECH

This document summarizes treelib internals, data flow, and known sharp edges.

## Module map

Low level:
- treelib/definitions.py: base tree_code library and shape naming.
- treelib/tools.py: parsing, validation, distance maps, canonical sorting.
- treelib/permute.py: inner-node flips and taxa relabeling permutations.
- treelib/sorting.py: similarity scoring and sorting by distance maps.

Higher level:
- treelib/lookup.py: lookup tables, validation on import, and convenience wrappers.
- treelib/output.py: ASCII and HTML rendering for tree_code strings.
- treelib/treecodeclass.py: TreeCode class that binds code strings to metadata,
  distance maps, and rendering helpers.

## Data flow overview

Base tree codes are defined in treelib.definitions. On import, treelib.lookup:
- validates every base code with tools.validate_tree_code(base=True)
- builds name and leaf-count lookup maps
- checks library size against expected counts
- prints a short summary to stdout

Generation pipeline (high level):
1) Start from base tree_code strings (definitions).
2) Apply inner-node flips (permute.get_all_inner_node_permutations_from_tree_code).
3) Apply taxa permutations (tools.get_comb_safe_taxa_permutations plus
   tools.replace_taxa_letters).
4) Apply local canonical filtering (tools.is_gene_tree_alpha_sorted).
5) Deduplicate with set(...) and optionally wrap in TreeCode objects.

TreeCode.__init__ performs a final tools.sort_alpha_for_gene_tree normalization
and precomputes a taxa distance map for fast comparisons.

## Canonicalization and comparison

Canonicalization is local:
- tools.sort_alpha_for_gene_tree only swaps immediate letter neighbors of a node.
- tools.is_gene_tree_alpha_sorted only checks adjacent letters around each node.

Similarity is based on taxa distance maps:
- tools.generate_taxa_distance_map records the internal node number that joins
  each taxon pair.
- sorting.compare_taxa_distance_maps compares those maps and returns a [0, 1]
  score used by TreeCode and lookup.sort_treecodes_by_taxa_distances.

## Rendering internals

GeneTreeOutput renders in two steps:
1) make_char_tree_array builds a fixed-size grid:
   - rows = 2 * leaves - 1
   - cols = 3 * leaves + 3
   - line length = 3 * internal_node + 1
2) make_html_tree_array converts the char grid into a table of <td> cells.

get_html_from_tree_code validates HTML with tools.is_valid_html. Newlines are
rejected, so HTML output must stay on a single line.

## Performance and caching

Caching:
- tools uses lru_cache for common parsing utilities.
- lookup caches generated treecode lists in module globals for reuse.

Complexity:
- Full permutations grow rapidly with leaf count.
- permute.get_all_permutations_from_tree_code raises an error above 8 leaves.
- lookup prints warnings when asked to generate large sets.

## Known sharp edges

Single-digit node IDs:
- Internal node identifiers are single digits, so practical support is limited
  to at most 10 leaves (9 internal nodes). Many call sites use <= 8 leaves.

Multi-character taxa:
- replace_taxa_letters wraps multi-character taxa as |NAME|.
- tools.validate_tree_code does not accept pipes or multi-character taxa.
- Canonicalization is local and can skip ordering when pipes are present.
- GeneTreeOutput writes a single character per leaf in its grid, so multi-
  character taxa will not render as full names.

Stale function call:
- permute.get_all_permutations_from_tree_code calls tools.replace_gene_letters,
  which does not exist. This path will fail if invoked.
  Use lookup.get_all_taxa_permuted_tree_codes_for_leaf_count or
  permute.get_all_taxa_permuted_tree_codes_from_tree_code_list instead.

Import side effects:
- treelib.lookup prints a summary line on import. Avoid importing it at module
  top level if you need clean stdout.
