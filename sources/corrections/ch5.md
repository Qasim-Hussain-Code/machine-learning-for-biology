# Corrections for Chapter 5, Gut bacteria and cardiovascular risk (logistic regression, support vector machine planned)

Each entry gives the chapter's sentence before and after the change, the repository file that settles it, and the
value found there. The repository is `Qasim-Hussain-Code/tmao_cardiovascular_risk_prediction` at the chapter's pinned
commit `9985756c2db6` throughout.

## 1. The substances measured in every patient, 600 other to 405 of a panel of 600

Before: Every patient also had 600 other substances measured.

After: The dataset lists a panel of 600 substances, those four among them, and 405 of the 600 were measured in every
patient.

Files: `results/metrics/00_summary.json`, with `docs/data_dictionary_st001420.md` and `src/tmao_cvd/st001420.py`.

Value found: `"n_metabolites": 600` under `dataset`; `"metabolites_fully_observed": 405` and
`"metabolites_absent_for_everyone": 195` under `post_hoc`; `"panel_size": 405` under `question_1.panel_context`. The
data dictionary lists the four pathway metabolites, `Trimethylamine N-oxide`, `Choline`, `Betaine` and `Carnitine`,
among the "600 metabolite columns", and `st001420.py` sets `EXPECTED_METABOLITES = 600`, with `metabolite_columns`
returning "The 600 deposited metabolite columns". The README, section 4: "Of the panel, 405 metabolites are fully
observed and 195 are absent for every participant". The 600 therefore include TMAO and its three precursors, so they
are not other substances, and only 405 of them were measured in every patient. Those 405 are TMAO and the "other 404
substances measured" that the chapter gives later, which needed no change. The chapter's "all 600 substances" for the
whole-panel model also stays, because `docs/reanalysis_plan.md`, section 6, describes that model as "L2 penalised
logistic regression on all 600 metabolites".

## 2. The set TMAO is ranked within, the panel to the substances measured in every patient

Before (front matter summary): A model built on all 600 substances came back nearly perfect, TMAO ranked around the
64th percentile of the panel, and without the lab processing order the dataset cannot fully rule out a handling effect,
so the rise cannot be read as strong evidence about TMAO specifically.

After: A model built on all 600 substances came back nearly perfect, TMAO ranked around the 64th percentile of the
substances measured in every patient, and without the lab processing order the dataset cannot fully rule out a
handling effect, so the rise cannot be read as strong evidence about TMAO specifically.

File: `results/metrics/00_summary.json`.

Value found: under `question_1.panel_context`, `"percentile_of_panel": 64.2`, `"metabolites_ranking_higher": 144` and
`"panel_size": 405`. The README, section 5: "the 64.2nd percentile of the 405 fully observed metabolites". This follows
from correction 1: once the chapter names the panel as 600 substances, "of the panel" would place TMAO among all 600
rather than among the 405 measured in every patient. The percentile itself is unchanged.

## 3. The model behind both results, a support vector machine to logistic regression

Before (front matter): model: Support vector machine

After: model: Logistic regression (support vector machine planned)

Before (front matter summary, after the first sentence): The question then became whether TMAO helps predict
cardiovascular risk on top of everything doctors already check, and the data to answer that directly is not public. In
a narrower public dataset of 750 patients, followed for nine months after a heart procedure to see who had chest pain
again, adding TMAO to a model of its three precursors raised the area under the ROC curve for predicting that from
0.848 to 0.873. A model built on all 600 substances came back nearly perfect, TMAO ranked around the 64th percentile of
the substances measured in every patient, and without the lab processing order the dataset cannot fully rule out a
handling effect, so the rise cannot be read as strong evidence about TMAO specifically.

