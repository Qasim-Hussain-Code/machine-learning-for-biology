# Corrections for Chapter 2, What does a cell show to the immune system? (decision tree)

Each entry gives the chapter's sentence before and after the change, the repository file that settles it, and the
value found there. The repository is `Qasim-Hussain-Code/peptide_mhc_binding_prediction` at the chapter's pinned
commit `d701b62eb203` throughout.

## 1. The binder count in the corrected cohort, 4,957 to 4,958

Before: The corrected cohort is 11,723 measurements, 8,346 distinct peptides, and 4,957 that bound below 500
nanomolar. That is 42.29%, not 53.7%.

After: The corrected cohort is 11,723 measurements, 8,346 distinct peptides, and 4,958 that bound below 500
nanomolar. That is 42.29%, not 53.7%.

File: `results/metrics/01_cohort.json`, repeated in `results/metrics/00_summary.json`.

Value found: `"n_binders": 4958`, `"n_nonbinders": 6765`, `"n_measurements": 11723`, `"pct_binders": 42.29`. The two
class counts sum to the cohort total only at 4,958, and 4,958 of 11,723 is the 42.29% the chapter quotes in the same
sentence, where 4,957 would be 42.28%. The repository README repeats the 4,957 slip while quoting 42.29 percent.

The same count appears in the front matter summary and was changed with it, from "of which 4,957 bound below 500
nanomolar" to "of which 4,958 bound below 500 nanomolar".

## 2. The half-life count among the non-nanomolar rows, 1,770 to 2,225

Before: 1,770 half-lives. 1,087 unitless figures. 333 melting temperatures. 219 interatomic distances.

After: 2,225 half-lives. 1,087 unitless figures. 333 melting temperatures. 219 interatomic distances.

File: `results/metrics/01_cohort.json`, unit census, with the same table in `README.md`.

Value found: `"units_seen_before_filter": {"nM": 11723, "min": 2225, "°C": 333, "angstroms": 219, "1/s": 8, "1/M": 2}`,
against `"n_dropped_wrong_units": 3874`. The README's unit table gives the same row as "| min | 2,225 | Complex
stability, dissociation half-life |". At 1,770 the four counts in the sentence account for 3,409 of the 3,874
non-nanomolar rows named in the sentence before them; at 2,225 they account for 3,864, with the remaining ten rows
being the 8 dissociation rate constants and 2 association constants in the census, which the chapter does not list.

## 3. The two depth-sweep scores, 0.7079 and 0.7153, to 0.7095 and 0.7118

Before: Eight questions deep scores 0.7079. Thirteen questions deep scores 0.7153.

After: Eight questions deep scores a cross-validated F1 of 0.7095. Thirteen questions deep scores 0.7118. Both are the
one-hot tree.

File: `results/metrics/05_cv_onehot.json`.

Value found: at `"max_depth": 8`, `"cv_f1_mean": 0.709492`; at `"max_depth": 13`, `"cv_f1_mean": 0.711826`. Each of the
chapter's two figures comes from a different file. 0.7079 is the ordinal encoding's cross-validated F1 at depth eight,
`results/metrics/05_cv_ordinal.json`, `"cv_f1_mean": 0.707857`, carried into
`results/metrics/06_final_ordinal.json` as `"cv_f1_at_best_depth"`. 0.7153 is the one-hot tree's held-out test F1,
`results/metrics/06_final_onehot.json`, `"test_f1": 0.715285`, which is the same value the chapter quotes two sections
earlier as the test result. The section compares two points on the one-hot cross-validation curve, and both corrected
values sit on it, which is also what makes the chapter's next sentence, that both numbers are in the repository, true:
there is no test F1 at depth eight for the one-hot tree anywhere in the record. The held-out numbers at the other depths
are all accuracies: the train and test accuracies `pipeline.py` section 14 plots in `figures/04_overfitting_curve.png`
for depths one to twenty, and `"test_accuracy": 0.778909` at unlimited depth in
`results/metrics/07_onehot_unlimited.json`, which is the 0.7789 the chapter quotes in the same section. The repository
README repeats the depth-eight slip but gives the depth-thirteen value correctly, as 0.7118.

## 4. The gain across the plateau, 0.0074 to 0.0023

Before: Depth eight to depth thirteen buys 0.0074. Five extra levels of questions for seven thousandths.

After: Depth eight to depth thirteen buys 0.0023. Five extra levels of questions for two thousandths.

