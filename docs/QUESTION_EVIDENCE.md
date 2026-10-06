# Question evidence

Evidence base for [QUESTION_PEDAGOGY_GUIDE.md](QUESTION_PEDAGOGY_GUIDE.md),
[QUESTION_VOICE_GUIDE.md](QUESTION_VOICE_GUIDE.md), and
[QUESTION_EXEMPLARS.md](QUESTION_EXEMPLARS.md): the corpus audit of this repository's questions
and the verified published research and book passages behind the rules. Collected 2026-10-02
and 2026-10-03 from Neil's exams, generator output, YAML banks, git history, changelogs, journal
articles, and local book conversions. Quotes are verbatim except for HTML entities used to keep
this file ASCII. This file holds evidence, not rules; the rules live in the two guides.

Snapshot note: byte-identical copies live in the vosslab-skills repository under
`skills/experts/bptools-writer-expert/references/docs/` and
`skills/experts/webwork-writer-expert/references/docs/`. Refresh both copies in the same change
that edits this file. Backticked repo paths refer to the biology-problems repository.

## Why this evidence was collected

Questions written through the `bptools-writer-expert` skill had correct Python but
student-facing text that Neil had to rework by hand. Reading every file of that skill showed
no guidance at all on stems, distractors, emphasis, or pedagogy. This file records what good
questions in this repository look like, what goes wrong, and the evidence for each rule in the
guides. It also serves as source material for a future manuscript on the bptools corpus.

## Sources

- Neil's printed exams, gitignored in `~/nsh/PROBLEMS/exam-formatting-tools/ARTIFACTS/`:
  `2019_exam2-final.pdf` (2019 genetics final), `exam1-chap1-5.pdf` (2019 biochemistry exam 1),
  `2025_genetics_final_exam2.pdf`, `2025_genetics_midterm_exam1-edit.pdf`. Neil approved
  verbatim quotes.
- Pre-agent generator text: git snapshot `c3cb2d0` (2025-11-19, last commit before coding
  agents) and older commits. Rendered website files
  (`biology-problems-website/site_docs/**/human_readable-*.html`) reflect current code, which
  agents edited in 2026.
