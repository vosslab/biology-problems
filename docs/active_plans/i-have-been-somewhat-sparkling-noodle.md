# Plan: student-facing question best practices for the bptools and webwork writer skills

## Context

Questions written through `bptools-writer-expert` have fine Python but student-facing text
that needs rework. Root cause, confirmed by reading every skill file: the skill has zero
guidance on student-facing text. SKILL.md and its 8 references cover structure, argparse, BBQ
format, anti-cheat flags, and a `--seed 12345` byte-identical proof that `bptools.py` cannot
produce (no seed flag exists; the repo prefers true randomness). `problems/TEMPLATE.py`, the
file agents copy first, has the stem `"This is a hard question?"` and leaves a second
correct-looking term in the choice pool.

Outcome: canonical, evidence-built guidance for student-facing question text in
`biology-problems/docs/`, bundled into `bptools-writer-expert` and `webwork-writer-expert`,
used as a design-first step and an automated plus agent-judged review step, and shown by a
blind old-vs-new experiment to reduce the corrections Neil has historically made by hand.
The whole plan runs with a manager and subagents only; no step waits on a human.

## Decision hierarchy (one rule for authors)

1. Neil's stated guidance wins: `docs/HUMAN_GUIDANCE.md` plus statements in this session.
2. Published item-writing standards: Haladyna, Downing, and Rodriguez (2002); NBME Item-Writing
   Guide (cover-the-options, testwiseness cues, homogeneous options).
3. Patterns from Neil's best work (real exams, 2018-2022 generators) as the course layer.
4. Corrections drawn from flaws found in any corpus. Judge text, not provenance: many 2026
   items carry Neil's ideas (for example ordering model organisms by complexity: flies have
   legs, eyes, and a brain; worms do not).

Known conflict resolved by rule 1: Neil loves seriously absurd choices; the literature asks for
plausible distractors. Absurd choices are available as course voice; each item keeps enough
meaningful alternatives to assess the intended reasoning. No quota in either direction.

## Core principle: puzzle first, few words

Neil: "I am not a writer. I hate writing. I am a thinking and problem/puzzle solver with
strong math mind." The guides lead with this:
- A question is a puzzle. Design the data, constraints, answer, and computed wrong answers
  first; the prose is the thinnest wrapper that makes the puzzle unambiguous.
- Every sentence supplies data, scope, or the question.
- Agents own mechanical polish (spelling, grammar, units, spacing) and add no extra prose.

This explains the strengths in his corpus (computed distractors, show-the-setup choices,
self-checking word answers, data-first figures) and the weaknesses (typos, occasional
tool-polished filler).

## Evidence summary

Literature and books (cited per rule, collected in a References section of the pedagogy guide
so they serve a future manuscript on the bptools corpus):
- Papers: Haladyna, Downing, and Rodriguez (2002) Applied Measurement in Education 15(3);
  NBME Item-Writing Guide; arXiv 2602.18891 (LLM MCQs strong on grammar, weak on cognitive
  depth and difficulty calibration). Step 1 adds verified citations for option count
  (Rodriguez 2005 meta-analysis), item-writing flaws, and distractor generation.
- `~/nsh/MARKDOWN_BOOKS/` (local, not committed; cite by bare path plus grep term):
  `assessment_taxonomy/A_Taxonomy_for_Learning_Teaching_and_Assessing_a_Revision_of_Bloom_s_Taxonomy_of-2001.md`
  (cognitive-process scale for the reasoning target; grep `distractor`, 16 hits);
  `learning_design/Design_for_How_People_Learn-2015.md` (practice and scenario design, 15 hits);
  `learning_design/Gamification_of_Learning_and_Instruction-2012.md` and its 2013 fieldbook
  (puzzle and game mechanics); `testbanks/Lehninger_Principles_of_Biochemistry_Testbank-2005.md`
  (commercial testbank contrast corpus); `mcat/AAMC_MCAT_Practice_Test_*` (passage-based item
  sets). Gap: no item-writing handbook in the corpus.

Full quotes go into the audit doc (execution step 1). Sources: Neil's exams
(`~/nsh/PROBLEMS/exam-formatting-tools/ARTIFACTS/`, verbatim quotes approved); pre-agent
generator text from git `c3cb2d0` (2025-11-19) and older commits; 2026 generators and banks;
changelog and git history of Neil's 2026 corrections; the three research reports from this
session (Neil-era generators, 2026 generators, YAML banks).