After: The public data could not support that design, and the support vector machine never ran; the question then
became whether TMAO helps predict cardiovascular risk on top of everything doctors already check, and the data to
answer that directly is not public either. In a narrower public dataset of 750 patients, followed for nine months after
a heart procedure to see who had chest pain again, adding TMAO to a logistic regression on its three precursors raised
the area under the ROC curve, scored on patients each model had not been trained on, from 0.848 to 0.873, a difference
of 0.0256 with an interval of 0.0075 to 0.0436, and the rise met both parts of the rule fixed before any model was
fitted. A penalised logistic regression on all 600 substances came back nearly perfect, with an area of 1.0; TMAO
ranked around the 64th percentile of the substances measured in every patient, and without the lab processing order
the dataset cannot fully rule out a handling effect, so the rise cannot be read as strong evidence about TMAO
specifically.

The summary also carries entries 5, 6 and 7: how the areas were scored, the difference and its interval, the rule, the
whole-panel area, and the design the public data could not support.

Before (heading): Why a support vector machine

After: Why a support vector machine was planned

Before (first paragraph of that section): The features here, the measurements the model is given for each person, are a
short list: the six genes of the pathway that makes TMA, each with a mechanistic reason to be there. Six numbers per
person, a few hundred people, and a boundary that may curve rather than split cleanly.

After: The metagenomic design was planned around a support vector machine. Its features, the measurements the model
would be given for each person, were a short list: the six genes of the pathway that makes TMA, each with a mechanistic
reason to be there. Six numbers per person, a few hundred people, and a boundary that might curve rather than split
cleanly.

Before (rules box, Changed because the data is not public): The chapter moved to a public dataset of 750 patients and
asked two narrower questions of it, with the rules for judging both answers written down before either test ran.

After: The chapter moved to a public dataset of 750 patients and asked two narrower questions of it. Both were answered
with logistic regression, not a support vector machine, and every model was scored on patients it had not been trained
on.

The clause removed from that item is entry 4.

Added (A narrower dataset, after Figure 5.3): No support vector machine ran on this dataset. I answered both questions
with logistic regression, the model of Chapter 1. For the first, a logistic regression on the three ingredients was set
against the same model with TMAO added, with no penalty on either. For the second, a logistic regression was given all
600 substances and penalised to keep its weights small, and the strength of that penalty was chosen inside each
training set, so that the patients held back for scoring played no part in choosing it.

The rest of that paragraph is entry 5.

Before (closing): That makes five chapters and five models. Every chapter so far has paired one model with one
biological question chosen to make that model earn its place. The support vector machine looked for the widest
possible gap between two outcomes, rather than any line that happened to separate them.

After: That makes five chapters and five models, though the fifth was planned and never run. Every chapter so far has
paired one model with one biological question chosen to make that model earn its place. Here the support vector
machine, which looks for the widest possible gap between two outcomes rather than any line that happens to separate
them, was paired with the metagenomic question, and both results came instead from logistic regression, the model of
Chapter 1.

Files: `src/tmao_cvd/reanalysis.py`, `src/tmao_cvd/models.py`, `docs/reanalysis_plan.md` and `README.md`.

Value found: `reanalysis.py`, `question_one`: `baseline = cross_validated_predictions(make_logistic_model,
frame[PRECURSOR_FEATURES], outcome, config)`, and the same with `EXTENDED_FEATURES` for the model with TMAO.
`models.py`: `make_logistic_model` is "Unpenalised logistic regression with imputation and standardisation", built as
`LogisticRegression(penalty=None, solver="lbfgs", max_iter=2000, random_state=seed)`. `reanalysis.py`,
`question_two`: `predictions = cross_validated_predictions(_panel_model, panel, outcome, config)`, where `_panel_model`
is "L2 penalised logistic regression with the penalty chosen in-fold", `LogisticRegressionCV(Cs=np.logspace(-3, 1, 5),
cv=5, penalty="l2", ...)`, placed inside the outer resampling loop "so no information from a held out fold reaches
model selection". The plan, section 6, question 1: "Estimator: unpenalised logistic regression."; question 2: "Model:
L2 penalised logistic regression on all 600 metabolites, with the penalty selected inside each training fold by nested
cross validation". The README, The chapter as published: "Days 47 to 51 set out a study of gut metagenomic gene
abundances that the public data could not support." No file at the commit fits a support vector machine: a search of
every text file for "svm", "svc", "support vector" and "kernel" finds only `posts/day47.txt`, `posts/day50.txt`,
`posts/day51.txt` and the README's table entry for `posts/day51.txt`. The rest of the section on the support vector
machine explains the planned model and stays; Figure 5.2 and its caption show how a support vector machine draws its
boundary, which is still true.

