# Multi-Subject Classification and Full CSV Assignment

## Summary

Complete the classification by adding missing subject and chapter assignments to the existing `topic_classifier/task_files/*.csv` files.

Treat every assignment already present in the task CSVs as correct and intentional. This project is additive:

- add missing questions
- add missing cross-subject assignments
- preserve all existing rows in their current files and chapters
- preserve existing repeated rows, which may intentionally control question frequency

A concrete question variant may appear in every subject where it reasonably functions as instructional material. Within each newly added subject, choose one appropriate chapter.

Classification will be performed through direct source analysis and manual CSV editing. Existing JSONL classification runs may be consulted as supporting evidence. Validation tooling should prove that additions are valid, correctly routed, complete, and fully additive.

## Current-File Safety

The repository may have changed since this plan was drafted. Begin by reading the current plan, repository rules, and the latest versions of all affected files.

Use the current repository contents as the editing baseline.

Before editing each task CSV:

- reload the current file
- preserve all existing rows and formatting
- incorporate work already completed by the coder or other agents
- merge additions into the latest available version
- confirm that the resulting change remains additive

If affected files change during implementation, reconcile additions against the latest file contents before writing.

## Authoritative Inputs

### Existing assignments

All rows currently present in `topic_classifier/task_files/*.csv` are authoritative assignments for this project.

Preserve existing assignments in their current files and chapters, including:

- assignments that differ from automated recommendations
- rows that appear in only one subject
- repeated identical rows
- rows that may reflect deliberate frequency weighting
- assignments whose placement could support more than one reasonable interpretation

This plan evaluates existing questions only to identify additional subjects and chapters that should be added.

### Question content

Generator and YAML source content is authoritative when deciding whether an additional subject assignment should be added.

### Chapter definitions

Current subject and chapter metadata are authoritative when choosing the chapter for a new assignment.

### Existing JSONL and comparison artifacts

Existing classification logs and comparison results provide supporting evidence. Each final addition must also be supported by direct source analysis.

## Frozen Baseline and Inventory

Create two distinct snapshots before curation.

### Assignment baseline

Record the exact current contents of all task CSVs before making additions.

Use this baseline to prove that:

- every original row remains
- every original row remains unchanged
- every original row remains in the same file
- repeated rows retain their original multiplicity
- the final files equal the original row multisets plus approved additions

### Source inventory

Run the repository's existing generator and YAML discovery commands and record:

- exact commands
- Python runtime
- date
- discovered source count
- concrete variant count, where supported
- resulting inventory artifact

Freeze this inventory for the project.

Use the frozen inventory as the source set for this pass. Include later inventory corrections when they are required for complete coverage.

## Classification Unit

The practical unit of review is the assignable row or concrete source variant represented by the task-file format.

### Generators

Use the task-file identity fields already supported by the repository, including:

`script + flags + input`

Review distinct flags or inputs separately when they materially change question content, depth, or subject relevance.

### YAML banks

Use the repository's existing task-file representation for YAML sources.

Preserve all fields needed by the current loader, including:

- source path
- markers
- inputs
- identifiers
- row-specific data

Use the existing task-file and loader design as the source of truth for YAML granularity.

### Additive assignment invariant

For each reviewed source or concrete variant:

- preserve all existing assignments
- identify additional applicable subjects
- add one chapter assignment within each newly selected subject
- add each normalized assignment once unless repeated frequency is intentionally requested
- preserve all existing rows unchanged

## Broad-Relevance Policy

Add a question to every additional subject where it could reasonably function as instructional material.

Judge relevance from:

- the concept actually tested
- the reasoning required
- the instructional purpose
- the course scope
- the question depth
- whether the question is independently useful in that subject

Base subject relevance on the concept and reasoning the question actually tests. Require each new subject assignment to function as genuine instructional material in that course.

### Laboratory relevance

Assign the laboratory subject when the question develops a practical laboratory outcome or workflow skill, including:

- experimental planning and method selection
- PCR primer or digest design
- sample preparation and assay execution
- interpretation of gels, kinetic measurements, diagnostic assays, or instrument output
- analysis of sequence, alignment, or distance-matrix results produced in a laboratory or computational workflow

Use the underlying scientific concept for its relevant content subject. Reserve laboratory assignments for questions that ask students to plan, perform, evaluate, or interpret experimental work.

## Chapter Selection for New Assignments

Subject selection and chapter selection are separate decisions.

For each new subject assignment:

- choose exactly one valid chapter
- match the chapter to the question's instructional depth
- consider introductory and review chapters as valid destinations
- select the chapter that best fits the question's actual emphasis
- inspect chapter metadata and neighboring existing assignments
- use existing rows as examples of course organization

