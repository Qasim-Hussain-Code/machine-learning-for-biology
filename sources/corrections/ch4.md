# Corrections for Chapter 4, What happens to the patients who are still alive? (gradient boosting)

Each entry gives the chapter's sentence before and after the change, the repository file that settles it, and the
value found there. The repository is `Qasim-Hussain-Code/cancer_survival_ml_pipeline` at the chapter's pinned commit
`85d831ca383c` throughout, except in entry 11, which is settled by Chapter 5's repository. The repository keeps the
posts for Days 40 to 45 under `posts/`. None of them corrects an earlier post, so no published correction applies to
this chapter.

## 1. The wrong split that had cost a chapter, removed

Before: The grouped split did not need deciding. It needed restating, because getting it wrong once had already cost
a chapter.

After: The grouped split did not need deciding, only restating.

Files: `posts/day42.txt`, with `scripts/02_build_cohort.py`.

Value found: the Day 42 post kept at the pinned commit says "That part does not need deciding. It needs restating,
because getting it wrong once already cost a chapter." It does not say which chapter, or what was lost, and no other
post and no file in the repository does. The nearest is the check in `scripts/02_build_cohort.py` that stops the run
if any patient falls on both sides of the split, which calls that "the Chapter 3 failure": it names the failure the
check guards against, not a chapter that was lost. A claim that cannot be checked was taken out. The rule itself is
unchanged in the rules box.

## 2. What the second warning was checked on, grade and tumour size to pT and pN

Before: The version here is one clinical fact, detected through three correlated proxies and reported as three
important features instead of one.

Added, as a paragraph after it: This data turned out to record neither grade nor tumour size, so the check for this
warning ran on stage and the other descriptors that were recorded, with pT, the T category of TNM, standing in for
tumour size, and pN, the N category, for the lymph nodes. Stage is built partly from those two, so the check still
asked the same question.

Files: `scripts/config.py`, block `DEVIATION_DAY43_CORRELATION`, with `results/metrics/03_correlation_check.json` and
`README.md`, Deviations from the pre-registration, item 1.

Value found: the deviation reads "Tumour grade and tumour size are not recorded in this data and the check cannot be
run on the three variables Day 43 named. Grade is populated for 1 of 459 TCGA-COAD patients in the harmonised GDC
clinical layer and is absent from the BCR Biotab clinical_patient file entirely. Tumour largest dimension is empty for
every patient in both candidate cohorts." The substitution reads "The check is run on the pathological descriptors
that do exist: pathological stage, pT category, pN category, lymph nodes examined count, residual tumour status, and
lymphovascular invasion. pT is the recorded stand-in for tumour size and pN for nodal burden." The rationale ends "pT
and pN are the components pathological stage is built from, so the substitution tests the same claim on the variables
actually present." In `03_correlation_check.json`, `day43_named_variables` marks grade and tumour size
`"available": false`, and `variables_checked` lists the six descriptors. The chapter says "built partly" because stage
also takes in M, spread to distant parts of the body, which is not among them. Figure 4.2 and its alt text give the
check as it ran, "rank correlation among stage, pT, pN and others", not as Day 43 planned it on stage, grade and size;
this matches `variables_checked` and the file's `method`, "Spearman rank correlation on complete pairs". The caption,
which describes the check set against each warning, stays true.

## 3. How stage was turned into a score

Before: Stage alone, the number a doctor already has before any model is involved, scored 0.6743 on the same
patients.

After: To score stage alone on the same patients, I fitted a Cox proportional hazards model, a regression model built
for survival data, to stage and nothing else on the 410 training patients, giving patients whose stage was not
recorded a level of their own. Stage alone scored 0.6743.

Before (the paragraph that introduces the baseline): The baseline is whatever a clinician already knows from TNM
staging, unaided.

After: The baseline is stage alone: whatever a clinician already knows from TNM staging, and nothing else.

Files: `results/metrics/05_baseline_stage.json`, `scripts/05_baseline_stage.py` and `scripts/survival_utils.py`.

