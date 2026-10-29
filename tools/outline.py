import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
F=os.path.expanduser('~/Library/Fonts/'); _c={}
def font(n):
    if n not in _c: _c[n]=TTFont(F+n)
    return _c[n]
def outline(fn,text,size,tracking=0.0,x0=0,baseline=0):
    f=font(fn); gs=f.getGlyphSet(); cmap=f.getBestCmap(); upm=f['head'].unitsPerEm; s=size/upm
    pen=SVGPathPen(gs); x=x0
    for ch in text:
        g=cmap.get(ord(ch))
        if g is None: x+=size*0.3; continue
        gs[g].draw(TransformPen(pen,(s,0,0,-s,x,baseline))); x+=gs[g].width*s+tracking*size
    return pen.getCommands(), x-x0