Course voice and pedagogy to teach:
- Data or scenario first, then one short lead-in: "Which one of the following ...", "What
  fraction of their sons ...", "Based on the lanes in the RFLP gel above, who is the father of
  the child?" ("Which one of" in 148 rendered sets; "best describes" in 2.)
- Rule sentence, case sentence, short question. Figure pointers ("table (above)").
- Emphasis only on the discriminating word (woman/man, linear/circular) and on NOT, EXCEPT,
  TRUE, FALSE. Hints resolve ambiguity ("Hint: the first gene on the end is gene C.").
- Distractors computed from named errors; choices often show the setup
  ("(493+476+29+22)/6000 = 17.0 m.u."); arithmetic handed over so the concept is graded.
- Fixed ladders ("None, 0% / 1/4, 25% / ... / All, 100%"); natural choice order.
- Shared-figure item sets and multi-part family stories; difficulty scales by data.
- Misconception placement by design (non-selected enzyme on the 0 kb mark).
- Puzzles and self-checking answers (deletion order spells a word); deliberate red herrings.
- Seriously absurd choices, deadpan and form-matched ("named for famous scientist Chandler
  Wobble", "NEITHER linked NOR unlinked"); mnemonic invented names ("bumpy, waxy, yucky" for
  b, w, y; fantasy taxa); fictional worlds ("On planet Zygora, the glowstem plant ...").
- Statement banks: lowercase fragments finishing "Which one of the following statements is
  TRUE regarding <topic>?"; false versions by one-term swap with every permutation listed;
  true-but-out-of-scope facts; numbers bracketing the true range; about 2 false per true;
  absolute words appear in true statements too.
- Matching: exact letter-use instruction ("Letters will be used exactly once."); applied
  pairings (cross -> progeny, scenario -> category).
- Numbers spelled with digits ("two (2)"); FIB entry rules with a worked example.

Patterns to correct (any author):
- Hedge/absolute asymmetry between true and false statements; "because" clause on the key
  only; key is the longest or only non-parallel choice; answer-revealing parentheticals.
- Matching values that echo key words or carry giveaway dates; slide-heading keys.
- Encyclopedic preambles, meta-commentary ("The table shows what happens ..."), definitions
  and symbols stated twice, caveats and citations in the stem, solution-path hints.
- "Not enough information" escapes that are never or ambiguously the key.
- Cosmetic variation (same key under reworded stems); tiny scenario spaces.
- Decoration (row fills, captions, legends); typos, unit mismatches, template grammar slips.
- Allele letters that do not match invented names (C -> "Doubled"/"Zippy").

Neil's 2026 correction log, pre-registered as experiment categories (from changelog and
commits `bd221d8`, `208524c`, `61101b0` on `lethal_allele_survival.py`,
`monohybrid_litter_inference.py`, `epistasis_test_cross.py`):
- C1 What is counted is explicit ("Before considering survival, assume the cross produces N").
- C2 No redundant instruction, label, legend, or meta-commentary.
- C3 Numbers chosen for whole-number arithmetic (offspring totals multiples of 12).
- C4 Misconception pair present (both 1/3 and 2/3 for lethal alleles).
- C5 Natural choice order (ascending; homozygous dominant, heterozygous, recessive).
- C6 Choices carry mechanism or type labels ("Hh (heterozygous)", mechanism then term).
- C7 Context consistency ("wildtype" label; no "litter" for plants or people).
- C8 Data first; meaning survives without color (labels, counts, shapes).
- C9 No ambiguous-information escape choice.

## Rubric, routed by item type

Universal (every item, both skills):
- U1 Data or scenario first; one lead-in; every sentence supplies data, scope, or the question.
- U2 Emphasis only on discriminators and negations.
- U3 What is counted is explicit; numbers give whole-number arithmetic where intended.
- U4 Nothing said twice; no preamble, meta-commentary, caveat, or citation in the stem.
- U5 Sampled items differ in data or scenario, not only in wording or order.
- U6 Names deliberate (real, or mnemonic and letter-matched); emoji only as a labeled icon,
  ASCII-escaped in source.
- U7 Mechanics clean: spelling, spacing, units match between stem and answer, "X-linked",
  5'-3' sequences in monospace, HTML entities.
