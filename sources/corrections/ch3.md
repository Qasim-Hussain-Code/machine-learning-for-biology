# Corrections for Chapter 3, Is a gene a fact or a call? (random forest)

Each entry gives the chapter's sentence before and after the change, the repository file that settles it, and the
value found there. The repository is `Qasim-Hussain-Code/bakta_prokka_disagreement_prediction` at the chapter's pinned
commit `4f797c3fa09d` throughout.

## 1. The regions given Bakta's fallback names, 4,650 to 4,494

Before: There are 4,650 such regions, 9% of the set, disagreeing almost every time. Take them out and the remaining
45,716 regions disagree 47.0% of the time.

After: There are 4,210 such regions, and 284 more where Bakta calls the protein uncharacterised and adds only the name
of its open reading frame, which Prokka never matches either. Together that is 4,494 regions, 9% of the set,
disagreeing almost every time. Take them out and the remaining 45,716 regions disagree 47.0% of the time.

Files: `results/metrics/22_content_mechanism.json`, with `results/metrics/12_content_cohort.json`, `README.md` and the
patterns in `scripts/lib_names.py`.

Value found: under `fallback_naming_families`, `"per_pattern_counts_overlapping": {"domain_containing": 4210, "duf":
156, "uncharacterized_orf_name": 284}`, `"sum_of_patterns_double_counts": 4650`, `"distinct_union": 4494` and
`"duf_entirely_inside_domain_containing": true`; the excluded set is `"families": {"n": 4494, "n_disagree": 4491,
"rate": 0.9993}` and what is left is `"remainder": {"n": 45716, "n_disagree": 21486, "rate": 0.47}`.
`12_content_cohort.json`, under `declared_generic_families_within_primary_set`, gives the same split:
`uncharacterized_orf_name` n 284 with a disagreement rate of 1.0, `domain_containing` n 4210 at 0.9993, and
`none_of_these` n 45716 at 0.47. The README: "matched independently they total 4,650 rows, but every one of the 156 DUF
names also ends in `domain-containing protein`, so the sum double-counts. 4,494 is the distinct union." 4,650 counts
the 156 DUF names twice, and 50,210 less 4,494 is the 45,716 the chapter already gives, where 50,210 less 4,650 would be
45,560. The 284 are the pattern `(?i)^uncharacteri[sz]ed protein [A-Za-z0-9_.\-]+$` in `scripts/lib_names.py`, the
name Uncharacterized protein followed by one open reading frame name, which the README lists among the conventions
"which cannot match Prokka by construction". The 9% holds: 4,494 of 50,210 is 9.0%.

The closing section repeats the exclusion and was changed with it, from "Without one tool's habit of naming genes after
a generic protein domain, it is still 47.0%." to "Without one tool's habit of naming genes after a generic protein
domain, or after an open reading frame alone, it is still 47.0%." The 47.0% leaves out the 284 as well. Leaving out
the 4,210 domain names alone would leave 46,000 regions, of which 21,770 disagree, which is 47.3%.

## 2. The random forest's false alarms, 2,142 to 2,140

Before: 3,965 of those flags were correct. 2,142 were not.

After: 3,965 of those flags were correct. 2,140 were not.

File: `results/metrics/17_content_final_random_forest.json`, repeated in `results/metrics/19_content_circularity.json`
(`arms.full.test` and `side_by_side.full`) and `results/metrics/20_content_summary.json`.

Value found: under `test.confusion_matrix_counts`, `"true_negative": 4036`, `"false_positive": 2140`,
`"false_negative": 2142`, `"true_positive": 3965`, on `"n_rows": 12283` with `"n_positive": 6107`. The flags are the
true positives and false positives together, 3,965 and 2,140, which is the 6,105 the chapter gives in the sentence
before. 2,142 is the false-negative count, the real disagreements the forest did not flag; 3,965 and 2,142 together are
the 6,107 real disagreements among the test regions, not the flags. The ratio the chapter draws next, one false alarm
in every three flags, holds at 2,140 of 6,105.

## 3. The length expectation, from written before any result to reasoned from the tools

Before (What the two tools actually do): That changed what I expected the forest to find. If the two callers were
independent, disagreement might trace to something subtle in the sequence, a signal one caller catches and the other
misses. If they mostly share a caller, disagreement should trace to something blunter. Length, mostly, because short
proteins are what one tool looks for and the other does not. I wrote this down before I had looked at a single result.
If the forest's top feature, the column of data it leaned on most, turned out not to be length, I would have
misunderstood something.

After: That changes what the forest should find. If the two callers were independent, disagreement might trace to
something subtle in the sequence, a signal one caller catches and the other misses. If they mostly share a caller,
disagreement should trace to something blunter. Length, mostly, because short proteins are what one tool looks for and
the other does not. If the forest's top feature, the column of data it leans on most, is not length, I have
misunderstood something.

Before (Seventy-two rows): I had predicted that any disagreement would be blunt rather than subtle. What I did not know
was the size. I expected a small signal. I got 72 rows.

After: I expected a small signal. I got 72 rows.

Before: The expectation about length held. Asked to pick out the 72 coordinate disagreements, the forest leaned on
length more than anything else.

After: The reasoning about length held. Asked to pick out the 72 coordinate disagreements, the forest leaned on the
length Bakta gave each call more than on anything else.

Files: `notes/lab_notebook.md`, `notes/finish_pipeline.log`, `results/metrics/09_feature_importance.json` and
`results/metrics/06_features.json`, with `sources/series-dates.md`.

Value found: the notebook's first entry, dated 2026-08-20 and headed "panel chosen, annotation started", records no
expectation about length and no shared gene caller. The shared caller first appears in the next entry, headed "the
pipeline ran, and the premise mostly failed", where it is read from the output: "The reason is visible in the GFF
`source` column", followed by "This was knowable before a single genome was downloaded, by reading what each tool
wraps." The run log builds the label at `2026-08-20T19:47:06+08:00`, fits the forest at `19:47:50` and ranks its
features at `19:48:53`. The series ran one post a day from 24 July 2026, so the Day 29 post that stated the expectation
appeared on 21 August, after those results existed, and nothing in the repository records the expectation earlier. The
ranking itself stands: `09_feature_importance.json`, `"measured_on": "held-out genomes, not the training set"`, puts
`"feature": "length_bp"` first by permutation (`0.304133`) and by impurity (`0.151783`), and `06_features.json`
describes it as `"length of the interval Bakta chose"`. The chapter's own "The reason was sitting in the tools' own
documentation, and I had not read it first" agrees with the record.

