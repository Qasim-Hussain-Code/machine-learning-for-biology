<!-- Day 26 -->

Machine Learning for Biology | Day 26
Chapter 3 begins

Two programs read the same bacterial genome.

One says there is a gene here. The other says there is nothing here.

Same DNA. The same letters, in the same order, read twice.

Neither program is broken. Bakta and Prokka are both standard tools, both widely used, and they disagree about real genomes every day.

Chapter 3 asks whether that disagreement can be predicted from the sequence alone.

It is not asking whether a gene is really there. Nothing in this project can tell you that.

The answer being predicted was produced by software. A model trained on it learns the annotator, not the organism.

That is the harder thing about this chapter, and it is the point.

The model is a random forest. Many trees, each shown a different slice of the data, voting on the answer.

Chapter 2 ended on a single tree, and the best moment in it was reading the thing. I could print the questions it had chosen. It had found a real binding rule that nobody told it about.

A hundred trees will score higher. I will not be able to read any of them.

Same task. Harder label. A model I cannot read.

<!-- Day 27 -->

Machine Learning for Biology | Day 27
Chapter 3: Is gene a fact or a call?

In 2000 a team sequenced Campylobacter jejuni and reported 1,654 genes.

In 2007 another team read the same genome and reported fewer.

Not a new strain. Not new sequencing. The same 1,641,481 letters, read again with better software.

The DNA did not change. The count did.

So where do the genes come from?

Start with what a gene caller is looking for. A protein-coding gene begins with a start codon, runs in groups of three letters, and ends at a stop codon. The stretch in between is an open reading frame.

Find every open reading frame and you have found every possible gene. That is the easy part, and it is useless on its own.

Three of the sixty-four possible codons mean stop. In Campylobacter, which is AT-rich, those three are common. Read a random stretch of this genome and you hit a stop every thirteen codons or so.

So the genome is full of short open reading frames that mean nothing. Millions of letters, six reading frames, stops everywhere.

The real genes average 316 codons. They are the long ones. But length alone will not separate them. A short gene is still a gene, and a long accident is still an accident.

So the caller weighs other things.

Does the codon usage inside this frame look like the codon usage of known genes in this organism? Is there a ribosome binding site sitting just upstream? Does the protein it would produce resemble a protein somebody has already described?

Every one of those is evidence. Not one of them is proof.

And every one of them needs a cutoff. How similar is similar enough. How long is long enough. How close does the binding site have to sit.

Nobody finds those numbers in the genome. They are chosen, by the people who write the software.

Two programs make those choices differently. That is the whole of Chapter 3.

94.3% of this genome codes for protein. What about the rest? Tomorrow.

<!-- Day 28 -->

Machine Learning for Biology | Day 28
Chapter 3: Is a gene a fact or a call?

Somebody printed a microarray with 1,731 spots on it.

One spot for every gene in the Campylobacter jejuni genome. Real glass, real DNA, an experiment you could run.

By the time the genome paper was published, 77 of those spots represented nothing.

The count had been revised down to 1,654 before print. The slides were already made.

Those 77 spots stayed on the glass. The software that read the array flagged each one as not an annotated gene.

Seven years later the count went to 1,643.

1,731. Then 1,654. Then 1,643. Eighty-eight genes withdrawn, and the DNA never changed once.

Yesterday I said 94.3% of this genome codes for protein. Today, the other 5.7%.

That is about 93,564 letters. It is not empty and it is not junk.

Some of it is genes that make RNA instead of protein. The ribosomal RNA the cell builds its ribosomes from. The transfer RNAs that carry amino acids into place.

Some of it is control. Promoters where transcription starts. Ribosome binding sites. Terminators that say stop here.

And besides ribosomal and transfer RNA, this genome has four annotated RNAs. Four, in 1.6 million letters.

That is not a claim that only four exist. It is a count of how many anybody has written down.

Which brings me to the word intergenic.

It sounds like a description of a place. Between the genes. It is not.

Intergenic means nothing has been annotated here. It is a residual, defined by absence, and the absence is in the record rather than the molecule.

Move a gene boundary and the intergenic space moves. Withdraw a gene and the intergenic space grows.

Two annotation tools disagree about a region. Which means one of them calls it a gene and the other calls it intergenic.

