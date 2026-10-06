# Question-voice skill evaluation

## Status

Evaluation is complete. This report records the protocol before scoring so that final tables
can distinguish observed results from the pre-specified comparison.

## Frozen bases and arm construction

| Material | Base or freeze | State |
| --- | --- | --- |
| biology-problems | `82bca89bd442209f823091f1aebfd705be7a49e1` | base recorded before implementation edits |
| vosslab-skills | `93fc5e2b24195866bd0794f4fdbe02e48b2e3195` | base recorded; its working tree had implementation edits |
| control | `git archive` of both bases | target files and changelogs removed |
| treatment | biology archive plus frozen local guides, TEMPLATE, checker, and bptools skill | target files, changelogs, target correction history, and QUESTION_EVIDENCE removed |

The target generators were removed in both arms:
`lethal_allele_survival.py` and `monohybrid_litter_inference.py`. Target tests and all
`docs/CHANGELOG*.md` files were also removed. The treatment arm excluded
`QUESTION_EVIDENCE.md`, target-specific exemplar passages, target function inventories, and
their bundled copies. The sanitized pedagogy, voice, and exemplar snapshots matched their
treatment-arm copies byte-for-byte. This keeps R1 and R2 from directly reading their own
correction history. It does not remove a model's general biology knowledge or shared training
priors, so the comparison cannot establish a clean causal pedagogy effect.

## Requests

| ID | Request | Provenance |
| --- | --- | --- |
| R1 | "Added a monohybrid litter inference generator in `inheritance-problems/monohybrid_litter_inference.py` inspired by single-gene dominance scenarios." | Exact recovered changelog sentence at commit `566b690`; normalized to an imperative request for authors. |
| R2 | "Added a lethal allele survival generator in `inheritance-problems/lethal_allele_survival.py` for heterozygote crosses with lethal homozygotes." | Exact recovered changelog sentence at commit `566b690`; normalized to an imperative request for authors. |
| R3 | Write a two-allele incomplete-dominance probability generator with a phenotype rule, parental cross, and target offspring phenotype. | New request, written for this evaluation. |

Each arm receives the identical request text for a request ID. Two independent authors per arm
write a local generator and render five actual BBQ items with `-d 5`, giving 12 author runs and
60 rendered items if all runs succeed. R1 and R2 are in-sample because the rules drew on their
history; R3 is out-of-sample. Fresh authors were instructed to use only assigned local materials
and not to inspect peer outputs, checker/judge results, or rationales. Shared filesystem access
means this was procedural isolation, not OS-enforced isolation.

## Scoring protocol

The manager removes arm labels, assigns opaque item IDs, and gives the same item-only corpus to
three new judges. Each judge records pass, fail, or not applicable for C1-C9, U1-U8, and the
item-type rubric, quoting the stem or choice line that supports each decision. Judges do not
receive an expected winner. A category result is the majority of the three item judgments. The
checker runs on every output and its findings are advisory prompts for judges, never automatic
failures. A separate fresh verifier receives generators and outputs without judge scores and
independently recomputes every answer key. U9 is verifier-owned. Judges and verifier are distinct
fresh agents.

### C1-C9 applicability rules and primary measure

These rules apply identically to both arms. A category is excluded from a request total only when
its named feature is absent; it is not counted as a pass by default.

| Category | Applies when | Pass condition |
| --- | --- | --- |
| C1 | a count, fraction, or probability is asked | the requested population and denominator are explicit |
| C2 | every item | every instruction, label, legend, and sentence supplies needed information |
| C3 | supplied counts require arithmetic | the stated arithmetic yields intended whole-number results |
| C4 | a lethal-survival selected-response item | both `1/3` and `2/3` survivor alternatives appear; FIB/NUM items are not applicable |
| C5 | choices have an inherent numeric or genotype order | choices use that natural order |
| C6 | choices name a genotype, mechanism, or type | labels make that identity explicit and parallel |
| C7 | every scenario has organism or role wording | the wording matches its stated organism and role |
| C8 | every item | data appear before the question and remain understandable without color alone |
| C9 | every item | pass if no insufficiency escape appears, or if one is unambiguous and correct in at least one possible scenario |