- U8 Difficulty from data; hints only resolve ambiguity.
- U9 Answer key verified independently by a method that fits the item type: enumeration or a
  second implementation for computed items; a separate agent check against source data for
  recall, matching, and statement items.

By type (PGML equivalents in parentheses):
- MC and MA (RadioButtons, CheckboxList): M1 cover-the-options; M2 each distractor tagged with
  its error or as "absurd", enough error-derived ones to discriminate; M3 homogeneous options in
  natural order; M4 no testwise cues (length, hedge asymmetry, key-word echo, grammar
  mismatch); M5 "cannot be determined" only when sometimes the key and unambiguous.
- Statement banks: S1 lowercase fragments that finish the stem; S2 one-term swaps; S3 hedge and
  absolute words balanced across true and false; S4 false pool larger than true pool.
- Matching (PopUp matching): T1 exact letter-use instruction; T2 values echo no key words or
  dates; T3 values parallel, one idea each.
- FIB and NUM (answer blanks, numeric answers): F1 entry rules with a worked example; F2 units
  and rounding stated; F3 tolerance matches the arithmetic.
- Ordering (draggable lists, ORD): O1 one unambiguous ordering criterion stated; O2 consistent
  item format (for example binomial plus common name throughout).

Automated where mechanical: a checker script (deliverable A) covers M4, S3, T2, and the
mechanical parts of U4 and U7. Agent judges cover the rest.

## Deliverables

### A. biology-problems

- `docs/active_plans/audits/question_voice_audit.md`: full evidence with verbatim quotes.
- `docs/QUESTION_PEDAGOGY_GUIDE.md`: puzzle-first design workflow (reasoning target, error list,
  computed distractors, absurd choices as voice, show-the-setup choices, data-first and
  shared-figure sets, stories, misconception placement, difficulty by data, red herrings,
  self-checking answers, statement-bank construction), the routed rubric, and a References
  section (verified papers plus book paths and grep terms). Up to 1000 lines per doc
  (`test_source_file_line_limit`).
- `docs/QUESTION_VOICE_GUIDE.md`: stem anatomy, lead-ins, emphasis, hints, choice layout and
  ladders, matching and FIB instructions, statement-bank form, numbers, formatting.
- `docs/QUESTION_EXEMPLARS.md`: verbatim exemplars labeled "model" or "fix" (never by author),
  each citing its rule by heading; one distractor recipe per family (error -> code -> choice);
  Neil-era generator quotes from git `c3cb2d0` or the named older commit.
- `devel/check_question_text.py`: reads a BBQ file and reports testwise cues (longest-key rate,
  hedge/absolute asymmetry, key-word echo, "a" before a vowel sound, doubled or missing spaces,
  stem-vs-choice unit mismatch, generic lead-ins). Advisory report, exit 0. Focused tests in
  `tests/test_check_question_text.py` with small inline BBQ fixtures.
- `problems/TEMPLATE.py`: same structure; content becomes a small real example with a
  data-first stem, "Which one of the following ..." lead-in, error-derived distractors each
  commented with its error, one deadpan absurd choice commented as optional voice, natural
  choice order, and a docstring pointer to the guides.
- `AGENTS.md`: one bullet under Style and workflow pointing student-facing text to the guides.
- `docs/QUESTION_AUTHORING_GUIDE.md`: short "Student-facing text" section linking the guides;
  replace the `"wrong 1"` skeleton with an error-derived example.
- `problems/multiple_choice_statements/MC_STATEMENTS_AUTHORING_GUIDE.md` and
  `problems/matching_sets/MATCHING_SET_AUTHORING_GUIDE.md`: keep mechanics; replace rule prose
  that conflicts (1:1 counts, "clearly wrong" as the easy mode) with links to the canonical
  rule headings.
- `docs/DESIGN_DECISIONS.md`: "Question-writing guides are canonical in biology-problems; writer
  skills bundle snapshots" (Owner: `docs/QUESTION_PEDAGOGY_GUIDE.md`).
- `docs/HUMAN_GUIDANCE.md`: five bullets in Neil's words: (1) student-facing voice, style, and
  pedagogy need as much care as the Python, which is already fine; (2) my content is not
  perfect either; we are developing best practices, not copying my old questions; (3) I love
  seriously absurd choices; (4) do not assume everything is AI; ideas such as ordering model
  organisms by complexity are mine; (5) I am a thinker and puzzle solver, not a writer;
  questions should be puzzles with few words.
