<!-- Day 2 -->

Machine Learning for Biology | Day 2
Chapter 1: Predicting antibiotic resistance from a genome

Campylobacter has 1.6 million bases of DNA. Change one of them, a single C to a T, and ciprofloxacin stops working.

One letter out of 1.6 million.

That is not a figure of speech.

Fluoroquinolones kill bacteria by jamming the enzymes that untangle DNA during replication.

E. coli has two of them, DNA gyrase and topoisomerase IV. Mutate one and the drug still has the other, which is why resistance in E. coli usually needs hits in both.

Campylobacter jejuni has no topoisomerase IV. Repeated attempts to find parC have failed. The genome does not carry it.

One target. No backup.

A single base change at position 257 of gyrA, turning threonine 86 into isoleucine, raises the ciprofloxacin MIC 128-fold. 

But, appearing is one thing. Lasting is another.

Most human Campylobacter infection comes from poultry. The question is not whether the mutation survives inside a patient. It is whether it survives inside a chicken, with no drug anywhere near it.

It does. Resistant and susceptible strains both colonised chickens equally well with no antibiotic present. Nothing pushes the mutation back out. Once it appears, it stays.

So the answer is in the genome. Known gene, known position.

Meanwhile the clinic still does it the slow way. Grow the organism, expose it to the drug, wait.

Campylobacter is microaerophilic and slow. That is days, and the patient is treated on a guess in the meantime.

Sequencing takes a day. Read position 257 and you are done.

But you are not.

Two isolates. Both carry the change at 257. One dies at a concentration of ciprofloxacin that the other survives.

Why?

Campylobacter has a pump, CmeABC, that pushes the drug back out of the cell before it ever reaches the gyrase. Disable the pump and the resistance collapses, mutation still intact.

Position 257 is not a switch. It is a contribution, and how much it contributes depends on what else the genome is carrying.

Which is the question this chapter is built on.

If resistance is written in the sequence, why can nobody simply read it off?

Tomorrow: the second half of that problem, which is not in the biology. It is in the machine learning.

<!-- Day 3 -->

Machine Learning for Biology | Day 3
Chapter 1: Predicting antibiotic resistance from a genome

Yesterday I said position 257 is not a switch.

Today I put it to the test.

I took 3,984 Campylobacter genomes from NCBI. Every one had a ciprofloxacin result measured on a plate.

Then I asked one question of each. Is there a substitution at gyrA position 86.

Nothing else. No pump, no context, no second gene.

It was right for all but thirteen of them. 99.67%.

The pump is real. Two isolates with the same mutation do survive different doses of the drug.

I modelled none of it. I asked one question and it was right 3,971 times.

The reason has nothing to do with the bacterium.

It is about what the laboratory measured.

Not the word resistant. A number.

The organism goes into a row of tubes. Each holds twice as much ciprofloxacin as the one before it.

The lowest concentration that stops it growing is the result.

That number is continuous. Some stop at a low dose, some need far more.

Then somebody draws a line across it, susceptible below it, resistant above it.

A good pump buys the organism another tube or two. 

The pump did something. The label recorded nothing.

I did not solve yesterday's problem. I answered a newer one.

Before that 99.67% impresses anybody, including me.

Try to guess susceptible every time. Read no DNA at all. Most Campylobacter is susceptible, so you get 79.32%.

That is the floor. Find the floor before you believe any number.

One question about one position beats it by twenty points.

I gave a second model all 84 resistance genes and let it weight them freely.

It did not beat the one question.

Which is the lesson, and it arrives before any algorithm.

What a model looks at are its features. What it predicts is its label.

And the label is a decision somebody made, usually before you arrived, often for convenience.

Choose the label and you have fixed the ceiling. Every model after that, however clever, works underneath it.

Everything here arrives with its answers attached. That is supervised learning.

The 84-gene model gave position 86 a weight of 8.9.

It gave a beta-lactamase 2.364.

It gave a real gyrase mutation 2.364.

The same number, to three decimals, for a gene that does nothing to fluoroquinolones.

Why? Tomorrow.

<!-- Day 4 -->

Machine Learning for Biology | Day 4
Chapter 1: Predicting antibiotic resistance from a genome

