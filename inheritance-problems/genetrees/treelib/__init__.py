"""
*-- __init__.py (module)
*-- definitions.py (module)
*-- lookup.py (module)
  |-- get_common_name_from_tree_code (function)
  |-- get_tree_code_from_common_name (function)
  |-- get_random_base_tree_code_for_leaf_count (function)
  |-- get_all_base_tree_codes_for_leaf_count (function)
  *-- get_all_permuted_tree_codes_for_leaf_count (function)
*-- output.py (module)
  *-- GeneTreeOutput (class)
    |-- __init__ (function)
    |-- create_empty_char_tree_array (function)
    |-- make_char_tree_array (function)
    |-- internal_node_number_to_line_length (function)
    |-- get_internal_node_for_taxon (function)
    |-- print_ascii_tree (function)
    |-- get_gene_name_td_cell (function)
    |-- get_td_cell (function)
    |-- make_html_tree_array (function)
    |-- format_array_into_html_table (function)
    *-- get_html_from_tree_code (function)
*-- permute.py (module)
  |-- _flip_tree_code (function)
  |-- _get_left_of_node (function)
  |-- _get_right_of_node (function)
  |-- _flip_node_in_code (function)
  |-- _permute_code_by_node (function)
  |-- _permute_code_by_node_binary (function)
  |-- _convert_int_to_binary_list (function)
  |-- get_all_alpha_sorted_code_rotation_permutations (function)
  |-- get_all_code_permutations (function)
  |-- get_random_code_permutation (function)
  *-- get_random_even_code_permutation (function)
*-- sorting.py (module)
  |-- get_highest_number (function)
  |-- find_node_number_for_taxa_pair (function)
  |-- generate_taxa_distance_map (function)
  |-- compare_taxa_distance_maps (function)
  |-- compare_tree_codes (function)
  |-- tree_codes_match (function)
  *-- sort_tree_codes_by_taxa_distances (function)
*-- test_filter.py (module)
  |-- utf8_array_replace (function)
  *-- match_and_replace (function)
*-- tools.py (module)
  |-- expected_number_of_tree_types_for_leaf_count (function)
  |-- expected_number_of_edge_labeled_trees_for_leaf_count (function)
  |-- get_comb_safe_taxa_permutations (function)
  |-- code_to_taxa_list (function)
  |-- code_to_number_of_taxa (function)
  |-- reset_sort_taxa_in_code (function)
  |-- code_to_internal_node_list (function)
  |-- code_to_number_of_internal_nodes (function)
  |-- is_gene_tree_alpha_sorted (function)
  |-- sort_alpha_for_gene_tree (function)
  |-- replace_gene_letters (function)
  |-- check_matching_parens (function)
  |-- validate_tree_code_by_reduction (function)
  |-- validate_tree_code (function)
  *-- is_valid_html (function)
*-- treecodeclass.py (module)
  *-- TreeCode (class)
    |-- __init__ (function)
    |-- _compute_similarity_to_base_comb (function)
    |-- compare_to (function)
    |-- __lt__ (function)
    |-- __eq__ (function)
    |-- get_html_tree (function)
    *-- print_ascii_tree (function)
"""
