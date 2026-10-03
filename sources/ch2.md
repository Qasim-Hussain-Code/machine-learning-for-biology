<!-- Day 12 -->

Machine Learning for Biology | Day 12 
Chapter 2 begins

There is a reason Chapter 1 stopped at logistic regression.

It was already enough. Eighty-four features did no better than one, and adding a more powerful model to a solved problem teaches nothing.

Chapter 2 keeps the same task, predicting a category, and changes the problem underneath it.

Decision trees and the rules they learn. Random forests and why many weak models beat one strong one. Gradient boosting and the difference between fitting and overfitting. Support vector machines and the geometry of a decision boundary.

One model at a time, one chapter each.

Chapter 2 is decision trees.

Same question. Harder data. Real differences between models.

<!-- Day 13 -->

Machine Learning for Biology | Day 13
Chapter 2: What does a cell show to the immune system?

Right now, every cell in your body is holding up samples of what is inside it.

Proteins get chopped into short fragments. Some of those fragments are carried to the cell surface and held there, where passing immune cells inspect them.

If a fragment looks foreign, the cell is killed.

That is how your immune system finds a virus hiding inside a cell without ever going in. It reads the samples on the outside.

The molecule doing the holding is called Major Histocompatibility Complex class I, or MHC class I.

It has a groove. A fragment nine amino acids long sits in that groove like a key in a lock. Two of those nine do most of the gripping, the second and the ninth.

Get both right and the fragment is displayed.

Get one wrong and it falls out. The immune system never sees it. A virus with the wrong fragments is invisible.

Now look at the shape of that rule.

Chapter 1 was one position. One change at gyrA 86 and ciprofloxacin stops working. One question, one answer.

This needs two positions to agree at once. And what counts as agreeable at position nine depends on which MHC molecule you have, and people carry different ones.

That is a conjunction, not a threshold.

Which is exactly what a decision tree is made of. It asks one question, then asks a different question depending on the answer, then another. Follow the path and you have a chain of conditions.

The groove enforces a chain of conditions. The tree is built from them.

So here is the chapter.

Give the model nine amino acids. Ask whether they bind.

One MHC molecule, HLA-A*02:01, the most studied variant in the world. 15,597 laboratory measurements. 9,142 distinct fragments.

53.7% of them bind.

Which is almost exactly a coin flip.

Chapter 1 handed me twenty free points before I read a single base of DNA. This time guessing gets me nothing.

One more thing, and it should feel familiar.

Binding strength is a number. Somebody drew a line across it and called everything on one side a binder.

The database that supplies this data says, in its own documentation, that the line should probably sit somewhere different for every MHC molecule.

Tomorrow: what a peptide looks like to a model that has never seen a protein.

<!-- Day 14 -->

Machine Learning for Biology | Day 14
Chapter 2: What does a cell show to the immune system?

GILGFVFTL.

Nine letters. Positions 58 to 66 of the influenza A matrix protein.

If you carry HLA-A\*02:01, your cells display this fragment when you have flu. It is the most studied T cell target we have.

Yesterday I set the problem. An MHC class I molecule holds a nine amino acid fragment in a groove. Two positions do most of the gripping, the second and the ninth. Get both right and the fragment is displayed.

In GILGFVFTL, position two is isoleucine and position nine is leucine. Both sit in their pockets.

Now hand those nine letters to a model.

It sees nine characters. No chemistry. No shape. No charge. Only characters.

Machine learning models take numbers, and a peptide sequence is text. Something has to convert one into the other, and that something is a choice.

The obvious choice is to number the alphabet. Alanine becomes 1, cysteine 2, and so on to tyrosine at 20.

Nine columns. Done.

It is also wrong.

A decision tree splits by asking whether a number falls below some value. Ask whether the amino acid is below ten and you have grouped alanine, aspartate, phenylalanine and lysine. They share nothing except the alphabet.

The honest version is called one-hot encoding, one column for every amino acid at every position. Nine positions and twenty amino acids give 180 columns, each holding a zero or a one.

Every column is one yes or no question. Is position two a leucine. Is position three a valine.

That is the question the groove asks.

