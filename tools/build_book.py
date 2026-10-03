"""Build the web edition of Machine Learning for Biology into docs/ (static HTML, ready for GitHub Pages).
Design: study 29 (Navy night, STIX Two) with the sky accent, dark by default with a light mode toggle.
usage: python tools/build_book.py"""
import html, os, re, shutil
import markdown, yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'docs')
BOOK = 'Machine Learning for Biology'
AUTHOR = 'Qasim Hussain'
EPIGRAPH = 'We’ve essentially found a way to make sand think. It’s miraculous.'
EPI_WHO = 'Demis Hassabis'
EPI_ROLE = ('Nobel Laureate · Co-Founder and Chair, Google DeepMind · Chief Scientist, Alphabet · '
            'Founder and CEO, Isomorphic Labs')
EPI_SRC = '“A Framework for Frontier AI and the Dawning of a New Age”, 14 July 2026'

# reading order: (file stem, page name, part)
ORDER = [('preface', 'preface', None)] + \
        [(f'ch{n:02d}', f'chapter-{n}', 'I' if n < 7 else 'II') for n in range(1, 8)] + [('epilogue', 'epilogue', None)]
PARTS = {'I': 'Part I · Learning from labels', 'II': 'Part II · Learning without labels'}

FONTS = ('https://fonts.googleapis.com/css2?family=STIX+Two+Text:ital,wght@0,400..700;1,400'
         '&family=IBM+Plex+Mono:wght@400;500;600&display=swap')


def front_matter(block):
    """Read 'key: value' lines. Tolerant of colons inside values and of YAML block scalars (> or |)."""
    try:
        meta = yaml.safe_load(block)
        if isinstance(meta, dict):
            return meta
    except yaml.YAMLError:
        pass
    meta, key, buf = {}, None, []
    for line in block.splitlines():
        m = re.match(r'^([A-Za-z_][\w-]*):\s?(.*)$', line)
        if m and not line.startswith(' '):
            if key is not None:
                meta[key] = ' '.join(buf).strip()
            key, first = m.group(1), m.group(2).strip()
            buf = [] if first in ('>', '|', '>-', '|-') else [first]
        elif key is not None:
            buf.append(line.strip())
    if key is not None:
        meta[key] = ' '.join(buf).strip()
    for k, v in meta.items():
        if isinstance(v, str) and len(v) > 1 and v[0] == v[-1] and v[0] in '"\'':
            meta[k] = v[1:-1]
        if isinstance(v, str) and v.isdigit():
            meta[k] = int(v)
    return meta


def load(stem):
    path = os.path.join(ROOT, 'chapters', f'{stem}.md')
    if not os.path.exists(path):
        return None
    text = open(path, encoding='utf-8').read().replace('\r\n', '\n')
    m = re.match(r'^---\n(.*?)\n---\n', text, re.S)
    meta = front_matter(m.group(1)) if m else {}
    return meta or {}, text[m.end():] if m else text


NBSP = ' '
ALLELE = re.compile(r'\b((?:HLA|Mamu|Eqca|BoLA|Gaga)-[A-Za-z0-9]+\*\d{2,4}:\d{2}(?: [A-Z]\d+[A-Z]\b)?)')


def polish_text(segment):
    """Typography for running text (never applied inside tags, code or pre): keep a label and its number together,
    keep allele names on one line, and make DOIs links."""
    segment = re.sub(r'\b(Figure|Listing|Table|Chapter|Chapters|Part|Day|Days)\s+(?=[0-9IVX])', lambda m: m.group(1) + NBSP, segment)
    segment = ALLELE.sub(r'<span class="nw">\1</span>', segment)
    segment = re.sub(r'(https://doi\.org/[^\s<]+[^\s<.,;)])', r'<a href="\1">\1</a>', segment)
    return segment


BLOCK_TAGS = {'p', 'figcaption', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div', 'blockquote', 'td', 'th', 'section',
              'header', 'aside', 'summary', 'details', 'br', 'figure', 'nav', 'footer', 'main', 'ol', 'ul', 'table'}


def curl(text, prev=' '):
    """Curl the straight quotes left in running text. Smarty curls Markdown text but not raw HTML blocks such as figure
    captions, nor fields rendered outside Markdown. prev is the character before text, so a quote that starts a segment
    after an inline tag is read in context: "<i>word</i>" gets an opening and a closing mark."""
    out = []
    for i, ch in enumerate(text):
        before = out[-1] if out else prev
        if ch == '"':
            out.append('\u201c' if before.isspace() or before in '([{\u2018\u201c/' else '\u201d')
        elif ch == "'":
            after = text[i + 1] if i + 1 < len(text) else ''
            if before.isalnum() or before in '.,;:?)]}\u2019\u201d' or after.isdigit():
                out.append('\u2019')
            else:
                out.append('\u2018')
        else:
            out.append(ch)
    return ''.join(out)