Value found: under `pooled`, `"model": "Cox proportional hazards, stage only"`, `"features": ["pathological stage,
one-hot, reference Stage I, with an explicit unknown level"]`, `"penalizer": 0.01`, `"train": {"patients": 410,
"events": 129, ...}` and `"test": {"patients": 176, "events": 56, "concordance_index": 0.6743}`.
`05_baseline_stage.py` fits `CoxPHFitter(penalizer=0.01)` to the training rows and scores the test rows with
`predict_partial_hazard`. `stage_design` in `survival_utils.py` builds the levels, with `stage_unknown` for the 20
patients that `stage_distribution` counts as unknown. The fitted hazard ratios against stage I are 1.1142 for stage
II, 2.0265 for III, 6.4678 for IV and 2.7781 for unknown, so it was the fitted model that placed unstaged patients
between stages III and IV. The score was a model's output, and "before any model is involved" did not hold. The rule
in the rules box, stage alone on the same patients, is unchanged. For the same reason "unaided" was taken out of the
paragraph that introduces the baseline, which now gives the rule as `05_baseline_stage.json` records it under
`baseline_definition`: "The comparison this model has to beat is stage alone."

## 4. The colon-only check, both models refitted

Before: The first asked what happens when only colon cancer is considered, leaving out rectal cancer. On colon cases
alone, the model scored 0.7228 against 0.706 for stage.

After: The first asked what happens when only colon cancer is considered, leaving out rectal cancer. I refitted both
models on the 297 colon patients in the training set, 96 of whom had an event, and scored them on the 128 colon
patients held out, 42 of whom had one. The model scored 0.7228 against 0.706 for stage.

Before (front matter summary): On colon cases alone the gap narrowed to 0.7228 against 0.706 and could not be told
apart from chance, and adding tumour mutation count changed the concordance index by less than a hundredth.

After: With both models refitted on colon cases alone, the gap narrowed to 0.7228 against 0.706 and could not be told
apart from chance; adding tumour mutation count, tested on the 159 held-out patients who had it, changed the
concordance index by less than a hundredth.

Files: `scripts/07_final_gbm.py`, `scripts/05_baseline_stage.py`, `results/metrics/07_final_gbm.json`,
`results/metrics/05_baseline_stage.json` and `results/metrics/06_cv_gbm.json`.

Value found: `07_final_gbm.py` calls `fit_arm(frame[frame["project_id"] == "TCGA-COAD"].copy(),
cv["sensitivity_coad_only"]["selected"], "coad_only")`, which trains a new boosted model on the colon training rows,
and `05_baseline_stage.py` calls `fit_and_score(frame[frame["project_id"] == "TCGA-COAD"].copy(), "coad_only")`, which
fits a new stage model on them. Both metrics files give, under `sensitivity_coad_only`, `"train": {"patients": 297,
"events": 96, ...}` and `"test": {"patients": 128, "events": 42, ...}`, with test concordance 0.7228 for the boosted
model and 0.706 for stage. `06_cv_gbm.json` records the colon arm's own cross-validated selection on the same 297
patients and 96 events, which chose the same settings as the main arm. The 297 and 128 make up the 425 colon patients
of `results/metrics/02_censoring_audit.json`, with 138 events between them. The mutation half of the summary sentence
belongs to entry 6.

## 5. The pattern in the mutation counts, stated

Before: Of the 586 patients, 540 had this data, and the pattern in the numbers matched what is already known about
this type of cancer, so I trust the measurement.

After: Of the 586 patients, 540 had this data. Their mutation counts split into two groups, as expected in this
cancer: 77 of the 540 tumours, 14.3%, carry more than 10 mutations per megabase, which is the hypermutated fraction
already known in colorectal cancer. So I trust the measurement.

Files: `README.md`, Sensitivity arm: mutation burden, and `results/metrics/09_mutation_burden.json`.

Value found: the README: "540 of 586 patients have a sequenced tumour. The distribution is bimodal as expected:
median 2.3 mutations per Mb, 90th percentile 26.0, maximum 342.2, with 77 patients (14.3 per cent) above 10 per Mb,
which is the MSI-high and POLE hypermutator fraction." Under `distribution`, `"hypermutated_above_10_per_mb": 77` and
`"hypermutated_fraction": 0.1426`, out of the `"patients_with_mutation_data": 540` under `coverage`. The count is of
protein-altering (non-synonymous) variants per patient, divided by an assumed exome of 38 megabases (`definition`,
`"exome_mb_assumed": 38.0`).

## 6. The mutation count check, measured on the 159 held-out patients with mutation data

