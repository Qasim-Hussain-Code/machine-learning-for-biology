<!-- Day 62 -->

Machine Learning for Biology | Day 62
Chapter 7: Immune cell subtype discovery from single-cell RNA-seq

Draw a tube of blood, spin it down, and the thin white layer in the middle holds T cells, B cells, NK cells, monocytes and dendritic cells, tangled together. 

Under a microscope, several of them look nearly identical.

Every chapter in this series so far has told the model the correct answer during training.

Logistic regression knew which genomes carried resistance. 

The network in Chapter 6 knew which peptides provoked a response. 

Day 2 of this series raised a different possibility and then left it alone for six chapters: biologists already sort cells into types without any of that supervision.

This chapter is where that gets tested properly.

The question: given only a cell's gene expression, nothing else, can an algorithm that has never seen a cell type label recover the immune cell populations a lab already knows are there?

The check is what makes this answerable rather than just interesting. 

The cells used here were sorted into ten populations by an entirely different method from transcriptomics. 

Those labels never touch the clustering. They exist only to be compared against afterward.

One limitation, named now. Clustering finds structure, not names. It can group T cells together without knowing to call them T cells, and it can just as easily split one real population into two or merge two distinct ones, especially where biology itself is gradual rather than discrete.

Whatever comes out of this still needs a human, and marker genes, to say what each group actually is.

<!-- Day 63 -->

Machine Learning for Biology | Day 63
Chapter 7: Immune cell subtype discovery from single-cell RNA-seq

A correction first. Day 62 said the ten populations were sorted by flow cytometry. They were not. They were pulled out of one donor's blood with antibody-coated beads, and flow cytometry only came in afterwards, to check how pure each tube was. Other published work describes this dataset as FACS-sorted too, which is how the slip travels.

The correction matters because it shows where the answer key came from. Every label here was made with an antibody against a protein on the cell surface: CD4, CD8, CD14, CD19, CD25, CD34, CD45RA, CD45RO, CD56.

The algorithm will never see a protein. It sees RNA, counted from the tail end of each message. Proteins and messages usually agree. Here are three places they do not.

One label is close to invisible. Naive and memory T cells were separated using CD45RA versus CD45RO. Those are not two genes. They are two versions of one gene, PTPRC, made by cutting different pieces out of the same message, and those pieces sit near the front, far from the tail this chemistry reads. A 2024 study tested exactly this on tail-end data from blood cells: even with very deep sequencing, fewer than one cell in ten showed either version.

Some labels overlap by definition. The helper T cells were selected on CD4 alone. Naive, memory and regulatory T cells all carry CD4, so the helper tube holds cells matching three other labels. The two CD8 populations nest the same way, with a twist: some of the most experienced killer T cells switch CD45RA back on, so "naive" here is not purely naive.

One label is mostly something else. The CD34+ tube was 45% pure by the dataset's own flow check.

This is the Chapter 7 version of Day 48. There, the gene did not follow the organism. Here, the label does not fully follow the RNA.

So, a prediction, written down before any code runs. Not a blind one: others have clustered these cells before. B cells and monocytes will come back largely intact. NK cells will partly blur into cytotoxic T cells, because both run the same killing programme. The six T cell labels will not separate cleanly, and the helper label cannot separate from the populations nested inside it. If it does, something other than biology is doing the separating. The CD34+ label will mostly hold together, as it did in a 2020 re-analysis. That is odd for a tube that is 45% pure, and odd results get checked against the run first.

One decision, made now rather than after a disappointing score. Results get scored against the ten labels, as promised, and against six broad lineages: B cells, monocytes, NK cells, CD34+ progenitors, CD4 T cells and CD8 T cells. Both are declared today, so neither can be chosen later to flatter the result.

<!-- Day 64 -->

Machine Learning for Biology | Day 64
Chapter 7: Immune cell subtype discovery from single-cell RNA-seq

The model for the final chapter is k-means. Here is how it works, and why it got the job.

Each cell starts as counts for thousands of genes. Many of those genes rise and fall together, so they can be squeezed into 50 combined axes that keep the main patterns. That squeeze is called principal component analysis. Now picture every cell as a point in a space with those 50 directions. Similar cells sit close together.

k-means drops k markers into that space. Every cell joins its nearest marker. Each marker moves to the middle of the cells that joined it. Cells switch to whichever marker is now nearest. Repeat until nothing moves.

That is the whole algorithm. No answer key anywhere. The one instruction it gets is k, the number of groups.

Chapter 5's support vector machine searched for the widest gap between two outcomes it had been told about. k-means has no outcomes. It decides where the gaps are on its own.

It is not a toy choice for this data. The 2017 paper that produced these cells clustered with k-means, on 50 principal components, and for its 68,000-cell blood sample it set k to 10 after reading an error curve. Reading a curve like that is a judgement call made after seeing the data. This chapter replaces it with a rule fixed in advance, published tomorrow.