def polish(body):
    out, depth, prev = [], 0, ' '
    for part in re.split(r'(<[^>]+>)', body):
        if part.startswith('<'):
            tag = re.match(r'</?\s*([a-zA-Z0-9]+)', part)
            name = tag.group(1).lower() if tag else ''
            if name in ('pre', 'code', 'a', 'svg'):
                depth += -1 if part.startswith('</') else 1
            if name in BLOCK_TAGS:
                prev = ' '
            out.append(part)
        else:
            out.append(part if depth > 0 else polish_text(curl(part, prev)))
            if part:
                prev = part[-1]
    return ''.join(out)


def sections(md_text, chapter):
    """(number, title, slug) for each numbered section, as render_body numbers them."""
    out, k = [], 0
    for m in re.finditer(r'^## (.+)$', md_text, re.M):
        title = m.group(1).strip()
        plain = re.sub(r'[*_`]', '', title)
        slug = re.sub(r'[^a-z0-9]+', '-', plain.lower()).strip('-')
        if plain.lower() == 'references' or not chapter:
            continue
        k += 1
        out.append((f'{chapter}.{k}', plain, slug))
    return out


INLINE_SVG = True  # the EPUB build sets this to False and ships the drawn figures as image files


def svg_figure(m):
    """A drawn figure, figures/svg/*.svg, placed in the page so that its colour classes follow the theme."""
    src, alt = m.group(1), m.group(2)
    svg = open(os.path.join(ROOT, src), encoding='utf-8').read()
    svg = re.sub(r'<\?xml[^>]*\?>\s*', '', svg).strip()
    if not re.match(r'<svg\b[^>]*\bclass="[^"]*figsvg', svg):
        svg = re.sub(r'<svg\b', '<svg class="figsvg"', svg, count=1)
    return re.sub(r'<svg\b', f'<svg role="img" aria-label="{alt}"', svg, count=1)


def render_body(md_text, chapter):
    body = markdown.markdown(md_text, extensions=['extra', 'sane_lists', 'smarty'], output_format='html5')
    if INLINE_SVG:
        body = re.sub(r'<img src="(figures/svg/[^"]+\.svg)" alt="([^"]*)"\s*/?>', svg_figure, body)
    k = 0

    def heading(m):
        nonlocal k
        title = m.group(1)
        plain = re.sub(r'<[^>]+>', '', title)
        slug = re.sub(r'[^a-z0-9]+', '-', html.unescape(plain).lower()).strip('-')
        if plain.strip().lower() == 'references' or not chapter:
            return f'<h2 id="{slug}">{title}</h2>'
        k += 1
        return f'<h2 id="{slug}"><span class="secno">{chapter}.{k}</span> {title}</h2>'
    body = re.sub(r'<h2>(.*?)</h2>', heading, body)
    body = re.sub(r'<div class="rules">', '<div class="rules"><p class="rh">Rules for this chapter</p>', body)
    body = re.sub(r'(<figure class="fig"[^>]*>)\s*(<img src="([^"]+)"[^>]*>)',
                  r'\1<a class="figlink" href="\3" title="Open the full-size image">\2</a>', body)
    body = body.replace('<pre>', '<pre tabindex="0">')
    return polish(body)


def toc(current, secs=None):
    items, part = [], None
    for stem, page, p in ORDER:
        got = load(stem)
        if not got:
            continue
        meta = got[0]
        if p and p != part:
            items.append(f'<li class="part">{PARTS[p]}</li>')
            part = p
        label = meta.get('title', stem.title())
        num = f'<span class="n">{meta["chapter"]}</span> ' if meta.get('chapter') else ''
        model = f'<span class="m">{html.escape(meta["model"])}</span>' if meta.get('model') else ''
        on = page == current
        sub = ''
        if on and secs:
            sub = '<ol class="secs">' + ''.join(
                f'<li><a href="#{slug}"><span class="sn">{sn}</span>{html.escape(title)}</a></li>' for sn, title, slug in secs) + '</ol>'
        li_cls = ' class="on"' if on else ''
        aria = ' aria-current="page"' if on else ''
        items.append(f'<li{li_cls}><a href="{page}.html"{aria}>{num}{html.escape(label)}{model}</a>{sub}</li>')
    return ('<nav class="toc" aria-label="Contents"><details class="tocd" open><summary class="toch">Contents</summary>'
            f'<ol>{"".join(items)}</ol><p class="tohome"><a href="index.html">Title page and contents</a></p></details></nav>')