## 4. When the rules for the narrower dataset were written, before any model was fitted but after a first look

Before (rules box, Changed because the data is not public): The chapter moved to a public dataset of 750 patients and
asked two narrower questions of it, with the rules for judging both answers written down before either test ran.

After: as in entry 3, with a new item at the end of the box.

Added (rules box): **Looked at before these rules were written.** TMAO and its three precursors, summarised in each
group of patients, with a rank-sum test on TMAO. Which way the TMAO difference ran was therefore known in advance.

Before (The rules, opening): The rules were written before anything was downloaded.

After: The rules for the metagenomic design were written before anything was downloaded. The last three items in the
box belong to the narrower dataset the chapter later moved to, described below.

Added (A narrower dataset): I wrote down the rules for judging both answers before any model was fitted, but not before
I had looked at the data. To check that the dataset was usable at all, I had already summarised TMAO and its three
ingredients in each group of patients and run a rank-sum test on TMAO, so I knew which way the TMAO difference ran
before the rules existed. That is a departure from an ideal pre-registration.

File: `docs/reanalysis_plan.md`, sections 2 and 8, with the repository's commit history up to the pinned commit.

Value found: section 2, "Disclosure of partial unblinding": "Before this plan was written, the analyst had already
loaded the matrix and computed univariate summaries of the four pathway metabolites by outcome group, including a rank
sum test on TMAO. That check was performed to establish that the dataset was usable at all, and its result is known.
This is a real departure from an ideal pre-registration and is recorded here rather than concealed. Its practical
consequence is that the direction of the univariate TMAO difference is known in advance. The thresholds in section 6
were nevertheless fixed before any model was fitted, any cross validation was run, or any discrimination, calibration
or net benefit statistic was computed." Section 8 lists the partial unblinding as "a departure from an ideal
pre-registration". The plan opens: "This document is written before any loader, model or estimate exists in the
repository, and it is committed before the code it governs." The commit history agrees: `add_reanalysis_plan`
(`6ae296b83aa7`) precedes `add_reanalysis_questions` (`09758972cce2`) on 11 September 2026. The closing sentence "The
code, the rules written before each test, and every result in this chapter are in the repository" stays, because the
rules did precede every model test.

## 5. How the scores were measured, and their intervals

Added (A narrower dataset, the rest of the paragraph in entry 3): Every model was scored on patients it had not been
trained on, by cross-validation as in Chapter 2. The 750 patients were divided into five parts, each model was trained
on four parts and scored on the fifth, in turn, and the whole division was made five times, with different parts each
time.

Before (What came back): Adding TMAO to a model of its own three building blocks, choline, betaine and carnitine, raised
the area under the ROC curve for predicting who would have chest pain again from 0.848 to 0.873. That is a real
improvement.

After: Adding TMAO to a model of its own three building blocks, choline, betaine and carnitine, raised the area under
the ROC curve for predicting who would have chest pain again from 0.848 to 0.873. More precisely, the model without
TMAO scored 0.8475, with a confidence interval of 0.8132 to 0.8818, and the model with it scored 0.8731, with an
interval of 0.8402 to 0.906. The difference was 0.0256, with an interval of 0.0075 to 0.0436, clear of zero.

The two sentences that follow it are entry 6.

Before: A model built from all 600 substances came back nearly perfect at separating the patients who had chest pain
again from those who did not.

