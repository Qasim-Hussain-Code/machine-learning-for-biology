# Corrections for Chapter 7, Immune cell subtype discovery from single-cell RNA-seq (k-means)

Each entry gives the chapter's sentence before and after the change, the repository file that settles it, and the
value found there. The repository is `Qasim-Hussain-Code/immune_cell_subtype_discovery` at the chapter's pinned commit
`1141fa411573` throughout, except in entry 16, which names Chapter 5's. That commit is the head of the repository.

## 1. How the ten populations were made, sorted to bead-enriched

Before (opening): The cells used here were sorted into ten populations by an entirely different method from
transcriptomics.

After: The cells used here were separated into ten populations by an entirely different method from transcriptomics.

Before (front matter summary): Blood cells from ten populations sorted without transcriptomics, 94,655 in all, were
pooled with their labels locked away, and k-means was asked to group them from gene expression alone.

After: Blood cells from ten bead-enriched populations, 94,655 in all, were pooled with their labels locked away, and
k-means was asked to group them from gene expression alone.

Added to the caption of Figure 7.1, while the figure was the series' image `figures/web/day-62.jpeg`: The panel headed
The Check, as it was published, describes the populations as sorted by flow cytometry; they were bead-enriched, and flow
cytometry was used only to check how pure they were.

After (the caption as it now stands, after the figure was drawn for the book as `figures/svg/fig-7-1.svg`, which does
not say how the populations were made): Where the labels go. In Chapters 1 to 6, the labels went into training the
model; in this chapter, k-means sees only gene expression, and the ten labels meet its groups only afterwards, when the
two are compared.

Files: `notes/decisions_log.md`, `posts/day_63.md`, `README.md` and `notes/preregistration.md`.

Value found: the decisions log, 2026-09-28: "The published Day 62 describes the populations as "sorted". Day 63
corrects this: they were enriched with antibody-coated beads, and flow cytometry was used only to measure purity. The
repository follows Day 63." The published Day 63 post, kept verbatim in the repository, opens: "A correction first. Day
62 said the ten populations were sorted by flow cytometry. They were not." The README, Data: "The populations were
enriched with antibody-coated beads; flow cytometry was used afterwards only to measure purity, and the cells were not
sorted by flow cytometry." The preregistration, section 2, says the same. When this entry was made, the book's copy of
the posts lacked the Day 63 correction (entry 7 brings it in line), but it called the populations "the ten
bead-enriched populations" (Day 65), as the chapter's rules box already did. The image `figures/web/day-62.jpeg` prints
"Validation uses ten populations sorted by flow cytometry", which is why its caption said so; the drawn figure makes no
such claim, so the sentence went with the image.

## 2. Which groups were named twice, every group to the two of the chosen run

Before: Finally, every group was named from its genes, twice.

After: Finally, the two groups k-means chose for itself were named from their genes, twice.

Files: `notes/human_naming.md`, `results/metrics/07_evaluate.json` and `scripts/06_blind_naming.py`, with `README.md`.

Value found: `notes/human_naming.md` is headed "Second naming: primary k-means partition" and has two rows, the
91,134-cell cluster (rule-based name CD8 T cells, lineage call unresolved) and the 3,521-cell cluster (Monocytes,
Monocytes). Under `naming_scores` in `07_evaluate.json` the second naming appears only as `human_kmeans_primary`, with
`"n_clusters": 2`, while the fixed rule appears for all three named partitions, `rule_kmeans_primary`,
`rule_kmeans_oracle_k10` and `rule_leiden_primary`, the 2, 10 and 23 groups of the chapter. `06_blind_naming.py` line
264: "# Template for the second naming of the primary partition." The README, Limitations: "My own naming covers only
the two clusters of the chosen partition". The README's Methods says "every cluster was named twice", which its own
Limitations and the files above contradict. The rules box kept the rule as published on Day 65 until entry 10.

## 3. The deviation that the record does not contain, removed

Before: The second naming, the one I had said I would do myself, worked from the same marker genes before the key
opened, and called the big group "unresolved": a mix of several cell types. That change is logged in the repository as
a deviation from the plan.

After: The second naming, the one I had said I would do myself, worked from the same marker genes before the key
opened, and called the big group "unresolved": a mix of several cell types.

Files: `notes/deviations.md`, `README.md` and `notes/decisions_log.md`, with the history of `notes/deviations.md`.

