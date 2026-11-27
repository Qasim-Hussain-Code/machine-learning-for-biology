"""Build the print edition of Machine Learning for Biology as a PDF.
The whole book is written into one HTML document (docs/print.html, styled by tools/theme/print.css) and printed by
headless Chrome (tools/print_pdf.mjs). It is printed twice: the first pass finds the page on which each part begins,
and the second fills those page numbers into the contents. The cover (figures/cover.jpg) is then put in front as an
uncounted sheet in place of a title page, so the PDF has one page more than the highest printed page number.
usage: python tools/print_book.py        -> docs/machine-learning-for-biology.pdf"""
import html, os, re, shutil, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_book as B  # noqa: E402
from pypdf import PdfReader  # noqa: E402

HTML_NAME = 'print.html'
PDF_PATH = os.path.join(B.OUT, 'machine-learning-for-biology.pdf')
PRINTER = os.path.join(B.ROOT, 'tools', 'print_pdf.mjs')
COVER = os.path.join(B.ROOT, 'figures', 'cover.jpg')
COVER_GROUND = '#0E1626'   # the cover's navy, painted beside the image to the edges of the sheet
# The cover's lettering, measured in the picture's own pixels (1600 x 2400, design 62): each line's words, its tag,
# its left and right edges, its baseline and its type size. The same words are laid over the picture as invisible
# text, so that programs which read a PDF's first page (Google Scholar, screen readers) find the title and the author
# there. COVER_SHA guards the measurements: a new cover needs them taken again.
COVER_SHA = 'a57452443595e3ec'
COVER_WORDS = (('Machine Learning', '/H1', 162, 1438, 332, 160),
               ('for Biology', '/H1', 162, 914, 504, 160),
               ('Qasim Hussain', '/P', 163, 728, 674, 66))
# Times-Roman advance widths, in thousandths of the type size, for the letters above: each invisible line is stretched
# to the width of the lettering it lies over
TIMES = {' ': 250, 'B': 667, 'H': 722, 'L': 611, 'M': 889, 'Q': 722, 'a': 444, 'c': 444, 'e': 444, 'f': 333, 'g': 500,
         'h': 500, 'i': 278, 'l': 278, 'm': 778, 'n': 500, 'o': 500, 'r': 333, 's': 389, 'u': 500, 'y': 500}


def piece(stem, page):
    meta, md_text = B.load(stem)
    n = meta.get('chapter')
    body = B.render_body(md_text, n)
    body = re.sub(r'<h2 id="([^"]+)"', lambda m: f'<h2 id="{page}-{m.group(1)}"', body)
    refs = re.search(r'<h2 id="[^"]*references">.*?</h2>', body, re.S)
    if refs:
        body = body[:refs.end()] + '<div class="refs">' + body[refs.end():] + '</div>'
    title = html.escape(meta.get('title', stem.title()))
    if n:
        head = (f'<header class="opener"><p class="kicker">Chapter {n}</p><h1>{title}</h1>'
                f'<p class="model">Model: {html.escape(str(meta.get("model", "")))}</p>'
                + (f'<p class="question">{html.escape(B.curl(meta["question"]))}</p>' if meta.get('question') else '') + '</header>')
        summ = (f'<section class="summary"><p class="sk">Summary</p><p>{B.polish(B.markdown.markdown(str(meta["summary"]), extensions=["smarty"])[3:-4])}</p></section>'
                if meta.get('summary') else '')
    else:
        head, summ = f'<header class="opener"><h1>{title}</h1></header>', ''
    end = ''
    if meta.get('repository'):
        repo, commit = meta['repository'], str(meta.get('commit', ''))
        url = f'https://github.com/{repo}'
        end = (f'<section class="endm"><div><p class="eh">Run it</p>'
               f'<p><span class="lbl">Repository</span><a href="{url}">github.com/{repo}</a></p>'
               f'<p><span class="lbl">Commit</span><a href="{url}/tree/{commit}"><code>{commit}</code></a></p></div>'
               f'<div><p class="eh">Cite this chapter</p><p>{B.cite(meta.get("title", ""), n)}</p></div></section>')
    cls = 'piece chapter' if n else 'piece'
    return meta, f'<section class="{cls}" id="p-{page}">{head}{summ}<div class="body">{body}</div>{end}</section>'