## 4. The rule that built the label, from seventy per cent overlap to one shared base on the same strand

Before (The rules): The rule for what counts as a disagreement was published before I had run it on a single genome. A
gene call from Bakta and a gene call from Prokka count as the same call under one condition: they overlap by seventy per
cent or more on both sides, meaning the shared stretch covers at least seventy per cent of each call, and they sit on
the same strand.

After: The rule for what counts as a disagreement was written into the code before the label was built. Each
protein-coding gene Bakta called is one row. If anything Prokka annotated on the same strand overlaps that call, by as
little as a single base, the call counts as matched. If nothing does, Bakta made a call there and Prokka did not, and
the row is a disagreement.

Before: Fifty per cent is the common convention. I chose seventy because of how these tools differ. They mostly agree on
where a gene starts and stops, and when they do not, it is usually over the exact start codon: a difference of a few
dozen letters, inside a call both tools clearly made. That is not a disagreement. Both tools found the gene. Seventy per
cent still calls it a match, and it is tight enough that a genuinely different claim cannot sneak through as one (Figure
3.2).

After: One base sounds loose, and it is meant to be. The two tools mostly agree on where a gene starts and stops, and
when they do not, it is usually over the exact start codon: a difference of a few dozen letters, inside a call both
tools clearly made. That is not a disagreement. Both tools found the gene. A rule that demanded a large overlap on both
sides would turn some of those start-codon differences into missing genes. So the label asks only whether Prokka claimed
the stretch at all. Whether the two calls share a start, and whether they share a stop, are recorded beside the label
rather than mixed into it (Figure 3.2).

Before: Strand matters twice. DNA has two strands, and a gene can sit on either. A call on the other strand is a
different gene, not the same gene read differently, so two calls must share a strand to count as a match. And if Prokka
has a call on the opposite strand where Bakta has one, the region is not empty. Prokka made a claim there, a different
claim rather than a missing one. Counting that region as one Bakta called and Prokka did not would make the label say
something it does not mean.

After: Strand matters. DNA has two strands, and a gene can sit on either. Two genes on opposite strands can occupy the
same letters and still be different genes, so only what Prokka annotated on the same strand is consulted. If the only
call Prokka made at that place is on the other strand, the Bakta call counts as one Prokka did not make. The kind of
annotation does not matter. If Prokka called a transfer RNA on the same strand where Bakta called a protein-coding gene,
Prokka did not leave the region empty. It made a different claim, not a missing one, and counting it as silence would
put two unlike things in one label. Those calls count as matched, and there are 29 of them.

Before: One more decision was easy to get wrong. When both tools call the same gene but pick different start codons,
which coordinates go in the table? Using one tool's coordinates for the agreed cases would hide a tell, and the model
could learn that tool's habits instead of the sequence. So the table records the overlap between them, which belongs to
neither tool and to both.

After: One more decision was easy to get wrong. When both tools call the same gene but pick different start codons,
which coordinates go in the table? Every row carries Bakta's, matched or not: where Bakta's call starts and stops, and
how long it is. How much of it Prokka's call covers is kept as a separate count. So the length of every call in the
table is the length Bakta chose, and a model that leans on length can learn that tool's habits instead of the sequence.

Before: Two more thresholds went into the record alongside seventy per cent: fifty and ninety. They were named as
sensitivity checks, a test of how much the answer depends on where the line is drawn, not as alternatives to switch to
later. That line matters more than it looks. A threshold chosen after seeing which one gives the better story is not a
threshold. It is the story wearing a number.

After: The rule did not change once the label existed, and that matters more than it looks. A threshold chosen after
seeing which one gives the better story is not a threshold. It is the story wearing a number.

Before (rules box): **Fixed before any genome was run.** Two calls are the same call if they overlap by seventy per cent
or more, on both sides, on the same strand. A region where Prokka has a call on the opposite strand is not counted as
empty. Calls both tools made are recorded by the overlap of their coordinates, not by either tool's own. Fifty and
ninety per cent are recorded as sensitivity checks, not as alternatives.

After: **Fixed before the label was built.** Each protein-coding gene Bakta called is one row. It counts as matched if
anything Prokka annotated on the same strand overlaps it by at least one base, whatever the kind of annotation; if
nothing does, it is a call Prokka did not make. Prokka's annotations on the opposite strand are not consulted. Every row
carries Bakta's coordinates. The overlap with Prokka's call, and whether the two calls share a start and a stop, are
recorded beside the label, not in it.

Before (caption of Figure 3.2): The overlap rule, fixed before the pipeline ran. Calls that overlap by seventy per cent
or more on both sides, on the same strand, are one call; below the threshold they are two claims.

After: The rule that built the label. A Bakta call that shares even one base with anything Prokka annotated on the same
strand is matched; a Bakta call with nothing from Prokka on its strand is a call Prokka did not make, whatever Prokka
called on the other strand.

After (the caption as it now stands, after the figure was drawn for the book as `figures/svg/fig-3-2.svg`): The rule
that built the label, in three cases, with each arrow pointing along the strand it sits on. A Bakta call that shares
even one base with anything Prokka annotated on the same strand is matched, whether Prokka's call starts somewhere else
or is another kind of annotation, such as a transfer RNA; a Bakta call with nothing from Prokka on its strand is a call
Prokka did not make, whatever Prokka called on the other strand.

The alternative text of Figure 3.2 was rewritten to the same content, and again when the figure was drawn, to describe
its three cases.

Before (Seventy-two rows): The overlap threshold turned out not to matter. When 87,788 of 87,888 pairs are
coordinate-identical, the distribution of overlaps sits at the two extremes with almost nothing in between. Fifty,
seventy or ninety would have given nearly the same answer. I could not have known that in advance, and choosing the
threshold afterwards, once I could see which one flattered the result, would not have been a choice at all. A rule that
turns out not to bind is still worth fixing beforehand.

After: How much overlap the rule demanded hardly mattered. When 87,788 of the 87,888 matched calls are identical to the
base, they would match under any threshold, and the 72 with nothing overlapping them would match under none. A stricter
threshold could have changed the label for at most the remaining hundred of the 87,960 calls. I could not have known
that in advance, and choosing the threshold afterwards, once I could see which one flattered the result, would not have
been a choice at all. A rule that turns out not to bind is still worth fixing beforehand.

Files: `scripts/05_build_disagreement_set.py`, `results/metrics/05_disagreement.json` and `notes/finish_pipeline.log`,
with the history of the script and a search of five commits up to the pinned one.