Value found: `notes/deviations.md`: "None. The analysis followed the pre-registered plan. Judgement calls that did not
change the plan are listed in `decisions_log.md`." The README: "The analysis followed the pre-registered plan, and
`notes/deviations.md` records no departures." No entry in the decisions log records a change to the naming: the entries
that touch on it settle technical details of how the names were made, keep the finer calls of the second naming as
description only, and record that the key was opened only after the second set of names was committed.
`notes/deviations.md` was last changed in commit `11e2e6de2b55` ("add_human_names"), the commit that added the second
naming, and no version of it has listed a deviation. Both names stand side by side in `notes/human_naming.md`, and each
is scored in its own table, `results/tables/07_naming_rule_kmeans_primary.csv` and `07_naming_human_kmeans_primary.csv`.
This settles the earlier question about the deviation.

## 4. The highest score among the shuffles, not one above 0.003 to a maximum of 0.003

Before: I shuffled the labels 1,000 times, and not one shuffle scored above 0.003.

After: I shuffled the labels 1,000 times, and the highest any shuffle scored was 0.003.

Files: `results/metrics/07_evaluate.json`, with `README.md`.

Value found: under `ari`, `technical_k_chosen`, `six_lineages`, `"null_max": 0.0030453656771102897`, the largest
across the five scored groupings and both keys. The README: "the largest null value across all partitions and keys was
0.0030". At least one shuffle therefore scored just above 0.003, and 0.003 is the maximum at the precision the chapter
gives.

## 5. The CD34+ groups, all of the tube to most of it, and what the 98% measures

Before: It split into three groups of its own, each more than 98% CD34+ cells.

After: Most of it split into three groups of its own, each more than 98% cells from the CD34+ tube.