The cost is that similarity disappears. Leucine and isoleucine are the same atoms arranged differently. Across 180 columns they are strangers, and the model has to learn each one alone.

The third option is to describe each amino acid instead of naming it. Hydrophobicity, volume and charge become the columns, and similar residues then get similar numbers.

That is fewer columns and more biology, but it is a bet placed before the model has seen anything.

All three go in the repository. I am writing down now which one I expect to win. A choice made after seeing the scores is not really a choice.

Here is the part that took me a while to see.

Chapter 1 never made this choice at all. A tool called AMRFinderPlus handed me a finished table of genes present or absent and substitutions found or not.

Somebody else had decided what counted as a feature. I inherited that decision and never noticed I had.

A feature matrix is not a fact about nature. It is a claim about what matters.

Tomorrow: how a tree decides which question to ask first.

<!-- Day 15 -->

Machine Learning for Biology | Day 15
Chapter 2: What does a cell show to the immune system?

Every textbook gives the same rule for HLA-A*02:01. Leucine or methionine at position two.

The most studied T cell target in immunology has neither.

GILGFVFTL. Nine amino acids cut out of the influenza matrix protein. Position two is isoleucine.

It binds anyway. It binds so well that your killer T cells go after it before almost anything else in the virus.

The rule is not wrong. It is just not the whole story.

Now watch what happens when a machine tries to learn that rule from data.

Yesterday the peptide became a table. One column for every amino acid at every position. Nine positions and twenty amino acids give 180 columns, each holding a zero or a one.

Every column is a question. Is position two a leucine.

A decision tree gets all 180, and it may ask only one of them first.

It chooses by counting.

Put every peptide in one pile. 15,597 laboratory measurements on this molecule, 8,376 that bound and 7,221 that did not. The pile is a coin flip.

Now ask one question and let the pile fall into two.

Ask something irrelevant and nothing happens. Both piles come out half and half, and you have learned nothing.

Ask about leucine at position two and one pile should come out mostly binders.

The tree tries all 180 questions, measures how much each one tidies the piles, and keeps the winner. That tidying has a name. It is called information gain.

Then it starts the whole search again inside each pile.

The tree cannot look ahead. It takes whichever question pays now. A weaker first question might set up a far stronger second, and the tree never looks. That is called a greedy search.

Most of the time that works. Position two really does carry signal on its own, so the tree will find it.

And then the tree does exactly what the textbook does. It sends GILGFVFTL to the wrong side.

One awkward peptide would be a footnote. Sidney and colleagues counted fourteen A*0201 epitopes in vaccinia virus. Eight of them did not fit the rule.

Chapter 1 never had this problem. In Campylobacter, one amino acid sits at position 86 of a gene called gyrA. Change it and ciprofloxacin stops working.

That was correct for 99.67% of the 3,984 isolates I tested. One question, whole model, done.

Peptides do not hand you that.

So the tree asks again. And again. Nothing in the arithmetic tells it when to stop. A tree that never stops can memorise every peptide it has ever seen.

What stops it? Tomorrow.

<!-- Day 16 -->

Machine Learning for Biology | Day 16
Chapter 2: What does a cell show to the immune system?

Keep asking questions and you can be right about everything.

A decision tree splits a pile of peptides in two, then splits each half again, and keeps going. Yesterday it chose its first question out of 180.

Nothing tells it to stop.

Ask enough questions and every peptide ends up alone in its own group. A group of one is never wrong.

A near-perfect score on all 15,597 measurements, and worth nothing.

A group holding one peptide is not a rule. It is a memory. The tree has recorded that this exact sequence bound. It has learned nothing about a sequence it has never seen.

Machine learning has a name for this. Overfitting is a model that fits the data in front of it and describes nothing else.

So what stops the tree?

You do.

You can cap how many questions deep it may go. You can refuse to split a group below some size. Or let it grow wild and cut the branches back afterwards, which is called pruning.

Every one of those is a number you picked. Not one of them came out of the data.

The honest way to choose is to hide some peptides. Fit the tree on the rest. Then ask it about the ones it never saw. Keep the depth that does best on those. That is cross-validation.

