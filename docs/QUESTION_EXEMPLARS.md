# Question exemplars

Worked examples for [QUESTION_PEDAGOGY_GUIDE.md](QUESTION_PEDAGOGY_GUIDE.md) and
[QUESTION_VOICE_GUIDE.md](QUESTION_VOICE_GUIDE.md). Each example is labeled **model** (imitate
it) or **fix** (a flaw with a rewrite), and cites the rule it shows as "guide > heading". The
rules themselves live only in the two guides; this file shows them in use. The full corpus
evidence is in [QUESTION_EVIDENCE.md](QUESTION_EVIDENCE.md).

Snapshot note: byte-identical copies live in the vosslab-skills repository under
`skills/experts/bptools-writer-expert/references/docs/` and
`skills/experts/webwork-writer-expert/references/docs/`. Refresh both copies in the same change
that edits this file. Backticked repo paths refer to the biology-problems repository.

Sources: Neil's printed exams (2019 genetics final, 2019 biochemistry exam 1, 2025 genetics
midterm and final), generator text from git snapshot `c3cb2d0` and older commits, current
generator output, and YAML banks. Quotes are verbatim except for HTML entities and emoji; exam
quotes keep their original wording and choice order ("as printed").

## Stems

### Data first, one choice set for sibling questions (model)

2019 genetics final, Q19-21, below a linear map with TaqI and BamHI sites (as printed):

```text
Questions 19-21. Refer to the linear section of DNA below-left. The dashes at the left and
right indicate that the next restriction site is very far away.
19. If you digest the 8kb linear DNA section with only TaqI, which set of fragments will you
obtain?
A. only 3 kb  B. only 4 kb  C. 1 and 2 kb  D. 1 and 3 kb  E. 1, 2, and 3 kb
```

Q20 and Q21 repeat the stem for BamHI and for both enzymes with mostly the same choices; Q22-24
do the same for a "circular DNA plasmid". "linear DNA section" and "circular DNA plasmid" are
underlined. Rules: pedagogy > Data first and shared-figure sets; voice > Emphasis.

### Lab scenario in second person (model)

2019 biochemistry exam 1, Q50:

```text
50. You are purifying a protein with a pI = 5.1. Which one of the following columns and pH
values would you use to purify your protein by attaching it to the column?
A. anion (+) exchange resin, pH 7.0    B. anion (+) exchange resin, pH 3.0
```

Rules: voice > Voice in one paragraph; voice > Lead-ins.

### Transfer to a new case (model)

2019 biochemistry exam 1, Q48 (imitate the stem; choice D is an escape that is never the key):

```text
48. If two alanine residues were separated by 12 other amino acids within a single
beta-strand instead of an alpha-helix, how would their spacing be changed?
A. longer distance than in the alpha-helix      B. same distance as in the alpha-helix
C. shorter distance than in the alpha-helix     D. cannot predict, need the amino acid composition
```

Rule: pedagogy > Name the reasoning target.

### Rule, case, question (model)

`blood_type_mother.py` (snapshot `c3cb2d0`):

```text
For the ABO blood group in humans, the i^A and i^B alleles are codominant and the i allele is
recessive.
A father &male; with blood type AB has a son &male; with blood type A.
Which of the following blood types could the mother &female; possibly have? Check all that
apply.
```

Rule: voice > Rule, case, question.

### State what is counted (fix)

`lethal_allele_survival.py`. An agent draft asked about "If 80 conceptions occur ..."; Neil's
commit `bd221d8` rewrote the count stem as:

```text
Before considering survival, assume the cross produces 96 offspring.
How many would you expect to survive with the wildtype phenotype?
```

Totals are multiples of 12, so thirds and quarters come out whole.
Rules: voice > Rule, case, question; pedagogy > Build the data.

### Background preamble (fix)

`hemoglobin_oxygen_affinity.py`:

- Before: "Hemoglobin is one of the most heavily modulated proteins in the body. Its oxygen
  binding affinity is regulated by multiple physiological factors that shift the balance
  between different conformational states of the protein. Cooler temperatures of the lungs has
  this effect on the normal adult hemoglobin protein:"
- After: "How do the cooler temperatures in the lungs affect the oxygen affinity of adult
  hemoglobin?"

Rules: voice > Keep the stem lean; voice > Lead-ins; voice > Mechanics.

### Facts stated twice (fix)

`fatty_acid_naming_omega.py`:

