# Question pedagogy guide

Canonical source for how student-facing questions are designed and reviewed in this
repository. Wording and formatting rules live in [QUESTION_VOICE_GUIDE.md](QUESTION_VOICE_GUIDE.md);
worked examples live in [QUESTION_EXEMPLARS.md](QUESTION_EXEMPLARS.md). Each rule lives in one
of these files; the others cite it as "guide > heading".

Snapshot note: byte-identical copies live in the vosslab-skills repository under
`skills/experts/bptools-writer-expert/references/docs/` and
`skills/experts/webwork-writer-expert/references/docs/`. Refresh both copies in the same change
that edits this file. Backticked repo paths refer to the biology-problems repository. The
evidence behind these rules (corpus audit, verified research, book passages) is in
[QUESTION_EVIDENCE.md](QUESTION_EVIDENCE.md).

## Decision hierarchy

Apply these sources in order when they disagree:

1. Neil's stated guidance (`docs/HUMAN_GUIDANCE.md` and his direct requests) wins.
2. Published item-writing standards (see [References](#references)).
3. Patterns from Neil's strongest questions: his printed exams and the 2018-2022 generators.
4. Corrections drawn from flaws found in any corpus.

Judge each text on its wording and construction, whoever wrote it. Many recent generators
carry Neil's ideas; for example, ordering model organisms by complexity (flies have legs, eyes,
and a brain; worms do not) is his design.

One conflict is settled by rule 1. Neil loves seriously absurd choices. Haladyna, Downing, and
Rodriguez (2002) allow humor in classroom tests (guideline 31) but list "blatantly absurd,
ridiculous options" as a clue to the answer (guideline 28f). The resolution is in
[Seriously absurd choices](#seriously-absurd-choices).

## Puzzle first, few words

Neil: "I am not a writer. I hate writing. I am a thinking and problem/puzzle solver with
strong math mind." Design questions accordingly:

- Treat each question as a puzzle. Build the data, the constraint, the answer, and the wrong
  answers before writing any sentence.
- Wrap the puzzle in the fewest words that make it unambiguous (voice > Keep the stem lean).
  Most of Neil's exam stems run 25 to 55 words outside the data; reread any stem over 80 words.
- Let the data carry the difficulty: a gel, table, map, cross, or sequence does the work that a
  paragraph of explanation would otherwise attempt.
- Polish mechanics and keep the word count low (voice > Mechanics).

Why: "Minimize the amount of reading in each item" and "Avoid window dressing (excessive
verbiage)" (Haladyna et al. 2002, guidelines 13 and 16). A puzzle the learner wants to solve
shifts motivation toward the intrinsic kind (Dirksen 2015).

## Design workflow

Complete these steps in the authoring contract before writing generator code.

### Name the reasoning target

State what the student must do with the data, on the revised Bloom cognitive-process scale:
apply (use a rule on a new case), analyze (pull structure out of data, including telling
relevant from irrelevant numbers), or evaluate (judge a claim or a calculation). Label
vocabulary sets as recall.

Examples: "analyze a gel to identify the father"; "apply survival among surviving offspring to
a cross with a lethal genotype"; "evaluate which worked distance calculation pairs the right
progeny classes".

Why: "Each item should assess application of knowledge, not recall of an isolated fact" (NBME
Rule 2). AI-written items skew toward Remember and Understand (Law et al. 2025) and fall short
on cognitive depth (An 2026).

### Build the data

Choose the table, figure, cross, sequence, or scenario that forces the target reasoning.
Randomize the parts that change the answer (allele letters, counts, positions, enzymes) so
items differ in substance. Pick numbers that make the intended arithmetic come out whole
(offspring totals that are multiples of 12; volumes that divide evenly).

Why: tasks that are new to the student make them use the intended cognitive process instead of
memory (Anderson and Krathwohl 2001).

### List the student errors

Write down the specific mistakes a student makes on this task: swapped roles, reversed
direction, wrong denominator, missed exception, decimal moved the wrong way, adjacent concept.
Each error becomes one wrong choice. Sources: teaching experience, past answer data, textbook
misconceptions, and the recipes in [QUESTION_EXEMPLARS.md](QUESTION_EXEMPLARS.md).

Why: "Use typical errors of students to write your distractors" (Haladyna et al. 2002,
guideline 30).

### Compute the wrong answers

Generate each distractor in code from its named error, with a comment naming the error. Remove
duplicates and any distractor equal to the key. When a misconception has complementary outcomes
or paired cases, keep the contrast that makes that misconception visible when subsampling the
choice pool. See [Error-derived distractors](#error-derived-distractors).

### Write the thinnest wrapper

Write the stem as [QUESTION_VOICE_GUIDE.md](QUESTION_VOICE_GUIDE.md) directs (voice > Stem
anatomy).

### Review

Render several items, run the advisory checker `devel/check_question_text.py` on the BBQ output,
verify the key ([Answer verification](#answer-verification)), and apply the
[Review rubric](#review-rubric).

## Distractor design

### Error-derived distractors

Every ordinary wrong choice is the answer a student gets by making one named mistake:

- Dilution: swapped aliquot and diluent; total volume used as the aliquot; doubled aliquot.
- Transcription: template copied; template reversed; complement not reversed; half-and-half
  chimera.
- PCR primers: one primer flipped; both flipped.
- Gene mapping: worked distance calculations that leave out the double crossovers.
- Lethal genotypes: 1/4 and 3/4 (lethality ignored) beside 1/3 and 2/3.

Why: an error-derived distractor attracts exactly the students who hold that misconception, so
each choice carries information. This is the repository's concrete application of Haladyna et
al. (2002), guideline 30: "Use typical errors of students to write your distractors."

### Balance the variations

When distractors are variations of the key, vary them in several directions so the key is not
the choice that shares the most parts with the others. Spread each component (a term, a number,
an enzyme) across several choices.

Why: when distractors are "permutations of the correct answer", testwise students converge on
the key; the fix is to "balance use of terms" across the options (NBME convergence flaw).

### Show-the-setup choices

When the concept is choosing the right setup, put the worked calculation in every choice:
"(493+476+29+22)/6000 = 17.0 m.u." beside "(493+476)/6000 = 16.2 m.u.". The student judges the
reasoning; the arithmetic is already done. When arithmetic is not the point at all, hand it
over in a note (voice > Hints and notes).

### Seriously absurd choices

Neil loves seriously absurd choices; they are welcome course voice:

- "the G&middot;U wobble base pair is named for famous scientist Chandler Wobble"
- "The two genes are NEITHER linked NOR unlinked."
- "molecular stopper", "proteomic pothole"
- "xDNA stands for extreme DNA because it does not denature even in boiling water"

Craft:
- Deliver it deadpan, in the same grammar, length, and register as the real choices; it is
  absurd by content only.
- Make it a pun or a confident wrong claim on the item's own topic.
- Use enough meaningful alternatives, including error-derived distractors where they serve the
  reasoning target, to assess the intended reasoning. There is no universal numerical quota for
  either error-derived or absurd choices. Rodriguez (2005) supports three good options in most
  settings; it does not make a joke distractor free.

Why: humor in classroom tests is "probably a good thing" when the overall good exceeds any bad
(Haladyna et al. 2002); controlled studies find humorous items do not lower performance or raise
anxiety (McMorris, Urbach, and Connor 1985) and can help modestly (Berk and Nanda 2006).
Incongruity and surprise gain attention (Kapp 2012).

### Misconception placement

Build the misconception into the data, not only into the choices. Example from
`docs/HUMAN_GUIDANCE.md`: in restriction-digest maps, place the non-selected enzyme's site on the
0 kb mark, because students assume DNA is always cut at 0. Weight scenarios toward the answers
students most often miss; the lethal-genotype generator weights the 1/3 and 2/3 keys 8 to 1.

### Cannot be determined

Offer "cannot be determined" only when it is the correct answer for some scenarios in the pool
and is unambiguous in every scenario where it appears. Example: when every offspring is
wildtype, the father's genotype cannot be determined. Replace escape choices that are never or
ambiguously correct with error-derived distractors.

## Item structure

### Data first and shared-figure sets

Present the figure or table first, then ask. One figure can carry several questions
("Questions 11-12 ..."), each reusing mostly the same choice set; the student invests once in
reading the data and is tested several ways. Point at the data in the question (voice > Figure
pointers).

Why: without a stimulus, an item "will generally be assessing knowledge recall" (NBME Rule 2).

### Multi-part stories

A single family or experiment can carry a run of questions: genotype of the woman, of the man,
fraction of sons, fraction of daughters, transfusion compatibility. Name characters plainly
("A man named David ...").

### Self-checking answers and puzzles

Design answers the student can verify: deletion orders that spell English words, peptide
sequences that spell Wordle words, a map order that fits every listed deletion. A checkable
answer rewards reasoning and catches careless errors.

### Red herrings

When recognizing irrelevant information is part of the skill, put red herrings in the data:
molecular weight in a volume/volume problem, a molecular weight column in an isoelectric-point
table.

Why: differentiating "relevant from irrelevant information" is an Analyze process (Anderson and
Krathwohl 2001).

### Difficulty from data

Scale difficulty by the size and structure of the data: 3, 5, or 9 candidate fathers; 4, 5, or
6 genes; more restriction sites. Keep the stem wording the same across levels.

### Scenario variety

Sampled items should differ in data or scenario. Reworded stems, reordered choices, and labels
with the same key and data count as one question. Review rendered samples for meaningful changes
to the data and target. Biology can constrain a question family to one scenario type, so vary the
facts that support the target rather than forcing an artificial cross or scenario change. Select
scenarios with true randomness, then review the requested rendered sample for cosmetic-only
duplication. When a requested batch exceeds the meaningful family capacity, reuse scenarios
deliberately rather than inventing artificial variants; sample without replacement when the batch
is meant to be unique.

### Names and invented worlds

Use real organisms, genes, and diseases, or invented names that help memory and remove prior
knowledge:

- Letter-matched phenotypes: "bumpy, waxy, yucky" for genes b, w, y; Neil's fly dictionary
  ("nerdy", "quacky") keyed by first letter.
- Fantasy taxa for tree topology: "Rynoth, Ashen, Inktoad, Phoenix, Gorret, Unicorn".
- Fictional worlds: "On planet Zygora, the glowstem plant species ...".
- Fictional diseases for population genetics: "cooties", "homework-itis", "zoom fatigue".

Rules for names:
- Choose allele letters whose upper and lower case differ in shape (b, d, e, f, h, n, r, t), and
  match each invented name's first letter to its allele letter.
- Call an invented trait hypothetical, and use the same names in the table, the rule, and the
  question.
- Label the reference phenotype "wildtype" beside its description ("straight wings
  (wildtype)").
- Keep context words true to the organism: "litter" for mammals, "seeds" or "offspring" for
  plants, "children" for people.
- Use an emoji only as an intentional label for a recurring entity, ASCII-escaped in source.

Why: "An imaginary country is used to ensure that the student has not encountered it in the
past and thus cannot answer the questions based on memory alone" (Anderson and Krathwohl 2001).

## Statement banks

Statement banks feed "Which one of the following statements is TRUE (or FALSE) regarding
<topic>?" questions. Form rules are in voice > Statement bank form.

### One-term swaps

Write the true statement first. Build each false statement by changing exactly one key term,
and list every plausible swap as lettered variants: "ionic bonds hold the two strands
together", "phosphodiester bonds hold ...", "disulfide bonds hold ...". Add a seriously absurd
variant when it amuses.

### Out-of-scope facts and bracketed numbers

In a TRUE bank, use true facts that lie outside the topic as false choices when the topic has a
clear edge: "DNA is the genetic material responsible for inheritance" is true but was not
obtained from Photograph 51. (Under a NOT stem the same fact becomes the key.) For numeric
claims, place wrong values on both sides of the true range ("shorter than 10 nucleotides", "at
least 50 nucleotides").

### Balanced hedges and absolutes

Use hedging words (commonly, often, can) and absolute words (always, never, only) at similar
rates in true and false statements, and put some absolutes in true statements ("group I introns
are always self-splicing"). The checker reports the rates per side (K2) and flags a gap of 25
percentage points or more.

Why: absolute terms and vague frequency terms are listed testwiseness and irrelevant-difficulty
flaws (NBME); when hedges mark true statements and absolutes mark false ones, a test-wise student
answers without knowing the biology.

### Pool sizes

Write more false statements than true ones (about two to one): a TRUE question uses one true and
four false statements. When the bank also asks FALSE questions, include at least four true
statements. Go deep on one contrast per bank, and check new banks against existing ones for
duplicated concepts.

## Matching sets

### Applied pairings

Match things students must reason about: crosses to progeny outcomes, scenarios to categories,
stages to events, people to roles. Use biological entities and categories as keys, and make the
key description accurate.

### Values without cues

Keep each value a short fragment in one shared frame ("this enzyme unwinds the parental DNA
double helix"). Paraphrase each value without the key's own words, category words, or giveaway
dates. Deliberate mirror pairs are the exception: "the bigger this number, the smaller the
p-value" vs "the smaller this number, the bigger the chi2 test statistic". Merge stages that are
truly hard to tell apart into one key ("Diplotene or Diakinesis, combined"). Add variants only
where real alternative phrasings exist.

## Answer verification

Verify the key with a method independent of the generator:

- Computed items (crosses, distances, dilutions, digests): enumerate every scenario in a
  temporary check, or recompute with a second implementation, and compare to the key.
- Recall, matching, and statement items: a separate agent checks each key against the source
  data or bank, item by item.

Why: a real key bug survived rereading the generator's own logic (`x_linked_tortoiseshell.py`
compared "daughters" to "female"). Reviewers found factual or conceptual errors in 22% of
LLM-written practice items (Camarata et al. 2025).

## Review rubric

The rubric indexes rules; the wording of each rule lives at the heading named in parentheses.
Apply the universal checks to every item and the type checks that fit.

Universal:
- U1 Puzzle first and data first (Puzzle first, few words; voice > Rule, case, question).
- U2 Emphasis on discriminators and negations only (voice > Emphasis).
- U3 What is counted is explicit; numbers give whole-number arithmetic (Build the data; voice >
  Rule, case, question).
- U4 Lean stem: each fact once, data first, caveats and citations in code comments (voice >
  Keep the stem lean).
- U5 Sampled items differ in data or scenario (Scenario variety).
- U6 Names are deliberate (Names and invented worlds).
- U7 Mechanics, units, and symbols are clean (voice > Mechanics; voice > Numbers, units, and
  symbols).
- U8 Difficulty comes from data (Difficulty from data; voice > Hints and notes).
- U9 The key is verified independently (Answer verification).

Multiple choice and multiple answer (PGML radio buttons and checkbox lists):
- M1 Cover-the-options: a prepared student can answer from the stem before reading the choices
  (voice > Lead-ins).
- M2 Each distractor is tagged with its error or as absurd. The item has enough meaningful
  alternatives to assess its intended reasoning and retains misconception contrasts when choices
  are subsampled; no universal numerical quota applies
  (Error-derived distractors; Seriously absurd choices).
- M3 Options are homogeneous and in natural order (voice > Layout and order).
- M4 No testwise cue: the key is not the longest or most qualified choice; stem words appear in
  every choice or none; abbreviations or glosses are not carried only by some choices; the
  variations are balanced (voice > Parallel form; Balance the variations).
- M5 "Cannot be determined" appears only when sometimes the key and never ambiguous (Cannot be
  determined).

Statement banks:
- S1 Statement form (voice > Statement bank form).
- S2 One-term swaps (One-term swaps).
- S3 Balanced hedges and absolutes (Balanced hedges and absolutes).
- S4 Pool sizes (Pool sizes).

Matching (PGML pop-up matching):
- T1 Letter-use instruction (voice > Matching).
- T2 Values without cues (Values without cues).
- T3 Values parallel, one idea each (Values without cues).

Fill in the blank and numeric (PGML answer blanks):
- F1 Entry rules with a worked example; F2 units and rounding; F3 tolerance that matches the
  arithmetic (voice > Fill in the blank and numeric).

Ordering (PGML draggable lists):
- O1 One stated ordering criterion; O2 one item format (voice > Ordering).

Checker map: `devel/check_question_text.py` findings are advisory and send an item to a closer
read. K1 longest key -> M4; K2 hedge/absolute asymmetry -> S3 and M4; K3 key-word echo -> M4 and
T2; K4 article slips, K5 spacing, K6 unit mismatch -> U7; K7 generic lead-in -> M1 (voice >
Lead-ins).

## References

Published sources:
- Anderson, L. W., and Krathwohl, D. R. (Eds.) (2001). A Taxonomy for Learning, Teaching, and
  Assessing: A Revision of Bloom's Taxonomy of Educational Objectives. Longman.
- An, Y. (2026). Orchestrating LLM agents for scientific research: A pilot study of multiple
  choice question (MCQ) generation and evaluation. arXiv:2602.18891.
- Berk, R. A., and Nanda, J. P. (2006). A randomized trial of humor effects on test anxiety and
  test performance. Humor, 19(4), 425-454. doi:10.1515/HUMOR.2006.021
- Billings, M. S., DeRuchie, K., Hussie, K., et al. NBME Item-Writing Guide: Constructing Written
  Test Questions for the Health Sciences (6th ed., rev. October 2024). National Board of
  Medical Examiners.
- Camarata, T., McCoy, L., Rosenberg, R., et al. (2025). LLM-generated multiple choice practice
  quizzes for preclinical medical students. Advances in Physiology Education, 49(3), 758-763.
  doi:10.1152/advan.00106.2024
- Dirksen, J. (2015). Design for How People Learn (2nd ed.). New Riders.
- Downing, S. M. (2005). The effects of violating standard item writing principles on tests and
  students. Advances in Health Sciences Education, 10(2), 133-143.
  doi:10.1007/s10459-004-4019-5
- Gierl, M. J., Bulut, O., Guo, Q., and Zhang, X. (2017). Developing, analyzing, and using
  distractors for multiple-choice tests in education: A comprehensive review. Review of
  Educational Research, 87(6), 1082-1116. doi:10.3102/0034654317726529
- Gierl, M. J., and Haladyna, T. M. (Eds.) (2012). Automatic Item Generation: Theory and
  Practice. Routledge. doi:10.4324/9780203803912
- Gierl, M. J., Lai, H., and Turner, S. R. (2012). Using automatic item generation to create
  multiple-choice test items. Medical Education, 46(8), 757-765.
  doi:10.1111/j.1365-2923.2012.04289.x
- Haladyna, T. M., Downing, S. M., and Rodriguez, M. C. (2002). A review of multiple-choice
  item-writing guidelines for classroom assessment. Applied Measurement in Education, 15(3),
  309-334. doi:10.1207/S15324818AME1503_5
- Kapp, K. M. (2012). The Gamification of Learning and Instruction. Pfeiffer.
- Law, A. K. K., So, J., Lui, C. T., et al. (2025). AI versus human-generated multiple-choice
  questions for medical education: A cohort study in a high-stakes examination. BMC Medical
  Education, 25, 208. doi:10.1186/s12909-025-06796-6
- McMorris, R. F., Urbach, S. L., and Connor, M. C. (1985). Effects of incorporating humor in
  test items. Journal of Educational Measurement, 22(2), 147-155.
  doi:10.1111/j.1745-3984.1985.tb01054.x
- Moore, S., Nguyen, H. A., Chen, T., and Stamper, J. (2023). Assessing the quality of
  multiple-choice questions using GPT-4 and rule-based methods. EC-TEL 2023, LNCS 14200,
  229-245. doi:10.1007/978-3-031-42682-7_16 (a rule-based checker caught 91% of flaws, GPT-4
  79%; the model for `devel/check_question_text.py`).
- Rodriguez, M. C. (2005). Three options are optimal for multiple-choice items: A meta-analysis
  of 80 years of research. Educational Measurement: Issues and Practice, 24(2), 3-13.
  doi:10.1111/j.1745-3992.2005.00006.x
- Tarrant, M., and Ware, J. (2008). Impact of item-writing flaws in multiple-choice questions on
  student achievement in high-stakes nursing assessments. Medical Education, 42(2), 198-206.
  doi:10.1111/j.1365-2923.2007.02957.x

Local book conversions in `~/nsh/MARKDOWN_BOOKS/` (path, then a search term that finds the
passage):
- `assessment_taxonomy/A_Taxonomy_for_Learning_Teaching_and_Assessing_a_Revision_of_Bloom_s_Taxonomy_of-2001.md`:
  `imaginary country`, `new to the student`, `unimportant information`,
  `homogeneous set of response`.
- `learning_design/Design_for_How_People_Learn-2015.md`: `genuinely interesting challenge`,
  `practice needs to match`.
- `learning_design/Gamification_of_Learning_and_Instruction-2012.md`: `incongruity`,
  `too hard or too simple`.
- `learning_design/The_Gamification_of_Learning_and_Instruction_Fieldbook-2013.md`:
  `process of elimination`, `trying to figure something out`.
- `game_design/The_Art_of_Game_Design_3rd_Edition-2019.md`: `Sense of Solvability` (puzzle
  principles).
