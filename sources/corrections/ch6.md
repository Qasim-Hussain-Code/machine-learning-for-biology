# Corrections for Chapter 6, Neoantigen immunogenicity for cancer vaccine design (neural network)

Each entry gives the chapter's sentence before and after the change, the repository file that settles it, and the
value found there. The repository is `Qasim-Hussain-Code/neoantigen_immunogenicity_prediction` at the chapter's pinned
commit `68a12d14824d` throughout, except where another repository is named. That commit is the head of the repository.

## 1. The expectation that immunogenic peptides would be the minority class

Before: The cohort came to 1,200 peptides, all confirmed to bind HLA-A*02:01. Of those, 606 were immunogenic and 594
were not.

After: The cohort came to 1,200 peptides, all confirmed to bind HLA-A*02:01. Of those, 606 were immunogenic and 594 were
not. The rules had been written expecting the immunogenic peptides to be the minority class, and the memorisation risk
rested on the same expectation. At 50.5% of the cohort they were a slim majority instead.

File: `results/metrics/01_cohort_composition.json`, with `README.md`.

Value found: under `outcome`, `"n_peptides": 1200`, `"n_immunogenic": 606`, `"n_assay_negative": 594`,
`"prevalence": 0.505` and `"chance_auprc": 0.505`. The README, Results: "The outcome is close to balanced at 606
immunogenic against 594 assay-negative, prevalence 0.505." The chapter's counts were already right. What the record
settles is that the pre-registered Metric rule, which calls the immunogenic peptides the minority class, and the fourth
failure mode, which calls the positive class small, were both written before the cohort existed and the cohort did not
bear them out: 606 of 1,200 is 50.5%, a slim majority. The rules box and the four ways this could be wrong are quoted
pre-registration and are left exactly as published; the outcome is now stated where the counts are given.

The caption of Figure 6.3, which is the book's own summary of those four and not a quotation, follows the same record.
Before: "and a small positive class invites memorisation". After: "and the model may learn the particular peptides
rather than the pattern behind them". The drawn figure names the fourth risk as memorisation and does not call the
positive class small.

## 2. Near-identical variants, common to the exception, and what the 13.7% counts

Before: I split by cluster rather than by peptide, since near-identical variants of the same epitope are common in this
data. A random split would have let 13.7% of validation peptides leak from training. The cluster split brought that to
zero.

After: I split by cluster rather than by peptide. Near-identical variants of the same epitope are not the rule in this
data: 1,061 of the 1,098 clusters hold a single peptide, and only 139 of the 1,200 peptides sit in a cluster with any
other. That small group is what a random split would have spread across both sides, leaving 13.7% of validation
peptides within two substitutions of a training peptide. The cluster split brought that to zero, and left 899 peptides
for training and 301 for validation, 146 of them immunogenic.

File: `results/metrics/02_cluster_split.json`, with `README.md`.

Value found: under `clusters`, `"n_peptides": 1200`, `"n_clusters": 1098`, `"singleton_clusters": 1061`,
`"peptides_in_non_singleton_clusters": 139`, `"largest_cluster": 33` and `"median_cluster_size": 1.0`. Under
`leakage_check`, `"validation_peptides_near_a_training_peptide_random_split": 0.136667` against
`"validation_peptides_near_a_training_peptide_cluster_split": 0.0`, with
`"definition": "within Hamming distance 2 of any training peptide"` and `"max_hamming": 2` at the top of the file,
which is what the 13.7% counts and why the chapter now says within two substitutions. The README, Results: "Most
peptides are alone: 1,061 clusters are singletons and only 139 peptides sit in a cluster with anyone else", and "A
small minority of the cohort drives the leak, and that minority is precisely where a model can memorise instead of
learn." The 13.7% is unchanged, and so is the reason for splitting by cluster; only the claim that near-identical
variants are common is replaced by the counts that measure how common they are.

