# Changelog

## 2026-10-27

- Improve two-point distance MC distractors by prioritizing single parental and recombinant
  counts before mixed pairs. Deduplicate displayed distances and sort numerically, preventing
  the correct answer from being the only choice well below 50 cM. Preserve selectable counts
  and three-point behavior. Limit distractors at or above 49 cM to at most half the
  distractors. Focused tests and two-/three-point generator smoke checks pass.

## 2026-10-26

### Ordering audit

- Complete six independent review passes for YAML ordering. Correct the Topic 04 command
  and obsolete subset-validation description, clarify the historical glycolysis migration
  reference, and remove a redundant validation comment. Retain both focused ordering tests.
- Fresh checks: 180 ordering/YAML/helper tests and 9 website alias tests passed. The YAML
  date index remains stale because rebuilding it invokes Git, outside the authorized scope.
  Website artifact regeneration and LMS import remain unverified. See the
  [audit report](archive/audits/yaml_ordering_audit.md).

## 2026-10-25

### YAML ordering

- Add keyed ordering banks with per-step wording alternatives, generated topic-based stems,
  question overrides, and the existing bptools replacement rules. Provide separate native
  ordering and MC ordering scripts sharing one helper, following MATCH/WOMC.
- Migrate the 16S survey, model-organism ranks, and glycolysis structures; retire their
  standalone generators. Every authored step is used, with no count or subset options.
  Reuse moleculelib and preserve the named-pathway clue. Update website task registrations.
- Validation: 180 focused bank/helper checks and 9 website task checks pass. All three
  banks generate both formats, export structurally valid QTI 2.1 packages, and render in
  Chromium; the text checker reports no findings. Full suite: 5705 passed, 5 failures in
  unrelated stale documentation links, document size, and the file-discovery deletion test.

- Revise all three algae biofuel challenge choices to focus on extracting oil
  and separating it from other cell material, following instructor feedback.

- Expand `biofuels.yml` to six descriptions per key: three source descriptions
  and three challenge descriptions. Keep the four biofuel labels unchanged.

- Merge biofuel sources and challenges into `biofuels.yml`, with two alternate
  descriptions per type. Use one website task and retain a ten-point selection
  by assigning culture enrichment two points.

### Question banks

- Clean the plant transgenes bank with the bptools voice checklist and humanizer:
  remove trait hints from labels, unsupported praise, and unclear source claims.
  Keep three descriptions per prompt and four pairs per question. Distinguish AVP1
  from gutD by function, remove the unnamed mangrove gene, and replace vague medical
  and shelf-life categories with antibody and antisense polygalacturonase examples.
- Refresh the Nobel bank to 2026, add 2023-2025 topics and move 2022 topics to distractors.
  Disable NOT questions so students always select a current-year topic. Preserve the
  short phrase structure and five-choice format; retain older distractor wording.
  Verified keys against prize sources, passed 12 focused checks, reviewed a browser
  preview, and found no advisory text issues in eight generated samples.
- Add topic04 remediation-site, biofuel-source, and biofuel-challenge matching banks using
  the talking points. Add plain-language glucose MC and Agrobacterium/gene-gun/CRISPR TFMS.
- Add `--mc` to the 16S survey ordering generator while retaining its original ORDER mode.
  MC questions use shuffled numbered steps and four possible sequences.
- Correct DNA-SIP/RNA-SIP and subtraction wording, remove the XNA base-count error, and
  remove stale "this week" and bonus wording from the historical 2022 Nobel bank.
- Record the ten-point selection and answer/preview checks in
  [BIOTECH_TOPIC04.md](archive/BIOTECH_TOPIC04.md).

### Documentation

- Add [TOPIC_QUESTION_DEVELOPMENT.md](TOPIC_QUESTION_DEVELOPMENT.md) with a reusable workflow
  for topic scope, coverage gaps, book research, parallel question design, complete review
  examples, answer checks, and candidate delivery. Link it from the authoring guide.

## 2026-10-24

### Behavior or Interface Changes

- Improve hypothesis selection with observed counts; add `-c/--num-choices` (4 or 5).
- Add default random mix and exclusive `--null`, `--alt`, and `--mix`; remove `--scenario`.
- Retire `chi2-review_hypotheses.py` and its registrations in favor of the selection banks.

- Use dice modes `degrees-free`, `expected-count`, and `row-calc` in output filenames. Use
  plain word-and-number df choices, varied misconception-based expected-count
  distractors, and worked single-row contributions with slanted fractions and
  bold decimal results. Randomize the answer's numerical rank while retaining
  ascending choices; exclude equivalent and rounded duplicate answers.
- Retire the dice calculation-error and interpretation modes. Keep all six face
  rows and remove unused critical-value and hypothesis-decision calculations.
- Put dice `-k/--kind`, `-D/--degrees-free`, `-E/--expected-count`, and
  `-R/--row-calc` selectors in one mutually exclusive group, retaining
  expected-count practice as the default.

- Check that Playwright Chromium launches before collecting questions with `-I`,
  or before direct question-file writes. Missing browsers fail immediately with
  installation instructions instead of failing after the question file is saved.

- Record in [HUMAN_GUIDANCE.md](HUMAN_GUIDANCE.md) that executable and library names
  should differ near the beginning to support autocomplete.
- Move chi-square generators into `problems/chi_square/` and use descriptive
  `chi2-` filenames for calculation, table selection, dice practice, error finding,
  Hardy-Weinberg testing, hypothesis selection, and lab-partner review.
- Keep the shared helper named `chisquarelib.py` so autocomplete distinguishes it
  from the `chi2-` executables. Update test paths, classifier inventory paths, and
  documentation. Preserve generator executable permissions.
- Coordinate the new paths with BPW tasks and retain curated title and Bloom metadata
  for the newly named output banks.
- Validation: all chi-square task variants generate questions. The full suite passes
  5677 tests; the unchanged file-discovery deletion test still raises `FileNotFoundError`.

### Documentation

- Refocus the Topic 07 candidate list on chi-square and binomial offspring questions.
  Separate eight earlier-topic candidates and four optional discussions, add eight explicit
  binomial examples, and preserve original question numbers for review.

- Revise all 40 Topic 07 candidates in plain language with explicit lettered choices,
  a marked correct answer, and a separate instructor explanation for each question.

