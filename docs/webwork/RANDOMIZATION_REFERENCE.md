# Randomization reference

This note summarizes common PG randomization entry points for the local renderer
snapshot (PG 2.17-based, trimmed macro set). Use it when you need seed-stable
behavior, linting checks, or to choose the right helper macro.

## Core PG (PGbasicmacros.pl)
- `random(begin, end, incr)`
- `non_zero_random(...)`
- `list_random(...)`
- `SRAND(seed)` (resets the main PG random generator)

## Core PG auxiliary functions (PGauxiliaryFunctions.pl)
- `random_coprime([arrays...])`
- `random_pairwise_coprime([arrays...])`

## Choice macros (PGchoicemacros.pl) [deprecated]
- `NchooseK(N, K)` (deprecated)
- `shuffle(n)` (deprecated)

## Parser widgets (internal randomization helpers)
- `randomOrder(...)` in:
  - `parserPopUp.pl`
  - `parserRadioButtons.pl`

## Contexts
- `randomPrime(start, end)` (contextInteger.pl)

## Matrix macros
- `random_inv_matrix(rows, cols)` (PGmorematrixmacros.pl)
- `random_diag_matrix(n)` (PGmorematrixmacros.pl)

## Statistics macros
- `urand(mean, sd, N, digits)` (normal distribution)
- `exprand(lambda, N, digits)` (exponential)
- `poissonrand(lambda, N)` (Poisson)
- `binomrand(p, N, num)` (binomial)
- `bernoullirand(p, num, options)` (Bernoulli)
- `discreterand(n, @table)` (discrete distribution)

## Deprecated or legacy macros
- `ProblemRandomize(...)` (problemRandomize.pl)

## RNG objects and direct usage
- `PGrandom->random(...)` and `PGrandom->srand(...)`
- `$PG_random_generator->random(...)` and `$PG_random_generator->srand(...)`

## Practical guidance
- For deterministic output with a fixed seed, prefer a local `PGrandom` instance
  and seed it with `problemSeed`.
- Avoid `SRAND(seed)` unless you intend to reset the global RNG for the entire
  problem.
- If you select from hash keys, sort the keys before random selection so the
  same seed yields the same result across runs.
- In this renderer snapshot, avoid `NchooseK`/`shuffle` and use a local
  `PGrandom` plus manual selection for subsets or indices.
