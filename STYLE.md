# Editorial guide

This book is rewritten from the daily series Machine Learning for Biology (24 July to 1 October 2026). The posts are in
`sources/`. A chapter is the posts of that chapter turned into one continuous piece of prose. It is not a list of days.

## Voice

Write as the author wrote the posts.

- First person singular. "I took 3,984 genomes from NCBI." Never "we" for the author alone.
- No contractions: "did not", "it is". The posts never use them.
- Mostly short declarative sentences, with longer ones where an explanation needs room. A fragment is allowed now and
  then for weight, as the posts do ("One target, and no backup."), but no more than one or two per section.
- Plain words. Say what was done and what was found. Keep the honesty about failure; it is the book's character.
- British spelling: analyse, behaviour, colour, labelled, modelling, tumour, haemagglutinin, centre, per cent in prose
  (write "%" after a figure, as the posts do: "99.67%").

## What to remove from the posts

- Day framing: "Yesterday I said", "Tomorrow:", "Today I put it to the test", "Day 4", "this series".
- Social framing: hooks written to stop a scroll, calls to action ("Tell me in the comments"), hashtags, link
  placeholders, sign-offs.
- Repetition that only existed because each post had to stand alone. Say a thing once, in the right place.

## What never to do

- Never add a fact, number, date, name or result that is not in the sources for that chapter. If a number appears in
  the posts, copy it exactly. If something is unclear in the posts, leave it out rather than guess.
- Never invent a citation. Name a published work only if the posts name it; give full bibliographic details only if you
  have verified them with a search tool, and otherwise cite it as the posts do ("Jesse and colleagues, 2006").
- No em dashes and no en dashes as punctuation. No emojis. No exclamation marks.
- Avoid the patterns catalogued in Wikipedia: Signs of AI writing. In particular:
  - inflated significance ("pivotal", "crucial", "a testament to", "underscores", "highlights the importance",
    "plays a key role", "marks a shift", "evolving landscape");
  - the vocabulary "delve", "intricate", "tapestry", "robust" (except as a technical term), "showcase", "foster",
    "enhance", "meticulous", "seamless", "valuable insights", "align with", "additionally" at the start of a sentence;
  - negative parallelisms used as a formula ("not just X, but Y", "it is not X, it is Y" more than once a chapter);
  - lists of three by reflex; tidy summaries at the end of sections ("In summary", "Overall", "In conclusion");
  - vague attributions ("experts say", "studies show") and promotional adjectives.
- No bold in running text except the labels inside rules boxes and notes. Headings in sentence case.

## Corrections from the repository

The posts are the source of the text, but each chapter's repository at its pinned commit is the record of the
analysis. Where a number in the posts disagrees with that record, and the record settles it without interpretation (an
arithmetic slip, one count transposed with another, a value copied from the wrong file), the book uses the record's
value. Each such correction is written to `sources/corrections/chN.md` with the chapter's sentence before and after,
the repository file and commit, and the value found there, so that anyone can check the change. Where the posts and the
record disagree about something that needs interpretation (which model produced a number, whether a rule was fixed in
advance, how a result should be described), the book keeps the posts' account and the question goes to the author.

## When the record and the posts disagree (the author's decision, 2 October 2026)

The author has asked for the book to be correct before anything else. Where a chapter's repository at its pinned commit
records what was actually done, and the posts say otherwise (which model ran, which rule the code applied, what was
fixed in advance and when, which set a number was measured on), the book follows the record. The passage is rewritten
in the author's voice, says plainly what was done, and keeps the lesson where the lesson still holds; it does not
describe the posts or the correction itself. Each such change is logged in `sources/corrections/chN.md` like a
corrected number, with the file and commit that settle it. Where the record is silent, the book keeps the posts'
account but never states as fact something the record contradicts. Published corrections in the author's own later
posts (kept verbatim in a chapter's repository under `posts/`) count as sources.

## Drawn figures

Every figure is drawn for the book as an SVG file, `figures/svg/fig-N-M.svg`, and the build places it in the page.

- Root: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 H" class="figsvg">`, 640 wide, height as needed (keep
  it under about 560). No `<style>`, no `id` attributes, no scripts, no embedded images, no masthead or title text
  inside the figure: the caption carries the title.
