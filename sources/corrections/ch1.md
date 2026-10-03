# Corrections for Chapter 1, Predicting antibiotic resistance from a genome (logistic regression)

Each entry gives the chapter's sentence before and after the change, the repository file that settles it, and the
value found there. The repository is `Qasim-Hussain-Code/campylobacter_amr_phenotype_prediction` at the chapter's
pinned commit `0e2b3df4c587` throughout.

The figures were later drawn for the book as `figures/svg/fig-1-1.svg` to `figures/svg/fig-1-8.svg`, with new captions
and alternative text. Entries 1, 5, 6, 7, 12 and 14 quote captions, alternative text or image labels from when the
figures were the series' images in `figures/web/`. As the chapter now stands, Figure 1.1 shows only the supervised and
unsupervised tables and carries no score, Figure 1.8 gives the regression its cross-validated 99.60%, no caption or
alternative text names the species, the caption of Figure 1.3 no longer gives the weights, and Figures 1.2 and 1.4 and
their captions carry the corrected values and wording.

## 1. The weight on the isoleucine change at position 86, 8.9 to 8.845

Before: It gave position 86 a weight of 8.9. It gave a real gyrase mutation 2.364.

After: It gave the isoleucine change at position 86 a weight of 8.845. It gave a real gyrase mutation, the valine change
at the same position, 2.364.

Files: `results/metrics/model_results_ciprofloxacin.txt`, and the footer of `posts/day-03.md`.

Value found: under GROUPED SPLIT, "largest logistic coefficients", `+8.845  gyrA_T86I=POINT`, `+2.364  blaOXA-493` and
`+2.364  gyrA_T86V=POINT`. The post's own footer maps the number to that line: "weight of 8.9 ... 2.364, twice
(grouped split; 8.9 is printed as +8.845)". To one decimal place 8.845 is 8.8, so 8.9 came from rounding twice. The
sentence's two 2.364 values come from the same grouped-split fit, and Figure 1.2 beside it prints `gyrA T86I 8.845`.
Naming the two changes (isoleucine for 8.845, valine for the gyrase mutation at 2.364) follows the labels in the same
figure, `gyrA T86I` and `gyrA T86V`, and is a clarification rather than a correction.

## 2. The isolates that fall into clusters, 3,984 to 3,520

Before: My 3,984 isolates fall into 1,128 clusters.

After: Of my 3,984 isolates, 3,520 fall into 1,128 clusters, and the other 464 have no cluster assignment.

Files: `results/metrics/cohort_summary_ciprofloxacin.txt`, with the same statement in `README.md`.

Value found: under "SNP cluster structure", `isolates with a cluster: 3,520`, `isolates without: 464`,
`distinct clusters: 1,128`. The README: "464 isolates have no cluster assignment and are treated as singleton groups
when splitting." Listing 1.1, quoted in the same section, handles those 464.

## 3. The isolates with a nalidixic acid result, every isolate to 3,816

Before: The explanation came from a second drug. Every isolate here was also tested against nalidixic acid, the
original quinolone, in clinical use since the 1960s. Ciprofloxacin came later. It is a fluoroquinolone, a far more
potent version of the same idea, aimed at the same enzyme. All four alanine isolates are resistant to nalidixic acid.

After: The explanation came from a second drug, nalidixic acid, the original quinolone, in clinical use since the 1960s.
Ciprofloxacin came later. It is a fluoroquinolone, a far more potent version of the same idea, aimed at the same
enzyme. The NCBI release that supplied these genomes also holds nalidixic acid results for 3,816 sequenced isolates,
the four alanine isolates among them. All four are resistant to nalidixic acid.

Files: `results/metrics/provenance_nalidixic_acid.txt`, `results/metrics/variant_table_nalidixic_acid.txt`,
`results/metrics/cohort_summary_ciprofloxacin.txt` and `scripts/02_build_cohort.py`.