## 3. The set the chance line is measured on, and the size of the split

Before: Chance there is 0.485, the fraction of those peptides that are immunogenic rather than of the cohort as a whole.

After: Chance there is 0.485, the fraction of the 301 validation peptides that are immunogenic, and not the 0.505 of the
cohort as a whole.

Before (front matter summary): A neural network was trained on peptides that all bind HLA-A*02:01, a cohort of 1,200
with 606 immunogenic and 594 not, split by sequence cluster rather than by peptide.

After: A neural network was trained on peptides that all bind HLA-A*02:01, a cohort of 1,200 with 606 immunogenic and
594 not, split by sequence cluster rather than by peptide into 899 peptides for training and 301 for validation, 146 of
those immunogenic.

Files: `results/metrics/02_cluster_split.json` and `results/metrics/05_baseline_validation.json`, with
`results/metrics/01_cohort_composition.json`.

Value found: under `split` in the cluster file, `"train_peptides": 899`, `"train_positive": 460`,
`"train_prevalence": 0.51168`, `"validation_peptides": 301`, `"validation_positive": 146`,
`"validation_prevalence": 0.48505` and `"shared_clusters": 0`. The baseline file records the same set under
`validation`: `"n": 301`, `"n_positive": 146`, `"prevalence": 0.48505` and `"chance_auprc": 0.48505`.
`04_selected_model.json` carries `"validation_prevalence": 0.48505` beside the network's score. The cohort's own
prevalence, in `01_cohort_composition.json`, is 0.505. So 0.485 is the prevalence of the 301 validation peptides, 146
of them immunogenic, and not of the 1,200.

## 4. The standard AUC the pre-registered rule promised

Before: (no value: the Metric rule promises AUPRC "reported alongside standard AUC", and no AUC appeared in the
chapter)

After: The standard AUC the rules promised beside the AUPRC puts the two in the same order. The selected network reached
0.665 on the validation peptides, and the binding-affinity baseline 0.629, against 0.5 for chance, which on that curve
does not move with the class balance.

Before (front matter summary): On the validation peptides the selected network scored 0.610 AUPRC against 0.591 for a
baseline that used binding affinity alone, with chance there at 0.485, and that margin of 0.019 is the size of the
network's own run-to-run variation.

After: On the validation peptides the selected network scored 0.610 AUPRC and 0.665 AUC against 0.591 and 0.629 for a
baseline that used binding affinity alone, with chance at 0.485 and 0.5, and that margin of 0.019 in AUPRC is the size
of the network's own run-to-run variation.

Files: `results/metrics/04_selected_model.json` and `results/metrics/05_baseline_validation.json`, with
`results/metrics/04_architecture_selection.json` and `README.md`.

Value found: `"mean_validation_auroc": 0.665073` for the selected feedforward network, the one with 64 hidden units,
averaged over its five seeds, beside `"mean_validation_auprc": 0.609655` and `"sd_validation_auprc": 0.019259`. In the
baseline file, under `validation`, `"auroc": 0.629342` with `"auroc_ci95": [0.565329, 0.693208]` and
`"chance_auroc": 0.5`. The README, Results: "its AUC-ROC is higher too, 0.681 against 0.665" for the interaction model
against the selected one, and "The binding-only baseline reaches 0.591 AUPRC ... with AUC-ROC 0.629, against the same
0.485 chance line." The chapter states the order of the two models on this curve and no more, because the AUC margin of
0.036 is wider than the network's seed-to-seed spread on that curve, `"sd_validation_auroc": 0.016144` in
`04_architecture_selection.json`, and so is not the matched pair the AUPRC margin is.

## 5. Why the final evaluation did not run, a paywall to the access record

Before: The validated data sits behind a paywall.