It can still be fooled, and here the data does the fooling.

There are 15,597 measurements here and only 9,142 distinct peptides. So 6,455 of those measurements are a repeat reading of a peptide already in the set.

Hide a peptide from the tree. A copy of it may still be sitting in the data you trained on.

The tree is not being tested then. It is being asked to recall.

Chapter 1 had the same problem and got away with it. 344 groups of closely related Campylobacter isolates sat on both sides of a random split.

It changed nothing. The accuracy stayed at 99.65% correct.

The model had found the one position that decides resistance. There was nothing left worth memorising.

A tree deep enough to memorise has plenty to memorise.

Those 9,142 peptides came out of 2,874 different proteins, so many of them are near neighbours rather than copies.

What happens when the twin is not identical, only similar? Tomorrow.

<!-- Day 17 -->

Machine Learning for Biology | Day 17
Chapter 2: What does a cell show to the immune system?

Change one letter in GILGFVFTL.

Is it still the same peptide?

Ask the MHC molecule holding it and the answer may be yes. The groove grips position two and position nine. Change position five and the grip barely notices.

Ask a T cell and the answer may be no. Position five points up, out of the groove, straight at the receptor.

Same nine letters, two different answers, depending on who is asking.

Yesterday I hid a peptide from a model and found an exact copy of it sitting in the training data. 6,455 of the 15,597 measurements here are repeat readings.

Today is the harder version. Not copies. Relatives.

These 9,142 peptides came out of 2,874 proteins. Just over three peptides per protein.

Split them at random and peptides from the same protein land on both sides of the line.

The model studies one. Then it gets asked about the neighbour.

The repair is to split by group instead of by row. Every peptide from one protein goes to the same side, training or testing, never both.

That is grouped splitting. One line of code, and the accuracy usually drops.

That drop is the point. The old number was scoring the model on neighbours it had already studied. The new one asks about proteins it has never met.

Grouping by source protein is a guess. Two peptides from different proteins can differ by a single letter. Two from the same protein can share almost nothing.

The protein is a convenient handle. It is not the thing that matters.

What matters is how similar two sequences are. The usual fix is to cluster the peptides by sequence identity and split whole clusters instead.

Then you have to choose the identity threshold. Eighty per cent? Seventy?

You have swapped one arbitrary line for another.

So you decide. Then you report a number that is partly a report about your decision.

There is no neutral split.

53.7% of these measurements are binders. A model that answers yes to everything is right more than half the time.

What is a score worth then? Tomorrow.

<!-- Day 18 -->

Machine Learning for Biology | Day 18
Chapter 2: What does a cell show to the immune system?

A 45 degree melting point is not a binding affinity.

The pipeline ran this week. Day 17 asked what a score is worth. The answer arrived before a single model trained.

IEDB stores measurements from many assay types in the same column. Radioactive inhibition assays report affinity in nanomolar. Thermal shift assays report melting temperatures in degrees. Stability assays report half-lives in minutes. Structural assays report distances in ångströms. The column is called quantitative measurement. No unit is attached.

A 500 nanomolar threshold on that column does not select binders. It selects numbers below 500.

Of the 15,597 measurements quoted since Day 13, 3,874 were not nanomolar. Of those, 3,418 fell below 500 and were labelled binders.

1,770 half-lives. 1,087 unitless figures. 333 melting temperatures. 219 interatomic distances.

A half-life of 23 minutes is a stable complex, not a tight binder. A melting temperature of 45 degrees is a structural property, not an affinity. Both were in the training data as binders.

The corrected cohort: 11,723 measurements, 8,346 distinct peptides, 4,957 bound below 500 nanomolar. That is 42.29%, not 53.7%.

I expected one-hot to win. It did not.

Physicochemical encoding, 27 columns of chemistry, outperformed one-hot at 180.

What the tree found. Tomorrow.

Code and data pipeline: [link to the chapter repository]

<!-- Day 19 -->

Machine Learning for Biology | Day 19
Chapter 2: What does a cell show to the immune system?

In 1991 somebody stripped the peptides off an MHC molecule and sequenced them all at once.