For example, a basic DNA base-pairing question might be newly added to:

- biotechnology: `dna_genomics`
- biochemistry: `nucleic_acids`
- molecular biology: `dna_structure`
- genetics: the valid chapter that best matches the question's depth

Existing assignments remain in place. These are additional placements only.

## Ambiguity Resolution

Resolve every proposed addition within this plan.

When the correct chapter for a new subject is unclear:

1. inspect the actual question source and relevant flags or inputs

2. inspect the valid chapter definitions

3. inspect nearby existing rows in that subject

4. compare similar questions already assigned

5. consult existing JSONL evidence when useful

6. choose the most defensible chapter

7. record the decision and rationale

Escalate uncertain cases to the manager or a dedicated review owner within the project.

The ambiguity record should contain:

- source or concrete variant
- proposed additional subject
- candidate chapters
- evidence considered
- final chapter
- rationale
- reviewer

All proposed additions must have final decisions before completion.

## Parallel Dispatch Strategy

Use parallel atomic tasks once the shared baseline work is complete.

The dependency sequence is:

1. WP1 establishes the current files, baseline, inventory, and file map.

2. WP2 and WP3 run in parallel.

3. WP4 and WP5 run in parallel after WP2 and WP3 complete.

4. WP6 integrates both curation streams.

5. WP7 and WP8 run in parallel against the integrated result.

6. WP9 completes documentation after validation results are available.

Each work package has one owner, one concrete output, and one verification step.

## Work Items

## WP1: Inspect Current State and Freeze Baselines

**Owner:** repository inspection agent

**Files:**

- `topic_classifier/task_files/*.csv`
- current discovery scripts
- current metadata and routing files
- current validation and report files

**Scope:**

- read repository instruction and rules files
- inspect the latest versions of affected files
- identify work already completed by the coder or other agents
- create the task-CSV assignment baseline with row multiplicity preserved
- run and record the source discovery commands
- verify the linked task-file directory and sibling repository relationship
- identify the exact files involved in routing, loading, reporting, validation, tests, and changelog handling

**Outputs:**

- current-state report
- frozen assignment baseline
- frozen source inventory
- discovery command record
- file-impact map

**Success criteria:**

- every current CSV row is represented in the baseline
- repeated rows retain their original counts
- two consecutive discovery runs produce the same frozen inventory
- the file-impact map names every file required by later work packages
- existing coder work is incorporated into the baseline

**Validation:**

- compare the baseline against the current task CSVs
- rerun discovery and compare inventory results
- verify that all affected files are named in the file-impact map

## WP2: Audit Routing for New Assignments

**Owner:** routing audit agent

**Files:**

- subject metadata files
- chapter metadata files
- chapter-to-task-file routing definitions
- `topic_classifier/task_files/*.csv`

**Scope:**

- enumerate valid subjects and chapters
- identify the destination task CSV for every valid chapter
- resolve missing or conflicting routes before curation begins
- preserve existing row placement

**Outputs:**

- chapter-to-task-file routing audit
- explicit chapter-to-task-file map
- completed routing corrections required for new additions

**Success criteria:**

- every valid chapter has exactly one destination task CSV
- every chapter that may receive an addition has a confirmed route
- routing behavior is explicit and deterministic

**Validation:**

- run routing coverage across all current chapter metadata
- verify one destination for every valid chapter
- verify that every task CSV destination exists

## WP3: Define Additive Merge and Comparison Semantics

**Owner:** assignment-model agent

**Files:**

- assignment-loading modules
- comparison modules
- reporting modules
- tests covering assignment identity and merge behavior

**Scope:**

- inspect how current loaders and comparison tools handle repeated script paths, flags, inputs, and YAML fields
- define comparison behavior that preserves the entire existing baseline
- define normalized identity for newly added rows
- implement required fixes so all distinct rows remain visible during validation

**Required invariant:**

`final CSV row multiset = original CSV row multiset + approved new rows`

The implementation must preserve:

- every original row
- original row order where practical
- original repeated-row counts
- distinct flags and inputs
- YAML-specific row fields
- valid cross-subject additions

**Outputs:**

- baseline-preservation rule
- normalized identity definition
- concrete overwrite or collapse examples
- completed loader and comparison fixes
- focused tests

**Success criteria:**

- every original row survives loading and comparison
- repeated rows retain multiplicity
- distinct variants remain distinct
- valid multi-subject additions remain distinct
- accidental repeated additions are detectable

**Validation:**

- test repeated script paths
- test distinct flags and inputs
- test YAML-specific identity fields
- test existing repeated rows
- test valid multi-subject additions

## WP4: Add Missing Generator Assignments

**Owner:** generator curation agent

**Files:**