Value found: `NCBI Pathogen Detection release: PDG000000003.2859` and `Cohort size: 3,816 isolates` for nalidixic
acid, against `Cohort: 3,984 isolates` for ciprofloxacin from the same release. The variant table gives
`Cohort: 3,816 isolates, 797 resistant`, `gyrA_T86A=POINT  4  4  0` and `gyrA_T86I=POINT  775  772  3`, against 810
isoleucine isolates in the ciprofloxacin cohort. `scripts/02_build_cohort.py` admits an isolate to a drug's cohort only
when it has an interpretable result (S, I or R) for that drug and a genome assembly, and every ciprofloxacin isolate has
an assembly, so at least 168 of the 3,984, including at least 35 of the 810 isoleucine isolates, have no usable
nalidixic acid result. All four alanine isolates do have one. The nalidixic acid variant table counts four
`gyrA_T86A=POINT` isolates, and NCBI's BioSample records for the four in the ciprofloxacin cohort (SAMN12087875,
SAMN13836751, SAMN16231212 and SAMN16231145, for `GCA_007913865.1`, `GCA_010310705.1`, `GCA_014723015.1` and
`GCA_014721345.1`, read on 2 October 2026) each record nalidixic acid resistant at an MIC of 64 mg/L or more and
ciprofloxacin susceptible at 0.5 mg/L. So the argument of the section stands. This settles the earlier question about
775 against 810.

## 4. What the tetracycline hypothesis rule counts as broken, partial copies to partial or mistranslated copies

Before (rules box): **Tetracycline, kept in the repository as a hypothesis.** The same rule, with *tet(O)* counted as
absent where the annotation reports only a partial copy, because the mechanism says a truncated protein cannot work.

After (rules box): **Tetracycline, kept in the repository as a hypothesis.** The same rule, with *tet(O)* counted as
absent where the annotation reports only partial copies or copies broken by an internal stop or a frameshift, because
the mechanism says a truncated protein cannot work.

Before (text): Separate them, and 99.32% becomes 99.45%. That is five isolates out of 3,983.

After (text): Separate them, and 99.32% becomes 99.45%. That is five isolates out of 3,983: the four that carry only a
fragment, and one whose only copies are a fragment and a copy broken by an internal stop or a frameshift.

Files: `scripts/12_test_refined_features.py`, `results/metrics/refined_features_tetracycline.txt` and `README.md`.

Value found: the script sets `BROKEN_QUALS = {"PARTIAL", "MISTRANSLATION"}`, and its docstring defines
`MISTRANSLATION    internal stop or frameshift detected`. The metrics file gives `intact tet call  1889  13  9  2072
0.9945` and "intact tet call: 5 isolates change, 5 now correct, 0 now wrong". Four of the five carry `tet(O)=PARTIAL`
as their only *tet* call; the fifth is `[S] GCA_008897765.1  blaOXA-193,tet(O)=MISTRANSLATION,tet(O)=PARTIAL`. The
README: "requiring an intact call, excluding =PARTIAL and =MISTRANSLATION but retaining =PARTIAL_END_OF_CONTIG, gives
0.9945". A rule that discarded partial copies alone would change four isolates, not five, and would not reach 99.45%.
The chapter's "Nine of the fourteen are still unexplained" is fourteen less these five.

## 5. The gyrase mutation carried by the five blaOXA-493 isolates, named (a clarification)

Before: Every one also carries a gyrase mutation, with no exceptions.

After: Every one also carries a gyrase mutation, the valine change at position 86, with no exceptions.

Files: `results/metrics/discordant_ciprofloxacin.txt` and `results/metrics/model_results_ciprofloxacin.txt`, with
Figure 1.2 (`figures/web/day-04.jpeg`).

Value found: under "RESISTANT on the plate, no gyrA_T86I detected", the five isolates that carry the gene,
`GCA_005199195.1`, `GCA_005326385.1`, `GCA_005326525.1`, `GCA_005333285.1` and `GCA_018175995.1`, each have the full
genotype string `blaOXA-493,gyrA_T86V=POINT`, so none of them carries the isoleucine change. The grouped-split weights
the section turns on are `+2.364  blaOXA-493` and `+2.364  gyrA_T86V=POINT`, and Figure 1.2 sets `gyrA T86V 2.364`
beside `blaOXA-493 2.364`. The posts say only "a gyrase mutation". Without the name, a reader who takes the mutation to
be the isoleucine change at 8.845 cannot make "the model split the credit, 2.364 each" add up. As in entry 1, naming the
change is a clarification rather than a correction.

## 6. The logistic regression on all 84 genes, given its own cross-validated score

Before (text): The logistic regression, with all 84 genes to draw on, did not beat the one question.