- Add [GENETICS_TOPIC07_QUESTION_CANDIDATES.md](archive/GENETICS_TOPIC07_QUESTION_CANDIDATES.md)
  with 40 book-informed candidate questions, grouped by parallel learning goals, including
  original example data, expected reasoning, source passages, and review priorities.

## 2026-10-23

### Behavior or Interface Changes

- Retire paired chi-square hypotheses from Biostatistics as well as Genetics;
  remove the remaining task, generator mode, and catalog references. This supersedes
  the earlier audit decision to retain it for Biostatistics.

- Use consistent amber for the chi-square statistic in calculation-table footers,
  matching statistic labels; keep chi-square test names neutral.

- Standardize chi-square terminology across Python generators, MC statements, and
  matching: blue null hypothesis (H0), orange alternative hypothesis (Ha), violet
  level of significance (alpha), and amber chi-square statistic (chi-squared symbol).
  Distinguish the chi-square test procedure from its numeric statistic and use
  parenthesized symbols consistently.

- Place October 22-23 changelog entries under category headings to resolve orphan-bullet warnings.

- Audit correction: retain paired hypotheses for the active Biostatistics consumer
  and register its mode explicitly. Clean retired genetics metadata and point the
  download test at the retained binomial bank. Remove random sampling at library import.

- Remove the unregistered paired-hypothesis mode and its private helpers/data,
  the binomial-only mode selector and unused scenario, and retired generated artifacts.

- Remove standalone factorial and factorial-denominator explanation banks, their
  generator modes, and build tasks. Retain applied binomial and Pascal practice.

- Finish factorial-practice choices with evaluated numeric results and remove the
  instruction to leave expressions unevaluated. Show the addition distractor as a
  sum without falsely equating it to a factorial.

- Simplify the Pascal shoe-family prompt to ask about one randomly selected sex,
  retaining its colored count and symbol plus inline N choose r notation.

- Remove redundant observed-data and Hardy-Weinberg table captions. Move the
  chi-square critical-value/right-tail explanation from the caption into prose.

- Center shared chi-square table column headings without changing body-cell alignment.

- Add decorative phenotype-word colors across topic07 probability and chi-square
  generators: purple/white flowers, black/brown coats, red/pink/white flowers, and
  yellow/green peas. Preserve text labels and use readable dark colors on white.

- Show both boys and girls counts in Pascal shoe-family prompts with number words,
  numerals, matching offspring-bank colors, and male/female symbols.

- Place Pascal practice binomial notation inline with its N choose r wording.

- Give Pascal triangle rows equal-width cells while retaining borders and modest padding.

- Default worked chi-square tables to no caption and remove redundant dice/calculated
  captions. Keep N italic on white and restrict the footer accent fill to the chi-square
  result cell; retain optional captions for labeled table comparisons.

- Rename the calculated chi-square ACCEPT mode and bank to SUPPORT; retain
  fail-to-reject wording and the existing REJECT generator mode.

- Make Pascal practice connect N choose r and binomial notation to a coefficient
  in a bordered, padded row without index labels. Use distinct numeric row entries
  as choices (three for row 5); remove the probability calculation.

- Frame Pascal triangle practice around the woman who lived in a shoe: 5-9 children,
  exactly 0 through N girls or boys, and independent equal probabilities.

- Add standalone `pascal_triangle.py` row-reading MC practice for rows 6-12, using rendered binomial
  notation and distinct answer values drawn from the supplied row.

- Remove the standalone progeny coefficient MC bank and its build registration; retain
  coefficient calculations used by the binomial and explanation questions.

- Filter binomial-practice distractors to 0.5%-60%, excluding duplicate displayed
  percentages and the correct result. Supplement omission errors with substitutions
  using only counts and probabilities from the scenario. Verify four distinct choices
  across all 15 scenario/count combinations (300 sampled questions).
- Simplify calculation-table footers to left-aligned N and right-aligned chi-square,
  removing individual count sums and filler dashes. Match footer and heading accents;
  choose a random existing dark color-wheel color when no accent is supplied.
- Standardize calculation-table totals through one shared helper: Total, expected and
  observed sums, a calculation dash, and chi-square equals the supplied statistic or
  a blank. Use three decimal places for worked statistics; preserve intentional errors.
- Show only the decimal chi-square total in shared worked tables, omitting the reduced
  fraction so the total follows the decimal row contributions.
- Redraw dice error-analysis datasets when any observed count equals its expected count.
  Show contributions to three decimals so small nonzero values remain visible; retain the
  mathematically correct zero total for the deliberately unsquared-differences error.
- Replace dice calculation choices with error analysis of a lab partner's complete six-row
  chi-square table and total. Apply one mistake consistently: divide by observed counts,
  omit squaring, square the expected denominator, or divide by six faces. Avoid undefined
  divisions and cases where dividing by six is correct. Simulate fair or biased die rolls
  instead of shuffling fixed deviation templates; vary totals from 30 to 180 in multiples
  of six. Verify table arithmetic and answer keys for all four errors, check 500 simulated
  datasets, and review calculation and interpretation samples at narrow and desktop widths.
- Remove the remaining horizontal rules from chi-square calculation-choice, error-analysis,
  paired-hypothesis, and lab-partner hypothesis questions; table styling separates the sections.
- Remove the horizontal rule between the data table and prompt in calculated chi-square
  questions (shared by ACCEPT and REJECT modes).
- Remove the horizontal rule immediately before the lab-partner paragraph in Hardy-Weinberg
  chi-square questions.
- Finish coefficient choices with their numeric sequence counts and binomial choices with
  calculated decimal probabilities and percentages. Use the shared worked-binomial renderer
  and result formatting; remove the instruction to leave binomial answers unevaluated.
- Remove the unnecessary probability-calculation instruction and zero-factorial reminder
  from coefficient question stems.
- Add `binomiallib.binomial_probability(n, k, p, q)` to render the whole worked
  `C(n,k) p^(n-k) q^k` choice using exact fractions through the calculation. Use
  `worked=False` for setup-only practice. Remove the older generator's calculation/rendering
  helpers. Draw distractor `n` and `k` only from the total and two phenotype counts stated
  in the question, with `k <= n`; use only 1:1 or 1:3/3:1 probabilities for `p` and `q`.
  Retain results between 1% and 40%, excluding the correct displayed percentage and repeated
  percentages. Use fewer choices when these mistakes yield too few distinct eligible results.
  All choices use the same equation with internally consistent arithmetic. Verify 330 results independently
  by enumerating outcomes, including zero-count and all-one-outcome cases.
