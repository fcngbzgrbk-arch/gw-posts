"""Gerador de artes GW Fotovoltaica — visual aprovado no Claude Design (09/10/2026).
Foto no topo, painel escuro com cantos arredondados embaixo, selo, logo, titulo,
numeros em caixas e chamada para o WhatsApp.
Uso: python3 arte.py spec.json posts/AAAA-MM-DD/arte  -> arte_feed.jpg + arte_story.jpg
Campos do spec: foto, selo, kicker, titulo, destaque, sub, stats, placas, cta, tsize, fy, acento
"""
import sys, json, os
ROOT = os.path.dirname(os.path.abspath(__file__))
from PIL import Image, ImageOps, ImageDraw, ImageFont
F = os.path.join(ROOT, 'assets', 'fonts', 'Poppins-')
def font(w, s): return ImageFont.truetype(F + w + '.ttf', s)

DARK = (8, 24, 18); GREEN = (34, 197, 94); YELLOW = (250, 204, 21); WHITE = (255, 255, 255)
SOFT = (212, 230, 218); MUTED = (190, 220, 200); CARD = (18, 41, 31)
TARIFA = 0.89; KWH_POR_PLACA = 75
WHATS = '(17) 99671-7575'

def cover(im, W, H, fy=0.5):
    r = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * r) + 1, int(im.height * r) + 1), Image.LANCZOS)
    x = (im.width - W) // 2; y = int((im.height - H) * fy)
    return im.crop((x, y, x + W, y + H))

def wrap(d, text, f, maxw):
    out = []
    for para in text.split('\n'):
        line = ''
        for w in para.split():
            t = (line + ' ' + w).strip()
            if d.textlength(t, font=f) <= maxw: line = t
            else: out.append(line); line = w
        out.append(line)
    return out

def fmt(n): return f'{n:,.0f}'.replace(',', '.')

def auto_stats(spec):
    if spec.get('placas') and not spec.get('stats'):
        p = spec['placas']; k = p * KWH_POR_PLACA
        spec['stats'] = [[str(p), 'placas'], [fmt(k), 'kWh/mês'], ['R$ ' + fmt(int(k * TARIFA + 0.5)), 'de energia/mês']]
    return spec

LOGO = Image.open(os.path.join(ROOT, 'assets', 'logo_branco.png')).convert('RGBA')

