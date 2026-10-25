# Genetics Topic 07 candidates

Review draft, revised 2026-10-24. The main list now focuses on **chi-square analysis and
binomial offspring probabilities**. Earlier-topic questions and optional discussion questions
appear separately at the end. Original question numbers are preserved for review.

## What belongs in Topic 07

A question belongs here when students must do at least one of these things:

- Calculate or interpret a chi-square statistic, p-value, or degrees of freedom.
- Choose or check a hypothesis for a statistical test.
- Explain how sample size or a counting mistake affects that test.
- Find the probability of a particular number of offspring with a trait in a group of offspring.

Working out a 3:1, 1:2:1, or 9:7 inheritance ratio by itself belongs in an earlier topic.
For Topic 07, give that ratio or the probability for one offspring, then ask students to
use it in a statistical test or a binomial probability calculation.

## Changes after scope review

- **Main list: 36 questions.** Twenty-seven focus on chi-square; nine focus on binomial
  offspring probabilities, including the retained question 04 and eight new questions, 41-48.
- **Earlier-topic list: eight questions.** Questions 01, 02, 03, 05, 08, 09, 35, and 37 are
  retained below for possible use in Topics 04-05, rather than included in the main list.
- **Optional discussion: four questions.** Questions 34, 36, 39, and 40 concern linkage,
  repeated copies of the same offspring, selective reporting, or possible causes of a result.
  They are not priorities for the core Topic 07 practice list.
- Questions 06 and 10 remain because they ask students to state a statistical hypothesis.
  Their 1:1 prediction is now supplied so students can focus on the test.
- Questions 31-33 remain because they supply the candidate ratios and ask students to compare
  chi-square results. Students do not have to discover the inheritance pattern.

**Suggested first picks:** 11, 12, 14, 19, 23, 25, 26, 31, 41, 42, 45, and 48.

## How to read each question

- **Question** and **Choices** are the proposed student-facing text.
- **Correct answer** identifies the one correct choice.
- **Why** explains the answer and mistakes behind other choices for instructor review.
- **Book source** identifies the passage that inspired the idea; filenames appear at the end.

All example counts are invented for teaching. These are review drafts, not published banks.
Answer letters are not balanced in this draft.

## Calculation rules

For chi-square, add `(observed - expected)^2 / expected` for each group. Use the formula as
written, without a small-sample correction. Unless stated otherwise, alpha = 0.05: reject
when p < 0.05. Alpha is chosen before examining the results; p is calculated from the results.
"Fail to reject" does not mean the prediction has been proved.

For binomial questions, n is the number of offspring, k is the number with the specified trait,
and p is the probability that one offspring has it. Offspring outcomes are independent and p
stays the same for all offspring in the group. Supply those assumptions in the final questions.
The probability of exactly k is `C(n,k) * p^k * (1-p)^(n-k)`; C(n,k) counts the possible
positions of those k offspring. The question must distinguish a specified order from any order.

For all questions, assume equal survival and accurate counting unless the question explicitly
asks about a failure of those conditions. Genetic predictions are chosen before counting.

## Chi-square hypotheses

### 06. The nursery packet label

**Question:** A packet is labeled "offspring of Bb x bb." B produces bitter plants and is dominant
to b. The cross predicts a 1:1 ratio. Which null hypothesis tests the label's prediction?

**Choices:**

- **A.** Every sample contains exactly equal numbers of bitter and non-bitter plants.
- **B.** Each offspring has a 3/4 chance of being bitter.
- **C.** Each offspring has a 1/2 chance of being bitter.

**Correct answer: C.**

**Why:** A Bb x bb cross predicts a 1/2 probability, not exactly equal counts in every sample. A 3/4
probability would fit Bb x Bb.

**Book source:** E, heterozygous purple x white example. Practices choosing a null hypothesis.

### 07. Inheritance of a glowing marker

**Question:** An Rr x rr cross predicts that half the offspring inherit R, a marker that makes them
glow. What is the alternative hypothesis for a chi-square test of this 1:1 prediction?

**Choices:**

- **A.** The chance of inheriting R differs from 1/2.
- **B.** The chance of inheriting R must be greater than 1/2.
- **C.** The chance of inheriting R must be less than 1/2.

**Correct answer: A.**

**Why:** This test looks for a departure in either direction. Either of the other choices leaves out
one possible direction.

**Book source:** B, hypothesis-testing method; C, gene-drive context. Uses an invented glowing
marker.

### 10. The overconfident lab partner

**Question:** Ordinary Mendelian inheritance predicts 1:1 for this cross. An Rr x rr cross produces
58 glowing and 42 dark offspring. A lab partner writes, "The
null hypothesis predicts 58% glowing because that is what we observed." Which prediction should test
ordinary Mendelian inheritance?