def shell(title, current, main, prev=None, nxt=None, secs=None):
    pn = ''
    if prev or nxt:
        pn = '<nav class="pn" aria-label="Previous and next">' + \
             (f'<a class="prev" href="{prev[0]}.html"><span>Previous</span>{html.escape(prev[1])}</a>' if prev else '<span></span>') + \
             (f'<a class="next" href="{nxt[0]}.html"><span>Next</span>{html.escape(nxt[1])}</a>' if nxt else '') + '</nav>'
    return f'''<!doctype html><html lang="en-GB" data-theme="dark"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{BOOK}, a book by {AUTHOR}.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONTS}" rel="stylesheet"><link rel="stylesheet" href="assets/book.css">
<script>(function(){{var r=document.documentElement;try{{var s=localStorage.getItem('mlb-theme');if(s)r.dataset.theme=s;}}catch(e){{}}}})();</script>
</head><body class="lay-sidebar hs-smallcaps justify">
<a class="skip" href="#main">Skip to the text</a>
<header class="topbar"><a class="tb-title" href="index.html">{BOOK}</a>
<div class="tb-right">{editions()}<button class="modebtn" type="button" aria-label="Switch to light mode">Light<span class="wide"> mode</span></button></div></header>
<div class="frame">{toc(current, secs)}<main class="col" id="main">{main}{pn}</main></div>
<script src="assets/book.js"></script></body></html>'''


def collapse_listings(body):
    """On the web, each code listing folds away under its caption and opens on a click. (The print edition keeps them open.)"""
    pat = re.compile(r'<p class="lst-cap">(.*?)</p>\s*(<pre tabindex="0">.*?</pre>)', re.S)
    return pat.sub(lambda m: f'<details class="lst"><summary class="lst-cap"><span class="lt">{m.group(1)}</span></summary>'
                             f'{m.group(2)}</details>', body)


def notes_first(body):
    """On the web a note floats into the right margin from where it stands, so it is moved ahead of the paragraph it
    glosses and starts level with it. (The print edition keeps the notes after their paragraphs.)"""
    return re.sub(r'(<p>(?:(?!</p>).)*</p>)\s*(<aside class="note">.*?</aside>)', r'\2\n\1', body, flags=re.S)


def chapter_page(i, stem, page):
    meta, md_text = load(stem)
    n = meta.get('chapter')
    body = notes_first(collapse_listings(render_body(md_text, n)))
    if n:
        part = PARTS['I' if n < 7 else 'II']
        head = f'''<header class="opener op-smallcaps"><p class="op-kicker">Chapter {n} · {part}</p>
<h1 class="op-title">{html.escape(meta["title"])}</h1><p class="op-model">Model: {html.escape(str(meta.get("model", "")))}</p>
{f'<p class="op-question">{html.escape(curl(meta["question"]))}</p>' if meta.get("question") else ''}</header>'''
    else:
        head = f'<header class="opener op-smallcaps"><h1 class="op-title">{html.escape(meta.get("title", stem.title()))}</h1></header>'
    summ = f'<section class="summary"><p class="sk">Summary</p><p>{polish(markdown.markdown(str(meta["summary"]), extensions=["smarty"])[3:-4])}</p></section>' \
        if meta.get('summary') and n else ''
    end = ''
    if meta.get('repository'):
        repo = meta['repository']
        end = f'''<section class="endm"><div class="run"><p class="eh">Run it</p>
<p><span class="lbl">Repository</span> <a href="https://github.com/{repo}">{repo.split("/")[1]}</a></p>
<p><span class="lbl">Commit</span> <a href="https://github.com/{repo}/tree/{meta.get("commit", "")}"><code>{meta.get("commit", "")}</code></a></p></div>
<div class="cite"><p class="eh">Cite this chapter</p><p>{cite(meta["title"], n)}</p></div></section>'''
    present = [(p, (load(s) or [{}])[0]) for s, p, _ in ORDER if load(s)]
    idx = [p for p, _ in present].index(page)
    lab = lambda j: (present[j][0], (f'Chapter {present[j][1]["chapter"]}: ' if present[j][1].get('chapter') else '') + present[j][1].get('title', present[j][0].title()))
    prev = lab(idx - 1) if idx > 0 else ('index', 'Title page')
    nxt = lab(idx + 1) if idx + 1 < len(present) else None
    title = f'{meta.get("title", stem.title())} · {BOOK}'
    return shell(title, page, head + summ + f'<div class="bodywrap">{body}</div>' + end, prev, nxt, sections(md_text, n))