Two reasons it closes the series. It is the plainest version of the idea, the unsupervised counterpart to Chapter 1's logistic regression. And it drags the most important decision into the open. How many groups are there? Most methods answer that quietly, inside a setting. k-means will not start until someone answers it.

One weakness shows up at the start line: where the markers begin can change where they finish. So every run starts from 50 different random positions and keeps the tightest result.

k-means is not what single-cell labs usually reach for. Seurat and Scanpy, two of the most widely used toolkits, default to graph-based clustering: link each cell to its nearest neighbours, then find communities more tightly linked inside than out. The version used here is called Leiden. It needs no k, only a resolution dial that does the same job less visibly. Leiden runs alongside, its dial set by the same rule that picks k.

If the textbook method loses to the field's default, that gets reported too.

<!-- Day 65 -->

Machine Learning for Biology | Day 65
Chapter 7: Immune cell subtype discovery from single-cell RNA-seq

The rules, fixed before any code runs.

The data: the ten bead-enriched populations released by 10x Genomics alongside Zheng and colleagues, Nature Communications, 2017. Every cell the original pipeline called a cell, pooled into one table. Nothing removed on top by thresholds of my choosing.

The answer key goes in a locked drawer. At the very first step the labels move to a separate file, every cell gets a random code in place of its name, and the order is shuffled. No script that groups cells may open that file. It opens once, after the groups are final and committed to the repository.

The input is gene expression and nothing else. The settings are borrowed, not tuned: the processing recipe from the 2017 paper, which the Scanpy library ships under that paper's name. The 1,000 most variable genes, squeezed to 50 axes. No correction for sequencing batch, because here batch and label are the same thing. Tomorrow explains.

The number of groups comes from the data. Anything from 2 to 20 is allowed. The winner is the number where cells sit most clearly inside their own group rather than the next one over, a measure called the silhouette. It will never be set to ten because the key says ten. One extra run, labelled as borrowing from the key, forces ten groups, so a wrong count can be told apart from a wrong grouping.

The score: the adjusted Rand index. 0 is what random grouping scores on average, 1 is perfect agreement. It comes with a 95% confidence interval, and the 0 gets checked by shuffling the key 1,000 times. Scored twice, as declared on Day 63: against the ten labels and against the six lineages.

The baseline to beat: the same model, fed three numbers per cell that describe the measurement rather than the cell. Molecules captured, genes detected, and the share of molecules from mitochondrial genes. If gene expression cannot clearly beat that, the groups describe the machine.

Names before answers. Before the key opens, every group gets a name from its marker genes, twice: once by a fixed rule written down now, once by me. Both get committed, then scored.

Every setting, down to the random seed, goes into the repository before the analysis starts, along with a pass or fail test for each prediction from Day 63.

<!-- Day 66 -->

Machine Learning for Biology | Day 66
Chapter 7: Immune cell subtype discovery from single-cell RNA-seq

Here are the ways this chapter can go wrong. 

1. It might sort by tube, not by cell.
Imagine ten piles of holiday photos, each taken with a different camera. Ask someone to sort them by who is in them, and they might sort them by camera instead, because one camera's photos are brighter and another's are blurrier.

The same risk exists here. Each cell type arrived in its own tube and was measured separately, some far more thoroughly than others.

Check: I give the computer only the "camera settings", three numbers about how well each cell was measured and nothing about the cell itself. The real data has to clearly beat that. If it cannot, the groups are about the camera, not the people.

Second check: one tube, the helper T cells, was collected with a broad net, so it already holds many cells from another tube, the naive T cells. Those two should be hard to separate. If the computer separates them more easily than two tubes that really are different, it is sorting by tube.

2. It might count wrong but sort right.
The computer decides how many groups there are by looking for the cleanest splits. In blood, the cleanest splits are the big ones, so it may find three or four groups where the lab defined ten.

Check: I publish its score for every group count from 2 to 20, plus one extra run where I tell it to make ten.

4. It never says "I am not sure".
Every cell must go into some group, even cells caught halfway through changing from one type to another. And where the computer starts is random, which can change where it ends.

Check: I run it 20 times from different starting points, and compare it with a second sorting method, Leiden, that many labs use.

5. A strange group is not a discovery.
A group that matches no label might be a new cell type. It is just as likely to be stray cells, two cells stuck together, or dying cells.

Check: any such group is called "unresolved" and its genes are listed. No new cell types will be claimed.

The labels stay locked away until every group is final.

<!-- Day 67 -->

Machine Learning for Biology | Day 67
Chapter 7: Immune cell subtype discovery from single-cell RNA-seq

Before the answer key opened, everything below was frozen and committed to the repository.

94,655 blood cells went in. Each one was just a list of gene counts. No names attached.

The first job was to decide how many groups to make. The rule from Day 65 tried every number from 2 to 20 and kept the one where cells sat most clearly inside their own group.

It picked 2.

Not ten. Not six. Two. One group of 3,521 cells full of monocyte genes. One group of 91,134 cells holding everything else.

