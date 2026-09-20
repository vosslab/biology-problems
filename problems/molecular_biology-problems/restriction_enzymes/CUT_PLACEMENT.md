# Restriction-digest cut placement

Teaching and drawing rules for [linear_digest.py](linear_digest.py) and
[circular_digest.py](circular_digest.py).

Every difficulty uses the same question: two enzymes on the map, one named
for the digest, students select the distinct gel-band sizes.

The design goal is a large family of valid questions at every difficulty,
enough for about 199 unique patterns per mode. That is a check on the
search space, not a generation gate.

## Core model

Generation has three stages:

1. Place a geometrically legal map by random coordinates and enzyme
   interleaving.
2. Evaluate both enzymes' digest outcomes under the question DNA type.
3. Retry placement with the same fixed difficulty parameters until a map
   meets the validity and difficulty requirements.

Placement changes only the site coordinates. Difficulty, molecule length,
site counts, and DNA type stay fixed during the search for one question.
Each question is an independent random draw from the family of maps that
meet that mode.

A **valid** map is legal to ask. A **difficulty requirement** is essential
to that mode.

## Validity

A map is valid when:

- answers use only the selected enzyme
- at least two distinct correct bands remain
- `shared_correct_fraction <= 0.5`
- the selected enzyme has at least two sites
- geometry below holds
- in linear strand mode, selected strand bands differ from the fragment
  reading of those same selected sites: the strand intervals plus the two
  end pieces `s0` and `length - sN`

```text
shared_correct_fraction =
    len(intersect(correct_bands, distractor_bands)) / len(correct_bands)
```

The distractor may share at most half of the correct band sizes.

Adjacent restriction sites are allowed. Equal-sized fragments co-migrate
as one gel band.

## Placement

Follow the original linear method. Choose integer coordinates at random,
sort them, then assign enzyme identities in an alternating pattern. The
interleaving mixes the two enzymes. The random coordinates supply a large
space of different questions.

```text
A B A
A B A B A
```

Selected occupies both ends, so it has one more site than the distractor.

Circular 2+2 uses the same assignment around the ring, with `0 kb` as `B`:

```text
B A B A
```

Circular 3+2 keeps `0 kb` as `B`. Sort the four remaining sites clockwise
and assign three to `A` and one to `B` while keeping the enzymes mixed.
For example:

```text
B A B A A
B A A B A
```

Choose among valid mixed arrangements rather than requiring strict
alternation.

Placement retains that large random space. It does not engineer one ideal
spacing pattern. Evaluation rejects arrangements that fail the teaching
requirements.

## Circular geometry

- `0 kb` sits at the center of the top straight.
- Enzyme sites occupy straight-edge coordinates with enough room for inside
  labels. The selected enzyme does not use `0 kb`.
- The distractor enzyme has a site at `0 kb`. Treat `0` and `length` as
  the same coordinate; store and render only `0`.
- Integer kb values on rounded corners stay ordinary coordinate marks:
  black tick, outside numeric label.
- Coordinates walk the full rounded-rectangle centerline clockwise from
  `0 kb`, including the corner arcs.
- Each restriction site stays at its true kb value.

Every integer kb has one tick and one numeric label. At a restriction site,
the enzyme-colored tick replaces the black tick and the enzyme name sits
inside the DNA.

## Evaluation

Compute fragments for the selected enzyme and for the distractor using the
question DNA type. On a linear strand map, the selected enzyme uses the
strand formula and the distractor uses the fragment formula. Then:

```text
correct_bands = set(correct_fragments)
distractor_bands = set(distractor_fragments)
overlap = intersect(correct_bands, distractor_bands)
shared_correct_fraction = len(overlap) / len(correct_bands)
co_migration = len(correct_fragments) > len(correct_bands)
```

Validity uses the checks above. Difficulty uses the band requirements
below. Keep any map that satisfies both.

## Difficulty

Difficulty constrains the resulting digest and answer structure. It does
not prescribe a small number of site arrangements. Evaluation accepts any
arrangement that meets the teaching rules for that mode. Unequal fragments
and co-migration apply to the selected enzyme only.

Linear Easy and Medium are fragment questions. Linear Rigorous is a strand
question: co-migration and a different reading of the ends.

Easy circular maps use two selected sites. Medium and rigorous circular
maps use three selected sites so students follow more intervals around the
ring.

`-E` / `-M` / `-R` select the presets below. The fragment lists in the
examples show the answer shape, not a required set of sizes.

### Easy

Simple answer structure: two selected sites, all selected fragments
unequal, at least two distinct correct bands, no co-migration.

Linear: 10 kb fragment, 2 selected sites, 1 distractor site.

Circular: 10 kb circle, 2 selected sites, 2 distractor sites including
`0 kb`.

### Medium

More intervals than Easy: three selected sites, all selected fragments
unequal, no co-migration.

Example of the shape, not a required key:

```text
fragments {2, 4, 6} -> bands {2, 4, 6}
```

Linear: 12 kb fragment, 3 selected sites, 2 distractor sites.

Circular: 12 kb circle, 3 selected sites, 2 distractor sites including
`0 kb`.

### Rigorous

Selected-enzyme co-migration required: a repeated selected fragment size,
at least two distinct correct bands, fewer distinct bands than fragments.

Example of the shape, not a required key:

```text
fragments {5, 5, 6} -> bands {5, 6}
```

Linear: 16 kb open strand, 4 selected sites, 3 distractor sites.

Circular: 16 kb circle, 3 selected sites, 2 distractor sites including
`0 kb`.

## Digest calculations

Calculate each enzyme independently. Sort only that enzyme's cut
coordinates, then apply the question DNA type.

For sorted sites `s0 < s1 < ... < sN`:

Linear fragment, both physical end pieces are in the digest:

```text
s0
s1 - s0
...
sN - s(N-1)
length - sN
```

Linear strand, selected enzyme only: intervals between consecutive selected
sites. The two outside pieces belong to the larger molecule and are not
gel bands for the named enzyme:

```text
s1 - s0
...
sN - s(N-1)
```

The distractor on a strand map still includes its two end pieces, using the
linear-fragment formula.

Circular, including the wraparound fragment. A site at `0 kb` is the same
physical position as `length kb`; include it once:

```text
s1 - s0
...
sN - s(N-1)
length - sN + s0
```

Run that calculation for the selected enzyme and for the distractor, except
linear strand as above. Then convert each fragment list to its set of
distinct gel-band sizes.

Same selected coordinates, three DNA types:

```text
length = 10, sites = {2, 6}
linear fragment: {2, 4, 4}
linear strand:   {4}
circular:        {4, 6}
```

## Ownership

- [linear_digest.py](linear_digest.py): linear placement, interleaving,
  fragment and strand logic
- [circular_digest.py](circular_digest.py): circular geometry, `0 kb`,
  wraparound fragments
- [digest_lib.py](digest_lib.py): shared enzyme names, and shared
  evaluation when both scripts can use the same scoring
