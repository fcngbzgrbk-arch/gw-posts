"""Carrossel GW (Instagram, 1080x1350): capa com foto (arte.py) + slides internos no mesmo molde.
Uso: python3 carrossel.py spec.json pasta_saida
spec: {"capa": {...spec do arte.py...}, "slides": [{"num":"01","titulo":"linha\\n*destaque*","texto":"...","stats":[[v,k],...]}], "fim": {"titulo":"...","texto":"..."}}
"""
import sys, json, os
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import arte
W, H = 1080, 1350
DARK, GREEN, YELLOW, SOFT, MUTED = arte.DARK, arte.GREEN, arte.YELLOW, arte.SOFT, arte.MUTED
def base(i, n):
    im = Image.new('RGB', (W, H), DARK); d = ImageDraw.Draw(im)
    for y in range(H):  # leve degradê
        t = y / H; d.line([(0, y), (W, y)], fill=(int(8 + 6 * t), int(24 + 14 * t), int(18 + 8 * t)))
    lg = arte.LOGO.resize((130, int(arte.LOGO.height * 130 / arte.LOGO.width)))
    im.paste(lg, (W - 64 - 130, 56), lg)
    # barra de progresso
    seg = (W - 128 - 160) / n
    for k in range(n):
        x0 = 64 + k * seg
        d.rounded_rectangle([x0 + 4, 70, x0 + seg - 4, 80], radius=5, fill=YELLOW if k == i else (40, 70, 55))
    return im, d
def titulo(d, txt, y, size=120, maxw=W - 128):
    for l in [l for l in txt.split('\n') if l.strip()]:
        hl = l.startswith('*'); t = l.strip('*').upper(); f = arte.bebas(size)
        while d.textlength(t, font=f) > maxw and f.size > 60: f = arte.bebas(f.size - 4)
        d.text((64, y), t, font=f, fill=YELLOW if hl else (255, 255, 255)); y += int(f.size * 0.95)
    return y
def texto(d, txt, y, size=40):
    f = arte.poppins('Medium', size)
    for par in txt.split('\n'):
        for l in arte.wrap(d, par, f, W - 140):
            d.text((64, y), l, font=f, fill=SOFT); y += int(size * 1.45)
        y += 14
    return y
def rodape(d, txt='Arrasta para o lado  >>'):
    fp = arte.poppins('Bold', 28); pw = d.textlength(arte.WHATS, font=fp) + 64
    d.rounded_rectangle([W - 64 - pw, H - 140, W - 64, H - 64], radius=38, fill=GREEN)
    d.text((W - 64 - pw / 2, H - 102), arte.WHATS, font=fp, fill=DARK, anchor='mm')
    d.text((64, H - 102), txt, font=arte.poppins('Medium', 26), fill=MUTED, anchor='lm')
def render(spec, out):
    os.makedirs(out, exist_ok=True)
    arte.render(spec['capa'], W, H, f'{out}/slide01.jpg')
    arte.render(spec['capa'], 1080, 1920, f'{out}/arte_story.jpg')
    slides = spec['slides']; n = len(slides) + 2
    for i, s in enumerate(slides, start=1):
        im, d = base(i, n); y = 200
        if s.get('num'): d.text((64, y), s['num'], font=arte.bebas(200), fill=(34, 90, 60)); y += 190
        y = titulo(d, s['titulo'], y) + 30
        if s.get('texto'): y = texto(d, s['texto'], y)
        if s.get('stats'):
            sts = s['stats']; g = 18; bw = (W - 128 - (len(sts) - 1) * g) // len(sts); sy = max(y + 20, H - 360)
            for k, (v, lab) in enumerate(sts):
                x = 64 + k * (bw + g); d.rounded_rectangle([x, sy, x + bw, sy + 140], radius=22, fill=DARK, outline=YELLOW, width=3)
                fv = arte.bebas(72)
                while d.textlength(v, font=fv) > bw - 40: fv = arte.bebas(fv.size - 4)
                d.text((x + 24, sy + 16), v, font=fv, fill=YELLOW); d.text((x + 24, sy + 96), lab, font=arte.poppins('Medium', 22), fill=MUTED)
        if s.get('nota'): d.text((64, H - 190), s['nota'], font=arte.poppins('Medium', 22), fill=MUTED)
        rodape(d); im.save(f'{out}/slide{i+1:02d}.jpg', quality=90)
    im, d = base(n - 1, n); f = spec['fim']
    y = titulo(d, f['titulo'], 330, 140) + 40
    y = texto(d, f['texto'], y, 42)
    d.rounded_rectangle([64, y + 30, W - 64, y + 160], radius=65, fill=GREEN)
    d.text((W / 2, y + 95), 'WhatsApp ' + arte.WHATS, font=arte.poppins('Bold', 46), fill=DARK, anchor='mm')
    rodape(d, 'Economia média de 80% · Rio Preto e região'); im.save(f'{out}/slide{n:02d}.jpg', quality=90)
    # arte_feed = capa (usada no Facebook)
    Image.open(f'{out}/slide01.jpg').save(f'{out}/arte_feed.jpg', quality=90)
if __name__ == '__main__':
    render(json.load(open(sys.argv[1])), sys.argv[2])
