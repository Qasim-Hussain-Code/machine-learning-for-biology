"""Build the EPUB edition of Machine Learning for Biology: docs/machine-learning-for-biology.epub.
EPUB 3 with an EPUB 2 table of contents for older readers. The text is rendered by the same code as the web and print
editions (tools/build_book.py, tools/print_book.py); code listings are shown in full, and the reader's own settings
decide the type size. The build checks that every file is well-formed XML and that every reference resolves.
usage: python tools/epub_book.py"""
import datetime, html, io, os, re, sys, uuid, zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_book as B  # noqa: E402
import print_book as P  # noqa: E402
from lxml import etree, html as lhtml  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

EPUB = os.path.join(B.OUT, 'machine-learning-for-biology.epub')
BOOK_ID = 'urn:uuid:' + str(uuid.uuid5(uuid.NAMESPACE_URL, 'https://github.com/Qasim-Hussain-Code/machine-learning-for-biology'))
XHTML_NS = 'http://www.w3.org/1999/xhtml'

CSS = """@charset "utf-8";
body{font-family:"STIX Two Text","STIXGeneral",Georgia,serif;line-height:1.5;color:#202326;margin:0 3%}
p{margin:0 0 .65em;text-align:justify;-webkit-hyphens:auto;hyphens:auto;orphans:2;widows:2}
a{color:#036394;text-decoration:none}
code,pre{font-family:"IBM Plex Mono",Consolas,"Courier New",monospace}
code{font-size:.85em}
h1,h2{color:#111111;font-weight:500;line-height:1.25;-webkit-hyphens:none;hyphens:none}
.cover{margin:0;padding:0;text-align:center}
.cover img{max-width:100%;max-height:100%}
.titlepage{margin-top:28%}
.titlepage h1{font-size:2em;font-weight:600;margin:0 0 .8em}
.titlepage .rule{width:4em;border-top:1px solid #036394;margin:0 0 1.2em}
.titlepage .author{letter-spacing:.14em;text-transform:uppercase;color:#5F6368;font-size:.9em;text-align:left}
.epipage{margin-top:30%}
.epipage blockquote{margin:0 0 1em;font-style:italic;font-size:1.15em;color:#111111}
.epipage p{text-align:left;font-size:.8em;color:#5F6368;margin:0}
.epipage .who{font-weight:600;color:#111111;font-size:.9em}
.partpage{margin-top:35%}
.partpage .pk{font-size:.75em;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:#036394;text-align:left}
.partpage h1{font-size:1.7em;font-variant:small-caps;margin:0}
.opener{margin:1.5em 0 1.4em}
.opener .kicker{font-size:.72em;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:#036394;margin:0 0 .5em;text-align:left}
.opener h1{font-size:1.55em;font-variant:small-caps;margin:0 0 .35em}
.opener .model{font-family:"IBM Plex Mono",Consolas,monospace;font-size:.75em;color:#5F6368;text-align:left;margin:0 0 .4em}
.opener .question{font-style:italic;font-size:1.05em;color:#111111;text-align:left;margin:0}
.summary{border-top:1px solid #111111;border-bottom:1px solid #D5D7DA;padding:.6em 0 .3em;margin:0 0 1.4em}
.summary .sk{font-size:.7em;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:#036394;margin:0 0 .3em;text-align:left}
.summary p{font-size:.92em}
h2{font-size:1.1em;font-variant:small-caps;letter-spacing:.02em;margin:1.5em 0 .5em;page-break-after:avoid}
.secno{font-family:"IBM Plex Mono",Consolas,monospace;font-size:.75em;color:#5F6368;font-variant:normal;margin-right:.4em}
aside.note{display:block;margin:.5em 0 1em;padding:.4em .8em;border-left:2px solid #036394;background:#F4F7F9;font-size:.88em}
aside.note p{text-align:left;margin:0}
.rules{border-top:1px solid #111111;border-bottom:1px solid #111111;padding:.4em 0 .1em;margin:1em 0 1.3em}
.rules p{text-align:left;font-size:.92em;border-top:1px solid #D5D7DA;padding:.4em 0;margin:0}
.rules p.rh{border-top:0;font-size:.7em;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:#036394}
.rules p strong{display:block;font-family:"IBM Plex Mono",Consolas,monospace;font-size:.82em;font-weight:500;color:#111111}
figure.fig{margin:1.2em 0;page-break-inside:avoid}
figure.fig img{display:block;width:100%;height:auto;margin:0 auto;border:1px solid #D5D7DA}
figcaption{font-size:.84em;line-height:1.4;color:#3C4043;margin-top:.5em;text-align:left}
figcaption b{color:#111111}
.lst-cap{font-size:.84em;color:#3C4043;text-align:left;margin:1.2em 0 .3em;page-break-after:avoid}
.lst-cap b{color:#111111}
pre{font-size:.72em;line-height:1.4;background:#F6F6F5;border:1px solid #D5D7DA;padding:.6em .8em;margin:0 0 1em;
  white-space:pre-wrap;word-wrap:break-word}
pre code{font-size:1em}
.prov{font-size:.84em;font-style:italic;color:#5F6368;text-align:left;margin-top:1.4em}
.refs p{font-size:.88em;text-align:left;padding-left:1.4em;text-indent:-1.4em}
.endm{margin-top:1.6em;border-top:1px solid #111111;padding-top:.5em}
.endm .eh{font-size:.7em;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:#036394;margin:.6em 0 .2em;text-align:left}
.endm p{font-size:.86em;text-align:left;margin:0 0 .25em}
.endm .lbl{font-family:"IBM Plex Mono",Consolas,monospace;font-size:.85em;color:#5F6368;margin-right:.4em}
.nw{white-space:nowrap}
nav#toc ol{list-style:none;padding-left:1.1em}
nav#toc>ol{padding-left:0}
nav#toc li{margin:.25em 0}
"""


