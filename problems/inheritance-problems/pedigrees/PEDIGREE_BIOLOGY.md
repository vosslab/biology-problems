# Pedigree biology and teaching

This page owns the biological model and visible-evidence acceptance. Procedural structure and
workload live in [PEDIGREE_DIFFICULTY.md](PEDIGREE_DIFFICULTY.md). YAML authoring rules are in
[PEDIGREE_AUTHORING.md](PEDIGREE_AUTHORING.md).

## Family and genotype model

`Union.children` is the only parentage authority. People have stable string IDs, sex, and optional
labels. Generations are derived from parentage and partner relationships; drawing coordinates are
never authored. Validation rejects missing references, duplicate IDs or parentage, ancestry cycles,
incompatible generations, and multiple reproductive unions per person. Founders, marrying-in
spouses, and cousin unions use the same relationship model. Each union has one male father and one
female mother.

Genotypes are separate from observations. Allele `0` is ordinary and `1` is the trait allele.
Autosomal and female X-linked genotypes have two alleles; male X/Y genotypes have one; females have
no Y genotype. A carrier marking identifies a known unaffected heterozygote. Unmarked unaffected
people may still be carriers. Hiding carrier status changes no genotype.

Simulation samples actual gametes, retaining their Mendelian multiplicities. Compatibility analysis
uses the same transmissions with genotype-domain propagation and backtracking across every union
and founding family. It assumes complete penetrance and no new mutations. By default,
`inheritance.analyze` does not constrain unrelated spouses; its `noncarrier_ids` option can constrain
selected people. Homework assessment applies this to unaffected spouses entering in generation II
or later under each tested mode. Any generation-I person may carry the trait allele and descendants
may inherit it. Descendants of another founder family are not unrelated outsiders.

Autosomal recessive generation seeds generation-I founders as carriers. A generation-I founder who
married into a later-generation union is sampled as 90% homozygous unaffected or 10% affected, never
heterozygous. X-linked recessive allows carrier seeding only in generation I; descendants inherit
normally. These are teaching-example sampling weights, not population frequencies or promised
percentages among accepted output.

An affected father and son do not alone exclude X-linked inheritance: the son can receive the allele
from his mother. Two affected recessive parents cannot have unaffected children. Affected-by-carrier
crosses use the transmission model rather than phenotype shortcuts.

## Visible teaching profiles

The profiles encode multi-clue lecture reasoning. They are selective classroom criteria, not
inheritance laws or statistical likelihoods. A question asks which pattern is *most likely* under a
rare-trait assumption. A case must have exactly one supported teaching profile among modes that are
biologically compatible; alternatives can remain biologically possible. Sex counts alone never
establish an answer or resolve a tie.

| Mode | Required visible evidence |
| --- | --- |
| Autosomal dominant | Affected lineage across three generations; both sexes affected; an affected father has an unaffected daughter; no affected child of two unaffected parents |
| Autosomal recessive | Unaffected parents have affected offspring, plus both sexes affected or related parents of an affected child |
| X-linked dominant | Affected father with affected daughters and unaffected sons from an unaffected mother, plus an affected mother with affected sons and unaffected offspring |
| X-linked recessive | Affected grandfather, unaffected connecting daughter, affected grandson; affected son of unaffected parents; only males observed affected |
| Y-linked | Affected father-son lineage across three generations; multiple affected sons in a sibship with daughters; all observed females unaffected; compatibility checks every father-son relationship |

Homework requires known affected/unaffected observations for every person. The lower-level engine
and renderers can represent unknown phenotype (`null`, displayed as `?`). Instructor JSON records
the rationale and compatible modes under homework assumptions. Hidden genotypes and authored
`expected_mode` metadata do not determine the answer; metadata is checked after evaluation.

Homework also rejects cases that need hidden unaffected carrier spouses for compatibility, even
when those carriers are not visible. Student commands select connected cases and hide carriers
before evaluating the answer. A case that becomes unclear after carrier hiding is rejected.

## Sex-balance filter

After one supported teaching profile is identified, the evaluator applies a classroom clarity filter
with affected male count M and affected female count F:

`S = (M - F)^2 / (M + F)`

At least two people must be affected. Autosomal dominant and recessive require `S < 0.25`. X-linked
dominant requires `S > 0.99` and more affected females; X-linked recessive requires `S > 0.99` and
more affected males. Y-linked requires affected males only and the paternal transmission evidence.
The established male-only X-linked recessive profile still applies. The cutoffs are strict; for
example, `S = 0.25` and `S = 0.99` fail. These are not biological laws or sex-specific incidence
estimates.

## Other teaching gate

At least one visibly affected person must occur in the final or penultimate generation:
`A_N + A_(N-1) > 0`. This rejects two or more entirely unaffected trailing rows. It does not require
every branch to contain affected people or make unaffected relatives biologically useless. Valid
inheritance examples can fail this deliberate selection rule.

## Offspring-count filter

After the visible-evidence answer is established, every sibship must have an exact affected-count
tail of at least 0.05 under its parental cross, conditional on the children's sexes. Fresh and cached
procedural cases use original sampled genotypes; authored examples without sampled states use a
compatible witness. Extreme candidates are rejected and generation continues with random draws.
Repair and polishing also recheck the filter before accepting a proposal. This classroom policy
does not force exact Mendelian ratios or declare unusual outcomes biologically impossible.
See [PEDIGREE_PROBABILITY.md](PEDIGREE_PROBABILITY.md) for the tail definition and examples.

Candidates pass rare-trait, biological, teaching, offspring-count, and layout checks. A different answer, weak or
tied evidence, hidden-carrier dependency, or ambiguous drawing blocks a question. Bounded search
reports rejection reasons on exhaustion; invalid inputs and programming errors propagate. Preserve
the biological and evidence diagnostics when reporting a rejection.