The pattern was unmissable. Two positions out of nine did nearly all the gripping.

This week a decision tree found the same two positions.

Nobody told it they existed.

It was given 8,346 peptides, nine letters each. 180 columns, one for every amino acid at every position. Is position one an alanine. Is position one a cysteine. On to position nine.

That is all. No groove, no pockets, no anchors. Nine letters and a label saying bound or did not.

A decision tree picks one column, splits the peptides in two, and repeats. Nothing guide it. It keeps whichever question separates binders from non-binders best.

Its first question was position two, leucine.

Then position two again, methionine. Then position nine, valine. Then position two, isoleucine. Then position nine, leucine.

Five questions. Two positions. It had nine to choose from.

Those two are the pockets. An MHC molecule is the clamp on your cell surface that holds a fragment up for T cells to inspect. The second and ninth residues drop into it and hold the fragment still.

The tree found the clamp by counting.

It did not discover it. Falk and colleagues published the pattern in Nature in 1991. Thirty-five years ago.

So this is not a discovery. It is a check that passed.

A tree insisting that position four decides everything would have told me the pipeline was still broken. Contaminated units, duplicated peptides, relatives sitting on both sides of a split. Any of those shows up as a model confidently finding the wrong thing.

It found the right thing instead.

Chapter 1 ended the same way. The model walked to position 86 of a gene called gyrA, which microbiologists have known about for decades.

Recovering a known answer is not a finding. It is a receipt.

The tree found the rule. Does it beat the rule? Tomorrow.

Code and data pipeline: [link to the chapter repository]

<!-- Day 20 -->

Machine Learning for Biology | Day 20
Chapter 2: What does a cell show to the immune system?

I can build you a model that is right 63% of the time and never finds a single binder.

It answers no to everything.

37.2% of the 1,375 peptides in the test set bind. Say no to all of them and you are correct about the other 62.8%.

Accuracy 0.6284. Binders found: none.

Day 17 asked what a score is worth. That is the answer.

Accuracy counts how often you were right. It says nothing about what you were right about.

So you need two numbers instead of one.

Of the peptides you called binders, how many actually bound? That is precision.

Of the peptides that actually bound, how many did you catch? That is recall.

Either one alone is easy to fake. Call a single peptide a binder and be right about it: precision is perfect, recall is almost nothing. Call everything a binder: recall is perfect, precision collapses to the share that bind.

F1 is one number that only rises when both rise. The model that says no to everything scores 0.0000.

Now the comparison. Every number below comes from the same held-out proteins.

The textbook rule first. Leucine or methionine at position two, predict binder. Accuracy 0.7542. F1 0.6667.

One question about one position, and it beats saying no to everything on both counts.

Then the trees, tested on the same proteins they never saw during training.

Nine columns of alphabet numbering: F1 0.6983.

180 columns of one-hot: F1 0.7153.

27 columns of hydrophobicity, volume and charge: F1 0.7399.

So yes. The tree beats the rule.

One hundred and eighty columns and thirteen levels of questions bought 0.0486 F1 over one rule about one position.

The 27 columns of chemistry bought 0.0732.

Chapter 1 went the other way. Eighty-four engineered features lost to a single codon.

Here the model wins. That is the size of the win.

The winning encoding used 27 columns. The one it beat used 180.
Why? Tomorrow.

Tomorrow.

<!-- Day 21 -->

Machine Learning for Biology | Day 21
Chapter 2: What does a cell show to the immune system?

Leucine and isoleucine are the same atoms in a different arrangement.

To one of my encodings they were neighbours. To another they were strangers.

That difference decided which model won.

On Day 14 I turned nine amino acids into columns three ways.

Number the alphabet: nine columns.

One column for every amino acid at every position: 180 columns, each holding a zero or a one.

Describe each residue by hydrophobicity, volume and charge: 27 columns.

I said then that one-hot has a cost. Leucine and isoleucine become strangers, and the model has to learn each one alone.

I wrote that as a caveat. It turned out to be the result.

Chemistry, 27 columns: F1 0.7399.

One-hot, 180 columns: F1 0.7153.