- 2026 generators and YAML banks (AI-drafted text, often on Neil's concepts).
- Neil's 2026 hand corrections: commits `bd221d8`, `208524c`, `61101b0`, `75e704d`, and
  changelog entries in `docs/CHANGELOG.md` and `docs/CHANGELOG-2026-09a.md`.
- `docs/HUMAN_GUIDANCE.md` and statements Neil made during the audit session.

## Neil's statements during the audit session

- "my content is not perfect either, we are trying to develop best practices"
- "I love seriously absurd choices"
- "organism complexity is my think, I like to point out that flies have legs, eyes, and a
  brain whereas worms do not; thus worms are less complex than flies. Simple stuff, more for
  model organism selection in biotech. Do not assume everything is AI."
- "I am not a writer. I hate writing. I am a thinking and problem/puzzle solver with strong
  math mind"
- "Plan milestones should not require human interaction"

## Exams: what Neil's printed questions look like

### Stems

- Data first, then one bold question sentence. 2019 genetics Q1-4: a mutant-class growth
  table, then "Questions 1-4. A mutant screen was carried out to produce the above diagram.
  ..." and "1. Which one of the following reactions is the first (1st) reaction in the
  pathway?"
- "Which one of the following ..." is the default lead-in: "Which one of the following is
  TRUE regarding melting temperature of DNA, Tm?" (TRUE underlined); "Which one of the
  following crosses represents a test-cross?"
- Short direct questions: "26. Based on the DNA gel profile below-left, who is the father of
  the child?"; "27. ... which suspect dropped blood at the crime scene?"
- Second person for lab work: "50. You are purifying a protein with a pI = 5.1. Which one of
  the following columns and pH values would you use to purify your protein by attaching it to
  the column?"; "39. You are preparing a karyotype for a patient, during which phase of cell
  division do you take a snapshot of the cell?"
- Conversational scope: "We are ignoring sex-linked disorders."; "A Punnett square is
  provided for your convenience, but will NOT be graded."
- Transfer: "48. If two alanine residues were separated by 12 other amino acids within a single
  beta-strand instead of an alpha-helix, how would their spacing be changed?" with option
  "D. cannot predict, need the amino acid composition".

### Emphasis on the discriminating word

- Underlined: "linear DNA section" vs "circular DNA plasmid" (Q19-24); "woman" vs "man",
  "sons" vs "daughters", "carriers", "type O blood" (Q48-55).
- Capitals: NOT, EXCEPT, LEAST, TRUE, FALSE, DIFFERENT. "Which two of the following ...
  Choose two answers." (underlined). "Multiple answers may be correct."
- 2025 exams color the contrasted terms: "Which one of the following statements is FALSE
  concerning mitosis and meiosis cell division?" with mitosis and meiosis in two colors;
  female and male in two fixed colors throughout.

### Hints and notes

- Resolve ambiguity, never teach the answer: "75. What the correct order for the four genes?
  Hint: the first gene on the end is gene C."
- Point at a trap: "Hint: pay close attention to the 5' and 3' directions of the strand."
- State the figure's rule: "Note: The dashes at both ends of the strand indicate the next
  restriction site is far away and outside the visible region. Because this segment is part of
  a much larger molecule, any uncut or very large fragments will not travel into the gel and
  will appear to be stuck in the well."
- Hand over arithmetic: "90. The rabbit-eating tree is found to be decaploid (10n) with 110
  chromosomes in total. ... Note: 110/10 = 11 and 110/2 = 55"

### Choices

- Show the setup, so the student judges reasoning rather than arithmetic:
  - "A. (493+476+29+22)/6000 = 17.0 m.u." / "C. (493+476)/6000 = 16.2 m.u." /
    "D. (131+118)/6000 = 4.1 m.u." (2019 Q61-63)
  - "A. 0.162x0.041x6000 = 39.9" / "B. 0.170x0.050x6000 = 51.0" (2019 Q65)
  - Binomial variants: "6!/(3!(6-3)!) (1/2)^6 = 31.3%" vs "9!/(3!(9-3)!) (1/2)^9 = 16.4%" vs
    "6!/(3!(6-3)!) (1/2)^9 = 3.9%" (2019 Q41)
  - "A. 2^2 = 4 (i.e., two genes with two forms each)" (2025 Q30)
  - "A. 1/16x160 = 10 ... E. 9/16x160 = 90" (2025 midterm Q93)
- Fixed fraction ladder: "A. None, 0% B. 1/4, 25% C. 1/2, 50% D. 3/4, 75% E. All, 100%"
  reused across many questions.
- One choice set shared by a family of questions (Q19-21 digests; Q56-60 genotype pairs).
- Yes/No with reason, bold on the key words: "A. No, expected and observed numbers are
  similar." / "D. Yes, expected and observed numbers are quite different."
- Deliberate misconception options: "D. cross-over does not occur during meiosis";
  "D. cannot be determined".

### Matching instructions

- "Letters will be used exactly once." / "Letters will be used more than once; all letters
  will be used." / "Some letters will be used more than once; not all letters will be used." /
  "Only one letter will not be used." / "All letters will be used; one letter is used twice."
- Mnemonic labels: "A. Nucleic [A]cid  B. Protein  C. [C]arbohydrates  D. Lipi[D]s".

### Stories, puzzles, invented names

- Multi-part family story: "A color-blind woman with type B blood marries a man with normal
  vision and type A blood. They have a color-blind son with type O blood." then eight
  questions (Q48-55).
- Real quirky biology: "The sparrow with four sexes. In particular species of sparrow, a
  mutation has flipped a large section of chromosome 2 ..." (Q87-88).
- Named characters: "A man named David is a carrier for CF but unaffected by AIS. ... A woman
  named Laura ..." (2025 midterm Q82-84).
- Fictional worlds: "On planet Zygora, the glowstem plant species has two independent traits."
- Letter-matched invented phenotypes: "bumpy, waxy, yucky" for genes b, w, y (2025 Q75-79).
- Fantasy taxa: "Rynoth, Ashen, Inktoad, Phoenix, Gorret, Unicorn" (2025 Q99).
- Palindrome completion puzzles: "The following numbered sequences only contains half of a
  palindromic sequence. Match the correct lettered sequence that would finish and replace the
  'N's ..."

### Weaknesses found in the exams

- Typos: "complimentary" (complementary), "A women has six children", "What the correct order",
  "would present in the gametes".
- Incomplete-sentence stems that fail the cover-the-options rule: "16. A weak acid can act as
  a buffer at", "17. Buffer solutions".
- Filler openers (2025): "Phylogenetic trees are fundamental tools in genetics research,
  enabling scientists to visualize evolutionary relationships among species or populations.";
  "HLA genotyping serves as a key component in the field of immunogenetics."
- Definitions inside lead-ins, once pasted onto the wrong item: "76. Identify the double
  crossover genotype combinations. These are the allele combinations that the parent fruit
  flies originally carried."

## Pre-agent generators

Two layers. Layer A (2018-2022 originals) is short and blunt; Layer B (2023 to Nov 2025
rewrites) adds headers, background paragraphs, and some tool-assisted formality.

- Layer A: `who_killer_html` (2022): "Who is the killer?" then "Based on the DNA gel profile
  above, which suspect left blood at the crime scene?"; `chymotrypsin_substrate` (2022):
  "Given the following peptide sequence, ..., at which peptide bond location will chymotrypsin
  most likely cleave first?"
- Layer B: `who_killer_html` (2023): "In adherence to the principles of due process, all
  individuals in this exercise shall be presumed innocent until proven guilty beyond a
  reasonable doubt in a court of law."

### Stem patterns

- Rule sentence, case sentence, question (`blood_type_mother`): "For the ABO blood group in
  humans, the i^A and i^B alleles are codominant and the i allele is recessive." / "A father
  &male; with blood type AB has a son &male; with blood type A." / "Which of the following
  blood types could the mother &female; possibly have? Check all that apply."
- Figure pointers: "Using the table (above), calculate the value for the Michaelis-Menten
  constant, K_M." (`michaelis_menten_table-Km`); "Look at the metabolic pathway in the table
  above." (`beadle_tatum`).
- Short questions: "How much liquid do you add to make a total of {volume}?"
  (`dilution_factor_mc`); "Which pipet and setting would you use to pipet {volume} using only
  one step?" (`pipet_size_mc`); "What is the correct order of the six (6) genes?"
  (`deletionlib`).
- Numbers spelled with digits: "two (2)", "three (3)", "six (6) genes".

### Hints, notes, and entry rules

- "Hint 1: the first gene on the end is gene %s." (`deletion_mutants`, 2022)
- "Hint: pay close attention to the 5&prime; and 3&prime; directions!" (`rna_transcribe_prime`)
- "Note: {56}/{14} = {4} and {56}/2 = {28}" shown in random order (`polyploid-gametes`)
- "Hint: I tried to make this question pretty easy and it does not require a calculator."
  (`dna_melting_temp`)
- FIB entry rules with a worked example: "Your answer should be written as a numerical value
  only, with no spaces, commas, or units such as "cM" or "map units". For example, if the
  distance is fifty one centimorgans, simply write "51"." (`three-point_test_cross-distances_plus`);
  "Note: Do not enter a percentage on the blank. For example, if the answer is 12.3%, enter 0.123
  on the blank." (`hardy_weinberg_numeric`)
- Self-check: "Deletion questions can be hard to solve, but once you have an answer, it is easy
  to check if it is correct!" (`deletionlib`)

### Distractor recipes (each wrong choice is a named mistake)

- Dilution (`dilution_factor_mc`, 2022): swapped aliquot/diluent; diluent or total used as the
  aliquot; doubled aliquot.
- Transcription (`rna_transcribe_prime`): template copied; template reversed; complement not
  reversed; half-and-half chimera (`nube = question_seq[:half] + answer_seq[half:]`).
- PCR primers (`pcr_design`): one primer flipped; both flipped (5'/3' orientation error).
- Amplicon copies (`amplicon_copies`): consecutive powers of two around 2^n vs 2^(n-2).
- Orders of magnitude (`orders_of_magnitude_mc`): decimal moved the wrong way; x10 and x100
  versions; sorted numerically.
- Polyploid gametes: ploidy, 2x ploidy, monoploid, total, sorted ascending as "{n} chromosomes".
- Gene-map distance (`genemapclass`): every choice a full worked calculation pairing the wrong
  progeny classes.
- Z-score biodiversity (`z_score_table_interp`): "Mid-range Overall with Highest Individual
  Z-score: A distractor with one high individual value".
- Chi-square error finding (`chi_square_errors`): "However, it appears they made an error. What
  did they do wrong?" with choices such as "The numbers in the calculation have to be squared
  and they are not squared."
- Restriction digests (HUMAN_GUIDANCE): non-selected enzyme placed on the 0 kb mark because
  students assume DNA is always cut at 0.

### Absurd choices and humor (Neil: "I love seriously absurd choices")

- Fake jargon (`metabolic_pathway_inhibitor`): "molecular stopper", "metabolic blocker",
  "biochemical brake", "proteomic pothole", "catalytic converter"; (`overhang_type`): "hanger
  end", "straight edge".
- Absurd logic (`tetrad`): "The two genes are NEITHER linked NOR unlinked." / "... BOTH linked
  AND unlinked."
- Lab partner: "Your lab partner is trying again (eye roll) and did another a chi-squared test";
  "Before you ask your instructor for a new lab partner, tell them which table is correct AND
  whether they can reject or fail to reject the null hypothesis".
- Fictional diseases (`hardy_weinberg_numeric`): "cooties", "homework-itis", "zoom fatigue",
  "powerpoint poisoning".
- Letter-matched fly phenotypes (`phenotypes_for_flies.py`): "nerdy: has large, prominent eyes
  that stand out, much like thick-rimmed glasses."; "quacky: emits sounds that oddly mimic the
  quack of a duck."

### Other signature moves

- Red herrings on purpose: molecular weight given in v/v problems; a molecular weight column in
  the isoelectric table.
- Orientation and frame traps: random 5'/3' display; translation grouped in fours.
- Self-checking answers: deletion order spells an English word; peptides spell Wordle words.
- No generic "None/All of the above"; the one exception is content-specific: "None of the above
  are possible; the father &male; is not related to his son &male;".
- Difficulty by data: `who_father` easy/medium/hard = 3/5/9 males; deletion mutants 4/5/6 genes.

### Weaknesses found

- Typos: "dihybid", "did another a chi-squared", "will not be appear".
- Unit mismatch: `serial_dilution_factor_mc` stem says uL, choices say mL.

## YAML banks

Rendered stems: statement banks use "Which one of the following statements is {TRUE|FALSE}
{concerning|about|regarding|of} {topic}?" (`yaml_mc_statements_to_bbq.py`); matching uses
"Match each of the following {keys description} with their corresponding {values description}."

### Pre-2025 statement banks

- Lowercase fragments, no period, about 7-11 words, finishing the stem: "the backbone contains
  only phosphate and sugar" (`dna_structure.yml`); "the primers are about 18 to 30 nucleotides
  in length" (`pcr_primers.yml`).
- One-term swap with every permutation: "ionic bonds hold the two strands together" /
  "phosphodiester bonds hold ..." / "disulfide bonds hold ..." (`dna_structure.yml`);
  leading/lagging false versions 1a-1i.
- True-but-out-of-scope facts as false choices (`franklin_diffraction.yml`): "DNA is the genetic
  material responsible for inheritance" (not obtained from Photograph 51).
- Numbers bracketing the true range (`pcr_primers.yml`): "shorter than 10 nucleotides" / "at
  least 50 nucleotides in length, if not longer".
- About two false per true (leading_v_lagging 14/35; rna_v_dna 18/35).
- Absolute words in true statements too: TRUE "group I introns are always self-splicing";
  FALSE "group II introns are never self-splicing" (`intron_splicing.yml`).
- Jokes: "the G&middot;U wobble base pair is named for famous scientist Chandler Wobble."
  (`g-u_wobble.yml`); "xDNA stands for extreme DNA because it does not denature even in boiling
  water (100&deg;C)" (`xna_and_xdna.yml`); "dihydrogen oxide" (`membrane_diffusion.yml`);
  "stereo speakers playing a John Coltrane saxophone solo" (`potential_v_kinetic_energy.yml`).
- Color on the contrasted term via `replacement_rules`: mitosis OrangeRed, meiosis MediumBlue;
  REJECTED in red.

### Pre-2025 matching sets

- Applied pairings: crosses to progeny ("Aa x aa: Half of the offspring display the recessive
  phenotype"); scenarios to categories ("crossing a horse with a donkey to create a mule");
  people to roles (`theranos_people.yml`: "the "pitbull" lawyer who represented Theranos ...").
- Terse values in one frame: "this enzyme unwinds the parental DNA double helix".
- Mirrored values that force discrimination (`chi-square_terms.yml`): "the bigger this number,
  the smaller the p-value" vs "the smaller this number, the bigger the chi2 test statistic".

### 2026 banks: patterns to correct

- Hedge/absolute asymmetry (`senses_chemosensation_smell_taste.yml`): 17 of 25 true statements
  hedged; 9 of 24 false contain absolutes, 1 true does. TRUE: "Salty taste commonly involves ion
  movement through channels rather than GPCR signaling." FALSE: "A single olfactory sensory
  neuron expresses every odorant receptor type."
- "because" clause only on the true version (`protein_stability.yml`): TRUE "Asparagine and
  glutamine make proteins less stable at high temperature because they lose their amide groups."
  FALSE "Asparagine and glutamine make proteins more stable at high temperature."
- Values echo key words (`senses_signal_transduction_matching_set.yml`): "IP3: Molecule that
  opens IP3 receptors ..."; "Gustducin: Taste G protein ..."
- Giveaway dates (`biotechnology_periods_and_milestones.yml`): "Classical times (1800-1945):"
  with "Penicillin discovered by Alexander Fleming (1928)".
- Slide-heading keys and buzzwords (`model_organism_principles.yml`): "Advantages:" with "High
  tractability, ethical viability, and accelerated discovery cycles."
- Category name as a choice (`inventions_v_discoveries.yml`): "truth1: invention".
- Good model kept: `fermentation.yml` grocery examples ("Double India Pale Ale").

## 2026 generators

### Patterns to correct

- Encyclopedic preamble repeated in every item (`hemoglobin_oxygen_affinity`): "Hemoglobin is
  one of the most heavily modulated proteins in the body."
- Four sentences where Neil's 2020 version used one. Neil (`fatty_acid_naming.py`, 2020):
  "What is the correct &omega; (omega) notation for the {0} carbon fatty acid pictured above?"
  2026 (`fatty_acid_naming_omega`): "The skeletal structure above shows an unsaturated fatty
  acid with 20 carbons. The methyl end is on the left (H3C) and the carboxyl end (COOH) is on
  the right. Each vertex and line end represents one carbon atom. What is the correct &omega;
  (omega) notation describing the positions of the double bonds in this 20-carbon fatty acid?"
- Meta-commentary Neil later removed: "The table shows what happens with each genotype."; "These
  counts match the expected ratio for the cross."
- Symbols defined twice (`delta_g_prime_standard_state`): "&Delta;G&deg;&prime; (delta G
  naught-prime, &Delta;G&deg;&prime;)".
- Caveats, citations, and a solution-path hint in the stem (`horse_coat_pattern_inference`,
  about 250 words): "Hint: Start with the lethal-white count to see whether the stallion can
  pass an O allele. Then use the fewspot count ..."
- Form cues: the key is the longest or only non-parallel choice
  (`delta_g_prime_standard_state`: "pH is fixed at 7 ([H+] = 1 x 10^-7 M instead of 1 M)").
- Fake abbreviations beside the two real model names (`allosteric_enzyme_models`): "cooperative
  (COOP)", "Hill (HC)" against MWC and KNF.
- Answer-revealing parentheticals (`exergonic_endergonic_reactions`): "endergonic
  (energy-absorbing)".
- Cosmetic variation: "4 stem wording variants" with the same key (`delta_g_prime_standard_state`).
- Generic lead-in: "Which statement best describes" appears only in 2026 generators
  (`thermodynamics_law_statements`, `x_linked_reciprocal_cross`); "Which one of the following"
  appears in 148 rendered website sets.
- Grammar slips from templates: "A black female mates with a orange male." (`x_linked_tortoiseshell`);
  "Cooler temperatures of the lungs has this effect" (`hemoglobin_oxygen_affinity`).
- Tiny scenario space: `x_linked_reciprocal_cross` renders near-identical items.

### Good patterns in 2026 generators

- Worked-setup count choices (`lethal_allele_survival`): "1/3 x 96 = 32 offspring".
- Fixed fraction ladder (`x_linked_tortoiseshell`).
- Fatty-acid distractors built from errors (inherited from Neil's 2020 logic): "wrong-end",
  "off-by-one shift", "just-count".

## Neil's 2026 correction log

Neil steered agents through many rounds on `lethal_allele_survival.py`,
`monohybrid_litter_inference.py`, `epistasis_test_cross.py`, and the dihybrid gene-interaction
choices. These fixes are pre-registered categories C1-C9 for the old-vs-new skill experiment.

- C1 What is counted is explicit: "Clarified the denominator in both lethal-allele question
  sets with "Before considering survival, assume the cross produces N offspring" and "How many
  would you expect."" Neil's commit `bd221d8` has exactly "Before considering survival, assume
  the cross produces {total} offspring." and "How many would you expect to {outcome_text}?". An
  intermediate agent draft ("These parents produce 96 offspring in total. Include those that do
  not survive.") appears only in the changelog, not in any commit of the generator.
- C2 No redundancy: "Removed the redundant calculation instruction."; "Removed repeated
  baseline cross/ratio labels, the genotype-class legend, and phenotype-grouping instructions.";
  "Removed redundant "one-gene model" and "use a simple model" framing."; "Removed the symbol
  legend from all three pedigree question formats; students must know or look up the
  conventions."
- C3 Friendly numbers: "All offspring totals in both generators are multiples of 12, so halves,
  thirds, and quarters give whole numbers."
- C4 Misconception pair: "Include both 1/3 and 2/3 in fraction/count choices and weight
  scenarios with those correct probabilities eight times more heavily."
- C5 Natural order: "Sorted lethal-allele fraction and calculation choices by increasing
  percentage"; "keep choices in homozygous dominant, heterozygous, homozygous recessive order".
- C6 Labels in choices: "genotype types alongside the randomized allele pairs in all three
  choices" ("Hh (heterozygous)"); "Put the mechanism first in dihybrid gene-interaction choices,
  followed by plain-text "known as" terminology."
- C7 Context consistency: "Removed "large litter" wording from questions that also use plants
  and people."; "label the reference phenotype as "wildtype" alongside its concrete
  description".
- C8 Data first, meaning without color: "A compact two-column offspring table now comes first";
  "Written labels, counts, and different symbol shapes preserve meaning without color."
- C9 No ambiguous escape: "remove the ambiguous-information distractor".

Related: Neil's commit `bd221d8` replaced real-organism traits with hypothetical traits from his
fly phenotype dictionary and added one ASCII-escaped organism emoji per setup; gene letters are
randomized from `"bdefhnrt"` to avoid look-alikes such as C/c and X/x.

## Defects found (separate follow-up, not part of the skill work)

- Wrong key: `x_linked_tortoiseshell.py` keys every "daughters" question "None, 0%".
  `make_cross()` picks `"daughters"` (line 76); `fraction_matching()` filters on the sex label
  `"female"` (line 63), so the selection is empty.
- Unit mismatch in `serial_dilution_factor_mc.py` (uL total, mL choices).
- Typos in pre-2025 banks ("occuring", "frequecies", "Niagra").
- Generator grammar slips listed above.
- Text rewrites worth doing: `x_linked_reciprocal_cross.py`, `x_linked_tortoiseshell.py`,
  `horse_coat_pattern_inference.py`.

## The skill before this work

- `bptools-writer-expert/SKILL.md` and its references covered structure, argparse, BBQ format,
  anti-cheat flags, and seed reproducibility only.
- `references/testing_and_oracles.md` required a `--seed 12345` byte-identical proof; `bptools.py`
  has no seed flag and the repository prefers true randomness.
- `problems/TEMPLATE.py` used the stem `"This is a hard question?"` and kept both
  `'competitive inhibitor'` and `'non-competitive inhibitor'` in the choice pool, so one
  correct-looking term always remained as a distractor.

## About the research sections

The sections below were compiled 2026-10-02 by a research pass. Bibliographic fields were
checked against Crossref metadata and, where marked "full text read", against the article
itself. Local book paths are relative to `~/nsh/MARKDOWN_BOOKS/` (local conversions, not
committed); each passage lists a search term that finds it.

## Published research: verified papers

### 1. Haladyna, Downing, and Rodriguez (2002)

Haladyna, T. M., Downing, S. M., and Rodriguez, M. C. (2002). A review of multiple-choice
item-writing guidelines for classroom assessment. *Applied Measurement in Education*, 15(3),
309-334. https://doi.org/10.1207/S15324818AME1503_5 (full text read; the printed header says
309-334, Crossref lists 309-333.)

Finding: 31 guidelines checked against 27 measurement textbooks and 27 studies from 1990 on.
Table 1 (p. 312) gives the wording below. Table 2 gives the share of textbooks that support
each one (For / Uncited / Against).

| No. | Table 1 wording (verbatim) | For/Unc/Ag (%) |
| --- | --- | --- |
| 3 | "Use novel material to test higher level learning. Paraphrase textbook language ... to avoid testing for simply recall." | 85/15/0 |
| 7 | "Avoid trick items." | 67/33/0 |
| 13 | "Minimize the amount of reading in each item." | 67/33/0 |
| 16 | "Avoid window dressing (excessive verbiage)." | 52/48/0 |
| 17 | "Word the stem positively, avoid negatives such as NOT or EXCEPT. If negative words are used, use the word cautiously and always ensure that the word appears capitalized and boldface." | 63/19/18 |
| 18 | "Develop as many effective choices as you can, but research suggests three is adequate." | 70/26/4 |
| 21 | "Place choices in logical or numerical order." | 67/33/0 |
| 23 | "Keep choices homogeneous in content and grammatical structure." | 67/33/0 |
| 24 | "Keep the length of choices about equal." | 85/15/0 |
| 25 | "None-of-the-above should be used carefully." | 44/7/48 |
| 26 | "Avoid All-of-the-above." | 70/7/22 |
| 28 | "Avoid giving clues to the right answer, such as" (a) "Specific determiners including always, never, completely, and absolutely." (b) "Clang associations ..." (c) grammatical inconsistencies (d) "Conspicuous correct choice." (e) pairs or triplets of options (f) "Blatantly absurd, ridiculous options." | 96/4/0 |
| 29 | "Make all distractors plausible." | 96/4/0 |
| 30 | "Use typical errors of students to write your distractors." | 70/30/0 |
| 31 | "Use humor if it is compatible with the teacher and the learning environment." (Table 2 label: "Use humor sparingly") | 0/85/15 |

Notes from the body text:
- Option count (p. 318): "three options are sufficient in most instances. The effort of
  developing that fourth option (the third plausible distractor) is probably not worth it."
  The usual number of working distractors per item was one.
- Order (p. 318): every textbook agreed with this guideline. Huntley and Welch (1993) found
  random option order may pose obstacles for lower-ability students on math items.
- NOTA (p. 319): all five studies found that NOTA made items harder. NOTA "should generally be
  avoided by novice item writers."
- AOTA (p. 319): AOTA cues the answer and lowered reliability. "We continue to support this
  guideline to avoid AOTA."
- Humor (p. 320): following McMorris et al. (1997), the authors "concur that humor is probably
  a good thing for classroom assessment but only if the overall good exceeds any bad". In
  high-stakes testing "humor should probably not be used."
- Tension for the guide: guideline 28f counts "blatantly absurd, ridiculous options" as a clue
  to the right answer. In this taxonomy a joke distractor is a non-functioning option. It costs
  one option slot and makes the item easier, so it is allowed under guideline 31 only in
  low-stakes classroom use.

### 2. NBME Item-Writing Guide (current edition)

Billings, M. S., DeRuchie, K., Go, S., Hussie, K., Kulesher, A., Merrell, J., Morales, A.,
Paniagua, M. A., Sherlock, J., Swygert, K. A., and Tyson, J. *NBME Item-Writing Guide:
Constructing Written Test Questions for the Health Sciences*, 6th ed. Philadelphia, PA:
National Board of Medical Examiners. The copy read is dated October 2024. Its copyright line
reads "1996, 1998, 2001, 2002, 2016, 2020, 2024". The 2021 URL
(nbme.org/sites/default/files/2021-02/NBME_Item%20Writing%20Guide_R_6.pdf) now redirects to
https://info.nbme.org/rs/552-QHC-046/images/NBME_Item-Writing-Guide.pdf (full text read).

Findings relevant to question writing:
- Five rules. Rule 2: "Each item should assess application of knowledge, not recall of an
  isolated fact." Rule 3: the test-taker "should be able to answer the item based on the
  vignette and lead-in alone." Rule 4: "All options should be homogeneous and plausible to
  avoid cueing to the correct option."
- Cover-the-options rule (p. 12): "If a lead-in is properly focused, a test-taker should
  usually be able to read the vignette and lead-in, cover the options, and guess the correct
  answer without seeing the option set."
- Homogeneous options "can be rank ordered along a single dimension" (p. 12).
- Without a stimulus (vignette or experiment), "the resulting item will generally be
  assessing knowledge recall" (Rule 2 section).
- Chapter 3 names two kinds of technical flaws. Irrelevant-difficulty flaws "can confuse all
  test-takers". Testwiseness flaws cue "the more savvy and confident test-takers".
- Irrelevant-difficulty flaws (summary table, p. 25): long, complex options; tricky,
  unnecessarily complicated stems ("Avoid teaching statements"); inconsistent numeric data;
  vague frequency terms ("usually", "often"); "None of the above"; nonparallel options; and
  negatively structured stems ("EXCEPT"). Numeric options "should be listed in numeric order
  and in a single format (ie, as terms or ranges)", with no overlapping options.
- Testwiseness flaws (p. 25): collectively exhaustive subsets; absolute terms ("always",
  "never"); grammatical clues; word repeats ("clang clue"); convergence; and a correct answer
  that stands out. The fix for the last: "Revise options to equal length. Remove language used
  for teaching points and rationales."
- Convergence warning (p. 24), important for computed distractors: "This flaw occurs when item
  writers start with the correct answer and write the distractors as permutations of the
  correct answer." The fix is to "balance use of terms" across the options.

### 3. Rodriguez (2005)

Rodriguez, M. C. (2005). Three options are optimal for multiple-choice items: A meta-analysis
of 80 years of research. *Educational Measurement: Issues and Practice*, 24(2), 3-13.
https://doi.org/10.1111/j.1745-3992.2005.00006.x (full text read)

Finding: 27 studies yielded 56 independent trials. Going from 4 to 3 options lowers item
difficulty by .04, raises discrimination by .03, and raises reliability by .02. Going from
5 or 4 options down to 2 hurts all three measures. Deleting random distractors hurts
reliability much more than deleting non-functioning ones. So three good options beat four or
five padded ones: "Three options are optimal for MC items in most settings."

### 4. Tarrant and Ware (2008)

Tarrant, M., and Ware, J. (2008). Impact of item-writing flaws in multiple-choice questions on
student achievement in high-stakes nursing assessments. *Medical Education*, 42(2), 198-206.
https://doi.org/10.1111/j.1365-2923.2007.02957.x

Finding: 47.3% of items on 10 nursing papers were flawed (range 28-75% per paper). Flaws did
not hurt borderline students. High-achieving students were the ones penalized: scores of 80%
or above fell from 20.9% on the standard-item scale to 14.5% on the full scale. So flaws blunt
the item's ability to reward real mastery.

### 5. Gierl, Bulut, Guo, and Zhang (2017)

Gierl, M. J., Bulut, O., Guo, Q., and Zhang, X. (2017). Developing, analyzing, and using
distractors for multiple-choice tests in education: A comprehensive review. *Review of
Educational Research*, 87(6), 1082-1116. https://doi.org/10.3102/0034654317726529 (ERIC
EJ1159693; abstract read)

Finding: the abstract notes that "the task of creating distractors has received much less
attention" than the rest of MC testing. The review covers distractor development methods,
distractor analysis, the optimal number and order of distractors, and current
recommendations. Use it as the general entry point for distractor quality.

### 6a. Gierl and Haladyna (2012), book

Gierl, M. J., and Haladyna, T. M. (Eds.). (2012). *Automatic Item Generation: Theory and
Practice*. New York: Routledge. ISBN 978-0-415-89750-1 (hb), 978-0-415-89751-8 (pb).
https://doi.org/10.4324/9780203803912

Finding: this edited volume sets out the theory of templated item generation. An item model,
a stem plus options with variable slots, is filled by software to make many parallel items.
The bptools Python generators are this kind of item model.

### 6b. Gierl, Lai, and Turner (2012)

Gierl, M. J., Lai, H., and Turner, S. R. (2012). Using automatic item generation to create
multiple-choice test items. *Medical Education*, 46(8), 757-765.
https://doi.org/10.1111/j.1365-2923.2012.04289.x

Finding: AIG runs in three stages: (1) a cognitive model of the knowledge and reasoning the
problem needs, (2) an item model (template), (3) software that fills the template to make
hundreds of items. The abstract reports 1,248 generated items. It does not establish that
distractors must be mapped to named wrong paths; this
repository uses named student errors as its local implementation of Haladyna et al. (2002),
guideline 30.

### 7. An (2026), arXiv 2602.18891

An, Y. (2026). Orchestrating LLM agents for scientific research: A pilot study of multiple
choice question (MCQ) generation and evaluation. arXiv:2602.18891 [cs.CY], submitted
21 February 2026. https://arxiv.org/abs/2602.18891 (abstract read; single author)

Finding: LLM agents extracted and aligned 1,071 SAT Math MCQs, generated new ones, and scored
them on a 24-criterion rubric. The generated items never matched the expert baseline on all
24 criteria. The gaps "concentrated in skill depth, cognitive engagement, difficulty
calibration, and metadata alignment". Grammar and option clarity were consistently strong. The
human's work moved from writing items to specification, verification, and governance.

### 8a. Law et al. (2025)

Law, A. K. K., So, J., Lui, C. T., Choi, Y. F., Cheung, K. H., Hung, K. K., and Graham, C. A.
(2025). AI versus human-generated multiple-choice questions for medical education: A cohort
study in a high-stakes examination. *BMC Medical Education*, 25, 208.
https://doi.org/10.1186/s12909-025-06796-6 (PMC11806894, read)

Finding: 100 ChatGPT-4o MCQs were compared with 100 human-written MCQs on an emergency-medicine
primary exam (AI versus human): item-writing flaws 37% vs 35%, factual errors 6% vs 4%,
inappropriate difficulty 14% vs 1%, mean difficulty index 0.78 vs 0.69 (AI easier). AI items
skewed toward Remember and Understand; human items reached Apply and Analyse
(p = .003). Discrimination did not differ significantly.

### 8b. Camarata et al. (2025)

Camarata, T., McCoy, L., Rosenberg, R., Temprine Grellinger, K. R., Brettschnieder, K., and
Berman, J. (2025). LLM-generated multiple choice practice quizzes for preclinical medical
students. *Advances in Physiology Education*, 49(3), 758-763.
https://doi.org/10.1152/advan.00106.2024

Finding: experts reviewed ChatGPT-written renal-physiology practice items against NBME/NBOME
guidelines. "Forty-nine percent of questions contained item writing flaws, and 22% contained
factual or conceptual errors". 91% were usable as a starting point for revision. The authors
call LLM items feasible "only when supervised by a subject matter expert with training in exam
item writing."

### 8c. Moore, Nguyen, Chen, and Stamper (2023)

Moore, S., Nguyen, H. A., Chen, T., and Stamper, J. (2023). Assessing the quality of
multiple-choice questions using GPT-4 and rule-based methods. In O. Viberg et al. (Eds.),
*EC-TEL 2023*, LNCS 14200, pp. 229-245. Springer.
https://doi.org/10.1007/978-3-031-42682-7_16 (full text read)

Finding: a 19-flaw rubric was applied to 200 questions. The flaws are ambiguous wording,
implausible distractors, NOTA, longest option correct, gratuitous information, true/false
series, convergence cues, logical cues, AOTA, mid-stem fill-in-blank, absolute terms, word
repeats, unfocused stem, K-type, grammatical cues, lost sequence (options not in
"chronological or numerical order"), vague terms, more than one correct, and negative wording.
A rule-based checker caught 91% of human-flagged flaws and GPT-4 caught 79%. Implausible
distractors were the most common flaw by human rating. This rubric is usable as a lint
checklist for generated items.

### 9a. McMorris, Boothroyd, and Pietrangelo (1997)

McMorris, R. F., Boothroyd, R. A., and Pietrangelo, D. J. (1997). Humor in educational testing:
A review and discussion. *Applied Measurement in Education*, 10(3), 269-297.
https://doi.org/10.1207/s15324818ame1003_5 (metadata verified. The full text was blocked, so
the findings below come from secondary sources.)