Yesterday the model paid a beta-lactamase the same as a gyrase mutation.

So what does a beta-lactamase do?

It cuts open a beta-lactam ring. Penicillin has one. Amoxicillin has one.

Ciprofloxacin has none. There is nothing there for the enzyme to cut.

The gene is blaOXA-493. Five isolates carry it. All five are resistant.

So the model paid it.

Now look at those five again.

Every one also carries a gyrase mutation. All five. No exceptions.

Put yourself where the model sits. You see two columns. They rise and fall together. Where both are present, the isolate is resistant.

Which one is responsible?

You cannot tell. Nothing in the table can tell you.

So the model split the credit. 2.364 each. It had no other option.

That is confounding, and it is the oldest problem in statistics wearing a genomic coat.

Now the part that should worry you.

Suppose a sixth isolate turns up. It carries blaOXA-493 and no gyrase mutation.

The model calls it resistant. The model is wrong.

There is no sixth isolate. Not in these 3,984.

The mistake is already in the model. Nothing in the data will show it to you.

The model did not learn what the gene does. It learned what the gene travels with.

Why they travel together, I cannot tell you from five isolates. Shared ancestry, perhaps. Or nothing at all.

The model cannot tell you either. It only ever saw them arrive as a pair.

Which is the limit of the whole method.

A model sees co-occurrence. That is all it ever sees. Causes and companions look identical from inside a table.

What separates them is knowing what the gene does, and that never comes from the data.

It comes from biology.

It comes from somebody who knows ciprofloxacin has no beta-lactam ring.

If the model is reading company rather than mechanism, there is a way to catch it.

Hide whole families of isolates from it. Then see whether it still works.

Tomorrow.

<!-- Day 5 -->

Machine Learning for Biology | Day 5
Chapter 1: Predicting antibiotic resistance from a genome

Yesterday I said there was a way to catch a model reading correlation in place of causation.

Hide whole families of isolates from it.

To see why that helps, start with how a model gets tested at all.

You hold data back. Train on three quarters of the isolates, then score the model on the quarter it has never seen. If the model performs well on the unseen, it has learned something.

That only works if the held-back quarter is genuinely new to it.

Now look at what these isolates are.

NCBI sorts them into SNP clusters. Two genomes in the same cluster differ by a handful of bases out of 1.6 million. The same organism, sampled twice, often from two patients in one outbreak.

My 3,984 isolates fall into 1,128 clusters.

Split them at random and 344 of those clusters end up with isolates in both halves.

So the model learns from one genome and is then tested on its near-identical twin. It scores well and it has learned nothing. It is recognising a genome it has already seen.

That is data leakage. Information reaching the test set through a back door.

So I split again, keeping every cluster whole this time. No family on both sides.

344 became zero.

Then I repeated it twenty five times, because one quarter of 3,984 isolates can be accidentally kind.

0.9965 with families split. 0.9965 with families kept whole.

The number did not move.

Which is good news.

If the model was reading family resemblance, it would have failed on families it had never seen. It did not fail. The model predicted resistance in families it had never encountered, and that is what learning a mechanism looks like.

But yesterday's beta-lactamase is still sitting in there.

In the random split its weight was 1.469. In the grouped split, 2.364.

Splitting by family did not remove it.

It could not. blaOXA-493 and the gyrA mutation appear together in every isolate that carries either one. Divide the data any way you like and they are still together on both sides.

So there are two problems here and they are not the same problem.

Leakage is about how you divide the data. Dividing it better fixes it.

Confounding is about what is in the data. No division fixes it at all.

Tomorrow: the gene was there. The protein was not.

Code and data pipeline: [link to the chapter repository]

<!-- Day 6 -->

Machine Learning for Biology | Day 6
Chapter 1: Predicting antibiotic resistance from a genome

Different drug today. Tetracycline.

Tetracycline sits down on the ribosome and blocks the seat where each new amino acid has to arrive. Protein synthesis stops. The cell cannot build anything.

Campylobacter's answer is a gene called tet(O). It makes a protein that binds the ribosome and dislodges the drug.

So the rule is easy. Does the genome carry tet(O)? If it does, call the isolate resistant.