For each request, the primary comparison is the mean pass rate over only C1-C9 slots that apply
to every rendered item in both arms for that request. This fixed common-slot rule avoids treating
an MC-only criterion as an automatic advantage over an FIB item. The report will also show raw
satisfied-category counts and their denominators, but those descriptive totals are not the
primary comparison.

Routed rubric rows follow the actual rendered item type. MC and MA use M1-M5, FIB and numeric
use F1-F3, matching uses T1-T3, statement banks use S1-S4, and ordering uses O1-O2. Because R3
permits either MC or FIB, results will keep routed scores separate by item type and will not pool
incompatible denominators. Judges receive opaque replicate grouping for U5 scenario-variety
review, not arm identities. U9 is verifier-owned rather than an item-only judge decision. M2
judges assess whether choices plausibly represent distinct student errors from the output; only
the verifier may compare that judgment with the separate sanitized author rationale.

## Results

All 12 author runs rendered five items, for 60 items. Three judges scored the opaque corpus
independently; each item-category label had a literal two- or three-judge majority. The separate
enumeration verifier found every key correct: 60/60.

| Request | Common C slots | Control | Treatment | Result |
| --- | --- | --- | --- | --- |
| R1 | C2, C3, C6, C7, C8, C9 | 60/60 (100.0%) | 60/60 (100.0%) | tie |
| R2 | C1, C2, C4, C5, C6, C7, C8, C9 | 70/80 (87.5%) | 69/80 (86.3%) | control higher |
| R3 | C1, C2, C6, C7, C8, C9 | 59/60 (98.3%) | 60/60 (100.0%) | treatment higher |
| Combined | request-specific common slots | 189/200 (94.5%) | 189/200 (94.5%) | tie |

The literal majority-vote table yielded a 189/200 tie, so the strict pre-registered success
condition was not met. The result is not evidence that the treatment worsened question text. R1
tied, R2 favored control by one applicable item-category, R3 favored treatment by one. There is
an applicability limitation: the initial report table had described C4 too narrowly. The actual
frozen blind rubric applied C4 to every lethal selected-response item and required both `1/3` and
`2/3`, so valid genotype-ratio and count problems were penalized by this fraction-specific
criterion. The 189/200 is retained as the observed literal scorecard result; an optional C4-N/A
sensitivity analysis is descriptive only and cannot establish success. Item-type variation was
also material: control R3 replicate 1
produced FIB while the other R3 outputs were selected-response, so routed scores remain
descriptive rather than pooled.

Selected majority evidence shows why the result is mixed:

- Treatment R2 replicate 1 omitted the required `1/3` and `2/3` fraction alternatives; judges
  quoted genotype-ratio choices such as `2 Cc : 1 cc`, so C4 failed for all five items.
- Control R2 replicate 2 included both `2/3` and `1/3`, so C4 passed, but its fraction choices
  were shuffled, so C5 and M3 failed.
- Treatment R2 replicate 2 passed C4 for four items but the item asking for a dominant phenotype
  omitted `1/3`; the majority scored that one C4 failure.
- Control R3 replicate 2 used `In a population of fur`, which the majority treated as inconsistent
  with a parent-offspring scenario, producing the one C7 failure.

The advisory checker was run on every output and did not determine scores. It found a longest-key
and stem-key echo pattern in control R1 replicate 2, article slips in two control R2 replicate 2
items, and an absolute-word asymmetry in treatment R3 replicate 2; all other set-level reports
were clean. The checker report is retained in the evaluation scratch directory.

The verifier independently enumerated every cross from the rendered stem rather than using the
generator's marked key. It confirmed all 60 keys. Treatment R3 replicate 2 is an operational
deviation: it used a custom `bbq_writer.py` and `actual-d5.txt`, rather than `bptools`, and its
copied-root bootstrap needed a recorded nonfatal Git-check fallback. Its five records and biology
keys were valid, but the deviation remains part of the evaluation record.

### Loop 1