- Before: "The skeletal structure above shows an unsaturated fatty acid with 20 carbons. The
  methyl end is on the left (H3C) and the carboxyl end (COOH) is on the right. Each vertex and
  line end represents one carbon atom. What is the correct &omega; (omega) notation describing
  the positions of the double bonds in this 20-carbon fatty acid?"
- After (Neil's 2020 wording): "What is the correct &omega; (omega) notation for the 20 carbon
  fatty acid pictured above?"

Rule: voice > Keep the stem lean.

### Filler opener (fix)

2025 genetics final, Q99:

- Before: "Phylogenetic trees are fundamental tools in genetics research, enabling scientists to
  visualize evolutionary relationships among species or populations." (then the reference tree)
- After: start with the reference tree, then "All but one of the trees below show the same
  relationships as the tree above. Which one of the following trees is DIFFERENT?"

Rule: voice > Keep the stem lean.

### Fragment stem (fix)

2019 biochemistry exam 1, Q16:

- Before: "16. A weak acid can act as a buffer at" / "A. body temperatures  B. pH values =
  pKa &plusmn;1  C. pH values = pKa &plusmn;2  D. pH values = pKa &plusmn;0.1"
- After: "Over which pH range does a weak acid act as an effective buffer?" with "pH = pK<sub>a</sub>
  &plusmn; 0.1", "pH = pK<sub>a</sub> &plusmn; 1" (key), "pH = pK<sub>a</sub> &plusmn; 2",
  "pH = pK<sub>a</sub> &plusmn; 3", in ascending order; the off-type "body temperatures" choice is
  gone.

Rules: voice > Lead-ins; voice > Layout and order.

### Generic lead-in, tiny scenario space (fix)

`x_linked_reciprocal_cross.py` renders near-identical items:

- Before: "In fruit flies, eye color is X-linked with red eyes dominant to white eyes. A
  true-breeding red-eyed female is crossed with a white-eyed male. Which statement best
  describes the F1 offspring?"
- After: "In fruit flies, white eyes (w) is an X-linked recessive trait; red eyes (w+) is
  wildtype. A homozygous red-eyed female &female; is crossed with a white-eyed male &male;.
  What fraction of their <u>sons</u> &male; will have white eyes?" with the quarters ladder
  (key: None, 0%). Sibling items ask about daughters, carriers, and the reciprocal cross, and
  the pool varies the trait and the parents.

Rules: voice > Lead-ins; voice > Fixed ladders; pedagogy > Scenario variety.

## Emphasis, hints, and notes

### Hint that resolves ambiguity (model)

2019 genetics final, Q75 (deletion mapping; as printed):

```text
75. What the correct order for the four genes? Hint: the first gene on the end is gene C.
A. CABD   B. CBDA   C. CBAD   D. CDAB   E. CADB
```

The hint removes the reversed-order duplicate answer without solving the map. A generator would
sort these choices alphabetically and fix the typo ("What is the correct order").
Rules: voice > Hints and notes; voice > Layout and order; voice > Mechanics.

### Note that hands over arithmetic (model)

2025 genetics final, Q90:

```text
90. The rabbit-eating tree is found to be decaploid (10n) with 110 chromosomes in total. What
are the monoploid (m) and haploid (h) numbers for this tree? Note: 110/10 = 11 and 110/2 = 55
```

Rules: voice > Hints and notes; pedagogy > Show-the-setup choices.

### Checkable-constraint hint (model)

`deletionlib.py`: "Hint: The correct answer is an English dictionary word of length six (6)."
The constraint lets the student check the gene order without being told the method. Rules:
voice > Hints and notes; pedagogy > Self-checking answers and puzzles.

### Solution-path hint (fix)

`horse_coat_pattern_inference.py`:

- Before: "Hint: Start with the lethal-white count to see whether the stallion can pass an O
  allele. Then use the fewspot count, remembering that O/O foals are counted as lethal white."
- After: remove the hint. Keep one rule sentence per locus, the offspring-count table, and
  "Which one of the following stallion genotypes can produce all six (6) offspring counts?";
  move the source citations to code comments.

Rules: voice > Hints and notes; voice > Keep the stem lean.

## Choices

### Show the setup (model)

2019 genetics final, Q61-63 (three-point cross, 6,000 progeny; parentals + b c and a + +,
double crossovers + b + and a + c, so the gene order is A-C-B). Choices as printed:

```text
Gene distances. Match the following lettered distances to the appropriate numbered pair of
genes. Not all letters will be used.
A. (493+476+29+22)/6000 = 17.0 m.u.     B. (131+118+29+22)/6000 = 5.0 m.u.
C. (493+476)/6000 = 16.2 m.u.           D. (131+118)/6000 = 4.1 m.u.
E. (493+476+131+118)/6000 = 20.3 m.u
61. Distance between genes A and B?   62. Distance between genes A and C?
63. Distance between genes B and C?
```

Keys: Q61 E (20.3), Q62 A (17.0), Q63 B (5.0). C and D leave the double crossovers out, the
classic error; they are the unused letters. (Rounded as printed: 16.15 shows as 16.2 and 4.15 as
4.1; code should round consistently.) A generator would list these by result.
Rules: pedagogy > Show-the-setup choices; pedagogy > Error-derived distractors.

### Formula variants as distractors (model)

2019 genetics final, Q41 (as printed):

```text
41. A women has six children, what is the probability that she has exactly 3 boys and 3 girls?
A. 6!/(3!(6-3)!) (1/2)^6 = 31.3%     B. 9!/(3!(9-3)!) (1/2)^9 = 16.4%
C. 6!/(3!(6-3)!) (1/2)^9 = 3.9%      D. 6!/3! (1/2)^9 = 23.4%
```

A generator would sort by result and fix the mechanics: "A woman has six (6) children. What is
the probability ...?" Rules: pedagogy > Show-the-setup choices; voice > Mechanics.

### Fixed ladder across a multi-part story (model)

2019 genetics final, Q48-55 (as printed; "co-dominant" is the exam's shorthand, since O is
recessive):

```text
A color-blind woman with type B blood marries a man with normal vision and type A blood. They
have a color-blind son with type O blood. ABO blood groups are autosomal co-dominant, and
red-green color-blindness is X-linked recessive.
52. What fraction of their sons will have normal vision?
A. None, 0%  B. 1/4, 25%  C. 1/2, 50%  D. 3/4, 75%  E. All, 100%
53. What fraction of their daughters will have normal vision AND have type AB blood?
```

"sons", "daughters", "vision", and "type AB blood" are underlined.
Rules: pedagogy > Multi-part stories; voice > Fixed ladders; voice > Emphasis.

### Natural order and type labels (model)

`monohybrid_litter_inference.py` after Neil's correction lists choices as "HH (homozygous
dominant)", "Hh (heterozygous)", "hh (homozygous recessive)" in that order. Lethal-genotype count
choices are sorted ascending: "0 &times; 48 = 0 offspring", "1/3 &times; 48 = 16 offspring",
"1/2 &times; 48 = 24 offspring", "2/3 &times; 48 = 32 offspring", "1 &times; 48 = 48 offspring".
Rules: voice > Layout and order; voice > Parallel form.