def xhtml(fragment):
    """An HTML fragment as well-formed XHTML, with the web edition's interactive parts removed."""
    root = lhtml.fragment_fromstring(fragment, create_parent='div')
    for a in root.xpath('.//a[@class="figlink"]'):
        img = a.find('img')
        parent = a.getparent()
        img.tail = (img.tail or '') + (a.tail or '')
        parent.replace(a, img)
    for img in root.xpath('.//img'):
        img.set('src', '../images/' + os.path.basename(img.get('src')))
    for el in root.xpath('.//*[@tabindex]'):
        del el.attrib['tabindex']
    for el in root.xpath('.//*[@title]'):
        if el.tag == 'a':
            del el.attrib['title']
    out = html.escape(root.text or '', quote=False)
    for child in root:
        out += etree.tostring(child, method='xml', encoding='unicode')
    return out


def page(title, body, epub_type):
    return ('<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n'
            f'<html xmlns="{XHTML_NS}" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en-GB" lang="en-GB">\n'
            f'<head><meta charset="utf-8"/><title>{html.escape(title)}</title>'
            '<link rel="stylesheet" type="text/css" href="../css/book.css"/></head>\n'
            f'<body epub:type="{epub_type}">{body}</body></html>\n')


SVG_STYLE = ('<style>.fi{fill:#111111}.fm{fill:#5F6368}.fl{fill:#D5D7DA}.fa{fill:#036394}.fa2{fill:#B45309}.fb{fill:#B91C1C}'
             '.fp{fill:#F2F5F8}.fbg{fill:#FFFFFF}.fn{fill:none}.si{stroke:#111111}.sm{stroke:#5F6368}.sl{stroke:#D5D7DA}'
             '.sa{stroke:#036394}.sa2{stroke:#B45309}.sb{stroke:#B91C1C}text{font-family:"STIX Two Text",STIXGeneral,Georgia,serif}'
             '.num,.num text{font-family:"IBM Plex Mono",Consolas,monospace}</style>')


def figure_bytes(name):
    """An image for the e-book: a photograph or infographic as it is, or a drawn figure with its light palette written in."""
    if name.lower().endswith('.svg'):
        svg = open(os.path.join(B.ROOT, 'figures', 'svg', name), encoding='utf-8').read()
        svg = re.sub(r'(<svg\b[^>]*>)', lambda m: m.group(1) + SVG_STYLE, svg, count=1)
        return svg.encode('utf-8')
    return open(os.path.join(B.ROOT, 'figures', 'web', name), 'rb').read()