Before: Adding it changed the concordance index by less than a hundredth, and that change could easily be nothing at
all.

After: I refitted the model with and without mutation count on the patients who had it, and scored both on the 159 of
them held out, 52 with an event. Without mutation count the model scored 0.7243, and with it 0.7302. The difference,
0.0059, is less than a hundredth, and its 95% interval runs from negative 0.0055 to 0.0186. That takes in zero, so the
change could easily be nothing at all.

Files: `results/metrics/09_mutation_burden.json`, `scripts/09_mutation_burden.py` and `README.md`, Sensitivity arm:
mutation burden.

Value found: under `comparison`, `"test_patients": 159`, `"test_events": 52`, `"c_index_clinical_only": 0.7243`,
`"c_index_clinical_plus_burden": 0.7302`, `"difference": 0.0059`, `"difference_ci_95_paired_bootstrap": [-0.0055,
0.0186]` and `"difference_excludes_zero": false`. `09_mutation_burden.py` fits both models on the patients with a
sequenced tumour, `fit(with_tmb, cfg.PRIMARY_FEATURES, params, "without")` and `fit(with_tmb, cfg.PRIMARY_FEATURES +
["log_tmb"], params, "with")`, with the main arm's settings, and scores both on that subset's test rows: "This is a
smaller test set than the primary comparison and is not interchangeable with it." The 0.7243 is therefore not the
0.7289 of the main result, which was measured on all 176 held-out patients. "Less than a hundredth" holds. The front
matter summary was changed with this entry (see entry 4).

## 7. The outcome of the first warning, added

Before: Two of the warnings were also put to the test.

After: Then the four warnings. The first, that this cohort is not a random sample of cancer patients, cannot be tested
from within the cohort. Every number in this chapter describes these patients, not colorectal cancer patients in
general.

Files: `results/metrics/00_summary.json` and `README.md`, The four named failure modes.

Value found: under `day43_checks`, `cohort_selection_bias`, `"addressed": "Named in the README as a limit on external
validity. Not testable from within the cohort."` The README: "Not testable from inside the cohort. TCGA is not a
random sample of colorectal cancer patients, and every number here describes that population only." The chapter had
said that each warning would be checked and reported, and gave the outcome of two of the four.

## 8. The two features behind the second warning, named

Before: The second asked whether the model would find one real signal and report it as two or three separate
important features, making it look as if it used more information than it did. That one did happen.

After: The second warning asked whether the model would find one real signal and report it as two or three separate
important features, making it look as if it used more information than it did. That one did happen. The two most
important features were stage and pN, the lymph node category, and the two move together. Across the 566 patients
with both recorded, their rank correlation is 0.8289, where 1 would mean that they always rise together. They are
largely one fact about the patient, counted twice.

Files: `results/metrics/03_correlation_check.json`, `results/metrics/08_feature_importance.json`, `README.md` and
`posts/day45.txt`.

Value found: in `03_correlation_check.json`, `flagged_pairs` holds one pair, `"pair": ["stage_ordinal",
"pn_ordinal"], "n": 566, "spearman_rho": 0.8289`, the only pair at or above `"high_correlation_threshold": 0.7`,
computed on complete pairs. In `08_feature_importance.json`, the pooled arm's permutation importance on the 176
held-out patients puts `stage_ordinal` first at 0.0556 and `pn_ordinal` second at 0.038, with `age_at_diagnosis` third
at 0.0377. The README: "Pathological stage and pN category correlate at Spearman rho = 0.8289 across 566 patients. In
the permutation importance table, stage (+0.0556) and pN (+0.038) are the top two ranked features. They are
substantially one clinical fact reported twice, not two independent signals". The Day 45 text kept at the pinned
commit says "Cancer stage and lymph node status turned out to be very closely related to each other, and both showed
up as the two most important features in the model." The chapter says "largely one fact", as the README says
"substantially": a rank correlation of 0.8289 falls short of the 1 at which the two would always rise together.

## 9. The outcome of the third warning, added

Added, as a paragraph after the second warning's outcome: The third was the event count. Before fitting, I had fixed
a floor of 50 events, below which a result would carry a warning. The main split, colon and rectal cases together,
cleared it, with 129 events among the training patients and 56 among those held out. The colon-only test set did not.
It had 42, and at that number of events the colon gap cannot be told apart from chance.

