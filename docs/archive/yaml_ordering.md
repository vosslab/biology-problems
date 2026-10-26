# YAML ordering implementation plan

## Settled contract

- Add the ordering family alongside MATCH and TFMS, reusing the existing bptools loader,
  replacement helpers, formatters, collector, and exports.
- Use `topic`, optional `question override`, optional `replacement_rules`, and a `steps`
  mapping. Each `step N` maps to a list of equivalent alternatives; numeric rank defines order.
- Every step is required. The user's subsequent corrections remove YAML counts, CLI count
  flags, and subset/window selection. Shorter exercises require a separately authored bank.
- Use separate native and MC executables, following MATCH/WOMC, with shared `orderinglib.py`.
- Native ordering uses the selected prose/structures in correct order. MC shuffles their
  display labels and supplies four complete permutations, one correct.
- Generate MC alternatives from adjacent swaps and reversal; choose one wording per step
  and keep that choice consistent within the instance.
- Apply replacement rules once to each prose field, before assembling the question.

## Migration

- Migrate all six 16S steps, seven model-organism ranks, and eleven glycolysis structures.
- Reuse the molecule renderer and named-pathway identification clue.
- Replace the old generators and update website aliases, task inputs, output discovery,
  and corresponding title/Bloom metadata. Retain historical changelog records.
- Add the template and a short guide. Update the changelog and current references.
- Git and staging are outside scope except an actual file move requiring `git mv`.

## Verification

- Protect numeric rank, alternative selection, replacement integration, and complete MC
  permutations with focused tests. Reuse the existing YAML and replacement helper tests.
- Generate both formats from every bank, inspect keys, export native QTI, and render samples.
- Check website task loading and bank-specific output ownership.
- Run the advisory text checker and appropriate repository checks; record limitations honestly.

## Implementation evidence

Implemented with two executable wrappers and one shared helper. All counts and subset
selection were removed as requested. The website tasks retain their native/MC formats and
now use every authored item.

- Focused validation: 180 bank/helper tests and 9 website task-loading tests passed.
- Generated three instances per bank and format. The identical native glycolysis instances
  deduplicate to one item through the existing package reader; the renderer shuffles it.
- Six QTI 2.1 ZIPs passed manifest, archive integrity, and XML parsing checks.
- All six HTML previews opened in Chromium without script errors. Both glycolysis formats
  drew all eleven structures; the other four previews displayed their text and controls.
- Every question-text checker report had zero findings.
- Temporary samples, checker logs, QTI packages, and WebP previews are in
  `/private/tmp/ordering_review`. They are review artifacts, not published website content.

The visual review caught an unnecessary canvas-ID rewrite that also changed an RDKit method
name. It was removed. The shared molecule renderer is now used unchanged, and both previews
were regenerated and rechecked successfully.

### Sample key review

One rendered 16S instance displayed extraction (1), clustering/classification (2), sequencing
(3), abundance interpretation (4), collection (5), and PCR (6).

| Choice | Sequence | Independent review |
| --- | --- | --- |
| A | 4 -> 2 -> 3 -> 6 -> 1 -> 5 | Reversed workflow |
| B | 5 -> 6 -> 1 -> 3 -> 2 -> 4 | PCR before DNA extraction |
| C | 5 -> 1 -> 3 -> 6 -> 2 -> 4 | Sequencing before PCR |
| D | 5 -> 1 -> 6 -> 3 -> 2 -> 4 | Correct workflow |

The wrong sequences come from reversal and adjacent swaps in `sequence_choices()`.
Organism selections were checked against the original seven-rank ladder. Glycolysis retains
the original eleven molecular records and their name-to-structure clue. The focused tests
independently reconstruct the MC key from displayed labels and the authored sequence.

### Full-suite limits

The full biology-problems suite completed with 5705 passes and five failures:

- `test_file_discovery_deletions.py`: its synthetic deleted-file filter raises FileNotFoundError.
- Three Markdown-link cases: unrelated retired chi-square and progeny-probability paths in
  the January changelog, genetics HTML audit, and usage guide.
- The genetics Topic 07 candidate document exceeds the existing source-file line limit.

These failures do not involve ordering files. No LMS import or website publication was performed.
