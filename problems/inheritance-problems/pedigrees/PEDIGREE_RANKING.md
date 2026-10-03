# Pedigree candidate ranking

The production sorter chooses an ordering within the current eligible pool. It is a reversible
selection heuristic, not an acceptance rule or calibrated quality score. Pipeline placement is in
[PEDIGREE_PIPELINE.md](PEDIGREE_PIPELINE.md); native geometry definitions are in
[PEDIGREE_LAYOUT.md](PEDIGREE_LAYOUT.md).

## Five production signals

[ranking.py](pedigree_lib/ranking.py) computes five favorable percentile ranks against the current
pool, then averages them equally. Ties use average midranks; stable randomized arrival order breaks
final score ties. Higher-ranked candidates come first. The five signals are:

1. Lower fraction of all people outside the set of affected people, their ancestors, and the
   immediate partners of anyone in that set. Partner ancestors and descendants are not recursively
   included; hidden carriers do not enter this visible measure.
2. Higher affected-region fill, using the person-only native cells defined in
   [PEDIGREE_LAYOUT.md](PEDIGREE_LAYOUT.md).
3. Higher generation progression: count each expansion as +1 and each contraction as -1 between
   rows beginning after generation I; sum the signs. The implementation is
   [generation_features.py](pedigree_lib/generation_features.py).
4. Lower mean row density, as defined in [PEDIGREE_LAYOUT.md](PEDIGREE_LAYOUT.md).
5. Lower excess bottom-empty fraction, `max(0, E - 0.12)`.

Unaffected relatives remain available for teaching; affected reach only changes ordering.

The bottom-empty fraction `E` is the largest bottom-anchored empty rectangle divided by the tight
content bounding-box area. It is measured before display scaling. Candidates at or below the 12%
repair target receive the same rank on this signal. See [PEDIGREE_POLISHING.md](PEDIGREE_POLISHING.md)
for the separate geometric repair stage.

The mean is pool-relative. It is recomputed when pool membership changes and is not stored in cache.
It expresses no absolute quality level. Random candidate generation supplies arrival order; output
scenario and choice shuffling happens later in the pipeline.

## Evidence and limits

Historical numbers and their interpretation limits are consolidated in
[PEDIGREE_EVIDENCE.md](PEDIGREE_EVIDENCE.md). The sorter comparison is retrospective on a selected
1,000-case corpus; it supports a simple reversible ordering choice, not prospective improvement or
independent generalization. No additional calibration is planned.

Other structural/topological measurements were explored, but they do not contribute to the
production sorter. See [PEDIGREE_GRAPH_ANALYSIS.md](PEDIGREE_GRAPH_ANALYSIS.md) for separate graph
comparison diagnostics and their limitations.