Files: `scripts/config.py`, `results/metrics/02_censoring_audit.json`, `results/metrics/07_final_gbm.json` and
`scripts/07_final_gbm.py`.

Value found: `scripts/config.py` sets `MIN_EVENTS_WARNING = 50` under the comment "Threshold fixed before fitting, and
expected to fire on the test arm." `02_censoring_audit.json`, under `event_count_reliability`: `"threshold": 50`,
`"train_events": 129`, `"test_events": 56`, `"warning_active_train": false` and `"warning_active_test": false`.
`07_final_gbm.json` gives `"reliability_warning": false` for the pooled arm and `true` for `sensitivity_coad_only`,
whose test set has 42 events; `07_final_gbm.py` sets the flag when the test events fall below
`cfg.MIN_EVENTS_WARNING`. Under `comparison_against_baseline`, `coad_only` has `"difference_ci_95": [-0.0495, 0.0831]`
and `"difference_interpretation": "The 95 per cent interval on the difference includes zero. The boosted model ranks
better on these patients, but the improvement is not separable from chance at this number of events. Day 43's third
warning is the reason."` The README's paragraph on the third warning reports the main split only.

## 10. The fourth warning, no evidence found on a window widened from 90 to 365 days

Before: The fourth asked whether patients who are checked on more often, because a doctor is more concerned about
them, get a worse risk score simply from being watched more closely rather than from anything about their cancer.
That did not happen.

After: The fourth asked whether patients who are checked on more often, because a doctor is more concerned about them,
get a worse risk score simply from being watched more closely rather than from anything about their cancer. I found
no evidence that they did. The test I had fixed before looking at the data counted each patient's follow-up contacts
in the first 90 days after diagnosis, and asked whether that count predicted an event after those 90 days. It could
not run. Follow-up forms in these datasets are filed once a year, so only 4 of the 544 patients still at risk at 90
days had any contact inside the window. After seeing that, and before testing anything against outcome, I widened the
window to the first 365 days. Each extra contact in that year went with a hazard ratio of 0.455 for an event
afterwards. A hazard ratio of 1 would mean no effect at all, and the 95% interval around 0.455, from 0.1678 to 1.2341,
takes in 1.

Files: `results/metrics/04_followup_leakage_check.json`, `scripts/04_followup_leakage_check.py`, `scripts/config.py`
and `README.md`, Deviations from the pre-registration, item 2.

Value found: under `landmark_pre_registered`, `"landmark_days": 90`, `"pre_registered": true`,
`"patients_at_risk_at_landmark": 544`, `"patients_with_nonzero_intensity": 4`, `"testable": false` and the reason "Only
4 of 544 patients have any follow-up contact inside this window. TCGA follow-up forms are filed annually, so a 90-day
window carries almost no variance and cannot test the warning." Under `landmark_post_hoc`, `"landmark_days": 365`,
`"pre_registered": false`, `"patients_at_risk_at_landmark": 442`, `"events_after_landmark": 101`, `"unadjusted":
{"hazard_ratio": 0.455, "ci_95": [0.1678, 1.2341], "p_value": 0.1219, ...}`, `"leakage_detected": false` and the
justification "A 365-day window was chosen after seeing that, on the basis of variance in the intensity measure alone
and before any association with outcome was computed. It is post-hoc and is labelled as such." The `conclusion` block
reads "No evidence of follow-up intensity leakage.", with `"based_on_landmark_days": 365` and
`"based_on_pre_registered_window": false`. `scripts/config.py` sets `LANDMARK_DAYS = 90`, and the README says the
window "was fixed in `config.py` before the data was inspected". In `04_followup_leakage_check.py`, `landmark_test`
keeps the patients whose time is at least the landmark, counts each one's follow-up contacts from diagnosis to the
landmark, and fits a Cox model of the time after the landmark on that count; it returns without a test when fewer than
20 patients have any contact. The estimate adjusted for stage, pT, pN and age, 0.4822 with interval 0.1768 to 1.3147
on 426 patients, agrees and is not quoted in the chapter. The test fixed in advance never ran, so "That did not
happen" said more than the record shows. Entry 12 later changed the first two sentences of this passage.

## 11. What Chapter 5 does with a support vector machine

Before: Chapter 5 moves to support vector machines, the next step on that same standard progression.