**Choices:**

- **A.** 50% glowing and 50% dark
- **B.** 58% glowing and 42% dark
- **C.** 75% glowing and 25% dark

**Correct answer: A.**

**Why:** The cross predicts 1:1 before the offspring are counted. Using the observed percentages as
the prediction guarantees a perfect fit.

**Book source:** E, distinction between a genetic prediction and observed counts.

## Chi-square calculations

### 11. The greenhouse tally

**Question:** A 3:1 prediction gives expected counts of 90 purple and 30 white plants. Observed
counts are 84 purple and 36 white. What is the total chi-square statistic?

**Choices:**

- **A.** 36/90 = 0.400
- **B.** 36/90 + 36/30 = 1.600
- **C.** 36/84 + 36/36 = 1.429

**Correct answer: B.**

**Why:** Square each observed-minus-expected difference, divide by its expected count, and add. A
omits one group; C divides by observed counts.

**Book source:** G, calculation worksheet; E, calculation procedure.

### 12. The rare group matters

**Question:** Four offspring groups have expected counts of 180, 60, 60, and 20. Their observed
counts are 174, 60, 60, and 26. Which group adds the largest amount to the chi-square statistic?

**Choices:**

- **A.** Group 1: expected 180, observed 174
- **B.** Group 4: expected 20, observed 26
- **C.** Groups 1 and 4 add equal amounts.

**Correct answer: B.**

**Why:** Both differences are six, but 36/20 = 1.800 is larger than 36/180 = 0.200. The same
difference matters more when fewer offspring are expected.

**Book source:** B, category-by-category calculation. Compares two terms in the same calculation.

### 13. The perfect cancellation

**Question:** A cross predicts 50 offspring of each type but produces 65 and 35. A spreadsheet adds
+15 and -15 and reports zero. What is the correct chi-square calculation?

**Choices:**

- **A.** (15 - 15)^2/100 = 0.000
- **B.** (15 + 15)/50 = 0.600
- **C.** 15^2/50 + (-15)^2/50 = 9.000

**Correct answer: C.**

**Why:** Square each difference separately before adding. Positive and negative differences should
not cancel; they should not be added without squaring either.

**Book source:** S, problem 7.11 and the check that the differences sum to zero.

### 14. The percentage spreadsheet

**Question:** Among 400 offspring, 220 inherit a marker and 180 do not. The cross predicts 1:1. A
spreadsheet uses percentages, 55 and 45, against 50 and 50. What calculation should use the actual
counts?

**Choices:**

- **A.** 20^2/200 + (-20)^2/200 = 4.000
- **B.** 5^2/50 + (-5)^2/50 = 1.000
- **C.** 20^2/400 + (-20)^2/400 = 2.000

**Correct answer: A.**

**Why:** Each expected count is 200. B uses percentages and loses the sample size; C divides each
term by the total rather than that group's expected count.

**Book source:** E, warning about percentages; S, chi-square limitations.

### 15. The erased table cell

**Question:** Expected counts are 40, 80, and 40. Observed counts are 36, blank, and 44, totaling
160. What is the total chi-square statistic?

**Choices:**

- **A.** 0.400
- **B.** 0.800
- **C.** 1.600

**Correct answer: B.**

**Why:** The missing count is 80. The three terms are 16/40, 0/80, and 16/40. A omits one nonzero
term; C doubles the correct sum.

**Book source:** E, summing contributions; S, observed and expected totals must agree.

## Degrees of freedom

### 16. Three genotypes, two appearances

**Question:** An Aa plant self-fertilizes. Students record only dominant versus recessive
appearance, then test a 3:1 prediction. How many degrees of freedom does this test have?

**Choices:**

- **A.** 1
- **B.** 2
- **C.** 3

**Correct answer: A.**

**Why:** There are two recorded groups, so degrees of freedom = 2 - 1. Counting AA and Aa separately
would count information that was not recorded.

**Book source:** E, degrees-of-freedom explanation; K, section 3.8.

### 17. A DNA test adds information

**Question:** An Aa plant self-fertilizes. A DNA test distinguishes AA, Aa, and aa offspring. How
many degrees of freedom does a test of the predicted 1:2:1 ratio have?

**Choices:**

- **A.** 1
- **B.** 2
- **C.** 3

**Correct answer: B.**

**Why:** There are three recorded groups, so degrees of freedom = 3 - 1. Unlike question 16, AA and
Aa can now be told apart.

**Book source:** E and K, category-based degrees of freedom; invented DNA-test setting.

### 18. Eight marker combinations

**Question:** An AaBbDd x aabbdd cross produces eight distinguishable offspring groups. The genes
assort independently, so each group is predicted at 1/8. How many degrees of freedom does the test
have?