File: `results/metrics/05_cv_onehot.json`.

Value found: 0.711826 minus 0.709492 is 0.002334. The gap follows from correction 3 and was changed with it. The
README gives the gap as 0.0039, computed from its own 0.7079 for depth eight, which is the ordinal file's value.

## 5. The peptides the printed tree was fitted on, 8,346 to 6,971

Before: It was given 8,346 peptides, nine letters each, and 180 columns.

After: The grouped split put 6,971 of the 8,346 peptides on the training side and the other 1,375 on the test side.
The tree was given those 6,971 training peptides, nine letters each, and the same 180 columns.

Files: `pipeline.py` section 13, and `results/metrics/06_final_onehot.json`.

Value found: section 13 fits the tree whose questions the chapter then lists on the training indices alone,
`clf_oh.fit(ENCODINGS["onehot"][tr_idx], y[tr_idx])`, and writes its rules to
`results/metrics/08_onehot_tree_rules.txt`, whose first splits are `pos2_L`, `pos2_M`, `pos9_V`, `pos2_I` and
`pos9_L`, exactly as the chapter reports them. `results/metrics/06_final_onehot.json` gives `"n_train": 6971` and
`"n_test": 1375`. 8,346 is the size of the deduplicated cohort before the grouped split, which the chapter gives
correctly elsewhere.

## 6. The depth sweep ran before the evaluation split was drawn

Before: So I tested every depth from one to twenty, five times each, on peptides held back from different proteins each
time, and kept the depth with the best cross-validated F1. That is what the pipeline did, before I looked at the test
set. Thirteen won.

After: So I tested every depth from one to twenty, five times each, on peptides held back from different proteins each
time, and kept the depth with the best cross-validated F1. Thirteen won. The sweep ran over all 8,346 peptides, and the
training and test split was drawn after it, so the 1,375 test peptides sat inside the folds the depth was chosen on. The
trees scored earlier in this chapter were fitted on the training peptides alone, and every fold of the sweep held its
own peptides back while its tree was fitted, but the depth those trees were given had been chosen over a cohort that
included the test peptides. Of everything I report, the depth is the one choice the test set helped make.

Files: `pipeline.py` sections 11 and 12, and `results/metrics/06_final_onehot.json`.

Value found: section 11, the depth sweep, calls `cross_validate(clf, X, y, groups=grp, cv=GKF, scoring=[...])` on the
whole encoded cohort, `X` and `y` being the 8,346 deduplicated peptides built in sections 8 and 9, and writes
`results/metrics/05_cv_*.json` from it. Only then does section 12 draw the evaluation split,
`tr_idx, te_idx = next(gss.split(seqs, y, groups=grp))` with `GroupShuffleSplit(n_splits=1, test_size=0.2)`, and select
each encoding's depth as the maximum of the already computed `cv_f1_mean`. `results/metrics/06_final_onehot.json` gives
`"n_train": 6971` and `"n_test": 1375`, and those 1,375 test peptides are part of the 8,346 the sweep scored. The
repository README says the opposite, that depth is chosen "on the training data ... and only then is the test set
touched, once"; the code is the record of what ran, so the chapter follows the code. The fitting inside each fold is
unaffected: `cross_validate` fits on four folds and scores the fifth, and section 13 fits the reported trees on
`X[tr_idx]` alone.

## 7. The note naming the expected winning encoding was never written

Before: All three go in the repository (Figure 2.3), and I said I would write down which one I expected to win before
any of them had a score. A choice made after seeing the scores is not really a choice.

After: All three go in the repository (Figure 2.3), and I said I would write down which one I expected to win before any
of them had a score, because a choice made after seeing the scores is not really a choice. I never wrote it. The
pipeline did not run for several days, and when it did, there was nothing on record saying which encoding I had backed.

File: `README.md`, under the known limitations.

Value found: "**No pre-registration file was written.** An early post committed to recording the expected winning
encoding before any score was seen. The pipeline did not run until several days later and that file was never created.
The stated expectation was one-hot; the physicochemical encoding won. This is recorded as an unmet commitment, not as a
prediction." No such file exists in the repository at the pinned commit. The dates agree: the post making the
commitment is Day 14, 6 August 2026, and `results/metrics/01_cohort.json` gives `"pipeline_date": "2026-08-10"`. The
Day 14 post commits to writing the expectation down without naming an encoding, and "I expected one-hot to win. It did
not." appears only in the later post that also reports the corrected cohort, after the scores were in. That sentence is
kept, with "I am saying so after the scores, and without the note I said I would write, so it is not a prediction."
added after it, so that the chapter does not assert an expectation it has already said was never recorded.