def document(pages=None):
    pages = pages or {}
    contents, parts, seen_part = [], [], None

    def pg(key):
        return f'<span class="pg">{pages.get(key, "")}</span>'
    for stem, page, p in B.ORDER:
        got = B.load(stem)
        if not got:
            continue
        meta, text = piece(stem, page)
        if p and p != seen_part:
            seen_part = p
            num, label = B.PARTS[p].split(' · ')
            contents.append(f'<li class="part"><a href="#part-{p}" style="display:block;border:0;padding:0">{html.escape(B.PARTS[p])}</a></li>')
            parts.append(f'<section class="partpage" id="part-{p}"><p class="pk">{num}</p><h1>{html.escape(label)}</h1></section>')
        n = meta.get('chapter')
        num = f'<span class="n">{n}</span>' if n else '<span class="n"></span>'
        model = f'<span class="m">{html.escape(meta["model"])}</span>' if meta.get('model') else ''
        contents.append(f'<li><a href="#p-{page}">{num}<span class="t">{html.escape(meta.get("title", stem.title()))}</span>{pg(page)}{model}</a></li>')
        parts.append(text)
    # No title page: the cover, put in front by finish(), shows the title and the author, and a title page after it
    # only repeated them. The cover also carries both as invisible, tagged text (see add_cover), which is what Google
    # Scholar and a screen reader read; the document information, which finish() writes, names them as well.
    front = (f'<section class="epipage"><blockquote>{B.EPIGRAPH}</blockquote><p class="who">{B.EPI_WHO}</p>'
             f'<p>{B.EPI_ROLE}</p><p>{B.EPI_SRC}</p></section>'
             f'<section class="contents-page"><h2>Contents</h2><ol>{"".join(contents)}</ol></section>')
    return f'''<!doctype html><html lang="en-GB"><head><meta charset="utf-8">
<title>{B.BOOK}</title><meta name="author" content="{B.AUTHOR}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{B.FONTS}" rel="stylesheet"><link rel="stylesheet" href="assets/print.css"></head>
<body>{front}{"".join(parts)}</body></html>'''


def print_pdf(out):
    r = subprocess.run(['node', PRINTER, B.OUT, HTML_NAME, out], capture_output=True, text=True, encoding='utf-8')
    if r.returncode:
        sys.exit(f'printing failed: {r.stderr.strip() or r.stdout.strip()}')
    return r.stdout.strip()


def link_targets(pdf):
    """Map each #fragment linked from the contents page to the (1-based) page it lands on."""
    reader = PdfReader(pdf)
    named = {}
    for name, dest in reader.named_destinations.items():
        try:
            named[name.lstrip('/')] = reader.get_destination_page_number(dest) + 1
        except Exception:
            pass
    found = {}
    for i, page in enumerate(reader.pages[:8]):
        for ref in page.get('/Annots') or []:
            a = ref.get_object()
            if a.get('/Subtype') != '/Link':
                continue
            dest = a.get('/Dest')
            if dest is None and a.get('/A') is not None:
                dest = a['/A'].get('/D')
            if dest is None:
                continue
            if isinstance(dest, (str, bytes)) or hasattr(dest, 'original_bytes'):
                key = str(dest).lstrip('/')
                if key in named:
                    found[key] = named[key]
            else:
                try:
                    found[f'page{len(found)}'] = reader.get_page_number(dest[0].get_object() if hasattr(dest[0], 'get_object') else dest[0]) + 1
                except Exception:
                    pass
    return found, named, len(reader.pages)