- Render factorial quotients in coefficient choices and coefficient explanations as stacked
  numerator/denominator fractions with a horizontal bar, including the distractors.
- Include H0 and Ha with every null/alternative hypothesis mention in the single-hypothesis
  chi-square question stems, using HTML subscripts consistent with the paired questions.
- Reuse the offspring-sex generator's stacked binomial coefficient notation in phenotype
  probability expressions, sequence-count factorial choices, and coefficient interpretation
  stems. Move the existing parentheses renderer into `binomiallib.py`; preserve the original
  sex-count formula output and keep complete new expressions inside presentation tables.
- Standardize chi-square calculation headings as Category, Expected, Observed, Calculation,
  and Statistic. Compact the dice worked examples into these five columns, retaining the
  substitution and squared numerator in Calculation and the contribution in Statistic.
  Reorder Hardy-Weinberg counts to match; preserve exact totals and grading calculations.
- Add an optional `color` argument to the shared chi-square table renderer and its helpers.
  Colored captions regain a full-width pale band and accent border; column headings use the
  same tint while body rows remain neutral. Keep the default data-table appearance unchanged.
- Use the lab-partner comparison's existing orange, blue, and magenta for both tables and
  answer labels. Give critical-value reference tables a subdued gray accent by default.
  Document the argument in the usage guide.

### Fixes and Maintenance

- Consolidate offspring binomial notation in `binomiallib.py`: both probability generators
  use its coefficient, fraction, and expression renderers. Remove the older generator's
  duplicate fraction renderer and hand-built equation tables; preserve its calculation steps.
- Size binomial parentheses directly and remove their table's positional offset so expression
  rows reserve their full height. This removes vertical choice scrollbars caused by transformed
  parentheses overflowing the layout box. Browser measurements on 20 coefficient choices at
  390 and 768 pixels confirm no horizontal or vertical overflow.
- Synchronized shared style guides, tests, and repository support files from the starter template.

### Developer Tests and Notes

- Verify binomial notation against the original renderer and sex-count formulas byte for byte.
  Independently enumerate offspring sequences to check every supported coefficient count and
  probability setup, including zero-count cases and unique correct answers. Generate five
  questions per updated mode; text advisories and focused lint pass. Review desktop and
  narrow-screen self-tests; retain WebP review captures and remove temporary checks.
- Verify the compact calculation layout with five existing chi-square tests, focused lint,
  temporary checks of Expected/Observed column mapping and totals, and a fresh five-question
  dice interpretation bank with desktop and narrow self-test screenshots.
- Pass five existing chi-square tests, 86 Markdown link checks, and focused pyflakes checks.
  Temporary comparisons confirm unchanged default markup and unchanged content and answer keys
  across 18 seeded error/outcome cases. Generate five questions and inspect standalone and
  self-test screenshots at desktop and 390-pixel widths. Existing narrow-screen table overflow
  remains unchanged; this update changes color treatment only.

## 2026-10-22

### Behavior or Interface Changes

- Shorten baby-weight and Busse Woods conclusion reminders to one optional
  consider sentence referring to the stated significance level, with hypothesis
  and significance-level colors matching the terminology bank; remove the incorrect
  reference to entering a p-value above.
  Expand lab-partner hypothesis labels and state independent assortment and
  complete dominance briefly in the dihybrid scenarios.

### Chi-square worked calculations

- Show compact, smaller arithmetic beside bold final answers in dice MC choices
  for expected counts, degrees of
  freedom, category contributions, and summing contributions. Assess the choice
  of calculation without requiring a calculator. Keep calculator-based numeric
  entry in the existing assignment generator; remove equivalent distractors after
  rounding and evaluate sums from the displayed numbers.

- Route critical-value reference tables through the same shared renderer, with
  selectable degrees of freedom and right-tail probabilities. Remove the duplicate
  Hardy-Weinberg reference table and replace hardcoded dice critical values with
  library calculations. Finish fail-to-reject wording in the affected prompts and
  pair symbols with full names in the chi-square paired-hypothesis choices.

- Generalize `chisquarelib.py` table rendering for arbitrary category labels, row
  counts, and column headings. Reuse it for dice, hypothesis and lab-partner
  questions, error tables, missing calculations, and Hardy-Weinberg tables. Keep
  supplied work and totals verbatim, including intentional errors; calculate correct
  worked examples only through the separate worked-table helper.

- Expand dice interpretation tables to show observed minus expected, its square,
  each chi-square contribution, and the summed statistic. Show the exact total
  alongside its rounded value. Keep calculation answers hidden in calculation modes.

### Factorials and binomial reasoning

- Remove the combined dice chi-square MA conclusions and quantity-to-value
  matching modes and their writers. Retain separate expected-count,
  degrees-of-freedom, calculation, and interpretation MC modes. Remove the
  matching task registration; no task row registers the removed MA bank.

- Add four Lecture 07B/07C offspring-practice modes: factorial meaning for labeled
  seeds, factorial arrangement counts, binomial expression setup, and why repeated
  phenotypes require division by factorials. Include 0! and surviving-offspring
  probabilities; require no calculator. Default to binomial setup. Remove the four
  introductory modes (independence, outcomes, supplied tables, and general
  calculations), their unused helpers, and the retired distribution test. Retain
  the original advanced generator.

### Biostatistics question clarity

- Use explicit `fail2reject` and `doesntsupport` replacement tokens in the
  decision bank; student-facing phrases remain fully spelled out.

- Align non-numeric test-selection and Z/t tutorial banks with the test colors.
  Use fail-to-reject and sufficient/insufficient evidence language in decision
  questions. Simplify hypothesis terminology and remove a misleading sample-size
  cutoff from test selection.

- Add a brief conclusion prompt to each numeric test question using a significance
  level of 0.05 and the reject/fail-to-reject evidence distinction. Keep the graded
  response as the p-value. Pair hypothesis symbols with their full names throughout
  calculation questions and hypothesis-practice stems and choices.

- Align baby-weight scenarios with their selected alternative hypotheses and repeat
  the one-tailed or two-tailed requirement in p-value entry instructions.
- Apply the matching-set template palette to test labels: Z blue (`#003fff`),
  t green (`#007a00`), F magenta (`#c80085`), and ANOVA gold (`#935d00`).
  Emphasize tail labels in all numeric test questions with bold, enlarged text:
  one-tailed teal (`#00775f`) and two-tailed red-orange (`#b74300`). Repeat the
  styling in p-value prompts while preserving the corrected Busse Woods wording.