Because the initial literal comparison did not meet the success condition, the canonical guides
received one narrow, general revision: retain meaningful misconception contrasts when sampling,
keep homogeneous ratio components in their meaningful order, and inspect rendered variety without
a numerical quota or a forced no-replacement rule. The treatment material remained sanitized of
the target correction history. Six new control and six new treatment authors produced fresh
five-item outputs. The treatment checker was accidentally omitted from the initial loop sandbox;
it was copied unchanged before freeze, each treatment author ran it and documented a review, and
their original outputs were preserved. The manager's checker found one advisory control R1
stem-key echo; no treatment output had a checker finding.

The same three-judge rubric and separate enumeration approach were repeated. All loop-1 keys
were correct (60/60). The unchanged primary rule keeps only C slots applicable to every item in
both arms for a request:

| Request | Common C slots | Control | Treatment |
| --- | --- | --- | --- |
| R1 | C2, C5, C6, C7, C8, C9 | 60/60 (100.0%) | 52/60 (86.7%) |
| R2 | C1, C2, C5, C6, C7, C8, C9 | 60/70 (85.7%) | 70/70 (100.0%) |
| R3 | C1, C2, C5, C6, C7, C8, C9 | 65/70 (92.9%) | 70/70 (100.0%) |
| Combined | request-specific common slots | 185/200 (92.5%) | 192/200 (96.0%) |

The loop-1 author outputs, checker reviews, and 60/60 independent key verification are complete.
An initial set-level aggregation was rejected because it collapsed item-level votes. A replacement
aggregation used literal majority votes for each of the 60 items and every C1-C9 criterion before
deriving common slots. Under that required calculation, loop 1 meets the strict success condition:
treatment has seven more C1-C9 passes (192/200 versus 185/200) and no wrong key. The loop R3
result is a rerun of the original holdout after the initial experiment and feedback, so it is not
fresh independent out-of-sample evidence.

Representative blind evidence: treatment R2 retained both `1/3` and `2/3` survivor alternatives
in its fraction items, while control R2 had shuffled fraction or count choices; treatment R1
included an unsupported `cannot be determined from this litter` choice in one replicate; and the
control R3 numeric output inserted one-pixel white text with a stated 1% tolerance that did not
match its stored tolerance. The loop verifier also recorded a treatment R1 standalone formatter
without the shared collector and a control R3 legacy NUM output with hidden spans. These are
operational deviations, not key errors.

## V4 WebWork and V5 review pass

V4 initially failed the real renderer because a bare description line was executed as Perl, and
its `0.5 for one-half` entry example revealed the answer. The author preserved that source as
`v4_initial.pgml`, then commented the description and changed the example to `0.25 for
one-fourth`. Independent renderer evidence at seed 4242 then passed lint, awarded score 1 to
`0.5`, rejected `0.25` with score 0, and produced a Playwright screenshot with a readable prompt,
subscripts and italics, one answer field, visible controls, and no clipping. The revised static
judge found U1-U4 and U6-U8 plus F1-F3 satisfactory; U5 did not pass because it is a fixed
single-scenario fixture. U9 remained verifier-owned.

V5 made no generator edits. The treatment review correctly flagged the reciprocal-cross
generator's two-scenario pool and `Which statement best describes ...` lead-in; it did not flag a
long stem or solution-path hint there. It flagged the horse generator's long nonessential
preamble/citations and its explicit ordered solution-path hint; its six-source scenario pool is
not tiny, although the sampled output repeated scenarios because draws are with replacement.

## Decisions and failures

- The comparison is a small procedural experiment with shared model priors and only procedural
  isolation; it cannot prove a causal pedagogical effect of the guides.
- The strict success condition failed on an initial tie (189/200 each). The planned bounded
  revision-loop triggered one general-guide revision and a fresh two-arm loop. The corrected
  item-level loop-1 analysis met the condition (192/200 treatment versus 185/200 control), so a
  second loop is not required.
- Renderer access was initially unavailable, then a loopback renderer enabled a bounded V4 repair
  and independent lint, grading, and visual proof. The initial failure is retained rather than
  rewritten as a first-pass success.

## Follow-up outside this plan

The separate source review identified a wrong daughters key and grammar issue in
`x_linked_tortoiseshell.py`, a uL/mL mismatch in `serial_dilution_factor_mc.py`, and text issues
in the reciprocal-cross and horse-coat generators. These are not changed by this evaluation.
