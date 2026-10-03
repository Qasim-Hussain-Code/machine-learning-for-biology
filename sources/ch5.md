<!-- Day 47 -->

Machine Learning for Biology | Day 47
Chapter 5 begins

Somewhere in your gut, right now, bacteria are doing something no cell in your body can do.

Your own enzymes cannot break the bond between carbon and nitrogen in a choline molecule. Certain gut bacteria carry one that can, a glycyl radical enzyme called TMA-lyase, and they use it constantly, cleaving choline and carnitine from the steak or eggs you ate and releasing a waste gas called trimethylamine.

That gas crosses into your bloodstream and reaches your liver, where a single enzyme, FMO3, oxidises it into trimethylamine N-oxide. TMAO.

From there it does real damage. It pushes macrophages to swallow more cholesterol than they should, turning them into the foam cells that build atherosclerotic plaque. It blocks the pathway that clears cholesterol back out of your arteries. It makes platelets clot more readily than they should. Elevated TMAO is now one of the more consistently replicated predictors of cardiovascular risk in the literature, and it predicts risk independently of cholesterol itself.

Here is the question this chapter asks.

The enzyme is bacterial. The bacteria that carry it are identifiable. If a support vector machine is shown only the abundance of those specific TMA-producing genera, nothing else, no host genetics, no cholesterol panel, can it predict cardiovascular risk from that alone?

Measuring TMAO itself requires mass spectrometry, and almost nobody who could benefit from knowing their risk will ever have it run. The question underneath the question is whether the presence of the machinery that makes TMAO can stand in for measuring TMAO at all.

This is why the model matters as much as the biology. The feature set here is not the whole gut microbiome. It is a short, mechanistically justified list, the handful of genera actually carrying TMA-lyase. Small feature count, a boundary that may curve rather than split cleanly. That is close to the exact problem support vector machines were built to solve.

One limitation, named now rather than discovered later. TMA-lyase only matters if there is substrate to cut. A person can carry every one of these bacteria and still produce almost no TMAO, if choline and carnitine barely appear in what they eat. Without diet data, this model has a hard ceiling on what it can know, and that ceiling is part of the chapter, not a footnote added after the fact.

Chapter 5 starts tomorrow.

<!-- Day 48 -->

Machine Learning for Biology | Day 48
Chapter 5: Gut Bacteria and Cardiovascular Risk

The enzyme is not the organism.

Yesterday I said the plan was to give the model the abundance of bacteria known to carry TMA-lyase. That sentence hides a problem, and the problem is the whole chapter.

The gene for choline TMA-lyase is called cutC. It does not follow the family tree.

Two genera carry it in every sequenced genome, Desulfosporosinus and Proteus. Almost nothing else does.

Four per cent of Escherichia coli genomes carry a cutC homologue. The other ninety six per cent do not.

Same genus. Same name in your results table. One in twenty five can actually perform the reaction.

The gene spread by horizontal transfer, passed sideways between organisms rather than inherited down a lineage. It turns up in patches across at least a hundred genera. It is absent from most members of most of them.

Which means the obvious approach does not work.

Most public microbiome data is 16S sequencing. It reads one marker gene and tells you which genera are present, and in what proportion. It does not tell you which genes those organisms carry.

If I hand a model the abundance of a genus that sometimes carries cutC, I am not handing it the pathway. I am handing it a proxy for a proxy.

How good a proxy depends on what fraction of that genus carries the gene in that particular person's gut. 16S cannot measure that fraction.

There is a second kind of data that can. Shotgun metagenomics sequences everything. It lets you count cutC directly, as a gene, regardless of which organism carries it.

Those are two different experiments with two different ceilings, and choosing between them is the first thing this chapter has to decide in public.

Tomorrow: the rule, written down before any data is downloaded.

<!-- Day 49 -->

Machine Learning for Biology | Day 49
Chapter 5: Gut Bacteria and Cardiovascular Risk

Here is the rule, written before anything is downloaded.

The data must be shotgun metagenomics, not 16S. Yesterday's post is the reason. If cutC is patchily distributed inside genera, genus abundance is a broken proxy for the pathway. I would be measuring the wrong thing carefully.

If no suitable shotgun cohort with cardiovascular outcomes exists in public data, this chapter reports that and stops. It does not fall back to 16S.

The features are gene abundances, not taxa. cutC and cutD for choline. cntA and cntB for carnitine. yeaW and yeaX, which do the same job by a different route. Normalised to total reads, so a deeper-sequenced sample does not look like a sicker one.

Nothing else goes in. No age, no cholesterol, no blood pressure. The question is what the pathway alone can carry. Adding a clinical panel answers a different and much easier question.

The outcome is atherosclerotic cardiovascular disease, present or absent, taken from the cohort's own clinical labels. I decide what counts as a case before I see how many cases there are.

The split is by person, not by sample.

Some cohorts collect several stool samples from the same individual. Every sample from one person goes on the same side, train or test, never both.

Otherwise the model meets that person in training, recognises them again in the test set, and scores well without having learned anything about the pathway.

The metric is area under the ROC curve. It answers one question. Pick one patient with disease and one without, at random. Does the model give the sick one a higher score?

At 0.5 it is guessing. At 1.0 it is always right.

Every score comes with a confidence interval. A number built from a few hundred people has a range around it, and hiding that range would flatter the result.

The bar to beat is deliberately unglamorous. Add all six TMA-lyase genes together into a single number, total pathway abundance, and classify on that alone.

If six separate gene abundances cannot beat that single summed number, the useful signal is just how much pathway is present. Which genes, and in what proportion, would be adding nothing.

