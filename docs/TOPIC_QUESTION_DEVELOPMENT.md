# Developing questions for a topic

## Purpose

Turn a request such as "Find 20-50 more questions for Genetics Topic 07" into a useful,
book-informed list that an instructor can review and select from.

The result should practice the right skills, add useful variety, and show exactly what
students would see and answer. A topic name and a list of interesting scenarios are not enough.

This guide covers discovery and candidate review. Use
[QUESTION_PEDAGOGY_GUIDE.md](QUESTION_PEDAGOGY_GUIDE.md) for question design,
[QUESTION_VOICE_GUIDE.md](QUESTION_VOICE_GUIDE.md) for student-facing wording, and
[QUESTION_AUTHORING_GUIDE.md](QUESTION_AUTHORING_GUIDE.md) when implementing generators.
Those guides remain the owners of their detailed rules.

## 1. Establish the topic boundary

Read the current BPW topic page, its task assignments, representative questions, and the
neighboring topic names. Use the actual questions to understand what students practice;
titles alone can conceal overlap or missing skills. Check recent topic changes when relevant.

Write a short scope statement before drafting candidates:

- **Students practice:** the actions this topic teaches, such as calculating a probability
  or interpreting a test result.
- **Students already know:** earlier material that can be supplied or used as background.
- **Outside this request:** related tasks that belong elsewhere.

Use this test for every candidate: **What must the student actually do to answer it?**
Classify by that action, not by the organism, vocabulary, or chapter where the source appears.

For Genetics Topic 07:

| Student task | Placement |
| --- | --- |
| Work out a 9:7 ratio from a two-gene pigment pathway | Earlier gene-interaction topic |
| Use a supplied 9:7 ratio to test observed offspring counts | Topic 07: chi-square |
| Work out the chance that one offspring has a recessive trait | Earlier inheritance practice |
| Use that chance to find exactly two affected offspring out of six | Topic 07: binomial |

Calling a ratio a "null hypothesis" does not automatically turn a ratio-derivation question
into a statistics question. Supply earlier knowledge when the intended task is to apply it.

Resolve routine scope questions from the course materials. Ask a narrow clarification only
when the available evidence leaves a choice that would substantially change the candidate list.
Continue independent source review while waiting; do not make every step an approval gate.

## 2. Find the useful gaps

Make a small working table before choosing the number of candidates for each skill.

| Skill | What the existing questions cover | Useful addition |
| --- | --- | --- |
| Chi-square calculation | Complete dihybrid tables | Find a missing count or compare two terms |
| Chi-square interpretation | Reject or fail to reject | Same statistic with different degrees of freedom |
| Binomial offspring probability | Exactly k offspring | At least k, specified order, or probability of a group |

Distinguish three reasons to add a question:

- **More practice:** the same skill in a meaningfully different situation.
- **A missing task:** a skill within the topic that has little or no coverage.
- **An extension:** a harder comparison or explanation that still uses the topic's methods.

Allocate the requested count across the topic's main skills before writing. Do not let the
easiest source material fill the list. A topic covering both chi-square and binomial offspring
probability needs deliberate coverage of both; equal counts are not required.

Count questions honestly. A new organism name or shuffled choices do not make a new setup.
Several questions using one table can be useful, but identify them as a shared-data set.
Do not pad the list with earlier-topic questions to meet a requested count.

## 3. Read sources for ideas

Start with the books or materials the instructor names. Search for the target skills,
worked examples, exercises, common errors, and useful biological situations. Read the
surrounding passage before adapting an idea. Search hits and tables of contents are leads,
not enough evidence by themselves.

Keep brief source notes:

- Book filename and section, exercise number, or local line number.
- The idea being borrowed: a reasoning task, a comparison, or a biological setting.
- Any damaged formula, unclear assumption, or questionable explanation that needs checking.

Create fresh teaching examples rather than lightly rewording a textbook exercise. Label
invented counts and hypothetical biology. Distinguish a source for the setting from a source
for the statistical task. A book citation does not verify an invented answer.

Do not claim to have read every book when the work consisted of searching the collection and
reading relevant passages. Prefer a few well-supported sources to a long decorative list.

## 4. Build parallel questions

Group candidates by what students do. Within each group, keep the main skill stable while
changing the data or situation enough to require fresh reasoning.

For example, "find exactly k offspring with a trait" could use seedling color, inheritance
of a DNA marker, or offspring sex. Supply the probability for one offspring when deriving
that probability would distract from the binomial task.

Useful changes include:

- Different probabilities and group sizes.
- Counting individual offspring versus pairs or trays.
- Reading a table, a small diagram, or a short experimental record.
- Comparing two experiments instead of calculating one result.
- Finding an error instead of repeating a complete calculation.

Creativity should help the puzzle. Avoid adding unfamiliar biology that students must learn
just to understand the question. A new setup earns its place when it changes what students
must notice or calculate, while preserving the intended learning goal.

Build the data and correct answer first. Then write plausible wrong choices from specific
mistakes, following the pedagogy guide. Write the shortest clear question last.

## 5. Show complete review examples

Use plain, concrete language throughout, including instructor notes. Keep technical terms
when they are part of the lesson, and explain unfamiliar terms when needed. Prefer
"observed minus expected" to "residual" when the simpler phrase communicates the task.

Each candidate must show a complete example, not an outline of possible answers.

```text
### 12. Exactly two white seedlings

Skill practiced: Find the probability of exactly k offspring with a trait.
Adds: More practice with a probability other than 1/2.

Question: Each of six independently produced seedlings has a 1/4 chance of
being white. Which expression gives the probability that exactly two are
white, in any order?

Choices:
A. (1/4)^2 * (3/4)^4
B. 15 * (1/4)^2 * (3/4)^4
C. 15 * (1/4)^4 * (3/4)^2

Correct answer: B.
Why: There are 15 possible positions for the two white seedlings.
A counts only one specified order. C swaps the white and non-white counts.

Book source: Filename, section or exercise, and the idea adapted.
```

The student sees the question and choices. The correct answer, explanation, source, and
development notes are separate instructor material. Avoid unexplained labels such as "key"
and "distractor" in the review document.

Use the response format that fits the task. For numeric entry, show the required units,
precision, correct value, and accepted tolerance instead of inventing choices. For matching,
show both lists and the answer mapping. Do not describe a question as multiple choice without
showing its actual choices.

## 6. Check before delivery

Review the complete list once for scope and coverage, then check each candidate.

| Check | Evidence needed |
| --- | --- |
| Topic fit | The required student action uses a target skill. |
| Coverage | All requested skills receive intentional attention. |
| Added value | The candidate adds practice, a missing task, or a useful extension. |
| Clear task | The question can be understood before reading the choices. |
| Correct answer | Recalculate independently or use a small temporary checking script. |
| Wrong choices | Each reflects an identifiable mistake and is actually wrong. |
| Assumptions | Necessary conditions are stated without giving away the answer. |
| Plain language | Unnecessary terminology and background have been removed. |
| Source accuracy | The cited passage supports the claimed inspiration. |

For statistics, check that the observations, expected counts, and probabilities describe
the same thing. Distinguish exactly from at least, a specified order from any order,
and rejecting a prediction from proving a cause. Check every displayed calculation,
including calculations in wrong choices.

Move earlier-topic ideas out of the main list. Put broader discussion questions in a clearly
marked optional section. Preserve useful ideas without counting them as core candidates.

For a document-only task, use temporary arithmetic and structure checks as needed; permanent
tests are not required. A verified example does not establish that a future randomized
generator or Blackboard rendering works.

## 7. Deliver for selection

Save a local Markdown file when requested. Include:

- A short scope statement and a count of the main candidates by skill.
- A small recommended starting set, chosen for topic fit and added value.
- Complete candidates grouped by skill, with stable question numbers.
- Separate earlier-topic and optional sections only when they contain useful ideas.
- A source list and a short statement of what was checked.

Keep revisions focused on the instructor's feedback. Preserve question numbers when moving
items between sections. Recheck coverage after removing or replacing candidates.

When the request is for candidates, finish with a reviewable candidate file. If implementation
is also requested or already authorized, continue under the authoring guide: build the
generators, vary substantive data with true randomness, verify answers, and review rendered
student questions. Candidate selection, generator correctness, and publication are distinct
results; report only what has actually been completed.

## Reusable request template

```text
Develop [number] candidate questions for [course and topic].
Use [books or other sources] for ideas.

Check the current BPW questions and neighboring topics first. State what
students should practice here and what belongs earlier. Identify useful
gaps, then balance the candidates across the topic's main skills.

Use varied, creative setups that practice the same learning goals.
Supply earlier-topic facts when the goal is to apply them here.
Write in plain language. Show complete questions, actual answer choices
or entry instructions, the correct answer, a short explanation, and sources.

Check topic fit and answers before delivery. Save the candidates to a local
Markdown file, with a recommended starting set and stable question numbers.
Separate earlier-topic ideas and optional discussions from the main list.
```