Neither is looking at anything the other cannot see.

So what do the two tools actually do differently? Tomorrow.

<!-- Day 29 -->

Machine Learning for Biology | Day 29
Chapter 3: Is a gene a fact or a call?

Bakta and Prokka do not disagree the way I assumed.

I assumed two independent gene callers, each trained differently, each finding its own answer. That is not what is happening underneath.

Prokka calls genes with a program called Prodigal.

Bakta calls genes with a program called Pyrodigal. Pyrodigal is a rewrite of Prodigal. Same model, same scoring, faster code, some bugs fixed.

They are close enough to the same caller. Most of a genome will come out identical either way.

So where does the disagreement come from?

Not from two ways of reading the sequence. From two decisions about what to look for in it.

Bakta adds a search for very short proteins, under thirty amino acids. Prodigal was never built to find those.

Bakta also calls pseudogenes. A gene broken by a stop codon or a frameshift, still recognisable, still worth recording. Prokka mostly does not.

So a real disagreement here will rarely look like two tools reading the same DNA and reaching different conclusions.

It will look like one tool asking a question the other tool never asked.

That changes what I expect the forest to find.

If the two callers were independent, disagreement might trace to something subtle in the sequence. A signal one model catches and the other misses.

If they mostly share a caller, disagreement should trace to something blunter. Length, mostly. Short proteins are what one tool looks for and the other does not.

I am writing this before I have looked at a single result.

If the forest's top feature is not length, I have misunderstood something here. That will be worth a post on its own.

Tomorrow: the rule for what counts as a disagreement.

<!-- Day 30 -->

Machine Learning for Biology | Day 30
Chapter 3: Is a gene a fact or a call?

Here is the rule, published before I have run it on a single genome.

A gene call from Bakta and a gene call from Prokka count as the same call under one condition. They overlap by seventy percent or more, on both sides, on the same strand.

Not fifty percent, which is the common convention. Seventy.

Both tools mostly agree on where a gene starts and stops. When they disagree, it is usually the exact start codon. A difference of a few dozen letters, inside a call both tools clearly made.

A loose threshold would count that as a disagreement. It is not one. Both tools found the gene.

Seventy percent still calls that a match. It is also tight enough that a genuinely different claim cannot sneak through as one.

Strand matters twice.

Same strand is required for two calls to count as a match. A call on the other strand is a different gene, not the same gene read differently.

Same strand is also required before I call something bakta_only. If Prokka has a call there on the opposite strand, the region is not empty. Prokka made a claim. A different claim, not a missing one.

Folding that in would make the label say something it does not mean.

One more decision, easy to get wrong. When both tools call the same gene but pick different start codons, which coordinates go in the table?

Not Bakta's. Not Prokka's either. The overlap between them.

Using one tool's coordinates for the agreed cases would hide a tell. The model could learn a tool's own habits, not the sequence.

The overlap belongs to neither tool and to both.

Two sensitivity thresholds go in the record alongside seventy percent. Fifty, and ninety. Named as sensitivity checks, not as alternatives to switch to later.

That line matters more than it looks. A threshold chosen after seeing which one gives the better story is not a threshold. It is the story wearing a number.

The pipeline is running. First numbers, tomorrow.

<!-- Day 31 -->

Machine Learning for Biology | Day 31
Chapter 3: Is a gene a fact or a call?

The pipeline ran. 

87,960 gene calls from Bakta. 72 of them have no matching call from Prokka.

That is a disagreement rate of 0.0008. Eight in ten thousand.

Of the 87,888 calls both tools made, 87,788 have identical start and stop coordinates. Not overlapping. Identical, to the base.

Here is why, and it was knowable before I downloaded a single genome.

Prokka calls genes with Prodigal. Bakta calls genes with Pyrodigal.

Pyrodigal is a rewrite of Prodigal in a different language. Same model, same scoring, some bugs fixed.

So asking whether Bakta and Prokka disagree about where genes are is mostly asking whether Prodigal agrees with itself.

It does. 38 divergences in 87,917 calls, which is 0.04%.

I said this on Day 29. I wrote down that the tools share a caller and that any disagreement should be blunt rather than subtle.

What I did not know was the size. I expected a small signal. I got 72 rows