After: I could not get the table of validated peptides. The public Synapse deposit, syn21048999, holds only raw
whole-exome and RNA sequencing, with no peptide-level table in it. The table is published in the supplementary
material of the TESLA paper, and at PMC that download was blocked by a browser challenge, while Europe PMC would not
serve the article either, reporting it as not open access. A person can still fetch that file in a browser, and the
script that would score it is written and has been exercised on a synthetic table, so what is missing is the file
itself.

Before (front matter summary): The pre-registered final test on TESLA's tumour-derived peptides never ran, because the
validated data sits behind a paywall.

After: The pre-registered final test on TESLA's tumour-derived peptides never ran, because the table of validated
peptides could not be retrieved: the public deposit holds only raw sequencing, and the supplement that carries the
table was blocked by a browser challenge at PMC while Europe PMC refused the article as not open access.

File: `provenance/tesla_access.json`, with `README.md`.

Value found: `"status": "peptide-level TESLA data was NOT obtained. Stage 7 has not been run."` The logged accesses, in
order: the Synapse project syn21048999 is "public with zero access requirements", with folders named "lung cancer",
"melanoma 1", "melanoma 2"; a recursive listing found "only raw whole-exome and RNA sequencing (FASTQ, .bed) for the
three cohorts, 36 to 221 GB per cohort. There is no peptide-level immunogenicity table."; the attempt on "the seven
supplementary tables of the TESLA paper from PMC7652061, which is where the validated peptides are published" returned
"Blocked. PMC serves file downloads behind a proof-of-work browser challenge. Not circumvented."; and the Europe PMC
supplementaryFiles API for the same article was "Refused: 'Article with id PMC7652061 is not open access one'." The
same file records what would finish the evaluation: "The supplementary table of screened TESLA peptides, which a person
can download from the publisher or from PMC7652061 in a browser", and that stage 7 "is written, its scoring path has
been exercised on a synthetic table". The README's Limitations adds "a subscription at the publisher", which no logged
access tested, so the chapter names only the two blockers the access log records.

## 6. The cross-reference to Chapter 5, a model that ran to a design that did not

Before: Chapter 5 asked a support vector machine to find the widest boundary between two outcomes, using six numbers per
person. That works when the features are few and the relationship between them is fairly stable.

After: Chapter 5 took up a support vector machine, which finds the widest boundary between two outcomes. It was chosen
for six numbers per person, the abundances of the genes of one bacterial pathway, and that design never ran, because the
data it needed is not public. The approach works when the features are few and the relationship between them is fairly
stable.

Before (caption of Figure 6.1): The support vector machine of Chapter 5 works on a few stable features, while nine
interdependent peptide positions are the kind of input a network is built for.

After (the caption as it now stands, after the figure was drawn for the book): Why the model changes in this chapter.
The nine peptide positions do not act one at a time: change one and the meaning of another can change with it. A support
vector machine can be given those combinations by hand, while a network learns which of them matter from the data. The
caption no longer attributes a feature set to Chapter 5's support vector machine at all.

Files: `docs/reanalysis_plan.md`, `src/tmao_cvd/models.py` and `src/tmao_cvd/reanalysis.py` in Chapter 5's repository,
`Qasim-Hussain-Code/tmao_cardiovascular_risk_prediction` at its pinned commit `9985756c2db6`, with `chapters/ch05.md`.

Value found: the six numbers are the six gene abundances of the pathway that makes TMA, *cutC*, *cutD*, *cntA*, *cntB*,
*yeaW* and *yeaX*, which Chapter 5's rules box fixes as its features and which need shotgun metagenomics. That design
never ran: the same rules box records the change "because the data is not public", and Chapter 5 reports two other
models instead. Neither of those two is a support vector machine. `docs/reanalysis_plan.md`, section 6, question 1:
"Baseline model: log choline, log betaine, log carnitine. Extended model: baseline plus log TMAO. Estimator:
unpenalised logistic regression"; section 6, question 2: "Model: L2 penalised logistic regression on all 600
metabolites". The estimators those two files fit are `LogisticRegression` and `HistGradientBoostingClassifier` in
`models.py`, the second a stated sensitivity analysis, and `LogisticRegression` with `LogisticRegressionCV` in
`reanalysis.py`; no file in that repository fits a support vector machine, and the words appear only in the posts kept
under `posts/` and in the README's index of them. The cross-reference therefore no longer says the support vector
machine was given six numbers per person; it says the design that would have given it those six numbers never ran.

