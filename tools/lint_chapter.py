"""Check a chapter against STYLE.md. usage: python tools/lint_chapter.py chapters/ch01.md sources/ch1.md [more sources]
Prints JSON; exit 1 on any FAIL. FAIL: dashes as punctuation, emoji, exclamation mark, contraction, day framing,
hashtag or link placeholder, AI vocabulary, a number that does not appear in the sources, malformed front matter.
WARN: American spelling, negative parallelism, more than two fragments in a row, bold in running text."""
import json, re, sys

chapter, sources = sys.argv[1], sys.argv[2:]
text = open(chapter, encoding='utf-8').read()
src = ' '.join(open(s, encoding='utf-8').read() for s in sources)
fails, warns = [], []

fm = re.match(r'^---\n(.*?)\n---\n', text, re.S)
if not fm:
    fails.append('missing front matter')
    body = text
else:
    body = text[fm.end():]
    for key in ('title', 'summary'):
        if not re.search(rf'^{key}:', fm.group(1), re.M):
            fails.append(f'front matter lacks {key}')

prose = re.sub(r'```.*?```', ' ', body, flags=re.S)          # code is quoted verbatim, so not checked as prose
prose_nohtml = re.sub(r'<[^>]+>', ' ', prose)
whole = (fm.group(1) if fm else '') + '\n' + prose_nohtml

if re.search('[—–]', whole) or re.search(r'\s--\s', whole):
    fails.append('em or en dash used as punctuation')
if re.search('[\U0001F000-\U0001FAFF☀-➿⬀-⯿️]', whole):
    fails.append('emoji')
if re.search(r'\w!(\s|$)', whole):
    fails.append('exclamation mark')
m = re.findall(r"\b\w+(?:n['’]t|['’](?:re|ve|ll|d|m))\b", whole)
if m:
    fails.append(f'contractions: {sorted(set(m))[:8]}')
for pat in (r'\byesterday\b', r'\btomorrow\b', r'\btoday I\b', r'\bDay \d+\b(?!.*of the series)', r'\bthis series\b',
            r'\bin the comments\b', r'hashtag', r'link to the chapter repository'):
    for hit in re.finditer(pat, whole, re.I):
        line = whole[max(0, hit.start() - 40): hit.end() + 30].replace('\n', ' ')
        if 'rewritten from the posts' in line:
            continue
        fails.append(f'day or social framing: ...{line}...')
        break
AI = ['delve', 'intricate', 'tapestry', 'showcase', 'foster', 'meticulous', 'seamless', 'valuable insight', 'pivotal',
      'crucial', 'testament', 'underscore', 'evolving landscape', 'plays a key role', 'plays a crucial role', 'vibrant',
      'groundbreaking', 'in conclusion', 'in summary', 'overall,', 'additionally,', 'it is important to note',
      'it is worth noting', 'navigate the', 'realm', 'embark']
low = whole.lower()
for w in AI:
    if w in low:
        fails.append(f'AI vocabulary: "{w}"')
srcnums = set(n.replace(',', '') for n in re.findall(r'\d[\d,]*(?:\.\d+)?', src))
# Figure and listing labels are editorial apparatus, numbered within the chapter, so they are not facts from the sources.
# The References section is left out as well: STYLE.md allows full bibliographic details (volume, issue, pages) once
# they have been verified with a search tool, and those are not in the posts.
countable = re.sub(r'\b(?:Figure|Listing|Table)\s+\d+\.\d+', ' ', re.split(r'^## References\b', whole, flags=re.M)[0])
for n in sorted(set(re.findall(r'(?<![\w.#/-])\d[\d,]*(?:\.\d+)?(?![\w/-])', countable))):
    k = n.replace(',', '').rstrip('.')
    if k and k not in srcnums and not (k.isdigit() and int(k) <= 10):
        fails.append(f'number not in the sources: {n}')
AMER = {r'\banalyz': 'analys', r'\bcolor(?:s|ed|ing|ful|less)?\b': 'colour',  # whole word: colorectal is British too
        r'\bbehavior': 'behaviour', r'\blabeled\b': 'labelled',
        r'\bmodeling\b': 'modelling', r'\btumor': 'tumour', r'\bcenter\b': 'centre', r'\bhemagglutinin': 'haemagglutinin'}
for pat, fix in AMER.items():
    if re.search(pat, low):
        warns.append(f'American spelling, use {fix}')
neg = re.findall(r"\b(?:not just|not only)\b[^.]{0,80}\bbut\b", low)
if len(neg) > 1:
    warns.append(f'negative parallelism used {len(neg)} times')
if re.search(r'(?<![<\w])\*\*[^*]+\*\*', re.sub(r'<(div|aside)[^>]*>.*?</(div|aside)>', ' ', prose, flags=re.S)):
    warns.append('bold in running text')
res = {'ok': not fails, 'fails': sorted(set(fails)), 'warns': sorted(set(warns)),
       'words': len(re.findall(r"[A-Za-z][A-Za-z'’-]*", prose_nohtml))}
print(json.dumps(res, indent=1, ensure_ascii=False))
sys.exit(0 if not fails else 1)
