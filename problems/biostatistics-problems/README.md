# Biostatistics problem generators

These Python generators create Blackboard statistics questions. Spreadsheet assignments assess tutorial completion: students enter fresh data into their completed tutorial spreadsheets and submit one numeric result.

## Generator families

| Family | Scripts | Answer |
| --- | --- | --- |
| Descriptive statistics | `descriptive_stats_google_sheet.py`, `measures_of_center.py` | Multiple blanks, matching, or multiple choice |
| Z-scores | `z_score_google_sheet.py`, `z_score_table_interp.py` | Multiple choice |
| Hypotheses | `null_and_alternative_hypotheses.py`, `hypothesis_statement_errors.py` | Multiple choice |
| Boxplots | `boxplot_from_*.py` | Multiple choice |
| Baby weights | `babies_one_sample_z_test.py`, `babies_one_sample_t_test.py`, `babies_two_sample_t_test.py` | Numeric p-value |
| Busse Woods diversity | `busse_woods_one_sample_tests.py`, `busse_woods_two_sample_t_test.py`, `busse_woods_two_sample_f_test.py`, `busse_woods_anova.py` | Numeric p-value |
| Dr. Caffeine regression | `dr_caffeine_linear_regression.py`, `dr_caffeine_quadratic_regression.py` | Numeric R-squared |

## Run a generator

Run from the repository root:

```bash
source source_me.sh
python3 problems/biostatistics-problems/dr_caffeine_linear_regression.py -d 5
python3 problems/biostatistics-problems/dr_caffeine_quadratic_regression.py -d 5
```

Each command writes a `bbq-*.txt` bank in the current directory. Use `--help` for
shared options, including `-B` for Blackboard export. Generated question banks
stay out of Git.

## Spreadsheet assignments

Students reuse the spreadsheet they completed during the corresponding tutorial.
They replace the old observations with each question's data and report the requested
numeric result. Sample sizes follow each generator's worksheet requirements;
Busse Woods assignments do not require the tutorial's original sample size.

Tables provide a readable view. The separate comma-separated text remains copyable
when Blackboard export converts a table to an image. Copy only the data rows, paste
into the corresponding data columns, and split text using the comma separator.

When authoring copyable data, include only the columns needed for the calculation.
For a single numeric variable, use one number per line with no header or commas so
students can paste directly into Google Sheets. For example, a one-sample Busse Woods
test needs `4.32`, not `Parking Lot,4.32`; location names can stay in the display table.
Keep separators when multiple numeric columns are needed, as with paired sleep and
exam-score data. This is guidance for future edits; existing generators are unchanged.

## Dr. Caffeine workflow

The three lessons and student workbook are in the `dr_caffeine_regression/` folder.
Complete the relevant tutorial before using its assignment generator.

| Task | Completed worksheet | Report |
| --- | --- | --- |
| Linear regression | Linear Regression | Linear model R-squared |
| Quadratic regression | Quadratic Regression | Quadratic model R-squared |

Both generators supply 25 paired observations. Replace the old sleep and exam-score
data in the corresponding analysis worksheet and follow the completed tutorial workflow.
Prompts identify the data and result by their labels so they do not depend on cell positions.

Fresh samples can have either slope direction or either curvature sign. Do not reuse
the tutorial's numerical answers. Report R-squared as a decimal between 0 and 1,
using at least three decimal places. Grading allows an absolute tolerance of 0.001.
The tutorial's p-value calculations remain available but are not graded here.

These assignments check completion of the tutorial workflow. Interpretation of
R-squared and comparisons between models remain in the tutorials.

The supplied workbook is an uncompleted template, not an answer workbook. New
generators use the existing NumPy dependency; they do not create spreadsheets.

For repository setup and export details, see [../../docs/INSTALL.md](../../docs/INSTALL.md)
and [../../docs/USAGE.md](../../docs/USAGE.md).
