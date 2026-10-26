# Ultra/Classic showcase question catalog

Catalog of every question generator evaluated for the Blackboard Classic vs
Blackboard Ultra HTML-sanitization showcase
([devel/ultra_classic_showcase.py](../../../devel/ultra_classic_showcase.py)),
which ones were selected, and why the rest were left out.

## Purpose and audience

The showcase exists to prove, with real graded content, that Blackboard Ultra's
HTML sanitizer strips or flattens information that Blackboard Classic renders
correctly. The audience is IT staff deciding whether to retain Classic, not
students. That drives two selection rules:

- Short over long. Each item should show one failure with minimal reading.
- One strong exemplar per failure class. Breadth of failure classes matters more
  than breadth of biology topics or question types. The showcase is about HTML
  failures, not "it works across question types."

## Failure-class taxonomy

Confirmed by side-by-side Learn/Ultra PDFs:

- color = data: color carries the content (maps, gel bands, numeric place value).
- color = identity: a color links a figure to recurring labels in the prose or
  options; stripping it breaks the link.
- script render: client-side JavaScript draws a figure into a `<canvas>`; Ultra
  strips `<script>`/`<canvas>` and the figure is blank.
- spacing = data: HTML table-cell spacing positions content (rulers, number
  lines); reflow destroys the positions.
- width = data: table column widths or whitespace hold a structure together;
  reflow collapses or scrambles it.
- color = convenience: color aids reading (disambiguation, emphasis, readability)
  but the data survives in text.
- structural type-drop: not an HTML failure; Ultra's QTI v2.1 import drops
  unsupported types (Matching). The chosen matching set does double duty: it also
  colors each column-type name (IEX, AC, HIC, SEC) and the recurring key terms,
  linking colored prompt to colored description, so it reinforces the color-identity
  failure where the pool export carries it into Ultra.

Two classes are likely but await an Ultra import confirmation:

- script render (RDKit.js `<canvas>`): near-certain, see item 5.
- monospace / `font-family` alignment: probed by the control item (11).

## Selected set (12)

Ordered by failure mode, worst first, to match the companion email.

| # | Generator | Script | Type | Failure class |
| --- | --- | --- | --- | --- |
| 1 | deletion_mutant_random | problems/inheritance-problems/deletion_mutants/deletion_mutant_random.py | MC | color = data (deletion map) |
| 2 | hla_genotype (3 markers) | problems/dna_profiling-problems/hla_genotype.py | MC | color = data (inline text color = parental chromosome) |
| 3 | pipet_size_mc | problems/laboratory-problems/pipet_size_mc.py | MC | color = data (red digits encode place value) + small stacked layout |
| 4 | metabolic_pathway_inhibitor | problems/biochemistry-problems/enzymes/metabolic_pathway_inhibitor.py | MC | color = identity (figure to text) |
| 5 | which_amino_acid | problems/biochemistry-problems/PUBCHEM/AMINO_ACIDS/which_amino_acid.py | MC | script render (RDKit.js canvas) |
| 6 | linear_digest (length 8, 2 sites) | problems/molecular_biology-problems/linear_digest.py | MA | spacing = data (digest ruler) |
| 7 | classify_Haworth | problems/biochemistry-problems/carbs/classify_Haworth.py | MA | width = data (ring structure) |
| 8 | monohybrid_genotype_statements | problems/inheritance-problems/monohybrid_genotype_statements.py | MC | color = convenience (disambiguate AA/Aa/aa) |
| 9 | photosynthetic_light_pigments | problems/biochemistry-problems/photosynthetic_light_pigments.py | MC | color = convenience (colored terms) |
| 10 | michaelis_menten_table-Km | problems/biochemistry-problems/enzymes/michaelis_menten_table-Km.py | MC | color = convenience (zebra readability) |
| 11 | overhang_sequence | problems/molecular_biology-problems/overhang_sequence.py | FIB | control + monospace probe |
| 12 | yaml_match_to_bbq (column_chromatography) | problems/matching_sets/yaml_match_to_bbq.py | MAT | structural type-drop + reinforces colored-term identity |

## Considered but not used

Item numbers below refer to the selected set (12) above.

### MC / MA / NUM / FIB candidates

