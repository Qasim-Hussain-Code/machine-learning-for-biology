---
kind: prologue
title: Prologue
summary: A method published in *Nature Medicine* in 2006 read the gene expression profile of a patient's tumour and predicted which chemotherapy drug it would respond to; three clinical trials were built on it, and cancer patients at Duke University were assigned regimens by its predictions. Two biostatisticians at MD Anderson, Keith Baggerly and Kevin Coombes, spent more than 1,500 hours reconstructing the analysis from its published results and posted files. They found reversed sample labels and gene lists shifted by one position, and the trials were suspended. The prologue argues that most machine learning failures in biology are data failures. It explains why the author, with around sixty computational biology analyses open-sourced and almost none of them machine learning, began the work this book is rewritten from.
---

Cancer patients at Duke University were assigned to chemotherapy regimens chosen by a machine learning model. The model was wrong. Proving it took two statisticians more than 1,500 hours (Coombes, 2012), because the code and the processed data behind it were never released in full.

The method was published in *Nature Medicine* in 2006. It read the gene expression profile of a patient's tumour and predicted which drug that tumour would respond to. Oncology wants this badly, and three clinical trials were built on it. What went wrong is the reason this book exists. None of the errors found later was in the algorithm.

Keith Baggerly and Kevin Coombes, biostatisticians at MD Anderson, tried to reuse the method and could not reproduce it. So they reverse-engineered the analysis from the published results and the files the authors had posted, a practice they called forensic bioinformatics (Baggerly and Coombes, 2009). They found sample labels reversed between the responder and non-responder groups, and gene lists shifted by one position against their identifiers. Off-by-one errors and mislabelled columns: the kind of thing that never appears in a methods section. The trials were suspended.

The lesson generalises far beyond this case. In biology, most machine learning failures are not modelling failures. They are data failures wearing a model's clothes. An accuracy figure means nothing until you know the provenance of every label that produced it, and checking that requires understanding the laboratory assay, not the model's architecture.

## Why I am writing this

When I began writing the daily posts this book is rewritten from, I had open-sourced around sixty computational biology analyses: metagenomic co-assemblies, pangenomes, single-nucleus atlases, cross-tissue transcriptome-wide association studies, spatial transcriptomics. Almost none of it was machine learning.

It was the half of the problem that Baggerly and Coombes were doing: provenance, labels, the orientation of a matrix. The other half, building models, was missing. Both halves are required, and most people I meet are missing one of them.

So I set out to spend the next year, or years, helping everyone close that gap. The plan was foundations first, then classical methods on omics data, then deep learning, sequence models, and generative and agentic systems. The code, the notebooks, the mistakes and the dead ends would all be open-sourced and public. This book covers the first part of that plan, the basics of machine learning in seven models from logistic regression to k-means, and it stops there on purpose.

<p class="prov">This prologue is rewritten from the post for Day 1 of the series.</p>

## References

Baggerly, K. A. and Coombes, K. R. (2009). Deriving chemosensitivity from cell lines: Forensic bioinformatics and
reproducible research in high-throughput biology. *The Annals of Applied Statistics*, 3(4), 1309-1334.
https://doi.org/10.1214/09-AOAS291

Coombes, K. R. (2012). The need for publicly verifiable and reproducible data and analyses. Slides for a talk at
Research Integrity, Mohonk, 8 August 2012.
<https://www.uab.edu/norc/images/conferences/documents/KCoombes-Mohonk-Aug-2012.pdf>