After (text): The logistic regression, with all 84 genes to draw on, did not beat the one question. Its score is
cross-validated, averaged over repeated divisions of the data and each time measured only on isolates held back from its
training. It was right 99.60% of the time, and 99.57% when whole families of related genomes were held back together.
The rule has nothing to fit, so it scores 99.67% either way.

Before (summary): and a logistic regression given all 84 resistance genes does no better.

After (summary): and a logistic regression given all 84 resistance genes does no better, at 99.60% under
cross-validation.

Before (What survives): One feature is right 99.67% of the time across 3,984 isolates, and eighty-four features do no
better.

After (What survives): One feature is right 99.67% of the time across 3,984 isolates, and eighty-four features do no
better, at 99.60% under cross-validation.

Before (Figure 1.1 alt text): one feature at gyrA position 86 at 99.67% and all 84 resistance genes at 99.67%

After (Figure 1.1 alt text): one feature at gyrA position 86 at 99.67% and all 84 resistance genes in a logistic
regression at 99.60% under cross-validation

Files: `results/metrics/threshold_sweep_ciprofloxacin.txt` and `README.md`, with the footer of `posts/day-03.md`.

Value found: `Vocabulary: 84 distinct gene entries`, `Scheme: 5-fold x 3 repeats = 15 folds per scheme`, and the row for
a minimum count of 1, `1  84  4  0.9967  0.9960  0.9967  0.9957  6` (rule random, logistic random, rule grouped,
logistic grouped). The README: "Fitted on those, logistic regression reaches 0.9960 under random cross-validation and
0.9957 under grouped, against 0.9967 for the rule". The day-03 footer ties "all 84 resistance genes" to the vocabulary
at rarity threshold 1. No file gives 99.67% for the 84-gene regression: the third bar of `figures/web/day-03.jpeg`
repeats the rule's score, and the day-11 image gives the regression 99.60%. The image file itself is left for the
redrawing of the figures.

## 7. The model and the split behind the weights

Before (text): The logistic regression's weights showed the next problem. It gave the isoleucine change at position 86 a
weight of 8.845.

After (text): The weights showed the next problem. I read them from the same kind of model fitted to a narrower table,
the 58 genes found in at least three isolates, using the training isolates of a split that kept families of related
genomes together. The chapter comes back to both choices. That model gave the isoleucine change at position 86 a weight
of 8.845.

Before (text): So the model split the credit, 2.364 each, because it had no other option.

After (text): Trained with families kept together, the 58-gene model split the credit, 2.364 each, because it had no
other option.

Before (text): In the random split its weight was 1.469. In the grouped split, which gave the weights quoted earlier, it
was 2.364. Splitting by family did not remove it, and it could not.

After (text): Three of the eight valine isolates carry no *blaOXA-493*. The random split left valine isolates without
the gene on the training side, so the 58-gene model could give the valine change more of the credit: 3.689, against
1.469 for the beta-lactamase. The grouped split, which gave the weights quoted earlier, held all three back for testing,
so the model never saw the two apart and paid them 2.364 each. Splitting by family did not remove the gene's weight, and
it could not.

Before (Figure 1.2 caption): The model gives the beta-lactamase the same weight as a real gyrase mutation, 2.364.

After (Figure 1.2 caption): Trained with families kept together, the logistic regression on the 58 genes found in at
least three isolates gives the beta-lactamase the same weight as a real gyrase mutation, 2.364.

Before (Figure 1.3 caption): while the weight on <i>blaOXA-493</i> goes from 1.469 to 2.364.

After (Figure 1.3 caption): while the weight on <i>blaOXA-493</i> in the 58-gene logistic regression goes from 1.469 to
2.364.

Before (summary): the model pays a beta-lactamase the same weight as a real gyrase mutation because the gene never
appears without the mutation,

After (summary): a regression on the 58 genes found in at least three isolates, fitted with families of related genomes
kept together, pays a beta-lactamase the same weight as the gyrase mutation it always travels with;

Before (What survives): The model paid a gene that cannot touch the drug the same as a real gyrase mutation, because the
gene never appears without the mutation, and hiding whole families did not fix it.

After (What survives): The regression on the 58 genes found in at least three isolates paid a gene that cannot touch the
drug, because the gene never appears without a real gyrase mutation. Hiding whole families did not fix it. With families
kept together, the regression paid the two the same.