**Choices:**

- **A.** 3
- **B.** 7
- **C.** 8

**Correct answer: B.**

**Why:** There are eight groups, giving 8 - 1 = 7 degrees of freedom. A counts genes; C forgets to
subtract one.

**Book source:** S, problem 7.30, trihybrid testcross.

### 19. The empty offspring group

**Question:** Four offspring groups each have expected count 20. Observed counts are 38, 22, 20, and
0. How many degrees of freedom does the test have?

**Choices:**

- **A.** 2
- **B.** 3
- **C.** 4

**Correct answer: B.**

**Why:** All four groups still belong in the test, including the group with zero observed offspring.
Its expected count is positive. Thus df = 4 - 1.

**Book source:** E, category definition. Original application of the rule.

### 20. The four-seed trays

**Question:** Each of 320 trays contains four seedlings. Each seedling independently has a 1/2
chance of glowing. Trays are grouped by glowing count: 0, 1, 2, 3, or 4. How many degrees of freedom
does a test of the predicted tray counts have?

**Choices:**

- **A.** 1
- **B.** 4
- **C.** 5

**Correct answer: B.**

**Why:** The observations are trays, sorted into five groups, so df = 5 - 1. Counting only glowing
versus dark seedlings answers a different question.

**Book source:** S, problem 7.14.

## Chi-square conclusions

### 21. The glowing marker passed the test

**Question:** A test of 1:1 inheritance gives p = 0.31. At alpha = 0.05, which conclusion is
justified?

**Choices:**

- **A.** Reject 1:1 inheritance.
- **B.** Fail to reject 1:1 inheritance.
- **C.** Conclude that 1:1 inheritance is proved.

**Correct answer: B.**

**Why:** Since 0.31 is greater than 0.05, the test does not reject 1:1. That does not prove the
prediction is correct.

**Book source:** K, interpretation of probability values; E, goodness-of-fit interpretation.

### 22. The pigment prediction fails

**Question:** An experiment tests a 9:7 pigment prediction and obtains p = 0.004. Which conclusion
follows at alpha = 0.05?

**Choices:**

- **A.** Reject the 9:7 prediction.
- **B.** Fail to reject the 9:7 prediction.
- **C.** Conclude that a 3:1 prediction is proved.

**Correct answer: A.**

**Why:** Since 0.004 is below 0.05, reject 9:7. This result alone does not establish which other
prediction is correct.

**Book source:** S, complementary-gene example; K, rejection interpretation.

### 23. Same statistic, different table row

**Question:** A two-group test and a four-group test each give chi-square = 6.000. At alpha = 0.05,
the critical values are 3.841 for df = 1 and 7.815 for df = 3. Which test rejects its null
hypothesis?

**Choices:**

- **A.** Both tests
- **B.** Only the two-group test
- **C.** Only the four-group test
- **D.** Neither test

**Correct answer: B.**

**Why:** Six exceeds 3.841 but not 7.815. The same statistic can lead to different decisions when
the number of groups differs.

**Book source:** K, section 3.8; E, curves for different degrees of freedom.

### 24. Two significance cutoffs

**Question:** The same cross gives p = 0.032. Two researchers chose their cutoffs before collecting
data: alpha = 0.05 and alpha = 0.01. What decisions follow?

**Choices:**

- **A.** Reject at both cutoffs.
- **B.** Reject at 0.05; fail to reject at 0.01.
- **C.** Fail to reject at 0.05; reject at 0.01.
- **D.** Fail to reject at both cutoffs.

**Correct answer: B.**

**Why:** The p-value lies between the two cutoffs. Changing the cutoff changes the decision, not the
data or the p-value.

**Book source:** K, significance-threshold discussion and associated exercise.

### 25. What does eight percent mean?

**Question:** A chi-square test gives p = 0.08. Which statement explains this result correctly?

**Choices:**

- **A.** The null hypothesis has an 8% chance of being true.
- **B.** Exactly these offspring counts have an 8% chance of occurring.
- **C.** If the null hypothesis and test assumptions hold, a chi-square statistic this large or
  larger has an 8% chance of occurring.

**Correct answer: C.**

**Why:** The p-value concerns how far results depart from the prediction, assuming that prediction
is correct. It is not the probability that the prediction itself is true.

**Book source:** E, example with chi-square = 3.00; K, p-value interpretation.

## Sample size and chi-square

### 26. The greenhouse expansion

**Question:** A 1:1 cross produces 24:16 offspring in a small study and 240:160 in a separate larger
study. Which gives the larger chi-square statistic?

**Choices:**

- **A.** The smaller study
- **B.** The larger study
- **C.** Both give the same statistic.

**Correct answer: B.**

