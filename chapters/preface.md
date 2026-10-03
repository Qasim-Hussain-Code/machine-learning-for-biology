---
kind: preface
title: Preface
---

This book began as a series of daily posts. Between 24 July and 1 October 2026, I posted seventy of them on machine
learning for biology, one a day, each written to stand on its own. The first, which introduced the series, is not
included. The last is rewritten as the epilogue, and the rest as seven chapters, with one model and one biological
question to each.

Chapter 1 uses logistic regression to ask whether antibiotic resistance can be read straight from a bacterial genome.
Chapter 2 uses a decision tree to ask which fragments of a protein, called peptides, a cell will show to the immune
system. Chapter 3 uses a random forest to ask whether the disagreements between two annotation tools, programs that find
the genes in a genome and name them, can be predicted from the DNA alone. The two read the same genomes and often name
the same gene differently. Chapter 4 uses gradient boosting to rank cancer patients by their risk of recurrence or death
when most of them have not had the event the study is waiting for. Chapter 5 sets out to use a support vector machine on
gut bacteria and cardiovascular risk, finds that the public data cannot support its design, and answers two narrower
questions of a public dataset with logistic regression instead. Chapter 6 uses a neural network to ask which peptides on
a tumour cell a T cell will notice.

Those six are supervised. They learn from examples that someone has already labelled. Chapter 7 is not. It uses k-means
on single-cell RNA sequencing (RNA-seq) data and has to find the groups of immune cells without ever being shown one.

The method stays the same throughout. The rules are written down before any model is fitted, and in most chapters so are
the ways the analysis could go wrong. Every result is set against a baseline it has to beat, and the baselines are
deliberately plain. They include guessing the commonest answer, a textbook rule about one position in a peptide, a model
given only the stage a clinician already knows, and one given nothing but how tightly each peptide binds the molecule
that displays it. Results that failed are reported beside results that held, and some chapters are mostly about the
failures.

The epilogue sets the seven models side by side at the end. I wrote the book for two kinds of reader: biologists who
want to see what a model is doing, and people who build models and want to see where biological data can mislead them.
Terms from either side are explained where they first appear, many of them in short notes beside the text.

Every chapter has a public repository with its code, its data pipeline and the numbers it reports. The end of each
chapter links to that repository, pinned to the commit the chapter describes, and the code listings in the text are
quoted from that commit.

The chapters can be read in order, from logistic regression to k-means, or one at a time. Each opens with a summary of
its question and its main results.