- Colour only through classes, never a fill or stroke colour written into the file: fills `fi` (ink), `fm` (muted),
  `fl` (rule line), `fa` (accent), `fa2` (second accent), `fb` (wrong or failed), `fp` (panel), `fbg` (page), `fn` (none);
  strokes `si`, `sm`, `sl`, `sa`, `sa2`, `sb`. Every shape and every text element carries a class, directly or from a
  parent `<g>`. The classes resolve to the light or dark palette, so a figure works on both.
- Type: text in the book's serif by default, numbers with class `num` (monospace). No text smaller than 22 units, key
  numbers 24 or more, so that the smallest text is about 12 px on a 358 px phone column. At most a dozen labels.
- Content: only what the chapter's text, its sources or its corrections log state. Axes start at zero unless the axis is
  clearly marked otherwise. British spelling, no em or en dashes, no day or series framing.
- Simple forms: bars, dots, small tables, boxes and arrows. A figure shows one idea.
- Check every figure with `node tools/render_figures.mjs <out_dir> figures/svg/fig-N-M.svg` and look at all four renders
  (light and dark, desktop and phone). `tools/figure_reference.svg` shows the conventions.

## Chapter anatomy

Use the series' own method as the structure, but only where the chapter's posts support each part. Headings are short
and plain, in sentence case, and describe what the section does. The build numbers them (1.1, 1.2 and so on); do not
number them yourself. A typical chapter:

1. An opening with no heading: the biological problem in concrete terms, and the question the chapter asks.
2. Why this model, and what it does, explained so that a biologist new to machine learning can follow.
3. The rules, fixed before running anything, set in a rules box. Include the rules that were changed after looking, and
   why, if the posts record them.
4. The ways the chapter could be wrong, as the posts stated them in advance, where they did.
5. What happened: every result against its baseline.
6. What went wrong, or what the result does and does not show.
7. A closing paragraph that hands on to the next chapter, using the recap posts where they help.

After the closing paragraph, end with the provenance line exactly in this form:

    <p class="prov">This chapter is rewritten from the posts for Days 2 to 11 of the series.</p>

Then a `## References` section only if the chapter cites published work.

Length: as long as the material needs, usually 3,000 to 4,500 words for a chapter with ten or more posts, less for the
shorter chapters. Do not pad.

## Format

Each chapter file starts with front matter:

    ---
    chapter: 1
    title: Predicting antibiotic resistance from a genome
    model: Logistic regression
    question: If resistance is written in the genome, why can nobody simply read it off?
    summary: Three or four sentences, the chapter's abstract, with its central numbers.
    repository: Qasim-Hussain-Code/campylobacter_amr_phenotype_prediction
    commit: 0e2b3df4c587
    ---

Sections are `## Heading`. Inside the body, use these blocks exactly (blank line before and after each):

Rules box:

    <div class="rules" markdown="1">
    **Fixed before any modelling.** Call an isolate resistant if *gyrA* carries any substitution at position 86.

    **Changed after looking.** The same rule without alanine at position 86, justified by a separate assay.
    </div>

Note (a definition or aside that sits beside the text):

    <aside class="note" markdown="1">**Minimum inhibitory concentration (MIC).** The lowest concentration of a drug that
    stops visible growth.</aside>

Figure (the series' infographics are in `figures/web/`, named by day; use only those that belong to the chapter's days,
and describe in the caption only what the image shows):

    <figure class="fig" id="fig-1-1"><img src="figures/web/day-03.jpeg" alt="Plain description of what the image shows.">
    <figcaption><b>Figure 1.1</b> Caption in one or two sentences.</figcaption></figure>

Refer to figures in the text as "Figure 1.1". Number figures in order within the chapter.

Code listing (optional, at most two per chapter, each at most 25 lines, quoted verbatim from the chapter's repository at
its pinned commit; fetch it read-only with `gh api repos/<repository>/contents/<path>?ref=<commit>`):

    <p class="lst-cap"><b>Listing 1.1</b> What it does, from <code>scripts/07_split_data.py</code>.</p>

    ```python
    ...verbatim lines...
    ```

Italicise species and gene names: *Campylobacter jejuni*, *gyrA*.