**Why:** The statistics are 1.600 and 16.000. With the same percentages, ten times as many offspring
gives ten times the statistic.

**Book source:** S, problems 7.11 and 7.31; K, chance deviation and sample size.

### 27. Ten extra seedlings

**Question:** Two studies test a 1:1 prediction. Study A observes 60:40; study B observes 510:490.
Both have ten extra offspring of the first type. Which gives the larger chi-square statistic?

**Choices:**

- **A.** Study A
- **B.** Study B
- **C.** Both give the same statistic.

**Correct answer: A.**

**Why:** The statistics are 4.000 and 0.400. Ten extra offspring is a larger difference relative to
50 expected than to 500 expected.

**Book source:** S, sample-size comparison principle; original paired data.

### 28. Matching percentages, hidden totals

**Question:** Two reports show 60% versus 40% for a predicted 1:1 ratio, but give no sample sizes.
What can you conclude about their chi-square statistics?

**Choices:**

- **A.** They must be equal because the percentages match.
- **B.** They must both exceed the rejection cutoff.
- **C.** They cannot be compared without the sample sizes.

**Correct answer: C.**

**Why:** Chi-square uses counts. Matching percentages can give different statistics when the numbers
of offspring differ.

**Book source:** E, count requirement; S, problem 7.11.

### 29. Opposite greenhouse results

**Question:** Two separate crosses each predict 1:1. Their counts are 70:30 and 30:70. A researcher
combines them into 100:100 and reports a perfect fit. What does combining the counts hide?

**Choices:**

- **A.** Both individual crosses depart from 1:1, in opposite directions.
- **B.** Both individual crosses fit 1:1 exactly.
- **C.** Only the first cross departs from 1:1.

**Correct answer: A.**

**Why:** Each separate cross gives chi-square = 16.000. Combining the counts cancels the differences
and hides the pattern between crosses.

**Book source:** S, replicated-cross exercises; original opposing-deviation setup.

### 30. A small but detectable difference

**Question:** Of 10,000 offspring, 5,200 inherit a marker and 4,800 do not. The 1:1 test gives
chi-square = 16.000 and rejects the prediction. Which statement correctly describes the result?

**Choices:**

- **A.** Inheritance was 52%, two percentage points above 50%; the test does not establish
  biological importance.
- **B.** Inheritance was 52%, so it was 52 percentage points above the prediction.
- **C.** Rejecting 1:1 establishes that the difference is biologically important.

**Correct answer: A.**

**Why:** A large sample can detect a small difference. Deciding whether that difference matters
biologically requires more than the test result.

**Book source:** S, sample-size principle; original interpretation extension.

## Comparing predictions with chi-square

### 31. The survivor-ratio contest

**Question:** A hypothetical cross produces 120 short-winged and 60 normal-winged survivors. Two
predictions were chosen before counting: 3:1 and 2:1. Their chi-square statistics are 6.667 and
0.000. The rejection cutoff is 3.841. Which prediction is rejected?

**Choices:**

- **A.** Only 3:1
- **B.** Only 2:1
- **C.** Both
- **D.** Neither

**Correct answer: A.**

**Why:** Only 6.667 exceeds the cutoff. A 2:1 fit is consistent with loss of one genotype before
hatching, but does not prove that explanation.

**Book source:** S, problem 7.33. Compare models rather than merely calculating one statistic.

### 32. One pigment gene or two?

**Question:** A hypothetical cross produces 94 pigmented and 66 unpigmented plants. Two predictions
chosen before counting give these statistics: 3:1 gives 22.533; 9:7 gives 0.406. The rejection
cutoff is 3.841. Which prediction is rejected?

**Choices:**

- **A.** Only 3:1
- **B.** Only 9:7
- **C.** Both
- **D.** Neither

**Correct answer: A.**

**Why:** The 3:1 statistic exceeds the cutoff; the 9:7 statistic does not. This compares the
predictions without requiring students to memorize the underlying pigment pathways.

**Book source:** S, problems 7.37-7.38; H, complementary gene action.

### 33. Both explanations remain possible

**Question:** A cross produces 74 dominant-looking and 22 recessive-looking offspring. Two
predictions chosen before counting give these statistics: 3:1 gives 0.222; 13:3 gives 1.094. The
rejection cutoff is 3.841. Which conclusion follows?

**Choices:**

- **A.** The 3:1 prediction is proved because its statistic is smaller.
- **B.** The 13:3 prediction is rejected because its statistic is larger.
- **C.** Neither prediction is rejected.

**Correct answer: C.**

**Why:** Both statistics are below the cutoff. A smaller statistic does not prove that one
explanation is correct.

**Book source:** S, problem 7.38. Shows why neither explanation can be ruled out by this test.

## Checking expected counts