Finding (via Haladyna et al. 2002, p. 320, verified): the review defined types and purposes
of test humor and "concluded that humor is probably a good thing for classroom assessment."
Secondary summaries say the evidence that humor improves performance or lowers anxiety was
weak and inconsistent. Treat that wording as secondary (see Unverified).

### 9b. McMorris, Urbach, and Connor (1985)

McMorris, R. F., Urbach, S. L., and Connor, M. C. (1985). Effects of incorporating humor in
test items. *Journal of Educational Measurement*, 22(2), 147-155.
https://doi.org/10.1111/j.1745-3984.1985.tb01054.x

Finding (paraphrase of the Crossref abstract): 126 eighth graders took matched 50-item grammar
forms, one with 20 humorous items. Humor did not lower performance, students wanted it and
rated humorous items easier, and measured anxiety did not differ.

### 9c. Berk (2000)

Berk, R. A. (2000). Does humor in course tests reduce anxiety and improve performance?
*College Teaching*, 48(4), 151-158. https://doi.org/10.1080/87567550009595834 (ERIC EJ619990)

Finding: reviews the humor-in-testing research and reports a survey of Johns Hopkins nursing
students. The students "feel that humor makes a difference in their test performance." The
article gives practical tactics for humorous test items.

### 9d. Berk and Nanda (2006)