When 87,788 of 87,888 pairs are coordinate-identical, the distribution sits at the two extremes with almost nothing in between. Fifty, seventy or ninety would have given nearly the same answer.

I could not have known that in advance. Choosing the threshold afterwards, once I could see which one flattered the result, would not be a choice at all.

A rule that turns out not to bind is still worth fixing beforehand.

What are those 72? Tomorrow.

Code and data pipeline: [link to the chapter repository]

<!-- Day 32 -->

Machine Learning for Biology | Day 32
Chapter 3: Is a gene a fact or a call?

On Day 29 I wrote down what I expected the model to find, before I had run anything.

Length, mostly. Short proteins are what one tool looks for and the other does not.

That is what it found.

Of the 72 disagreements, 34 come from one module.

After the main gene caller finishes, Bakta runs a second search for short open reading frames, under thirty amino acids. Prokka has nothing equivalent.

Bakta made 43 such calls across the whole panel. 34 of them are disagreements.

Nearly every short protein Bakta finds, Prokka misses. Not because it looked and decided no. Because it never looked.

Prodigal's default minimum gene length is 90 base pairs. The shortest disagreement here is 45.

Now the part that is actually biology.

Look at what those short proteins are.

Type I toxin-antitoxin system Ibs family toxins. Leader peptides from the tryptophan and histidine operons.

These are real, well described, functionally important. A toxin whose antitoxin is an RNA that stops it being translated. A short peptide whose ribosome stalls or does not, and in stalling decides whether the operon behind it gets transcribed.

Textbook regulatory biology, and exactly the class a dedicated short-ORF finder is built to catch.

So the disagreement is real and it points at something real.

But the label is not what I said it was.

It is not two tools reading the same DNA and reaching different conclusions.

It is one tool running an extra module.

That is a fact about software architecture. The biology is downstream of it.

One more thing went wrong before I could trust any of this. Tomorrow.

Code and data pipeline: [link to the chapter repository]

<!-- Day 33 -->

Machine Learning for Biology | Day 33
Chapter 3: Is a gene a fact or a call?

Prokka found zero ribosomal RNAs in all 25 genomes.

It reported that, and exited successfully.

Every bacterial genome has ribosomal RNA. It is not optional. A genome with none is not a genome.

The tool did not crash, did not warn, did not return an error code. It printed Found 0 rRNAs and finished.

This surfaced while I was checking why the held-out set only had 13 positives.

Here is the chain.

Prokka does not find ribosomal RNA itself. It calls a program called barrnap. Barrnap does not do it either. It calls nhmmer.

The nhmmer binary in that environment was compiled against one version of a maths library. The environment shipped a different version.

So nhmmer failed at runtime, every time, silently. Barrnap got nothing back and reported nothing. Prokka reported what barrnap told it.

Three programs deep, and nobody raised a hand.

Now think about what that does to my label.

The label is a region one tool called and the other did not. If Prokka finds no ribosomal RNA anywhere, then every ribosomal RNA Bakta calls becomes a disagreement.

Not a real one. A missing shared library, written into the training data as biology.

I caught it because the count was zero rather than low. Zero is impossible and impossible is visible.

The first complete run, 87,901 calls and no ribosomal RNA, was thrown away and redone.

The rule I took from this. A program exiting successfully is not evidence that it did its job.

The pipeline now records how many of each feature type each tool produced, per genome. Not because I expect this bug again. Because the next one will also exit zero.

Same regions, different question. Tomorrow.

<!-- Day 34 -->

Machine Learning for Biology | Day 34
Chapter 3: Is a gene a fact or a call?

My code decided that GTPase Era and GTPase Era were different names.

Twenty-three times.

Same string. Same letters, same spaces, same capitals. Scored as a disagreement between two tools that had written exactly the same thing.

Here is how that happened, because the shape of it is common.

Comparing product names by exact string match is too strict. One tool writes 50S ribosomal protein L7 slash L12. The other writes the same thing with a bracket on the end. Those are the same claim and counting them as different would make the whole exercise meaningless.

So names get normalised before comparison. Strip a trailing bracket. Strip a trailing gene symbol, because one tool often appends it and the other does not. 

The gene symbol strip is where it broke.

To strip a trailing gene symbol you need to know what the gene symbols are. My first version read each record's own symbol field and stripped that.

