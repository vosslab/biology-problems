# Topic 04 homework

## Ten-point selection

Choose one question from each row. For 10 points, keep culture enrichment at **2 points**
and assign **1 point** to each of the other eight questions in Blackboard.
The task CSV selects banks; it does not set assignment point values.

| Question | Format | Bank or generator |
| --- | --- | --- |
| Culture enrichment | Matching | `culture_enrichment.yml` |
| Plant transgenes | Matching | `plant_transgenes.yml` |
| xDNA and XNA | TFMS | `xna_and_xdna.yml` |
| Current-year Nobel Prize topics (2026) | TFMS | `nobel_prizes.yml` |
| 16S survey steps | MC | `python3 problems/ordering/yaml_mc_order_to_bbq.py -y problems/ordering/biotechnology/microbial_16s_survey.yml` |
| Remediation sites | Matching | `remediation_sites.yml` |
| Biofuel sources and challenges | Matching | `biofuels.yml` |
| Glucose measurement through skin | MC | `bloodless_glucose.yml` |
| Agrobacterium, gene guns, and CRISPR | TFMS | `plant_gene_methods.yml` |

The biofuel bank randomly chooses a source or challenge description for each of its four
types. Each type has six descriptions: three about sources and three about challenges.

Matching banks also produce WOMC alternatives on BPW. These are alternatives, not extra
questions in this ten-point assignment. The glucose bank uses the statement generator
but asks a direct MC question. TFMS questions are also stored as MC records.

## Content and sources

These are broad, open-book familiarity questions, as requested for a course without exams.
Students identify sites, sources, production challenges, and basic methods. They do not
design experiments or explain detailed molecular mechanisms.

The source is `LECT06/djot/lect06c-set_4_tp_chapter_12_16_material.djot` and its included
chapter files in the instructor's `djot-slide-builder/biotech` checkout:

- Chapter 12, talking points 4-9: every remediation site is named in these slides.
  The category identifies the pollution discussed, not a claim that cleanup succeeded.
- Chapter 13, talking points 14-17: biofuel sources and challenges. Challenges belong to
  the stated examples; the questions do not claim that each challenge affects only one fuel.
- Chapter 14, talking point 22: other substances in skin affect the light signal used
  for glucose readings. The question asks why this is difficult, not impossible.
- Chapter 15, talking points 24-25: Agrobacterium and gene guns. The instructor also
  requested the basic fact that CRISPR is used to edit a chosen DNA sequence.

The old 2021 quiz supplied the six-step 16S workflow. The 2016 textbook chapters 12-16
were background sources, not the source of new sites students would need to look up.

## Answers and wrong choices

| Site in the slides | Category |
| --- | --- |
| Exxon Valdez; Deepwater Horizon | Hydrocarbon remediation |
| Hudson River; Love Canal | Chemical spill remediation |
| Kerala | Pesticide remediation |
| Chernobyl; Fukushima | Nuclear remediation |
| Hinkley; Berkeley Pit | Heavy metal remediation |
| East Metro Twin Cities (Minnesota); Parkersburg | Forever chemical remediation (PFAS) |

Each matching question draws four sites from four different categories. Exclusions stop
two sites with the same answer from appearing together, including in WOMC alternatives.

| Question family | Correct idea | Mistakes represented by wrong choices |
| --- | --- | --- |
| 16S MC | Collect, extract DNA, PCR, sequence, cluster, analyze abundance | Swap neighboring stages or reverse the workflow |
| Remediation matching | Pair each site with its slide category | Confuse the pollution associated with two sites |
| Biofuel sources matching | Grain; plant cell walls; oils/fats; oils from algae | Swap the four starting materials |
| Biofuel challenges matching | Food use; tough walls; used-oil processing; extracting oil from cells and separating cell material | Swap the four production examples |
| Glucose MC | Other skin substances also affect light | Assume no glucose signal, no light through skin, glucose only inside cells, or light destroys glucose |
| Plant TFMS | Bacterial DNA transfer; DNA-coated particles; gold; CRISPR editing; gene-gun name | Swap bacteria with viruses/fungi, particles with microbes/pollen, or CRISPR with a carrier |