Files: `results/metrics/model_results_ciprofloxacin.txt`, `results/metrics/threshold_sweep_ciprofloxacin.txt`,
`results/metrics/cross_validation_ciprofloxacin.txt`, `results/metrics/discordant_ciprofloxacin.txt`,
`scripts/06_build_features.py` and `scripts/08_train_models.py`.

Value found: `model_results_ciprofloxacin.txt` opens with `Features: 58`, the count the sweep gives for a minimum of 3
(`3  58  3 ...`), against 84 at a minimum of 1, and no 84-feature fit prints a weight. Under RANDOM SPLIT (train 2,988,
test 996): `+8.947  gyrA_T86I=POINT`, `+3.689  gyrA_T86V=POINT`, `+1.469  blaOXA-493`. Under GROUPED SPLIT (train
3,082, test 902): `+8.845  gyrA_T86I=POINT`, `+2.364  blaOXA-493`, `+2.364  gyrA_T86V=POINT`. The fit on all isolates
gives 3.92 and 1.90 (`cross_validation_ciprofloxacin.txt`, co-occurrence table). In `discordant_ciprofloxacin.txt` five
of the eight `gyrA_T86V=POINT` isolates carry `blaOXA-493`; the other three, `GCA_005289865.1`, `GCA_005361245.1` and
`GCA_004876765.1`, do not, and all eight are resistant. The split assignments are not kept in `results/metrics/`, so the
sides follow from the weights. `08_train_models.py` fits scikit-learn's default logistic regression (L2 penalty, C = 1)
to the training rows. Because every `blaOXA-493` isolate carries the valine change, at the fitted optimum the valine
weight exceeds the gene's by the summed shortfall (1 minus the predicted probability) of the resistant training isolates
that carry the valine change without the gene, so the two weights are equal only if no such isolate is in training. A
simulation with the same estimator showed one such isolate separating the two weights by about 0.7. The grouped weights
are equal, so all three were on the test side; the random weights differ by 2.220, more than one isolate's shortfall can
supply, and the regression there calls three more resistant training isolates susceptible than the rule does (611
against 614 found). The grouped counts agree: the rule finds 610 and 206 resistant isolates (train, test) and the
regression 606 and 202, so four valine isolates sit on each side, all called susceptible.

## 8. What the model does with blaOXA-493 alone

Before: The model calls it resistant, and the model is wrong.

After: The model counts the gene towards resistance and raises the probability it gives that isolate, for a reason that
has nothing to do with the drug.

Files: `results/metrics/model_results_ciprofloxacin.txt` and `results/metrics/variant_table_ciprofloxacin.txt`.

Value found: under GROUPED SPLIT the regression's counts (TP, FN, FP, TN) are `606  10  2  2464` for train and
`202  6  0  694` for test: 810 isolates called resistant, 808 of them correctly, the isoleucine count
(`gyrA_T86I=POINT  810  808  2`). The rule, which also covers the valine change, finds 610 and 206. So the regression
called all eight valine isolates susceptible, the five that also carry `blaOXA-493` among them, and an isolate with the
gene alone (+2.364, against +4.728 for the pair) would be called susceptible too. The intercept is not printed. The
gene's weight is positive in both splits (+2.364 grouped, +1.469 random), so it raises the predicted probability either
way.

## 9. The tetracycline rule: any tet gene, fixed before scoring

Before (text above the rules box): The rule for ciprofloxacin was fixed before any modelling, and changed once after I
had looked at the data. The rule for tetracycline has one change, kept in the repository as a hypothesis.

After (text above the rules box): Both rules were fixed before any modelling, and each was changed once after I had
looked at the data.

Before (rules box): **Tetracycline.** Call an isolate resistant if the genome carries *tet(O)*.

After (rules box): **Tetracycline, fixed before any modelling.** Call an isolate resistant if the genome carries any
*tet* gene.

Before (rules box): **Tetracycline, kept in the repository as a hypothesis.** The same rule, with *tet(O)* counted as
absent where the annotation reports only partial copies

After (rules box): **Tetracycline, changed after looking, kept as a hypothesis.** The same rule, with a *tet* gene
counted as absent where the annotation reports only partial copies

Before (text): So the rule is easy. If the genome carries *tet(O)*, call the isolate resistant. Across 3,983 isolates,
every one with a tetracycline result measured on a plate, that rule is right 99.32% of the time. But fourteen isolates
carry the gene and die of tetracycline.

