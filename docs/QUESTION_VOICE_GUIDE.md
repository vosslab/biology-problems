# Question voice guide

Canonical source for the wording and formatting of student-facing question text in this
repository. Design and review rules live in [QUESTION_PEDAGOGY_GUIDE.md](QUESTION_PEDAGOGY_GUIDE.md);
worked examples live in [QUESTION_EXEMPLARS.md](QUESTION_EXEMPLARS.md); evidence lives in
[QUESTION_EVIDENCE.md](QUESTION_EVIDENCE.md). Each rule lives in one of these files; the others
cite it as "guide > heading".

Snapshot note: byte-identical copies live in the vosslab-skills repository under
`skills/experts/bptools-writer-expert/references/docs/` and
`skills/experts/webwork-writer-expert/references/docs/`. Refresh both copies in the same change
that edits this file. Backticked repo paths refer to the biology-problems repository. Sections
tagged "(bptools)" apply to Python generators and YAML banks; the rest apply to PGML too.

## Voice in one paragraph

Plain, terse, and exact. The data does the talking; the prose names the task. Address the
student as "you" in lab scenarios, and use "we" for shared scope ("We are ignoring sex-linked
disorders."). Humor lives mostly in names, data, and choices, delivered deadpan; a short aside
in a stem is fine when it costs no clarity ("Your lab partner is trying again (eye roll)").

## Stem anatomy

### Rule, case, question

Order the stem as: figure or table (when present), one rule sentence if the student needs it,
one case sentence, one short question.

- Rule: "For the ABO blood group in humans, the i<sup>A</sup> and i<sup>B</sup> alleles are
  codominant and the i allele is recessive."
- Case: "A father &male; with blood type AB has a son &male; with blood type A."
- Question: "Which of the following blood types could the mother &female; possibly have?"

State what is counted when a count is asked: "Before considering survival, assume the cross
produces 96 offspring. How many would you expect to survive with the wildtype phenotype?"

### Lead-ins

End the stem with one direct question and a question mark; a selection cue may follow it.

- Single answer: "Which one of the following ...?" (with "one").
- Direct quantities: "What fraction of their sons ...?", "How many unique gametes ...?",
  "How much liquid do you add to make a total of 270 &micro;L?"
- Data questions: "Based on the lanes in the RFLP gel above, who is the father of the child?"
- Error analysis: "However, it appears they made an error. What did they do wrong?"
- Selection cue after a multiple-answer question: "Multiple answers may be correct." or
  "Choose two answers."

Write the lead-in as a complete question; a sentence fragment that the choices finish ("Buffer
solutions") fails the cover-the-options check.

### Figure pointers

Tell the student where the data is: "Using the table (above), ...", "Look at the metabolic
pathway in the table above.", "Based on the DNA gel profile below-left, ...".

### Keep the stem lean

Every sentence supplies data, scope, or the question.

- Open with the data or the case.
- State each fact once; let the table carry what the table shows.
- State the data and the question, and let the student choose the method (Neil removed "use a
  simple model" and "one-gene model" framing).
- Put sources, caveats, and teaching explanations in code comments or docs.
- Define only names and symbols invented for the item (allele letters, invented traits). Leave
  standard terms and symbols undefined (&Delta;G&deg;&prime;, &chi;<sup>2</sup>, cM, pK<sub>a</sub>).

## Emphasis

Emphasize only the word that changes the answer or tells two sibling questions apart:

- Phrase the lead-in positively unless the learning target requires a negation. When a negative
  is necessary, capitalize and bold only its discriminator: <strong>NOT</strong> or
  <strong>EXCEPT</strong>; do not emphasize the whole stem.
- Capitals for truth targets and other discriminators: LEAST, TRUE, FALSE, DIFFERENT.
- Underline (or bold) for sibling discriminators: woman/man, sons/daughters, linear DNA
  section/circular DNA plasmid.
- A fixed color only for a contrasted pair that recurs (female and male; mitosis and meiosis),
  always with a text label so the meaning survives without color.

Write the question sentence in plain text; Neil's printed exams set every question in bold as a
page style, and generators leave that to the exam formatter.

## Hints and notes

Use a hint to resolve one ambiguity, then stop before the solution:

- "Hint: the first gene on the end is gene C." (fixes the reading direction of the answer)
- "Hint: pay close attention to the 5&prime; and 3&prime; directions of the strand." (points at
  the trap)
- "Hint: The correct answer is an English dictionary word of length six (6)." (a checkable
  constraint)

Use a note to give a fact needed to read the figure, or an arithmetic result that is not being
graded:

- "Note: The dashes at both ends of the strand indicate the next restriction site is far away."
- "Note: 110/10 = 11 and 110/2 = 55" (show both divisions, in random order)

## Choices

### Layout and order

- Short, parallel, and of one type (all genotypes, all fractions, all worked calculations).
- Natural order when one exists: numbers ascending; genotypes as homozygous dominant,
  heterozygous, homozygous recessive; ratios ascending; short strings alphabetical. Shuffle only
  choices with no natural order.
- For ratio choices, write every option with the same components in the same order, then sort by
  the defined ratio value. Check the rendered order as a student sees it; do not rely on source
  order after a formatter or shuffle step.
- Put the mechanism first and the term second when both appear: "one gene masks the effect of
  another gene, known as epistasis".
- Write content-specific options in place of "None of the above" or "All of the above"; when
  nothing fits, say why: "None of the above are possible; the father &male; is not related to
  his son &male;".

### Fixed ladders

Reuse fixed choice ladders so students learn the format once:

- Quarters: "None, 0%" / "1/4, 25%" / "1/2, 50%" / "3/4, 75%" / "All, 100%".
- Thirds: "1/3, 33.3%" / "2/3, 66.7%"; eighths: "1/8, 12.5%".
- Worked counts: "1/3 &times; 96 = 32 offspring".
- Powers: "2<sup>3</sup> = 8".

### Parallel form

Write every choice, including the key and any absurd choice, in the same grammar, length range,
and register. Give every choice the same qualifiers, parentheticals, and "because" clauses, or
none. Apply one gloss rule to the whole set:

- When the item tests the term itself, write the bare term in every choice ("endergonic",
  "exergonic").
- When the item tests a genotype or mechanism, give every choice the same label ("Hh
  (heterozygous)", "hh (homozygous recessive)").

Keep the key from being the longest choice by a clear margin (the checker flags 1.3 times the
next longest). For statement banks this means the same length on the true and false sides.

## Instructions by item type

### Multiple answer

State the selection rule in one sentence after the question (see Lead-ins). When grading needs
an exact count, say it: "Select exactly three (3) boxes."

### Matching

Say whether letters repeat and whether every letter is used, in one sentence that is true for
the item. Examples: "Letters will be used exactly once."; "Letters will be used more than once;
all letters will be used."; "Not all letters will be used."; "Only one letter will not be used."

Use the stem "Match each of the following ... with their corresponding ...". Mnemonic labels
are welcome: "Nucleic [A]cid", "Lipi[D]s".

### Fill in the blank and numeric

State the exact entry format with a worked example:

- "Your answer should be written as a numerical value only, with no spaces, commas, or units.
  For example, if the distance is fifty one centimorgans, simply write "51"."
- "Do not enter a percentage on the blank. For example, if the answer is 12.3%, enter 0.123 on
  the blank."

State units and rounding when they matter ("Report each answer as a whole number."), and set
the tolerance to match the arithmetic.

### Ordering

State one ordering criterion and its direction: "Arrange the following model organisms from
least to most complex." For model organisms, complexity is the criterion Neil teaches (flies
have legs, eyes, and a brain; worms do not). Give every item the same format (for example
binomial name plus common name throughout).

## Statement bank form

(bptools YAML banks.)

- Write each statement as a lowercase clause with no final period that reads as a complete
  statement: "the backbone contains only phosphate and sugar".
- Keep statements short (about 7 to 12 words).
- Write the `topic` string to read naturally after "Which one of the following statements is
  TRUE regarding ...": "PCR primers that are efficient and avoid mispriming".
- Use `replacement_rules` color on the contrasted term (mitosis vs meiosis, increases vs
  decreases, REJECTED vs NOT REJECTED).
- Write custom stems with `override_question_*` for classification banks: "Which one of the
  following English words is <strong>NOT</strong> a palindrome?"

## Numbers, units, and symbols

- Write counts from two through nine as word plus digit ("two (2)", "six (6) genes"); write 10
  and above, and any number with a unit, as digits ("24 offspring", "4 kb").
- Use thousands separators ("58,000") and a space between number and unit ("4 kb", "10.45 cM",
  "270 &micro;L").
- Use the same unit in the stem and the choices.
- Write sequences 5&prime; to 3&prime; with labeled ends ("5&prime;-ATTCAGT-3&prime;") in
  monospace; group codons in threes, or fours when hiding the frame is the point.
- Show genotypes and alleles in monospace; mark people and animals with &female; or &male;
  after the noun.
- Use HTML entities for symbols (&alpha;, &Delta;G, &chi;<sup>2</sup>, &deg;C) and
  `<sub>`/`<sup>` for subscripts and superscripts.

## HTML and formatting

(Blackboard BBQ output; PGML follows the webwork skill's whitelist.)

- Use a small set of elements: `p`, `br`, `strong`, `u`, `sub`, `sup`, `table`, and `span` for
  color or monospace. Blackboard may rewrite complex markup; tables are fine because they are
  converted to images before import (`docs/HUMAN_GUIDANCE.md`).
- Keep tables minimal: a header row and thin borders. Add row fills or captions only when the
  color is data.
- Use color only when it carries meaning (a parental chromosome, a contrasted term, a gel band),
  and pair it with a text label.

## Mechanics

Agents own polish. Before finishing, read every rendered stem and choice for:

- spelling ("complementary", "occurring", "frequencies");
- articles ("an orange male", "a heterozygous female", "an X-linked trait");
- spacing: single spaces, a space after every period, "?" attached to the last word;
- subject-verb agreement in templated text ("Cooler temperatures of the lungs have ...");
- capitalization of fixed terms ("X-linked", "Y-linked", "F<sub>1</sub>").