- `docs/CHANGELOG.md` entry.

### B. bptools-writer-expert (vosslab-skills)

- `SKILL.md`, gated by `tests/test_skill_body_size.py` (150 lines, 8,000 characters) and the
  250-character description ceiling: Required reading adds the pedagogy and voice guides for any
  student-facing text; Workflow adds "Design the puzzle before code" and "Student-text review"
  (checker script, independent answer-key check, routed rubric); trim the duplicated Reference
  files list to make room; description adds student-facing wording and distractor design.
- New `references/question_voice.md`: routing list plus rubric item names. Reference files may
  run up to the repo's 1000-line source limit; only SKILL.md stays small.
- `references/testing_and_oracles.md`: replace the seed-reproducibility artifact with the
  student-text oracles; keep BBQ validity checks.
- `references/project_workflow.md`: authoring contract gains reasoning target, error list, and
  chosen exemplar; existing-repo path adds a text audit.
- `references/task_selection.md`: add item-type and reasoning-target dimensions (reasoning target
  named on the revised Bloom cognitive-process scale: apply, analyze, evaluate); align
  randomization with the repo's true-randomness rule.
- `references/topic_index.md`, `references/docs.md`: route wording, distractor, review, and bank
  requests to the guides.
- `references/docs/`: byte-identical snapshots of the three guides; refresh the MC-statement and
  matching guide snapshots.

### C. webwork-writer-expert (vosslab-skills)

- Same three snapshots; SKILL.md Required-reading pointer and Workflow line (same gates).
- `references/topic_index.md`, `references/docs.md`: route by PGML item type to the rubric; the
  guides decide what to emphasize and `QUESTION_STATEMENT_EMPHASIS.md` decides how to render it.
- `references/testing_and_oracles.md`: routed rubric as an oracle.

### D. vosslab-skills bookkeeping

- `docs/CHANGELOG.md`; run `index_lib/build_all.py` because both descriptions change.

## Source of truth and duplication (KISS)

- Each rule lives once: design and review rules in the pedagogy guide, wording and format rules
  in the voice guide; exemplars cite headings. Other docs and skill references link.
- Checked: vosslab-skills has no snapshot-drift test and no sync script. Decision: no new
  permanent gate. Each canonical guide carries a header naming its snapshot paths, and the
  implementation verifies byte identity with `cmp` before finishing.

## Validation (manager and subagents only)

V1 Automated gates:
- vosslab-skills: `test_skill_frontmatter`, `test_skill_body_size`, `test_skill_internal_links`,
  `test_ascii_compliance`, `test_markdown_links`, `test_expert_skill_parity`,
  `test_skills_index_in_sync`, `test_plugin_manifest_drift`.
- biology-problems: `test_markdown_links`, `test_ascii_compliance`,
  `test_source_file_line_limit`, `test_pyflakes_code_lint`, `test_check_question_text`;
  `problems/TEMPLATE.py -d 3` runs; checker runs clean on the TEMPLATE output.