Value found: the script's docstring: "The unit of analysis is one Bakta CDS call. The label is: 1 no Prokka feature
overlaps this interval on the same strand, 0 some Prokka feature does". Then: "Same strand only. Two genes on opposite
strands can occupy the same coordinates and still be different genes. Counting an opposite-strand overlap as agreement
would quietly mark real disagreements as matched." "Any Prokka feature type, not only CDS. If Prokka called a tRNA where
Bakta called a CDS, Prokka did not leave the region empty [...] folding it into the positive class would put two unlike
things in one label. Those cases are labelled 0 and kept identifiable via overlap_category." "One base pair of overlap
is enough to count as a match. Gene callers routinely pick different start codons for the same gene; requiring
reciprocal overlap would relabel start-codon disagreements as missing genes. Boundary disagreement is recorded
separately, as same_start and same_stop, rather than being mixed into the label." The code looks Prokka's features up by
`(seqid, strand)` alone (line 137), skips every Bakta feature that is not a CDS (line 139), and writes each row with
Bakta's `"start"`, `"end"` and `"length_bp"`, the overlap kept apart as `"best_overlap_bp"` and `"best_overlap_frac"`
(lines 158 to 177). `05_disagreement.json`: `"label_definition": "1 = no Prokka feature of any type overlaps this
interval by at least 1 bp on the same strand; 0 = one does"`, `"overlap_rule": "same strand, >=1 bp, any Prokka feature
type"`, `"category_counts": {"cds": 87859, "none": 72, "non_cds": 29}`, and under `boundary_agreement_among_matched`,
`"n_matched": 87888`, `"same_start_and_stop": 87788`, `"same_stop_only": 22`, `"same_start_only": 15`, `"neither": 63`.
The script was a stub, `raise SystemExit("not implemented")`, from `1f5d5ca2bffb` (14 August) until `0f6e6ef8cba5`
(`2026-08-20T09:03:55Z`), which wrote the rule above; the file is unchanged from there to `4f797c3fa09d`. The run log
builds the label at `2026-08-20T19:47:06+08:00`, 11:47 UTC the same day. No script, metrics file or document at
`1f5d5ca2bffb`, `0f6e6ef8cba5`, `414f949f9079`, `4c70e4515407` or `4f797c3fa09d` holds a percentage overlap threshold or
names fifty, seventy or ninety per cent as a check; the only threshold of 0.7 is `CORRELATION_THRESHOLD` in
`scripts/09_feature_importance.py` and `scripts/18_content_importance.py`, which groups correlated features. The post
that set out the seventy per cent rule, Day 30, appeared on 22 August, after the label was built.
Identical coordinates mean the two calls cover each other completely, so the 87,788 would match under any threshold; the
72 share no base on their strand with anything Prokka annotated, so they would match under none; 87,888 less 87,788
leaves the 100 whose label a stricter threshold could change.

## 5. The name rule, its full steps, and when it was fixed

Before (The rules): So names are normalised before comparison: strip a trailing bracket, and strip a trailing gene
symbol, because one tool often appends it and the other does not.

After: So names are normalised before comparison. Strip a trailing bracket. Strip a trailing gene symbol, because one
tool often appends it and the other does not. Strip a leading hedge word: putative, probable, possible, predicted or
conserved. Then ignore capitals and treat punctuation as a space. Under that rule, putative cytosol aminopeptidase and
Cytosol aminopeptidase are the same name.

Before (rules box): **Fixed before the names were compared.** Names are compared after stripping a trailing bracket and
a trailing gene symbol. The result is checked against the strings with nothing stripped, and against the loosest rule I
was willing to defend: drop generic words and ignore word order.

After: **Fixed before any model was fitted.** Names are compared after stripping a trailing bracket, a trailing gene
symbol and a leading hedge word such as putative, then ignoring capitals and treating punctuation as a space. The result
is checked against the strings as written, ignoring only capitals, spacing and a final full stop, and against the
loosest rule I was willing to defend, which also drops generic words and ignores word order. Both are checks, not
alternatives to switch to.

Before (Half the names): Compare the strings with nothing stripped and 56.0% disagree.

After: Compare the strings as written, ignoring only capitals, spacing and a full stop at the end, and 56.0% disagree.

Files: `scripts/lib_names.py` and `results/metrics/13_name_rules.json`, with `README.md`.

Value found: `13_name_rules.json`, `normalisation_rule.primary`: "1. Unicode NFKC, trim.", "2. Strip trailing (...) or
[...] qualifiers, repeatedly.", "3. Strip ONE trailing gene-symbol token.", "4. Strip leading hedges: putative,
probable, possible, predicted, conserved.", "5. Case-fold; every run of non-alphanumerics becomes one space; collapse
whitespace."; `"strict_sensitivity_check": "case-fold and whitespace only; nothing stripped"`; and under
`worked_examples.called_same_despite_differing_raw_strings`, `"product_bakta": "putative cytosol aminopeptidase"`
against `"product_prokka": "Cytosol aminopeptidase"`, both normalised to `"cytosol aminopeptidase"`, 12 times.
`lib_names.normalise` applies the five steps in that order (`HEDGES = ("putative", "probable", "possible", "predicted",
"conserved")`), and its strict level returns `re.sub(r"\s+", " ", s).rstrip(".").lower()` after NFKC and trimming, so
the strict check folds case, collapses spacing and drops a final full stop. On timing: `"fixed_before_fitting": "The
placeholder list, the normalisation rule and the two sensitivity checks were declared and approved before any model was
fitted. They are not revised after seeing a score."`, and the module's docstring says the same. Nothing in the record
dates the rule against the first comparison of names, and the first draft of the symbol strip was run on the names
before it was fixed, as the rules box records under Changed after looking. `"sensitivity_checks_were_named_in_advance":
"strict and loose are reported alongside primary. They are not alternatives to switch to after seeing which gives a
better number."` The rates are unchanged: strict `0.5601`, primary `0.5174`, loose `0.5062`.

## 6. The panel of 25 genomes, one from each of 25 species

Before (front matter summary): Bakta and Prokka were run on the same 25 genomes, and they almost never disagreed about
where genes are.

After: Bakta and Prokka were run on the same 25 bacterial genomes, one from each of 25 species, and they almost never
disagreed about where genes are.

Before (Seventy-two rows): The pipeline ran. Across a panel of 25 bacterial genomes, Bakta made 87,960 gene calls, and
72 of them have no matching call from Prokka.

After: The pipeline ran on 25 bacterial genomes, one from each of 25 species spread across eight phyla. The
*Campylobacter jejuni* genome this chapter opened with is one of them. Across all 25, Bakta made 87,960 gene calls, and
72 of them have no matching call from Prokka.