Bakta fills that field on 19,216 of these regions. Prokka fills it on 48,201.

So for thousands of pairs the strip fired on one side and not the other. Two identical strings went in. One came out shortened. The comparison said different.

The fix is one line of thinking rather than one line of code. Build the symbol list once per pair, from both tools, and apply it to both sides.

And then an assertion, because a fix you cannot verify is a hope.

If two raw strings are identical, they can never be scored as a disagreement. The pipeline checks this on every run and refuses to write the file if it fails. 29,808 pairs have identical raw strings. Zero violations.

Note the direction. The bug inflated the disagreement rate. It made my result more interesting.

Tomorrow.

<!-- Day 35 -->

Machine Learning for Biology | Day 35
Chapter 3: Is a gene a fact or a call?

Two standard annotation tools read the same 50,210 genes.

They give different names to 25,977 of them.

That is 51.7%. About half.

Not different coordinates. Identical regions, both tools confident enough to write a name, and the names do not match.

Before anyone asks whether this is a formatting artefact, I checked, and the check was fixed before I ran it.

Compare the raw strings with nothing stripped: 56.0% disagree.

Compare with my normalisation rule: 51.7%.

Compare with the loosest rule I was willing to defend, dropping generic words and ignoring word order: 50.6%.

Five points across the entire range from strictest to loosest. The disagreement is not punctuation.

One more objection worth answering.

Bakta has a naming style that guarantees a mismatch. When it can only match a structural domain it writes something ending in domain-containing protein. Prokka does not do that, so those are near-certain disagreements.

There are 4,650 such regions, 9% of the set, disagreeing almost every time.

Take them out. The remaining 45,716 regions disagree 47.0% of the time.

Two more numbers from the same regions. Where both tools assign a gene symbol, they differ 41.1% of the time. Where both assign an enzyme number, 16.7%.

Now what this means, and it is not an argument about software.

Pangenome analyses group genes by name. Functional enrichment counts categories built from names. Resistance reports quote a gene product.

Every one of those inherits whichever tool was run.

Not a claim that either tool is wrong. I have no way to know which name is right, and neither does anybody working from annotation output alone.

Can it be predicted? Tomorrow.

Code and data pipeline: [link to the chapter repository]

<!-- Day 36 -->

Machine Learning for Biology | Day 36
Chapter 3: Is a gene a fact or a call?

A model that reads nothing just won.

No sequence. No database matches. No information at all. It always guesses the same answer.

It got the highest score in the whole comparison.

Here is how a model that knows nothing beats models that know something.

Half the regions in this data are real disagreements between the two tools. So a model that always says yes, this is a disagreement, is right about half the time by luck alone.

There is a popular score called F1. It rewards catching every true case. It barely punishes false alarms.

Say yes to everything and you catch every true case. F1 does not penalise the false alarms enough to notice.

So the model that never looks at the data scored 0.664 on F1. Higher than any model that actually learned something.

This happened once before, on Day 20. A score means nothing until you know what a model that knows nothing would score.

So here is the honest comparison, using a different measure. Not F1. A score called MCC, which does punish false alarms as much as it rewards true catches. Zero means no better than a coin flip. One means perfect.

Guess randomly: 0.000
Look only at how long the protein is: 0.028
Look only at whether either tool found a database match for it: 0.141
One simple decision tree: 0.261
Many trees voting together, a random forest: 0.303
A more advanced technique, gradient boosting: 0.288

The fanciest model on that list did not win. The random forest did. More computing power bought nothing here.

What does the random forest actually get right and wrong?

Tested on 12,283 regions it had never seen. It flagged 6,105 as disagreements.

3,965 of those flags were correct. 2,142 were not.

So for every three regions it flags, one is a false alarm.

That is real signal. It is nowhere near reliable enough to trust on its own.

So what is the model actually using to make these calls? Tomorrow.

<!-- Day 37 -->

Machine Learning for Biology | Day 37
Chapter 3: Is a gene a fact or a call?

Take away one set of features and the model barely notices.

Take away a different set and it falls apart completely.

Same random forest, three times. Same folds, same seed, same everything. Only the columns it is allowed to see change.

With all 61 features, it scores 0.303 on MCC.