After (text): So the rule is easy. If the genome carries a *tet* gene, call the isolate resistant. In these genomes,
that means *tet(O)*, except in five isolates that carry one of two mosaic genes instead, *tet(O/M/O)* in four and
*tet(O/W/32/O)* in one, all five of them resistant. Across 3,983 isolates, every one with a tetracycline result measured
on a plate, that rule is right 99.32% of the time. A rule that asked about *tet(O)* alone would miss those five and
score 99.20%. But fourteen isolates carry *tet(O)* and die of tetracycline.

Files: `results/metrics/marker_comparison_tetracycline.txt`, `scripts/05_compare_markers.py`,
`results/metrics/variant_table_tetracycline.txt`, `results/metrics/discordant_tetracycline.txt`,
`scripts/12_test_refined_features.py`, `results/metrics/refined_features_tetracycline.txt` and `README.md`.

Value found: `tet(O) only  1884  18  14  2067  0.991  0.993  0.9920  32` and
`any tet gene  1889  13  14  2067  0.993  0.993  0.9932  27`, under the note "these definitions were chosen on
mechanistic grounds before scoring, not selected by whichever performed best". The script defines
`("tet(O) only", ["tet(O)"])` and `("any tet gene", ["tet("])`, so 99.32% belongs to any *tet* gene. The variant table
gives `tet(O/M/O)  4  4  0` and `tet(O/W/32/O)  1  1  0`, each with `alone` equal to `n`, so none of the five carries
*tet(O)*; they are the five resistant isolates (1889 against 1884) that *tet(O)* alone misses. All fourteen susceptible
isolates with a *tet* call carry *tet(O)* in some form. The intact-copy rule (`intact tet call`) applies to every `tet(`
entry, and `12_test_refined_features.py` says "The intact-versus-fragment distinction was noticed while reading this
dataset"; the metrics file is headed "POST HOC. These definitions were shaped by reading this dataset", and the README
calls the refinements "hypotheses requiring independent confirmation". The repository gives the two genes only by name;
"mosaic" is the wording of the author's decisions of 2 October 2026.

## 10. The rule, not the table, read every tet(O) call as present

Before (text): A different drug exposed a different weakness in the table.

After (text): A different drug exposed a different weakness.

Before (text): I had been reading both as present.

After (text): My rule had been reading both as present.

Before (text): My feature matrix held a 1 or a 0 for every gene, present or absent. The annotation had been telling me
more than that, and I threw it away before the model ever ran.

After (text): My table already kept `tet(O)` and `tet(O)=PARTIAL` in separate columns. The rule merged them. It counted
every *tet* entry as present, so it read a fragment of *tet(O)* the same as a whole copy. The annotation had been
telling me more than that, and I threw it away before the rule ever ran.

Files: `scripts/06_build_features.py`, `README.md`, `results/metrics/cross_validation_tetracycline.txt`,
`scripts/05_compare_markers.py` and `scripts/12_test_refined_features.py`.

Value found: `06_build_features.py`: "Each distinct gene entry across the cohort becomes one column"; the README: "one
binary column per distinct gene entry". In `cross_validation_tetracycline.txt` (`Features: 58`) the regression's
co-occurrence table lists `tet(O)=PARTIAL_END_OF_CONTIG  15  1.48` and `tet(O)=PARTIAL  17  0.65` as columns of their
own, while the rule is the union of every `tet(` column, `['tet(O)', 'tet(O)=MISTRANSLATION', 'tet(O)=PARTIAL',
'tet(O)=PARTIAL_END_OF_CONTIG', 'tet(O/M/O)']`. The marker scripts flag an isolate when any entry starts with `tet(`.

## 11. The tetracycline gain against the fold-to-fold spread

Before: What they show is how far the score moves from one division of the data to the next, and whether a gain of five
isolates is larger than that.

After: What they show is how far the difference between the two rules moves from one division of the data to the next,
and whether a gain of five isolates is larger than that. It is about the same size. The gain is 1.1 times that spread,
and anything below about 1 cannot be told apart from noise.

Files: `results/metrics/refined_features_tetracycline.txt`, `scripts/12_test_refined_features.py` and `README.md`.