Alphabet numbering, 9 columns: F1 0.6983.

The smallest useful encoding beat the largest one, on the same peptides, with the same kind of model.

Look at how deep each tree had to go.

Chemistry needed seven questions. One-hot needed thirteen.

That is the mechanism. A tree using chemistry asks one question. Is this position hydrophobic. That catches leucine, isoleucine, valine and methionine at once.

A tree using one-hot has to ask about each of them separately. Four questions to say what the other tree said in one.

The MHC groove does not read letters. It has a pocket with a shape and a chemistry, and any residue that fits, fits.

An encoding that describes shape and chemistry sits closer to what the molecule is doing. Spelling names does not.

One caution before anyone generalises this.

Three physicochemical properties per position is a choice I made before seeing any result. A different three might do better or worse.

This is not a finding about encodings. It is one comparison, on one allele, with one model.

Thirteen questions or eight? The plateau nobody mentions. Tomorrow.

Code and data pipeline: [link to the chapter repository]

<!-- Day 22 -->

Machine Learning for Biology | Day 22
Chapter 2: What does a cell show to the immune system?

Eight questions deep scores 0.7079. Thirteen questions deep scores 0.7153.

I reported thirteen. I am not certain that was right.

Here is the situation, and it is more common than the tidy version of research suggests.

A decision tree needs a depth limit. Without one it kept splitting until every group agreed with itself. That took 1,140 groups for 6,971 training peptides, and it scored 1.0000 on all of them.

On peptides it had not seen, that same tree scored 0.7789. The one I kept scored 0.7927.

So I tested every depth from one to twenty. Five times each, on peptides held back from different proteins each time. Then I kept the depth that scored best.

That is what the pipeline did, before I looked at the test set. Thirteen won.

Now look at the curve it won on.

The score climbs steeply to about depth eight. After that it is almost flat. Depth eight to depth thirteen buys 0.0074.

Five extra levels of questions for seven thousandths.

There is a standard rule for exactly this. Take the simplest model within one standard error of the best one. It exists because a flat plateau is mostly noise, and the peak of noise is not a real peak.

Under that rule I would have reported depth eight. A tree half as deep, easier to read, almost the same score.

So why did I report thirteen?

Because the rule I wrote down beforehand said take the maximum, and I only saw the plateau afterwards.

Changing the rule after seeing the answer is how you get results that do not replicate. Even when the new rule is better. Even when you are certain your motives are clean.

Both numbers are in the repository. Depth thirteen is the reported one because it is the pre-specified one.

Notice what this is not. It is not a data problem, or a modelling error, or something a better pipeline would catch.

It is a judgement, made by me, that changes the number I publish.

Day 17 said there is no neutral split. There is no neutral depth either.

Which mistakes does it make? Tomorrow.

<!-- Day 23 -->

Machine Learning for Biology | Day 23
Chapter 2: What does a cell show to the immune system?

My best model missed 117 real binders.

My second best missed 153.

There are 511 binders in the test set, so those are both bad numbers. But they are bad in different ways, and F1 cannot tell you how.

1,375 peptides. 511 bind. 864 do not.

The chemistry model called 554 of them binders. 394 of those calls were right. 160 were wrong.

The one-hot model was more cautious. It called 490 binders, and 358 were right.

Being cautious cost it. It missed 153 real binders where chemistry missed 117.

So chemistry catches 36 more binders than one-hot, and raises 28 more false alarms doing it.

That is the trade underneath a gap of 0.0246 in F1.

Day 20 defined the two numbers. Here they are with counts attached.

Precision is how often a binder call was right. Chemistry 0.7112, one-hot 0.7306.

Recall is how many real binders you caught. Chemistry 0.7710, one-hot 0.7006.

One-hot is the better guesser. Chemistry is the better finder.

Which one you want depends on what a mistake costs, and nothing in the data can tell you that.

A false alarm is one assay you run and throw away.

A missed binder is a peptide you never look at again.

For screening vaccine candidates those two prices are nowhere near equal. Twenty-eight more assays would be cheap. Thirty-six peptides you never test could include the one that mattered.

Now the textbook rule, on the same 1,375 peptides.