def cite(title, n):
    """Hussain, Q. (2026). Title. In Machine Learning for Biology, chapter n. No second stop after a title ending in ? or !"""
    stop = '' if title.rstrip()[-1:] in ('?', '!', '.') else '.'
    return f'{AUTHOR.split()[1]}, {AUTHOR.split()[0][0]}. (2026). {html.escape(title)}{stop} In <i>{BOOK}</i>, chapter {n}.'


def editions():
    """Links to the PDF and EPUB editions for the top bar, each shown once its build (tools/print_book.py,
    tools/epub_book.py) has made the file."""
    links = []
    for ext, label, what in (('pdf', 'PDF', 'the print edition, PDF'), ('epub', 'EPUB', 'the e-book edition, EPUB')):
        path = os.path.join(OUT, f'machine-learning-for-biology.{ext}')
        if os.path.exists(path):
            size = f'{os.path.getsize(path) / 1e6:.0f} MB'
            dl = ' download' if ext == 'epub' else ''
            links.append(f'<a class="tb-ed" href="machine-learning-for-biology.{ext}"{dl} '
                         f'aria-label="Download {what} ({size})" title="Download {what} ({size})">{label}</a>')
    return ''.join(links)


def title_page():
    contents = []
    part = None
    for stem, page, p in ORDER:
        got = load(stem)
        if not got:
            continue
        meta = got[0]
        if p and p != part:
            contents.append(f'<li class="part">{PARTS[p]}</li>')
            part = p
        num = f'<span class="n">{meta["chapter"]}</span>' if meta.get('chapter') else '<span class="n"></span>'
        model = f'<span class="m">{html.escape(meta["model"])}</span>' if meta.get('model') else ''
        contents.append(f'<li><a href="{page}.html">{num}<span class="t">{html.escape(meta.get("title", stem.title()))}</span>{model}</a></li>')
    first = next(p for s, p, _ in ORDER if load(s))
    main = f'''<section class="titlepage"><h1 class="tp-title">{BOOK}</h1>
<figure class="epigraph"><blockquote>{EPIGRAPH}</blockquote><figcaption><span class="who">{EPI_WHO}</span>
<span class="role">{EPI_ROLE}</span><span class="src">{EPI_SRC}</span></figcaption></figure>
<p class="tp-author">{AUTHOR}</p><p class="tp-beta"><b>Beta edition.</b> This book will be revised, corrected and extended continuously for some time yet. Suggestions for its improvement are most welcome, through an <a href="https://github.com/Qasim-Hussain-Code/machine-learning-for-biology/issues">issue on its repository</a> or a message on <a href="https://www.linkedin.com/in/qasim--hussain">LinkedIn</a>.</p></section><hr class="tpbreak">
<section class="contents"><h2 class="ch">Contents</h2><ol>{"".join(contents)}</ol></section>'''
    return shell(BOOK, 'index', main, None, (first, 'Begin reading'))


def copy_figures():
    """Copy into docs/figures only the image files the chapters use; the untouched originals and unused files stay out."""
    used = set()
    for stem, _, _ in ORDER:
        path = os.path.join(ROOT, 'chapters', f'{stem}.md')
        if os.path.exists(path):
            used |= set(re.findall(r'src="(figures/[^"]+)"', open(path, encoding='utf-8').read()))
    shutil.rmtree(os.path.join(OUT, 'figures'), ignore_errors=True)
    for rel in sorted(used):
        dst = os.path.join(OUT, *rel.split('/'))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(os.path.join(ROOT, *rel.split('/')), dst)
    return used


if __name__ == '__main__':
    os.makedirs(os.path.join(OUT, 'assets'), exist_ok=True)
    copy_figures()
    for f in ('book.css', 'book.js'):
        shutil.copy(os.path.join(ROOT, 'tools', 'theme', f), os.path.join(OUT, 'assets', f))
    open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(title_page())
    built = ['index']
    for i, (stem, page, _) in enumerate(ORDER):
        if load(stem):
            open(os.path.join(OUT, f'{page}.html'), 'w', encoding='utf-8').write(chapter_page(i, stem, page))
            built.append(page)
    open(os.path.join(OUT, '.nojekyll'), 'w').close()
    print('built:', ', '.join(built))