Value found: `intact tet call vs any tet call  +0.0013  0.0011  1.1`, with "ratio = difference relative to fold-to-fold
spread. Below about 1 the difference is indistinguishable from noise." The script takes the per-fold accuracy difference
between the two rules over 25 grouped folds and divides its mean by its standard deviation, so the spread is that of the
difference, which the sentence now names. The README: "Requiring intact tet calls scores 1.1, which sits at the boundary
rather than beyond it", and "a value below about 1 cannot be told apart from noise". Five isolates in 3,983 is the mean
difference of +0.0013.

## 12. The threshold of ten belonged to an early version of the pipeline

Before (text): I picked ten. Anything found in fewer than ten isolates was gone before the model ran.

After (text): In an early version of the pipeline, I picked ten. Anything found in fewer than ten isolates was gone
before the model ran.

Added (text), after "It removed the best-evidenced resistance mutation in the dataset after the common one.": I have
tested it since. The pipeline now scores the rule and the logistic regression with the threshold at 1, 3, 5, 10 and 20,
and at no setting does the regression beat the rule. The default is three, the smallest count that removes a two-isolate
column like the one above. That is why the valine change, in eight isolates, and *blaOXA-493*, in five, both carry
weights in the model I read them from. Three is a choice too, and it still cuts the rarest change at position 86, which
a single isolate carries.

Before (Figure 1.4 caption): A rarity threshold of ten removes the column for the valine change

After (Figure 1.4 caption): A rarity threshold of ten, the setting of an early version of the pipeline, removes the
column for the valine change

Before (summary): a rarity threshold of ten deletes a resistance mutation without warning,

After (summary): a rarity threshold of ten, in an early version of the pipeline, deleted a resistance mutation without
warning;

Before (What survives): A rarity threshold I chose in seconds deleted a resistance mutation, and no accuracy figure
noticed.

After (What survives): A rarity threshold I chose in seconds, in an early version of the pipeline, deleted a resistance
mutation, and no accuracy figure noticed.

Files: `README.md`, `data/README.md`, `scripts/06_build_features.py`, `scripts/10_threshold_sweep.py`,
`scripts/08_train_models.py`, `results/metrics/threshold_sweep_ciprofloxacin.txt` and
`results/metrics/variant_table_ciprofloxacin.txt`.

Value found: the README: "An early version filtered out gene entries seen in fewer than 10 isolates. `gyrA_T86V` appears
in 8 isolates, across 7 distinct SNP clusters, and is resistant in all of them ... It was removed silently, and no
accuracy figure revealed it." `06_build_features.py`: `MIN_COUNT = int(sys.argv[2]) if len(sys.argv) > 2 else 3`, under
the comment "A column with two positives cannot support a reliable estimate of its effect"; `data/README.md`: "The
default threshold of 3 retains 58 features". `10_threshold_sweep.py`: `THRESHOLDS = [1, 3, 5, 10, 20]`. The sweep
(rule random, logistic random, rule grouped, logistic grouped): 1: 0.9967, 0.9960, 0.9967, 0.9957; 3: 0.9965, 0.9960,
0.9964, 0.9957; 5: 0.9975, 0.9960, 0.9974, 0.9957; 10 and 20: 0.9955, 0.9955, 0.9954, 0.9954. The regression never
scores above the rule. The variant table: `gyrA_T86V=POINT  8`, `blaOXA-493  5`, `gyrA_T86K=POINT  1`; the README: "The
single isolate carrying T86K falls below the threshold and is missed". The docstring of `08_train_models.py` still reads
"40 fitted parameters", the 39 features of the threshold-ten row plus an intercept. The section's 99.55% and 99.75% are
the sweep's rule figures at ten and five and are unchanged.

## 13. cmeB, reported in six genomes

Before: It is part of CmeABC, the pump *Campylobacter* uses to throw fluoroquinolones back out of the cell before they
reach their target. *cmeB* was not on my list.

After: It is part of CmeABC, the pump *Campylobacter* uses to throw fluoroquinolones back out of the cell before they
reach their target. The annotation reported *cmeB* in only six of the 3,984 genomes, the six counted above. *cmeB* was
not on my list.

Files: `results/metrics/variant_table_ciprofloxacin.txt` and `results/metrics/threshold_sweep_ciprofloxacin.txt`.

Value found: `cmeB  6  6  0 100.0%  6  5` in a cohort of 3,984, and the passenger lists for minimum counts of 1, 3 and 5
begin `cmeB (n=6)`. Neither the repository nor the posts say why the annotation reports *cmeB* so rarely, so the
sentence states only what was reported.