## 8. What Chapter 1 gave before any DNA was read, twenty free points to 79.32%

Before: Chapter 1 handed me twenty free points before I read a single base of DNA. This time guessing gets me nothing.

After: In Chapter 1, guessing susceptible every time was right 79.32% of the time before I read a single base of DNA.
This time, guessing gets me nothing.

File: `results/metrics/model_results_ciprofloxacin.txt` in the Chapter 1 repository,
`Qasim-Hussain-Code/campylobacter_amr_phenotype_prediction` at that chapter's pinned commit `0e2b3df4c587`.

Value found: "test set is 20.7% resistant, so the majority-class floor on test is 0.7932", with the baseline row giving
accuracy 0.7932 on the training and the test side alike. The twenty points are what the rule about *gyrA* position 86
earned above that floor, 99.67% against 79.32%, which Chapter 1 reports as "That beats the floor by twenty points".
What guessing handed over before any DNA was read is the floor itself.

## 9. The third encoding's second property, volume to molecular weight

Before: The third option is to describe each amino acid instead of naming it. Hydrophobicity, volume and charge become
the columns, three numbers for every position and twenty-seven in all, and similar residues then get similar numbers.

After: The third option is to describe each amino acid instead of naming it. Hydrophobicity, molecular weight and
charge become the columns, three numbers for every position and twenty-seven in all. Molecular weight stands in for the
size of the residue, and similar residues then get similar numbers.

File: `pipeline.py` sections 3 and 9.

Value found: section 3 defines three lookup tables, `KD` ("Kyte-Doolittle"), `MW` ("residue molecular weight (Da)",
A=89.09 through W=204.23) and `CH` ("charge pH 7.4"), and section 9 builds the physicochemical encoding from exactly
those three, `row += [KD.get(aa, 0.0), MW.get(aa, 0.0), CH.get(aa, 0.0)]`. The repository holds no residue volume
table. The same change was made in the front matter summary, from "27 columns of hydrophobicity, volume and charge" to
"27 columns of hydrophobicity, molecular weight and charge", in the list of scores under "What a score is worth", and in
the alt text of Figure 2.3. The Listing 2.1 caption already named the three tables correctly.

## 10. The opening counts are the first download, before the units were checked

Before: One MHC molecule, HLA-A*02:01, the most studied variant in the world. 15,597 laboratory measurements. 9,142
distinct fragments. 53.7% of the measurements are binders, which is almost exactly a coin flip.

After: One MHC molecule, HLA-A*02:01, the most studied variant in the world. The first download gave 15,597 laboratory
measurements and 9,142 distinct fragments, and 53.7% of those measurements were binders, which is almost exactly a coin
flip. Those counts are the download as it arrived, before I checked which unit each measurement was in, and the
corrected cohort, smaller and with a lower share of binders, comes later in this chapter.

Files: `README.md` and `results/metrics/01_cohort.json`.

Value found: "My own feasibility scan, run before the pipeline existed, reported 15,597 measurements at 53.7 percent
binders and I carried that figure forward as settled. It was not", and, under the known limitations, "The feasibility
scan reported 53.7 percent binders and that figure appeared in four posts before the unit contamination was found. The
correct rate is 42.29 percent at measurement level and 37.3 percent after deduplication." The cohort file gives
`"n_measurements": 11723`, `"pct_binders": 42.29` and `"n_dropped_wrong_units": 3874`, and 11,723 plus 3,874 is the
15,597 of the first download. The 53.7% is a share of measurements and not of distinct peptides: 8,376 of the 15,597
rows fell below 500, being the 4,958 nanomolar binders plus the 3,418 rows in other units that also fell below 500.

## 11. The vaccinia epitope count, a year and a reference added

Before: One awkward peptide would be a footnote. Sidney and colleagues counted fourteen A*0201 epitopes in vaccinia
virus. Eight of them did not fit the rule (Figure 2.4).

After: One awkward peptide would be a footnote. Sidney and colleagues counted fourteen A*0201 epitopes in vaccinia
virus and reported in 2008 that eight of them did not fit the rule (Figure 2.4).