Files: `data/accessions.tsv` and `results/metrics/01_genomes.json`, with `data/species.tsv`, `README.md` and
`notes/lab_notebook.md`.

Value found: `accessions.tsv` lists 25 species with one accession each, in eight phyla: Spirochaetota, Bacillota,
Campylobacterota, Pseudomonadota, Bacteroidota, Cyanobacteriota, Actinomycetota and Deinococcota. The README: "one panel
of 25 complete bacterial genomes (95.2 Mbp, 8 phyla, ...)"; the notebook: "25 species, one genome each" and "Spread
across 8 phyla instead." The *C. jejuni* genome is `GCF_000009085.1` (`ASM908v1`, taxid `192222`), and `01_genomes.json`
gives its `"length_bp": 1641481`, the 1,641,481 letters of the chapter's opening.

## 7. When the zero-rRNA failure was found, and what it would have done

Before: It printed Found 0 rRNAs and finished. This surfaced while I was checking why the held-out set had only 13
positives.

After: It printed Found 0 rRNAs and finished. I found it while the annotation was still being set up, before any label
had been built.

Before: Think about what that does to the label. The label was a region one tool called and the other did not. If Prokka
finds no ribosomal RNA anywhere, then every ribosomal RNA Bakta calls becomes a disagreement. Not a real one: a missing
shared library, written into the training data as biology.

After: Think about what that would have done to the comparison. A disagreement is a region one tool called and the other
did not. If Prokka finds no ribosomal RNA anywhere, then every ribosomal RNA Bakta calls looks like one. Not a real one:
a missing shared library, which would have gone into the data as biology.

The alternative text of Figure 3.3 changed with it, from "what it would have done to the label" to "what it would have
done to the comparison". When the figure was drawn for the book as `figures/svg/fig-3-3.svg`, its alternative text was
rewritten to describe the chain of programs alone, and it no longer says what the failure would have done.

Files: `notes/lab_notebook.md`, `scripts/lib_env.sh`, `scripts/05_build_disagreement_set.py` and
`results/metrics/04_calls.json`.

Value found: the notebook records the failure in its first entry, dated 2026-08-20 and headed "panel chosen, annotation
started": "Prokka found zero rRNAs in all 25 genomes [...] and still exited 0" and "First full Prokka run (87,901 CDS, 0
rRNA) was discarded and re-run." The same entry ends: "Bakta annotation not yet run; waiting on the database." and
"Nothing downstream of `04` has been executed on real data yet." The label is step 05, and the held-out set with 13
positives first appears in the next entry: `Held-out set: 18,735 rows, **13 positives**.` `lib_env.sh`, which holds the
fix: "with no rRNA from Prokka, every rRNA locus Bakta calls looks like a tool disagreement when it is really a missing
shared library." The label as built takes only Bakta's CDS calls as rows (`if cds["ftype"] != "CDS": continue`), so a
Bakta ribosomal RNA is never a row of it; the passage now describes the comparison of the two tools' output, as
`lib_env.sh` does, and no longer says that each ribosomal RNA would have become a disagreement in the label. After the
fix Prokka reports 351 rRNAs across the panel (`04_calls.json`, `totals.prokka.feature_counts`, `"rRNA": 351`).

## 8. The regions both tools called, 87,859, and the base of the 29,808

Before: With the coordinates settled, the same regions could be asked a different question. The two tools agree almost
perfectly on where genes are. Do they agree on what those genes are?

After: With the coordinates settled, the same regions could be asked a different question. At 87,859 places, both tools
called a protein-coding gene, almost always with the same start and stop. Do they agree on what those genes are?

Before: 29,808 pairs have identical raw strings. There are zero violations.

After: Across all 87,859 regions both tools called, 29,808 pairs have identical raw strings. There are zero violations.

Files: `results/metrics/12_content_cohort.json`, `results/metrics/13_name_rules.json` and
`scripts/12_content_cohort.py`, with `results/metrics/05_disagreement.json`.

Value found: `12_content_cohort.json`: `"pairing_rule": "same sequence, same strand, largest overlap in bp, Prokka
feature must be a CDS"`, `"n_paired": 87859`, `"n_unpaired": 101` and `"coordinate_agreement_among_pairs":
{"identical_start_and_stop": 87788, ...}`. `13_name_rules.json`, `symmetry_invariant`:
`"n_pairs_with_identical_raw_strings": 29808`, `"n_violations": 0`, over `"n_pairs": 87859` (`placeholder_rule.totals`).
`12_content_cohort.py` calls `lib_names.assert_symmetric(pairs)` on every pair, placeholders included, before the 50,210
regions both tools named are drawn from them, so 29,808 is a count over the 87,859 and not over the 50,210. The 87,859
are the 87,888 calls Prokka matched less the 29 it matched only with a feature that is not a CDS
(`05_disagreement.json`, `"cds": 87859`, `"non_cds": 29`). The 19,216 and 48,201 given two paragraphs after the first change
count over the same regions: "Bakta emits gene= on 19,216 of 87,859 CDS against Prokka's 48,201" (`13_name_rules.json`,
`step_3_is_pair_symmetric`).

## 9. The Matthews correlation coefficient, named (a clarification)

Before (front matter summary): A random forest predicted those naming disagreements with an MCC of 0.303, but its signal
came from database coverage, and with only DNA features on genomes held out properly it scored 0.070.

After: A random forest predicted those naming disagreements with a Matthews correlation coefficient (MCC) of 0.303 on
five held-out genomes, but its signal came from what each tool found in its reference databases, and with only DNA
features it scored 0.142 on the same genomes and 0.070 in cross-validation on the twenty training genomes.

Before (note): **MCC.** A score that punishes false alarms as much as it rewards true catches

After: **Matthews correlation coefficient (MCC).** A score that punishes false alarms as much as it rewards true catches

File: `scripts/lib_content.py`.

Value found: the selection rule, "mean Matthews correlation coefficient across five genome-grouped folds of the training
genomes", and every score in the naming experiment is computed with scikit-learn's `matthews_corrcoef`. The posts give
only "MCC". Naming the measure is a clarification rather than a correction. The rest of the summary sentence is entries
14 and 15.

## 10. The baseline at 0.000, guessing randomly to the model that always says yes

Before: So the honest comparison uses a different measure, MCC. Guessing randomly scores 0.000.

After: So the honest comparison uses a different measure, MCC, with every model and baseline scored on the same regions,
all from five genomes held out of training. The model that always says yes scores 0.000, as any model that gives the
same answer every time must.

