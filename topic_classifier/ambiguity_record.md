# Resolved Classification Ambiguities

Reviewer: Codex, 2026-07-12. No unresolved cases remain.

| Variant or group | Candidates considered | Final decision | Rationale |
| --- | --- | --- | --- |
| Basic DNA base pairing, Chargaff ratios, and DNA melting | introductory DNA chapters versus replication/PCR chapters | Biochemistry `nucleic_acids`; biotechnology `dna_genomics`; genetics and molecular biology `dna_structure` | These assess DNA composition and complementarity, not replication machinery or an applied PCR workflow. |
| PCR amplicon copy counting | molecular biology `dna_replication` versus `restriction_pcr`; biotechnology relevance | Molecular biology `restriction_pcr`; biotechnology `dna_genomics` | The mechanism assessed is PCR amplification. Copy-count arithmetic is conceptual rather than a laboratory outcome, so laboratory coverage is reserved for experimental design and result interpretation. |
| Consensus-sequence generators | molecular biology DNA structure, cloning/sequencing, or translation | `cloning_sequencing`; biotechnology `dna_genomics`; laboratory `bioinformatics` | Students infer a consensus from an alignment, an analytical sequencing/bioinformatics task rather than a base-pairing task. |
| Beadle-Tatum pathway and mutant-screen generators | molecular biology historical experiments, genetics gene interactions, or a biochemical metabolism chapter | Molecular biology `landmark_experiments`; genetics `gene_interactions`; biotechnology `biotech_basics` | The questions model one-gene/one-enzyme mutant complementation and pathway epistasis; no specific biochemical pathway is tested. |
| Polyploid chromosome-number generators | chromosomal inheritance versus chromosomal disorders | Genetics `chromosomal_disorders` | They classify abnormal whole-genome chromosome number and calculate its consequences, rather than tracing sex-linked inheritance. |
| Box plot derived from a CDF | distributions versus graph interpretation | Biostatistics `graph_reading` | The task is extracting quartiles from a plotted cumulative distribution and constructing/interpreting the display. |
| Generic chi-square questions | biostatistics hypothesis testing versus genetics chi square | Both subjects, one chapter each | The same test is directly usable as general inference and as evaluation of genetic-ratio expectations. |
| Cell membranes and sensory-system YAML banks | biochemistry chapters versus cell biology | Both subjects, one chapter each | The banks directly assess biochemical membrane/sensory mechanisms and core cell-biological structures or signaling. |

All baseline task-file placements were treated as authoritative. Ambiguity
analysis governed only newly added subject/chapter rows; no baseline row was
moved, removed, normalized, or de-duplicated.