- Name population means and variances explicitly in hypothesis-practice research
  questions, and clarify that two-sided alternatives include either direction.

## 2026-10-21

### Biostatistics question wording

- Make the one-tailed or two-tailed choice prominent in both Busse Woods F-test
  and Welch t-test questions, including the p-value entry instruction. Express
  each alternative hypothesis in plain language, preserving calculations and defaults.

### Fixes and Maintenance

- Label the tail count in both the statement and p-value entry instruction for
  the Busse Woods one-sample Z/t tests and ANOVA. Specify the right tail for the
  ANOVA F-test; retain all calculations and defaults.

## 2026-10-20

### Genetics quiz questions

- Draw all six dice faces with compact HTML pip tables beside their numeric
  labels in every dice question mode, avoiding dependence on dice-symbol fonts.
- Replace the turn-taking hypothesis distractor with confusion between sample
  size and expected ratio. Use parallel "enough evidence" / "not enough evidence"
  dice conclusions, and document the four-context limit of the hypothesis banks.
- Add four offspring-probability quiz modes (MC, MA, Matching): independence,
  visible outcomes, supplied probability tables, and calculations with two to four
  offspring. Supply intermediate arithmetic for unequal probabilities and identify
  surviving offspring explicitly in the short-tail examples.
- Add six dice chi-square modes covering expected counts, five degrees of freedom,
  a missing contribution or sum, interpretation, combined statements, and Matching.
  Recompute the Bozeman example as 58/6 and use evidence-based conclusions without
  claiming that failure to reject proves a die fair.
- Simplify standalone null/alternative choices and lab-partner error analysis.
  Remove observations from prediction-only questions and the repeated eye-roll
  opener; retain the paired mode for its existing Biostatistics consumer.
- Save the approved plan and authoring/review evidence under `docs/active_plans/`.
  Add two durable tests for independently enumerated probability mass and dice
  arithmetic/decisions. Independent review led to multiple-key MA outcomes,
  parallel hypothesis choices, and three distinct Matching pairs.

## 2026-10-14

### Fixes and Maintenance

- Rephrase the Genetics terminology genome definition as "all the DNA in an
  organism" and regenerate both PGML forms in the local output directory.

- Use the existing `perl_string_literal()` helper in both YAML matching PGML
  generators and shared Perl hash keys. Preserve apostrophes in matching data,
  exclusions, prompts, notes, and which-one choices without escapes that PG's
  translator doubles into invalid Perl. Leave the renderer and PLE unchanged.

- Correct CSS at the question generators for QPM conversion: add hexadecimal color
  prefixes and remove the ignored `spacing` property in ordered tetrad octads,
  give shared phylogenetic tree row heights pixel units, and use `vertical-align`
  in shared enzyme tables. Preserve question data and answer selection.

### Developer Tests and Notes

- Complete independent Plan, Test, Style, Docs, Legacy, and Comment audits of
  the ten-file BPQ change set. Clarify two complete-literal variable names and
  distinguish final regeneration from earlier render evidence. The independent
  checks pass 164 YAML tests and 34 shared-helper/PGML tests; the focused ten
  tests pass again after the naming correction. No permanent tests are added
  by the audit. Final renderer verification passes for both regenerated Genetics
  forms at seeds 1 and 1234, with no errors, warnings, or internal diagnostics.

- Regenerate 22 affected matching/which-one files from 11 YAML banks with the
  existing BPQ CLIs into ignored `output_pgml_escaping/`. All 44 renders (seeds 1
  and 1234) pass against the clean renderer HEAD image using its existing API
  lint helper, with no error flags, PG warnings, or internal diagnostics.
  Verify the original Genetics terminology matching HTML in a browser. These
  original render receipts preceded the final genome wording edit. Recheck both
  final PGML forms at seeds 1 and 1234 and refresh their four HTML/JSON receipts.
  The YAML test
  suite passes all 164 tests, including apostrophe coverage. Keep website copies
  unchanged; regenerated PGML and temporary render receipts remain in BPQ output.

- Verify 32 fresh items across 16 parameter variants through Python QPM validation
  and Rust PLE Native JSON conversion, including both tetrad formats and the already
  corrected Beadle-Tatum generator. Pyflakes and `git diff --check` pass. Keep existing
  website banks unchanged; regenerated artifacts need separate acceptance.

## 2026-10-13

### Behavior or Interface Changes

- Allow equal-sized fragments in medium restriction digests while easy forbids
  co-migration and rigorous requires it. Keep medium linear defaults at 12 kb and
  three cuts; five consecutive choices now admit eight answer sets instead of one.
  Include the gel-band co-migration explanation in medium linear questions.
- Add --random to poisson_flies.py to sample the five distinguishable parental
  crosses independently of question number. Preserve default cycling. Check 300
  single-question draws cover all five answers and emitted items retain five choices
  with one correct key; verify the default cycle and pyflakes.

- Add opt-in --random to both epistasis_test_cross.py directions. Sample the prompt
  ratio independently of question number while retaining even default batch cycling.
  Verify 840 questions across both modes and settings: all nine forward and five inverse
  prompts appear, defaults cycle evenly, five choices contain one valid key, and pyflakes passes.

- Add --random to dihybrid_cross_epistatic_gene_interactions.py so independent
  single-question runs can sample all seven interactions. Preserve even cycling
  by default. Verify 140 random question-1 calls cover all seven, a 140-question
  default batch yields 20 per interaction, and every emitted item has one key.
  Confirm monohybrid_degrees_of_dominance.py already randomizes all three modes.

- Store each shared-cross parent's name color in a required `name_color` JSON
  field using `#RRGGBB`. Select colors once when creating a scenario and reuse
  them in stems and worksheet labels across all four question modes. Existing
  scenario files need the field added; malformed color values are rejected.

### Fixes and Maintenance

- Restore phenotype color swatches in monohybrid degrees-of-dominance exam text
  by emitting hex colors instead of CSS color names. Color the names with readable
  dark shades while retaining the exact Punnett-square colors in the swatches.
  Verify all 13 colors through exam HTML cleanup and DOCX, all 36 palette/dominance
  combinations, and a browser preview. Leave scenario randomization unchanged.