Before (alternative text of Figure 3.5): Infographic. A model that always guesses the same answer scores 0.664 with F1,
the highest in the comparison, and 0.000 with MCC. A bar chart of MCC shows guess randomly 0.000, protein length only
0.028, database match only 0.141, one decision tree 0.261, random forest 0.303 and gradient boosting 0.288.

After: Chart. The model that always says yes scores 0.664 with F1, the highest F1 in the comparison, and 0.000 with MCC.
A bar chart of MCC on the same held-out regions shows always says yes 0.000, protein length only 0.028, Prokka's
UniProtKB match only 0.141, one decision tree 0.261, random forest 0.303 and gradient boosting 0.288.

Before (caption of Figure 3.5): The same constant model scored with F1 and with MCC, and the MCC of each model and
baseline. The random forest is highest at 0.303.

After: The model that always says yes, scored with F1 and with MCC, and the MCC of each model and baseline on the same
held-out regions. The random forest is highest at 0.303.

After (the alternative text and caption as they now stand, after the figure was drawn for the book as
`figures/svg/fig-3-5.svg`): the alternative text describes horizontal bars of MCC on an axis from 0 to 0.4, every model
scored on the same held-out regions, with three baselines in grey (the model that always says yes, a hairline at zero
marked 0.000, with the note but 0.664 with F1, the highest F1 of all; protein length only, 0.028; Prokka's UniProtKB
match only, 0.141) and three models in colour (one decision tree, 0.261; random forest, 0.303; gradient boosting,
0.288). The caption: MCC for the three baselines, in grey, and the three models, all scored on the same held-out
regions, on an axis from zero. The model that always says yes scores 0.000, although its F1 of 0.664 was the highest of
all; the random forest is highest at 0.303.

File: `results/metrics/15_content_baselines.json`, with `README.md`.

Value found: `"scored_on": "held-out test genomes only, the same rows every model is scored on"`, `"n_test_rows":
12283`. Under `majority_class`: `"description": "always predict the majority class of the training genomes"`,
`"predicted_class": 1`, `"train_positive_rate": 0.5239`, and on the test rows `"recall": 1.0`, `"f1": 0.66417`, `"mcc":
0.0`, with the note "MCC is 0 by construction for a constant predictor." No baseline in the repository guesses at
random. The 0.000 belongs to the constant model that says yes to every region, the same model that scores 0.664 on F1
earlier in the same section. The README's results table: `majority class | 0.000 | 0.497 | 0.664`.

## 11. The 0.141 baseline, a database match by either tool to Prokka's UniProtKB match, a substitute

Before: One that looks only at whether either tool found a database match for the region scores 0.141.

After: One that looks only at whether Prokka found a similar protein in UniProtKB, a large public protein database,
scores 0.141. It stands in for the baseline I had planned, which asked whether either tool had left the protein unnamed:
every region here was named by both tools, so that question has the same answer everywhere.

The bar "database match only" in the alternative text of Figure 3.5 changed with it (entry 10).

File: `results/metrics/15_content_baselines.json`, with `notes/lab_notebook.md`.

Value found: `database_coverage_substitute`: `"description": "substitute for the degenerate baseline above: predict from
whether Prokka found a UniProtKB similarity hit"`, `"is_a_substitute": true`, `"feature": "prokka_has_similarity_hit"`,
`"rule": "predict disagreement when prokka_has_similarity_hit <= 0"`, and on the test rows `"mcc": 0.14134`. No Bakta
feature enters it. The baseline it stands in for, `is_either_product_hypothetical`: `"description": "specified baseline:
predict disagreement when either tool's product is a placeholder"`, `"computed": false`, `"reason": "Degenerate by
construction. The primary analysis set is defined as both tools having assigned a non-placeholder product, so this
predictor takes the value 0 on every row it would be scored on. ..."`. The notebook: "Reported as uncomputable rather
than swapped for something that produces a number; a substitute carrying the same intent [...] did Prokka find a
UniProtKB similarity hit [...] was added and labelled as a substitute."

## 12. "More computing power bought nothing here", left out

Before (Day 36 post): The fanciest model on that list did not win. The random forest did. More computing power bought
nothing here.

After (chapter): The most elaborate model on that list did not win; the random forest did (Figure 3.5).

Files: `results/metrics/16_content_cv_gradient_boosting.json` and `results/metrics/16_content_cv_random_forest.json`,
with `scripts/lib_content.py`.

Value found: the gradient boosting sweep took `"elapsed_seconds": 20.6` against the random forest's `"elapsed_seconds":
199.3`; the decision tree's took 60.1. Gradient boosting ran as `HistGradientBoostingClassifier`, chosen for
"computational tractability" (`lib_content.py`). The more elaborate model was the cheaper one to fit, so the record
contradicts the sentence. It was already absent from the chapter before this pass; the author's decision of 2 October
2026 keeps it out.

## 13. The seventeen DNA features and the thirty-five gene-caller features, described (a clarification)

Before: I ran the same random forest three times, with the same folds, the same random seed and everything else the
same. Only the columns it was allowed to see changed (Figure 3.6). With all 61 features, it scores 0.303 on MCC.

After: I ran the same random forest three times, with the same folds, the same random seed and the same way of choosing
its settings. Only the columns it was allowed to see changed (Figure 3.6). The seventeen columns that describe the raw
DNA include the GC content of the gene and of the hundred letters on either side, how repetitive the sequence is, how
often stop codons fall in its emptiest reading frame, and three properties of the whole genome. Thirty-five come from
the gene caller: the boundaries it chose, the reading frame and strand they imply, and everything computed from the
protein those boundaries translate into, such as its length and the share of each amino acid. The other nine describe
what each tool found in its databases.

With all 61 features, the forest scores 0.303 on MCC on the five held-out genomes.

Files: `results/metrics/14_content_features.json` and `results/metrics/19_content_circularity.json`.

Value found: `14_content_features.json`, `"counts": {"caller_derived": 35, "db_derived": 9, "neither": 17, ...}`. The
seventeen, the `sequence_only` arm of `19_content_circularity.json`, are `gc_content`, `gc_skew`, `at_skew`,
`gc_minus_genome`, `entropy_3mer`, `low_complexity_dna_frac`, `max_homopolymer`, `longest_orf_frac`, `min_stops_per_kb`,
`flank_gc_up`, `flank_gc_down`, `dist_to_contig_end`, `near_contig_edge`, `ambiguous_frac`, `genome_gc`,
`genome_length_bp` and `genome_n_contigs`, described among others as "GC of the 100 bp before the interval", "Shannon
entropy of 3-mer composition, bits; low in repetitive sequence" and "stop codons per kb in the emptiest of the 6
frames". The caller flag: "the value encodes a gene-caller decision: chosen boundaries, the reading frame they imply,
the strand. Everything computed from the translated protein is included, because there is no protein without a frame.";
its 35 include `length_bp`, `protein_length_aa` and the twenty `aa_frac_` features. The arms held `"folds, grid,
selection rule, seed"` identical (`held_identical_between_arms`), and the rule chose `"max_depth": 8` for the full and
no-caller arms and `"max_depth": 4` for the DNA-only arm, which is why "everything else the same" became "the same way
of choosing its settings".

