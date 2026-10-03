<!-- Day 55 -->

Machine Learning for Biology | Day 55
Chapter 6 begins

Somewhere on the surface of a tumour cell, right now, a protein is sitting that your immune system has never seen before.

Cancer cells accumulate mutations. Some change a protein's sequence enough that when a fragment of it is displayed on the cell surface, it looks foreign. That fragment is called a neoantigen, and it exists nowhere else in the body.

Chapter 2 asked whether a peptide binds MHC and gets displayed at all. That question mattered, but it was only the first hurdle.

Most displayed neoantigens are still ignored. A T-cell has to actually notice the fragment and mount a response, and most of the time none does.

Here is the question this chapter asks.

Given a candidate neoantigen and the MHC molecule presenting it, can a neural network predict which ones will actually provoke a T-cell response, not merely which ones get displayed?

The question underneath the question matters for a real reason. Personalised cancer vaccines can only include a small number of targets. A candidate that gets displayed but never noticed wastes a manufacturing slot that a genuinely immunogenic one could have filled.

This is why the model matters as much as the biology. Immunogenicity depends on interactions across the whole peptide, position by position, combined with which HLA molecule is presenting it. That is not a boundary a single line or split can capture. It is closer to a pattern a network has to learn.

One limitation, named now rather than discovered later. The model can learn what tends to provoke a response in general. It cannot see a specific patient's own T-cell repertoire, and two people can react differently to the exact same neoantigen. That ceiling is part of the chapter, not a footnote added later.

Chapter 6 starts tomorrow.

<!-- Day 56 -->

Machine Learning for Biology | Day 56
Chapter 6: Neoantigen Immunogenicity for Cancer Vaccine Design

Most of what we know about T-cell response is not about cancer at all.

The data this chapter needs comes from IEDB, the same database Chapter 2 used. It records whether a peptide, once shown to a T-cell, actually provoked a response. That is immunogenicity data, and it is rarer than binding data. Most peptides in IEDB have only ever been tested for binding, not response.

Of the peptides that do have a response recorded, most come from viruses and other pathogens. Tumour-derived neoantigens are a small fraction of the whole.

There is a second problem underneath that one. A peptide that never binds MHC in the first place cannot be immunogenic, it is never shown to a T-cell at all. If a model trains on all peptides, bound and unbound together, it can learn to predict binding and call that immunogenicity. The two get confounded.

So the rule going in is this. Every peptide used here, for training or testing, already binds MHC. The question this model answers is narrower than "is this peptide dangerous". It is "given a peptide already sitting on the cell surface, does a T-cell actually notice it".

That narrows the training data further, to mostly pathogen epitopes that bind and provoke a response, tested against the much smaller set of tumour neoantigens that do the same. TESLA, a benchmark of real tumour neoantigens with confirmed T-cell response, is the largest of those.

The model trains on the broad set. It gets tested, once, on the narrow one.

<!-- Day 57 -->

Machine Learning for Biology | Day 57
Chapter 6: Neoantigen Immunogenicity for Cancer Vaccine Design 

The rules, written before any pipeline runs.

Data. IEDB's T cell assay records, restricted to HLA-A*02:01, the same allele Chapter 2 used. Every peptide included already has confirmed MHC binding, nothing that was never displayed. TESLA is held out completely, untouched until the very end.

Features. The nine peptide positions, nothing else. No HLA sequence, no clinical data, no patient information. HLA-A*02:01 is fixed across the whole dataset, so it cannot be a feature.

Outcome. Positive means a T cell response was recorded in the assay. Negative means the peptide was tested and no response was detected. That definition is fixed now, before anyone looks at how many of each there are.

Split. Peptides are clustered by sequence similarity first, then split by cluster, not by individual peptide. Near-identical peptides landing on both sides of the split would let the model memorise instead of learn.

Metric. Immunogenic peptides are the minority class here, so accuracy is not the number that matters. The primary metric is area under the precision-recall curve, reported alongside standard AUC. Chance is not 0.5 this time, chance is whatever fraction of the dataset is actually positive.