### Key is the only long, qualified choice (fix)

`delta_g_prime_standard_state.py`. Stem: "Which condition is specified differently in the
biochemical standard state than in the chemical standard state?"

- Before: key "pH is fixed at 7 ([H+] = 1 &times; 10<sup>-7</sup> M instead of 1 M)" beside
  "pressure is different from 1 atm" and "temperature is different from 298 K (25 &deg;C)".
- After: one frame for every choice, each wrong choice a named error:
  - "the H<sup>+</sup> concentration is fixed at 10<sup>-7</sup> M" (key)
  - "the H<sup>+</sup> concentration is fixed at 1 M" (the chemical standard state)
  - "the temperature is fixed at 37 &deg;C" (body temperature)
  - "the solute concentrations are fixed at 1 mM" (physiological concentrations)
  - "the pressure is fixed at 1 atm" (the same in both states)

Rules: voice > Parallel form; pedagogy > Error-derived distractors.

### Answer-revealing gloss (fix)

`exergonic_endergonic_reactions.py`: "endergonic (energy-absorbing)" and "exergonic
(energy-releasing)" teach the answer inside the choice. After: "endergonic", "exergonic", "at
equilibrium". Rule: voice > Parallel form.

### Invented names not tied to the allele letter (fix)

`lethal_allele_survival.py`: "C is dominant to c, so C_ produces the doubled phenotype and cc
produces the zippy phenotype." After: draw the allele letter from the phenotype name, for
example "The dewy allele D is dominant to the wildtype allele d. Dd flies are dewy, dd flies are
wildtype, and DD is lethal." Rule: pedagogy > Names and invented worlds.

## Seriously absurd choices

### Absurd choices delivered deadpan (model)