def add_cover(writer):
    """Put the cover (figures/cover.jpg, the image the EPUB uses) in front of the printed pages as a sheet of its own.
    The sheet is painted in the cover's navy to its edges and the image is fitted by height and centred, so no white
    shows. The cover is not counted: the page labels call it "Cover" and the epigraph is page 1, as printed.

    The title and the author are lettered into the picture, where no program can read them, so the same words are
    laid over the lettering as invisible text (rendering mode 3, the way a scanned page carries its recognised text)
    and tagged as a heading and a paragraph. Google Scholar takes a document's title and authors from the text of its
    first page, and a screen reader now finds them on the cover too."""
    import hashlib
    from PIL import Image
    from pypdf import PageObject
    from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject, NumberObject, StreamObject
    if hashlib.sha256(open(COVER, 'rb').read()).hexdigest()[:16] != COVER_SHA:
        sys.exit(f'{COVER} has changed: measure its lettering again and update COVER_WORDS and COVER_SHA')
    box = writer.pages[0].mediabox
    W, H = float(box.width), float(box.height)
    with Image.open(COVER) as im:
        iw, ih = im.size
        if im.format != 'JPEG' or im.mode != 'RGB':
            sys.exit(f'{COVER} must be an RGB JPEG to go into the PDF as it is')
    image = StreamObject()
    image._data = open(COVER, 'rb').read()
    image.update({NameObject('/Type'): NameObject('/XObject'), NameObject('/Subtype'): NameObject('/Image'),
                  NameObject('/Width'): NumberObject(iw), NameObject('/Height'): NumberObject(ih),
                  NameObject('/ColorSpace'): NameObject('/DeviceRGB'), NameObject('/BitsPerComponent'): NumberObject(8),
                  NameObject('/Filter'): NameObject('/DCTDecode')})
    w = H * iw / ih
    x0, s = (W - w) / 2, H / ih   # where the picture starts on the sheet, and points per pixel of the picture
    r, g, b = (int(COVER_GROUND[i:i + 2], 16) / 255 for i in (1, 3, 5))
    # the picture and the navy beside it are decoration, so they are marked as an artifact; the words are not
    ops = [f'/Artifact BMC q {r:.4f} {g:.4f} {b:.4f} rg 0 0 {W:.2f} {H:.2f} re f Q '
           f'q {w:.2f} 0 0 {H:.2f} {x0:.2f} 0 cm /Cover Do Q EMC']
    for mcid, (words, tag, left, right, base, size) in enumerate(COVER_WORDS):
        pt = size * s
        stretch = 100 * (right - left) * s / (sum(TIMES[c] for c in words) / 1000 * pt)
        ops.append(f'{tag} <</MCID {mcid}>> BDC BT 3 Tr /Words {pt:.2f} Tf {stretch:.1f} Tz '
                   f'1 0 0 1 {x0 + left * s:.2f} {H - base * s:.2f} Tm ({words}) Tj ET EMC')
    draw = DecodedStreamObject()
    draw.set_data(' '.join(ops).encode('ascii'))
    font = DictionaryObject({NameObject('/Type'): NameObject('/Font'), NameObject('/Subtype'): NameObject('/Type1'),
                             NameObject('/BaseFont'): NameObject('/Times-Roman'),
                             NameObject('/Encoding'): NameObject('/WinAnsiEncoding')})
    page = PageObject.create_blank_page(width=W, height=H)
    page[NameObject('/Resources')] = DictionaryObject({
        NameObject('/XObject'): DictionaryObject({NameObject('/Cover'): writer._add_object(image)}),
        NameObject('/Font'): DictionaryObject({NameObject('/Words'): writer._add_object(font)})})
    page[NameObject('/Contents')] = writer._add_object(draw)
    writer.insert_page(page, 0)
    tag_cover(writer, writer.pages[0])
    writer.set_page_label(0, 0, prefix='Cover')
    writer.set_page_label(1, len(writer.pages) - 1, style='/D', start=1)