V2 Replay experiment, contamination-free:
- Record base commits at step 0 (all implementation edits stay uncommitted, so base = pre-change).
- Build two sandboxes in the scratchpad with `git archive <base>`: control and treatment. In
  both, delete `lethal_allele_survival.py`, `monohybrid_litter_inference.py`, their tests, and
  `docs/CHANGELOG*.md` (which narrate Neil's fixes). The treatment copies of the guides hold out
  exemplar lines specific to lethal alleles and monohybrid inference, and TEMPLATE.py uses an
  unrelated puzzle (dilution), so R1/R2 test the general rules; the report labels R1/R2
  in-sample (rules drew on their history) and R3 out-of-sample. Control keeps the old docs, TEMPLATE, and a
  `git archive` copy of the old skill; treatment receives the new guides, TEMPLATE, authoring
  guides, and the edited skill.
- Requests: the original requests for both generators, reconstructed from the 2026-01-04
  changelog entries and commit `566b690`, plus one new request (two-allele incomplete-dominance
  probability). The report marks each request sentence as recovered (quoted from a commit or
  changelog) or inferred. Each arm reads its own skill files by path.
- Two replicates per arm per request, each a fresh subagent; each writes the generator in its
  sandbox and renders `-d 5` BBQ output.

V3 Blind scoring:
- Manager strips arm labels and shuffles outputs. Three fresh judge subagents score every output
  against C1-C9 and the routed rubric, pass or fail per item with a quoted line as evidence.
  The checker script runs on every output. A fresh verifier subagent checks every answer key by
  independent enumeration.
- Majority vote per item. Result table: categories satisfied per arm per request.
- Success: across all requests combined, treatment satisfies more pre-registered categories than
  control, with no wrong keys; per-request results are reported separately. Checker findings
  stay advisory: each one sends the item to judge review rather than failing it. Otherwise
  revise the guides for the failing categories and rerun (up to two loops); if still short,
  record the outcome under Decisions and Failures and finish.

V4 WebWork check: a fresh subagent with the treatment webwork skill writes the
incomplete-dominance item as PGML; lint (and render when the local renderer responds); one
judge scores it with the PGML-routed rubric.

V5 Review-pass dry run: the treatment review step on current rendered output of
`x_linked_reciprocal_cross.py` and `horse_coat_pattern_inference.py`; a judge confirms it flags
the pre-listed defects (tiny scenario space, "best describes", stem length, solution-path hint).
No generator edits.

Report: `docs/active_plans/reports/question_voice_skill_eval.md` with tables and quotes.

## Execution order (parallel where independent)

0. Record base commits for both repos; build the control sandbox.
1. Write the audit doc. In parallel, a research subagent verifies each citation (WebSearch),
   adds the option-count, item-flaw, and distractor-generation papers, and greps the books for
   supporting passages (path, grep term, short quote).
2. Write the exemplars, then the pedagogy and voice guides in parallel; an independent reviewer
   subagent checks hierarchy, single-home rules, positive phrasing, and ASCII; apply fixes.
3. In parallel: supporting biology-problems edits; checker script and tests.
4. In parallel: bptools skill edits; webwork skill edits; snapshots; `build_all.py`.
5. V1 gates; fix failures.
6. Treatment sandbox; V2-V5; revision loops; write the report and both changelogs.

## Current implementation status

- Completed: the canonical pedagogy, voice, exemplar, and evidence documents; the advisory
  checker and its focused tests; supporting biology-problems documentation; both writer-skill
  workflows, routing references, and bundled snapshots; and both changelog entries. The template
  correction has a richer named-error pool sampled before natural sorting and passed final review.
- V1 complete: the biology-problems full suite passed 4,993 tests (with two existing source-size
  advisory warnings), and all specified vosslab-skills V1 gates passed 1,291 tests.
- Deviation recorded: `QUESTION_EVIDENCE.md` is the canonical audit and evidence record. It
  replaces the planned duplicate `docs/active_plans/audits/question_voice_audit.md`, preserving
  one durable source for the corpus, correction log, research, and book evidence.
- This plan intentionally remains at its existing root-level path. It was already untracked, so
  the required `git mv` archive operation would first alter the index. To preserve the existing
  index and staging state, this practical deviation retains the requested path; the active-plan
  rule also preserves existing root-level files until an explicitly approved sweep.
- Evaluation complete: the corrected loop-one blind sample scored
  control 185/200 (92.5%) and treatment 192/200 (96.0%): R1 60/60 versus 52/60, R2 60/70 versus
  70/70, and R3 65/70 versus 70/70. All 120 independently checked keys across both rounds are
  correct; V4 runtime and V5 dry-run checks are complete. The initial literal replay tie at
  189/200 remains valid. A first loop-one set-level summary (41/44) and provisional 95%/92.5%
  comparison were corrected before review; the independent final review accepted the per-item
  192/200 versus 185/200 result. No second guide loop is required.

## Completion

- Complete. This plan remains at its requested root-level path for the index-preservation reason
  recorded above; no index or staging state was changed to archive an untracked file.

## Separate follow-up (found during research, outside this plan's outcome)

Listed in the report for later dispatch: wrong "daughters" key in `x_linked_tortoiseshell.py`
(`make_cross()` picks `"daughters"` at line 76, `fraction_matching()` filters on `"female"` at
line 63) and "a orange male"; uL/mL mismatch in `serial_dilution_factor_mc.py`; typos in
pre-2025 banks; grammar slips in 2026 generators; text rewrites of `x_linked_reciprocal_cross.py`,
`x_linked_tortoiseshell.py`, `horse_coat_pattern_inference.py`.