- generator source files
- relevant subject and chapter metadata
- `topic_classifier/task_files/*.csv`
- generator curation workstream artifact

**Scope:**

- inspect every frozen generator or supported concrete generator variant
- identify subjects not already represented for that question
- add each defensible missing subject assignment
- choose the appropriate chapter for each addition
- preserve every existing generator row unchanged
- edit current task CSV versions by hand
- record every addition and its rationale

**Outputs:**

- additive generator rows
- generator addition report
- resolved generator ambiguity records

**Success criteria:**

- every frozen generator is reviewed
- every defensible missing subject assignment is added
- each added chapter is valid
- each added row routes to the intended CSV
- every existing generator row remains unchanged

**Validation:**

- compare final generator rows against the baseline
- validate all added chapters and routes
- verify one newly added row per normalized assignment
- verify complete generator review coverage

## WP5: Add Missing YAML Assignments

**Owner:** YAML curation agent

**Files:**

- YAML question banks
- relevant subject and chapter metadata
- `topic_classifier/task_files/*.csv`
- YAML curation workstream artifact

**Scope:**

- inspect each frozen YAML source at the granularity supported by the existing task-file format
- identify additional applicable subjects
- add defensible missing subject assignments
- preserve required markers, inputs, and identifiers
- preserve every existing YAML row unchanged
- record every addition and its rationale

**Outputs:**

- additive YAML rows
- YAML addition report
- resolved YAML ambiguity records

**Success criteria:**

- every frozen YAML source is reviewed
- every defensible missing subject assignment is added
- all additions preserve the existing row schema
- all added chapters and routes are valid
- every existing YAML row remains unchanged

**Validation:**

- compare final YAML rows against the baseline
- validate markers, inputs, identifiers, chapters, and routes
- verify complete YAML review coverage

## WP6: Integrate Current CSV Changes Safely

**Owner:** integration review agent

**Files:**

- all affected `topic_classifier/task_files/*.csv`
- generator addition report
- YAML addition report
- ambiguity records
- baseline snapshot

**Scope:**

- reload all affected CSVs before integration
- incorporate changes made by the coder or concurrent agents
- merge generator and YAML additions into the latest file versions
- preserve all pre-existing and concurrently added valid rows
- review the additive diff only
- retain existing ordering and formatting where practical
- resolve overlapping additions between WP4 and WP5

**Outputs:**

- final additive CSV changes
- consolidated addition report
- baseline-preservation report
- resolved ambiguity record

**Success criteria:**

- every baseline row remains with identical content and multiplicity
- every baseline row remains in the same file
- every existing chapter value remains unchanged
- every final difference from baseline is an approved added row
- overlapping additions are reconciled exactly once
- concurrent changes are preserved

**Validation:**

- run full baseline multiset comparison
- inspect the final additive diff
- verify every added row against its curation record
- verify every ambiguity record has a final decision

## WP7: Add Minimal Validation Infrastructure

**Owner:** validation agent

**Files:**

- assignment-loading modules
- validation modules
- coverage-report modules
- routing validators
- focused tests
- report outputs

**Scope:**

Implement the tooling needed to validate the additive result:

- load every assignment while preserving rows that share a script path
- validate subjects and chapters on newly added rows
- validate routing for newly added rows
- compare final CSVs against the frozen baseline
- verify that every baseline row retains its original content, location, and multiplicity
- detect accidental repeated additions
- report source coverage
- report additions grouped by subject and chapter

Validation tools should inspect and report while leaving task CSV contents unchanged.

**Outputs:**

- baseline-preservation validator
- added-row validator
- routing validator
- coverage report
- addition summary
- focused tests

**Success criteria:**

- every baseline alteration is detected
- repeated-row multiplicity is preserved
- multi-subject additions remain visible
- every added row is validated
- reports operate at the repository's supported source granularity
- validation tools leave source data unchanged

**Validation:**

- run focused validator tests
- compare file checksums before and after validation
- verify report completeness against the frozen inventory
- verify coverage of every added row

## WP8: Regression Coverage

**Owner:** regression agent

**Files:**

- regression fixtures
- relevant test modules
- expected assignment data

**Scope:**

Create a balanced regression set covering:

- a question added to four subjects
- subject relevance grounded in the concept and reasoning actually tested
- introductory versus advanced placement for a new assignment
- flag-dependent applicability
- distinct variants sharing one script path
- YAML rows with required markers or inputs
- a genuinely single-subject question correctly retained in one subject
- accidental duplicate addition detection
- preservation of intentional existing repeated rows
- detection of a removed, changed, or relocated baseline row

The DNA base-pairing example should remain one case within the balanced set.

**Outputs:**

- complete regression fixture set
- expected assignment sets
- focused regression tests