def tag_cover(writer, page):
    """Put the cover's words at the head of the document's structure, as a heading (the title, both lines) and a
    paragraph (the author), and give the cover its entry in the parent tree, which maps each marked piece of a page
    back to its element."""
    from pypdf.generic import ArrayObject, DictionaryObject, IndirectObject, NameObject, NumberObject
    tree = writer._root_object['/StructTreeRoot'].get_object()
    top_ref = tree.raw_get('/K')
    if not isinstance(top_ref, IndirectObject):
        sys.exit('the structure tree has no single top element to put the cover under')
    top = top_ref.get_object()
    elems = {}
    for mcid, (_, tag, *_) in enumerate(COVER_WORDS):
        if tag not in elems:
            elems[tag] = DictionaryObject({NameObject('/Type'): NameObject('/StructElem'), NameObject('/S'): NameObject(tag),
                                           NameObject('/P'): top_ref, NameObject('/Pg'): page.indirect_reference,
                                           NameObject('/K'): ArrayObject()})
        elems[tag]['/K'].append(NumberObject(mcid))
    refs = {tag: writer._add_object(e) for tag, e in elems.items()}
    kids = top.get('/K')
    kids = list(kids) if isinstance(kids, list) else ([] if kids is None else [top.raw_get('/K')])
    top[NameObject('/K')] = ArrayObject(list(refs.values()) + kids)
    key = int(tree['/ParentTreeNextKey'])
    page[NameObject('/StructParents')] = NumberObject(key)
    tree['/ParentTree'].get_object()['/Nums'].extend([NumberObject(key), ArrayObject([refs[t] for _, t, *_ in COVER_WORDS])])
    tree[NameObject('/ParentTreeNextKey')] = NumberObject(key + 1)


def finish(pdf, html_text):
    """Chrome drops the space where a heading wraps when it builds the bookmarks, so put the headings' own text back,
    record the title and author in the document information, and put the cover in front."""
    from pypdf import PdfWriter
    from pypdf.generic import NameObject, TextStringObject
    squash = lambda s: re.sub(r'\s+', '', s)
    heads = [html.unescape(re.sub(r'<[^>]+>', ' ', h)).strip() for h in re.findall(r'<h[12][^>]*>(.*?)</h[12]>', html_text, re.S)]
    want = {squash(h): re.sub(r'\s+', ' ', h) for h in heads}
    writer = PdfWriter(clone_from=pdf)
    fixed = 0

    def walk(node):
        nonlocal fixed
        while node is not None:
            item = node.get_object()
            title = str(item.get('/Title', ''))
            better = want.get(squash(title))
            if better and better != title:
                item[NameObject('/Title')] = TextStringObject(better)
                fixed += 1
            if '/First' in item:
                walk(item['/First'])
            node = item.get('/Next')
    outlines = writer._root_object.get('/Outlines')
    if outlines is not None and '/First' in outlines.get_object():
        walk(outlines.get_object()['/First'])
    writer.add_metadata({'/Title': B.BOOK, '/Author': B.AUTHOR, '/Subject': 'Machine learning for biology, in seven chapters'})
    add_cover(writer)
    tmp = pdf + '.tmp'
    with open(tmp, 'wb') as f:
        writer.write(f)
    os.replace(tmp, pdf)
    return fixed


if __name__ == '__main__':
    os.makedirs(os.path.join(B.OUT, 'assets'), exist_ok=True)
    shutil.copy(os.path.join(B.ROOT, 'tools', 'theme', 'print.css'), os.path.join(B.OUT, 'assets', 'print.css'))
    B.copy_figures()
    target = os.path.join(B.OUT, HTML_NAME)
    open(target, 'w', encoding='utf-8').write(document({page: '000' for _, page, _ in B.ORDER}))
    first = PDF_PATH + '.pass1.pdf'
    print_pdf(first)
    found, named, total = link_targets(first)
    pages = {}
    for _, page, _ in B.ORDER:
        key = f'p-{page}'
        if key in named:
            pages[page] = named[key]
    missing = [page for stem, page, _ in B.ORDER if B.load(stem) and page not in pages]
    if missing:
        sys.exit(f'could not find the start page of: {missing} (named destinations: {sorted(named)[:20]})')
    open(target, 'w', encoding='utf-8').write(document(pages))
    print_pdf(PDF_PATH)
    _, named2, total2 = link_targets(PDF_PATH)
    moved = {p: (pages[p], named2.get(f'p-{p}')) for p in pages if named2.get(f'p-{p}') != pages[p]}
    os.remove(first)
    if moved:
        sys.exit(f'page numbers moved between passes: {moved}')
    fixed = finish(PDF_PATH, open(target, encoding='utf-8').read())
    print(f'{PDF_PATH}: the cover and {total2} pages, {fixed} bookmark titles repaired; starts: '
          + ', '.join(f'{p} {n}' for p, n in pages.items()))