Leucine or methionine at position two catches 338 binders and raises 165 false alarms.

Chemistry catches 56 more than that, and raises 5 fewer.

Better on both counts at once. No trade, no judgement call, just better.

That is the clearest thing this chapter has produced. It took 27 columns and seven questions.

127 peptides in this data disagree with themselves. Tomorrow.

<!-- Day 24 -->

Machine Learning for Biology | Day 24
Chapter 2: What does a cell show to the immune system?

127 peptides in this dataset disagree with themselves.

Measured more than once. One result says binder. Another says not.

I expected that number to be far worse.

Here is what disagreeing means.

8,346 distinct nine-mers in the corrected cohort. 2,660 of them were measured more than once, in different labs, in different years, with different reagents.

Nearly a third of the dataset.

For most of them the repeats agree. Two readings of 15 and 40 nanomolar both say binder. Two at 6,000 and 12,000 both say not.

127 do not agree. One reading falls below 500 nanomolar and another falls above it.

Same nine amino acids. Same molecule. Two answers.

That is 4.8% of the repeat-measured peptides.

A correction while I am here. Day 16 said 6,455 measurements were repeat readings. That was before the unit contamination came out. The figure is 3,377.

So what do you do with 127 peptides that contradict themselves?

You cannot keep both readings. The model would see the same nine letters labelled two ways and learn nothing from either.

You cannot drop them either. That deletes the peptides sitting nearest the line. Those are the ones a binding model most needs to get right.

I took the median of every peptide's measurements and labelled that. Three readings of 200, 400 and 900 become 400, and 400 is a binder.

It is a defensible choice. It is still a choice, and a different one would give a different training set.

Now the part worth sitting with.

A binding affinity is not a fact you look up. It is the output of an assay, run by people, with reagents that vary.

Run it twice and you get two numbers. Draw a line anywhere through the middle of them and some pairs will land on opposite sides.

Those 127 peptides are not errors. They are what measurement looks like when you stop rounding it off.

Move the threshold and a different set of peptides straddles it. The disagreement does not go away. It relocates.

263 of my measurements came from a macaque. Tomorrow.

<!-- Day 25 -->

Machine Learning for Biology | Day 25
Chapter 2: What does a cell show to the immune system?

My human dataset contained 263 measurements from a rhesus macaque.

Also horse. Also cattle. Also chicken.

None of that was a download error. I wrote one line of code that let them in.

The allele I am studying is HLA-A*02:01. To pull its measurements out of a nine gigabyte file, I asked for every row whose allele name contains 02:01.

That is the natural thing to write and it is wrong.

Mamu-A1*002:01 is a macaque molecule. Contains 02:01.

Eqca-1*002:01 is horse. BoLA-3*002:01 is cattle. Gaga-BF2*002:01 is chicken.

All of them contain 02:01, because the naming is done per species. The number after the asterisk identifies an allele within its own species, not across them.

Two different species can both have an 02:01 and share nothing but the label.

Then there were eleven more. HLA-A*02:01 K66A. HLA-A*02:01 A150P. Point mutants, engineered in a lab, one amino acid changed inside the groove.

Those are human, and they are the same allele, and they are still the wrong molecule. The whole point of mutating position 66 is to change what binds there.

Together they added 302 measurements and 262 peptides that do not belong.

Matching the allele name exactly removed all of them and reproduced my feasibility scan to the row.

Unit contamination announced itself. Melting points and half-lives sit in the wrong column and a check catches them.

This did not announce itself. Every one of those rows is a real peptide, measured properly, against a real MHC molecule. Nothing is corrupt.

They are simply not the molecule I said I was studying. And a model would have learned from them happily.

The nomenclature was doing exactly what it was designed to do. My filter was the thing making the claim.

A substring is not an identifier.

That is where Chapter 2 ends. Not on the model that worked, but on the filter that almost let a macaque define a human molecule.

Everything is in the repository. The corrected cohort, the three encodings, every metrics file, and every number I got wrong on the way.

Chapter 3 is about what happens when two annotation tools read the same genome and disagree.

Code and data pipeline: [link to the chapter repository]