The plant statements deliberately stay at the level of familiar tools and their uses.
They do not assess guide RNA, DNA repair, insertion-site choice, or delivery of CRISPR components.

## Validation record

### Plant bank wording review

The plant bank now has eleven prompts with three descriptions each. Each question still
draws four pairs. Descriptions may restate the same fact: alternate wording is intentional,
not a claim that each version teaches a different fact. Labels name a gene or construct;
descriptions state its function in similar amounts of detail.

Before: `aro A (Glyphosate Resistant)` matched `Allows for resistance to glyphosate herbicides`.
After: `Modified aroA gene` matches any of these:

- Allows plants to keep making amino acids when treated with glyphosate
- Produces a form of EPSPS that still works in the presence of glyphosate
- Produces an enzyme that resists glyphosate, the herbicide sold as Roundup

The humanizer pass removed praise, filler, and vague claims. The bptools voice pass removed
answer hints from labels and checked that each description has one clear match. The unnamed
mangrove gene was removed. Medical protein production now uses human antibody genes;
the shelf-life example now names an antisense PG construct (PG is polygalacturonase).
It asks about reduced pectin breakdown, not a claim that fruit stops ripening.

The wrong matches represent swapped functions: insect toxin versus stress regulation,
vacuolar proton pump versus sorbitol production, and glyphosate versus sulfonylurea versus
atrazine resistance. Each herbicide description names its target chemical or pathway.
A separate reader checked all 33 descriptions. Six focused matching tests passed, and
MATCH/WOMC samples were generated and reviewed in the browser. The text checker is advisory:
gene names vary naturally in length, and shared words such as `gene` or `protein` are not
removed when they are needed to name the material accurately.

Supporting primary studies for the less familiar examples:
[gutD in maize](https://pubmed.ncbi.nlm.nih.gov/18726503/),
[AVP1](https://pubmed.ncbi.nlm.nih.gov/11572991/), and
[antisense polygalacturonase](https://pubmed.ncbi.nlm.nih.gov/16593997/).

### Topic checks

Before: the 16S question was an `ORD` record with the six answers stored in order.
After: an `MC` record lists shuffled, numbered steps and offers four sequences.
For displayed steps clustering, extraction, collection, PCR, sequencing, abundance,
the correct answer is `3 -> 2 -> 4 -> 5 -> 1 -> 6`.

- The YAML ordering migration now retains all six steps in every instance. Its focused
  checks reconstruct the MC key from displayed labels and check four distinct complete
  sequences. Both native and MC samples passed browser and QTI export checks; see the
  [implementation evidence](yaml_ordering.md).
- Ran the four focused matching/statement YAML test modules: 17 tests passed.
- A separate reader checked all five new banks against the slides. Replaced extra source
  examples with slide wording and corrected the CRISPR source note.
- Read generated samples and opened browser self-tests for all six new or converted banks.
  The numbered 16S list, MC choices, and matching controls displayed correctly.
- The final advisory text check found no issues in 16S, remediation, biofuel sources,
  biofuel challenges, or glucose samples. One plant sample shared the word `plant` between
  stem and key. Retained: it names the subject and appears in both true and false statements.
- Narrow existing-bank fixes: label DNA-SIP explicitly to distinguish it from RNA-SIP;
  use DNA rather than mRNA for the environmental subtraction example; remove the incorrect
  XNA base-count claim. The Nobel bank now asks only for a 2026 topic, with earlier years
  as distractors. Refresh it after each year's announcements; there is no NOT-question form.

The local BPW topic build completed with the new banks and MC workflow. Its unrelated
missing genetics generator prevented global orphan cleanup; the old topic04 ORDER bank
was removed explicitly. No website deployment or Blackboard import/grading test was performed.
