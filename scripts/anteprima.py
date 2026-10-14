# Costruisce l'anteprima navigabile da dist/ per la pubblicazione come artifact.
# - _astro -> assets (i percorsi con "_" sono riservati)
# - link e srcset resi relativi alla profondità di ogni pagina
# - solo le foto davvero usate; si tolgono le 1920 se si supera il limite di file
# - index: la home senza doctype/head/body (lo scheletro lo aggiunge la pubblicazione)
import os, re, shutil, glob, json
SRC = 'dist'; OUT = '../anteprima'
shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
pages = sorted(glob.glob(f'{SRC}/**/*.html', recursive=True))
html = {os.path.relpath(p, SRC): open(p, encoding='utf-8').read() for p in pages}
# quali file statici servono
used = set()
for s in html.values():
    for m in re.findall(r'(?:src|href|srcset)="([^"]+)"', s):
        for part in m.split(','):
            u = part.strip().split(' ')[0]
            if u.startswith('/') and not u.startswith('//'): used.add(u.split('#')[0].split('?')[0])
    for m in re.findall(r'url\((/[^)]+)\)', s): used.add(m)
for css in glob.glob(f'{SRC}/_astro/*.css'):
    for m in re.findall(r'url\((/[^)"\']+)\)', open(css).read()): used.add(m)
statici = sorted(u for u in used if os.path.isfile(SRC + u) and not u.endswith('.html'))
limite = 255 - len(html) - 5
togli1920 = len(statici) > limite
if togli1920: statici = [u for u in statici if not u.endswith('-1920.webp')]
print('pagine', len(html), '| file statici', len(statici), '| senza 1920:', togli1920)
PAGINE = {'/' + k[:-5] for k in html}  # es. /agriturismo, /bottega/pozzello, /index

def rel(url, depth):
    pre = '../' * depth if depth else './'
    u, frag = (url.split('#', 1) + [''])[:2]
    frag = '#' + frag if frag else ''
    if u == '/': return (pre + 'index.html' if depth else 'index.html') + frag
    if u.startswith('/_astro/'): u = '/assets/' + u[len('/_astro/'):]
    if u in PAGINE: u += '.html'
    return pre + u.lstrip('/') + frag

def conv(s, depth):
    if togli1920: s = re.sub(r',\s*/img/web/[^" ,]+-1920\.webp 1920w', '', s)
    s = re.sub(r'(src|href)="(/[^/"][^"]*|/)"', lambda m: f'{m.group(1)}="{rel(m.group(2), depth)}"', s)
    s = re.sub(r'srcset="([^"]+)"', lambda m: 'srcset="' + ', '.join(
        (rel(p.strip().split(' ')[0], depth) + ' ' + ' '.join(p.strip().split(' ')[1:])).strip() for p in m.group(1).split(',')) + '"', s)
    s = re.sub(r'url\(/_astro/', 'url(' + ('../' * depth if depth else './') + 'assets/', s)
    # torna in alto al caricamento (l'anteprima conserva lo scorrimento tra una pagina e l'altra)
    s = s.replace('</body>', '<script>addEventListener("load",()=>{if(!location.hash)scrollTo(0,0)})</script></body>')
    return s

files = {}
for k, s in html.items():
    depth = k.count('/')
    s = conv(s, depth)
    if k == 'index.html':
        head = re.search(r'<head>(.*?)</head>', s, re.S).group(1)
        head = re.sub(r'<meta charset[^>]*>|<meta name="viewport"[^>]*>', '', head)
        body = re.search(r'<body[^>]*>(.*)</body>', s, re.S).group(1)
        s = head + body
    dst = os.path.join(OUT, k); os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst, 'w', encoding='utf-8').write(s)
    if k != 'index.html': files[k] = k
for u in statici:
    d = u.lstrip('/')
    if d.startswith('_astro/'): d = 'assets/' + d[len('_astro/'):]
    dst = os.path.join(OUT, d); os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy(SRC + u, dst)
    if d.endswith('.css'):
        c = open(dst).read()
        c = c.replace('url(/_astro/', 'url(./')  # i font stanno nella stessa cartella assets
        open(dst, 'w').write(c)
    files[d] = d
json.dump(files, open(os.path.join(OUT, '_files.json'), 'w'), indent=0)
print('totale file da pubblicare:', len(files) + 1)