3,983 isolates, every one with a tetracycline result measured on a plate. The rule gets it right 99.32% of the time.

But, fourteen isolates carry the gene and die of tetracycline.

Carrying a gene is one thing. Making a working protein is another.

Look at how the gene was written down.

AMRFinderPlus is the software that reads a genome and reports which resistance genes are in it. It works by comparing the sequence against a reference copy of each known gene.

And it does not answer yes or no. When the match covers the whole reference gene, it writes tet(O). When the match covers only part of it, it writes tet(O)=PARTIAL.

I had been reading both as present.

1,890 isolates carry a full-length copy. 99.6% of them survive tetracycline.

Four isolates carry a fragment and nothing else. No full copy anywhere in the genome.

All four died.

Tet(O) has to reach the ribosome and take hold of it. Part of a Tet(O) reaches nothing.

The gene was there. The protein was not.

Then there is a second kind of partial.

Fifteen isolates carry tet(O)=PARTIAL_END_OF_CONTIG, and 93% of those are resistant.

That flag means something entirely different.

Sequencing does not hand you a genome in one piece. It hands you fragments, called contigs, and this gene ran off the edge of one. The sequence stops because the assembly stops, not because anything is missing from the bacterium.

One word, partial, covering two situations. One of them is the organism. The other is about how its genome was pieced together.

Separate them, and 99.32% becomes 99.45%.

Which is five isolates out of 3,983.

I ran the comparison twenty five times, dividing the data differently each time.

The mechanism says a truncated protein cannot work. The data agrees quietly and cannot prove it. So it goes in the repository as a hypothesis.

Nine of the fourteen are still unexplained. Intact gene, susceptible on the plate, and difficult to tell you why.

But the lesson underneath does not need the significance.

My feature matrix held a 1 or a 0 for every gene. Present or absent.

The annotation had been telling me more than that, and I threw it away before the model ever ran.

Tomorrow: a number I chose, and the feature it quietly deleted.

Code and data pipeline: [link to the chapter repository]

<!-- Day 7 -->

Machine Learning for Biology | Day 7
Chapter 1: Predicting antibiotic resistance from a genome

Back to ciprofloxacin.

Everything in this chapter runs off one table. One row per isolate, one column per resistance gene, a 1 where the gene is present and a 0 where it is not. Those columns are the features.

Before any model uses that table, you have to decide which columns to keep.

Here is why you would drop any. Suppose a gene turns up in two isolates out of 3,984, and both happen to be resistant. In the table that column looks perfect. It is also worthless. Two isolates tell you nothing about a gene, and the model cannot know that.

So the standard move is to delete rare features. Pick a minimum count and cut everything below it.

I picked ten.

Anything found in fewer than ten isolates was gone before the model ran.

Now look at what that removed.

Day 2 was about one change at position 86 of gyrA. Threonine becomes isoleucine, and ciprofloxacin stops working.

There is a second change at the same position. Threonine becomes valine instead.

Eight isolates in this cohort carry it. Every one of them is resistant.

Those eight sit in seven different SNP clusters, the groups of near-identical genomes from Day 5. So they are seven independent observations, not one outbreak counted repeatedly.

Eight is fewer than ten.

The rule I have been using asks one question of each genome. Is there a substitution at gyrA position 86?

With my threshold at ten, it could only find the isoleucine version. It got the right answer 99.55% of the time.

Lower the threshold to five, so the valine version survives the cut, and the same rule gets 99.75%.

The gap is eight isolates. Exactly the eight carrying the change I had deleted.

Nothing warned me about this.

No error, no missing file, no collapse in accuracy. Both numbers sit above 99% and both look like a model that works.

Ten was not a setting I tested. It was a number I chose in a few seconds because it sounded reasonable. It removed the best-evidenced resistance mutation in the dataset after the common one.

So the model I trained was never just the algorithm.

It was also every decision I made before the algorithm started. Which columns to keep. What counts as one sample. What the label is allowed to mean.

None of those show up in an accuracy figure. All of them decide what that figure is measuring.

Tomorrow: a third change at position 86, in four isolates, and not one of them resistant.

