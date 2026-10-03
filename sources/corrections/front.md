# Corrections for the front and back matter: preface, prologue and epilogue

Each entry gives the sentence before and after the change, the source that settles it, and the value found there. The
front and back matter have no repository of their own. For the prologue the sources are the published works it
describes, each checked against the document itself and, where it has a DOI, against its Crossref record
(`https://api.crossref.org/works/<doi>`). For the preface and the epilogue they are the chapter repositories at the
commits the chapters pin.

## 1. The hours Baggerly and Coombes spent, thousands to more than 1,500 (prologue)

Before: Proving it took two statisticians thousands of hours, because the code and the processed data behind it were
never released.

After: Proving it took two statisticians more than 1,500 hours (Coombes, 2012), because the code and the processed data
behind it were never released.

Before (front matter summary): Two biostatisticians at MD Anderson, Keith Baggerly and Kevin Coombes, spent thousands of
hours reconstructing the analysis from its published figures ...

After: ... spent more than 1,500 hours reconstructing the analysis from its published figures ...

Source: Kevin R. Coombes, "The need for publicly verifiable and reproducible data and analyses", slides for a talk at
Research Integrity, Mohonk, 8 August 2012,
`https://www.uab.edu/norc/images/conferences/documents/KCoombes-Mohonk-Aug-2012.pdf` (29 pages, footed "© Copyright
2011-2012, Kevin R. Coombes and Keith A. Baggerly").

Value found: the slide headed "Did the System Work?", numbered 11 (page 12 of the PDF): "Why was it so hard for the
investigators to see the problems clearly? We spent 1500+ hours figuring out what happened." The "we" is the two
statisticians: the same slide speaks of "the seriousness of the scientific errors that we complained about". The deck
also shows the two errors the prologue names, under the headings "Gene Lists Were Off-by-One" (slide 2) and
"Sensitive/Resistant Labels Were Reversed" (slide 5), and its timeline (slide 8) has Duke suspending the trials in
September and October 2009 and again in July 2010. The post gives no source for "thousands of hours". The end of the
body sentence was changed later, in entry 9.

## 2. The paper is not named (prologue)

The sentence "The method was published in *Nature Medicine* in 2006." keeps the post's wording. A version of this
pass named the paper and its 2011 retraction, with the Crossref records for `10.1038/nm1491` and `10.1038/nm0111-135`
as evidence; on 2 October 2026 the author asked for the paper not to be cited, so the name, the retraction and the two
reference entries were removed again. Only the journal and the year, as the post gives them, remain.

## 3. Citations in the text, and a References section (prologue)

Added: "(Coombes, 2012)" after "more than 1,500 hours"; "(Baggerly and Coombes, 2009)" after "a practice they called
forensic bioinformatics"; and, after the provenance line, a References section with two entries: Baggerly and Coombes
(2009) and Coombes (2012).

Value found, entry by entry:

- Baggerly and Coombes (2009). The Crossref record for `10.1214/09-AOAS291` gives the title "Deriving chemosensitivity
  from cell lines: Forensic bioinformatics and reproducible research in high-throughput biology", *The Annals of Applied
  Statistics*, volume 3, issue 4, 1 December 2009, by Keith A. Baggerly and Kevin R. Coombes, and no page range. The
  pages are printed in the header of the article itself, "The Annals of Applied Statistics 2009, Vol. 3, No. 4,
  1309-1334, DOI: 10.1214/09-AOAS291", in the copy deposited on arXiv as `1010.1092`, and the arXiv record's journal
  reference gives the same pages. The abstract names the practice ("exercises in 'forensic bioinformatics'"), section
  2.2 is headed "Training data sensitive/resistant labels are reversed", and section 3.2 traces gene lists that were
  "off-by-one" to "a single row shift". The footer of the Day 1 post in the Chapter 1 repository traces "label
  reversals, off-by-one" to this paper.
- Coombes (2012). Title, event, date and address from the first slide and the file of entry 1, whose PDF metadata names
  Kevin R. Coombes as the author.

## 4. Where the book stops (prologue)

Before (the last sentence of the prologue): The code, the notebooks, the mistakes and the dead ends would all be
open-sourced and public.

After: The code, the notebooks, the mistakes and the dead ends would all be open-sourced and public. This book covers
the first part of that plan, the basics of machine learning in seven models from logistic regression to k-means, and it
stops there on purpose.

Sources: `sources/interlude-61.md` (Day 61: "Machine Learning for Biology ends here on purpose, at a real stopping
point, not because the models ran out") and `sources/epilogue.md` (Day 70: "Seven chapters, seven models, and the basics
of machine learning, one idea at a time"). The copies of both posts kept in the Chapter 7 repository
(`Qasim-Hussain-Code/immune_cell_subtype_discovery`, `posts/day_61.md` and `posts/day_70.md` at `1141fa411573`) say the
same.

Value found: the plan in the prologue runs from foundations and classical methods on omics data to deep learning,
sequence models and generative and agentic systems. The seven chapters run from logistic regression in Chapter 1 to
k-means in Chapter 7.

## 5. What Chapter 5 ran (preface)

Before: Chapter 5 sets out to use a support vector machine on gut bacteria and cardiovascular risk, and finds that the
data its design needs is not public, so it asks two narrower questions of a public dataset instead.

After: Chapter 5 sets out to use a support vector machine on gut bacteria and cardiovascular risk, finds that the data
its design needs is not public, and answers two narrower questions of a public dataset with logistic regression
instead.

Files: `docs/reanalysis_plan.md`, section 6, `src/tmao_cvd/models.py`, `src/tmao_cvd/reanalysis.py` and `README.md`, in
`Qasim-Hussain-Code/tmao_cardiovascular_risk_prediction` at Chapter 5's pinned commit `9985756c2db6`.

Value found: section 6 of the plan, question 1, "Estimator: unpenalised logistic regression"; question 2, "Model: L2
penalised logistic regression on all 600 metabolites". `models.py` defines `make_logistic_model` as
`LogisticRegression(penalty=None, solver="lbfgs", ...)`, which `reanalysis.py` fits to the precursor model and to the
model with TMAO added, and `reanalysis.py` fits the whole panel with `LogisticRegressionCV(Cs=np.logspace(-3, 1, 5),
cv=5, penalty="l2", ...)`. No file at that commit fits a support vector machine: outside the posts kept verbatim in
`posts/`, the only mention is the README's table entry for `posts/day51.txt`, "Why a support vector machine, and what
the kernel does". The README: "Days 47 to 51 set out a study of gut metagenomic gene abundances that the public data
could not support." This follows the Chapter 5 decision that the support vector machine never ran.

## 6. When the rules are written, before anything runs to before any model is fitted (preface)

Before: The rules are written down before anything runs, and in most chapters so are the ways the analysis could go
wrong.

After: The rules are written down before any model is fitted, and in most chapters so are the ways the analysis could go
wrong.

Files: `docs/reanalysis_plan.md`, section 2, in the Chapter 5 repository at `9985756c2db6`; the history of
`scripts/05_build_disagreement_set.py` and `notes/finish_pipeline.log` in
`Qasim-Hussain-Code/bakta_prokka_disagreement_prediction`, Chapter 3's repository, at `4f797c3fa09d`.

Value found: section 2 of Chapter 5's plan, "Disclosure of partial unblinding": "Before this plan was written, the
analyst had already loaded the matrix and computed univariate summaries of the four pathway metabolites by outcome
group, including a rank sum test on TMAO", and "The thresholds in section 6 were nevertheless fixed before any model was
fitted, any cross validation was run, or any discrimination, calibration or net benefit statistic was computed." So in
Chapter 5 something had run before the rules were written, but no model had. In Chapter 3 the label script took its
matching rule, one base of overlap on the same strand, in commit `0f6e6ef8cba5` at 09:03 UTC on 20 August 2026, and the
pipeline log has the label built at 19:47:06 and the forest fitted at 19:47:50 that day (+08:00), so there too the rule
that ran came before any model was fitted. This follows the Chapter 3 and Chapter 5 decisions.

## 7. The stage baseline, the stage itself to a model given only the stage (preface)

Before: ... guessing the commonest answer, a textbook rule about one position in a peptide, the stage a clinician
already knows, a model given nothing but how tightly each peptide binds the molecule that displays it.

After: ... guessing the commonest answer, a textbook rule about one position in a peptide, a model given only the stage a
clinician already knows, and one given nothing but how tightly each peptide binds the molecule that displays it.

File: `results/metrics/05_baseline_stage.json` in `Qasim-Hussain-Code/cancer_survival_ml_pipeline` at Chapter 4's
pinned commit `85d831ca383c`.

Value found: `"rule": "The comparison this model has to beat is stage alone."`; under `pooled`, `"model": "Cox
proportional hazards, stage only"` and `"features": ["pathological stage, one-hot, reference Stage I, with an explicit
unknown level"]`, fitted on 410 patients and scored on 176, concordance index 0.6743. The baseline is a model fitted to
stage, not the stage itself, as the Chapter 4 decision on how stage was turned into a score has it. The Chapter 6
baseline in the same sentence is, in `results/metrics/05_baseline_validation.json` of
`Qasim-Hussain-Code/neoantigen_immunogenicity_prediction` at `68a12d14824d`, "logistic regression on log10 measured
affinity in nM" with one feature, and needed no change.

## 8. What Chapter 5 ran (epilogue)

Before: The support vector machine of Chapter 5 looked for the widest possible gap between two outcomes.

After: Chapter 5 set out to use a support vector machine, a model that looks for the widest possible gap between two
outcomes, and the data it needed was not public. It answered two narrower questions with logistic regression instead.

Before (front matter summary): Seven chapters used seven models, from logistic regression to k-means, to teach the
basics of machine learning one idea at a time.

After: Seven chapters introduced seven models, from logistic regression to k-means, to teach the basics of machine
learning one idea at a time. Chapter 5 set out to use a support vector machine, found that the data it needed was not
public, and answered two narrower questions with logistic regression.

Files and value found: as in entry 5. Day 70 as kept in the Chapter 7 repository (`posts/day_70.md` at `1141fa411573`)
reads "Chapter 5, a support vector machine: the widest possible gap between two outcomes", as the book's copy does, and
no later post corrects it. "Seven chapters, seven models" still opens the epilogue: Chapter 5 still explains what a
support vector machine does, so the book introduces seven models, one to a chapter, though the one Chapter 5 introduces
was never fitted.

## 9. Why the reconstruction took so long, never released to never released in full (prologue)

Before: Proving it took two statisticians more than 1,500 hours (Coombes, 2012), because the code and the processed data
behind it were never released.

After: Proving it took two statisticians more than 1,500 hours (Coombes, 2012), because the code and the processed data
behind it were never released in full.

Sources: Baggerly and Coombes (2009), in the arXiv copy of entry 3, and the slides of entry 1. The Institute of
Medicine's report Evolution of Translational Omics: Lessons Learned and the Path Forward (2012,
`https://doi.org/10.17226/13297`), Appendix B, agrees with both.

Value found: Table 1 of Baggerly and Coombes (2009), "Locations of data used in our analyses", lists under "Potti et al.
(2006) web site, accessed April 4, 2009" the file "Binreg.zip", "Metagene prediction software", and under "Potti et al.
(2006) web site, November 6, 2007, no longer posted" the file "Adria_ALL.txt", "Numbers, Sens/Res labels for 144
samples, 22 training cell lines, 122 testing samples". Section 2.1: "We first acquired the raw doxorubicin (adriamycin)
data (Adria_ALL.txt) posted by Potti and Nevins (2007)", and section 2.2 finds that "The posted numbers have been
transformed relative to the MAS5 quantifications used earlier". Section 3: "We acquired the binreg Matlab scripts used
for model fitting and heatmap generation from the Potti et al. (2006) web site." So some of the code and some of the
processed data were released, and "never released" is contradicted. What was missing was the rest: section 7.2 names
"incomplete documentation and lack of reproducibility", and section 7.3.2 says "We see it as unavoidable that complete
scripts will also eventually be required." The slides, slide 26, "The Institutional Challenge" (page 28 of the PDF):
"Insisting that code and data be made publicly available would not have prevented the problems at Duke. We might have
found the problems earlier; others might have been able to confirm them more easily." Appendix B of the report:
"Computer code used to generate the gene expression-based computational models in Potti et al. (2006a) was available on
a Duke website (Baggerly and Coombes, 2009)", and "Even with access to the publicly available primary data and code
posted by the authors on a Duke website, Baggerly and Coombes were unable to reproduce the published results." The
post's "were never released", which entry 1 kept, is the wording changed here.

## 10. What the analysis was reconstructed from (prologue)

Before: So they reverse-engineered the analysis from the published figures, a practice they called forensic
bioinformatics (Baggerly and Coombes, 2009). (Summary: ... reconstructing the analysis from its published figures ...)

After: So they reverse-engineered the analysis from the published results and the files the authors had posted, a
practice they called forensic bioinformatics (Baggerly and Coombes, 2009). (Summary: ... reconstructing the analysis
from its published results and posted files ...)

Source: Baggerly and Coombes (2009), as in entry 9.

Value found: the abstract describes forensic bioinformatics as working from "aspects of raw data and reported
results", Table 1 lists the files taken from the authors' website ("Binreg.zip", "Adria_ALL.txt"), and section 3 says
the Matlab scripts were acquired from that site. The post's "from the published figures" named only part of what they
worked from.

## 11. Before running anything, to before fitting anything (epilogue)

Before: Fix the rules before running anything.

After: Fix the rules before fitting anything.

Files and value found: as in entry 6. In Chapter 5 the data had been loaded and summarised before the reanalysis rules
were written, and in Chapter 3 the label was built with the rule that ran before the rule was posted; in every chapter
the rules were fixed before any model was fitted, which is what the maxim now says. Day 70's wording was "before
running anything".

## 12. One post a day, wrote to posted (preface)

Before: Between 24 July and 1 October 2026 I wrote seventy of them on machine learning for biology, one a day, each
written to stand on its own.

After: Between 24 July and 1 October 2026, I posted seventy of them on machine learning for biology, one a day, each
written to stand on its own.

Files: the history of `posts/` in `Qasim-Hussain-Code/cancer_survival_ml_pipeline`, Chapter 4's repository, up to its
pinned commit `85d831ca383c`, with `sources/series-dates.md`.

Value found: commit `26aef85b1464` ("add_prereg_posts"), at 09:57 UTC on 3 September 2026, adds `posts/day40.txt` to
`posts/day44.txt`, and the pinned commit `85d831ca383c` ("add_day45_post"), at 09:21 UTC on 4 September, adds
`posts/day45.txt`. With seventy posts on the seventy days from 24 July to 1 October (`sources/series-dates.md`), one to a
day, Day 42 fell on 3 September, Day 43 on 4 September, Day 44 on 5 September and Day 45 on 6 September, so the posts
for Days 43 to 45 were written before the days they appeared. What the sources give is one post for each day, not one
written each day.

## 13. What was not in the algorithm (prologue)

Before: What went wrong is the reason this book exists. It was not the algorithm.

After: What went wrong is the reason this book exists. None of the errors found later was in the algorithm.

Source: Baggerly and Coombes (2009), https://doi.org/10.1214/09-AOAS291, section 7.3.1.

Value found: the errors the reconstruction found, sensitive and resistant labels reversed and gene lists shifted by one
row, were in the data and its handling, not in the classifier. Section 7.3.1 adds that the approach did no better
without them: "We have tried making predictions from the NCI60 cell lines when we step through the process without the
errors noted above, and we get results no better than chance." So "It was not the algorithm" could be read as saying the
method would otherwise have worked, which the record does not support. The sentence now says only what the record shows.

## 14. Why Chapter 5's design never ran (preface and epilogue)

Before (preface): Chapter 5 sets out to use a support vector machine on gut bacteria and cardiovascular risk, finds that
the data its design needs is not public, and answers two narrower questions of a public dataset with logistic regression
instead.

After: Chapter 5 sets out to use a support vector machine on gut bacteria and cardiovascular risk, finds that the public
data cannot support its design, and answers two narrower questions of a public dataset with logistic regression instead.

Before (epilogue): Chapter 5 set out to use a support vector machine, a model that looks for the widest possible gap
between two outcomes, and the data it needed was not public.

After: Chapter 5 set out to use a support vector machine, a model that looks for the widest possible gap between two
outcomes, but the public data could not support the design it was chosen for.

Before (epilogue summary): Chapter 5 set out to use a support vector machine, found that the data it needed was not
public, and answered two narrower questions with logistic regression.

After: Chapter 5 set out to use a support vector machine, found that the public data could not support the design, and
answered two narrower questions with logistic regression.

File: `README.md` in Chapter 5's repository at 9985756c2db6.

Value found: "Days 47 to 51 set out a study of gut metagenomic gene abundances that the public data could not support."
The README's "No public dataset supports it" and "controlled access" are about the later plasma TMAO question, not the
metagenomic design. Chapter 5 itself says "that design never ran, because the public data could not support it", and
keeps "not public" for the TMAO question, where it belongs. This replaces the wording chosen under front decision 4.
Chapter 6's cross-reference is changed to match (sources/corrections/ch6.md entry 9).
