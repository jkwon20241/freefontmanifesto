import json, sys, shutil, os
D=sys.argv[1]; V=sys.argv[2]
S=json.load(open('svgs.json')); t=open('template.html').read()
nav=[("intro","","Introduction"),("q1","*","What is a free font?"),("specimens","","Specimens"),("q2","**","Should all fonts be free?"),("q3","***","What makes a typeface “good”?"),("q4","****","Is a typeface a meaningful gift to&nbsp;humanity?"),("conclusion","","Conclusion"),("colophon","","Colophon")]
navh='<ol class="contents">'+''.join(f'<li><a href="#{i}">'+(f'<span class="m">{m}</span>' if m else '')+f'{l}</a></li>' for i,m,l in nav)+'</ol>'
pairs=[("gtamerica","GT America","Grilli Type","A broad family that bridges American Gothic and European neo-grotesque traditions, with multiple widths and weights.",
        "Inter","Inter","Google Fonts","A screen-oriented sans-serif with strong legibility and a practical range of weights."),
       ("untitledserif","Untitled Serif","Klim Type Foundry","An understated old-style serif inspired by traditional metal-foundry workhorses.",
        "EB Garamond","EB Garamond","Georg Duffner","A revival of a sixteenth-century Garamond design, with a more historically rooted and calligraphic character."),
       ("sohnemono","Söhne Mono","Klim Type Foundry","A polished monospace family with a range of weights and matching italics, suitable for technical and editorial design.",
        "JetBrains Mono","JetBrains Mono","JetBrains","A monospace typeface designed for coding, with distinctive forms intended to improve character recognition."),
       ("gtwalsheim","GT Walsheim","Grilli Type","A geometric sans-serif with a distinctive, rounded construction and a strong contemporary graphic-design presence.",
        "Poppins","Poppins","Indian Type Foundry","A geometric sans-serif built around near-circular forms and relatively uniform strokes.")]
ph=''
for k,cn,cf,cd,fam,on,of,od in pairs:
    ph+=f'''<div class="pair">
  <figure class="spec"><img src="img/{k}.svg?v={V}" width="400" height="358" alt="{cn} by {cf}: the word FREE struck through, then its alphabet and numerals" loading="lazy"><figcaption class="cap"><b>Premium</b>{cd}</figcaption></figure>
  <figure class="spec"><div class="live" style="font-family:'{fam}'"><p class="free">FREE</p><p class="name" style="font-family:'{fam}'">{on}</p><p class="foundry">{of}</p><p class="alpha">Aa Bb Cc Dd Ee<br>Ff Gg Hh Ii Jj Kk<br>Ll Mm Nn Oo Pp<br>Qq Rr Ss Tt Uu<br>Vv Ww Xx Yy Zz</p><p class="nums">0123456789</p></div><figcaption class="cap"><b>Open source</b>{od}</figcaption></figure>
</div>'''
out=t.replace('{{NAV}}',navh).replace('{{PAIRS}}',ph).replace('{{HERO_D}}',S['hero_d']).replace('{{HERO_M}}',S['hero_m']).replace('{{BACK_D}}',S['back_d']).replace('{{BACK_M}}',S['back_m']).replace('{{ASTER}}',S['aster']).replace('{{V}}',V)
open(os.path.join(D,'index.html'),'w').write(out)
for f in ('style.css','app.js'): shutil.copy(f,D)
for f in os.listdir('site/img'): shutil.copy('site/img/'+f,os.path.join(D,'img'))
for f in ('gen_site.py','outline.py','build.py','template.html'): shutil.copy(f,os.path.join(D,'tools'))
print('built',len(out))