- In both ABO blood-type generators, color male terms and symbols dark blue
  (`#004d99`) and female terms and symbols dark magenta (`#99004d`). Bold the
  stated blood types and consistently phrase them as "type A blood", including
  the corresponding O, B, and AB cases. Verify all 16 phenotype pairs in each
  question family, both child sexes in mother questions, and the browser preview.
- Color gametes dark green (`#006400`), genotypes dark blue (`#003366`), and
  phenotypes dark orange (`#9A4600`) consistently in shared-cross stems, hints,
  and worksheets. Preserve the blank worksheet cells and existing calculations.
- Sort HLA choice markers by their visible labels instead of HTML color markup,
  grouping A alleles before B alleles and C alleles while preserving chromosome colors.
  For example, `A1,B8,C6,A9,B2,C2` becomes `A1,A9,B2,B8,C2,C6`.
  Verify ordering and answer keys in 35 generated items covering color and black-and-white
  output with 2, 3, and 7 markers; pyflakes and the question-text checker pass.

### Developer Tests and Notes

- Remove the newly added difficulty-policy matrix from permanent digest tests;
  difficulty settings remain tunable. The map enumeration and 400-question sample
  are one-time verification evidence, not lasting gates on answer-set counts.

- Shared-cross color checks: two focused tests pass, including enumeration of
  all 81 two-locus crosses, saved color reuse in all four modes, escaped names,
  and invalid color rejection. Verify four CLI exports and their colors in local
  Chromium; term contrast on white ranges from 6.46:1 to 12.61:1. The advisory
  checker still reports existing choice spacing and optional hint-length cues.

## 2026-10-12

### Features

- Consolidate large-cross questions in unique_counts.py and unique_counts_lib.py,
  retaining the three existing homework paths as thin entry points. Add mutually
  exclusive --gametes, --genotypes, and --phenotypes flags, with --parent 1/2 for
  gametes. Save named parental genotypes to JSON once and reuse them across questions;
  validate matching loci and refuse scenario overwrite. Preserve blank worksheet
  tables, numeric choice order, and five-choice defaults. Check all 81 two-locus
  crosses by independent gamete enumeration, JSON round trips, and all four modes
  through the exam task runner. Focused generator and lint checks: 406 passed.

- Add disjoint five-term halves of genetics_terminology.yml and
  mendelian_genetics_terms.yml for complete exam vocabulary coverage. Preserve original
  homework banks, all definition variants, and formatting rules. Keep meiosis_terms.yml
  unsplit; no matching-generator changes.

- Add `bonus_content/disney_princesses.yml` for the 13 characters on Disney's
  official Princess roster. The assistant reused nine movie-bank clues and wrote
  four new clues; add 13 alternatives from another LLM draft pasted by the user.
  Each princess has two possible clues (26 total); randomly select four princesses
  per question. Correct the attribution and treat all princess clues as editable
  drafts subject to the style and length guidance.
- Add `bonus_content/disney_movies.yml`, preserving 39 author-supplied plot clues
  for 37 Disney and Pixar movies. Keep both clues for Sleeping Beauty and Beauty
  and the Beast as alternatives under their movie titles, and preserve supplied
  wording even when a clue exceeds 100 characters. Use plain straight quotes and
  apostrophes in place of escaped curly quotes. Replace the Bambi clue with the
  author's revised wording about losing his mother and befriending a rabbit.
- Add `bonus_content/mcu_avengers.yml`, a bonus matching bank with eight MCU Avengers
  and 31 cryptic clues, including the author's original hammer, shield, assassin,
  and archer clues.
  Preserve author-supplied wording; style guidance and the 100-character limit
  apply to agent-authored clues. Questions randomly select four characters and one clue each.

### Fixes and Maintenance

- Preserve even interaction coverage as the default for metabolic epistasis batches.
  Add opt-in `--random` for independent single-question draws, as requested by the
  instructor. Verify two occurrences of every interaction in a 14-question default
  batch and varied interaction ratios across 70 random single-question calls.

- Randomly sample the metabolic epistasis interaction instead of cycling by question
  number. Single-question assessment runs can now draw any existing homework pathway
  rather than always returning digenic inheritance. Keep pathway choices unpinned.
  Validate 70 single-question calls with all seven ratios represented and one correct
  answer per item; hybrid-cross and lint checks pass (404 tests).

- Add circular-digest `-c/--num-choices` support. Sample maps whose correct bands fit
  a consecutive range with at least one distractor; share range construction with linear
  digests in digest_lib. Preserve default output when the option is absent.
- Enumerate existing easy/medium maps before choosing exam difficulty: five consecutive
  choices retain 34 easy circular maps and 38 medium circular maps. Medium linear fragment
  fits 76 maps but always yields bands {1,2,4,5}; document this limitation. Retain medium
  per instructor preference when it fits five choices.

- Replace sparse linear-digest choices with a consecutive positive range containing all
  correct bands. Allow shifted ranges such as 2-6 kb. Reject maps when the band span does
  not fit or the distinct correct-band count is not strictly less than the choice count.
  This supersedes the nearby-length selection described below.

- Refined question voice guidance to allow subtle alternating row shading for readable data lists,
  while preserving matrix/diagram geometry and distinguishing scientific color from row shading.
- Add optional `-c/--num-choices` to linear digests, retaining every correct band and nearby
  length distractors in numeric order. State "Select all that apply" in every mode.
- Add Punnett-square choice counts (2-6; default 6). Drop the most distant parental-genotype
  errors first, breaking ties randomly; randomize scenarios and choice order.

- Repair the four BPQ-owned genetics HTML findings: darken shared HTML gel bands
  to `#35558f` while preserving their blurred glow and geometry; reuse a dark
  metabolite-color mapping across the pathway figure, stem, and answers with valid
  CSS colors; keep the complete binomial model in one presentation table; and
  darken the shared Table 1 label to `#5d3b00`. Preserve question content, grading,
  and the original audit evidence. No EF or QPM source changes are included.
- Preserved the established `qti_package_maker` imports and `QTIPackageInterface` API. QPM
  abbreviates QTI Package Maker and names Rust, Wasm, and project integration surfaces; QTI
  format terminology remains unchanged.
- Add the genetics exam HTML repair audit covering all 54 selected tasks and
  five additional generated variants through the final PDF. Document four BP
  display-repair groups affecting five tasks, with raw examples and PDF crops;
  distinguish EF choice wrapping from BP source defects. Limit the handoff to
  demonstrated display problems, excluding lint, style-policy enforcement, and
  new validation gates. Preserve the gel's intentional blurred edges and glow;
  recommend darker bands for readability and remove numerical contrast targets.
  No generator or rendering code is changed.
