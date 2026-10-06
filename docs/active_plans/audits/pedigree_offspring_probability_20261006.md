# Pedigree offspring probability audit

Audited local HEAD `3b2849e` on 2026-10-06, starting with a clean working tree.
The current generator accepts `Aa x Aa` families with four affected offspring. This is valid
Mendelian sampling, but the existing probability diagnostic does not control classroom acceptance.
Generation code and acceptance policy were unchanged during this audit. In the follow-up, the user
selected a 5% exact affected-count cutoff; the production policy is documented in
[PEDIGREE_PROBABILITY.md](../../../problems/inheritance-problems/pedigrees/PEDIGREE_PROBABILITY.md).

## Reproduced outcome

A targeted run produced 1,000 accepted medium autosomal-recessive candidates using
`scenarios.generate_pool(random.Random(461006), 'medium', count=1000,
modes=('autosomal recessive',))`. Among 353 four-child carrier-by-carrier crosses, one had four
affected children: zero-based candidate 982, parents `p1` and `p2`, children `p4,p3,p6,p5`.
Both sexes occurred twice. All transmissions were possible.

The existing diagnostic, with 9,999 simulations and seed 461988, gave:

- Sibship Pearson statistic: 12.
- Sibship joint sex-and-phenotype p-value: 0.0146.
- Whole-pedigree p-value: 0.0142.

The probability of four affected offspring from this cross, ignoring sex, is
`(1/4)^4 = 1/256 = 0.00390625`. This is also the exact affected-count Pearson upper-tail
probability for this example. The existing diagnostic tests four sex/phenotype categories,
so its p-value answers a different question. A standalone two-boy/two-girl reproduction with
999,999 simulations and seed 20261006 gave joint p = 0.015579. A 1% threshold on the existing
joint diagnostic would therefore still allow this example.

## Mixed-mode audit

Generated 50 accepted candidates per difficulty with seeds 20261006 through 20261009.
Used the production identification pool, including repair/polishing and the bonus terminal-frontier
constructor. Retained original genotypes; no cache witnesses were substituted. Each diagnostic
used 9,999 simulations and seed `70000 + 100 * level_index + candidate_index`.

| Difficulty | Cases | Whole-pedigree p < 0.05 | Any sibship joint p < 0.05 |
| --- | --- | --- | --- |
| Easy | 50 | 1 | 0 |
| Medium | 50 | 2 | 1 |
| Rigorous | 50 | 0 | 2 |
| Bonus | 50 | 1 | 2 |
| Total | 200 | 4 | 6 |

No case had an impossible transmission, whole-pedigree p < 0.01, or sibship joint p < 0.01.
An exploratory exact affected-count tail, holding offspring sexes fixed, flagged one rigorous
case below 0.05 and none below 0.01. These are selected teaching candidates, not an unconditioned
random sample; percentages are descriptive and do not calibrate a population-level test.
The sample covers accepted pools before final ranking/export and does not establish rates among
exported questions or attribute outcomes to polishing.

## Initial recommendation

Keep Mendelian sampling and screen extreme affected/unaffected ratios within each sibship,
using an exact tail rather than an asymptotic chi-square approximation. A 1% threshold would reject
the reported four-of-four outcome and retain three-of-four (`p = 13/256 = 0.05078125`).
This is a classroom selection policy, not a claim that rejected pedigrees are biologically invalid.
Random resampling preserves variation without forcing textbook ratios or cycling through patterns.

For sex-linked modes, condition on observed offspring sexes when calculating phenotype expectations.
Keep this separate from the existing joint diagnostic and visible-evidence answer inference.
Any implementation must also cover post-polish acceptance and cache reuse; compact dominant-mode
cache records recover compatible witnesses rather than original sampled genotypes, so they cannot
silently be treated as original-cross diagnostic inputs.

## Reproduction artifacts

Follow-up verification of the user-selected 5% filter passed the full suite (5,048 tests).
Independent enumeration matched every exact tail in 200 fresh cases (1,911 sibships); all tails
were at least 0.05 and unchanged by cache round trips. The saved offending case was rejected and
cache replenishment succeeded. Post-change inputs, diagnostics, summaries, and the verification
script are under `output_pedigree/probability_filter_20261006/`.

Local ignored artifacts are under `output_pedigree/probability_audit_20261006/` at the repository
root: `audit.py`, `summarize.py`, original inputs and diagnostic results for the 200 cases,
`targeted_extremes.json`, the standalone four-affected input/result, and `summary.json`.
Scripts record the exact generation and diagnostic seeds. SHA-256 hashes are in `SHA256SUMS`.

The diagnostic's six existing focused tests passed:

```bash
source source_me.sh && python3 -m pytest tests/libs/pedigrees/test_offspring_probability.py -q
```

The diagnostic contract is in
[PEDIGREE_PROBABILITY.md](../../../problems/inheritance-problems/pedigrees/PEDIGREE_PROBABILITY.md).