Take away everything that comes from the gene caller itself. 26 features left. It scores 0.259. Barely moved.

Take away the database features too. 17 features left, all of them describing the raw DNA. It scores 0.142.

That number is generous. It was measured on genomes the model had seen in another role during training. Held out properly, it drops to 0.070.

0.070 is not a working model. It is close to nothing.

That is the honest answer to the question this chapter actually asked. Does the DNA sequence predict disagreement? Barely.

So which features were carrying the score before?

There is a way to check this honestly. Shuffle one column, score again, see how much you lost. Do it on genomes the model never saw, so the answer is about generalisation.

Add up the damage by category.

The nine features describing database cross-references: shuffling them cost 0.165.

The thirty-five features describing the gene call itself: cost 0.019.

The seventeen features describing raw DNA: cost negative 0.001.

Negative means shuffling those columns made the model slightly better. That is what noise looks like when you measure it honestly.

The top three: how many cross-references Bakta attached, whether Prokka assigned an enzyme number, whether Prokka matched a protein motif.

So here is what the model actually learned.

Two tools disagree on a name most often when neither database has strong evidence for that region. One guesses, the other guesses differently, and the model is really just detecting where the evidence ran thin.

That is a fact about two reference databases. It has nothing to do with the DNA sequence itself.

One decision made this visible. Every feature was labelled at creation with where it came from. The check reads those labels automatically, not a list I typed by hand.

Without that label, the 0.259 score would have looked like real biology. It was not.

<!-- Day 38 -->

Machine Learning for Biology | Day 38
Chapter 3: Is a gene a fact or a call?

I asked one question for days. Is a gene a fact or a call?

Here is the answer, in two parts.

Part one. Where does a gene start?

Two annotation tools. 87,960 genes called. Only 72 disagreements. That looks remarkable, until you find out why.

Both tools use the same underlying program to find genes. One is called Prodigal. The other is a rewrite of Prodigal.

So this was never two independent opinions. It was one opinion, copied.

Where a bacterial gene starts looks like a fact. It is one decision, made once, inherited by everyone who used the same software since.

A fact that spread is still just a copy.

Part two. What is that gene, once you have found it?

Here the story flips completely.

Same 50,210 genes. Both tools confident enough to give each one a name.

The names disagree 51.7% of the time.

Strip out one tool's habit of naming genes after a generic protein domain. It is still 47.0%.

Even the shorthand disagrees. Gene symbols differ 41.1% of the time. Enzyme codes differ 16.7% of the time.

Half the time, two respected tools looking at the same gene cannot agree what to call it.

Can a model predict which genes will disagree? Yes. Just not from the DNA.

Strip out every feature describing the sequence itself, and the model's score falls to 0.070. That is barely better than guessing.

What is left is database coverage. How much evidence each tool's reference library has for that gene.

Thin evidence produces a guess. A different guess from each tool produces a mismatch.

The DNA never changed. The books each tool checked did.

So, is a gene a fact or a call? Both. Where it starts is a call so old and so copied it behaves like a fact. What it does is a call made fresh, by whoever has the newer library.

Before I close this chapter, here is everything it got wrong.

I built an experiment around a disagreement that turned out to be 72 rows. The reason was sitting in the tools' own documentation. I had not read it first.

I told you a smaller reference database would make one tool name fewer genes. I had it backwards. That tool missed 12.5%. The other missed 40.2%.

My own code counted identical text as a disagreement, 23 separate times. That mistake made my result look better than it was.

One feature in the first half of this chapter never changed value across 87,960 rows. Nobody caught it until the second half.

Every number here, right and wrong, is in the repository below.

Code and data: [link to the chapter repository]

<!-- Day 39 -->

Machine Learning for Biology | Day 39

Chapter 3 asked whether a gene is a fact or a call.

The answer split in two. Where a gene starts behaves like a fact, but only because two tools quietly rely on the same underlying program. What a gene is called stays a call. It disagrees over half the time, driven by which reference library each tool happened to check.

Every wrong number from getting there is in the repository too.

So what should Chapter 4 be?

I have an idea. I am sitting on it for one more day and revealing it tomorrow.

What would you want to see next? A new organism. A new kind of model. A question nobody has tried because the data is too messy.

You can tell me in the comments. I am open to ideas before tomorrow's post.