- `g-u_wobble.yml` false statement: "the G&middot;U wobble base pair is named for famous
  scientist Chandler Wobble."
- `xna_and_xdna.yml` false statement: "xDNA stands for extreme DNA because it does not denature
  even in boiling water (100&deg;C)"
- `tetrad_unordered_two_gene-test_linkage.py` choices: "The two genes are NEITHER linked NOR
  unlinked." / "The two genes are BOTH linked AND unlinked."
- `metabolic_pathway_inhibitor.py` choices: "molecular stopper", "proteomic pothole",
  "catalytic converter".

Each can sit beside error-derived choices and matches their grammar and length; select enough
meaningful alternatives to assess the intended reasoning rather than applying a numerical quota.
Rule: pedagogy > Seriously absurd choices.

### Absurd choice that breaks register (fix)

`long_run_pcr.yml`: "long range PCR can amplify long target DNA sequences up to an amazing
3,000 kb". The word "amazing" marks it as the odd one out. After: "long range PCR can amplify
long target DNA sequences up to 3,000 kb", matching its true sibling "... up to 30 kb".
Rule: pedagogy > Seriously absurd choices.

## Distractor recipes (error, code, rendered choice)

### Dilution

`dilution_factor_mc.py` (snapshot `c3cb2d0`; comments added here) builds wrong volume pairs
from named role errors, where `format_volumes(aliquot, diluent)`:

```python
wrong = format_volumes(vol2, volume)   # diluent volume used as aliquot, total as diluent
wrong = format_volumes(volume, vol1)   # total volume used as aliquot
wrong = format_volumes(vol1a, vol2a)   # aliquot doubled, diluent recomputed
wrong = format_volumes(vol2, vol1)     # aliquot and diluent swapped (always kept)
```

Rendered (`serial_dilution_factor_mc.py`): key "150.0 ... previously diluted sample (aliquot)
/ 120 ... distilled water (diluent)" beside the swap "120.0 ... (aliquot) / 150 ...
(diluent)". Rules: pedagogy > Error-derived distractors; voice > Numbers, units, and symbols.

### Transcription

`rna_transcribe_prime.py` (snapshot `c3cb2d0`; comments added here):

```python
choice_list.append(question_seq)                 # template copied
choice_list.append(seqlib.flip(question_seq))    # template reversed
choice_list.append(seqlib.flip(answer_seq))      # complement written the wrong direction
nube = question_seq[:half] + answer_seq[half:]   # half-and-half chimera
choice_list.append(nube)
```

The display direction of the template and choices is randomized (5'-3' or 3'-5'), so reading
the labels is part of the skill. Rule: pedagogy > Error-derived distractors.

### Lethal genotypes

Survivor fractions are 1/3 and 2/3; the classic error ignores lethality and gives 1/4 and 3/4.
The current generator includes both pairs in every fraction or count item and weights scenarios
with thirds keys 8 to 1. Rules: pedagogy > Error-derived distractors; pedagogy > Misconception
placement.

### Restriction digests

The digest generators place the non-selected enzyme's site on the 0 kb mark (from
`docs/HUMAN_GUIDANCE.md`), so the student who assumes a cut at 0 picks a wrong band set. Rule:
pedagogy > Misconception placement.

### Statement swap

`dna_structure.yml`: true "hydrogen bonds hold the two strands together"; false "ionic bonds
hold the two strands together", "phosphodiester bonds hold the two strands together",
"disulfide bonds hold the two strands together", "peptide bonds hold the two strands together".
Rule: pedagogy > One-term swaps.

## Statement banks

### Out-of-scope and bracketed values (model)

- `franklin_diffraction.yml`, stem "What information was NOT obtained from Rosalind Franklin's
  diffraction pattern in Photograph 51?", key "DNA is the genetic material responsible for
  inheritance" (true fact, outside the photograph's evidence; in a TRUE bank it would serve as a
  false choice).
- `pcr_primers.yml`: true "the primers are about 18 to 30 nucleotides in length"; false "the
  primers are shorter than 10 nucleotides in length" and "the primers are at least 50
  nucleotides in length, if not longer".

Rule: pedagogy > Out-of-scope facts and bracketed numbers.

### Hedges on true, absolutes on false (fix)

`senses_chemosensation_smell_taste.yml` (17 of 25 true statements hedged):

- Before: TRUE "Salty taste commonly involves ion movement through channels rather than GPCR
  signaling." FALSE "A single olfactory sensory neuron expresses every odorant receptor type."