Day 66 warned about exactly this: in blood, the cleanest split is a coarse one. The clarity score for two groups was 0.63. For ten groups it was 0.21.

So the extra run, the one told to make exactly ten groups, now matters a lot. On their marker genes, its groups look like real cell families: B cells, NK cells, monocytes, several kinds of T cells, and three separate groups the naming rule called CD34+ progenitors.

Leiden, the kind of method most labs use, settled on 23 groups.

Then the 20 reruns from different random starting points. Leiden gave much the same answer each time. k-means did not. At two groups, 12 of the 20 reruns found a different split, and a slightly tighter one, than the run fixed in advance. The rules say the pre-committed run is the one that gets scored, so it is. The other answer gets reported next to it.

Finally, every group was named from its genes, twice. A fixed rule called the big group "CD8 T cells". The second naming, which Day 65 said I would do myself. It worked from the same marker genes, before the key opened, and called the big group "unresolved": a mix of several cell types. That change is logged in the repository as a deviation from the plan.

All of it was locked in before anyone looked at a label.

Tomorrow, the key opens.

Code and data pipeline: [link to the chapter repository]

<!-- Day 68 -->

Machine Learning for Biology | Day 68
Chapter 7: Immune cell subtype discovery from single-cell RNA-seq

The answer key is open. Here is how the computer's groups compare with the lab's labels.

I scored every grouping against two keys: the ten labels, one per tube, and the six broad families from Day 63, which lump related tubes together (the four CD4 T cell tubes become one family).

The score runs from 0 (random grouping) to 1 (perfect agreement).

Every grouping beat random easily. I shuffled the labels 1,000 times, and not one shuffle scored above 0.003.

That was the warm-up. The real test was the "camera settings" baseline from Day 66: the same sorting method, k-means, but given only three numbers about how well each cell was measured, and nothing about the cell itself.

The rule, fixed in advance, was strict: gene expression would only win if the whole 95% interval for its lead over the baseline sat above zero.

First, k-means had to decide for itself how many groups there were. It chose two. At two groups, gene expression lost.

Ten labels: gene expression 0.01, camera settings 0.04
Six families: gene expression 0.05, camera settings 0.13

The reason is almost boring. Gene expression split off a small group, mostly monocytes. The camera settings split off the cells that gave the most RNA. The CD34+ tube gave far more RNA per cell than any other, so 89% of it landed in that group. Against the labels, the camera-settings split happens to score better.

Then I told k-means to make ten groups, the same number as the lab's labels. This time gene expression won clearly.

Ten labels: gene expression 0.44, camera settings 0.08
Six families: gene expression 0.55, camera settings 0.09

Leiden, the second sorting method from Day 66, was also left to pick its own number of groups. It settled on 23 and beat two-group k-means on both keys: 0.58 on the ten labels, 0.42 on the six families.

Against ten-group k-means, it was a split decision. Leiden scored higher on the ten labels (0.58 vs 0.44), and k-means scored higher on the six families (0.55 vs 0.42). That comparison was not planned in advance, so it stays a description, not a verdict.

So the headline fits in two sentences. When k-means has to decide how many groups exist, it gets the count wrong, and the camera settings beat it. When it is told the count, it recovers a large part of the lab's structure from RNA alone.

Day 66 called this "count wrong but sort right". That is what happened.

Code and data pipeline: [link to the chapter repository]

<!-- Day 69 -->

Machine Learning for Biology | Day 69
Chapter 7: Immune cell subtype discovery from single-cell RNA-seq

On Day 63 I wrote down six predictions before any code ran. They were scored on the run told to make ten groups, because they are about ten labels.

Four passed. Two failed.

1. B cells come back intact. Pass. 99.9% of them landed in one group, and that group was 96% B cells.

2. Monocytes come back intact. Pass. 93% of them landed in one group.

3. NK cells partly blur into cytotoxic T cells. Fail. The prediction needed an overlap of at least 0.10. It came out at 0.05. Sharing a killing programme was not enough to mix them: 98% of NK cells sat in one group that was 96% NK cells.

4. The CD34+ tube mostly holds together. Fail, and the most interesting miss. The tube did not scatter into other cell types. It split into three groups of its own, each more than 98% CD34+ cells. But its biggest single group held only 30% of it, far short of the 80% needed. This was the one prediction shaped by the 2020 re-analysis, where most of these cells stayed in one cluster.

5. The six T cell labels do not separate cleanly. Pass. Not one of them got a group holding 80% of its cells at 80% purity.

6. The helper tube cannot be pulled apart from the naive T cells inside it. Pass, and this is the one that matters most. Helper against naive separated with a score of 0.05. Naive against memory, two genuinely different kinds of T cell, separated at 0.49. If the tubes, rather than the cells, had been driving the groups, that order would have flipped. It did not.

Two honest notes. These were not blind predictions: others had clustered these cells before, which made B cells and monocytes safe calls. And the two misses are the reason predictions get written down first: without Day 63 on record, it would be easy to claim afterwards that these results were expected.