- Extend the `tl_` module prefix throughout the tree library: `tl_definitions`,
  `tl_lookup`, `tl_output`, `tl_permute`, `tl_sorting`, and `tl_treecode`.
  Update package and standalone imports, all three generator callers, and the
  library documentation to avoid generic module names in fallback imports.
- Rename the phylogenetic tree helper from `tools.py` to `tl_tools.py` and update
  package imports, standalone imports, callers, and tree-library documentation.
  The specific module name avoids the reserved support-directory import name.
- Remove the local deleted-file discovery test, which exercises vendored hygiene
  internals, and the filename-based library import sweep with its separate loader.
  Remove shallow molecule HTML and hybrid-cross palette smoke tests, the exact
  Perl-source PGML assertion, redundant PGML marker/file-writing checks, and
  boxplot wording checks. Retain scientific, data-validation, escaping, and export
  recovery coverage; leave upstream-owned tests and shared dependencies intact.
- Synchronized shared style guides, tests, and repository support files from the starter template.

### Developer Tests and Notes

- Circular five-choice verification: 404 focused checks pass, including 200 easy and
  200 medium sampled maps with independent modulo-distance wraparound keys. Remove the
  temporary check after validation. Five easy CLI items pass the advisory text checker
  without findings. The full medium exam build has zero skips. Rendered example: cuts
  at 1, 5, 11 on a 12 kb circle give 4, 6, 2 kb, correctly keyed A/C/E in a 2-6 kb bank;
  3 and 5 kb remain consecutive-length distractors for interval-reading errors.

- Consecutive-bank follow-up: 404 focused checks pass. Temporary independent enumeration
  covers all 165 three-cut maps for fragment and strand interpretations; verifies complete
  consecutive banks, preserved keys, rejection of oversized spans and all-correct banks,
  and the shifted 2-6 kb example. Remove the one-time check after validation.

- Choice-limit verification: 414 focused generator/scenario/lint checks pass. Enumerate
  all 165 three-cut maps on a 12 kb fragment to check that five-choice selection retains
  every true interval, and cover all six Punnett crosses at choice counts 2-6.
- Before: a medium fragment bank could exceed A-E, and Punnett selection always had six
  squares. After: the rendered exam has five choices for each. Independently read the
  fragment cuts at 3, 9, 11 kb: bands 3, 6, 2, 1 kb match A/B/C/E; 5 kb is the nearby
  subtraction-error distractor. Strand cuts at 2, 7, 10 kb give 5 and 3 kb, matching B/D.
- Rendered Punnett example: AA x aa gives all Aa (B). Distractors AA x AA, Aa x aa,
  aa x aa, and AA x Aa model misidentifying one or both parental genotypes. The tied
  two-allele-distance distractor Aa x Aa was omitted. Choice order and scenarios are random;
  digest lengths remain sorted. Five-item advisory checks: no digest findings; Punnett
  K4 article warnings are false positives on allele labels such as "A a", not prose.

- Genetics HTML repair: generate 14 fresh questions and inspect Chromium output
  and all seven LibreOffice PDF pages at the normal 150-DPI export cap. Check gels
  in color and grayscale, pathway colors at 3/5/8 metabolites, and binomial models
  at 4/5/10 offspring. Controlled comparisons preserve gel band membership,
  pathway nutrient answers (also at 17 metabolites), binomial formulas and keys,
  and chi-square values and keys for both outcomes and all three error selections.
  Keep raw records, browser captures, PDF, and logs locally in ignored
  `output_genetics_html_repair/`; remove temporary verification scripts and add no
  permanent tests. The full suite reports 5,556 passed and 10 import-policy
  failures involving the separate `qti_package_maker` rename, with two existing
  source-size warnings; none of the failures names a repaired source file.
- After prefixing the remaining tree modules, all 5,424 tests pass in 12.32 seconds
  with the same two warnings. Package and standalone imports, rendering, distances,
  grouping, and permutations pass with unrelated modules occupying the old generic
  names in `sys.modules`.
- Reproduce six failures from the two reported causes before cleanup (5,533 pass).
  After cleanup, the full `source source_me.sh && pytest tests/` run passes all
  5,424 collected cases in 11.95 seconds, with the same two source-file-size warnings.
  Direct checks pass for package and standalone tree imports, distances, grouping,
  and HTML rendering. Remove four local test modules and four additional test
  functions (215 lines); shared test helpers and dependencies remain in use.

## 2026-10-10

### Behavior or Interface Changes

- Describe heterozygous females as tortoiseshell without labeling the mechanism
  as codominance or adding an X-inactivation explanation. State the equal XX/XY
  sex-ratio assumption used for all-kitten probabilities and keep the orange/black
  model specific to these cats. Remove redundant "true-breeding"
  labels from the white-eyed female/red-eyed male fly cross; retain it for the
  red-eyed female, whose homozygous genotype must be specified.
- Color eye phenotypes and sex labels in reciprocal X-linked fly crosses, reusing
  the dark red, gray, blue, and pink from `poisson_flies.py`. Apply the same labels
  to stems and choices. Color cat coat phenotypes orange and charcoal, alternating
  orange and charcoal letters in "tortoiseshell," starting with orange. Add sex symbols
  consistently in both generators and use "an orange" in crosses.
- Correct daughter-only tortoiseshell keys by translating the requested group
  "daughters" to the outcome sex "female" before calculating the fraction.
- Remove the reciprocal fly distractor "All offspring are red-eyed," which was
  also true for the red-eyed mother/white-eyed father cross.
- Let students infer the woman's recessive carrier genotype from her wildtype
  phenotype and affected father. Remove the explicit carrier label and the
  unnecessary grandmother phenotype from these scenarios.
- Require both traits to have variable outcomes in the requested offspring group
  for dominant/X-linked recessive variations. Add 1/8 and 3/8 to the answer ladder
  and remove 100%. Randomly alternate five ordered choices between 0% through 50%
  and 12.5% through 75%, independently of the answer. Sample the attainable answers
  (1/8, 1/4, and 3/8) equally before randomly choosing a compatible scenario.
