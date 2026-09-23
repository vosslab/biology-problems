# Question-Creator Function Index

This file lists key functions that create quiz/homework questions (or question items) and the date they first appeared in Git history.

- Source: `tools/build_question_function_index.py`
- Git HEAD: `6da6ad1` (2026-09-22)
- Date source: earliest commit that introduces `def <name>` in that file (`git log --follow -G ...`)
- Also shown: file birth date (`git log --follow --diff-filter=A`)
- Fallbacks: `git blame` on the `def ...` line; uncommitted/untracked files use file mtime (commit `WORKTREE`)
- YAML-driven banks are tracked separately in `docs/YAML_QUESTION_BANK_INDEX.md`.

## 2026-09-23
- 2026-09-23 - `problems/inheritance-problems/horse_coat_pattern_inference.py:175` - `write_question` (commit `WORKTREE`)
## 2026-09-22
- 2026-09-22 - `problems/molecular_biology-problems/complementary_sequences.py:167` - `write_prime_mc_question` (commit `730869d028`) - file 2023-10-31 (commit `198f957169`)
- 2026-09-22 - `problems/molecular_biology-problems/complementary_sequences.py:71` - `write_directionless_mc_question` (commit `730869d028`) - file 2023-10-31 (commit `198f957169`)
## 2026-09-20
- 2026-09-20 - `problems/molecular_biology-problems/restriction_enzymes/circular_digest.py:295` - `write_question` (commit `479ccce7a3`) - "Create one circular restriction-digest gel-band question."
## 2026-07-12
- 2026-07-12 - `problems/molecular_biology-problems/dna_melting_temp.py:67` - `write_question` (commit `4e164afa7d`) - file 2021-10-25 (commit `21799f9051`)
- 2026-07-12 - `problems/biochemistry-problems/electrophoresis/kaleidoscope_ladder/kaleidoscope_ladder_mapping.py:46` - `write_prelim_mapping_question` (commit `3ae8744372`) - file 2026-01-04 (commit `a36bce137d`)
## 2026-05-07
- 2026-05-07 - `problems/biochemistry-problems/PUBCHEM/PEPTIDES/tetrapeptide_net_charge.py:324` - `write_question` (commit `6b62ff7dbe`)
- 2026-05-07 - `problems/biochemistry-problems/PUBCHEM/PEPTIDES/tetrapeptide_net_charge.py:296` - `generate_complete_question` (commit `6b62ff7dbe`) - "Generate one complete tetrapeptide net-charge question."
## 2026-04-22
- 2026-04-22 - `problems/biochemistry-problems/lipids/fatty_acid_naming_omega.py:59` - `write_question` (commit `1df8134b78`) - "Generate one omega-notation MC question."
- 2026-04-22 - `problems/biochemistry-problems/lipids/fatty_acid_naming_delta.py:57` - `write_question` (commit `1df8134b78`) - "Generate one Delta-notation MC question."
- 2026-04-22 - `problems/biochemistry-problems/lipids/fatty_acid_match_omega.py:99` - `write_question` (commit `1df8134b78`) - "Generate one match-omega-to-structure MC question."
- 2026-04-22 - `problems/biochemistry-problems/lipids/fatty_acid_match_delta.py:89` - `write_question` (commit `1df8134b78`) - "Generate one match-Delta-to-structure MC question."
- 2026-04-22 - `problems/biochemistry-problems/PUBCHEM/NUCLEOBASES/match_pyrimidine_structures.py:60` - `write_question` (commit `28dbfaddc4`)
- 2026-04-22 - `problems/biochemistry-problems/PUBCHEM/NUCLEOBASES/match_purine_structures.py:59` - `write_question` (commit `28dbfaddc4`)
## 2026-03-30
- 2026-03-30 - `problems/biochemistry-problems/enzymes/michaelis_menten_table-inhibition.py:88` - `make_complete_problem` (commit `d1a1ded352`) - file 2021-10-20 (commit `57f8de01ea`) - "Build a complete MC question asking students to identify the inhibition type."
- 2026-03-30 - `problems/biochemistry-problems/enzymes/michaelis_menten_table-Km.py:16` - `make_complete_problem` (commit `d1a1ded352`) - file 2021-10-20 (commit `57f8de01ea`) - "Build a complete MC question asking students to determine Km from a table."
- 2026-03-30 - `problems/biochemistry-problems/enzymes/metabolic_pathway_allosteric.py:12` - `write_question` (commit `6c4ea7cbb6`) - file 2022-03-18 (commit `9c8694df5c`) - "Create an MC question about which enzyme is most likely allosteric."
- 2026-03-30 - `problems/biochemistry-problems/enzymes/feedback_merging_pathway.py:535` - `write_question` (commit `ed3ab6bb25`) - "Creates a formatted MC question about coordination in a merging pathway."
## 2026-03-27
- 2026-03-27 - `problems/biochemistry-problems/enzymes/hemoglobin_oxygen_affinity.py:109` - `write_question` (commit `72687ecede`) - "Creates a complete formatted MC question about hemoglobin oxygen affinity."
- 2026-03-27 - `problems/biochemistry-problems/enzymes/feedback_splitting_pathway.py:381` - `write_question` (commit `72687ecede`) - "Creates a formatted MC question about feedback splitting in a branched pathway."
- 2026-03-27 - `problems/biochemistry-problems/enzymes/allosteric_enzyme_models.py:85` - `write_question` (commit `72687ecede`) - "Creates a complete formatted MC question for allosteric enzyme model identification."
## 2026-02-25
- 2026-02-25 - `problems/biochemistry-problems/thermodynamics/thermodynamics_system_laws.py:92` - `write_question` (commit `5efb08dc11`) - "Create a complete formatted MC question about thermodynamic"
- 2026-02-25 - `problems/biochemistry-problems/thermodynamics/thermodynamics_law_statements.py:42` - `write_question` (commit `5efb08dc11`) - "Create a complete formatted MC question about identifying"
- 2026-02-25 - `problems/biochemistry-problems/thermodynamics/gibbs_free_energy_equation_symbols.py:39` - `write_question` (commit `5efb08dc11`) - "Create a complete formatted matching question for Gibbs free energy"
- 2026-02-25 - `problems/biochemistry-problems/thermodynamics/free_energy_keq_relationship.py:118` - `write_question` (commit `5efb08dc11`) - "Create a complete formatted MC question."
- 2026-02-25 - `problems/biochemistry-problems/thermodynamics/exergonic_endergonic_reactions.py:149` - `write_question` (commit `5efb08dc11`) - "Create a complete formatted MC question about exergonic/endergonic"
- 2026-02-25 - `problems/biochemistry-problems/thermodynamics/delta_g_prime_standard_state.py:69` - `write_question` (commit `5efb08dc11`) - "Create a complete formatted MC question about standard vs biochemical"
## 2026-02-12
- 2026-02-12 - `problems/biochemistry-problems/electrophoresis/titration_pI.py:367` - `write_question` (commit `cec291ced1`) - "Generate one pI calculation question with tiles and titration curve."
## 2026-02-11
- 2026-02-11 - `problems/biochemistry-problems/electrophoresis/kaleidoscope_ladder/kaleidoscope_ladder_unknown_band.py:494` - `write_question` (commit `6bd693f40b`)
- 2026-02-11 - `problems/biochemistry-problems/electrophoresis/kaleidoscope_ladder/kaleidoscope_ladder_mapping.py:130` - `write_question` (commit `6bd693f40b`) - file 2026-01-04 (commit `a36bce137d`)
## 2026-02-04
- 2026-02-04 - `problems/biochemistry-problems/PUBCHEM/AMINO_ACIDS/histidine_protonation_states.py:167` - `write_question` (commit `a7c8370d91`) - "Generate one histidine protonation-state question."
- 2026-02-04 - `problems/biochemistry-problems/PUBCHEM/AMINO_ACIDS/alanine_protonation_states.py:146` - `write_question` (commit `a7c8370d91`) - "Generate one alanine protonation-state question."
## 2026-02-03
- 2026-02-03 - `problems/biochemistry-problems/PUBCHEM/AMINO_ACIDS/alpha_amino_acid_identification.py:117` - `write_question` (commit `8b69c6f844`) - "Create a complete formatted question."
## 2026-01-28
- 2026-01-28 - `problems/biochemistry-problems/buffers/ph_h_concentration_ratio.py:151` - `write_question` (commit `9bd05cf2e0`) - "Create a complete formatted question."
- 2026-01-28 - `problems/biochemistry-problems/buffers/functional_groups_bond_types.py:134` - `write_question` (commit `9bd05cf2e0`) - "Create a complete formatted question."
- 2026-01-28 - `problems/biochemistry-problems/buffers/chemical_group_pka_forms.py:92` - `write_question` (commit `9bd05cf2e0`) - file 2026-02-02 (commit `1020a45296`) - "Create a complete formatted question."
- 2026-01-28 - `problems/biochemistry-problems/PUBCHEM/AMINO_ACIDS/which_amino_acid.py:57` - `write_question` (commit `435f6dfaac`) - file 2024-01-26 (commit `2479070cbc`)
- 2026-01-28 - `problems/biochemistry-problems/PUBCHEM/AMINO_ACIDS/match_amino_acid_structures.py:49` - `write_question` (commit `435f6dfaac`) - file 2024-01-26 (commit `2479070cbc`)
## 2026-01-11
- 2026-01-11 - `problems/inheritance-problems/pedigrees/write_pedigree_match_random.py:194` - `write_question` (commit `d59c5f0910`) - file 2026-01-10 (commit `962b4f9e5e`) - "Generate a single pedigree matching question with fresh random pedigrees."
- 2026-01-11 - `problems/inheritance-problems/pedigrees/write_pedigree_choice.py:29` - `write_question` (commit `d59c5f0910`) - file 2021-10-31 (commit `cf9a40554c`)
- 2026-01-11 - `problems/inheritance-problems/gene_mapping/three-point_test_cross-which_genotypes.py:66` - `write_question` (commit `d59c5f0910`) - file 2020-11-24 (commit `b7e09b97ac`)
- 2026-01-11 - `problems/inheritance-problems/gene_mapping/three-point_test_cross-one_gene_distance.py:60` - `write_question` (commit `d59c5f0910`) - file 2020-11-24 (commit `b7e09b97ac`)
- 2026-01-11 - `problems/inheritance-problems/gene_mapping/three-point_test_cross-find_interence.py:286` - `write_question` (commit `d59c5f0910`) - file 2023-11-06 (commit `265718c413`)
- 2026-01-11 - `problems/inheritance-problems/gene_mapping/three-point_test_cross-distances_plus.py:76` - `write_question` (commit `d59c5f0910`) - file 2020-11-24 (commit `b7e09b97ac`)
- 2026-01-11 - `problems/inheritance-problems/gene_mapping/tetrad_unordered_two_gene-test_linkage.py:296` - `write_question` (commit `d59c5f0910`) - file 2021-11-09 (commit `22d94705bd`)
- 2026-01-11 - `problems/inheritance-problems/gene_mapping/tetrad_unordered_two_gene-find_distance.py:352` - `write_question` (commit `d59c5f0910`) - file 2021-11-09 (commit `22d94705bd`)
- 2026-01-11 - `problems/inheritance-problems/gene_mapping/tetrad_unordered_three_gene-find_one_distance.py:243` - `write_question` (commit `d59c5f0910`) - file 2020-11-26 (commit `d3e24ca76e`)
- 2026-01-11 - `problems/inheritance-problems/gene_mapping/tetrad_unordered_three_gene-distances_plus.py:174` - `write_question` (commit `d59c5f0910`) - file 2020-11-26 (commit `d3e24ca76e`)
- 2026-01-11 - `problems/biochemistry-problems/enzymes/michaelis_menten_table-inhibition.py:176` - `write_question` (commit `7054183a39`) - file 2021-10-20 (commit `57f8de01ea`) - "Create a formatted MC question for inhibition type identification."
- 2026-01-11 - `problems/biochemistry-problems/enzymes/michaelis_menten_table-Km.py:86` - `write_question` (commit `7054183a39`) - file 2021-10-20 (commit `57f8de01ea`) - "Create a formatted MC question for Km determination from a table."
- 2026-01-11 - `problems/biochemistry-problems/carbs/D_to_L_Haworth_configuration.py:130` - `write_question` (commit `7054183a39`) - file 2021-10-20 (commit `57f8de01ea`)
- 2026-01-11 - `problems/biochemistry-problems/carbs/D_to_L_Haworth_configuration.py:32` - `write_haworth_question` (commit `7054183a39`) - file 2021-10-20 (commit `57f8de01ea`)
- 2026-01-11 - `problems/biochemistry-problems/carbs/D_to_L_Fischer_configuration.py:155` - `write_question` (commit `7054183a39`) - file 2020-10-28 (commit `79f564930d`)
- 2026-01-11 - `problems/biochemistry-problems/carbs/D_to_L_Fischer_configuration.py:14` - `write_fischer_question` (commit `7054183a39`) - file 2020-10-28 (commit `79f564930d`)
## 2026-01-10
- 2026-01-10 - `problems/biochemistry-problems/buffers/Henderson-Hasselbalch.py:515` - `_write_ratio_question` (commit `962b4f9e5e`) - file 2024-11-02 (commit `450cfb15cf`)
- 2026-01-10 - `problems/biochemistry-problems/buffers/Henderson-Hasselbalch.py:459` - `_write_pK_question` (commit `962b4f9e5e`) - file 2024-11-02 (commit `450cfb15cf`)
- 2026-01-10 - `problems/biochemistry-problems/buffers/Henderson-Hasselbalch.py:374` - `_write_pH_question` (commit `962b4f9e5e`) - file 2024-11-02 (commit `450cfb15cf`)
## 2026-01-05
- 2026-01-05 - `problems/inheritance-problems/translocation/robertsonian.py:79` - `write_question` (commit `9ec6038c42`) - file 2020-12-04 (commit `f02ddfe4fa`)
- 2026-01-05 - `problems/inheritance-problems/punnett_choice.py:175` - `write_question` (commit `9ec6038c42`) - file 2025-08-07 (commit `e981f49c30`)
- 2026-01-05 - `problems/inheritance-problems/punnett_choice.py:148` - `_format_question` (commit `9ec6038c42`) - file 2025-08-07 (commit `e981f49c30`) - "Creates a complete formatted question for output."
- 2026-01-05 - `problems/inheritance-problems/polyploid/polyploid-gametes.py:110` - `write_question` (commit `9ec6038c42`) - file 2021-11-24 (commit `d40f13f443`)
- 2026-01-05 - `problems/inheritance-problems/phylogenetic_trees/gene_tree_matches_plus.py:265` - `write_question` (commit `412a14fd19`) - file 2021-11-18 (commit `26236438db`) - "Generate a phylogenetic question based on the specified mode."
- 2026-01-05 - `problems/inheritance-problems/phylogenetic_trees/gene_tree_matches_plus.py:198` - `find_same_question` (commit `412a14fd19`) - file 2021-11-18 (commit `26236438db`) - "Generate a question asking students to identify the same phylogenetic tree."
- 2026-01-05 - `problems/inheritance-problems/phylogenetic_trees/gene_tree_matches_plus.py:125` - `find_diff_question` (commit `412a14fd19`) - file 2021-11-18 (commit `26236438db`) - "Generate a question asking students to identify the different phylogenetic tree."
- 2026-01-05 - `problems/inheritance-problems/phylogenetic_trees/gene_tree_choice_plus.py:522` - `write_question` (commit `412a14fd19`) - file 2021-11-18 (commit `b32382f761`) - "Wrapper for the shared question writer interface."
- 2026-01-05 - `problems/inheritance-problems/phylogenetic_trees/gene_tree_choice_plus.py:427` - `make_question` (commit `412a14fd19`) - file 2021-11-18 (commit `b32382f761`) - "Generate a multiple-choice question about gene trees based on a distance matrix."
- 2026-01-05 - `problems/inheritance-problems/gene_mapping/two-point_test_cross-which_genotypes.py:25` - `write_question` (commit `d30f49fc44`) - file 2023-11-05 (commit `4d0e14d53a`)
- 2026-01-05 - `problems/inheritance-problems/gene_mapping/two-point_test_cross-distance.py:60` - `generate_question` (commit `d30f49fc44`) - file 2020-11-24 (commit `b7e09b97ac`) - "Generates a formatted question string based on the type."
- 2026-01-05 - `problems/inheritance-problems/gene_mapping/two-point_test_cross-cis-trans.py:21` - `write_question` (commit `d30f49fc44`) - file 2023-11-05 (commit `4d0e14d53a`)
- 2026-01-05 - `problems/inheritance-problems/blood_type_offspring.py:95` - `write_question` (commit `9ec6038c42`) - file 2020-10-16 (commit `ef7ed68de4`)
- 2026-01-05 - `problems/inheritance-problems/blood_type_mother.py:156` - `write_question` (commit `9ec6038c42`) - file 2020-10-16 (commit `6e9f213024`)
- 2026-01-05 - `problems/inheritance-problems/blood_type_mother.py:109` - `_format_question` (commit `9ec6038c42`) - file 2020-10-16 (commit `6e9f213024`) - "Generate a formatted multiple-answer question string."
- 2026-01-05 - `problems/biostatistics-problems/busse_woods_two_sample_f_test.py:266` - `write_question` (commit `9ec6038c42`) - file 2025-10-20 (commit `654cc1465b`)
- 2026-01-05 - `problems/biostatistics-problems/busse_woods_two_sample_f_test.py:199` - `_write_one_question` (commit `9ec6038c42`) - file 2025-10-20 (commit `654cc1465b`) - "Create one Blackboard numeric question row for an F-test of variances."
- 2026-01-05 - `problems/biostatistics-problems/busse_woods_anova.py:305` - `write_question` (commit `9ec6038c42`) - file 2025-12-28 (commit `d484513fdb`)
- 2026-01-05 - `problems/biostatistics-problems/busse_woods_anova.py:225` - `_write_one_question` (commit `9ec6038c42`) - file 2025-12-28 (commit `d484513fdb`) - "Create one Blackboard numeric question row for ANOVA across 5 years"
- 2026-01-05 - `problems/biostatistics-problems/boxplot_from_unsorted_even.py:127` - `write_question` (commit `a1562c122f`)
- 2026-01-05 - `problems/biostatistics-problems/boxplot_from_summary.py:89` - `write_question` (commit `a1562c122f`)
- 2026-01-05 - `problems/biostatistics-problems/boxplot_from_sorted_data.py:125` - `write_question` (commit `a1562c122f`)
- 2026-01-05 - `problems/biostatistics-problems/boxplot_from_cdf.py:185` - `write_question` (commit `a1562c122f`)
- 2026-01-05 - `problems/biophysics-problems/fret_permute_colors.py:56` - `write_question` (commit `9ec6038c42`) - file 2021-10-20 (commit `ee00379b21`)
- 2026-01-05 - `problems/biochemistry-problems/photosynthetic_light_pigments.py:96` - `write_question` (commit `9ec6038c42`) - file 2022-03-06 (commit `c99c5c0101`)
- 2026-01-05 - `problems/biochemistry-problems/lipids/quick_fatty_acid_colon_system.py:49` - `write_question` (commit `9ec6038c42`) - file 2021-10-20 (commit `57f8de01ea`)
- 2026-01-05 - `problems/biochemistry-problems/lipids/quick_fatty_acid_colon_system.py:24` - `_format_question` (commit `9ec6038c42`) - file 2021-10-20 (commit `57f8de01ea`)
- 2026-01-05 - `problems/biochemistry-problems/electrophoresis/kaleidoscope_ladder/kaleidoscope_ladder_unknown_band.py:398` - `write_lane2_unknown_band_protein_mc_question` (commit `9ec6038c42`) - file 2026-02-11 (commit `6bd693f40b`) - "Lane 1: Kaleidoscope ladder bands."
- 2026-01-05 - `problems/biochemistry-problems/electrophoresis/kaleidoscope_ladder/kaleidoscope_ladder_unknown_band.py:230` - `write_lane2_unknown_band_mw_question` (commit `dae5797aaa`) - file 2026-02-11 (commit `6bd693f40b`) - "Lane 1: Kaleidoscope ladder bands (some may be off-gel if run too long)."
- 2026-01-05 - `problems/biochemistry-problems/carbs/convert_Haworth_to_Fischer.py:15` - `write_question` (commit `d30f49fc44`) - file 2025-03-28 (commit `21f2728be2`)
- 2026-01-05 - `problems/biochemistry-problems/carbs/convert_Fischer_to_Haworth.py:14` - `write_question` (commit `d30f49fc44`) - file 2025-03-28 (commit `21f2728be2`)
- 2026-01-05 - `problems/biochemistry-problems/carbs/classify_Haworth.py:14` - `write_question` (commit `0ff0ec23e6`) - file 2024-12-05 (commit `7bc1d2b29d`) - "Creates a multiple-choice question for classifying a sugar based on its Haworth projection."
- 2026-01-05 - `problems/biochemistry-problems/carbs/classify_Fischer.py:13` - `write_question` (commit `0ff0ec23e6`) - file 2021-10-20 (commit `57f8de01ea`) - "Creates a multiple-choice question for classifying a sugar based on its Fischer projection."
- 2026-01-05 - `problems/biochemistry-problems/buffers/pKa_buffer_state.py:81` - `write_question` (commit `9ec6038c42`) - file 2022-09-14 (commit `94f40179e3`) - "Create a single buffer protonation question."
- 2026-01-05 - `problems/biochemistry-problems/PUBCHEM/PEPTIDES/wordle_peptides.py:128` - `write_question_batch` (commit `a1562c122f`) - file 2023-10-11 (commit `05516645ca`)
- 2026-01-05 - `problems/biochemistry-problems/PUBCHEM/PEPTIDES/polypeptide_fib_sequence.py:136` - `write_question` (commit `a1562c122f`) - file 2024-01-26 (commit `0350196c87`)
- 2026-01-05 - `problems/biochemistry-problems/PUBCHEM/MACROMOLECULE_CATEGORIZE/which_macromolecule.py:172` - `write_question` (commit `a1562c122f`) - file 2024-01-24 (commit `d4e4d2615d`)
- 2026-01-05 - `problems/biochemistry-problems/PUBCHEM/GLYCOLYSIS/order_glycolysis_molecules.py:70` - `write_question` (commit `a1562c122f`) - file 2024-02-28 (commit `6942c3419a`)
## 2026-01-04
- 2026-01-04 - `problems/inheritance-problems/x_linked_tortoiseshell.py:84` - `write_question` (commit `566b69080e`)
- 2026-01-04 - `problems/inheritance-problems/x_linked_reciprocal_cross.py:38` - `write_question` (commit `566b69080e`)
- 2026-01-04 - `problems/inheritance-problems/translocation/letter_translocation_problem_color.py:488` - `write_question` (commit `55c9411bd0`) - file 2021-11-02 (commit `5a4e22f914`)
- 2026-01-04 - `problems/inheritance-problems/monohybrid_litter_inference.py:114` - `write_question` (commit `566b69080e`)
- 2026-01-04 - `problems/inheritance-problems/lethal_allele_survival.py:136` - `write_question` (commit `566b69080e`)
- 2026-01-04 - `problems/inheritance-problems/dominant_and_X-linked_recessive_variations.py:149` - `write_question` (commit `566b69080e`)
- 2026-01-04 - `problems/inheritance-problems/cytogenetic_notation/cytogenetic_notation-disorders.py:788` - `write_question` (commit `a63736b8ef`) - "Write one question using the YAML disorder data."
- 2026-01-04 - `problems/inheritance-problems/cytogenetic_notation/cytogenetic_notation-disorders.py:749` - `write_question_from_entry` (commit `a63736b8ef`) - "Create a formatted question from one disorder entry."
- 2026-01-04 - `problems/inheritance-problems/cytogenetic_notation/cytogenetic_notation-band_order.py:150` - `write_question` (commit `a63736b8ef`) - "Generate a formatted multiple-choice question."
- 2026-01-04 - `problems/inheritance-problems/chi_square/chi_square_hypotheses_lab_partner.py:240` - `write_question` (commit `566b69080e`)
- 2026-01-04 - `problems/inheritance-problems/chi_square/chi_square_hypotheses.py:315` - `write_question` (commit `566b69080e`)
- 2026-01-04 - `problems/biostatistics-problems/hypothesis_statements.py:384` - `write_question` (commit `566b69080e`)
- 2026-01-04 - `problems/biostatistics-problems/hypothesis_lab_partner.py:331` - `write_question` (commit `566b69080e`)
- 2026-01-04 - `problems/biochemistry-problems/electrophoresis/kaleidoscope_ladder/kaleidoscope_ladder_mapping.py:97` - `write_prelim_estimate_unknown_question` (commit `a36bce137d`)
## 2025-12-27
- 2025-12-27 - `problems/molecular_biology-problems/translate_genetic_code.py:147` - `write_question` (commit `b43f71cb79`) - file 2022-04-18 (commit `2c70a31db4`)
- 2025-12-27 - `problems/molecular_biology-problems/translate_genetic_code.py:92` - `make_complete_question` (commit `b43f71cb79`) - file 2022-04-18 (commit `2c70a31db4`)
- 2025-12-27 - `problems/molecular_biology-problems/rna_transcribe_prime_fill_blank.py:7` - `write_question` (commit `b43f71cb79`) - file 2020-09-19 (commit `18f2644fb3`)
- 2025-12-27 - `problems/molecular_biology-problems/rna_transcribe_prime.py:9` - `write_question` (commit `b43f71cb79`) - file 2020-09-19 (commit `5d1f85f1c4`)
- 2025-12-27 - `problems/molecular_biology-problems/restriction_enzymes/overhang_type.py:123` - `write_question_batch` (commit `b43f71cb79`) - file 2020-09-19 (commit `7c5c1f653c`)
- 2025-12-27 - `problems/molecular_biology-problems/restriction_enzymes/linear_digest.py:124` - `write_question` (commit `b43f71cb79`) - file 2020-10-03 (commit `08c17b9a7f`)
- 2025-12-27 - `problems/molecular_biology-problems/palindrome_sequence_match.py:117` - `write_question_wrapper` (commit `b43f71cb79`) - file 2018-10-22 (commit `e3bc01df2f`)
- 2025-12-27 - `problems/molecular_biology-problems/nested_pcr_design.py:111` - `write_question` (commit `b43f71cb79`) - file 2021-10-06 (commit `0cf277d538`)
- 2025-12-27 - `problems/molecular_biology-problems/inverse_pcr_design.py:127` - `write_question` (commit `b43f71cb79`) - file 2021-10-06 (commit `0cf277d538`)
- 2025-12-27 - `problems/molecular_biology-problems/exon_splicing.py:199` - `write_question` (commit `b43f71cb79`) - file 2021-12-04 (commit `3c9f864bf9`)
- 2025-12-27 - `problems/molecular_biology-problems/enhancer_gene_expression.py:181` - `write_question` (commit `b43f71cb79`) - file 2023-04-25 (commit `80420db04e`)
- 2025-12-27 - `problems/molecular_biology-problems/dna_melting_temp.py:43` - `make_question` (commit `b43f71cb79`) - file 2021-10-25 (commit `21799f9051`)
- 2025-12-27 - `problems/molecular_biology-problems/dna_gel-estimate_size-MC_or_NUM.py:170` - `write_question` (commit `b43f71cb79`) - file 2020-09-27 (commit `3e07e65d23`)
- 2025-12-27 - `problems/molecular_biology-problems/dna_gel-estimate_size-MC_or_NUM.py:121` - `GelMigration.writeProblem` (commit `b43f71cb79`) - file 2020-09-27 (commit `3e07e65d23`)
- 2025-12-27 - `problems/molecular_biology-problems/dna_gel-closest_farthest_MC.py:55` - `write_question` (commit `b43f71cb79`) - file 2021-10-20 (commit `0212b5986b`)
- 2025-12-27 - `problems/molecular_biology-problems/consensus_sequence_FIB-hard.py:133` - `write_question` (commit `b43f71cb79`) - file 2021-10-04 (commit `fd3c99a5f1`)
- 2025-12-27 - `problems/molecular_biology-problems/consensus_sequence_FIB-easy.py:122` - `write_question` (commit `b43f71cb79`) - file 2021-10-04 (commit `fd3c99a5f1`)
- 2025-12-27 - `problems/molecular_biology-problems/consensus_sequence_FIB-arbitrary_code.py:132` - `write_question` (commit `b43f71cb79`) - file 2021-10-04 (commit `fd3c99a5f1`)
- 2025-12-27 - `problems/molecular_biology-problems/chargaff_dna_percent.py:103` - `write_question` (commit `b43f71cb79`) - file 2019-10-30 (commit `1cb7860dfe`)
- 2025-12-27 - `problems/molecular_biology-problems/beadle_tatum-metabolic_pathway.py:43` - `write_question` (commit `b43f71cb79`) - file 2022-04-17 (commit `e66a6538b3`)
- 2025-12-27 - `problems/molecular_biology-problems/amplicon_copies.py:44` - `write_question_batch` (commit `b43f71cb79`) - file 2021-10-11 (commit `5490bc5e5b`)
- 2025-12-27 - `problems/molecular_biology-problems/RT-qPCR.py:114` - `write_question` (commit `b43f71cb79`) - file 2021-11-14 (commit `2488873bd4`)
- 2025-12-27 - `problems/laboratory-problems/solution-vol_vol-numeric.py:54` - `write_question` (commit `ab533c44b1`) - file 2021-04-28 (commit `17d8ae2513`)
- 2025-12-27 - `problems/laboratory-problems/solution-molarity-mol_weight-numeric.py:89` - `write_question` (commit `b43f71cb79`) - file 2021-04-28 (commit `17d8ae2513`)
- 2025-12-27 - `problems/laboratory-problems/solution-mass_vol-numeric.py:69` - `write_question` (commit `ab533c44b1`) - file 2021-04-28 (commit `17d8ae2513`)
- 2025-12-27 - `problems/laboratory-problems/solution-mass_concentration-numeric.py:74` - `write_question` (commit `ab533c44b1`) - file 2021-04-28 (commit `17d8ae2513`)
- 2025-12-27 - `problems/laboratory-problems/serial_dilution_factor_mc.py:130` - `write_question` (commit `ab533c44b1`) - file 2021-04-28 (commit `17d8ae2513`)
- 2025-12-27 - `problems/laboratory-problems/serial_dilution_factor_diluent_numeric.py:50` - `write_question` (commit `ab533c44b1`) - file 2021-04-28 (commit `17d8ae2513`)
- 2025-12-27 - `problems/laboratory-problems/pipet_size_mc.py:181` - `write_question` (commit `ab533c44b1`) - file 2021-04-28 (commit `17d8ae2513`)
- 2025-12-27 - `problems/laboratory-problems/percent_dilution_aliquot_numeric.py:97` - `write_question` (commit `ab533c44b1`) - file 2021-04-28 (commit `17d8ae2513`)
- 2025-12-27 - `problems/laboratory-problems/orders_of_magnitude_mc.py:129` - `write_question` (commit `ab533c44b1`) - file 2021-04-28 (commit `17d8ae2513`)
- 2025-12-27 - `problems/laboratory-problems/dilution_factor_mc.py:104` - `write_question` (commit `b43f71cb79`) - file 2021-04-28 (commit `17d8ae2513`)
- 2025-12-27 - `problems/laboratory-problems/dilution_factor_diluent_numeric.py:35` - `write_question` (commit `b43f71cb79`) - file 2021-04-28 (commit `17d8ae2513`)
- 2025-12-27 - `problems/laboratory-problems/dilution_factor_aliquot_numeric.py:35` - `write_question` (commit `b43f71cb79`) - file 2021-04-28 (commit `17d8ae2513`)
- 2025-12-27 - `problems/inheritance-problems/translocation/translocation_meiosis_table.py:122` - `write_question` (commit `b43f71cb79`) - file 2020-12-04 (commit `f02ddfe4fa`)
- 2025-12-27 - `problems/inheritance-problems/pedigrees/write_pedigree_match.py:51` - `matchingQuestionSet` (commit `273a936da2`) - file 2021-10-31 (commit `cf9a40554c`)
- 2025-12-27 - `problems/inheritance-problems/pedigrees/write_pedigree_choice.py:114` - `write_question_batch` (commit `b43f71cb79`) - file 2021-10-31 (commit `cf9a40554c`)
- 2025-12-27 - `problems/inheritance-problems/monohybrid_genotype_statements.py:180` - `write_question_batch` (commit `b43f71cb79`) - file 2024-11-02 (commit `450cfb15cf`) - "Generates and writes questions to file."
- 2025-12-27 - `problems/inheritance-problems/monohybrid_degrees_of_dominance.py:99` - `write_question` (commit `b43f71cb79`) - file 2025-08-07 (commit `e981f49c30`) - "Creates a formatted MC question about gene type interpretation."
- 2025-12-27 - `problems/inheritance-problems/hardy_weinberg/hardy_weinberg_numeric.py:431` - `write_question` (commit `b43f71cb79`) - file 2020-12-10 (commit `4e17403d3b`)
- 2025-12-27 - `problems/inheritance-problems/hardy_weinberg/hardy_weinberg_mc_type.py:392` - `write_question` (commit `b43f71cb79`) - file 2023-12-11 (commit `e7ae9002d7`)
- 2025-12-27 - `problems/inheritance-problems/dominant_and_X-linked_recessive.py:39` - `write_question` (commit `b43f71cb79`) - file 2021-10-25 (commit `b5e78e6caa`)
- 2025-12-27 - `problems/inheritance-problems/cytogenetic_notation/cytogenetic_notation-sub-band_notation.py:154` - `write_question` (commit `b43f71cb79`) - file 2024-11-02 (commit `450cfb15cf`) - "Creates a complete formatted question for output."
- 2025-12-27 - `problems/inheritance-problems/cytogenetic_notation/cytogenetic_notation-rearrangements.py:285` - `write_question` (commit `b43f71cb79`) - file 2024-11-13 (commit `6d485e4796`) - "Creates a complete formatted question for output."
- 2025-12-27 - `problems/inheritance-problems/chi_square/chi_square_hardy_weinberg.py:306` - `write_question` (commit `b43f71cb79`) - file 2020-12-10 (commit `bae8f50e09`)
- 2025-12-27 - `problems/inheritance-problems/chi_square/chi_square_choices.py:341` - `write_question` (commit `b43f71cb79`) - file 2020-10-23 (commit `3c8b1d6991`)
- 2025-12-27 - `problems/inheritance-problems/chi_square/chi_square_calculated.py:154` - `write_question` (commit `b43f71cb79`) - file 2021-10-17 (commit `d89a2d6f66`)
- 2025-12-27 - `problems/dna_profiling-problems/who_killer_html.py:443` - `write_question_wrapper` (commit `b43f71cb79`) - file 2018-09-28 (commit `b6cd8c505e`) - "Wrapper for collect_and_write_questions that uses precomputed params."
- 2025-12-27 - `problems/dna_profiling-problems/who_father_html.py:362` - `write_question_wrapper` (commit `b43f71cb79`) - file 2018-09-28 (commit `eb3cfd7555`) - "Wrapper for collect_and_write_questions that uses precomputed params."
- 2025-12-27 - `problems/dna_profiling-problems/blood_type_agglutination_test.py:281` - `write_question` (commit `b43f71cb79`) - file 2020-10-01 (commit `32e9dbb9ca`) - "Creates a complete formatted question for output."
- 2025-12-27 - `problems/biostatistics-problems/z_score_table_interp.py:377` - `write_question` (commit `b43f71cb79`) - file 2024-10-28 (commit `b8f12aee5c`) - "Creates a formatted multiple-choice question."
- 2025-12-27 - `problems/biostatistics-problems/z_score_google_sheet.py:248` - `write_question` (commit `b43f71cb79`) - file 2025-09-15 (commit `d7cf1aea49`) - "Create one Blackboard MC question row with Z-score targeting."
- 2025-12-27 - `problems/biostatistics-problems/population_test_google_sheet.py:193` - `write_question` (commit `b43f71cb79`) - file 2024-11-02 (commit `450cfb15cf`) - "Creates a complete formatted question for output."
- 2025-12-27 - `problems/biostatistics-problems/busse_woods_two_sample_t_test.py:236` - `write_question` (commit `b43f71cb79`) - file 2025-10-20 (commit `654cc1465b`) - "Create one Blackboard numeric question row for a two-sample test."
- 2025-12-27 - `problems/biostatistics-problems/busse_woods_one_sample_tests.py:269` - `write_question` (commit `b43f71cb79`) - file 2025-10-20 (commit `654cc1465b`) - "Create a complete formatted question for output."
- 2025-12-27 - `problems/biostatistics-problems/babies_two_sample_t_test.py:192` - `write_question` (commit `b43f71cb79`) - file 2024-11-02 (commit `450cfb15cf`) - "Create one Blackboard numeric question row for a two-sample t-test."
- 2025-12-27 - `problems/biophysics-problems/fret_overlap_colors.py:63` - `write_question` (commit `b43f71cb79`) - file 2021-10-20 (commit `ee00379b21`)
- 2025-12-27 - `problems/biochemistry-problems/lipids/which_hydrophobic-simple.py:67` - `write_question` (commit `b43f71cb79`) - file 2021-10-20 (commit `ee00379b21`) - "Creates a complete formatted question."
- 2025-12-27 - `problems/biochemistry-problems/enzymes/optimal_enzyme-type_3.py:10` - `write_question` (commit `b43f71cb79`) - file 2022-03-21 (commit `f5fae70b9e`)
- 2025-12-27 - `problems/biochemistry-problems/enzymes/optimal_enzyme-type_2.py:10` - `write_question` (commit `b43f71cb79`) - file 2022-03-21 (commit `f5fae70b9e`)
- 2025-12-27 - `problems/biochemistry-problems/enzymes/optimal_enzyme-type_1.py:10` - `write_question` (commit `b43f71cb79`) - file 2022-03-21 (commit `bbc4cdab47`)
- 2025-12-27 - `problems/biochemistry-problems/enzymes/metabolic_pathway_inhibitor.py:97` - `write_question` (commit `b43f71cb79`) - file 2022-03-18 (commit `9c8694df5c`) - "Create a metabolic pathway question about enzyme inhibition types."
- 2025-12-27 - `problems/biochemistry-problems/electrophoresis/protein_gel_migration.py:258` - `write_question` (commit `b43f71cb79`) - file 2021-10-20 (commit `0212b5986b`)
- 2025-12-27 - `problems/biochemistry-problems/electrophoresis/isoelectric_one_protein.py:91` - `write_question` (commit `b43f71cb79`) - file 2021-10-20 (commit `ee00379b21`)
- 2025-12-27 - `problems/biochemistry-problems/buffers/optimal_buffering_range.py:167` - `write_question` (commit `b43f71cb79`) - file 2024-11-02 (commit `450cfb15cf`) - "Creates a complete formatted question for output."
- 2025-12-27 - `problems/biochemistry-problems/PUBCHEM/PEPTIDES/polypeptide_mc_sequence.py:189` - `write_question` (commit `b43f71cb79`) - file 2024-01-26 (commit `0350196c87`)
## 2025-12-26
- 2025-12-26 - `problems/molecular_biology-problems/rna_transcribe_fill_blank.py:11` - `write_question` (commit `4ea5e957a1`) - file 2020-09-19 (commit `5d1f85f1c4`)
- 2025-12-26 - `problems/molecular_biology-problems/restriction_enzymes/overhang_sequence.py:158` - `write_question_batch` (commit `40a72dd38f`) - file 2020-09-19 (commit `7c5c1f653c`)
- 2025-12-26 - `problems/molecular_biology-problems/pcr_design.py:95` - `write_question` (commit `fa233f32ee`) - file 2021-10-06 (commit `0cf277d538`)
- 2025-12-26 - `problems/molecular_biology-problems/mutant_screen.py:70` - `write_question` (commit `2b5f045e0e`) - file 2018-10-22 (commit `e3bc01df2f`)
- 2025-12-26 - `problems/molecular_biology-problems/consensus_sequence_MC.py:133` - `write_question` (commit `d09c4c6b75`) - file 2021-04-28 (commit `17d8ae2513`)
- 2025-12-26 - `problems/molecular_biology-problems/complementary_sequences.py:249` - `write_question` (commit `d09c4c6b75`) - file 2023-10-31 (commit `198f957169`)
- 2025-12-26 - `problems/laboratory-problems/serial_dilution_factor_aliquot_numeric.py:61` - `write_question` (commit `cce2b62dbd`) - file 2021-04-28 (commit `17d8ae2513`)
- 2025-12-26 - `problems/laboratory-problems/dilution_factor_calc_numeric.py:38` - `write_question` (commit `017faf99cf`) - file 2022-01-18 (commit `a7d514e638`)
- 2025-12-26 - `problems/inheritance-problems/probabiliy_of_progeny.py:347` - `write_question` (commit `4ea5e957a1`) - file 2020-10-24 (commit `af21e74916`)
- 2025-12-26 - `problems/inheritance-problems/polyploid/polyploid-monoploid_v_haploid.py:62` - `write_question` (commit `cce2b62dbd`) - file 2020-12-04 (commit `f02ddfe4fa`)
- 2025-12-26 - `problems/inheritance-problems/poisson_flies.py:183` - `write_question` (commit `00a00437f0`) - file 2020-10-22 (commit `722c8c7614`)
- 2025-12-26 - `problems/inheritance-problems/poisson_flies.py:125` - `build_question` (commit `00a00437f0`) - file 2020-10-22 (commit `722c8c7614`)
- 2025-12-26 - `problems/inheritance-problems/pedigrees/write_pedigree_match.py:109` - `write_question_batch` (commit `40a72dd38f`) - file 2021-10-31 (commit `cf9a40554c`)
- 2025-12-26 - `problems/inheritance-problems/large_crosses/unique_gametes.py:22` - `write_question` (commit `511cfc02ae`) - file 2023-09-26 (commit `0a883d1f93`)
- 2025-12-26 - `problems/inheritance-problems/large_crosses/unique_cross_phenotypes.py:84` - `write_question` (commit `511cfc02ae`) - file 2021-10-04 (commit `4f08846330`)
- 2025-12-26 - `problems/inheritance-problems/large_crosses/unique_cross_genotypes.py:79` - `write_question` (commit `511cfc02ae`) - file 2021-10-04 (commit `36c4a232a3`)
- 2025-12-26 - `problems/inheritance-problems/epistasis/epistasis_test_cross.py:207` - `write_question` (commit `2b5f045e0e`) - file 2020-10-16 (commit `dbb07d0e9a`) - "Format a single MC Blackboard question for the provided F2 ratio."
- 2025-12-26 - `problems/inheritance-problems/epistasis/dihybrid_cross_epistatic_gene_metabolics.py:519` - `write_question` (commit `017faf99cf`) - file 2020-11-01 (commit `e5cf95d333`) - "Create a single epistatic gene interaction question."
- 2025-12-26 - `problems/inheritance-problems/epistasis/dihybrid_cross_epistatic_gene_metabolics.py:447` - `build_question` (commit `d09c4c6b75`) - file 2020-11-01 (commit `e5cf95d333`) - "Creates a formatted MC question about gene interaction types."
- 2025-12-26 - `problems/inheritance-problems/epistasis/dihybrid_cross_epistatic_gene_interactions.py:128` - `write_question` (commit `d09c4c6b75`) - file 2020-10-31 (commit `30f2e27da3`)
- 2025-12-26 - `problems/inheritance-problems/epistasis/dihybrid_cross_epistatic_gene_interactions.py:85` - `build_question` (commit `d09c4c6b75`) - file 2020-10-31 (commit `30f2e27da3`) - "Creates a formatted MC question about gene interaction types."
- 2025-12-26 - `problems/inheritance-problems/cytogenetic_notation/cytogenetic_notation-aneuploidy.py:193` - `write_question` (commit `4ea5e957a1`) - file 2024-11-13 (commit `a3cf91041b`) - "Creates a complete formatted question for output."
- 2025-12-26 - `problems/inheritance-problems/chi_square/chi_square_errors.py:347` - `write_question` (commit `4ea5e957a1`) - file 2020-10-23 (commit `3c8b1d6991`) - "Generate a formatted multiple-choice question for chi-square errors."
- 2025-12-26 - `problems/inheritance-problems/blood_type_offspring.py:61` - `build_question` (commit `4ea5e957a1`) - file 2020-10-16 (commit `ef7ed68de4`) - "Creates a complete formatted multiple-answer question string."
- 2025-12-26 - `problems/dna_profiling-problems/hla_genotype.py:124` - `write_question` (commit `d09c4c6b75`) - file 2018-10-22 (commit `e3bc01df2f`)
- 2025-12-26 - `problems/cell_biology-problems/cell_surf-to-vol_ratio.py:150` - `write_question` (commit `d09c4c6b75`) - file 2023-02-03 (commit `406b9be8bc`)
- 2025-12-26 - `problems/biostatistics-problems/descriptive_stats_google_sheet.py:144` - `write_question` (commit `d09c4c6b75`) - file 2025-09-04 (commit `2338cbd3a8`) - "Creates a complete formatted FIB_PLUS question row."
- 2025-12-26 - `problems/biochemistry-problems/lipids/which_lipid-chemical_formula.py:106` - `write_question` (commit `017faf99cf`) - file 2021-10-20 (commit `57f8de01ea`)
- 2025-12-26 - `problems/biochemistry-problems/ionic_bond_amino_acids.py:72` - `write_question` (commit `511cfc02ae`) - file 2024-01-24 (commit `65923792a6`) - "Creates a complete formatted question."
- 2025-12-26 - `problems/biochemistry-problems/enzymes/chymotrypsin_substrate.py:234` - `write_question` (commit `00a00437f0`) - file 2021-10-20 (commit `57f8de01ea`)
- 2025-12-26 - `problems/biochemistry-problems/enzymes/chymotrypsin_substrate.py:214` - `build_question` (commit `00a00437f0`) - file 2021-10-20 (commit `57f8de01ea`) - "Creates a complete formatted question for output."
- 2025-12-26 - `problems/biochemistry-problems/electrophoresis/isoelectric_two_proteins.py:226` - `write_question` (commit `2b5f045e0e`) - file 2021-10-20 (commit `ee00379b21`)
- 2025-12-26 - `problems/biochemistry-problems/buffers/pKa_buffer_state.py:37` - `write_question_text` (commit `00a00437f0`) - file 2022-09-14 (commit `94f40179e3`)
- 2025-12-26 - `problems/biochemistry-problems/buffers/Henderson-Hasselbalch.py:561` - `write_question` (commit `40a72dd38f`) - file 2024-11-02 (commit `450cfb15cf`)
- 2025-12-26 - `problems/biochemistry-problems/alpha_helix_h-bonds.py:79` - `write_question` (commit `511cfc02ae`) - file 2021-10-20 (commit `ee00379b21`)
## 2025-11-12
- 2025-11-12 - `problems/inheritance-problems/deletion_mutants/deletionlib.py:376` - `write_question_text` (commit `9ce33184ef`) - "Writes the question about gene order based on the original list and deletions."
## 2025-11-11
- 2025-11-11 - `problems/inheritance-problems/deletion_mutants/deletion_mutant_words.py:299` - `write_question` (commit `665b49b7d6`) - file 2018-11-14 (commit `6ab4a2f585`) - "Creates a single formatted question with various answer formats and tables."
## 2025-08-09
- 2025-08-09 - `problems/inheritance-problems/hardy_weinberg/hardy_weinberg_numeric.py:342` - `makeQuestion` (commit `39b9949d0c`) - file 2020-12-10 (commit `4e17403d3b`)
## 2025-08-08
- 2025-08-08 - `problems/inheritance-problems/epistasis/dihybrid_cross_epistatic_gene_metabolics.py:408` - `makeQuestion` (commit `c35bb86500`) - file 2020-11-01 (commit `e5cf95d333`)
## 2025-08-07
- 2025-08-07 - `problems/inheritance-problems/monohybrid_genotype_statements.py:132` - `write_question` (commit `682a2f13c9`) - file 2024-11-02 (commit `450cfb15cf`) - "Creates a complete formatted question for output."
## 2025-08-06
- 2025-08-06 - `problems/molecular_biology-problems/restriction_enzymes/overhang_type.py:58` - `write_question` (commit `bd97141350`) - file 2020-09-19 (commit `7c5c1f653c`)
- 2025-08-06 - `problems/molecular_biology-problems/restriction_enzymes/overhang_sequence.py:147` - `write_question` (commit `c67f21e393`) - file 2020-09-19 (commit `7c5c1f653c`)
- 2025-08-06 - `problems/molecular_biology-problems/restriction_enzymes/overhang_sequence.py:68` - `makeMultipleChoiceQuestion` (commit `ee66d3b302`) - file 2020-09-19 (commit `7c5c1f653c`)
- 2025-08-06 - `problems/molecular_biology-problems/restriction_enzymes/overhang_sequence.py:50` - `makeFillInBlankQuestion` (commit `ee66d3b302`) - file 2020-09-19 (commit `7c5c1f653c`)
- 2025-08-06 - `problems/molecular_biology-problems/palindrome_sequence_match.py:57` - `write_question` (commit `78ebfdd4b6`) - file 2018-10-22 (commit `e3bc01df2f`)
- 2025-08-06 - `problems/dna_profiling-problems/who_killer_html.py:392` - `write_question` (commit `5b4a591399`) - file 2018-09-28 (commit `b6cd8c505e`)
- 2025-08-06 - `problems/dna_profiling-problems/who_father_html.py:316` - `write_question` (commit `5b4a591399`) - file 2018-09-28 (commit `eb3cfd7555`)
## 2025-03-28
- 2025-03-28 - `problems/biochemistry-problems/carbs/D_to_L_Fischer_configuration.py:82` - `write_question2` (commit `2db7165d57`) - file 2020-10-28 (commit `79f564930d`)
## 2025-02-04
- 2025-02-04 - `problems/biochemistry-problems/buffers/Henderson-Hasselbalch.py:315` - `write_equation_question` (commit `f06e2d4f6e`) - file 2024-11-02 (commit `450cfb15cf`) - "Creates a complete formatted question for output."
## 2025-01-31
- 2025-01-31 - `problems/biochemistry-problems/PUBCHEM/PEPTIDES/polypeptide_mc_sequence.py:156` - `generate_complete_question` (commit `7c939af2ec`) - file 2024-01-26 (commit `0350196c87`) - "Given a word (amino acid sequence), generate a complete question."
## 2024-11-18
- 2024-11-18 - `problems/inheritance-problems/deletion_mutants/deletion_mutant_random.py:123` - `write_question` (commit `59fba6f559`) - file 2018-11-14 (commit `6ab4a2f585`) - "Creates a single formatted question with various answer formats and tables."
## 2024-11-06
- 2024-11-06 - `problems/inheritance-problems/gene_mapping/three-point_test_cross-find_interence.py:135` - `generate_question` (commit `39d86f1ed7`) - file 2023-11-06 (commit `265718c413`) - "Generates a formatted question string based on question type (multiple-choice or numeric answer)."
- 2024-11-06 - `problems/inheritance-problems/gene_mapping/tetrad_unordered_two_gene-test_linkage.py:194` - `generate_question` (commit `572b8d0eb6`) - file 2021-11-09 (commit `22d94705bd`) - "Generates a formatted multiple-choice question on gene linkage and genetic distance."
- 2024-11-06 - `problems/inheritance-problems/gene_mapping/tetrad_unordered_two_gene-find_distance.py:258` - `generate_question` (commit `39d86f1ed7`) - file 2021-11-09 (commit `22d94705bd`) - "Generates a formatted multiple-choice question on gene linkage and genetic distance."
## 2024-11-02
- 2024-11-02 - `problems/inheritance-problems/gene_mapping/tetrad_ordered-centromere_distance.py:257` - `generate_question` (commit `0eac97ab3a`) - file 2023-11-08 (commit `d865b5bf1d`) - "Generates a formatted question string based on the question type and question number."
## 2024-02-12
- 2024-02-12 - `problems/biochemistry-problems/electrophoresis/protein_gel_migration.py:189` - `GelMigration.write_question` (commit `b64accce99`) - file 2021-10-20 (commit `0212b5986b`) - "49. <p>The standard and unknown proteins listed in the table were run using SDS-PAGE.</p> <p><b>Estimate the molecula..."
## 2024-01-26
- 2024-01-26 - `problems/biochemistry-problems/PUBCHEM/PEPTIDES/polypeptide_fib_sequence.py:108` - `generate_complete_question` (commit `0350196c87`) - "Given a word (amino acid sequence), generate a complete question."
## 2023-12-11
- 2023-12-11 - `problems/inheritance-problems/gene_mapping/broken-tetrad_unordered_three_gene-distances_plus.py:254` - `makeQuestion` (commit `4abe320a59`) - file 2020-11-26 (commit `d3e24ca76e`)
## 2023-10-31
- 2023-10-31 - `problems/molecular_biology-problems/complementary_sequences.py:142` - `write_prime_fib_question` (commit `198f957169`)
- 2023-10-31 - `problems/molecular_biology-problems/complementary_sequences.py:46` - `write_directionless_fib_question` (commit `198f957169`)
- 2023-10-31 - `problems/inheritance-problems/chi_square/chi_square_choices.py:222` - `makeQuestion` (commit `054a705878`) - file 2020-10-23 (commit `3c8b1d6991`) - "Numpydoc Style:"
## 2023-10-11
- 2023-10-11 - `problems/biochemistry-problems/PUBCHEM/PEPTIDES/wordle_peptides.py:102` - `generate_complete_question` (commit `05516645ca`) - "Given a word (amino acid sequence), generate a complete question."
## 2022-09-15
- 2022-09-15 - `problems/biochemistry-problems/buffers/pKa_buffer_state.py:55` - `make_complete_question` (commit `9c90daf180`) - file 2022-09-14 (commit `94f40179e3`)
## 2021-12-09
- 2021-12-09 - `problems/molecular_biology-problems/exon_splicing.py:171` - `makeCompleteQuestion` (commit `c942aaec22`) - file 2021-12-04 (commit `3c9f864bf9`)
## 2021-11-25
- 2021-11-25 - `problems/inheritance-problems/translocation/robertsonian.py:18` - `blackboardFormat` (commit `e460638244`) - file 2020-12-04 (commit `f02ddfe4fa`)
## 2021-11-24
- 2021-11-24 - `problems/inheritance-problems/polyploid/polyploid-gametes.py:40` - `makeQuestion` (commit `d40f13f443`)
## 2021-10-20
- 2021-10-20 - `problems/molecular_biology-problems/consensus_sequence_FIB-arbitrary_code.py:106` - `makeCompleteQuestion` (commit `e2faece0a7`) - file 2021-10-04 (commit `fd3c99a5f1`)
## 2021-10-17
- 2021-10-17 - `problems/molecular_biology-problems/consensus_sequence_FIB-hard.py:107` - `makeCompleteQuestion` (commit `d89a2d6f66`) - file 2021-10-04 (commit `fd3c99a5f1`)
- 2021-10-17 - `problems/molecular_biology-problems/consensus_sequence_FIB-easy.py:96` - `makeCompleteQuestion` (commit `d89a2d6f66`) - file 2021-10-04 (commit `fd3c99a5f1`)
- 2021-10-17 - `problems/inheritance-problems/chi_square/chi_square_calculated.py:110` - `makeQuestion` (commit `d89a2d6f66`)
## 2020-12-10
- 2020-12-10 - `problems/inheritance-problems/chi_square/chi_square_hardy_weinberg.py:248` - `makeQuestion` (commit `7593122c25`)
## 2020-11-24
- 2020-11-24 - `problems/inheritance-problems/gene_mapping/four_point_test-cross_gene_map-distances_plus.py:118` - `makeQuestion` (commit `b7e09b97ac`)
## 2020-10-31
- 2020-10-31 - `problems/inheritance-problems/epistasis/dihybrid_cross_epistatic_gene_interactions.py:42` - `makeQuestion` (commit `30f2e27da3`)
## 2020-10-23
- 2020-10-23 - `problems/inheritance-problems/chi_square/chi_square_errors.py:305` - `makeQuestion` (commit `b5c5d2ad30`)