Source: Sidney, J., Assarsson, E., Moore, C., Ngo, S., Pinilla, C., Sette, A. and Peters, B. (2008). Quantitative
peptide binding motifs for 19 human and mouse MHC class I molecules derived using positional scanning combinatorial
peptide libraries. *Immunome Research*, 4, 2. https://doi.org/10.1186/1745-7580-4-2

Value found: the paper's own text reads "Indeed, in a recent study we observed that 57% (8/14) of the HLA-A*0201
restricted vaccinia-derived epitopes identified did not conform with the A*0201 motif derived by pool sequencing
analysis", in the paragraph that also gives GILGFVFTL as an A*0201 epitope lacking leucine or methionine at position
two. The count is the authors' own, written as "we", so the chapter's attribution to Sidney and colleagues holds, and
the entry has been added to the chapter's References. The epitopes themselves were identified in the study that
sentence cites, reference 4 of the same paper, Pasquetto and colleagues, *Journal of Immunology*, 2005;175(8):5504,
which the chapter does not name because the posts do not. The paper carries no retraction, correction or editorial
notice.

## 12. The two class counts of the first download are what a threshold selected, not what bound

Before: Put every measurement in one pile. 15,597 laboratory measurements on this molecule, 8,376 that bound and 7,221
that did not.

After: Put every measurement in one pile. 15,597 laboratory measurements on this molecule, 8,376 counted as binders and
7,221 not.

Files: `results/metrics/01_cohort.json` and `README.md`.

Value found: `"n_binders": 4958` and `"n_dropped_wrong_units": 3874`, with the README's unit section recording that "Of
the 3,874 non-nM rows, 3,418 fall below 500 and would be counted as binders". Of the 8,376 rows of the first download
that fell below 500 on the quantitative measurement column, 4,958 were affinity measurements in nanomolar and the other
3,418 were half-lives, melting points and interatomic distances, which the chapter sets out two sections later. The two
counts are unchanged, 8,376 being what a threshold of 500 on that column selected and 7,221 the remainder, and the
sentence no longer says that the 8,376 bound. The chapter's opening already marks these counts as the download before
the units were checked.

## 13. What the tree's score is called (the note beside "How a tree chooses, and what stops it")

Before: **Information gain.** The amount by which a question tidies the two piles it creates. The tree keeps the
question with the most of it.

After: **Impurity.** How mixed a pile is. A question is scored by how much it lowers the impurity of the two piles it
creates, and the tree keeps the question with the largest drop. The trees in this chapter measure impurity with the
Gini index, which is scikit-learn's default.

File: `pipeline.py` at `d701b62eb203`, lines 440, 488, 518, 533 and 620.

Value found: every tree is built as `DecisionTreeClassifier(max_depth=..., random_state=RNG)` with no `criterion`
argument, and scikit-learn's default criterion is `"gini"`, the Gini impurity decrease. Day 15 called the score
information gain, which is the entropy-based measure the trees did not use. The chapter's description of what the
score does (how much a question tidies the piles) is unchanged.

## 14. Which model stayed at 99.65% when families sat on both sides of a split (the Chapter 1 cross-reference)

Before: Chapter 1 had the same problem and got away with it. 344 groups of closely related *Campylobacter* isolates sat
on both sides of a random split, and it changed nothing: the accuracy stayed at 99.65% correct.

After: Chapter 1 had the same problem and got away with it. 344 groups of closely related *Campylobacter* isolates sat
on both sides of a random split, and it changed nothing: the one question about position 86 was still right 99.65% of
the time.

File: `results/metrics/cross_validation_ciprofloxacin.txt` in the Chapter 1 repository,
`Qasim-Hussain-Code/campylobacter_amr_phenotype_prediction` at that chapter's pinned commit `0e2b3df4c587`.

Value found: `Features: 58`, `Rule: ['gyrA_T86A=POINT', 'gyrA_T86I=POINT', 'gyrA_T86V=POINT']`, `5-fold, repeated 5
times`; under RANDOM FOLDS `rule 0.9965` and `logistic 0.9961`, and under GROUPED FOLDS `rule 0.9965` and `logistic
0.9960`. The 99.65% is the one question's score under both schemes, not a fitted model's, which is how Chapter 1 now
reads it and what entry 16 of `sources/corrections/ch1.md` records from the same file. Day 16 gives the number as "the
accuracy" without saying whose. The sentence that follows, about the model having found the one position, is unchanged:
it is about the regression, which moved from 0.9961 to 0.9960 and so also changed nothing.
