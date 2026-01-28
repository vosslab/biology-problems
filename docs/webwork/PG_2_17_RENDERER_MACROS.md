# PG 2.17 Renderer Macro Inventory

This document records the available macro files in the local PG 2.17 renderer
snapshot used by this repo. The renderer uses a trimmed, flattened PG tree, so
macro availability differs from a full PG checkout. Treat this list as the
allowlist for `loadMacros(...)` in renderer and ADAPT contexts.

Notes:

- The renderer snapshot reports PG 2.17 in `lib/PG/VERSION`, but the macro tree
  is flattened and some subdirectories/files are missing.
- `conf/pg_config.yml` still references `macros/math` and `macros/parsers`, but
  those subdirectories do not exist in the renderer snapshot.
- Examples of missing macros include `parserCheckboxList.pl` and
  `VectorListCheckers.pl`.

## How to refresh

Run this in `/Users/vosslab/nsh/webwork-pg-renderer` and replace the list below:

```
find lib/PG/macros/ | sort
```

## Renderer macro list (snapshot from 2026-01-28)

```
lib/PG/macros/
lib/PG/macros/alignedChoice.pl
lib/PG/macros/answerComposition.pl
lib/PG/macros/answerCustom.pl
lib/PG/macros/answerDiscussion.pl
lib/PG/macros/answerHints.pl
lib/PG/macros/answerVariableList.pl
lib/PG/macros/AppletObjects.pl
lib/PG/macros/bizarroArithmetic.pl
lib/PG/macros/CanvasObject.pl
lib/PG/macros/compoundProblem.pl
lib/PG/macros/compoundProblem2.pl
lib/PG/macros/compoundProblem5.pl
lib/PG/macros/contextABCD.pl
lib/PG/macros/contextAlternateDecimal.pl
lib/PG/macros/contextAlternateIntervals.pl
lib/PG/macros/contextArbitraryString.pl
lib/PG/macros/contextComplexExtras.pl
lib/PG/macros/contextComplexJ.pl
lib/PG/macros/contextCongruence.pl
lib/PG/macros/contextCurrency.pl
lib/PG/macros/contextFraction.pl
lib/PG/macros/contextInequalities.pl
lib/PG/macros/contextInequalitySetBuilder.pl
lib/PG/macros/contextInteger.pl
lib/PG/macros/contextIntegerFunctions.pl
lib/PG/macros/contextLeadingZero.pl
lib/PG/macros/contextLimitedComplex.pl
lib/PG/macros/contextLimitedFactor.pl
lib/PG/macros/contextLimitedNumeric.pl
lib/PG/macros/contextLimitedPoint.pl
lib/PG/macros/contextLimitedPolynomial.pl
lib/PG/macros/contextLimitedPowers.pl
lib/PG/macros/contextLimitedRadical.pl
lib/PG/macros/contextLimitedVector.pl
lib/PG/macros/contextMatrixExtras.pl
lib/PG/macros/contextOrdering.pl
lib/PG/macros/contextPartition.pl
lib/PG/macros/contextPercent.pl
lib/PG/macros/contextPeriodic.pl
lib/PG/macros/contextPermutation.pl
lib/PG/macros/contextPermutationUBC.pl
lib/PG/macros/contextPiecewiseFunction.pl
lib/PG/macros/contextPolynomialFactors.pl
lib/PG/macros/contextRationalFunction.pl
lib/PG/macros/contextReaction.pl
lib/PG/macros/contextScientificNotation.pl
lib/PG/macros/contextString.pl
lib/PG/macros/contextTF.pl
lib/PG/macros/contextTrigDegrees.pl
lib/PG/macros/contextTypeset.pl
lib/PG/macros/customizeLaTeX.pl
lib/PG/macros/draggableProof.pl
lib/PG/macros/draggableSubsets.pl
lib/PG/macros/extraAnswerEvaluators.pl
lib/PG/macros/LinearProgramming.pl
lib/PG/macros/LiveGraphics3D.pl
lib/PG/macros/MathObjects.pl
lib/PG/macros/MatrixCheckers.pl
lib/PG/macros/MatrixReduce.pl
lib/PG/macros/MatrixUnits.pl
lib/PG/macros/niceTables.pl
lib/PG/macros/Parser.pl
lib/PG/macros/parserAssignment.pl
lib/PG/macros/parserAutoStrings.pl
lib/PG/macros/parserCustomization.pl
lib/PG/macros/parserDifferenceQuotient.pl
lib/PG/macros/parserFormulaAnyVar.pl
lib/PG/macros/parserFormulaUpToConstant.pl
lib/PG/macros/parserFormulaWithUnits.pl
lib/PG/macros/parserFunction.pl
lib/PG/macros/parserFunctionPrime.pl
lib/PG/macros/parserGraphTool.pl
lib/PG/macros/parserImplicitEquation.pl
lib/PG/macros/parserImplicitPlane.pl
lib/PG/macros/parserLinearInequality.pl
lib/PG/macros/parserMultiAnswer.pl
lib/PG/macros/parserMultiPart.pl
lib/PG/macros/parserNumberWithUnits.pl
lib/PG/macros/parserOneOf.pl
lib/PG/macros/parserParametricLine.pl
lib/PG/macros/parserParametricPlane.pl
lib/PG/macros/parserPopUp.pl
lib/PG/macros/parserPrime.pl
lib/PG/macros/parserQuotedString.pl
lib/PG/macros/parserRadioButtons.pl
lib/PG/macros/parserRoot.pl
lib/PG/macros/parserSolutionFor.pl
lib/PG/macros/parserVectorUtils.pl
lib/PG/macros/parserWordCompletion.pl
lib/PG/macros/PG_CAPAmacros.pl
lib/PG/macros/PG_module_list.pl
lib/PG/macros/PG.pl
lib/PG/macros/PGanalyzeGraph.pl
lib/PG/macros/PGanswermacros.pl
lib/PG/macros/PGasu.pl
lib/PG/macros/PGauxiliaryFunctions.pl
lib/PG/macros/PGbasicmacros.pl
lib/PG/macros/PGchoicemacros.pl
lib/PG/macros/PGcommonFunctions.pl
lib/PG/macros/PGcomplexmacros.pl
lib/PG/macros/PGcomplexmacros2.pl
lib/PG/macros/PGcourse.pl
lib/PG/macros/PGdiffeqmacros.pl
lib/PG/macros/PGessaymacros.pl
lib/PG/macros/PGfunctionevaluators.pl
lib/PG/macros/PGgraders.pl
lib/PG/macros/PGgraphmacros.pl
lib/PG/macros/PGinfo.pl
lib/PG/macros/PGlateximage.pl
lib/PG/macros/PGmatrixmacros.pl
lib/PG/macros/PGmiscevaluators.pl
lib/PG/macros/PGML.pl
lib/PG/macros/PGmorematrixmacros.pl
lib/PG/macros/PGnumericalmacros.pl
lib/PG/macros/PGnumericevaluators.pl
lib/PG/macros/PGpolynomialmacros.pl
lib/PG/macros/PGsequentialmacros.pl
lib/PG/macros/PGstandard.pl
lib/PG/macros/PGstatisticsGraphMacros.pl
lib/PG/macros/PGstatisticsmacros.pl
lib/PG/macros/PGstringevaluators.pl
lib/PG/macros/PGtextevaluators.pl
lib/PG/macros/PGtikz.pl
lib/PG/macros/problemPanic.pl
lib/PG/macros/problemPreserveAnswers.pl
lib/PG/macros/problemRandomize.pl
lib/PG/macros/quickMatrixEntry.pl
lib/PG/macros/RserveClient.pl
lib/PG/macros/sage.pl
lib/PG/macros/scaffold.pl
lib/PG/macros/source.pl
lib/PG/macros/StdConst.pg
lib/PG/macros/StdUnits.pg
lib/PG/macros/tableau_main_subroutines.pl
lib/PG/macros/tableau.pl
lib/PG/macros/text2PG.pl
lib/PG/macros/unionLists.pl
lib/PG/macros/unionTables.pl
lib/PG/macros/Value.pl
lib/PG/macros/weightedGrader.pl
```