## 14. What 0.142 and 0.070 measure

Before: That last number is generous. It was measured on genomes the model had seen in another role during training.
Held out properly, it drops to 0.070, which is close to nothing.

After: That last number is generous. A test on five genomes is small, and its score moves with which five genomes happen
to be in it. The steadier measure comes from the twenty training genomes: split them into five groups, hold each group
out in turn while the forest trains on the other four, and average the five scores. On that measure the DNA-only forest
scores 0.070, which is close to nothing.

Before (front matter summary): and with only DNA features on genomes held out properly it scored 0.070.

After: and with only DNA features it scored 0.142 on the same genomes and 0.070 in cross-validation on the twenty
training genomes.

Before (closing): Give the model only the features that describe the DNA, on genomes held out properly, and the score
falls to 0.070.

After: Give the model only the features that describe the DNA, and the score falls to 0.142 on the five held-out
genomes, and to 0.070 in cross-validation on the twenty training genomes.

Before (caption of Figure 3.6): The same random forest with fewer columns: 0.303 with all 61 features, 0.259 without the
gene-caller columns and 0.070 with DNA features alone. Three panels give the cost of shuffling a group of features: the
database features, the DNA features and, under the heading 0.019, the thirty-five gene-call features.

After: The same random forest with fewer columns, scored on the five held-out genomes: 0.303 with all 61 features, 0.259
without the gene-caller columns and 0.142 with DNA features alone. A separate mark gives 0.070, the DNA-only forest in
cross-validation on the twenty training genomes. Below, the cost of shuffling each group of features: 0.165 for the nine
database features, 0.019 for the thirty-five gene-call features and negative 0.001 for the seventeen DNA features.

After (the caption as it now stands, after the figure was drawn for the book as `figures/svg/fig-3-6.svg`): The same
random forest given fewer columns, scored on the five held-out genomes, on an axis from zero: 0.303 with all 61
features, 0.259 with the gene-caller features taken away and 0.142 with the database features taken away too, leaving
the 17 that describe the raw DNA. The second bar for DNA alone, 0.070, is the same forest in cross-validation on the
twenty training genomes.

The drawn figure has no panel for the cost of shuffling each group of features; 0.165, 0.019 and negative 0.001 are
given in the text. The alternative text of Figure 3.6 was rewritten to the same content, and again to describe the
drawn figure; its panel on thin evidence is entry 15.

Files: `results/metrics/19_content_circularity.json`, `results/metrics/15_content_baselines.json`,
`scripts/lib_content.py` and `notes/lab_notebook.md`, with `README.md`.

Value found: `19_content_circularity.json`, `side_by_side`: full `"grouped_cv_mean_mcc": 0.29259`, `"test_mcc":
0.30275`; no_caller `0.23228` and `0.25937`; sequence_only `"grouped_cv_mean_mcc": 0.07013`, `"test_mcc": 0.14191`, the
test on `"n_rows": 12283` from the five held-out genomes. `15_content_baselines.json`, `split`:
`"n_overlapping_genomes": 0`, `"assertion": "set(train_genomes) & set(test_genomes) == empty"`, `"result": "passed"`.
`lib_content.py`: "fold 0 of lib_split is the test set [...] The remaining 20 training genomes are dealt into five
cross-validation folds by the same deterministic GC-rank round-robin. No genome appears in both training and test, and
that is asserted rather than assumed." The notebook: "Note the sequence-only arm's CV/test gap (0.070 vs 0.142). The
grouped-CV number is the one to trust for generalisation; a five-genome test set moves." So 0.142 was measured on five
genomes kept out of training and out of the choice of settings, and 0.070 is the mean over five genome-grouped folds of
the twenty training genomes; neither was measured on genomes the model had seen. The README, under its figure of the
three arms: "The gap between the two bars in each pair is the difference between holding out genomes during selection
and holding them out entirely."

## 15. What the forest's top features mean, thin evidence to two effects that pull opposite ways

Before: So here is what the model actually learned. Two tools disagree on a name most often when neither database has
strong evidence for that region. One guesses, the other guesses differently, and the model is really detecting where the
evidence ran thin. That is a fact about two reference databases. It has nothing to do with the DNA sequence itself.

After: The obvious reading is that the names disagree where the evidence runs thin: neither database knows the protein
well, each tool guesses, and the guesses differ. I tested that rather than assuming it, and it holds only in part. It
fits the 4,494 regions where Bakta fell back on a domain name or an open reading frame name, which disagree almost every
time. Among the other 45,716, it holds on Prokka's side. Where Prokka assigned no enzyme number, the names disagree
54.0% of the time, against 42.1% where it did.

On Bakta's side it runs the other way. Where Bakta attached two cross-references or fewer, as it does about nine times
in ten, the names disagree 44.2% of the time. Where it attached three, they disagree 79.8% of the time, and at four or
more, 62.8%. A third cross-reference is usually an enzyme number or a match in a more specialised database, and it comes
with a more specific name from Bakta, which is then more likely to differ from Prokka's more general one. That is why
the number of cross-references Bakta attached is the forest's strongest feature: on Bakta's side, more evidence goes
with more disagreement. Either way, what the model learned is a fact about two reference databases and how each tool names
from them. It has nothing to do with the DNA sequence itself.

Before (closing): What carries the prediction is database coverage: how much evidence each tool's reference library
holds for that gene. Thin evidence produces a guess, and a different guess from each tool produces a mismatch.

After: What carries the prediction is what each tool found in its reference library. Where Prokka found less, the names
disagree more often. Where Bakta found more, it gives a more specific name, which is more likely to differ from
Prokka's.

Before (front matter summary, in part): but its signal came from database coverage

After: but its signal came from what each tool found in its reference databases

Before (alternative text of Figure 3.6, in part): and that two tools disagree most where neither database has strong
evidence. A panel headed 0.019 notes reliance on enzyme numbers and protein motifs.