### 38. Too few rare offspring

**Question:** A 9:3:3:1 prediction is tested with 32 offspring. For this exercise, use the rule that
each expected count must be at least five. Which expected group is too small?

**Choices:**

- **A.** The 9/16 group
- **B.** Either 3/16 group
- **C.** The 1/16 group

**Correct answer: C.**

**Why:** Expected counts are 18, 6, 6, and 2. Only the last is below five. A total of at least 80
would meet this exercise's rule for all four groups.

**Book source:** S, chi-square limitations. The minimum-count rule is stated for this exercise.

## Binomial offspring probabilities

### 04. Pairs of glowing seedlings

**Question:** Each seedling from an Rr x rr cross has a 1/2 chance of glowing, independently of the
others. The class sorts 200 pairs by whether neither, one, or both seedlings glow. What pair counts
are expected, in that order?

**Choices:**

- **A.** 50, 50, 100
- **B.** 50, 100, 50
- **C.** 100, 200, 100

**Correct answer: B.**

**Why:** The pair probabilities are 1/4, 1/2, and 1/4. Either seedling can be the one that glows.
The last choice counts 400 pairs when there are only 200.

**Book source:** S, problem 7.34; K, binomial theorem. Connects pair probabilities to expected
counts.

### 41. Exactly two white seedlings

**Question:** Each offspring has a 1/4 chance of being white. For six independently produced
seedlings, which expression gives the probability that exactly two are white, in any order?

**Choices:**

- **A.** (1/4)^2 * (3/4)^4
- **B.** 15 * (1/4)^2 * (3/4)^4
- **C.** 15 * (1/4)^4 * (3/4)^2

**Correct answer: B.**

**Why:** There are C(6,2) = 15 ways to place the two white seedlings among six. A gives one
specified order; C swaps the white and non-white counts. The probability is about 29.663%.

**Book source:** S, chapter 7 binomial offspring exercises; H, section 4.5. Original seedling
example.

### 42. At least one glowing offspring

**Question:** Each of five independently produced offspring has a 1/2 chance of glowing. What is the
probability that at least one glows?

**Choices:**

- **A.** (1/2)^5 = 3.125%
- **B.** 1 - (1/2)^5 = 96.875%
- **C.** 5 * (1/2)^5 = 15.625%

**Correct answer: B.**

**Why:** Subtract the probability that none glow from one. A gives the probability of none; C gives
the probability of exactly one.

**Book source:** H, section 4.5 and problem 4.15; original glowing-offspring example.

### 43. One order or any order?

**Question:** Each offspring independently has a 1/4 chance of being white. A gardener plants four
seeds in numbered pots. Compare event 1: only pot 1 has a white seedling; event 2: exactly one pot
has a white seedling, whichever pot it is. How do their probabilities compare?

**Choices:**

- **A.** Event 2 is four times as likely.
- **B.** Both are equally likely.
- **C.** Event 1 is four times as likely.

**Correct answer: A.**

**Why:** Event 1 has probability (1/4)(3/4)^3. Event 2 includes four possible positions for the
white seedling, each with that probability.

**Book source:** S, chapter 7 binomial review, specified versus unspecified offspring order; K,
binomial theorem.

### 44. Which number is most likely?

**Question:** Each of four independently produced offspring has a 1/4 chance of showing a recessive
trait. The probabilities of 0, 1, 2, 3, or 4 showing it are 31.641%, 42.188%, 21.094%, 4.688%, and
0.391%. Which count is most likely?

**Choices:**

- **A.** Zero offspring
- **B.** One offspring
- **C.** Two offspring
- **D.** Four offspring

**Correct answer: B.**

**Why:** Exactly one has the largest probability. The expected count is also one here, but that does
not mean every group of four contains exactly one.

**Book source:** S, chapter 7 binomial offspring exercises; original table using p = 1/4.

### 45. Exactly two or three carriers

**Question:** Each of five independently produced offspring has a 1/2 chance of carrying a marked
allele. The probability of exactly two carriers is 10/32; exactly three is also 10/32. What is the
probability of two OR three carriers?

**Choices:**

- **A.** (10/32) * (10/32) = 9.766%
- **B.** 10/32 = 31.250%
- **C.** 10/32 + 10/32 = 62.500%

**Correct answer: C.**

**Why:** Add the probabilities because the same group cannot have both exactly two and exactly three
carriers. Multiplication would answer a different question about separate events.

**Book source:** H, section 4.5 and worked problem 2; original carrier example.

### 46. At least two white seedlings

**Question:** Each of four independently produced seedlings has a 1/4 chance of being white. P(none
white) = 81/256 and P(exactly one white) = 108/256. What is P(at least two white)?

**Choices:**