After: Chapter 5 sets out to use a support vector machine, the next step on that same standard progression.

Files: Chapter 5's repository, `Qasim-Hussain-Code/tmao_cardiovascular_risk_prediction` at its pinned commit
`9985756c2db6`: `src/tmao_cvd/models.py`, `src/tmao_cvd/reanalysis.py` and `README.md`.

Value found: the sentence is Day 46's, written before Chapter 5 began. No file at that commit fits a support vector
machine. The two reported questions are fitted in `reanalysis.py` with `make_logistic_model` from `models.py`,
"Unpenalised logistic regression with imputation and standardisation" (`LogisticRegression(penalty=None, ...)`), and
with `_panel_model`, "L2 penalised logistic regression with the penalty chosen in-fold" (`LogisticRegressionCV(...,
penalty="l2", ...)`). A search of every text file at that commit for "svm", "svc", "support vector" and "kernel" finds
only `posts/day47.txt`, `posts/day50.txt`, `posts/day51.txt` and the README's table entry for `posts/day51.txt`, "Why a
support vector machine, and what the kernel does". The book's Chapter 5 says the support vector machine never ran, and
the preface and epilogue say Chapter 5 set out to use one; this sentence now says the same.

## 12. What the follow-up check tested

Before: The fourth asked whether patients who are checked on more often, because a doctor is more concerned about them,
get a worse risk score simply from being watched more closely rather than from anything about their cancer. I found
no evidence that they did.

After: The fourth asked whether being checked on more often, because a doctor was more concerned, itself went with a
worse outcome, so that the model could have learned the doctor's worry rather than anything about the cancer. I found
no evidence that it did.

File: `scripts/04_followup_leakage_check.py` at `85d831ca383c`.

Value found: the script's docstring quotes the warning ("That worry, not the tumour, can end up predicting outcome")
and says the test counts each patient's follow-up contacts up to a landmark date, "then asks whether it predicts what
happens after that date"; `landmark_test` (line 65) does exactly that, "Count contacts inside the window, then test
against what follows it", and reports a hazard ratio for later events. The test asks whether the number of contacts
predicts the outcome; it does not score the model's risk predictions, and the contact count is not one of the model's
features. The rest of the paragraph, which describes the 90-day and 365-day windows and the hazard ratio of 0.455,
already followed the record.

## 13. The censored patient with an undated recurrence

Before: The cohort is 586 patients from two public colorectal cancer datasets. Of these, 185 had an event: the cancer
came back, or the patient died. The other 401 had not, as of the last time anyone checked on them.

After: The cohort is 586 patients from two public colorectal cancer datasets. Of these, 185 had an event: the cancer
came back, or the patient died. The other 401 had no event with a date, as of the last time anyone checked on them.
One of them did have a recurrence on record, but without a date it could not start a clock, so that patient was
censored with the others.

Before (front matter summary): Gradient boosting with a Cox partial likelihood objective, trained to rank colorectal
cancer patients by their risk of recurrence or death in a cohort of 586, treating the 401 without an event as not yet
rather than never.

After: Gradient boosting with a Cox partial likelihood objective, trained to rank colorectal cancer patients by their
risk of recurrence or death in a cohort of 586, treating the 401 with no dated event as not yet rather than never.

Files: `README.md`, Cohort, `results/metrics/02_censoring_audit.json` and `scripts/02_build_cohort.py`.

Value found: the README: "Events are 117 recurrences and 68 deaths. Median follow-up is 608 days. One patient carries
a recurrence with no recoverable date and is censored." In `02_censoring_audit.json`, `recurrence_annotation_quality`
gives `"patients_with_dated_recurrence": 117` and `"patients_with_undated_recurrence": 1`, with the note "A recurrence
without a date cannot start a clock. Such patients are censored, which understates the event count."
`02_build_cohort.py` keeps a new tumour event record with no `new_tumor_event_dx_days_to` out of the dated recurrences
that can become an event, and counts `recurrence_undated` on the final cohort, after the thirty-day exclusion, so the
patient is one of the 586. The code would still have made a dated death the event, so it is the README's "is
censored" that places the patient among the 401. The sentence from Day 45 said that none of the 401 had had an event.
What the record does show for all 401 is that none has a dated recurrence or a dated death, since either would have
made the patient an event (Listing 4.2), so the sentence now says that, and the summary's "the 401 without an event"
now says "the 401 with no dated event" for the same reason. It does not say that this is the only exception:
`vital_status_audit` also counts `"patients_flagged_dead_with_no_date_anywhere": 1`, but `build()` takes that count
before the thirty-day exclusion, and no file says whether that patient is among the 586.