**Success criteria:**

- relevance thresholds are represented with both qualifying and non-qualifying examples
- existing rows and new additions are distinguished
- additive-only behavior is enforced
- intentional frequency weighting is preserved
- structural validation covers additions while treating existing content as authoritative

**Validation:**

- run all focused regression tests
- verify each policy boundary has at least one passing case
- verify each structural failure has at least one failing case

## WP9: Changelog and Documentation

**Owner:** documentation agent

**Files:**

- `docs/CHANGELOG.md`
- planning reports
- audit artifacts
- decision records
- workstream artifacts

**Scope:**

- document the additive broad-relevance policy
- document baseline preservation
- document discovery and validation commands
- apply the repository changelog rotation rule when the active changelog reaches the documented threshold
- reconcile documentation with completed coder work
- organize planning artifacts according to `docs/REPO_STYLE.md`

**Outputs:**

- changelog update
- complete planning artifact set
- documented commands and report locations
- changelog rotation when required by the current line count

**Success criteria:**

- documentation describes the completed additive behavior accurately
- existing assignments are described as preserved
- planning artifacts follow repository organization rules
- changelog handling follows the repository rule
- all documentation references real files and validation commands

**Validation:**

- verify planning artifact organization
- validate local Markdown links
- confirm changelog line count and resulting rotation action
- compare documentation claims against final reports and test output

## Expected Task CSVs

Confirm the current directory contents before editing. Expected files include:

- `topic_classifier/task_files/biochem_tasks1.csv`
- `topic_classifier/task_files/biochem_tasks2.csv`
- `topic_classifier/task_files/biochem_tasks3.csv`
- `topic_classifier/task_files/biostats_tasks.csv`
- `topic_classifier/task_files/biotech_tasks.csv`
- `topic_classifier/task_files/genetics_tasks1.csv`
- `topic_classifier/task_files/genetics_tasks2.csv`
- `topic_classifier/task_files/laboratory_tasks.csv`
- `topic_classifier/task_files/molecular_bio_tasks.csv`
- `topic_classifier/task_files/other_tasks.csv`

WP1 must confirm the complete current file list before curation begins.

## Validation Plan

Use the repository-required Python 3.12 runtime and command pattern:

`source source_me.sh && python ...`

Run pytest with:

`pytest tests/`

### Baseline preservation

Verify that:

- every original row remains
- every original row remains in the same file
- every original field remains unchanged
- repeated rows retain the same multiplicity
- the final CSV difference consists only of additions

### Added-row validity

Verify that each added row:

- uses a discovered source
- preserves required flags, inputs, markers, and identifiers
- names a valid chapter
- appears in the correct task CSV
- represents a defensible additional subject
- appears once as a normalized addition unless repeated frequency is intentional

### Coverage

Run the existing unassigned and coverage reports at the repository's supported source granularity.

Success requires:

- every frozen source reviewed
- every previously unassigned source assigned
- every defensible missing subject assignment added
- every added assignment traceable to direct source analysis

### Repository tests

Run:

- focused additive-merge tests
- routing validation
- baseline-preservation validation
- coverage reports
- relevant classifier regression checks
- the full `pytest tests/` suite

## Completion Criteria

The plan is complete only when:

- the current repository state and existing coder changes were inspected
- all repository rules were read
- the original task-CSV row multiset was frozen
- every original task-CSV row remains unchanged
- every original task-CSV row remains in the same file
- every existing chapter assignment remains unchanged
- existing repeated rows retain their original counts
- every frozen source was directly reviewed for missing assignments
- every defensible missing subject assignment was added
- every addition has one valid chapter in that subject
- every addition routes to the correct task CSV
- all ambiguous additions have final decisions
- direct source analysis produced the final classifications
- existing JSONL results were used as supporting evidence
- every normalized new assignment appears once unless repeated frequency is intentional
- all assignments remain visible through loading and comparison
- coverage and validation reports pass
- the addition report is complete
- the ambiguity record contains final decisions for every case
- the relevant regressions and full Python 3.12 test suite pass
- changelog handling follows the current repository policy
- all planning artifacts follow repository organization rules

## Operational Workflow

Use this workflow:

- inspect the current repository and preserve existing work
- freeze the task-CSV baseline and source inventory
- audit routing and assignment identity in parallel
- analyze generator and YAML sources in parallel
- identify missing subject assignments
- choose chapters for new assignments
- manually add rows to the current task CSVs
- consult existing JSONL and comparison artifacts as evidence
- integrate additions against the latest files
- validate baseline preservation, routing, coverage, and regression behavior
- document the completed work in the designated planning artifacts

The final task CSVs consist of the current rows plus approved additions.