Code and data pipeline: [link to the chapter repository]

<!-- Day 8 -->

Machine Learning for Biology | Day 8
Chapter 1: Predicting antibiotic resistance from a genome

Ciprofloxacin kills bacteria by jamming an enzyme called DNA gyrase.

One amino acid in that enzyme, number 86, sits exactly where the drug has to bind. Change it and the drug loses its grip.

Four different changes turn up at position 86 in these 3,984 Campylobacter genomes.

Threonine normally sits there. In 810 isolates it has become isoleucine. In eight, valine. In one, lysine.

That is 819 isolates, and 817 of them survive ciprofloxacin.

The fourth change is alanine. Four isolates carry it.

None of the four is resistant.

Why?

Every isolate here was tested against a second drug as well. Nalidixic acid, the original quinolone, in clinical use since the 1960s. Ciprofloxacin came later. It is a fluoroquinolone, a far more potent version of the same idea, aimed at the same enzyme.

All four of those isolates are resistant to nalidixic acid.

Not one of them is resistant to ciprofloxacin.

The other three substitutions defeat both drugs. Isoleucine, 772 resistant out of 775. Valine, eight out of eight. Lysine, one out of one.

Alanine defeats only the old one.

Look at what each change does to the enzyme. Isoleucine and valine are bulky. Lysine is long and carries a charge. Alanine is the smallest substitution available, barely a change at all.

Enough to shake off nalidixic acid. Not enough to shake off ciprofloxacin.

None of which is new. Jesse and colleagues reported exactly this in 2006, in isolates that resisted high concentrations of nalidixic acid and were killed by low concentrations of ciprofloxacin.

My four isolates reproduced a twenty year old result without being asked to.

Now the part that concerns the model.

My feature was any substitution at position 86 of gyrA. I chose it from the mechanism, and Day 2 argued for it.

Position 86 is not one feature. It is four, and one of them points the other way.

Drop alanine from the rule and it goes from 99.67% correct to 99.77%.

That is four isolates. Three of the four sit in the same SNP cluster, so it is closer to two independent observations than four. The improvement is a fraction of the variation between cross-validation folds.

The biology is published. The statistics here are silent. Both of those are true at once.

Day 3 was about the resolution of the answer. Susceptible or resistant is a line drawn across a continuous measurement.

This is about the resolution of the question.

How finely you define a feature is a choice, and taking it from the mechanism does not protect you. The mechanism at position 86 turned out to be four mechanisms.

Tomorrow: I asked which genes were passengers. It named the efflux pump.

Code and data pipeline: [link to the chapter repository]

<!-- Day 9 -->

Machine Learning for Biology | Day 9
Chapter 1: Predicting antibiotic resistance from a genome

Two genes in this dataset look identical from the numbers.

The first appears in five isolates. All five resistant to ciprofloxacin. Four separate outbreak clusters. Never once without a mutation at position 86 of gyrA, the change that actually causes the resistance.

The second appears in six isolates. All six resistant. Five separate clusters. Never once without that same mutation.

One of them has nothing to do with ciprofloxacin at all.

The other pumps ciprofloxacin out of the cell.

Nothing in the table tells you which is which.

That is the problem in one paragraph.

A model looking at those two columns sees genes that turn up whenever resistance turns up. It cannot separate a cause from a travelling companion, so it hands weight to both.

The first gene is blaOXA-493. It makes an enzyme that cuts open beta-lactam rings, the chemical structure inside penicillin. Ciprofloxacin does not have one. That gene was Day 4.

So I wrote code to find the others.

The rule it starts from is the one this chapter has been testing. Does the genome carry a change at position 86 of gyrA?

The code then looks for genes that appear only in isolates that rule already calls resistant, and that have no known way of acting on the drug.

The first half of that is arithmetic. The second half is a list of gene names I typed into the script.

gyrA, parC, tet, 23S, erm. Five entries, covering the mechanisms I had in mind that afternoon.

The second gene is cmeB. It is part of CmeABC, the pump Campylobacter uses to throw fluoroquinolones back out of the cell before they reach their target.

cmeB was not on my list.

So the code did exactly what it was told, and accused the pump.

