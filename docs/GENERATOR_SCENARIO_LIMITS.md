# Generator scenario limits

Some generators intentionally contain fewer than 199 distinct questions. Requesting
more questions cannot expand these source-defined scenario spaces. This inventory
distinguishes those limits from generators that merely need more duplicate attempts.

## Explicit scenario limits

| Generator | Maximum | Basis |
| --- | ---: | --- |
| `biochemistry-problems/PUBCHEM/NUCLEOBASES/match_purine_structures.py` | 2 | Two purine structures |
| `biochemistry-problems/PUBCHEM/NUCLEOBASES/match_pyrimidine_structures.py` | 3 | Three pyrimidine structures |
| `biochemistry-problems/electrophoresis/kaleidoscope_ladder/kaleidoscope_ladder_mapping.py` | 6 | Six visually distinct band sets in mapping mode |
| `biochemistry-problems/PUBCHEM/AMINO_ACIDS/which_amino_acid.py` | 20 | Twenty standard amino acids |
| `biochemistry-problems/PUBCHEM/AMINO_ACIDS/match_amino_acid_structures.py` | 20 | Twenty standard amino acids |
| `molecular_biology-problems/amplicon_copies.py` | 30 | Thirty enumerated PCR scenarios |
| `biochemistry-problems/enzymes/michaelis_menten_table-Km.py` | 54 | Nine Vmax values by six Km values |
| `biochemistry-problems/enzymes/michaelis_menten_table-inhibition.py` | 135 | Three inhibition types by nine Vmax and five Km values |
| `laboratory-problems/pipet_size_mc.py` | 189 | Three disjoint pipet ranges with 63 valid settings each |

The amino-acid generator is used for both MC and FIB task variants, so both task
outputs stop at 20 even though they call the same source script differently.

## Finite rendered variants

`biochemistry-problems/thermodynamics/exergonic_endergonic_reactions.py` contains
eight authored prompts with four choices. If shuffled choice order is considered
part of question identity, it has at most `8 * 4! = 192` rendered variants. Random
sampling usually produces fewer than 192 within a small duplicate-attempt budget.

## Counts that are not limits

The following generators reached 199 questions when the duplicate-attempt budget
was increased from 219 to 1,000:

- `molecular_biology-problems/linear_digest.py`
- `inheritance-problems/poisson_flies.py`
- `biostatistics-problems/hypothesis_statements.py`
- `laboratory-problems/solution-molarity-mol_weight-numeric.py`

Their lower website counts are sampling-budget shortfalls, not finite scenario
limits. The website runner currently requests only 219 attempts for 199 accepted
questions. Duplicate-heavy generators need a larger or adaptive attempt budget.

The following checks also rule out apparent limits:

- `inheritance-problems/dominant_and_X-linked_recessive_variations.py` reaches 199
  questions with 219 attempts.
- `molecular_biology-problems/dna_gel-estimate_size-MC_or_NUM.py` now reaches 199
  after its calibration-range repair. Older 53-55 question files are stale output.

## Maintenance rule

Add a generator here only when its limit is established by an explicit source cap,
a complete finite scenario enumeration, or a mathematically bounded rendered space.
Do not infer a limit from one underfilled generated file.
