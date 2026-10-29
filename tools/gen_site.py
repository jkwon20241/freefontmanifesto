import re, random, json, os
from outline import outline
R=lambda d: re.sub(r'-?\d+\.\d+', lambda m: ('%.1f'%float(m.group())).rstrip('0').rstrip('.'), d)
AST=[(17.1,44),(25.3,32.1),(33.4,44),(45.1,36),(36.7,25.5),(50.6,21.7),(46.4,8.6),(32.1,13.6),(32.7,0),(17.8,0),(18.6,13.6),(4.2,8.6),(0,21.8),(14,25.5),(5.5,35.9)]
def ast_path(x,y,w):
    s=w/50.6; return 'M'+' L'.join(f'{x+px*s:.1f} {y+py*s:.1f}' for px,py in AST)+'Z'
AW=18  # one asterisk size across every glyph field
def field(w,h,avoid,size,seed,flowers,margin,n=47):
    random.seed(seed); L=list("loremipsumdolorsitametconsecteturadipiscingelit")[:n]; random.shuffle(L)
    pts=[]; t=0; mind=size*1.15
    while len(pts)<len(L)+flowers and t<60000:
        t+=1; x=random.uniform(margin,w-margin-size*0.7); y=random.uniform(margin+size*0.75,h-margin)
        if any(a[0]<x+size*0.8 and x<a[2] and a[1]<y and y-size*0.9<a[3] for a in avoid): continue
        if any((x-p[0])**2+(y-p[1])**2<mind*mind for p in pts): continue
        pts.append((x,y))
    out=[]
    for i,(x,y) in enumerate(pts):
        if i<len(L):
            d,wd=outline('ABCReproTrial-Black.otf',L[i],size,0,x,y); a=random.uniform(-6,6)
            out.append(f'<path class="g" d="{R(d)}" transform="rotate({a:.1f} {x+wd/2:.1f} {y-size*0.3:.1f})"/>')
        else:
            r=size*0.2; cx,cy=x+8,y-size*0.35; w=AW; hh=w*44/50.6
            out.append(f'<path class="a" d="{ast_path(cx-w/2,cy-hh/2,w)}"/>')
    return out
def svg(W,H,body,cls,label=None):
    return f'<svg xmlns="http://www.w3.org/2000/svg" class="{cls}" viewBox="0 0 {W} {H}" width="{W}" height="{H}" preserveAspectRatio="xMidYMid meet" style="aspect-ratio:{W}/{H}" aria-hidden="true" focusable="false">{body}</svg>'
def hero(W,H,m,szF,bF,bO,bM,gsz,seed,fl,extra=()):
    dF,wF=outline('ABCReproTrial-Black.otf','FREE',szF,-0.01,m,bF)
    dO,wO=outline('ABCReproTrial-Black.otf','FONT',szF,-0.01,m,bO)
    _,w0=outline('ABCReproTrial-Black.otf','MANIFESTO',100,-0.01); sz=100*(W-2*m)/w0
    dM,_=outline('ABCReproTrial-Black.otf','MANIFESTO',sz,-0.01,m,bM)
    cap=0.74
    av=[(m-8,bF-szF*cap-8,m+wF+12,bF+12),(m-8,bO-szF*cap-8,m+wO+12,bO+12),(m-8,bM-sz*cap-8,W-m+8,H)]
    g=field(W,H,av,gsz,seed,fl,m)
    for (x,y,w) in extra: g.append(f'<path class="a" d="{ast_path(x+(w-AW)/2,y+(w-AW)*44/50.6/2,AW)}"/>')
    return f'<g class="glyphs">{"".join(g)}</g><path class="ink" d="{R(dF)}"/><path class="ink" d="{R(dO)}"/><path class="red" d="{R(dM)}"/>'
OUT={}
OUT['hero_d']=svg(1088,760,hero(1088,760,64,230,380,570,712,52,11,9),'field cover hero-d')
mob_extra=[(68,30,14.6),(302,174,14.6),(194,150,14.6),(398,198,14.6),(308,402,14.6),(116,144,14.6)]
OUT['hero_m']=svg(440,560,hero(440,560,24,104,300,392,476,34,5,6,mob_extra),'field cover hero-m')
OUT['back_d']=svg(1088,280,'<g class="glyphs">'+''.join(field(1088,280,[],44,23,6,40))+'</g>','field end back-d')
OUT['back_m']=svg(440,300,'<g class="glyphs">'+''.join(field(440,300,[],34,31,4,20,n=24))+'</g>','field end back-m')
d,wa=outline('ABCReproTrial-Black.otf','*',260,0,0,250)
OUT['aster']=f'<svg xmlns="http://www.w3.org/2000/svg" class="colo-mark" width="{int(wa)+6}" height="200" viewBox="0 0 {int(wa)+6} 200" aria-hidden="true" focusable="false"><path d="{R(d)}" fill="none" stroke="#D7262C" stroke-width="2"/></svg>'
# commercial specimen cards (outlined from the real trial fonts)
cards=[('gtamerica','GT America','Grilli Type','GT-America-Standard-Bold-Trial.otf','GT-America-Standard-Medium-Trial.otf'),
 ('untitledserif','Untitled Serif','Klim Type Foundry','TestUntitledSerif-Bold.otf','TestUntitledSerif-Medium.otf'),
 ('sohnemono','Söhne Mono','Klim Type Foundry','TestSöhneMono-Fett.otf','TestSöhneMono-Buch.otf'),
 ('gtwalsheim','GT Walsheim','Grilli Type','GT-Walsheim-Bold-Trial.otf','GT-Walsheim-Medium-Trial.otf')]
spec=['Aa Bb Cc Dd Ee','Ff Gg Hh Ii Jj Kk','Ll Mm Nn Oo Pp','Qq Rr Ss Tt Uu','Vv Ww Xx Yy Zz']
os.makedirs('site/img',exist_ok=True)
for key,name,fd,bold,med in cards:
    b=''; d,wF=outline(bold,'FREE',64,0,0,54); b+=f'<path d="{R(d)}" fill="#8C8C8C"/>'
    b+=f'<rect x="-2" y="{54-64*0.36:.1f}" width="{wF+4:.1f}" height="{64*0.07:.1f}" fill="#8C8C8C"/>'
    d,_=outline(bold,name,16,0,0,92); b+=f'<path d="{R(d)}" fill="#D7262C"/>'
    d,_=outline(bold,fd,16,0,0,114); b+=f'<path d="{R(d)}" fill="#111"/>'
    y=162
    for ln in spec+['','0123456789']:
        if ln: d,_=outline(med,ln,24,0,0,y); b+=f'<path d="{R(d)}" fill="#111"/>'
        y+=30
    open(f'site/img/{key}.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-4 0 304 {y-14}" width="304" height="{y-14}">{b}</svg>')
json.dump(OUT,open('svgs.json','w'))
print({k:len(v) for k,v in OUT.items()}, [k for k,*_ in cards])