Berk, R. A., and Nanda, J. P. (2006). A randomized trial of humor effects on test anxiety and
test performance. *Humor: International Journal of Humor Research*, 19(4), 425-454.
https://doi.org/10.1515/HUMOR.2006.021

Finding: randomized pretest-posttest design with 98 graduate biostatistics students across
three exams. Humorous directions improved constructed-response scores on the first exam
(effect size .43). Most other contrasts were not significant, which the authors attribute to
low baseline anxiety and high scores. In this one randomized study, humor did not harm
performance; humorous directions improved constructed-response performance on the first test,
while other contrasts were nonsignificant.

## Published research: unverified leads

- Downing (2005): *The effects of violating standard item writing principles on tests and
  students: The consequences of using flawed test items on achievement examinations in medical
  education*, *Advances in Health Sciences Education*, 10(2), 133-143,
  https://doi.org/10.1007/s10459-004-4019-5. Crossref confirmed the bibliographic fields, but
  the full text was not read. Do not cite numerical findings or a reclassification claim from
  this source here.
- McMorris et al. (1997) detailed findings: the publisher page returned 403. Search results
  attribute "11 studies" and "insufficient and inconsistent evidence" to this review, but those
  phrases probably come from Berk and Nanda (2006) quoting it. Cite only the Haladyna et al.
  (2002) summary, which is verified.