- After (topic "smell and taste receptors"): true "each olfactory sensory neuron expresses only
  one odorant receptor gene"; false "each olfactory sensory neuron expresses every odorant
  receptor gene"; false "each olfactory sensory neuron expresses only one taste receptor gene".

The true statement now carries the absolute word, and both sides share one frame.
Rules: pedagogy > Balanced hedges and absolutes; voice > Statement bank form.

### Explanation on the key only (fix)

`protein_stability.yml`:

- Before: TRUE "Asparagine and glutamine make proteins less stable at high temperature because
  they lose their amide groups." FALSE "Asparagine and glutamine make proteins more stable at
  high temperature."
- After: true "asparagine and glutamine make proteins less stable at high temperature"; false
  "asparagine and glutamine make proteins more stable at high temperature".

Rule: voice > Parallel form.

## Matching sets

### Applied pairing with mirrored values (model)

- `monohybrid_cross_genotype.yml`: "Aa x aa" matched to "Half of the offspring display the
  recessive phenotype".
- `chi-square_terms.yml`: the chi2 statistic is "the bigger this number, the smaller the
  p-value"; the p-value is "the smaller this number, the bigger the chi2 test statistic".

Rules: pedagogy > Applied pairings; pedagogy > Values without cues.

### Value repeats the key (fix)

`senses_signal_transduction_matching_set.yml`:

- Before: "IP<sub>3</sub>: Molecule that opens IP<sub>3</sub> receptors on internal
  Ca<sup>2+</sup> stores"
- After: "IP<sub>3</sub>: second messenger that releases Ca<sup>2+</sup> from the endoplasmic
  reticulum"

Rule: pedagogy > Values without cues.

### Giveaway date (fix)

`biotechnology_periods_and_milestones.yml`:

- Before: key "Classical times (1800-1945):" with value "Penicillin discovered by Alexander
  Fleming (1928)"
- After: value "penicillin discovered by Alexander Fleming"

Rule: pedagogy > Values without cues.

### Letter-use instruction with mnemonic labels (model)

2019 biochemistry exam 1, Q1-8:

```text
For each of the following numbered chemical structures below match the correct lettered
macromolecular category. Letters will be used more than once; all letters will be used.
A. Nucleic [A]cid   B. Protein   C. [C]arbohydrates   D. Lipi[D]s
```

Rule: voice > Matching.

## Puzzles, stories, and worlds

### Invented names that help memory (model)

- 2025 genetics final, Q75-79: phenotypes "bumpy, waxy, yucky" for genes b, w, y in a
  three-point cross with 290,000 progeny.
- 2025 genetics midterm, Q92-93: "On planet Zygora, the glowstem plant species has two
  independent traits. Gene B controls leaf color (B = fluorescent blue, b = dull black), and
  gene R controls seed shape (R = round, r = spiked)."

Rule: pedagogy > Names and invented worlds.

### Error analysis (model)

`chi_square_errors.py`: a worked chi-square table with one deliberate mistake, then "However, it
appears they made an error. What did they do wrong?" Choices name each possible mistake: "The
numbers in the calculation have to be squared and they are not squared." / "The degrees of
freedom is wrong, it should be a different value." Rule: pedagogy > Name the reasoning target.

### Cannot be determined, used correctly (model)

`poisson_flies.py` (snapshot `c3cb2d0`): when every offspring is wildtype, the key is
"homozygous wildtype female (++) and male of unknown genotype", because the father's allele
cannot be determined from the data. Rule: pedagogy > Cannot be determined.

## Entry rules and mechanics

### Fill-in-the-blank entry rule (model)

`three-point_test_cross-distances_plus.py`: "Your answer should be written as a numerical value
only, with no spaces, commas, or units such as "cM" or "map units". For example, if the
distance is fifty one centimorgans, simply write "51"." Rule: voice > Fill in the blank and
numeric.

### Template slips (fix)

- "A black female mates with a orange male." -> "an orange male" (`x_linked_tortoiseshell.py`)
- "complimentary to the sequence" -> "complementary" (2019 genetics final, Q8)
- "How much liquid do you add to make a total of 270 &micro;L?" with choices in mL -> choices in
  &micro;L (`serial_dilution_factor_mc.py`)
- "hh.A pea plant" -> "hh. A pea plant" (`monohybrid_litter_inference.py`)

Rules: voice > Mechanics; voice > Numbers, units, and symbols.
