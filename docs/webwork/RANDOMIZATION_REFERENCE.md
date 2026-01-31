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

### Built-in random() functions are already seeded

The PG environment automatically seeds the random number generator with `$problemSeed` before your problem code runs. **For most problems, you can just use the built-in random functions directly without any manual seeding.**

**Simple approach (recommended for most problems):**
```perl
# These functions are already deterministic based on $problemSeed
$value = random(1, 10, 1);
$item = list_random(@items);
$nonzero = non_zero_random(-5, 5, 1);
```

The same `$problemSeed` will always produce the same sequence of random values.

### When and how to manually seed PGrandom

Create and seed a local `PGrandom` object when you need:
- Multiple independent random streams
- To save and restore RNG state
- Explicit control over seeding for complex randomization

**CORRECT way to manually seed:**
```perl
# Create an instance, then call srand on it
$local_random = PGrandom->new();
$local_random->srand($problemSeed);

# Now use the instance methods
$value = $local_random->random(1, 10, 1);
```

**INCORRECT - these will cause errors:**
```perl
# WRONG - seed() doesn't exist, use srand()
PGrandom->seed($problemSeed);  # ERROR!

# WRONG - can't call srand as a class method
PGrandom->srand($problemSeed);  # ERROR!

# Usually unnecessary - built-in random() is already seeded
SRAND($problemSeed);  # Resets global RNG (rarely needed)
```

**Key points:**
- Method name is `srand`, not `seed`
- Call `srand` on an **instance** (object), not the class
- Use `PGrandom->new()` to create an instance first

**Working examples in this repo:**
```bash
# Many files use this pattern successfully:
grep -r "local_random->srand" problems/
```

### Other practical tips

- Avoid `SRAND(seed)` unless you intend to reset the global RNG for the entire
  problem (rarely needed).
- If you select from hash keys, **sort the keys first** before random selection so the
  same seed yields the same result across runs:
  ```perl
  @sorted_keys = sort keys %hash;
  $selected = list_random(@sorted_keys);
  ```
- In this renderer snapshot, avoid `NchooseK`/`shuffle` and use built-in random
  selection or manual array manipulation for subsets or indices.