- Describe unaffected family members and offspring using disease-specific wildtype
  traits from the disorder YAML, such as height or androgen response. Italicize
  "wildtype" and retain the associated disease color. Retain genetic-testing
  evidence where a non-carrier genotype is specified.
- Keep disease background paragraphs compact and color only their headings.
  Add a small gap before the family scenario, group family facts by disease,
  italicize the reminder, and separate the final question. Inline paragraph
  margins preserve this prose layout in self-tests.
- Color gender references blue/pink and X-linked/autosomal disorder names
  gold/purple in the dominant/X-linked recessive variations generator. Apply
  the same colors to disease headings, abbreviations, gender symbols, and repeated
  references in the family story and final question.

### Developer Tests and Notes

- Independently verify both fly crosses and all five distractor subsets per
  cross: every choice set has exactly one true answer. Check all six cat crosses
  against hand-worked offspring distributions and verify all 12 denominator cases.
  The wording revisions preserve choices, keys, and random state for 100 matched
  seeds per generator. Nine scenario tests and six scoped hygiene checks pass;
  five-item CLI runs and desktop/mobile previews succeed for both generators.
- Verify alternating tortoiseshell letters in five native desktop/mobile previews:
  orange "trossel," charcoal "otiehl," intact spelling, and no horizontal overflow.
- Verify both reciprocal fly keys and all six cat crosses with both offspring
  denominators. Add six regression cases for the daughter-only cat bug; nine
  scenario tests and nine scoped hygiene checks pass. Review five native previews
  per generator on desktop, plus mobile captures. All six text colors pass the
  5.5:1 target on white (measured 6.23-15.91:1), including rendered glyph samples.
  The only text-checker findings are the existing generic fly lead-in.
- Verify the carrier-inference wording with 100 matched-seed comparisons that
  preserve answer keys, choices, and random state. Review five native self-test
  examples and desktop/mobile rendering. Three scenario tests, three scoped
  hygiene checks, and pyflakes pass; the text checker reports no findings.
- Independently enumerate gametes to verify the two-trait scenario pool and reject
  fixed-trait cases. All 56 supported scenarios accept either five-choice ladder.
  Three scenario tests and six scoped hygiene checks pass. Review five rendered
  examples plus mobile layout; the text checker reports no findings. The refreshed
  999-question bank has 345 keys at 1/8, 362 at 1/4, and 292 at 3/8; its lower and
  upper choice ladders occur 499 and 500 times.
- Verify all 2,544 disease/scenario combinations with wildtype wording; 100
  matched-seed comparisons preserve choices, answer keys, and random state.
  Desktop/mobile previews retain trait colors and wildtype italics without overflow.
  Six scoped hygiene/YAML checks and pyflakes pass. Regenerate 999 questions and
  the self-test; 0% and 100% answers account for 5.4% and 5.1%, respectively.
- Check the final heading-only background colors, 0.75em scenario gap, and italic
  reminder in desktop/mobile self-tests. Five matched scenarios retain their wording,
  choices, and keys. Regenerate all 999 questions and the self-test after the layout update.
- Verify the new blue/pink/gold/purple text at 6.00/6.13/5.54/7.70:1
  contrast against white, including rendered glyph samples. Desktop and mobile
  self-tests render without horizontal overflow. Thirty fixed-seed comparisons
  preserve all wording, choices, and keys; scoped lint and three hygiene checks pass.
  Regenerate the 999-question bank and self-test with the colored labels.
- Independently verify all 240 cross/event/group combinations by enumerating gametes.
  A 999-question export contains 67 zero-percent answers (6.7%) and 48 hundred-percent
  answers (4.8%); all items have one correct key. The 33 shared-helper tests pass.
  The question-text advisory flags only the intentional "None"/"All" endpoint labels.

## 2026-10-09

### Fixes and Maintenance

- Pair the fixed light backgrounds in dihybrid/test-cross tables, the macromolecule
  guide, and PubChem information tables with black text and a white table base.
  This preserves their existing cell colors while preventing inherited dark-mode
  foregrounds from making the content unreadable.

## 2026-10-07

### Additions and New Features

- Add a short calculator-free Z-test versus t-test statement bank for the national-average
  tutorials, with four choices per item and both TRUE/FALSE forms. Cover standard-deviation
  sources, reference distributions, comparison of means, and one-sample t-test degrees of freedom.
- Add calculator-free measures-of-center matching with completed mean and midrange
  calculations, plus an MC question about increasing the largest value without changing
  the median. Both use random small datasets and the shared BBQ/preview/export helpers.

### Fixes and Maintenance

- Address the six-pass audit: annotate the TRUE/FALSE formatter and its callback,
  remove unused decision/matching word rules, distinguish initial 18-answer evidence from the final 17-answer quiz, and rotate
  the active changelog with the repository tool. Keep palette marker aliases,
  following the existing bank convention documented on October 6.

- Ground the Z-test versus t-test bank in the two linked national-average tutorials.
  Test the SD inputs, unknown population SD, Joe's switch to t, and sample size
  minus 1 for degrees of freedom. Remove distribution-swapping and median/mode
  distractors and symbolic n notation. Independently verify every source claim
  and all five TRUE/six FALSE samples against downloaded tutorial text.
  Eleven focused tests pass; review five rendered samples of each form.

- Format TRUE/FALSE in the statement generator for both default and custom stems.
  Keep TRUE green (`#127663`) and FALSE red (`#ba372a`) even beside punctuation
  or inside bold tags. Preserve disabled stems and HTML attributes. The previous
  space-delimited base replacements missed custom bold labels. Ten focused tests
  and scoped lint pass.

- Rewrite median-change questions as server-tip scenarios. Supply the original
  mean and median, identify the extra tip and new total, and state that the other
  four totals stay the same. Use "Does not change" as the correct choice.
  Three focused tests verify the worked centers, reported mean/median, extra-tip
  arithmetic, and median invariant; scoped lint passes.

- Change null-hypothesis text from teal `#007576` to dark indigo `#49358c`
  in the terms matching and decision banks, separating it from green test-statistic
  text (`#00775f`). White-background contrast is 9.67:1 and 5.52:1, respectively.
  Inspect the regenerated quiz and verify its 17 answer keys independently.

- Simplify hypothesis-testing decisions to "reject / do not reject" and "the evidence
  supports / does not support" the alternative hypothesis. Remove "insufficient evidence"
  and comparisons between p-values and critical values or test statistics and significance
  levels. Use four choices per item, a short stem, and "past the critical value" in place
  of ambiguous region wording. Matching uses the same "significance level" term.
