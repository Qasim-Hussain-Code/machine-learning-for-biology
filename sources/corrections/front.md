# Corrections for the front and back matter: preface and epilogue

Each entry gives the sentence before and after the change, the source that settles it, and the value found there. The
front and back matter have no repository of their own; their sources are the chapter repositories at the
commits the chapters pin.

Entries 1 to 4, 9, 10 and 13 concerned the prologue, which was withdrawn from the book on 3 October 2026. They are not
reproduced here, and the remaining entries keep their numbers so that references to them still hold.

## 5. What Chapter 5 ran (preface)

Before: Chapter 5 sets out to use a support vector machine on gut bacteria and cardiovascular risk, and finds that the
data its design needs is not public, so it asks two narrower questions of a public dataset instead.

After: Chapter 5 sets out to use a support vector machine on gut bacteria and cardiovascular risk, finds that the data
its design needs is not public, and answers two narrower questions of a public dataset with logistic regression
instead.

Files: `docs/reanalysis_plan.md`, section 6, `src/tmao_cvd/models.py`, `src/tmao_cvd/reanalysis.py` and `README.md`, in
`Qasim-Hussain-Code/tmao_cardiovascular_risk_prediction` at Chapter 5's pinned commit `9985756c2db6`.

Value found: section 6 of the plan, question 1, "Estimator: unpenalised logistic regression"; question 2, "Model: L2
penalised logistic regression on all 600 metabolites". `models.py` defines `make_logistic_model` as
`LogisticRegression(penalty=None, solver="lbfgs", ...)`, which `reanalysis.py` fits to the precursor model and to the
model with TMAO added, and `reanalysis.py` fits the whole panel with `LogisticRegressionCV(Cs=np.logspace(-3, 1, 5),
cv=5, penalty="l2", ...)`. No file at that commit fits a support vector machine: outside the posts kept verbatim in
`posts/`, the only mention is the README's table entry for `posts/day51.txt`, "Why a support vector machine, and what
the kernel does". The README: "Days 47 to 51 set out a study of gut metagenomic gene abundances that the public data
could not support." This follows the Chapter 5 decision that the support vector machine never ran.

## 6. When the rules are written, before anything runs to before any model is fitted (preface)

Before: The rules are written down before anything runs, and in most chapters so are the ways the analysis could go
wrong.

After: The rules are written down before any model is fitted, and in most chapters so are the ways the analysis could go
wrong.

Files: `docs/reanalysis_plan.md`, section 2, in the Chapter 5 repository at `9985756c2db6`; the history of
`scripts/05_build_disagreement_set.py` and `notes/finish_pipeline.log` in
`Qasim-Hussain-Code/bakta_prokka_disagreement_prediction`, Chapter 3's repository, at `4f797c3fa09d`.

Value found: section 2 of Chapter 5's plan, "Disclosure of partial unblinding": "Before this plan was written, the
analyst had already loaded the matrix and computed univariate summaries of the four pathway metabolites by outcome
group, including a rank sum test on TMAO", and "The thresholds in section 6 were nevertheless fixed before any model was
fitted, any cross validation was run, or any discrimination, calibration or net benefit statistic was computed." So in
Chapter 5 something had run before the rules were written, but no model had. In Chapter 3 the label script took its
matching rule, one base of overlap on the same strand, in commit `0f6e6ef8cba5` at 09:03 UTC on 20 August 2026, and the
pipeline log has the label built at 19:47:06 and the forest fitted at 19:47:50 that day (+08:00), so there too the rule
that ran came before any model was fitted. This follows the Chapter 3 and Chapter 5 decisions.

## 7. The stage baseline, the stage itself to a model given only the stage (preface)

Before: ... guessing the commonest answer, a textbook rule about one position in a peptide, the stage a clinician
already knows, a model given nothing but how tightly each peptide binds the molecule that displays it.

After: ... guessing the commonest answer, a textbook rule about one position in a peptide, a model given only the stage a
clinician already knows, and one given nothing but how tightly each peptide binds the molecule that displays it.

File: `results/metrics/05_baseline_stage.json` in `Qasim-Hussain-Code/cancer_survival_ml_pipeline` at Chapter 4's
pinned commit `85d831ca383c`.

Value found: `"rule": "The comparison this model has to beat is stage alone."`; under `pooled`, `"model": "Cox
proportional hazards, stage only"` and `"features": ["pathological stage, one-hot, reference Stage I, with an explicit
unknown level"]`, fitted on 410 patients and scored on 176, concordance index 0.6743. The baseline is a model fitted to
stage, not the stage itself, as the Chapter 4 decision on how stage was turned into a score has it. The Chapter 6
baseline in the same sentence is, in `results/metrics/05_baseline_validation.json` of
`Qasim-Hussain-Code/neoantigen_immunogenicity_prediction` at `68a12d14824d`, "logistic regression on log10 measured
affinity in nM" with one feature, and needed no change.