Look at the two genes again. Five isolates against six. Both always alongside the causal mutation. Both perfectly correlated with resistance.

Statistically they are the same gene.

What separates them is knowing what the protein does, and that is not in the data. It is in a list.

Mine had five entries and it was missing one.

This is not carelessness I can fix by being more careful next time.

Every method that sorts real causes from things that merely travel beside them uses knowledge from outside the dataset. A pathway database. A curated catalogue. A prior. Somebody's judgement.

That knowledge is part of the method, and its gaps do not announce themselves.

<!-- Day 10 -->

Machine Learning for Biology | Day 10
Chapter 1: Predicting antibiotic resistance from a genome

Four bacteria in this dataset carry a mutation that should let them survive ciprofloxacin.

They do not survive.

I found them by reading through the data. Then I changed my rule to account for them, and my accuracy went up.

That sequence is how results go wrong.

Here is what the rule does.

It asks one thing of each genome. Is there a change at position 86 of gyrA, the amino acid where ciprofloxacin has to bind?

Four different changes turn up at that position. Three of them defeat the drug. 

Exclude alanine and the rule improves from 99.67% to 99.77%.

The number went up because I moved the goalposts after watching where the ball landed.

Do that often enough and you can improve any model to any level you like. Every dataset contains patterns that mean nothing. A rule shaped around them will not survive contact with the next dataset.

So the safe answer is to throw the improvement away and keep the original number.

That answer is wrong too.

Refusing to learn anything from data you have already seen is not rigour. It is superstition.

The question is not whether you looked. It is where the justification comes from.

I have two such reasons.

The first is a different experiment on the same four bacteria. Every isolate here was tested against nalidixic acid as well, the older quinolone, in use since the 1960s. All four of them are resistant to it.

So the mutation does something. It just does not do enough against the newer and stronger drug. That result came from a separate assay, not from the accuracy I was trying to raise.

The second is a paper from 2006. Jesse and colleagues found the same thing in bacteria I have never seen. Alanine at position 86, shrugging off the old drug, killed by the new one.

Neither of those could have come out of tuning.

So both numbers go into the repository with their labels attached.

Fixed before any modelling: any change at position 86. 99.67%.

Changed after looking, on the strength of a separate assay and a published result: excluding alanine. 99.77%.

Nobody has to guess which is which.

Looking at your data is not the sin. Pretending you did not is.

Tomorrow: what eleven days of this actually established, and what it did not.

<!-- Day 11 -->

Machine Learning for Biology | Day 11
Chapter 1: Predicting antibiotic resistance from a genome

Eleven days ago I asked whether a genome can tell you what a laboratory plate would.

It can. One feature, 99.67% correct across 3,984 isolates, and eighty-four features do no better.

That part took an afternoon.

The other ten days went on working out what the number does not mean.

The label made it easy. Susceptible and resistant are a line drawn across a continuous measurement. The efflux pump I spent Day 2 describing moves isolates underneath that line and never reaches the answer.

The model paid a beta-lactamase 2.364 and a real gyrase mutation 2.364. The same weight for a gene that cannot touch the drug, because the two never appear apart.

Hiding whole families of related genomes did not fix it. Two genes that always travel together travel together inside every fold.

A rarity threshold I chose in seconds deleted the best-evidenced mutation in the dataset. No accuracy figure noticed.

The feature I built from the mechanism turned out to be four mechanisms, and one of them points the other way.

The code I wrote to find passenger genes named the efflux pump. The list it checks against was mine, and it was incomplete.

And the best number in my results is one I cannot report, because I found it by looking at twenty.

What survives all of that is narrow and worth stating carefully.

In Campylobacter jejuni, ciprofloxacin resistance is explained well enough by one position in one gene that nothing I built improved on it. That is a claim about this organism and this drug. It is not a claim about resistance prediction in general.

Everything is in the repository. Twelve scripts, one pinned NCBI release, and the metrics file behind every number in these posts. Also a limitations section naming what the data could not establish.

Nine tetracycline isolates in there carry an intact resistance gene and die anyway. I do not know why. If you do, tell me.

Chapter 2 needs a harder problem. 

Tomorrow I will say what that is.