- Gierl et al. (2017): only the abstract was read. Specific recommendations in the body (for
  example on ordering or on the number of distractors) are not verified.
- Gierl, Lai, and Turner (2012): the accessible abstract supports the three-stage AIG
  description. It does not support the stronger claim that a cognitive model supplies named
  wrong paths for distractors.
- NBME edition year: the PDF says "sixth edition" and is dated October 2024. Whether the sixth
  edition first appeared in 2020 or 2021 is not confirmed from the document. Cite it as
  "6th ed., 2020; rev. Oct 2024" or simply "Oct 2024".
- Perlini, Nenonen, and Lind (1999), "Effects of humor on test anxiety and performance,"
  *Psychological Reports*, DOI 10.2466/pr0.1999.84.3c.1203. The title and DOI appeared in search
  results; the abstract was blocked (403). Not verified; do not cite findings.
- Townsend and Mahoney (1981), "Humor and anxiety: Effects on class test performance,"
  *Psychology in the Schools* 18:228-234. Seen only in a bibliography page; not verified.

## Local book passages

Paths are relative to `~/nsh/MARKDOWN_BOOKS/`. The Bloom and anatomy books are OCR scans:
quotes below fix OCR letter errors (for example "Ihe" to "the", "fuat" to "that"), and the grep
terms were chosen to match the raw OCR text. Smart quotes in the Dirksen book are stored as
HTML entities; quotes below use plain ASCII.