## 8. What Chapter 5 ran (epilogue)

Before: The support vector machine of Chapter 5 looked for the widest possible gap between two outcomes.

After: Chapter 5 set out to use a support vector machine, a model that looks for the widest possible gap between two
outcomes, and the data it needed was not public. It answered two narrower questions with logistic regression instead.

Before (front matter summary): Seven chapters used seven models, from logistic regression to k-means, to teach the
basics of machine learning one idea at a time.

After: Seven chapters introduced seven models, from logistic regression to k-means, to teach the basics of machine
learning one idea at a time. Chapter 5 set out to use a support vector machine, found that the data it needed was not
public, and answered two narrower questions with logistic regression.

Files and value found: as in entry 5. Day 70 as kept in the Chapter 7 repository (`posts/day_70.md` at `1141fa411573`)
reads "Chapter 5, a support vector machine: the widest possible gap between two outcomes", as the book's copy does, and
no later post corrects it. "Seven chapters, seven models" still opens the epilogue: Chapter 5 still explains what a
support vector machine does, so the book introduces seven models, one to a chapter, though the one Chapter 5 introduces
was never fitted.

## 11. Before running anything, to before fitting anything (epilogue)

Before: Fix the rules before running anything.

After: Fix the rules before fitting anything.

Files and value found: as in entry 6. In Chapter 5 the data had been loaded and summarised before the reanalysis rules
were written, and in Chapter 3 the label was built with the rule that ran before the rule was posted; in every chapter
the rules were fixed before any model was fitted, which is what the maxim now says. Day 70's wording was "before
running anything".

## 12. One post a day, wrote to posted (preface)

Before: Between 24 July and 1 October 2026 I wrote seventy of them on machine learning for biology, one a day, each
written to stand on its own.

After: Between 24 July and 1 October 2026, I posted seventy of them on machine learning for biology, one a day, each
written to stand on its own.

Files: the history of `posts/` in `Qasim-Hussain-Code/cancer_survival_ml_pipeline`, Chapter 4's repository, up to its
pinned commit `85d831ca383c`, with `sources/series-dates.md`.

Value found: commit `26aef85b1464` ("add_prereg_posts"), at 09:57 UTC on 3 September 2026, adds `posts/day40.txt` to
`posts/day44.txt`, and the pinned commit `85d831ca383c` ("add_day45_post"), at 09:21 UTC on 4 September, adds
`posts/day45.txt`. With seventy posts on the seventy days from 24 July to 1 October (`sources/series-dates.md`), one to a
day, Day 42 fell on 3 September, Day 43 on 4 September, Day 44 on 5 September and Day 45 on 6 September, so the posts
for Days 43 to 45 were written before the days they appeared. What the sources give is one post for each day, not one
written each day.

## 14. Why Chapter 5's design never ran (preface and epilogue)

Before (preface): Chapter 5 sets out to use a support vector machine on gut bacteria and cardiovascular risk, finds that
the data its design needs is not public, and answers two narrower questions of a public dataset with logistic regression
instead.

After: Chapter 5 sets out to use a support vector machine on gut bacteria and cardiovascular risk, finds that the public
data cannot support its design, and answers two narrower questions of a public dataset with logistic regression instead.

Before (epilogue): Chapter 5 set out to use a support vector machine, a model that looks for the widest possible gap
between two outcomes, and the data it needed was not public.

After: Chapter 5 set out to use a support vector machine, a model that looks for the widest possible gap between two
outcomes, but the public data could not support the design it was chosen for.

Before (epilogue summary): Chapter 5 set out to use a support vector machine, found that the data it needed was not
public, and answered two narrower questions with logistic regression.

After: Chapter 5 set out to use a support vector machine, found that the public data could not support the design, and
answered two narrower questions with logistic regression.

File: `README.md` in Chapter 5's repository at 9985756c2db6.

Value found: "Days 47 to 51 set out a study of gut metagenomic gene abundances that the public data could not support."
The README's "No public dataset supports it" and "controlled access" are about the later plasma TMAO question, not the
metagenomic design. Chapter 5 itself says "that design never ran, because the public data could not support it", and
keeps "not public" for the TMAO question, where it belongs. This replaces the wording chosen under front decision 4.
Chapter 6's cross-reference is changed to match (sources/corrections/ch6.md entry 9).