## 14. The cohort is Campylobacter, not shown to be C. jejuni alone

Before (text): In *Campylobacter jejuni*, ciprofloxacin resistance is explained well enough by one position in one gene
that nothing I built improved on it.

After (text): In *Campylobacter*, ciprofloxacin resistance is explained well enough by one position in one gene that
nothing I built improved on it.

Before (Figure 1.1 alt text): for 3,984 Campylobacter jejuni genomes with resistance measured on a plate.

After (Figure 1.1 alt text): for 3,984 Campylobacter genomes with resistance measured on a plate.

Before (Figure 1.8 alt text): on 3,984 Campylobacter jejuni genomes.

After (Figure 1.8 alt text): on 3,984 Campylobacter genomes.

Files: `scripts/01_fetch_ncbi_metadata.sh`, `scripts/02_build_cohort.py`, `data/README.md` and `README.md`.

Value found: the data come from `https://ftp.ncbi.nlm.nih.gov/pathogen/Results/Campylobacter/PDG000000003.2859`, the
*Campylobacter* organism group of NCBI Pathogen Detection ("Read all isolates from the metadata file (170,431 in this
release)"). `02_build_cohort.py` reads `target_acc`, `asm_acc`, `biosample_acc`, `collection_date`, `geo_loc_name`,
`isolation_source`, `epi_type`, `AST_phenotypes` and `AMR_genotypes`, and no species field, and keeps every isolate with
an interpretable call for the drug and an assembly. The README's "in *Campylobacter jejuni*" and "One species" are
stated, not shown by any file. The summary already said *Campylobacter*; the opening's sentence on topoisomerase IV
keeps *Campylobacter jejuni*, as a statement about that species.

## 15. Thirteen scripts

Before: Everything is in the repository: twelve scripts, one pinned NCBI release,

After: Everything is in the repository: thirteen scripts, one pinned NCBI release,

Files: the repository tree at `0e2b3df4c587` and the Reproducing block of `README.md`.

Value found: `scripts/` holds thirteen files, `00_setup_environment.sh`, `01_fetch_ncbi_metadata.sh` and
`02_build_cohort.py` to `12_test_refined_features.py`, and the README's Reproducing block runs all thirteen.

## 16. Which model scored 0.9965 in the split by family

Before: Averaged over those twenty-five, the proportion of held-back isolates called correctly was 0.9965 with families
allowed on both sides and 0.9965 with families kept whole. The number did not move.

After: Averaged over those twenty-five, the one question about position 86 was right for 0.9965 of the held-back
isolates with families allowed on both sides and for 0.9965 with families kept whole, and the 58-gene logistic
regression was right for 0.9961 and 0.9960. Neither number moved.

File: `results/metrics/cross_validation_ciprofloxacin.txt` at `0e2b3df4c587`.

Value found: `Features: 58`, `Rule: ['gyrA_T86A=POINT', 'gyrA_T86I=POINT', 'gyrA_T86V=POINT']`, `5-fold, repeated 5
times`. Under RANDOM FOLDS, `rule 0.9965` and `logistic 0.9961` mean accuracy; under GROUPED FOLDS, `rule 0.9965` and
`logistic 0.9960`. The posts attribute 0.9965 to "the model" without saying which; in the record it is the rule's
score under both schemes, and the sentence that follows, about reading family resemblance, can only be about the
regression, since a rule has nothing to fit.

## 17. The table the one question read in the twenty-five repeats

Before: Averaged over those twenty-five, the one question about position 86 was right for 0.9965 of the held-back
isolates with families allowed on both sides and for 0.9965 with families kept whole,

After: Averaged over those twenty-five, the one question about position 86, asked of the 58-gene table, was right for
0.9965 of the held-back isolates with families allowed on both sides and for 0.9965 with families kept whole,

Files: `results/metrics/cross_validation_ciprofloxacin.txt`, `scripts/09_cross_validate.py`,
`results/metrics/variant_table_ciprofloxacin.txt`, `README.md` and the footer of `posts/day-05.md`.

