"""Trim series framing from the infographics: the "DAY NN" strips and the footers that refer to other days.
The untouched images are kept in figures/original/, and every crop is made from them, so the step can be rerun
or undone (copy the originals back). Nothing inside an image's panels is changed.
usage: python tools/crop_figures.py"""
import os, shutil
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB = os.path.join(ROOT, 'figures', 'web')
ORIG = os.path.join(ROOT, 'figures', 'original')

# file: (pixels removed from the top, pixels removed from the bottom, what is removed)
CROPS = {
    'day-43.jpeg': (40, 0, 'the strip "MACHINE LEARNING FOR BIOLOGY - DAY 43"'),
    'day-44.jpeg': (37, 0, 'the strip "MACHINE LEARNING FOR BIOLOGY - DAY 44"'),
    'day-23.jpeg': (0, 29, 'the footer "Falk et al., Nature, 1991", which reads as the source of the chapter\'s own counts'),
    'day-24.jpeg': (0, 33, 'the footer "Correction to Day 16: repeat measurements are 3,377, not 6,455"'),
}

if __name__ == '__main__':
    os.makedirs(ORIG, exist_ok=True)
    for name, (top, bottom, what) in CROPS.items():
        src = os.path.join(ORIG, name)
        if not os.path.exists(src):
            shutil.copy2(os.path.join(WEB, name), src)
        im = Image.open(src)
        w, h = im.size
        out = im.crop((0, top, w, h - bottom))
        kw = {'quality': 92, 'subsampling': 0} if name.lower().endswith(('.jpg', '.jpeg')) else {}
        out.save(os.path.join(WEB, name), **kw)
        print(f'{name}: {w}x{h} -> {out.size[0]}x{out.size[1]}, removed {what}')