### Bloom revision (Anderson and Krathwohl 2001)

File: `assessment_taxonomy/A_Taxonomy_for_Learning_Teaching_and_Assessing_a_Revision_of_Bloom_s_Taxonomy_of-2001.md`

| Grep term | Line | Quote | Supports |
| --- | --- | --- | --- |
| `imaginary country` | 277 | "An imaginary country is used to ensure that the student has not encountered it in the past and thus cannot answer the questions based on memory alone." | Novel scenarios force reasoning over recall |
| `go beyond remembering` | 974 | "When the goal of instruction is to promote transfer, assessment tasks should tap cognitive processes that go beyond remembering." | Items above Remember |
| `new to the student` | 1050 | "using assessment tasks that are new to the student is a primary method of ensuring that students respond to the assessments at the most complex cognitive process called for in the objective." | Randomized new instances |
| `unimportant information` | 898 | "Differentiating occurs when a student discriminates relevant from irrelevant information, or important from unimportant information, and then attends to the relevant or important information." | Data-first stems with extra data (Analyze) |
| `homogeneous set of response` | 2532 | "If multiple-choice items are desired, the teacher can add a homogeneous set of response options to the questions." | Homogeneous options |

Also: line 816 (Table 5.1, grep `relevantandirrelevant`) gives the Differentiating example
"Distinguish between relevant and irrelevant numbers in a mathematical word problem." Line
2633 (grep `progressed little`) laments that item writing "has progressed little" since 1956.