- **A.** 1 - 81/256 = 68.359%
- **B.** 1 - 81/256 - 108/256 = 26.172%
- **C.** 54/256 = 21.094%

**Correct answer: B.**

**Why:** Exclude both zero and one. A includes exactly one; C counts exactly two but leaves out
three and four.

**Book source:** S, chapter 7 exercises on three or more offspring; H, section 4.5. Original
seedling example.

### 47. The next offspring after a streak

**Question:** Each offspring independently has a 1/4 chance of being white. The first five are all
non-white. What is the probability that the next two offspring are both white?

**Choices:**

- **A.** (1/4)^2 = 6.250%
- **B.** (3/4)^5 * (1/4)^2 = 1.483%
- **C.** 1/4 = 25.000%

**Correct answer: A.**

**Why:** The first five outcomes are already known. Independence leaves the probability for the next
two at (1/4)^2. B instead calculates the probability of the entire seven-offspring sequence before
any are observed.

**Book source:** H, section 4.5, independence of successive offspring; original sequence example.

### 48. From offspring probability to tray counts

**Question:** Each tray contains four independently produced seedlings, each with a 1/4 chance of
being white. The probability that a tray has exactly two white seedlings is 54/256. Among 256 such
trays, how many are expected to have exactly two white seedlings?

**Choices:**

- **A.** 2 trays
- **B.** 54 trays
- **C.** 64 trays

**Correct answer: B.**

**Why:** Multiply the number of trays by the probability for a tray: 256 * 54/256 = 54. A confuses
seedlings with trays; C uses the probability for one seedling. These expected tray counts could then
be compared with observed counts in a chi-square question.

**Book source:** S, problem 7.14, binomial probabilities converted to group counts; original tray
example.

## Better suited to earlier topics

These questions are preserved for possible reuse. They are not part of the main Topic 07 list.
The suggested destinations follow the current local BPW topic names.

| Question | Suggested topic | Reason |
| --- | --- | --- |
| 01 | 04: Mendelian Genetics | Converts a supplied 3:1 ratio into counts, without a statistical test. |
| 02 | 05: Gene Interactions | Works out the ratio after a lethal genotype is removed. |
| 03 | 05: Gene Interactions | Works out the 1:2:1 ratio for three visible phenotypes. |
| 05 | 04: Mendelian Genetics | Works out the four testcross outcomes. |
| 08 | 05: Gene Interactions | Works out a survivor ratio; calling it a null hypothesis does not change the main task. |
| 09 | 05: Gene Interactions | Works out a 9:7 ratio from a pigment pathway. |
| 35 | 04: Mendelian Genetics | Recognizes the ratio for a testcross. |
| 37 | 05: Gene Interactions | Explains how unequal survival changes an offspring ratio. |

### 01. The bitter seed packet

**Question:** A hypothetical cross predicts 3 bitter plants for every 1 non-bitter plant. A class
counts 120 plants. What numbers should they expect?

**Choices:**

- **A.** 30 bitter and 90 non-bitter
- **B.** 60 bitter and 60 non-bitter
- **C.** 90 bitter and 30 non-bitter

**Correct answer: C.**

**Why:** Three-fourths of 120 is 90; one-fourth is 30. The other choices reverse the ratio or use
equal numbers.

**Book source:** G, bitter-plant investigation. Practices expected counts, as the dice questions do.

### 02. The missing seedling genotype

**Question:** A hypothetical Dd plant self-fertilizes. DD embryos die before germination; Dd
seedlings are dwarf and dd seedlings are tall. Among 180 surviving seedlings, how many of each type
are expected?

**Choices:**

- **A.** 90 dwarf and 90 tall
- **B.** 120 dwarf and 60 tall
- **C.** 135 dwarf and 45 tall

**Correct answer: B.**

**Why:** The surviving genotypes are Dd, Dd, and dd: two dwarf for every one tall. The 135:45 choice
incorrectly keeps the usual 3:1 ratio.

**Book source:** S, problem 7.33; H, lethal-allele discussion. Focuses on counting survivors.

### 03. Sorting glowing seedlings

**Question:** In a hypothetical plant, RR seedlings glow brightly, Rr seedlings glow dimly, and rr
seedlings do not glow. An Rr x Rr cross produces 240 seedlings. What counts are expected?

**Choices:**

- **A.** 60 bright, 120 dim, 60 dark
- **B.** 80 bright, 80 dim, 80 dark
- **C.** 120 bright, 60 dim, 60 dark

**Correct answer: A.**

**Why:** The genotype ratio is 1:2:1. Equal thirds ignores the two ways to inherit Rr; the last
choice gives the largest group to RR.

**Book source:** S, problem 7.32; H, incomplete dominance. Uses three visible groups.

