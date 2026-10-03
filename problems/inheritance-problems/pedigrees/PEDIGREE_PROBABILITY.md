# Offspring probability diagnostic

`pedigree_lib.offspring_probability.diagnose(family, mode, genotypes, rng)` is a diagnostic for
fixed parental crosses. It does not reject or rank candidates. The source pedigree workflow and
selection limits are described in [PEDIGREE_PIPELINE.md](PEDIGREE_PIPELINE.md); polishing behavior
is in [PEDIGREE_POLISHING.md](PEDIGREE_POLISHING.md).

## Reference calculation

The diagnostic uses original sampled genotypes and shared `inheritance.transmissions()` for
autosomal dominant/recessive, X-linked dominant/recessive, and Y-linked inheritance. Each offspring
sex is equally likely. Categories are male unaffected, male affected, female unaffected, and female
affected. Repeated gamete outcomes retain their Mendelian multiplicities. Each union is analyzed
against its own parental cross; founders are not scored as offspring.

It sums Pearson statistics across sibships and compares the total with simulated sets of independent
sibships while holding each observed parental cross and sibship size fixed. The default uses 9,999
simulation sets and reports `(exceedances + 1) / (simulations + 1)`, including ties. This avoids an
asymptotic chi-square approximation for small sibships. The default Monte Carlo resolution is
0.0001; estimates near 0.05 have about 0.0022 standard error. Impossible transmissions produce
`p=0` and a null statistic. Zero-probability categories otherwise contribute nothing. Results
include per-sibship observed and expected counts, statistic, unadjusted p-value, and impossible
children. The worst sibship is the one with the smallest p-value, not necessarily the largest
statistic; its p-value is not adjusted for searching multiple sibships.

## Input and use

Original genotypes are required. Compact cache records reconstruct compatible witnesses and cannot
substitute for original sampled states. The CLI accepts JSON with allele 1 denoting the trait allele:

```json
{
  "mode": "autosomal recessive",
  "people": [
    {"id": "father", "sex": "male", "genotype": [0, 1]},
    {"id": "mother", "sex": "female", "genotype": [0, 1]},
    {"id": "child", "sex": "female", "genotype": [1, 1]}
  ],
  "unions": [{"father": "father", "mother": "mother", "children": ["child"]}]
}
```

From the repository root:

```bash
source source_me.sh && python3 tools/pedigree_probability.py -i pedigree.json
```

Use `-s/--seed` for reproducibility and `-n/--simulations` for a different Monte Carlo count.
Results are JSON on stdout. Y-linked females have genotype `[]`; X-linked and Y-linked males have
one allele; diploid tuples are sorted.

## Interpretation limits

This is a fixed-cross reference diagnostic, not the probability a pedigree is honest or the
probability of the exact displayed outcome. In multigeneration families, offspring can later be
parents; independent reference draws do not propagate their newly drawn genotypes downstream.
Sex assignment, teaching filters, phenotype selection, and ranking condition generated samples.
Even unpolished accepted cases need not have uniform p-values. Compare paired unpolished/polished
distributions before attributing a shift to polishing. The diagnostic does not affect acceptance or
ranking.

Two historical comparisons illustrate the selection limits. The preserved report for 1,000 paired
rigorous cases recorded p < 0.05 in 31 cases before and 33 after polishing, and recorded p < 0.01
in 9/9 cases; no impossible transmissions occurred. In a separate 80-case held-out local-search
experiment, 18/80
Pareto-selected pedigrees and 2/80 originals had fixed-cross p < 0.05; every recorded transmission
was valid. That difference is consistent with candidate selection enriching low-p cases. It does
not show impossible biology or prove that polishing alone caused the pattern. Both results are
experimental, not production acceptance evidence. The full caveats and report locations are in
[docs/CHANGELOG.md](../../../docs/CHANGELOG.md#2026-10-02) and the sibling
`pedigree-aesthetics` workspace.