### Design for How People Learn (Dirksen 2015)

File: `learning_design/Design_for_How_People_Learn-2015.md`

| Grep term | Line | Quote | Supports |
| --- | --- | --- | --- |
| `genuinely interesting challenge` | 797 | "If you start with a genuinely interesting challenge or puzzle that the learner needs to solve, their extrinsic motivation will start to drift toward a more intrinsic motivation, like puzzle-solving" | Questions as puzzles |
| `practice needs to match` | 2073 | "In the end, the practice needs to match the eventual use. If the learner just needs enough familiarity to recognize the right option, then practicing with recognition activities will be sufficient." | Format matches the cognitive task |
| `Recognition knowledge` | 2085 | "Recognition knowledge--the kind that might have gotten you through a multiple-choice test--is suddenly inadequate in the face of a mostly blank sheet of paper." | Limits of recognition-only MC |
| `confounds your expectations` | 1703 | Working memory admits things that are significant, sought, or actionable, or that "Surprises or confounds your expectations" | Rationale for an occasional absurd option |
| `know is a wrong answer` | 845 | "What do you know is a wrong answer? I'll ask a struggling learner for a wrong answer. Give me a number that's too high." (a quoted teacher) | Bracketing numeric answers |

### Gamification of Learning and Instruction (Kapp 2012)

File: `learning_design/Gamification_of_Learning_and_Instruction-2012.md`

| Grep term | Line | Quote | Supports |
| --- | --- | --- | --- |
| `abstract challenge` | 118 | "A game is a system in which players engage in an abstract challenge, defined by rules, interactivity, and feedback, that results in a quantifiable outcome often eliciting an emotional reaction." (Kapp quoting Koster) | Item as rule-bound puzzle |
| `too hard or too simple` | 122 | "For individuals to be motivated, the challenge must not be too hard or too simple." | Difficulty calibration |
| `informational feedback is designed` | 144 | "The informational feedback is designed to indicate the degree of 'rightness' or 'wrongness' of a response, action, or activity." | Distractor-specific feedback |
| `incongruity` | 164 | "Perceptual arousal has to do with gaining attention through the means of specific, relatable examples, the use of incongruity and/or conflict, or the element of surprise." | Humor or absurdity as an attention device |
| `unparsimonious` | 172 | "cognitive curiosity can be aroused by making learners believe their knowledge structures are incomplete, inconsistent, or unparsimonious." | Puzzles that expose misconceptions |