## 14. What the Cox partial likelihood judges

Before: Ask it for a risk score, and judge that score only by whether it puts patients in the right order.

After: Ask it for a risk score, and judge that score by how well it puts patients in the order in which their events
came.

Source: the definition of the partial likelihood, Cox, D. R. (1972), Regression models and life-tables, Journal of the
Royal Statistical Society, Series B, 34(2), 187-220.

Value found: the partial likelihood uses the follow-up times only through their order, but at each event it also depends
on how far the risk score of the patient who had the event stands above the scores of everyone still at risk. Only the
concordance index, defined in the chapter's note, is a pure count of pairs in the right order. "Only by whether"
described the concordance index rather than the objective. The next paragraph's account of the risk sets is unchanged.

## 15. Stage, grade and tumour size, correlated but not by construction

Before: Stage, grade and tumour size are correlated with each other by construction.

After: Stage, grade and tumour size are correlated with each other.

Sources: PDQ Adult Treatment Editorial Board, Colon Cancer Treatment (PDQ), Health Professional Version, National Cancer
Institute, updated 12 February 2025 and read on 2 October 2026,
https://www.cancer.gov/types/colorectal/hp/colon-treatment-pdq, section Stage Information for Colon Cancer, subsection
AJCC Stage Groupings and TNM Definitions, Tables 1 to 5, which reprint the stage groups and TNM definitions of the AJCC
Cancer Staging Manual, eighth edition, Colon and rectum (Amin, M. B., Edge, S. B., Greene, F. L. and others, editors,
Springer, 2017, pages 251-274); Maguire, A. and Sheahan, K. (2014), Controversies in the pathological assessment of
colorectal cancer, World Journal of Gastroenterology, 20(29), 9850-9861, https://doi.org/10.3748/wjg.v20.i29.9850;
Turkoglu, E. and others (2025), Prognostic impact of tumor size in patients with stage T3N1 colon cancer, Journal of
Clinical Medicine, 15(1), 247, https://doi.org/10.3390/jcm15010247. The manual itself was not read.

Value found: the stage group of a colorectal cancer is assigned from T (how far the primary tumour has invaded through
the bowel wall and beyond), N and M. The PDQ subsection begins "The AJCC has designated staging by TNM classification to
define colon cancer." Every stage group in its Tables 1 to 5, from 0 to IVC, is a combination of T, N and M categories
and nothing else: stage IIA is "T3, N0, M0" and stage IVA is "Any T, Any N, M1a". T1 to T4b are defined by how far the
tumour invades, for example "T3 = Tumor invades through the muscularis propria into pericolorectal tissues" and "T4b =
Tumor directly invades or adheres to adjacent organs or structures". Neither histological grade nor tumour size is an
input. The abstract of Maguire and Sheahan: "Many other histological features such as tumor budding, vascular invasion,
perineural invasion, tumor grade and rectal tumor regression grade that may be of prognostic value are not part of TNM
staging." Their paper predates the eighth edition, whose tables, as reprinted, still contain no grade. The abstract of
Turkoglu and others: "Tumor size is not included in the TNM staging system for colon cancer". Only stage and its own
components are related by construction, which the chapter says in the next paragraph ("Stage is built partly from those
two", pT and pN). Grade and size go with stage in practice, as the next sentence says, but not by construction. The
warning keeps its point: one clinical fact can be counted as several features.

## 16. What the mutation-count arm showed

Before: Mutation count did not help this model predict risk.

After: There is no evidence here that mutation count helped this model predict risk.

File: `results/metrics/09_mutation_burden.json` at 85d831ca383c.

Value found: "there is no evidence here that mutation burden adds ranking information beyond the clinical features",
with a difference of 0.0059 and a 95% interval of -0.0055 to 0.0186. The point estimate is above zero and the interval
takes in zero, so the record shows no evidence of help, not evidence that there was none. The sentence now says the
first, in the record's terms, as entry 10 did for the fourth warning.