def render(spec, W, H, out):
    spec = auto_stats(dict(spec))
    story = H > 1500
    acc = tuple(spec['acento']) if spec.get('acento') else GREEN
    pad = 72 if story else 64
    safe_top = 250 if story else 40          # zona segura do story
    safe_bot = 260 if story else 56
    maxw = W - 2 * pad

    fp = spec['foto'] if os.path.isabs(spec['foto']) else os.path.join(ROOT, spec['foto'])
    im = ImageOps.exif_transpose(Image.open(fp)).convert('RGB')
    tmp = ImageDraw.Draw(Image.new('RGB', (10, 10)))

    # ---- medir o painel ----
    f_kick = font('Bold', 28 if story else 26)
    f_tit = font('Bold', spec.get('tsize', 76 if story else 66))
    f_sub = font('Medium', 34 if story else 31)
    lh_t = int(f_tit.size * 1.1); lh_s = int(f_sub.size * 1.42)
    tit = wrap(tmp, spec['titulo'], f_tit, maxw)
    sub = wrap(tmp, spec['sub'], f_sub, maxw) if spec.get('sub') else []
    gap = 28
    h = 0
    if spec.get('kicker'): h += 40 + 14
    h += len(tit) * lh_t
    if sub: h += gap + len(sub) * lh_s
    if spec.get('stats'): h += gap + 150
    cta_h = 104
    h += gap + 12 + cta_h
    panel_top = H - safe_bot - h - pad
    panel_top = min(panel_top, int(H * (0.62 if story else 0.64)))  # foto ocupa no maximo isso

    # ---- foto + painel ----
    photo_h = panel_top + 60
    base = Image.new('RGB', (W, H), DARK)
    base.paste(cover(im, W, photo_h, spec.get('fy', 0.5)), (0, 0))
    d = ImageDraw.Draw(base)
    r = 56 if story else 48
    d.rounded_rectangle([0, panel_top, W, H + r], radius=r, fill=DARK)

    # ---- selo (pilula escura com ponto) ----
    if spec.get('selo'):
        f_selo = font('Bold', 26); txt = spec['selo'].upper()
        tw = d.textlength(txt, font=f_selo)
        x0, y0 = 48, safe_top + 8
        d.rounded_rectangle([x0, y0, x0 + 26 + 14 + 12 + tw + 26, y0 + 60], radius=30, fill=DARK)
        d.ellipse([x0 + 26, y0 + 23, x0 + 40, y0 + 37], fill=acc)
        d.text((x0 + 52, y0 + 30), txt, font=f_selo, fill=WHITE, anchor='lm')

    # ---- logo (com fundo escuro discreto para leitura sobre a foto) ----
    lw = 220 if story else 200
    lg = LOGO.resize((lw, int(LOGO.height * lw / LOGO.width)), Image.LANCZOS)
    lx, ly = W - 48 - lw, safe_top
    plate = Image.new('RGBA', (lw + 36, lg.height + 28), (0, 0, 0, 0))
    ImageDraw.Draw(plate).rounded_rectangle([0, 0, plate.width - 1, plate.height - 1], radius=24, fill=DARK + (200,))
    base.paste(plate, (lx - 18, ly - 14), plate)
    base.paste(lg, (lx, ly), lg)

    # ---- texto do painel ----
    y = panel_top + pad
    if spec.get('kicker'):
        d.text((pad, y), spec['kicker'].upper(), font=f_kick, fill=acc); y += 40 + 14
    hi = spec.get('destaque')
    for l in tit:
        d.text((pad, y), l, font=f_tit, fill=YELLOW if hi and hi in l else WHITE); y += lh_t
    if sub:
        y += gap
        for l in sub: d.text((pad, y), l, font=f_sub, fill=SOFT); y += lh_s
    if spec.get('stats'):
        y += gap
        n = len(spec['stats']); g = 20; bw = (maxw - (n - 1) * g) // n
        for i, (v, k) in enumerate(spec['stats']):
            x = pad + i * (bw + g)
            d.rounded_rectangle([x, y, x + bw, y + 150], radius=24, outline=acc, width=3, fill=DARK)
            fv = font('Bold', 44)
            while d.textlength(v, font=fv) > bw - 40: fv = font('Bold', fv.size - 2)
            d.text((x + 28, y + 26), v, font=fv, fill=YELLOW)
            fk = font('Medium', 22)
            d.text((x + 28, y + 96), k, font=fk, fill=MUTED)
        y += 150

    # ---- CTA ----
    cy = H - safe_bot - cta_h
    d.rounded_rectangle([pad, cy, W - pad, cy + cta_h], radius=cta_h // 2, fill=acc)
    cta = spec.get('cta', 'Simule grátis · ' + WHATS)
    fc = font('Bold', 34)
    while d.textlength(cta, font=fc) > maxw - 60: fc = font('Bold', fc.size - 2)
    d.text((W / 2, cy + cta_h / 2), cta, font=fc, fill=DARK, anchor='mm')
    if not story:
        pass
    else:
        d.text((W / 2, cy + cta_h + 40), 'Rio Preto e região  •  7 anos de mercado', font=font('Medium', 26), fill=MUTED, anchor='mm')

    base.save(out, quality=90, optimize=True)

if __name__ == '__main__':
    spec = json.load(open(sys.argv[1])); o = sys.argv[2]
    render(spec, 1080, 1350, o + '_feed.jpg'); render(spec, 1080, 1920, o + '_story.jpg')
