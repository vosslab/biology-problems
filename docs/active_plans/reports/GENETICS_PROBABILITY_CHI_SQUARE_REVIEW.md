# Genetics probability and chi-square review

## Delivered content

The [approved plan](../active/GENETICS_PROBABILITY_CHI_SQUARE.md) is implemented
with the bptools-writer-expert skill. Canonical generators live in BPQ; published
local banks and their catalog metadata live in the sibling BPW repository.
The chapter 7 task file has four probability modes, six dice modes, two separate
hypothesis modes, and the revised lab-partner mode. These 13 banks contain 362
items: 272 probability/dice items and 90 hypothesis/lab-partner items.

Independence uses 12 items and small-family calculation uses 20, respecting their
finite scenario pools. Other banks have 30. Null/alternative questions reuse four
biological cross models; shuffled choices do not create new biological scenarios.
Scenario selection is random, numeric choices retain numerical order, and bptools
collection applies its normal anti-cheat settings without overrides.

The existing probability bank moved byte-for-byte from topic06 to topic07:
SHA256 `5949346f92781a9b56e4749089d38df3eb241ddb6b5edf67f4d93f6b3da14ec6`.
The Genetics paired-hypothesis placement is removed. The pair-mode default and
Biostatistics placement remain available.

## Teaching and voice review

Sources: lectures 07B/07C/07D, the chi-square worksheet, the supplied Bozeman
subtitles, and the live question pedagogy/voice/exemplar guides. The new probability
work deliberately uses smaller families than the lectures' later binomial and
multinomial examples. Unequal-probability calculations hand over one-order
arithmetic. Survivor tables explicitly count surviving offspring. Hypothesis
selection contains no observed-count table or test conclusion.

Exemplars used: "Lab scenario in second person", "Rule, case, question", and
"Note that hands over arithmetic". The independent reader checked the first five
items of every new probability/dice bank and every item in the three hypothesis
banks. Initial feedback led to multiple-key MA outcomes, three distinct Matching
pairs, parallel hypothesis propositions, and evidence-based interpretation.
The final reader found no remaining material language, ambiguity, or key issues.

Before: "Your lab partner is trying again (eye roll)." followed by "but they wrote"
and "What is the main problem with their hypotheses?" even in correct cases.
After: "Your lab partner writes these hypotheses for a chi-square test" and
"What should your lab partner change, if anything?"

Before: "The offspring proportions are consistent with the expected 3:1 ratio
(any differences from the expected ratio are due to chance)."
After, standalone null: "The cross produces offspring with an expected 3:1 ratio."
Alternative: "The cross produces offspring with an expected ratio different from 3:1."
The lab-partner correct pair uses equivalent short expected-ratio predictions.

Local before/after BBQ samples, standalone previews, screenshots, and checker logs
are in ignored `output_genetics_review/`; final five-item samples are in its `final/`
subdirectory. These are review artifacts, not another source of published content.

## Follow-up wording and variety review

Replace the turn-taking distractor in both standalone hypothesis modes with:
"The cross produces offspring with an expected ratio that depends on sample size."
This targets confusion between expected counts and the predicted ratio. Counting
more offspring changes the expected counts, not the inheritance model's ratio.
The choice has the same sentence structure and expected-ratio vocabulary as the
key. The exact-observations distractor still targets a separate error: requiring
every finite sample to match the prediction exactly.

Lecture 07D explicitly uses "do not reject" and explanations about evidence.
Neither "insufficient evidence" nor "not enough evidence" appears verbatim in
the extracted slides. Use the simpler "there is not enough evidence" for the
dice conclusion and parallel "there is enough evidence" for rejection. These
are evidence statements, not proof that the die is fair or unfair.

Read two newly generated items for each cross in each hypothesis mode (16 total):

| Cross context | What the context contributes | Limit |
| --- | --- | --- |
| Aa x Aa, 3:1 | A familiar two-phenotype prediction | Ratio supplied; no Punnett-square reasoning required |
| Pink x pink, 1:2:1 | Three visible flower-color categories under incomplete dominance | Same hypothesis distinction as the monohybrid item |
| Dihybrid F2, 9:3:3:1 | The four-category prediction used in lecture 07D | No new hypothesis-selection operation |
| AaBb x aabb, 1:1:1:1 | An equal-category testcross prediction | Choice shuffling does not add reasoning |

These are useful short conceptual warm-ups across familiar crosses. There are
four distinct context/stem combinations per mode, eight across null and
alternative, rather than 60 distinct biological problems. Repeated questions
within one context only change choice order. The broader progression comes from
the probability, calculation, interpretation, and lab-partner families; the
standalone hypothesis banks should not be described as that progression themselves.

All eight fixed-context CLI runs and the five-item dice interpretation run
completed successfully. Read their actual stems, choices, and keys, including
dice results on both sides of the cutoff. Samples are in ignored
`output_genetics_review/wording_revision/`. No additional automated test suite,
browser, or LMS checks were run for this wording follow-up. Existing task rows
already select the revised modes. BPW banks were not regenerated in this follow-up;
the source revisions take effect on the next task-file generation.