After: the panel on thin evidence is gone, and 0.019 is given as the cost of shuffling the gene-call features (entry
14). The drawn figure, `figures/svg/fig-3-6.svg`, and its alternative text have no panel on evidence and give no
shuffling cost at all (entry 14).

File: `results/metrics/22_content_mechanism.json`, with `scripts/22_content_mechanism.py`, `notes/lab_notebook.md` and
`README.md`.

Value found: `"question": "Is the naming disagreement explained by thin reference-database evidence? Tested rather than
asserted."` Within the 45,716 remainder regions, `prokka_evidence_depth_remainder_only.by_ec`: `"with_ec": {"n": 26861,
..., "rate": 0.4209}` and `"without_ec": {"n": 18855, ..., "rate": 0.5399}`.
`bakta_evidence_depth_remainder_only.buckets`: `"2_the_minimum": {"n": 41308, ..., "rate": 0.4419}`, `"3": {"n": 2724,
..., "rate": 0.7981}`, `"4_or_more": {"n": 1684, ..., "rate": 0.6277}`. The script fills the first bucket with every
region where `n_dbxref <= 2`, which takes in 123 regions with a single cross-reference, hence "two or fewer"; 41,308 of
45,716 is 90.4%, and the file's own note says "the remainder carries three or more about one time in ten". The finding:
"Disagreement RISES with Bakta cross-reference count, from 44.2% at the minimum two to 79.8% at three. This is the
opposite of the thin-evidence chain. A third cross-reference is typically an EC number, a BlastRules hit, a
virulence-factor or insertion-sequence match, and it comes with a MORE specific Bakta name". The fallback families:
`"families": {"n": 4494, "n_disagree": 4491, "rate": 0.9993}`. The conclusion: "The chain holds for the fallback-naming
families and on Prokka's side, and reverses on Bakta's. There are two mechanisms pulling in opposite directions, not
one. bakta_n_dbxref is the forest's strongest feature because extra Bakta evidence predicts a more specific Bakta name
that Prokka does not match". The notebook: "It is cheap to test, so I tested it (`22_content_mechanism.json`) rather
than writing it up as a mechanism."

## 16. Bakta's database, and what the 12.5% and 40.2% measure

Before: I predicted that a smaller reference database would make one tool name fewer genes. I had it backwards. That
tool missed 12.5%. The other missed 40.2%.

After: Bakta ran on db-light, the smaller of its two reference databases, because the full one would not fit on my
machine. I predicted that the smaller database would leave Bakta naming fewer genes than Prokka. I had it backwards. Of
the 87,859 regions both tools called, Bakta left 12.5% with a placeholder such as hypothetical protein instead of a
name. Prokka left 40.2%.

Files: `README.md`, `notes/lab_notebook.md`, `results/metrics/02_annotation_versions.json`,
`results/metrics/12_content_cohort.json` and `results/metrics/13_name_rules.json`.

Value found: the README: "Bakta ran against **db-light**, not db-full: this machine had ~13 GB free and db-full does not
fit." and "Bakta on db-light leaves 12.5% of paired CDS as a placeholder against Prokka's 40.2%."
`02_annotation_versions.json`: `"db_type": "light"`, `"db_type_reason": "db-full does not fit in available disk on this
machine. db-light has fewer reference proteins, so some CDS that db-full would name are left hypothetical. ..."`. The
notebook: "The brief expected db-light to leave Bakta under-named relative to Prokka." `13_name_rules.json`,
`placeholder_rule.totals`: `"bakta_placeholder": 10950`, `"prokka_placeholder": 35352`, `"n_pairs": 87859`; 10,950 of
87,859 is 12.5% and 35,352 of 87,859 is 40.2%. The commonest placeholder is `"hypothetical protein"` (Bakta 10,930,
Prokka 34,776). `12_content_cohort.json` gives the same split by cell: `"both_placeholder": 8653`, `"prokka_named_only":
2297`, `"bakta_named_only": 26699`.

## 17. The size of the forest, a hundred trees to three hundred

Before (Why a random forest): A forest gives that up. A hundred trees will score higher than one, and I will not be
able to read any of them.

After: A forest gives that up. Three hundred trees will score higher than one, and I will not be able to read any of
them.

Files: `scripts/lib_model.py`, `scripts/lib_content.py`, `results/metrics/08_forest.json` and
`results/metrics/10_circularity_audit.json`, with `results/metrics/17_content_final_random_forest.json` and
`results/metrics/17_content_final_decision_tree.json`.

Value found: `lib_model.py`, `N_ESTIMATORS = 300` (line 26), passed as `n_estimators=N_ESTIMATORS` to the forest of the
first experiment; `lib_content.py`, `N_ESTIMATORS_FOREST = 300` (line 90), passed as `n_estimators=N_ESTIMATORS_FOREST`
by `build` to every forest of the naming experiment, the three of Figure 3.6 among them. `08_forest.json` and
`10_circularity_audit.json` record `"n_estimators": 300`. Each constant has been 300 since its file was first written,
at `3ed14c64febb` and `4c70e4515407` respectively. The Day 26 post that gave a hundred appeared on 18 August, before
either file was committed. The sentence's claim holds for the forest that ran: on the same 12,283 held-out regions it
scored an MCC of `0.30275` against the single tree's `0.26059`.

## 18. The 50,210 named regions, identical to the same

Before (Half the names): These are identical regions, with both tools confident enough to write a name, and the names
do not match.

After: These are the same regions, with both tools confident enough to write a name, and the names do not match.

Files: `scripts/12_content_cohort.py` and `results/metrics/14_content_features.json`, with
`scripts/14_content_features.py` and `results/metrics/12_content_cohort.json`.

Value found: `12_content_cohort.py` pairs each Bakta call with the same-strand Prokka CDS that overlaps it most and
records `"same_start": int(partner["start"] == c["start"])` and `"same_stop": int(partner["end"] == c["end"])`.
`14_content_features.json`, under `constant_feature_check.near_constant`, gives `same_start` the value 1 in a share of
`0.99932` and `same_stop` in a share of `0.99938`, and `14_content_features.py` takes those shares over the rows of the
primary set, the 50,210 regions both tools named. So 34 of the 50,210 differ in their start and 31 in their stop.
Across all 87,859 pairs, `12_content_cohort.json` gives `"identical_start_and_stop": 87788`. The 50,210 are the same
loci in both tools, almost always to the base, but not all of them are identical.

## 19. The 87,960 calls in the closing, the two tools' to Bakta's

Before (Fact or call): Where does a gene start? Two tools called 87,960 genes and disagreed about only 72 of them.