Value found: the cross-validation file gives `Features: 58` and `Rule: ['gyrA_T86A=POINT', 'gyrA_T86I=POINT',
'gyrA_T86V=POINT']`, and `09_cross_validate.py` builds the rule from the columns of that table whose names start with
`gyrA_T86`. The variant table gives `gyrA_T86K=POINT  1`, below the threshold of three. The README: "That figure is
0.9965 rather than the 0.9967 above because the cross-validated rule is built from the three substitutions that survive
the default rarity threshold, T86A, T86I and T86V. The single isolate carrying T86K falls below the threshold and is
missed, which costs one error." The day-05 footer: "the cross-validated rule covers T86A, T86I and T86V". With all four
changes the question makes 13 errors in 3,984 (99.67%); without the lysine column it makes 14, and 3,970 of 3,984 is
0.9965. Without the clause, the sentence gave the full question a score it does not have, after the chapter had said
that the rule scores 99.67% either way. The threshold section names the missing column: three "still cuts the rarest
change at position 86, which a single isolate carries".

## 18. The regression's score moved by 0.0001 between the two schemes

Before: and the 58-gene logistic regression was right for 0.9961 and 0.9960. Neither number moved.

After: and the 58-gene logistic regression was right for 0.9961 and 0.9960. The rule's number did not move, and the
regression's barely did.

File: `results/metrics/cross_validation_ciprofloxacin.txt` at `0e2b3df4c587`.

Value found: under RANDOM FOLDS, `rule 0.9965` and `logistic 0.9961`; under GROUPED FOLDS, `rule 0.9965` and
`logistic 0.9960`. The rule's mean is the same under both schemes, and the regression's is 0.0001 lower when families
are kept whole, so "Neither number moved" was true of the rule only. The point of the passage, that the regression did
not fail on families it had never seen, stands.

## 19. Seven SNP clusters, and how an isolate with no cluster is counted

Before: Those eight sit in seven different SNP clusters, so they are seven independent observations rather than one
outbreak counted repeatedly.

After: Those eight sit in seven different SNP clusters, counting an isolate with no cluster as a cluster of its own, as
the split does. So they are seven independent observations rather than one outbreak counted repeatedly.

Files: `results/metrics/variant_table_ciprofloxacin.txt`, `scripts/11_variant_table.py`, `scripts/07_split_data.py`
(Listing 1.1) and the README, at 0e2b3df4c587.

Value found: the variant table gives `gyrA_T86V=POINT` in `clust 7`, and the README says "across 7 distinct SNP
clusters". `11_variant_table.py` counts each isolate with no cluster as its own group, as the grouped split does. The
NCBI release the cohort was built from, PDG000000003.2859, is no longer on NCBI's FTP site, so its cluster identifiers
cannot be read again. In the current release, PDG000000003.2916, the eight valine isolates fall into six SNP clusters
and GCA_004876765.1 has none, which fits seven groups as six clusters and one isolate on its own. Seven independent
groups is right either way; the sentence now says how they are counted.

## 20. The mutation the six cmeB carriers never lack

Before: The second appears in six isolates, all six resistant, in five separate clusters, and never once without that
same mutation.

After: The second appears in six isolates, all six resistant, in five separate clusters, and never once without a
mutation at that position either.

Files: `results/metrics/threshold_sweep_ciprofloxacin.txt` and `results/metrics/discordant_ciprofloxacin.txt` at
0e2b3df4c587.

Value found: all six cmeB carriers carry the isoleucine change at position 86 of gyrA, and none of the eight valine
isolates carries cmeB. "That same mutation" could be read as one particular change at that position, which the six do
not share with blaOXA-493's carriers. What both genes share is a mutation at position 86, and the sentence now says so.

## 21. Where the doubling dilutions sit, tubes to wells

Before: The organism goes into a row of tubes, each holding twice as much ciprofloxacin as the one before it, and the
lowest concentration that stops it growing is the result.

After: The organism goes into a row of wells, each holding twice as much ciprofloxacin as the one before it, and the
lowest concentration that stops it growing is the result.

Files: `data/README.md` at 0e2b3df4c587, and the NCBI BioSample antibiograms of the four alanine isolates read for entry
3.

Value found: `data/README.md` describes the phenotypes as "measured MIC or disk diffusion results". The antibiograms
read for entry 3 give their minimum inhibitory concentrations as measured on Sensititre, a broth microdilution system,
in which the doubling concentrations sit in the wells of a plate. A row of tubes is the older macrodilution method. The
sentence now describes the method the records show.