| Generator | Script | Type | Class | Why not used |
| --- | --- | --- | --- | --- |
| kaleidoscope_ladder_unknown_band | problems/biochemistry-problems/electrophoresis/kaleidoscope_ladder/kaleidoscope_ladder_unknown_band.py | NUM | color = data (gel bands) | A strong failure, but the colored ladder is big and hard for a non-expert to parse; color=data is covered more cleanly by the deletion map (item 1) and the HLA markers (item 2) |
| monohybrid_degrees_of_dominance | problems/inheritance-problems/monohybrid_degrees_of_dominance.py | MC | color convenience (swatches) | Superseded by the shorter monohybrid_genotype_statements (item 8) |
| dihybrid_cross_epistatic_gene_metabolics | problems/inheritance-problems/epistasis/dihybrid_cross_epistatic_gene_metabolics.py | MA/MC | bgcolor as key | Long 4x4 Punnett; bgcolor convenience covered by the zebra table (item 10) |
| three-point_test_cross-distances_plus | problems/inheritance-problems/gene_mapping/three-point_test_cross-distances_plus.py | MULTI_FIB | width = data | Long; the only MULTI_FIB source, but type coverage is not a showcase goal |
| two-point_test_cross-distance | problems/inheritance-problems/gene_mapping/two-point_test_cross-distance.py | NUM | width = data (progeny table) | Replaced by the shorter digest ruler (item 6) for the layout class |
| protein_gel_migration | problems/biochemistry-problems/electrophoresis/protein_gel_migration.py | NUM | color = data (gel) | Gel-band color=data class; covered by the deletion map (item 1) and HLA markers (item 2), and the kaleidoscope ladder was dropped for the same reason |
| which_macromolecule | problems/biochemistry-problems/PUBCHEM/MACROMOLECULE_CATEGORIZE/which_macromolecule.py | MC | script render + bgcolor guide table | Replaced by the smaller which_amino_acid (item 5); large guide table made it long |
| exon_splicing | problems/molecular_biology-problems/exon_splicing.py | MC | color = identity + width | Strong but longer; the identity class is covered by the pathway item (item 4) |
| serial_dilution_factor_mc (and aliquot/diluent numeric) | problems/laboratory-problems/serial_dilution_factor_mc.py | MC/NUM | color convenience + monospace | Redundant; convenience and monospace already covered |
| xna_and_xdna statements | problems/multiple_choice_statements/yaml_mc_statements_to_bbq.py (-f biotechnology/xna_and_xdna.yml) | MC | isolated text color | Clean probe, but photosynthetic_light_pigments was chosen as the text-color exemplar |
| fret_overlap_colors / fret_permute_colors | problems/biophysics-problems/fret_overlap_colors.py | MC | saturated text color | Long: six full-sentence options; photosynthetic is shorter for the same class |
| metabolic_pathway_allosteric | problems/biochemistry-problems/enzymes/metabolic_pathway_allosteric.py | MC | color = identity | Alternate to item 4 |
| feedback_splitting_pathway / feedback_merging_pathway | problems/biochemistry-problems/enzymes/feedback_splitting_pathway.py | MC | color = identity | Branched-pathway alternates to item 4 |
| beadle_tatum-metabolic_pathway | problems/molecular_biology-problems/beadle_tatum-metabolic_pathway.py | MC | color = identity | Alternate to item 4 |
| robertsonian | problems/inheritance-problems/translocation/robertsonian.py | MC | color = identity + width (chromosome bars) | Long; classes already covered by items 4 and 6/7 |
| gene_tree_choice_plus (same phylogenetic trees) | problems/inheritance-problems/phylogenetic_trees/gene_tree_choice_plus.py | MC | color = identity + table tree | Easy to read but long |
| michaelis_menten_table-inhibition | problems/biochemistry-problems/enzymes/michaelis_menten_table-inhibition.py | MC | color convenience (zebra) | The -Km variant was chosen for the zebra class |

### Matching-set candidates (item 12 slot)

The matching slot was chosen to do double duty: prove the QTI type-drop AND reinforce
a color failure already shown elsewhere. All matching sets colorize their terms with
inline `<span>` color, so any reinforces the color failure; the choice was about which
reinforcement is clearest and shortest.

| Matching set | Script | Reinforces | Why not used |
| --- | --- | --- | --- |
| column_chromatography | problems/matching_sets/yaml_match_to_bbq.py (-f laboratory/column_chromatography.yml) | color = identity | SELECTED (item 12): 4 colored column-type names (IEX/AC/HIC/SEC) recur across the colored descriptions, so it shows color=identity recurrence on one screen |
| monohybrid_cross_genotype | problems/matching_sets/yaml_match_to_bbq.py (-f inheritance/monohybrid_cross_genotype.yml) | color = convenience (AA/Aa/aa) | Strong genetics tie to item 8, but reinforces only convenience-grade disambiguation; column_chromatography reinforces the more critical identity class |
| energy_terms | problems/matching_sets/yaml_match_to_bbq.py (-f biochemistry/energy_terms.yml) | color (thin) | Shortest (2 pairs), but a 2-item match barely reads as a matching question and the color is only 4 short phrases |
| degrees_of_dominance | problems/matching_sets/yaml_match_to_bbq.py (-f inheritance/degrees_of_dominance.yml) | none strong | Original placeholder pick; minimal HTML, so it isolated the type-drop but reinforced no color failure (the double-duty goal) |
| chromosome_shapes | problems/matching_sets/yaml_match_to_bbq.py (-f inheritance/chromosome_shapes.yml) | color (rainbow) | Rainbow term color, but the answer key includes filler distractor strings, making it messy to read |
| protein_v_dna_gels | problems/matching_sets/yaml_match_to_bbq.py (-f laboratory/protein_v_dna_gels.yml) | color (rainbow) | Topically ties to the SDS-PAGE hero, but its spans are rainbow-convenience term color, not gel-band color=data, so the tie is misleading |

## Notes

- Several rejected items (Robertsonian, exon splicing, the branched pathways) are
  excellent questions; they were left out only because their failure class is already
  represented by a shorter exemplar, not because they fail to demonstrate the issue.
- HLA was promoted from a color-identity alternate to the color=data slot (item 2):
  its marker color is required (it marks which parental chromosome each marker came
  from), and it is a short pure-text MC, the cleanest inline-text-color=data proof.
- If type coverage is ever wanted (showing MULTI_FIB round-trips), re-add
  three-point_test_cross-distances_plus as the lone long item.
- The color-identity slot (item 4) is interchangeable among the pathway, Robertsonian,
  and exon variants; the linear biochem pathway was chosen as the shortest.
