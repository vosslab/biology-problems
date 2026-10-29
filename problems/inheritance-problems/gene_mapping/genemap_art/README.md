# Gene-mapping artwork

Approved SVG renderers shared by the question generators and the
[visual sampler](../visual_sampler/README.md). The artwork stays local to gene mapping.

- [individual_phenotypes.py](individual_phenotypes.py) draws all 26 fly phenotypes at
  108 by 72 pixels beside their gene descriptions. Callers supply the question's gene color.
  Wings change color, heads retain each phenotype's base color, and other surfaces vary
  by phenotype. [phenotype_art.py](phenotype_art.py) supplies the shared side-view geometry.
- [asci.py](asci.py) draws four overlapping, labeled spores in an unordered ascus.
  Each recessive allele adds a sector in its gene's color; plus alleles remain neutral.
  Placement minimizes occluded colored sectors and carries no meiotic-order information.

The integration changes presentation of existing MC, MA, numeric, and fill-in-the-blank
questions. Counts, genotype multisets, mapping calculations, answer keys, distractors, and
scenario randomization retain their existing behavior. Flies illustrate individual gene
descriptions; offspring tables do not depict mixed phenotypes. Ordered tetrads retain their
existing rendering.

SVG is inline and self-contained. Both illustrations are inside HTML tables so the existing
`-B -I` export renders them into packaged PNGs for Blackboard. Use `--selftest` for an HTML
preview. Raw inline-SVG acceptance by a particular LMS must be checked in that LMS; prefer
the image export for import. Genotype letters remain visible independently of color.

The fly artwork is covered by [LICENSE.CC-BY-SA-4.0](../../../../LICENSE.CC-BY-SA-4.0).
The [sampler source ledger](../visual_sampler/README.md) records inspiration and drawing
references. These are humorous hypothetical phenotypes and schematic spores, not scientific
identification plates. Source code retains the repository's code license.