## 7. Six models, one of which never ran

Before: Six chapters have now used six models, and every one of them was handed the correct label during training and
asked to reproduce it, the last of them a network learning for itself which combinations of positions mattered.

After: Six chapters have now taken up six models, the fifth of them planned and never run, and every model that did run
was handed the correct label during training and asked to reproduce it, the last of them a network learning for itself
which combinations of positions mattered.

Files: `src/tmao_cvd/models.py`, `src/tmao_cvd/reanalysis.py` and `docs/reanalysis_plan.md` in Chapter 5's repository,
`Qasim-Hussain-Code/tmao_cardiovascular_risk_prediction` at its pinned commit `9985756c2db6`, with `chapters/ch05.md`.

Value found: no file in that repository fits a support vector machine, as entry 6 above records, so the fifth of the six
models was never trained on anything and could not have been handed a label. Chapter 5's own closing sentence says the
same: "That makes five chapters and five models, though the fifth was planned and never run." The recap the paragraph is
rewritten from counts six models and says that every one of them, without exception, was handed the correct label during
training; five of them were. The lesson is unchanged, because every model that did run was given the answer key and
Chapter 7 is the first that is not.

## 8. What the middle box of Figure 6.2 holds

Before (figure label, alt text and caption): "A T-cell response recorded"; "the box of peptides with a T-cell
response recorded"; "the peptides with a recorded T-cell response".

After: "Tested in a T-cell assay"; "the box of peptides tested in a T-cell assay, positive or negative"; "the peptides
that have been tested in a T-cell assay, positive or negative".

File: `results/metrics/01_cohort_composition.json` at `68a12d14824d`.

Value found: the cohort of 1,200 peptides holds 606 assay-positive and 594 assay-negative peptides
(`n_assay_negative 594`), so the box is every peptide with an assay result, not only those that provoked a response.
The old wording could be read as positives only, which would make the nesting wrong.

## 9. Why Chapter 5's design never ran (the cross-reference)

Before: ... and that design never ran, because the data it needed is not public.

After: ... and that design never ran, because the public data could not support it.

File: `README.md` in Chapter 5's repository at 9985756c2db6.

Value found: as sources/corrections/front.md entry 14. Chapter 5 says "that design never ran, because the public data
could not support it"; "not public" belongs to the later TMAO question.

## 10. The peptides whose assays point both ways

Before: (no sentence)

After: The label also hides a choice. A peptide counts as immunogenic if any one of its assays recorded a response, and
340 of the 1,200, 28.3%, have at least one assay that did and at least one that did not. All 340 are labelled
immunogenic, and every number in this chapter inherits that ambiguity.

Files: `results/metrics/01_cohort_composition.json`, `scripts/01_build_cohort.py` and `README.md` at 68a12d14824d.

Value found: `01_cohort_composition.json`, `outcome`: `"peptides_with_conflicting_assays": 340`,
`"conflicting_fraction": 0.283333` (28.3%) and `"label_rule": "immunogenic if at least one positive T-cell assay"`.
`01_build_cohort.py` sets the label from `n_positive_assays > 0` and counts as conflicting the peptides with at least
one positive and at least one negative assay. The README, Limitations: "340 peptides, 28.3 percent of the cohort, carry
both positive and negative assays and were labelled positive by the at-least-one-positive rule. Every number in this
README inherits that ambiguity." The chapter's first failure mode discusses assay negatives but never gave this count.
The new paragraph follows the counts it qualifies.