## Dice visuals

All six dice modes now show 40 x 40 px HTML dice with 6 px pips beside numeric
face labels. Each die uses a three-by-three presentation table with explicit
light surfaces and dark pips; it does not require a Unicode dice font. The
decorative table is hidden from assistive technology, while the numeric row
label remains readable. Reference tables for critical values retain their
ordinary numeric labels.

All six modes generated one sample and standalone HTML successfully. Inspected
the interpretation sample at a 390 px viewport: all six pip patterns are clear,
and counts align with their faces. The preview and screenshot are in ignored
`output_genetics_review/dice_visual/`. No BPW or LMS checks were added.

## Distractor rationales, including the wording revision

| Family and displayed case | Choice | Source |
| --- | --- | --- |
| Two offspring, purple probability 1/2, exactly zero purple | 1/4 | Key: white-white, 1/2 times 1/2 |
| Same probability item | 0 | Error: report target count / family size |
| Same probability item | 1/2 | Error: report one offspring's probability |
| Same probability item | 1 | Error: omit the non-target offspring factors |
| Dice: one contribution 0.20, remaining sum 2.70 | 2.90 | Key: add the contributions |
| Same dice item | 0.48 | Error: average the six contributions |
| Same dice item | 2.50 | Error: subtract the missing contribution |
| Same dice item | 2.70 | Error: omit the missing contribution |
| Null hypothesis, pink-by-pink cross | Expected 1:2:1 ratio | Key: prediction under the proposed inheritance pattern |
| Same hypothesis item | Expected ratio different from 1:2:1 | Error: choose the alternative |
| Same hypothesis item | Observed 1:2:1 ratio in every sample | Error: demand exact observed counts |
| Same hypothesis item | Expected ratio depends on sample size | Error: confuse changes in expected counts with changes in the predicted ratio |
| Lab partner, swapped 1:1:1:1 statements | Switch the labels | Key: null and alternative are reversed |
| Same lab-partner item | Allow observed counts to vary | Error: diagnose an exact-count claim that is absent |
| Same lab-partner item | Use the predicted ratio as reference | Error: diagnose a wrong ratio when the reference is correct |
| Same lab-partner item | Keep both hypotheses | Error: overlook the reversed labels |

## Key verification and advisory checks

- Independently read the final BBQ fields, enumerate ordered offspring outcomes,
  sum event probabilities, and recompute all dice contributions and decisions:
  all 272 probability/dice items pass. Matching values are distinct and every MA
  item has multiple keys. Dice calculations retain at least three distinct choices.
- A separate reader checked all 30 null, 30 alternative, and 30 lab-partner keys
  against their cross and statements; all pass. Matching keys were also checked
  item-by-item in the first-five samples of both Matching families.
- The Bozeman counts 2, 4, 8, 9, 3, 10 give 58/6, five degrees of freedom, and
  do not reject at 0.05. Durable tests separately guard probability mass and both
  sides of the chi-square decision. The one-time emitted-key checker is removed
  at closeout; its results remain in `output_genetics_review/independent-keys.log`.
- Final advisory checker: no findings in calculation, independence, expected-count,
  df, combined-conclusion, or Matching samples. K2 flags absolutes in hypothesis
  and interpretation distractors: retained because exact observations and proof
  are the misconceptions being assessed, not incidental stylistic qualifiers.
  K3 flags phenotype words in outcome choices and hypothesis/observation words in
  lab-partner answers: retained because identifying those features is the task.
  No longest-key, malformed-record, or unnecessary-jargon finding remains.

## Verification limits

Final scope correction from the instructor: "just make sure the generator works
and add to the task file." Every registered mode has run successfully through the
generator CLI. Generated HTML was checked at 390 and 1280 pixels in light and dark
themes: all 52 standalone views and correct-answer submissions passed. Table widths
fit their containers, and inspected mobile screenshots have readable labels and
choices. Temporary verification scripts were removed after recording the evidence.

Before that scope correction, 52 additional BPW views/submissions passed. Two dice
package downloads completed; a later download attempt timed out. No package or LMS
acceptance is claimed, and that out-of-scope investigation was stopped. These browser
results do not add a requirement to the final generator/task-file scope.

The BPQ full suite passed 5,641 tests. The BPW read-only full suite passed 3,416
with three existing trailing-whitespace failures in unrelated banks. The default
BPW test command initially auto-fixed those files; they were restored exactly to
HEAD and the suite rerun with automatic fixing disabled. The `--no-ascii-fix` flag
is mentioned in the tests but is not registered, so a temporary pytest plugin set
the existing `no_ascii_fix` option instead. No permanent test infrastructure changed.

Local regeneration and MkDocs builds complete. Remote publication and actual
Blackboard/Canvas import are outside this task; local export validation does not
claim LMS acceptance.