After: The model built from all 600 substances came back nearly perfect at separating the patients who had chest pain
again from those who did not. Scored on patients it had not been trained on, its area under the ROC curve was 1.0, and
its accuracy, the share of patients it put in the right group, was 0.9973.

The rules box ("every model was scored on patients it had not been trained on") and the summary (entry 3) say the
same.

Files: `results/metrics/00_summary.json`, `docs/reanalysis_plan.md`, `src/tmao_cvd/config.py`,
`src/tmao_cvd/models.py`, `src/tmao_cvd/evaluate.py` and `README.md`.

Value found: under `question_1`, `"baseline_auc": 0.8475`, `"baseline_auc_ci": [0.8132, 0.8818]`, `"extended_auc":
0.8731`, `"extended_auc_ci": [0.8402, 0.906]`, `"delta_auc": 0.0256` and `"delta_auc_ci": [0.0075, 0.0436]`; under
`question_2`, `"auc": 1.0` and `"accuracy": 0.9973`. The plan, section 6: "All estimates come from out of fold
predictions under repeated stratified cross validation, five folds by five repeats, with folds shared across every
model in a run so that comparisons are paired." `config.py` sets `n_splits: int = 5` and `n_repeats: int = 5`;
`models.py` splits with `RepeatedStratifiedKFold` and scores the "Mean out of fold prediction per participant across
repeats". `evaluate.py`, `auc_with_ci`: "Area under the curve with a DeLong confidence interval", with `alpha: float =
0.05`; `delong_difference_with_ci` takes the interval on the difference from the same covariance. The README, section
4, heads the question 2 column "Out of fold" and describes that model as "evaluated strictly out of fold". The 0.848 and
0.873 of the posts are the first two areas to three places and stay. The summary file gives no interval for the
whole-panel model's area, so the chapter gives none.

## 6. The rule for calling the rise a real improvement, and the result against it

Added (rules box): **Fixed before any model was fitted.** Adding TMAO to a model of its three precursors counts as a
real improvement only if two things hold. The confidence interval on the difference in area under the ROC curve
excludes zero, and the decision curve of the model with TMAO, a measure of how useful its predictions would be for
deciding whom to treat, lies above that of the model without it across a substantial part of the range of risk
thresholds.

Added (A narrower dataset): The rule for the first question, set out in the box earlier in the chapter, has two parts,
and they test different things. An interval on the difference in area that excludes zero shows that
the difference can be detected. The decision curve asks whether using the model with TMAO would lead to better
decisions than using the model without it. Had the first part held and the second failed, the rise would have been
reported as detectable but clinically negligible.

Added (note): **Decision curve.** A doctor treats a patient once the predicted risk passes some threshold, and where
that threshold sits says how many unnecessary treatments the doctor will accept to catch one real case. At each
threshold, a model's net benefit is the share of patients it rightly flags, less the share it wrongly flags weighted by
that trade. A decision curve plots net benefit across a range of thresholds.

Before (What came back): That is a real improvement.

After: The decision curve of the model with TMAO lay above that of the model without it across 0.9821 of the range of
thresholds, almost all of it. Both parts of the rule were met, so by the standard fixed before any model was fitted,
that is a real improvement.

The summary's "and the rise met both parts of the rule fixed before any model was fitted" (entry 3) rests on this
entry.

Files: `docs/reanalysis_plan.md`, `results/metrics/00_summary.json`, `src/tmao_cvd/reanalysis.py`,
`src/tmao_cvd/evaluate.py` and `README.md`.

Value found: the plan, section 6, question 1, "Fixed in advance": "Positive. The confidence interval on the difference
in area excludes zero, and the extended model's decision curve lies above the baseline model's across a substantial
part of the threshold range." and "Discordant. Interval excludes zero but the decision curves do not separate.
Conclusion: a statistically detectable but clinically negligible contribution." Net benefit is computed "across
thresholds from 0.05 to 0.60", which `reanalysis.py` sets as `Q1_THRESHOLDS = np.linspace(0.05, 0.60, 56)`, and the
code reads "a substantial part of the range" as a majority of that grid (`curves_separate = separation > 0.5`). Under
`question_1` in the summary: `"verdict": "POSITIVE"`, `"delta_auc_ci": [0.0075, 0.0436]` and
`"decision_curve_separation": 0.9821`. The README, section 4: "The interval on the difference excludes zero" and "The
extended model's decision curve lies above the baseline's across a proportion 0.9821 of the pre-specified threshold
range." The note follows `evaluate.py`, `net_benefit`: "At threshold t the benefit of a true positive is weighted
against the harm of a false positive by the odds t / (1 - t). The threshold is therefore an explicit statement of how
many unnecessary interventions a clinician would accept to prevent one event", computed as `true_positives / n -
(false_positives / n) * weight`; and the module's account of clinical utility: "Would using the model lead to better
decisions than treating everyone or nobody? Measured by net benefit across a range of decision thresholds".

## 7. The four ways the chapter could be wrong, limited to the design they were written for

Before (end of the section Four ways this could be wrong): If more than one cohort was available, I would test across
them. If only one was, the result would travel no further than that population.

After: the same two sentences, then: All four were written for the metagenomic design, and that design never ran,
because the public data could not support it. The tests that did run, on the narrower dataset described next, used
substances measured in plasma rather than genes counted in stool, so the first three do not apply to them. The fourth
applies only in its fallback form. That dataset is a single cohort, and what it shows travels no further than that
population.

Files: `README.md`, `docs/reanalysis_plan.md` and `results/metrics/00_summary.json`.

Value found: the README, The chapter as published: "Days 47 to 51 set out a study of gut metagenomic gene abundances
that the public data could not support." The plan, section 3, the Sampling row: "Fasting plasma drawn 48 hours after
percutaneous coronary intervention". The summary's `scope`: "these findings come from a single cohort of post-PCI
secondary prevention patients ... There is no external validation ... Nothing here transfers to primary prevention, to
hard cardiovascular endpoints, or to other populations." The README, section 3, says the same of the narrower question.
The first three ways concern genes counted in stool (presence against expression, the diet ceiling on a model of gene
abundance, and gene proportions that sum to a fixed total), and nothing in the reanalysis measures a gene. The fourth
way's own fallback, that a single cohort travels no further than its population, is what the record's scope states, so
the chapter says the fourth applies in that form rather than that none of the four applies.

## 8. The posts as published, checked without change

The published posts kept verbatim in `posts/` at the pinned commit (`day47.txt` to `day53.txt`) were compared with the
book's copy in `sources/ch5.md`. Apart from hashtags and the link placeholder they differ in two places: Day 52 reads
"something smaller but real" where the book's copy reads "something smaller", and Day 53 adds the sentence "Both things
are true, and both are worth saying." Neither corrects a number or an account, so the chapter did not change on their
account.

## 9. The whole-panel model: its columns and its pre-set verdict

Before: The model built from all 600 substances came back nearly perfect at separating the patients who had chest
pain again from those who did not. Scored on patients it had not been trained on, its area under the ROC curve was
1.0, and its accuracy, the share of patients it put in the right group, was 0.9973. For a hard clinical question that
is usually a sign to look closer rather than to celebrate.

After: The model built from the whole panel, in effect the 405 substances measured in every patient, since the other
195 were empty for everyone, came back nearly perfect ... was 0.9973. Even so, it only partly met the rule I had
fixed for it in advance. Its accuracy, overall and within each group of patients, was far above the floor of 0.85
that the rule set, but its calibration slope, 2.97, lay outside the band of 0.80 to 1.25 that the rule also required.
A slope that far from 1 means the predicted risks cannot be read as probabilities, even though the model ranked the
patients almost perfectly.

A score that high on a hard clinical question is usually a sign to look closer rather than to celebrate.

The last sentence opens a new paragraph and names the score, because after the added sentences "that" would have
pointed at the calibration slope rather than at the near-perfect result.

Files: `results/metrics/00_summary.json`, `docs/reanalysis_plan.md` sections 6 and 8, and `src/tmao_cvd/reanalysis.py`
(`question_two`, and line 232), at `9985756c2db6`.

Value found: `question_2` in the summary gives `"verdict": "PARTIAL"`, `"accuracy": 0.9973`, `"sensitivity": 1.0`,
`"specificity": 0.9963`, `"auc": 1.0` and `"calibration_slope": 2.9711`; `post_hoc` gives `metabolites_fully_observed
405` and `metabolites_absent_for_everyone 195`. Section 6 of the plan defines "Reproduced" as out-of-fold accuracy,
sensitivity and specificity all at or above 0.85 with "the calibration slope ... between 0.80 and 1.25", and gives
"Partial" as values that "fall between 0.75 and 0.85 with acceptable calibration", reported "with no verdict attached".
`reanalysis.py` sets `Q2_REPRODUCED_FLOOR = 0.85` and `Q2_CALIBRATION_SLOPE_RANGE = (0.80, 1.25)`, and attaches the
`PARTIAL` label to every case that is neither reproduced nor collapsed, which is the route this result took; section 8
of the plan records that the partial branch "was written for only one of the two ways of reaching it": what occurred was
"discrimination far above the reproduction floor with a calibration slope ... far above the acceptable band", the
verdict label unchanged "because the decision rule in the code behaved exactly as written". For that route the `reason`
the code writes into its statement ends: "A slope this far from one means the predicted risks are not usable as
probabilities even though the ranking is near perfect." Sensitivity and specificity are the accuracy within the patients
who had chest pain again and within those who did not (`np.mean(predicted[outcome == 1])` and
`np.mean(~predicted[outcome == 0])`), so "overall and within each group of patients" covers the three scores the rule
tests. The chapter says the result only partly met the rule, after the record's PARTIAL, rather than using the plan's
between-the-floors wording, which section 8 says does not fit this case; the rule's name for a full pass, "Reproduced",
is left out because the chapter does not describe the earlier figure it refers to. The whole-panel pipeline imputes
missing values with `SimpleImputer(strategy="median")`, which drops a column that is empty for every patient, so the
model drew on the 405 measured columns. The front-matter summary's "all 600 substances" was changed to "the whole panel"
with it. Where the chapter says what the model was given ("a logistic regression was given all 600 substances") or poses
the question it was built for, "all 600 substances" stays, as entry 1 records.

## 10. What measuring TMAO takes

Before: Measuring TMAO itself requires mass spectrometry, and almost nobody who could benefit from knowing their risk
will ever have it run.

After: Measuring TMAO itself needs a specialised laboratory assay, and almost nobody who could benefit from knowing
their risk will ever have it run.

Sources: `docs/reanalysis_plan.md` section 3 at 9985756c2db6, and the published nuclear magnetic resonance assay for
TMAO in serum and plasma: Garcia E, Wolak-Dinsmore J, Wang Z, Li XS, Bennett DW, Connelly MA, Otvos JD, Hazen SL,
Jeyarajah EJ. NMR quantification of trimethylamine-N-oxide in human serum and plasma in the clinical laboratory
setting. Clinical Biochemistry 2017;50(16-17):947-955, DOI 10.1016/j.clinbiochem.2017.06.003, PMID 28624482, PMCID
PMC5632584; abstract, methods and conflict of interest statement.

Value found: the deposit's TMAO was measured by targeted LC-MS/MS, but an automated nuclear magnetic resonance assay for
TMAO in serum and plasma has been published for the clinical laboratory, so mass spectrometry is not the only way to
measure it. Both are specialised assays, which is the sentence's point. The paper's abstract reads "The aim of this
study was to develop an automated nuclear magnetic resonance (NMR) spectroscopy assay for quantification of TMAO
concentration in serum and plasma using a high-throughput NMR clinical analyzer", and reports that the NMR values
"compared well with values obtained with the MS-based assay (R2=0.98)". The assay is sold as a send-out clinical test
(LabCorp test 123413, TMAO (Trimethylamine N-oxide), methodology "Nuclear magnetic resonance (NMR)", read 2 October
2026), so neither route is a routine chemistry panel measurement.

## 11. The deposit's numbering, and the check that found order along it

Before: ... Instruments drift over a long run, for example, so if most samples from one group had been processed before
most from the other, the drift alone could make many substances differ between the groups. That is a limit of what this
particular dataset can tell us.

After: ... the drift alone could make many substances differ between the groups. [new paragraph] The deposit's own
numbering makes that more than a hypothetical. Samples 1 to 210 are exactly the 210 patients who had chest pain again,
and samples 211 to 750 exactly the 540 who did not. The plan that held the rules also held a check on this. Within each
group separately, so that the difference between the groups played no part, it asked whether each substance's level rose
or fell with the sample number. If the numbering had nothing to do with the measurements, about 5% of the 405 substances
would appear to do so by chance. Among the patients who had chest pain again, it was 16.8%, and among the others 15.6%.
That does not show the samples were run in numbered order, because the numbering need not be the order the lab used. It
does mean that every difference between the two groups in this dataset may be tangled up with that order, to a degree
the deposit cannot measure. That is a limit of what this particular dataset can tell us.

Before (front matter summary): ... TMAO ranked around the 64th percentile of the substances measured in every patient,
and without the lab processing order the dataset cannot fully rule out a handling effect, so the rise cannot be read as
strong evidence about TMAO specifically.

After: ... TMAO ranked around the 64th percentile of the substances measured in every patient. The deposit numbers every
patient who had chest pain again before every patient who did not. A check fixed in advance found structure along that
numbering within both groups, and without the lab processing order, the dataset cannot fully rule out a handling effect,
so the rise cannot be read as strong evidence about TMAO specifically.

Files: `docs/reanalysis_plan.md` sections 5 and 6, `docs/data_dictionary_st001420.md`, `results/metrics/00_summary.json`
and `README.md` section 6, at 9985756c2db6.

Value found: the data dictionary: "Samples S1 to S210 are exactly the 210 cases and S211 to S750 exactly the 540
controls." Question 3, written into the plan before the run, computes within each outcome block the Spearman correlation
between sample index and log peak area for every metabolite, and declares order structure present if the proportion of p
values below 0.05 exceeds 0.10 in either block, or if a Kolmogorov-Smirnov test against the uniform gives p below 0.001
in either block. `00_summary.json`, `question_3`: verdict "ORDER STRUCTURE DETECTED", null expectation 0.05 (5%); cases
210 participants, 405 metabolites tested, proportion 0.1679 (16.8%), Kolmogorov-Smirnov p 5.88e-08; controls 540
participants, 405 metabolites, proportion 0.1556 (15.6%), p 8.3e-11. The plan's conclusion for this branch: "acquisition
order structure is detectable, and any between group difference in this dataset is confounded with it to an unknown
degree. Every other result in this analysis is then reported under that caveat." The README adds that detection "does
not establish that the signal is artefactual", since "the deposited ordering need not be the acquisition ordering". The
posts never reported question 3. The chapter now does, in the section that already carried the caveat, and the summary
says so.

## 12. How widely *cutC* is spread, at least a hundred genera to four bacterial phyla

Before: The gene spread by horizontal transfer, passed sideways between organisms rather than inherited down a lineage.
It turns up in patches across at least a hundred genera, and it is absent from most members of most of them.

After: The gene spread by horizontal transfer, passed sideways between organisms rather than inherited down a lineage.
It turns up in patches across four bacterial phyla, and it is absent from most members of most of the genera that carry
it.

Source: Martinez-del Campo A, Bodea S, Hamer HA, Marks JA, Haiser HJ, Turnbaugh PJ, Balskus EP. Characterization and
detection of a widely distributed gene cluster that predicts anaerobic choline utilization by human gut bacteria. mBio
2015;6(2):e00042-15, DOI 10.1128/mBio.00042-15, PMID 25873372, PMCID PMC4453576; Results, the section on the
distribution of the cut gene cluster in sequenced bacterial genomes, with Fig. 3A and Fig. 3C. Genus counts checked
against Cai YY and others. Integrated metagenomics identifies a crucial role for trimethylamine-producing
Lachnoclostridium in promoting atherosclerosis. npj Biofilms and Microbiomes 2022;8(1):11, DOI
10.1038/s41522-022-00273-4, PMCID PMC8913745; Rath S and others. Microbiome 2017;5:54, DOI 10.1186/s40168-017-0271-9;
Jameson E and others. Microbial Genomics 2016;2(9):e000080, DOI 10.1099/mgen.0.000080; and Falony G, Vieira-Silva S,
Raes J. Annual Review of Microbiology 2015;69:305-321, DOI 10.1146/annurev-micro-091014-104422.

Value found: the paper the passage rests on reports "459 CutC homologs (88% to 61% amino acid identity) distributed
across four bacterial phyla (Proteobacteria, Firmicutes, Actinobacteria, and Fusobacteria)" and gives no count of genera
anywhere; it reports homologues, phyla and per-genus genome ratios only. The one published genus count for *cutC* is
Cai and others 2022, which places CutC in 3 genera from Actinobacteria, 27 from Firmicutes, 18 from Proteobacteria and 4
from other phyla, that is 52 genera, with cutC and cutD together in 48. The two figures near a hundred in this
literature belong to other things: Cai's 102 genera cover cntA/B, yeaW/X and cutC/D taken together, and Falony and
others 2015 counted 102 genomes with TMA-producing potential, not genera. Rath 2017 screened 67,134 genomes and gives no
genus total. No source supports "at least a hundred genera", which is about double the only published count, so the
count is dropped and the chapter now gives only the figure its own source reports. The rest of the sentence stands: the
abstract of the same paper reports "an unexpectedly wide but discontinuous distribution for this pathway among bacterial
phyla and evidence of acquisition via horizontal gene transfer", and the ratios it lists, 4% of *Escherichia coli*, 15%
of *Streptococcus suis*, 66% of *Clostridium botulinum* and 62% of *Pectobacterium*, with only two genera at every
genome, are the absence from most members that the clause describes. "Most of them" became "most of the genera that
carry it" because, with the count gone, "them" had no genera left to refer to.

## 13. The *Escherichia coli* figure, its denominator named

Before: Four per cent of *Escherichia coli* genomes carry a *cutC* homologue, and the other ninety-six per cent do not.

After: Ninety-eight of 2,719 sequenced *Escherichia coli* genomes carry a *cutC* homologue, four per cent. The other
ninety-six per cent do not.

Source: Martinez-del Campo and others 2015, mBio 6(2):e00042-15, DOI 10.1128/mBio.00042-15, PMCID PMC4453576; Results,
the distribution section, with the Fig. 3A legend.

Value found: "only 4% (98) of the 2,719 Escherichia coli genes and 15% (16) of the 101 Streptococcus suis genes encode a
CutC homolog". The proportion and the count are the paper's own and did not change; the denominator is added so a reader
can check the figure against the sentence that carries it. That sentence says "genes" where the chapter says "genomes",
but the clause beside it counts genomes for *Desulfosporosinus* (6/6 genomes) and *Proteus* (17/17 genomes), and Fig. 3A
reports "the proportions of bacterial genomes that contain the cut gene cluster", so genomes is what the 98 of 2,719
counts and the paper's noun reads as a slip. The chapter therefore keeps genomes and names the denominator, so that a
reader who meets the paper's wording can see the figures agree. Figure 5.1 keeps 4% and 96% in its labels, its alt text
and its caption, because neither value changed.