- Color affirmative decision phrases dark blue (`#17365d`) and negative phrases dark
  red-orange (`#9c3b10`), for both true and false statements. The two colors have contrast
  ratios of 12.19:1 and 6.89:1 against white; rendered pixel checks agree.

### Developer Tests and Notes

- Initial 18-answer build: plain-language decision revision passed 12 focused YAML/generator tests. Five native
  before/after samples were rendered and independently reviewed; both advisory reports
  had no findings. All 20 source statements use color by decision wording. Selected a
  final print variation with two blue and two red-orange choices, and independently
  verified all 18 keys for that initial build. Evidence is in `output_biostats_review/plain_language/`.
- Initial Z-test versus t-test bank: nine focused YAML/generator tests passed. Independent
  readers verified every source statement, five native samples of each TRUE/FALSE
  form, and all 18 initial quiz keys. Both forms rendered cleanly and had no advisory
  text-check findings; evidence is in `output_biostats_review/AUTHORING_REVIEW.md`.
- Measures-of-center and statement-bank checks passed 12 focused tests and scoped
  `pyflakes`. A one-time independent arithmetic check covered all 78 supported dataset
  variants; five rendered samples per question family were reviewed. The advisory
  question-text checker found no issues. Review evidence is in `output_biostats_review/`.

## 2026-10-06

### Fixes and Maintenance

- Audited all 81 YAML replacement-rule mappings. Kept color-palette placeholders and short
  aliases, replaced obsolete plural/closing-tag workarounds with direct rules, and added full
  inflected forms so color spans cover complete words. Fixed singular-to-plural substitutions,
  lost spaces, misspelled labels, and the proofreading direction replaced by "primase".
  Removed unrelated copied rules and redundant bold wrappers inside color replacements.
- Corrected grammar and typos across the inheritance matching-set YAML banks. Color rules
  now preserve plural spellings, avoid duplicated F1/F2 generation labels, and retain the
  intended genotype and ectopic terminology. Added missing whole-word plural color rules.
- Addressed wording review by removing two dominance variants that incorrectly assume a
  dominant allele is always present, defining genetic code in terms of mRNA translation,
  describing drift through allele-frequency changes, and simplifying chromosome-arm wording.
- Reduced pedigree polish search work by skipping unions at their configured non-founder child
  cap and generations whose added child cannot improve row progression. Existing shuffle and
  random-draw order, difficulty checks, and acceptance gates remain; configured numeric limits
  are unchanged. On the 50 saved inputs, whole-call replay counts fell from 820 to 533 `Family`
  constructions and from 591 to 304 difficulty checks, including the unchanged final check.
  Timings did not establish a speed benefit.

### Behavior or Interface Changes

- WeBWorK replacement pairs now use the same literal, longest-match pass as Blackboard,
  replacing temporary-token substitution. Short aliases such as `stattest` remain supported,
  including at the end of a string. Deliberate short-word boundary guards remain where needed.
- Text replacement helpers now use one literal, longest-match pass over each source string;
  inserted markup is never matched again. The implementation spells out sorting, escaping,
  and match lookup. Updated the thermodynamics plural rule to match source text directly.
  Statement-question generation now formats stems and every choice once before constructing
  items, preventing repeated tagging across duplicate questions and final output formatting.
  Existing HTML is still eligible for matching; callers must supply each source field once.
- Added the user-selected 5% exact affected-count teaching filter to shared pedigree acceptance.
  Each sibship is tested conditional on offspring sexes; extreme candidates are rejected and
  generation continues randomly. Repair, polishing, and cache reuse share the gate. Four affected
  offspring from `Aa x Aa` are rejected; three of four remain eligible (tail 0.05078125).
  Cache records now preserve original genotypes, validate them against observations and inheritance,
  and skip legacy entries that cannot supply the original parental cross.
- Added the matched terminal-frontier interest review to
  [PEDIGREE_EVIDENCE.md](../problems/inheritance-problems/pedigrees/PEDIGREE_EVIDENCE.md).
  Two reviewers found no higher interest; their balance, readability, and usefulness judgments
  differed. The evidence preserves production policy and records the corrected-run limitation.

### Developer Tests and Notes

- Replacement audit: 80 focused tests passed; all matching and statement YAML files validated
  with zero errors and five existing warnings. Across 5,592 strings, Blackboard and WeBWorK
  replacement output matched exactly, with no nested color spans, partial-word matches, or
  closing-tag repair rules. All original palette placeholders were checked for preservation.
  The local WeBWorK renderer was unavailable on port 3000; browser rendering was not validated.
- Replacement and YAML-generator checks passed (48 tests). A one-time comparison of 3,438
  source strings across 81 rule-bearing YAML banks found no visible-text changes from the
  single-pass helper. Regression coverage checks plural precedence, literal keys and values,
  unmodified replacement output, item answer consistency, and statement-field formatting.
- The 5% pedigree filter passed the full suite (5,048 tests; two existing source-length warnings)
  and scoped `pyflakes`. Independent exhaustive enumeration agreed with the exact-tail helper for
  all 1,911 sibships in 200 fresh pedigrees across four difficulties; all met the cutoff and retained
  identical tails after cache round trips. The saved four-of-four case was rejected, and a bank with
  that case plus a legacy entry replenished successfully. All three CLI formats exported BBQ and
  HTML self-tests; question-text checks found no issues. Local evidence is under
  `output_pedigree/probability_filter_20261006/`.
- Audited the current pedigree generator with the existing probability tool: 200 fresh accepted
  cases had no impossible transmissions; four had whole-pedigree p < 0.05 and six had a sibship
  joint sex/phenotype p < 0.05. A separate 1,000-case medium autosomal-recessive probe reproduced
  one four-of-four affected carrier cross. Its joint p = 0.0146 exceeds 1% despite the affected-count
  tail being 1/256. Recorded an exact per-sibship phenotype-screen recommendation without changing
  generation policy; six diagnostic tests passed. See the
  [pedigree_offspring_probability_20261006.md](archive/audits/pedigree_offspring_probability_20261006.md).
- Focused pedigree tests passed (148); scoped `pyflakes` passed. All 50 saved inputs retained
  byte-identical results and ending RNG state. Whole-call replay work counts included the final
  endpoint check; paired timings varied without establishing a speed benefit.