Before (caption of Figure 7.4, while the figure was the series' image `figures/web/day-69.jpeg`): ... NK cells stayed
apart from cytotoxic T cells, and the CD34+ cells formed three groups.

After: ... NK cells stayed apart from cytotoxic T cells, and most of the CD34+ cells formed three groups.

After (the caption as it now stands, after the figure was drawn for the book as `figures/svg/fig-7-4.svg`, which gives
the number that decided the CD34+ prediction, the 30% of the tube in its biggest group against the 80% needed, so the
caption no longer describes the CD34+ groups): The six predictions, scored on the run told to make ten groups, each
with the number that decided it. The low overlap means NK and cytotoxic T cells stayed apart, so that prediction
failed; the equally low pair score means the helper and naive tubes did not separate, so that one passed.

Files: `results/tables/07_contingency_kmeans_oracle_k10_ten_labels.csv` and
`results/tables/07_cluster_truth_kmeans_oracle_k10.csv`, with `README.md`.

Value found: in the contingency table, row `cd34` puts 2,735, 2,709 and 2,318 cells in clusters 6, 7 and 8, which is
7,762 of the tube's 9,232 cells (84.1%). The rest are in cluster 9 (290), the monocyte cluster 5 (715), the B cell
cluster 3 (373) and clusters 1, 2 and 4 (75, 11 and 6). In the cluster truth table, clusters 6, 7 and 8 have
`plurality_population` `cd34` at shares 0.9870, 0.9919 and 0.9919: the share of each cluster that carries the CD34+
label, not the share of cells carrying the CD34 protein, which for the tube was 45%. The README: "the CD34+ population
mostly split into three clusters of its own, each at least 0.9870 CD34+ by label".

## 6. Where the other two-group answer is reported (a clarification)

Before: The other answer is reported next to it.

After: The other answer is reported next to it in the repository.

Files: `README.md`, Results, FM4, and `results/metrics/06_blind_naming.json`, key `kmeans_rerun_solutions`.

Value found: the README, FM4: "At k = 2, the 20 reruns reached two different solutions. 12 of the 20 found a tighter
split (83,404 and 11,251 cells ...), while the seed 7 primary run and 8 reruns found the looser one (91,134 and 3,521
cells ...)." `kmeans_rerun_solutions` records the same two solutions with their seeds. No later post reports the other
answer, so in the book the sentence pointed at nothing. Entry 11 now reports the other answer in the chapter, and the
sentence reads again "The other answer is reported next to it."

## 7. The book's copy of the posts, brought in line with the posts as published

This entry concerns `sources/ch7.md`, the book's copy of the posts, rather than the chapter. Every change is in Days 63
to 65.

Day 63, added at the start: "A correction first. Day 62 said the ten populations were sorted by flow cytometry. They
were not. They were pulled out of one donor's blood with antibody-coated beads, and flow cytometry only came in
afterwards, to check how pure each tube was. Other published work describes this dataset as FACS-sorted too, which is
how the slip travels." and "The correction matters because it shows where the answer key came from. Every label here
was made with an antibody against a protein on the cell surface: CD4, CD8, CD14, CD19, CD25, CD34, CD45RA, CD45RO,
CD56."

Day 63, before: ... so the helper tube holds cells matching other labels. After: ... so the helper tube holds cells
matching three other labels.

Day 64, before: The 2017 study that produced these cells ... After: The 2017 paper that produced these cells ... Added
after "How many groups are there?": "Most methods answer that quietly, inside a setting. k-means will not start until
someone answers it."

Day 65, before: ... which the Scanpy library ships under that study's name. ... No change for sequencing batch, because
here batch and label are the same thing. After: ... which the Scanpy library ships under that paper's name. ... No
correction for sequencing batch, because here batch and label are the same thing. Tomorrow explains. Added after "a
measure called the silhouette.": "It will never be set to ten because the key says ten. One extra run, labelled as
borrowing from the key, forces ten groups, so a wrong count can be told apart from a wrong grouping." Added after the
paragraph on the score: "The baseline to beat: the same model, fed three numbers per cell that describe the
measurement rather than the cell. Molecules captured, genes detected, and the share of molecules from mitochondrial
genes. If gene expression cannot clearly beat that, the groups describe the machine."

Files: `posts/day_63.md`, `posts/day_64.md` and `posts/day_65.md`, with `notes/decisions_log.md`.

Value found: the decisions log, 2026-09-28: "The posts in `posts/` are stored exactly as published on LinkedIn,
including LinkedIn's "hashtag#" copy artefacts, trailing spaces, the numbering of the Day 66 list (1, 2, 4, 5) and the
closing hashtag of Day 65." Each line above is copied from those files. Compared line by line, Days 62 and 66 to 69
already matched them, apart from a blank line the book's copy adds before the first "Check:" of Day 66. The book's copy
still leaves out the closing hashtags and gives the link lines of Days 67 and 68 as "[link to the chapter repository]",
as the copies of every chapter do.

## 8. How the labels were made, and the three labels inside the helper tube

Added at the start of "What the labels can and cannot see": The ten populations were pulled out of one donor's blood
with antibody-coated beads, and flow cytometry came in only afterwards, to check how pure each tube was. So every label
here, the whole answer key, was made with an antibody against a protein on the cell surface: CD4, CD8, CD14, CD19, CD25,
CD34, CD45RA, CD45RO and CD56.

Before: Naive, memory and regulatory T cells all carry CD4, so the helper tube holds cells that match other labels.

After: Naive, memory and regulatory T cells all carry CD4, so the helper tube holds cells that match three other labels.

Files: `posts/day_63.md`, with `notes/preregistration.md` and `README.md`.

Value found: the published Day 63: "They were pulled out of one donor's blood with antibody-coated beads, and flow
cytometry only came in afterwards, to check how pure each tube was." "Every label here was made with an antibody
against a protein on the cell surface: CD4, CD8, CD14, CD19, CD25, CD34, CD45RA, CD45RO, CD56." "... so the helper tube
holds cells matching three other labels." The preregistration, section 2: "Ten bead-enriched populations of peripheral
blood mononuclear cells from one donor" and "The helper population was enriched on CD4 alone, so it contains naive,
memory and regulatory CD4 T cells." The README, Data, says the same of the helper population.

## 9. The forced ten-group run and the baseline, set among the rules

Before (rules box): **Number of groups.** Anything from 2 to 20 is allowed. The winner is the number where cells sit
most clearly inside their own group rather than the next one over, a measure called the silhouette. The same rule sets
Leiden's dial.

After: **Number of groups.** Anything from 2 to 20 is allowed. The winner is the number where cells sit most clearly
inside their own group rather than the next one over, a measure called the silhouette, and the same rule sets Leiden's
dial. The number is never set to ten just because the key says ten. One extra run, labelled as borrowing from the
key, forces ten groups, so that a wrong count can be told apart from a wrong grouping.

Before (rules box): **Metric.** ... Its zero point is checked by shuffling the key 1,000 times. Gene expression beats
the baseline set out in the next section only if the whole 95% interval for its lead sits above zero.

After: **Metric.** ... Its zero point is checked by shuffling the key 1,000 times. Followed by a new rule:
**Baseline.** The same model, fed three numbers per cell that describe the measurement rather than the cell: molecules
captured, genes detected and the share of molecules from mitochondrial genes. Gene expression beats it only if the
whole 95% interval for its lead sits above zero. If gene expression cannot clearly beat it, the groups describe the
machine.

Before (the first way the chapter could go wrong): The check gives the same sorting method only the "camera settings",
three numbers about how well each cell was measured and nothing about the cell itself. The real data has to clearly
beat that.

After: The check is the baseline in the rules. Its three numbers are the "camera settings": they say how well each cell
was measured and nothing about the cell itself. The real data has to clearly beat them.

Added (why k-means closes the book), after "how many groups are there?": Most methods answer that quietly, inside a
setting. k-means will not start until someone answers it.

Files: `posts/day_64.md` and `posts/day_65.md`, with `config.yaml` and `README.md`.

Value found: the published Day 65: "It will never be set to ten because the key says ten. One extra run, labelled as
borrowing from the key, forces ten groups, so a wrong count can be told apart from a wrong grouping." and "The baseline
to beat: the same model, fed three numbers per cell that describe the measurement rather than the cell. Molecules
captured, genes detected, and the share of molecules from mitochondrial genes. If gene expression cannot clearly beat
that, the groups describe the machine." `config.yaml`: `oracle_k: 10`; under `technical_baseline`, `features:
[log10_total_counts, log10_n_genes, pct_mito]`, `scaling: zscore` and `k: [chosen, 10]`; under `evaluation`,
`beats_rule: "lower bound of paired bootstrap 95% CI of the ARI difference > 0"`. The README, Methods 4: "k-means forced
to k = 10, labelled as borrowing from the key". The two Day 64 sentences follow "How many groups are there?" in
`posts/day_64.md`.

## 10. The second naming in the rules box, every group to the groups of the run that chooses its own number

Before (rules box): **Names before answers.** Before the key opens, every group gets a name from its marker genes,
twice: once by a fixed rule written down in advance, once by me. Both are committed, then scored.

After: **Names before answers.** Before the key opens, each group of the k-means run that chooses its own number gets a
name from its marker genes, twice: once by a fixed rule written down in advance, once by me. Both are committed, then
scored.

Added after the naming in "Before the key opened": The fixed rule also named every group of the ten-group run and of
Leiden.

Files: `notes/human_naming.md`, `results/metrics/07_evaluate.json` and `scripts/06_blind_naming.py`, with
`posts/day_65.md`, `posts/day_67.md`, `config.yaml`, `notes/preregistration.md`, `scripts/common.py` and `README.md`.

Value found: the files in entry 2. The second naming covers only the two clusters of `kmeans_primary`, the run whose k
the silhouette chose, and the fixed rule named all three partitions (2, 10 and 23 groups). The published Day 65 gives
the rule as "every group gets a name from its marker genes, twice: once by a fixed rule written down now, once by me",
and the published Day 67 uses the same words for the two groups of that run: "Finally, every group was named from its
genes, twice. A fixed rule called the big group "CD8 T cells"." `config.yaml` has no setting for which groups the second
naming covers, and the preregistration, section 6, requires only that "the second set of names is complete and
committed after the freeze". What makes it complete is fixed in `scripts/common.py`: `open_answer_key`, the only reader
of the labels, refuses unless `validate_human_naming` finds no problem, and that check requires the rows of the naming
table to be exactly the clusters of `kmeans_primary` ("cluster rows ... do not match the primary partition clusters").
The same check is in the version of `scripts/common.py` committed with `config.yaml` and the preregistration in
`6187ac9a8889`, before the download script. The README, Limitations: "My own naming covers only the two clusters of the
chosen partition, so its perfect score is a small test."

## 11. The other two-group answer, reported

Before ("Before the key opened"): At two groups, 12 of the 20 reruns found a different split, and a slightly tighter
one, than the run fixed in advance. The rules say the pre-committed run is the one that gets scored, so it is. The other
answer is reported next to it in the repository.

After: At two groups, 12 of the 20 reruns found a different split from the run fixed in advance, and a slightly tighter
one, with 83,404 cells in one group and 11,251 in the other. The rules say the pre-committed run is the one that gets
scored, so it is. The other answer is reported next to it.

Added ("Against the answer key"), after the two-group result: The other two-group answer did better. The split that 12
of the 20 reruns found scored 0.06 on the ten labels and 0.18 on the six lineages, above the camera settings' 0.04 and
0.13. That comparison was not part of the plan and has no interval, so the verdict still rests on the run fixed in
advance.

Before (front matter summary): Left to choose the number of groups by the silhouette, it chose 2 and lost to a baseline
given only three numbers about how well each cell was measured, scoring 0.01 against 0.04 on the adjusted Rand index
for the ten labels.

After: Left to choose the number of groups by the silhouette, it chose 2, and the run fixed in advance lost to a
baseline given only three numbers about how well each cell was measured, scoring 0.01 against 0.04 on the adjusted Rand
index for the ten labels, although a different two-group split, found by 12 of 20 reruns from other starting points,
scored 0.06 in a comparison not fixed in advance.

Files: `results/metrics/06_blind_naming.json`, `results/metrics/08_failure_modes.json` and
`results/metrics/07_evaluate.json`, with `README.md`, Results, FM4.

Value found: `kmeans_rerun_solutions` in `06_blind_naming.json`: `"sizes": [83404, 11251]`, `"n_reruns": 12` and
inertia 15693770.758025091, against 15850196.053598313 for the 91,134 and 3,521 split of seed 7 and 8 reruns. Under
`FM4`, `stability_vs_labels`, `kmeans` (the same in `07_evaluate.json`): `ten_labels` max and median
0.057456401943032295, min 0.013896864975464069, the seed 7 run's score; `six_lineages` max and median
0.1830658921941195. Under `ari`, `technical_k_chosen`, `observed`: 0.03841819016522422 for the ten labels and
0.130629456447165 for the six lineages. The README, FM4: "The tighter split agrees better with the labels (ten-label ARI
0.0575, six-lineage ARI 0.1831), above the baseline's point estimates, but that comparison was not pre-registered and
has no interval; the pre-registered verdict rests on the seed 7 run." To two decimal places, 0.0575 is 0.06 and 0.1831
is 0.18. This supersedes entry 6.

## 12. The naming scores, reported

Added ("Against the answer key"): The names were scored too. A name counted as correct if it matched the group's most
common lineage, where that lineage made up at least half of the group, or if it said "unresolved" where no lineage did.
The big group k-means chose for itself was only 46% CD4 T cells, its most common lineage, so "unresolved" was the right
name and "CD8 T cells" was wrong. The fixed rule got 1 of those 2 groups right, and my second naming got both. My naming
covered only those two groups, so its perfect score is a small test. On the ten-group run, the fixed rule named 9 of 10
groups correctly, and on Leiden, 17 of 23. Every group it missed on those two runs was a small one.

Files: `results/metrics/07_evaluate.json`, key `naming_scores`, and `results/tables/07_naming_rule_kmeans_primary.csv`,
`07_naming_human_kmeans_primary.csv`, `07_naming_rule_kmeans_oracle_k10.csv`, `07_naming_rule_leiden_primary.csv` and
`07_cluster_truth_kmeans_primary.csv`, with `notes/preregistration.md` and `README.md`.

Value found: under `naming_scores`, `rule_kmeans_primary` has `"n_correct": 1` of `"n_clusters": 2`,
`human_kmeans_primary` 2 of 2, `rule_kmeans_oracle_k10` 9 of 10 and `rule_leiden_primary` 17 of 23. In the cluster truth
table the 91,134-cell cluster has `plurality_lineage` CD4 T cells at `plurality_share` 0.46267035354532887, and truth
unresolved. The preregistration, section 3: "The truth of a cluster is its most common lineage if that lineage makes up
at least half of the cluster, and "unresolved" otherwise." and "A name counts as correct when it equals the cluster's
truth." The rule's one miss on the ten-group run is cluster 9, 444 cells, named Monocytes with truth CD34+ progenitors;
its misses on Leiden are clusters of 364, 129, 107, 77, 34 and 19 cells. The README, Limitations: "My own naming covers
only the two clusters of the chosen partition, so its perfect score is a small test."

## 13. The CD34+ check, reported

Added ("The six predictions"), after the CD34+ prediction: The predictions said odd results get checked against the
sequencing batch first, and this result is odd in that way: a tube that was 45% pure kept most of its cells in groups of
its own. In the biggest of those groups, 34% of cells had at least one count of the *CD34* gene, against 2% of all the
cells outside it, so that group does carry the *CD34* message. Among cells from the CD34+ tube, the share was 34% inside
that group and 32% outside it. By this measure, the tube's cells outside its biggest group resemble the ones inside it
rather than contaminants. What the check cannot do is separate the cells from their run. The camera settings alone kept
much of the tube together: 89% of it in one group at two groups, and 54% at ten. Batch and label are the same thing
here, so nothing in this chapter can tell how far the tube stands apart because of its cells and how far because of its
run.

Files: `results/metrics/08_failure_modes.json`, `FM1`, `cd34`, with `scripts/08_failure_modes.py`,
`notes/preregistration.md` and `README.md`.

Value found: `oracle_best_cluster` 6, the ten-group cluster that holds 2,735 of the tube's cells (entry 5);
`cd34_detected_share_inside_best_cluster_all_cells` 0.3439191627571274;
`cd34_detected_share_outside_best_cluster_all_cells` 0.022963736885638415;
`cd34_detected_share_inside_best_cluster_cd34_labelled` 0.3440585009140768;
`cd34_detected_share_outside_best_cluster_cd34_labelled` 0.3227643527782053, over `n_cd34_labelled_outside` 6,497
cells; `recovery_technical_k_chosen` 0.8903812824956673; `recovery_technical_k10` 0.5427859618717504. In
`08_failure_modes.py` a cell counts as carrying CD34 when its raw count for the gene is above 0. The preregistration,
section 5, lists this check under FM1. The README, FM1: "so the labelled cells outside that cluster resemble those
inside it rather than contaminants"; Limitations: "Label and batch coincide by design, so no result here fully separates
biology from run".

## 14. The variable genes the recipe returned, 999

Added ("Before the key opened"): The processing recipe, asked for the 1,000 most variable genes, returned 999, and I used
its output as it was.

Files: `results/metrics/03_preprocess.json`, with `notes/decisions_log.md`, `notes/blind_report.md`, `README.md` and
`config.yaml`.

Value found: `"n_hvg": 999`. The decisions log, 2026-09-28: "`scanpy.pp.recipe_zheng17` was run with
`n_top_genes=1000`, as pre-registered, and returned 999 genes. ... I used the recipe's output as returned rather than
altering the recipe to force 1,000 genes." The blind report: "Highly variable genes: 999." The README, Methods 2: "The
recipe returned 999 genes rather than 1,000, and I used its output unchanged." The rules box keeps the 1,000 fixed in
advance, `n_top_genes: 1000` in `config.yaml`.

## 15. What the overlap and the pair score measure, defined

Added (a note in "The six predictions"): **Overlap and pair score.** The overlap of two labels adds up, over every
group, the smaller of two shares: the share of the first label's cells that sit in that group, and the share of the
second label's cells that sit there. It is 0 when the two labels never share a group, and 1 when they are spread across
the groups in exactly the same way. The pair score is the adjusted Rand index computed on only the cells that carry one
of the two labels, so it measures how cleanly the groups separate those two labels.

Files: `notes/preregistration.md`, section 3, with `config.yaml`.

Value found: "The overlap of two labels A and B is the sum over clusters of the smaller of the two shares, n(A, c)/n(A)
and n(B, c)/n(B). It is 0 when the two labels never share a cluster and 1 when they are spread across clusters
identically." "The sub-ARI of two labels is the ARI between the partition and the labels, computed on only the cells
carrying either label." `config.yaml`: P3 `stat: overlap`, `rule: ">= 0.10"`; P6 `stat: sub_ari`.

## 16. Chapter 5's support vector machine, described as planned

This entry is settled by Chapter 5's repository, `Qasim-Hussain-Code/tmao_cardiovascular_risk_prediction` at that
chapter's pinned commit `9985756c2db6`, not by this chapter's.

Before: Chapter 5's support vector machine searched for the widest gap between two outcomes it had been told about.

After: Chapter 5 set out to use a support vector machine, a model that searches for the widest gap between two outcomes
it has been told about.

Files: `src/tmao_cvd/models.py`, `src/tmao_cvd/reanalysis.py` and `docs/reanalysis_plan.md`, with `README.md`.

Value found: `models.py`, `make_logistic_model`: `LogisticRegression(penalty=None, solver="lbfgs", ...)`.
`reanalysis.py`: "L2 penalised logistic regression with the penalty chosen in-fold", fitted with
`LogisticRegressionCV(..., penalty="l2", ...)`. `reanalysis_plan.md`: "Estimator: unpenalised logistic regression." and
"Model: L2 penalised logistic regression on all 600 metabolites". No code, configuration or plan at that commit fits a
support vector machine. Outside the posts, the README names one only in its table of posts, for `posts/day51.txt`: "Why
a support vector machine, and what the kernel does".