### 05. The seed orchard cross

**Question:** Two genes assort independently in an AaBb x aabb cross. A DNA test distinguishes AaBb,
Aabb, aaBb, and aabb seedlings. Among 320 seedlings, what counts are expected in that order?

**Choices:**

- **A.** 80, 80, 80, 80
- **B.** 180, 60, 60, 20
- **C.** 160, 80, 40, 40

**Correct answer: A.**

**Why:** Each genotype has probability 1/4. The 9:3:3:1 counts belong to a different cross: AaBb x
AaBb.

**Book source:** F, transmission and marker examples; B, testcross exercise E10.

### 08. The disappearing genotype

**Question:** In a hypothetical Dd x Dd cross, DD embryos die before hatching, Dd hatchlings have
short wings, and dd hatchlings have normal wings. Which expected ratio should be tested among
hatchlings?

**Choices:**

- **A.** 1 short-winged : 1 normal-winged
- **B.** 2 short-winged : 1 normal-winged
- **C.** 3 short-winged : 1 normal-winged

**Correct answer: B.**

**Why:** After DD embryos are excluded, two Dd offspring remain for every dd offspring. The usual
3:1 ratio includes DD in the dominant group even though it does not survive.

**Book source:** S, problem 7.33. Like 02, but asks for a ratio instead of counts.

### 09. The two-step pigment pathway

**Question:** A hypothetical plant makes pigment only when it has at least one A allele AND at least
one B allele. The genes assort independently. AaBb plants self-fertilize. What pigment ratio is
expected?

**Choices:**

- **A.** 3 pigmented : 1 unpigmented
- **B.** 1 pigmented : 1 unpigmented
- **C.** 9 pigmented : 7 unpigmented

**Correct answer: C.**

**Why:** The chance of A_B_ is (3/4)(3/4) = 9/16. All other offspring lack pigment. A 3:1 ratio
treats the trait as if only one gene mattered.

**Book source:** S, problem 7.37; H, complementary pigment genes.

### 35. The wrong cross on the worksheet

**Question:** A technician records an AaBb x aabb cross with independently assorting genes, but
calculates expected counts using 9:3:3:1. What should be corrected first?

**Choices:**

- **A.** Keep 9:3:3:1 but change the degrees of freedom.
- **B.** Replace 9:3:3:1 with 1:1:1:1.
- **C.** Replace the expected counts with the observed counts.

**Correct answer: B.**

**Why:** The cross predicts four equally likely groups. Changing degrees of freedom does not repair
a wrong prediction; using observed counts guarantees a perfect fit.

**Book source:** B, testcross exercise E10; P, testing a genetic hypothesis.

### 37. The missing white seedlings

**Question:** A cross predicts 3 green seedlings for every 1 white seedling at germination. White
seedlings die sooner. Students count only survivors weeks later and test them against 3:1. What is
the problem?

**Choices:**

- **A.** The prediction must describe the survivors, or the seedlings must be counted before the
  deaths.
- **B.** The survivors must still have the same expected 3:1 ratio.
- **C.** Any departure from 3:1 proves that the parents had the wrong genotypes.

**Correct answer: A.**

**Why:** Unequal survival can change the ratio after germination. A count taken later does not
directly test the original ratio at germination.

**Book source:** S, lethal-genotype problem; G, scoring a plant sample.

## Optional discussion questions

These can support later discussion but are not priorities for routine Topic 07 practice.
Question 34 also connects to Topic 08: Gene Mapping. Questions 36, 39, and 40 ask broader
questions about how experiments are done and what their results can establish.

### 34. Each trait passes, the pair fails

**Question:** An AaBb x aabb cross gives AaBb, Aabb, aaBb, and aabb offspring counts of 90, 10, 10,
and 90. All types survive equally and are counted correctly. Each gene separately gives a 100:100
ratio. Do these separate checks establish independent assortment?

**Choices:**

- **A.** Yes; two separate 1:1 ratios establish independent assortment.
- **B.** No; the four combined groups differ sharply from 50:50:50:50.
- **C.** No; each gene separately differs sharply from 1:1.

**Correct answer: B.**

**Why:** Each gene separately fits 1:1, but the four-group statistic is 128.000. The excess of AaBb
and aabb offspring is consistent with the genes being linked.

**Book source:** S, problem 7.41. Would work well as a four-cell table.

### 36. The copied seedling labels

**Question:** A nursery grows 20 seedlings from separate seeds, then makes ten genetically identical
cuttings from each. A report treats the 200 cuttings as 200 separate results of inheritance. What is
wrong with that count?

**Choices:**

- **A.** Each cutting repeats the inherited genotype of its original seedling.
- **B.** Each cutting represents a new fertilization.
- **C.** Taking cuttings changes a 3:1 inheritance prediction into 1:1.