After: Where does a gene start? Bakta called 87,960 genes, and the two tools disagreed about only 72 of them.

Files: `results/metrics/05_disagreement.json` and `results/metrics/04_calls.json`.

Value found: `05_disagreement.json`, `"unit": "one Bakta CDS call"`, `"n_rows": 87960` and `"n_positive": 72`;
`04_calls.json`, `totals`: Bakta `"cds": 87960`, Prokka `"cds": 87860`. The 87,960 are Bakta's calls alone, as the
summary and the section Seventy-two rows already say. The reverse direction, which is not the label, is recorded per
genome as `"unique_to_prokka"`: 11 Prokka calls in all have nothing from Bakta overlapping them on their strand, and
they are not among the 87,960.

## 20. Who read the genome again in 2007

Before: In 2007 another team read the same genome and reported fewer.

After: In 2007, a team that included two of the original authors went back to the same genome and reported fewer.

Sources: Parkhill, Wren and others (2000), Nature 403:665-668, https://doi.org/10.1038/35001088; Gundogdu, Bentley,
Holden, Parkhill, Dorrell and Wren (2007), BMC Genomics 8:162, https://doi.org/10.1186/1471-2164-8-162.

Value found: Parkhill and Wren, the first two authors of the 2000 paper, are two of the six authors of the 2007
re-annotation, so "another team" was not accurate. The 2007 paper reports "In total, 11 CDSs were removed", and 1,654
less 11 is the 1,643 the chapter gives.

## 21. What else Prokka can call on the same strand

Before: If Prokka called a transfer RNA on the same strand where Bakta called a protein-coding gene, Prokka did not
leave the region empty.

After: If Prokka called a transfer RNA, or anything else that is not a protein-coding gene, on the same strand where
Bakta called a protein-coding gene, Prokka did not leave the region empty.

Files: `results/metrics/05_disagreement.json` and `results/metrics/04_calls.json` at 4f797c3fa09d.

Value found: `05_disagreement.json` records `"non_cds": 29`, the Bakta calls matched by a Prokka feature that is not a
coding sequence, without saying which kind; the kinds `04_calls.json` lists for Prokka besides coding sequences are
tRNA, rRNA, tmRNA and repeat_region. The sentence gave a transfer RNA as its only case, so a reader could take all 29 to
be transfer RNAs. It now says the rule covers any such feature and keeps the transfer RNA as the example.

## 22. How nhmmer failed

Before: So nhmmer failed at runtime, every time, silently.

After: So nhmmer failed at runtime, every time.

Before (Figure 3.3 caption): ... nhmmer had been compiled against a different version of a maths library from the one
shipped, failed every time without raising an error, and nothing came back up the chain.

After: ... nhmmer had been compiled against a different version of a maths library from the one shipped and failed every
time, and no error came back up the chain.

Files: `notes/lab_notebook.md` and `scripts/lib_env.sh` at 4f797c3fa09d.

Value found: the notebook: "Prokka's cached env ships `libgsl.so.27`, but the `nhmmer` binary in it was linked against
`libgsl.so.25`. `barrnap` shells out to `nhmmer`, so rRNA detection failed at runtime while Prokka reported `Found 0
rRNAs` and finished successfully." `lib_env.sh` says the same, with Prokka "still exiting 0". A program whose shared
library is missing is stopped by the system loader, which reports the missing library; the record does not say whether
barrnap passed that report on. The silence the record shows is Prokka's, not nhmmer's, so the chapter now says only that
nhmmer failed and that no error came back.

## 23. The 2007 re-annotation and the 1,731-spot array

Before: The same 1,641,481 letters were read again with better software.

After: The same 1,641,481 letters were read again, gene by gene, by curators.

Before: Somebody printed a microarray with 1,731 spots on it, one spot for every gene in the genome: real glass, real
DNA, an experiment you could run. By the time the genome paper was published, 77 of those spots represented nothing. The
count had been revised down to 1,654 before print, and the slides were already made. The 77 spots stayed on the glass,
and the software that read the array flagged each one as not an annotated gene. Seven years later the count went to
1,643. From 1,731 to 1,654 to 1,643 is eighty-eight genes withdrawn.

After: Somebody printed a microarray with 1,731 spots on it, one for every gene first identified in the genome: real
glass, real DNA, an experiment you could run. By the time the genome paper was published, 77 of those spots stood for
genes that were no longer in the annotation. The count had been revised down to 1,654, and the array had been built from
the longer list. The 77 spots stayed on the glass, and the gene lists in the analysis software flagged each one as a
"not annotated gene". Seven years later the count went to 1,643. From 1,731 to 1,654 to 1,643 is eighty-eight fewer
genes in the list.

Figure 3.1 changes to match: the first bar's label "printed before the paper" became "in the first list", the labels "77
withdrawn" and "88 withdrawn" became "77 fewer" and "88 fewer", and the alt text and caption follow.

Sources: Dorrell, Mangan, Laing, Hinds, Linton, Al-Ghusein, Barrell, Parkhill, Stoker, Karlyshev, Butcher and Wren
(2001), Whole genome comparison of Campylobacter jejuni human isolates using a low-cost microarray reveals extensive
genetic diversity, Genome Research 11(10):1706-1715, https://doi.org/10.1101/gr.185801, Results, first subsection;
Gundogdu, Bentley, Holden, Parkhill, Dorrell and Wren (2007), BMC Genomics 8:162,
https://doi.org/10.1186/1471-2164-8-162, Methods and Results (Gene number adjustment, Table 1).

Value found: Dorrell and others: "A whole genome DNA microarray was constructed containing an element representing each
of the 1731 CDSs originally identified from the genome sequence (J. Parkhill, unpubl.). The number of annotated CDSs in
the C. jejuni NCTC 11168 genome was subsequently reduced to 1654 (Parkhill et al. 2000). The resulting 77 "nongenes" are
therefore each flagged in the gene lists used in the analysis software as a "not annotated gene"." The spots carried DNA
from the genome, so they did not represent nothing, and the paper does not say when the slides were printed relative to
the genome paper. Gundogdu and others describe a manual re-annotation: "Manual re-annotation of all previously annotated
C. jejuni NCTC11168 CDSs was carried out based on results from BLASTP and FASTA sequence comparisons", and the 11 fewer
coding sequences came from "the merging of adjacent CDSs or the removal of CDSs" (ten merges and one removal in Table
1), so neither "better software" nor "withdrawn" described what happened. 1,731, 1,654, 77, 1,643 and 1,641,481 are
unchanged (the last confirmed against GenBank AL111168.1 and RefSeq NC_002163.1, both still at version 1).