### Gamification Fieldbook (Kapp, Blair, and Mesch 2013)

File: `learning_design/The_Gamification_of_Learning_and_Instruction_Fieldbook-2013.md`

| Grep term | Line | Quote | Supports |
| --- | --- | --- | --- |
| `trying to figure something out` | 1261 | "In these types of games, the players are trying to figure something out. They may need clues to solve the puzzle or they may have all the pieces in front of them" | Data-first puzzle items |
| `Puzzle Solving, Exploring` | 1537 | Goal-to-game table: "construct meaning ... through interpreting, exemplifying, classifying, summarizing, inferring, comparing, and explaining" maps to "Game (Puzzle Solving, Exploring)" | Puzzles serve Bloom Understand |
| `process of elimination` | 4616 | "Rather than encouraging critical thinking, multiple choice can encourage process of elimination and educated guessing." | Why distractors must survive elimination |
| `real consequences of wrong answers` | 4381 | "Learners have little insight into the real consequences of wrong answers or incorrect decisions other than being told they are not correct." | Explain each wrong path |

### Lehninger testbank (2005), contrast items

File: `testbanks/Lehninger_Principles_of_Biochemistry_Testbank-2005.md`

| Grep term | Line | Excerpt | Observation |
| --- | --- | --- | --- |
| `alphabetical order to avoid guessing` | 30 | Preface: "answers to the multiple choice questions are now listed in alphabetical order to avoid guessing by location" and the authors say "All (or none) of the above" items were eliminated | States the guidelines |
| `all of the above are true` | 651-661 | "Hydrophobic interactions make important energetic contributions to:" four true options, then keyed "E" "all of the above are true." | Keeps AOTA despite the preface; recall item |
| `second ionizable group` | 857-869 | Titration data, "The p*K*_a of the second ionizable group is:" with options "The pH cannot be determined...", 5.4, 5.6 (key), 6.0, 6.2 | Data-first and computed. My check: 6.0 is the answer if the amino group's buffering is ignored, and 6.2 copies the stem pH. The "pH" option does not match the stem's "pKa". |
| `Three buffers are made` | 875-895 | Volume table for three acetate buffers, then options ending "cannot be solved without knowing the value of p*K*_a" and "None of the above." | Good shared data, padded with filler options |

### AAMC MCAT Practice Test 3R (2014), shared-stimulus set

File: `mcat/AAMC_MCAT_Practice_Test_3R-2014.md` (Biological Sciences, Passage IV, items 156-161)

| Grep term | Line | Excerpt | Observation |
| --- | --- | --- | --- |
| `Familial hypercholesterolemia` | 1023 | Passage gives levels: healthy "about 1.8 mg/mL", moderate "about 3.0 mg/mL", severe "around 7.0 mg/mL"; no diet difference between families | Short data stimulus reused across items |
| `does this observation provide evidence` | 1037-1042 | Two 3.0 mg/mL parents have a 7.0 mg/mL child. Options pair a verdict with a reason: "No; HC is codominant, because the heterozygous parents have a less severe form..." | Verdict-plus-reason choices (worked setup) |
| `strongest_ support` | 1051-1056 | "provides the _strongest_ support for the hypothesis that HC is a genetic disease": all options are passage facts | Evaluate-level item built from the stimulus |
| `787 plants were tall` | 1060 | A cross gives 787 tall plants; short count options "0", "277", "787", "2361" | My analysis: each distractor is a named error (all dominant; 1:1 ratio; inverted 3:1). 277 is the only value consistent with 3:1 (answer key not checked). |

Note: items 156 and 160 in the same set test recall unrelated to the passage data. This is a
useful counterexample of weak stimulus dependence.

## Other relevant local books

- `game_design/The_Art_of_Game_Design_3rd_Edition-2019.md`: ten "Puzzle Principles" (line
  6111 onward), for example "Give a Sense of Solvability" (6179). Line 6087: "A puzzle is a game
  with a dominant strategy." Line 6083: puzzles lose replay value unless there is a "rich
  challenge-generation mechanism", which is the argument for randomized generators.
- `game_design/A_Theory_of_Fun_for_Game_Design-2013.md`: line 472, "It is the act of solving
  puzzles that makes games fun." Line 504, "Fun is just another word for learning."
- `game_design/Game_Design_Workshop_3rd_Edition-2014.md`: about 117 puzzle mentions, including
  puzzle-design material (not inspected in detail).
- `hci/Designing_with_the_Mind_in_Mind_User_Interface_Design_Guidelines-2021.md`: Chapter 9,
  "Recognition is Easy; Recall is Hard" (line 1843). Cognitive basis for MC versus fill-in.
- `assessment_taxonomy/How_to_Use_Bloom_s_Taxonomy_in_the_Classroom_The_Complete_Guide-2015.md`:
  question stems for each Bloom level (around line 582 onward).
- `assessment_taxonomy/A_New_Approach_to_Teaching_and_Learning_Anatomy_Objectives_and_Learning_Activities-1976.md`:
  line 87 (grep `complex learning outcomes`) says that to measure comprehension and
  application, "test items should consequently encompass more than those outcomes directly
  designated by specific behavioural objectives." It includes sample anatomy MCQs (Appendix B).
- `assessment_taxonomy/Designing_and_Teaching_Learning_Goals_and_Objectives-2009.md` (Marzano):
  learning goals and scales; marginal for item writing.
- `assessment_taxonomy/Better_Practices_in_the_Classroom-2024.md`: inclusive-teaching guide
  from a gender-studies framework; marginal.
- `mcat/AAMC_MCAT_Practice_Test_4R-2014.md` through `AAMC_MCAT_Practice_Test_9-2014.md`: more
  passage-based sets. `mcat/ExamKrackers_1001_Questions_in_MCAT_Biology-2003.md` gives
  commercial discrete items for contrast.
- `inheritance_genetics/Improving_Genetics_Education_in_Graduate_and_Health_Professional_Education-2015.md`:
  workshop summary on genetics education. No item-writing content was found.
- `psychology/`: none relevant (ADHD, pornography, behavioral genetics of psychopathology).
- `testbanks/` holds only the Lehninger testbank.