def cover_image():
    """A plain cover in the book's colours: the title, the accent rule and the author, set in STIX."""
    W, H = 1600, 2400
    im = Image.new('RGB', (W, H), '#0E1626')
    d = ImageDraw.Draw(im)
    try:
        import matplotlib
        fonts = os.path.join(os.path.dirname(matplotlib.__file__), 'mpl-data', 'fonts', 'ttf')
        title_font = ImageFont.truetype(os.path.join(fonts, 'STIXGeneralBol.ttf'), 150)
        author_font = ImageFont.truetype(os.path.join(fonts, 'STIXGeneral.ttf'), 58)
    except Exception:
        title_font = ImageFont.truetype('georgiab.ttf', 140)
        author_font = ImageFont.truetype('georgia.ttf', 56)
    x, y = 150, 820
    for line in ('Machine Learning', 'for Biology'):
        d.text((x, y), line, font=title_font, fill='#ECEEF0')
        y += 190
    d.rectangle([x, y + 60, x + 260, y + 66], fill='#7DD3FC')
    spaced = '  '.join(' '.join(word) for word in B.AUTHOR.upper().split())
    d.text((x, y + 130), spaced, font=author_font, fill='#C5CEDB')
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=90)
    return buf.getvalue()


def build():
    B.INLINE_SVG = False  # e-readers get the drawn figures as image files, coloured by their own style
    files, spine, nav, ncx = {}, [], [], []
    title_body = (f'<section class="titlepage" epub:type="titlepage"><h1>{B.BOOK}</h1><div class="rule"></div>'
                  f'<p class="author">{B.AUTHOR}</p></section>')
    epi_body = (f'<section class="epipage" epub:type="epigraph"><blockquote><p>{html.escape(B.EPIGRAPH)}</p></blockquote>'
                f'<p class="who">{B.EPI_WHO}</p><p>{html.escape(B.EPI_ROLE)}</p><p>{html.escape(B.EPI_SRC)}</p></section>')
    files['text/cover.xhtml'] = page(B.BOOK, '<div class="cover"><img src="../images/cover.jpg" alt="Cover: Machine Learning for Biology, by Qasim Hussain"/></div>', 'cover')
    files['text/title.xhtml'] = page(B.BOOK, title_body, 'frontmatter')
    files['text/epigraph.xhtml'] = page('Epigraph', epi_body, 'frontmatter')
    spine += ['text/cover.xhtml', 'text/title.xhtml', 'text/epigraph.xhtml', 'nav.xhtml']
    seen_part = None
    for stem, pg, part in B.ORDER:
        if not B.load(stem):
            continue
        meta, section = P.piece(stem, pg)
        if part and part != seen_part:
            seen_part = part
            num, label = B.PARTS[part].split(' · ')
            href = f'text/part-{part.lower()}.xhtml'
            files[href] = page(B.PARTS[part], f'<section class="partpage" epub:type="part"><p class="pk">{num}</p><h1>{html.escape(label)}</h1></section>', 'bodymatter')
            spine.append(href)
            nav.append({'href': href, 'label': B.PARTS[part], 'children': []})
        href = f'text/{pg}.xhtml'
        body = xhtml(section)
        kind = 'bodymatter chapter' if meta.get('chapter') else ('frontmatter preface' if stem == 'preface' else
                                                               'frontmatter prologue' if stem == 'prologue' else 'backmatter epilogue')
        files[href] = page(meta.get('title', stem.title()), body, kind)
        spine.append(href)
        doc = etree.fromstring(files[href].encode('utf-8'))
        secs = [{'href': f'{href}#{h.get("id")}', 'label': re.sub(r'\s+', ' ', ''.join(h.itertext())).strip(), 'children': []}
                for h in doc.iter(f'{{{XHTML_NS}}}h2') if h.get('id') and not h.get('id').endswith('references')]
        label = (f'{meta["chapter"]} ' if meta.get('chapter') else '') + meta.get('title', stem.title())
        entry = {'href': href, 'label': label, 'children': secs if meta.get('chapter') else []}
        (nav[-1]['children'] if part else nav).append(entry)

    def ol(items):
        return '<ol>' + ''.join(f'<li><a href="{html.escape(i["href"])}">{html.escape(i["label"])}</a>{ol(i["children"]) if i["children"] else ""}</li>'
                                for i in items) + '</ol>'
    files['nav.xhtml'] = ('<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n'
                          f'<html xmlns="{XHTML_NS}" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en-GB" lang="en-GB">\n'
                          '<head><meta charset="utf-8"/><title>Contents</title><link rel="stylesheet" type="text/css" href="css/book.css"/></head>\n'
                          f'<body epub:type="frontmatter"><nav epub:type="toc" id="toc"><h1>Contents</h1>{ol(nav)}</nav>'
                          '<nav epub:type="landmarks" hidden=""><ol><li><a epub:type="cover" href="text/cover.xhtml">Cover</a></li>'
                          '<li><a epub:type="toc" href="nav.xhtml">Contents</a></li>'
                          f'<li><a epub:type="bodymatter" href="{spine[4]}">Begin reading</a></li></ol></nav></body></html>\n')
    play = [0]

    def points(items):
        out = ''
        for i in items:
            play[0] += 1
            out += (f'<navPoint id="np{play[0]}" playOrder="{play[0]}"><navLabel><text>{html.escape(i["label"])}</text></navLabel>'
                    f'<content src="{html.escape(i["href"])}"/>{points(i["children"])}</navPoint>')
        return out
    files['toc.ncx'] = ('<?xml version="1.0" encoding="utf-8"?>\n<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">'
                        f'<head><meta name="dtb:uid" content="{BOOK_ID}"/></head><docTitle><text>{B.BOOK}</text></docTitle>'
                        f'<navMap>{points(nav)}</navMap></ncx>\n')
    files['css/book.css'] = CSS
    images = sorted({os.path.basename(s) for f in files.values() for s in re.findall(r'src="\.\./images/([^"]+)"', f)} - {'cover.jpg'})
    binary = {f'images/{n}': figure_bytes(n) for n in images}
    binary['images/cover.jpg'] = cover_image()
    modified = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    types = {'.xhtml': 'application/xhtml+xml', '.css': 'text/css', '.ncx': 'application/x-dtbncx+xml', '.svg': 'image/svg+xml',
             '.jpeg': 'image/jpeg', '.jpg': 'image/jpeg', '.png': 'image/png'}
    ids = {}
    manifest = []
    for href in list(files) + list(binary):
        ident = 'i-' + re.sub(r'[^A-Za-z0-9]+', '-', href)
        ids[href] = ident
        props = ' properties="nav"' if href == 'nav.xhtml' else ' properties="cover-image"' if href == 'images/cover.jpg' else ''
        manifest.append(f'<item id="{ident}" href="{href}" media-type="{types[os.path.splitext(href)[1]]}"{props}/>')
    opf = ('<?xml version="1.0" encoding="utf-8"?>\n'
           '<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid" xml:lang="en-GB">'
           '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">'
           f'<dc:identifier id="bookid">{BOOK_ID}</dc:identifier><dc:title>{B.BOOK}</dc:title>'
           f'<dc:creator id="author">{B.AUTHOR}</dc:creator><meta refines="#author" property="role" scheme="marc:relators">aut</meta>'
           f'<dc:language>en-GB</dc:language><dc:date>{modified[:10]}</dc:date><meta property="dcterms:modified">{modified}</meta>'
           f'<meta name="cover" content="{ids["images/cover.jpg"]}"/></metadata>'
           f'<manifest>{"".join(manifest)}</manifest>'
           f'<spine toc="{ids["toc.ncx"]}">' + ''.join(f'<itemref idref="{ids[h]}"/>' for h in spine) + '</spine></package>\n')
    files['content.opf'] = opf
    container = ('<?xml version="1.0" encoding="utf-8"?>\n<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
                 '<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>\n')
    # checks: every text file is well-formed XML, and every href and src inside the book resolves
    for name, text in list(files.items()) + [('container.xml', container)]:
        if name.endswith('.css'):
            continue
        etree.fromstring(text.encode('utf-8'))
    present = set(files) | set(binary)
    for name, text in files.items():
        base = os.path.dirname(name)
        for ref in re.findall(r'(?:href|src)="([^"#:]+)(?:#[^"]*)?"', text):
            target = os.path.normpath(os.path.join(base, ref)).replace('\\', '/')
            if target not in present and not ref.startswith('http'):
                sys.exit(f'{name}: unresolved reference {ref}')
    tmp = EPUB + '.tmp'
    with zipfile.ZipFile(tmp, 'w') as z:
        z.writestr(zipfile.ZipInfo('mimetype'), 'application/epub+zip', compress_type=zipfile.ZIP_STORED)
        z.writestr('META-INF/container.xml', container, compress_type=zipfile.ZIP_DEFLATED)
        for name, text in files.items():
            z.writestr(f'OEBPS/{name}', text, compress_type=zipfile.ZIP_DEFLATED)
        for name, data in binary.items():
            z.writestr(f'OEBPS/{name}', data, compress_type=zipfile.ZIP_STORED)
    os.replace(tmp, EPUB)
    return len(spine), len(binary), os.path.getsize(EPUB)


if __name__ == '__main__':
    n, imgs, size = build()
    print(f'{EPUB}: {n} documents in the reading order, {imgs} images, {size / 1e6:.1f} MB')