Baseline. A model that predicts immunogenicity using only the binding score, nothing about the sequence itself. If the network cannot beat a model that only knows binding strength, sequence pattern recognition added nothing.

<!-- Day 58 -->

Machine Learning for Biology | Day 58

Chapter 6: Neoantigen Immunogenicity for Cancer Vaccine Design 

Four ways this could be wrong. Written down before I know which of them is true.

One. Assay negative is not biological negative. A T cell assay tests one donor's blood at one point in time. A peptide marked non-immunogenic may simply have met a donor whose repertoire did not include the right T cell that day. Absence of response in the data is not proof the peptide can never provoke one.

Two. The training data still leans pathogen, not tumour, even after restricting to confirmed binders. Most immunogenic peptides in IEDB come from viruses. A pattern the network learns there may not transfer cleanly to a mutated self protein on a tumour cell.

Three. HLA-A*02:01 only. A large share of people do not carry this allele at all. Whatever this model learns says nothing about immunogenicity on any other HLA type, and that scope stays in the headline, not the fine print.

Four. Memorisation risk. The positive class here is small, and small positive classes are exactly where a network can learn the specific peptides in front of it rather than the pattern behind them. Clustering by similarity at the split reduces this. It does not remove it, and performance on TESLA is the real check.

<!-- Day 59 -->

Machine Learning for Biology | Day 59

Chapter 6: Neoantigen Immunogenicity for Cancer Vaccine Design 

Why a neural network, specifically?

Chapter 5 asked a support vector machine to find the widest boundary between two outcomes, using six numbers per sample. That works when the features are few and the relationship between them is fairly stable.

This chapter hands the model nine amino acid positions in sequence. Whether a peptide is noticed by a T cell does not depend on any one position alone. It depends on how positions combine, an anchor residue holding the peptide in the groove while a different position further along is what the T cell receptor actually touches. Change one position and the meaning of another can change with it.

A support vector machine can be given those combinations by hand, multiplying features together before fitting the boundary. A network learns which combinations matter on its own, from data, without being told in advance which positions interact.

That is the actual difference this chapter is testing. Not a bigger model for its own sake, a model built for inputs where position matters and positions talk to each other.

Architecture choice is not exotic. A small feedforward network reading the encoded sequence, compared against a version built to explicitly model interactions between positions, chosen by validation performance before TESLA is ever opened.

The pipeline runs next.

<!-- Day 60 -->

Machine Learning for Biology | Day 60
Chapter 6: Neoantigen Immunogenicity for Cancer Vaccine Design

This chapter's model was built to clearly beat a simpler one. It did not.

1,200 peptides, all confirmed to bind HLA-A*02:01. 606 immunogenic, 594 not.

Split by cluster rather than by peptide, since near-identical variants of the same epitope are common in this data. A random split would have let 13.7 percent of validation peptides leak from training. The cluster split brought that to zero.

Two architectures were compared, chosen on Day 59. A simple feedforward network, and a version built specifically to model interactions between peptide positions. The second was expected to win.

It did not win clearly. All six configurations scored between 0.603 and 0.615 AUPRC, inside each other's seed-to-seed noise. The pre-registered rule selected the feedforward network using an inner validation split. On the actual held-out set, the ranking flipped: the interaction model scored higher. Both numbers are reported here, not just the one that favours the winner.

The core comparison came out just as narrow. A baseline using only binding affinity, no sequence at all, scored 0.591 AUPRC. The selected network scored 0.610. Chance is 0.485. That 0.019 margin is the same size as the network's own run-to-run variation.

One result ran backwards from expectation. Weaker binders were more often immunogenic than tighter ones. 

Two explanations fit equally well: the immune system may delete the T-cell clones that would recognise tight-binding, self-like peptides, or tightly measured peptides may simply be the ones researchers chose to test. This data cannot tell which.

The bigger gap: the pre-registered final test, on TESLA's tumour-derived peptides, never happened. The validated data sits behind a paywall. The headline number here has not been checked against real tumour neoantigens.

Same pattern as Chapter 5: the real result is sometimes about what data you can actually reach, not the biology you set out to test.

Chapter 6 closes here. One chapter left in this series.

Code and data pipeline: [link to the chapter repository]
