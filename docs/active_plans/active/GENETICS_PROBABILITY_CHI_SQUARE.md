# Genetics probability and chi-square question banks

Status: implemented. The instructor narrowed final validation to working generators,
generated HTML, and task-file registration; BPW integration and download validation
are not completion requirements. See the
[review record](../reports/GENETICS_PROBABILITY_CHI_SQUARE_REVIEW.md).

## Goal and context

Implement the instructor-approved progression from concepts and visible outcomes to
manageable calculations and interpretation. Use lectures 07B, 07C, and 07D, the
chi-square worksheet, and the supplied Bozeman subtitles. The audience is Genetics
students; use MC, MA, and Matching for quizzes alongside existing MULTI-FIB work.
Follow the bptools-writer-expert skill and the live question voice, pedagogy, and
exemplar guides. External LLM feedback informs quality review, not human approval.

## Approach

1. Move the existing probability bank unchanged from BPW Genetics chapter 6 to 7.
   Preserve its filename and generator, update its CSV assignment, and regenerate
   affected catalogs, topic pages, navigation, and self-test metadata. Expand the
   chapter description to include probability without changing its URL or alias.
2. Add four probability modes: independence (MC), visible outcomes (MA), supplied
   probability tables (Matching), and small-family calculations (MC). Use two to
   four offspring, start with equal probabilities, then include Mendelian quarters.
   Supply sequence probabilities or intermediate arithmetic for unequal cases.
   Include surviving-offspring thirds only with an explicit denominator and supplied
   table. Keep factorial-heavy work in the existing advanced bank.
3. Shorten lab-partner hypotheses and choices, remove the reused eye-roll opener,
   and ask neutrally what should change, if anything. Retain swapped hypotheses,
   exact-observation claims, wrong ratios, and correct hypotheses as cases.
4. Replace the Genetics paired-hypothesis bank with separate null and alternative
   MC banks using existing kind flags. Choices state predictions, not conclusions;
   wrong choices use opposite hypotheses and specific misconceptions. Preserve the
   pair mode and default for the Biostatistics consumer.
5. Add six dice modes: expected counts (MC), degrees of freedom (MC), completing
   one calculation (MC), interpreting results (MC), evaluating conclusions (MA),
   and connecting quantities to values (Matching). Use six faces, five degrees of
   freedom, totals divisible by six, and expected counts of at least five. Supply
   critical values at alpha = 0.05, cover both decisions, and avoid rounding-boundary
   cases. Recompute the video's numbers; do not copy its rounded statistic or its
   claim that not rejecting proves fairness.

## File scope and interfaces

- New generators: `problems/inheritance-problems/progeny_probability_practice.py`
   and `problems/inheritance-problems/chi_square/chi_square_dice.py`. Fixed formats
   per `-k/--kind`, standard bptools collection/export flags, kind/type filenames.
- Edit the two existing chi-square hypothesis generators. Reuse bptools MC/MA/MAT
   and existing chi-square helpers. Keep scenario selection truly random and numeric
   choices in natural order; shuffle choices without a meaningful order.
- In the sibling BPW repository, update task CSV, title metadata, topic description,
   and affected generated outputs. Document changes in both changelogs.
- Save authoring and review evidence beside this plan under the reports directory.
   No remote publication, renderer changes, or unrelated bank regeneration.

## Authoring contract

Use the exemplars "Lab scenario in second person", "Rule, case, question", and
"Note that hands over arithmetic". Probability items apply independence, enumerate
outcomes, or combine disjoint orders. Errors include gambler's fallacy, omitted
orders, exactly versus at least, and treating unequal outcomes as equally likely.
Dice items apply expected counts and df, finish a term or sum, and evaluate a
decision. Errors include dividing by df, counting rolls as categories, omitting
the square, reversing a comparison, and claiming proof from a test. Hypothesis
items distinguish a prediction from the observed sample and from a test conclusion.
Matching pairs must have distinct values. Tables carry the data; prose names the task.

## Completion checks

- Independently enumerate probability outcomes and recompute dice statistics and
   keys. Check each response format, hypothesis case, and both test decisions.
- Review actual stems, choices, and any explanations against lectures and named
   exemplars. Specialized vocabulary must earn its place. Match choice length,
   grammar, formatting, vocabulary, and difficulty; keep hypotheses and conclusions
   separate. Mathematical correctness and teaching language are equally important.
- Collect before/after samples, distractor rationales, independent key evidence,
   and advisory text-checker dispositions. Obtain a separate reader for statement
   and matching keys, as required by the authoring skill.
- Inspect generated HTML and verify each generator mode runs successfully. Register
  the modes in the website task file. Per the instructor's scope correction, BPW
  integration, package downloads, and LMS import are not required validation.
- Verify the moved bank is byte-identical and the old Genetics pair bank is gone.
   Run focused and full repository checks without automatic whitespace rewriting.
   Keep durable tests only for meaningful mathematical/grading behavior; remove
   one-time verification scripts before closeout.