That is a real result, not a failed chapter, and it would be the headline.

Tomorrow: four ways this could go wrong, written down before I know which ones do.

<!-- Day 50 -->

Machine Learning for Biology | Day 50
Chapter 5: Gut Bacteria and Cardiovascular Risk

Four ways this could be wrong. Written down before I know which of them is true.

One. Gene presence is not gene expression. A metagenome tells me cutC is there. It does not tell me the organism is transcribing it, or that the enzyme is working, or that TMA is being produced today. Every result here is about capacity, not activity. Those are not the same claim.

Two. The substrate problem, named on Day 47 and still unsolved. A person can carry every gene in the pathway and produce almost no TMAO, if choline and carnitine barely appear in their diet. Without dietary data the model has a ceiling it cannot see past. If the cohort has diet records, I report results with and without them. If it does not, that limitation stays in the headline.

Three. Compositional data. Metagenomic abundances are proportions. They sum to a fixed total, so one gene rising forces every other gene to fall, whether or not anything real changed. Correlations here can be produced entirely by that constraint. I report results on a centred log ratio transform as well as on raw proportions. If the two disagree, the disagreement is the finding.

Four. Cohort geography. Gut microbiome composition varies enormously by population, diet and country. A model trained on one cohort may be detecting where samples came from, not who has disease. If more than one cohort is available, I test across them. If only one is, the result travels no further than that population.

Tomorrow: why a support vector machine, and what the kernel is actually doing here.

<!-- Day 51 -->

Machine Learning for Biology | Day 51
Chapter 5: Gut Bacteria and Cardiovascular Risk

Six numbers per person. A few hundred people. Here is the model built for exactly that shape of problem.

Every model in this series so far has worked by cutting the data into groups. Is this gene above a certain level, yes or no. Then it asks again. Stack enough of those yes-or-no cuts together and you get a decision tree, or a forest of them, or trees that correct each other. All of it is still cutting.

A support vector machine does something different. It does not cut. It measures the gap.

It looks at the healthy samples and the sick samples, finds the widest possible empty space between them, and draws its boundary straight down the middle of that space.

Why the widest gap matters: most models are happy with any boundary that separates the training data correctly. There are usually many such boundaries, and on the data you already have, they all look equally good. This model picks the one with the most room on either side, because room is what helps when the next patient does not look exactly like anyone it has seen before.

Something else follows from this. Only the patients sitting closest to the boundary actually shape it. Everyone comfortably inside their own group could be removed from the data and the boundary would not move. On a small group of patients, that is useful. The model is defined by its hardest, most borderline cases, not by the easy majority.

One more piece: sometimes no straight line can separate two groups, no matter how you angle it. For that, the model can change how it measures distance between patients, in a way that is the same as stretching the space until a straight line does work. Nothing new is measured. Only the notion of near and far changes, and a straight boundary in that stretched space comes back curved once you look at the original data.

Whether the straight version or the curved version works better here is something to test, not assume, and it gets decided using only the training data, before the final test ever runs.

<!-- Day 52 -->

Machine Learning for Biology | Day 52
Chapter 5: Gut Bacteria and Cardiovascular Risk

This is not a result about TMAO. It is a result about a dataset, and it changes the question this chapter is asking.

The plan was to see whether TMAO, a gut-bacteria byproduct, helps predict cardiovascular risk on top of everything doctors already check. The data to answer that directly is not public. The studies that have it keep it locked behind institutional approval, and that can take months with no guarantee of a yes. I am not chasing that any further.

Instead I found something smaller: a public dataset of 750 patients, all recently treated for a heart procedure, followed for nine months to see who had chest pain again. It measured TMAO and the three things TMAO is made from, choline, betaine, and carnitine, in every single patient, no gaps.

This dataset cannot answer the original question. It has no medical history, no other risk factors, nothing for TMAO to add value on top of. And the patients here already had heart problems, so this is not about predicting a first heart attack in a healthy person.

What it can answer: does TMAO carry any extra information beyond the three ingredients it is built from. And separately, since every patient also had 600 other substances measured: does a model built on all of that actually hold up when tested properly, or does it only look good on paper.

Both questions were tested, with the rules for judging the answer written down before either test ran. Tomorrow: what came back, and why the more interesting finding is not the one this chapter set out to find.

<!-- Day 53 -->

Machine Learning for Biology | Day 53
Chapter 5: Gut Bacteria and Cardiovascular Risk

Chapter 5 ends here, with two results.

Result one. Adding TMAO to a model of its own three building blocks, choline, betaine, and carnitine, raised the score from 0.848 to 0.873 at predicting who would have chest pain again. A real improvement.

Result two, and the one I trust more. A model built from all 600 substances in this dataset came back nearly perfect, and for a hard clinical question, that is usually a sign to look closer rather than celebrate. Looking closer: a large share of the panel, not just TMAO, could separate the two patient groups on its own. This is a public dataset, and like many public deposits, it does not include the lab processing order alongside the results. Without that, there is no way to fully rule out that something about how the two groups were handled, rather than their biology, is doing some of the work. That is a limit of what this particular dataset can tell us.

Seen against that backdrop, the TMAO number needs a caveat. Ranked against the other 404 substances measured, TMAO comes in around the 64th percentile, behind roughly 144 others, including betaine, one of its own ingredients. The result is exactly what I said in advance I would report. It just cannot be read as strong evidence about TMAO specifically, given what this dataset can and cannot rule out.

The original question, whether TMAO helps predict heart disease risk in healthy people, stays open. That data is not public, and I am not chasing it further. 

Code, the pre-registered rules, and every number here are in the repository: [link to the chapter repository]