**Correct answer: A.**

**Why:** The 200 cuttings represent only 20 separate seed-grown offspring. Copying a seedling does
not provide another independent result of the cross.

**Book source:** F, tree inheritance setting; K, independent-event reasoning. The counting problem
is an original example.

### 39. The conveniently perfect notebook

**Question:** A lab repeats every cross whose ratio looks unusual and keeps only the replacement
results. The notebook shows unusually close agreement with the predicted ratios. What explains this
pattern?

**Choices:**

- **A.** Keeping only replacement results can remove ordinary chance differences from the record.
- **B.** Repeating a cross changes the inheritance rule.
- **C.** Close agreement proves that all original counts were accurate.

**Correct answer: A.**

**Why:** Choosing which results to keep changes the record. This fictional example illustrates
biased reporting; a high p-value alone does not show that anyone altered data.

**Book source:** H, discussion of unusually good fits; D, historical debate about Mendel's data.

### 40. Does the marker prove gene drive?

**Question:** In a hypothetical Rr x rr cross, 160 offspring inherit R and 40 do not. A test rejects
1:1 inheritance. Gene drive can make an allele pass to more than half the offspring. Does this
result alone prove gene drive?

**Choices:**

- **A.** Yes; any rejection of 1:1 proves gene drive.
- **B.** No; unequal survival or counting errors could also change the observed ratio.
- **C.** No; gene drive must leave exactly half the offspring with R.

**Correct answer: B.**

**Why:** The test shows disagreement with 1:1 but does not identify its cause. Counting genotypes
before deaths occur could help check the survival explanation.

**Book source:** C, inheritance above the usual 1/2 probability; K, limits of hypothesis-test
conclusions.

## Books and passages

Primary folder: `/Users/vosslab/nsh/MARKDOWN_BOOKS/inheritance_genetics/`.
Line numbers refer to the local Markdown files as inspected on 2026-10-24. Searchable section
names and problem numbers are included because extraction and later cleanup can change lines.
The review searched the supplied collections and read relevant passages, not every book cover
to cover. The inheritance collection provides the main pedagogical sources.

| Code | Local book filename | Relevant passage |
| --- | --- | --- |
| S | `Schaum_s_Outline_of_Theory_and_Problems_of_Genetics_Third_Edition-1991.md` | Chi-square limitations, line 3823; chapter 7 problems 7.11, 7.14, 7.30-7.42; lethal example 7.33 at line 4021; marginal versus joint tests 7.41 at line 4049. |
| E | `Essential_Genetics_and_Genomics-2020.md` | "Chi-square tests goodness of fit of observed to expected numbers," lines 3362-3412; count versus percentage warning, line 3388. |
| K | `Concepts_of_Genetics-Klug_Cummings_Spencer_Palladino-2012.md` | Sections 3.7-3.8; chance variation, line 1185; degrees of freedom, line 1232; p-value interpretation, line 1249; threshold exercise near line 1426. |
| B | `Concepts_of_Genetics-Brooker-2012.md` | Chapter 3 hypothesis-testing procedure, lines 902-907; testcross exercise E10, line 986. |
| P | `Genetics_A_Conceptual_Approach-Pierce-2012.md` | Goodness-of-fit discussion, lines 1019-1036; worked genetic-hypothesis analysis near line 1036. |
| G | `Garden_Genetics-2006.md` | Bitter/non-bitter investigation and expected-count worksheet, lines 260-304; repeated student material near lines 1468-1479. |
| F | `Forest_Genetics-White_Adams_Neale-2007.md` | Transmission of chromosomes, cone-color goodness-of-fit example, lines 165-175; marker segregation example near line 199. |

Supplementary sources from the initially supplied collections:

| Code | Folder and filename | Relevant passage |
| --- | --- | --- |
| H | `genetics/Genetics_Analysis_of_Genes_and_Genomes-2019.md` | Incomplete dominance and epistasis, lines 1505-1523; lethal chicken example near line 1657; sections 4.5-4.6, lines 1876-1928. |
| C | `genetics_history/A_Crack_in_Creation_Gene_Editing_and_the_Unthinkable_Power_to_Control_Evolution-2017.md` | Gene drives and biased inheritance, lines 1048-1058; used only as context for hypothetical teaching experiments. |
| D | `genetics_history/Disputed_Inheritance-2023.md` | Historical interpretation of unusually close fits, lines 1112 and 2249; used to motivate a fictional reporting-bias puzzle. |

Supplementary paths are relative to `/Users/vosslab/nsh/MARKDOWN_BOOKS/`.
Some extracted books contain damaged formulas or imprecise statistical phrasing. The answers use the
chi-square formula and p-value meaning described above.
