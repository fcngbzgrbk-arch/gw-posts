"""Gerador de artes GW Fotovoltaica — estilo "título grande" aprovado pelo Maicon em 13/10/2026
(referência de estilo: perfis de energia solar com título condensado em duas cores sobre foto).
Foto real de obra em tela cheia, véu escuro, título enorme em Bebas Neue (branco + cor de destaque),
texto de apoio, números opcionais e rodapé com WhatsApp.

Uso: python3 arte.py spec.json posts/AAAA-MM-DD/arte  -> arte_feed.jpg + arte_story.jpg
Campos do spec:
  foto      caminho da foto (obrigatório)
  titulo    linhas separadas por \n; linha entre *asteriscos* sai na cor de destaque
  sub       texto de apoio (opcional)
  placas    nº de placas -> caixas com placas / kWh/mês / R$ de energia (opcional)
  stats     [[valor, rótulo], ...] no lugar de placas (opcional)
  selo      etiqueta pequena acima do título (ex.: "OBRA REAL") (opcional)
  layout    "topo" (padrão: véu de cima pra baixo, texto em cima) ou "esquerda" (véu lateral, texto à esquerda)
  acento    "amarelo" (padrão) ou "verde"
  rodape    texto à esquerda do rodapé (padrão: "Economia média de 80% · Rio Preto e região")
  fy        enquadramento vertical da foto 0–1 (padrão 0.5)
  tsize     tamanho do título em px no feed (padrão 132; o gerador reduz se não couber)
"""
import sys, json, os
ROOT = os.path.dirname(os.path.abspath(__file__))
from PIL import Image, ImageOps, ImageDraw, ImageFont
FD = os.path.join(ROOT, 'assets', 'fonts')
def poppins(w, s): return ImageFont.truetype(os.path.join(FD, 'Poppins-' + w + '.ttf'), s)
def bebas(s): return ImageFont.truetype(os.path.join(FD, 'BebasNeue-Regular.ttf'), s)

DARK = (8, 24, 18); GREEN = (34, 197, 94); YELLOW = (250, 204, 21); WHITE = (255, 255, 255)
SOFT = (228, 240, 232); MUTED = (190, 220, 200)
TARIFA = 0.89; KWH_POR_PLACA = 75
WHATS = '(17) 99671-7575'
LOGO = Image.open(os.path.join(ROOT, 'assets', 'logo_branco.png')).convert('RGBA')

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

def veil(W, H, layout, story, text_end=None):
    """Máscara (L) do véu escuro: 255 = cor escura total."""
    m = Image.new('L', (W, H), 0); d = ImageDraw.Draw(m)
    if layout == 'esquerda':
        for x in range(W):
            t = x / W
            a = 245 if t < 0.45 else int(245 - (t - 0.45) / 0.55 * 215)
            d.line([(x, 0), (x, H)], fill=max(a, 30))
    else:
        solid = max(int(H * 0.32), (text_end or 0) + 40)
        top_end = min(H, solid + int(H * 0.22))
        for y in range(top_end):
            a = 238 if y < solid else int(238 * (1 - (y - solid) / (top_end - solid)))
            d.line([(0, y), (W, y)], fill=a)
    # rodapé sempre escurecido
    fh = 760 if story else 300
    for y in range(H - fh, H):
        t = min(1, (y - (H - fh)) / (fh * 0.6))
        a = int(235 * t)
        cur = m.getpixel((0, y))
        d.line([(0, y), (W, y)], fill=max(cur, a))
    return m

def render(spec, W, H, out):
    spec = auto_stats(dict(spec))
    story = H > 1500
    layout = spec.get('layout', 'topo')
    acc = GREEN if spec.get('acento') == 'verde' else YELLOW
    pad = 72 if story else 64
    safe_top = 250 if story else 56
    safe_bot = 260 if story else 64

    fp = spec['foto'] if os.path.isabs(spec['foto']) else os.path.join(ROOT, spec['foto'])
    im = ImageOps.exif_transpose(Image.open(fp)).convert('RGB')
    photo = cover(im, W, H, spec.get('fy', 0.5))
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))   # logo + texto de cima (aplicado sobre foto+véu depois)
    d = ImageDraw.Draw(layer)

    # logo (topo direito no layout "topo", topo esquerdo no "esquerda")
    lw = 190 if story else 170
    lg = LOGO.resize((lw, int(LOGO.height * lw / LOGO.width)), Image.LANCZOS)
    lx = pad if layout == 'esquerda' else W - pad - lw
    layer.alpha_composite(lg, (lx, safe_top))

    text_w = (760 if layout == 'esquerda' else 800) if not story else 860
    # título
    raw = [l for l in spec['titulo'].split('\n') if l.strip()]
    lines = [(l.strip('*').upper(), l.startswith('*')) for l in raw]
    ts = spec.get('tsize', 132) * (1.12 if story else 1)
    ft = bebas(int(ts))
    while max(d.textlength(t, font=ft) for t, _ in lines) > text_w and ft.size > 70:
        ft = bebas(ft.size - 4)
    lh = int(ft.size * 0.92)

    # bloco de cima
    if layout == 'esquerda':
        y = int(H * 0.27) if not story else int(H * 0.30)
    else:
        y = safe_top + (lg.height + 40 if lw + 60 > W - text_w - pad else 20)
    if spec.get('selo'):
        fs = poppins('Bold', 26)
        d.text((pad, y), spec['selo'].upper(), font=fs, fill=GREEN if acc == YELLOW else YELLOW)
        y += 50
    for t, hi in lines:
        d.text((pad, y), t, font=ft, fill=acc if hi else WHITE)
        y += lh
    y += 26
    if spec.get('sub'):
        fsub = poppins('Medium', 34 if story else 30)
        for l in wrap(d, spec['sub'], fsub, text_w - 40):
            d.text((pad, y), l, font=fsub, fill=SOFT); y += int(fsub.size * 1.42)
    # agora que sabemos onde o texto termina: foto + véu, e o texto por cima
    base = Image.composite(Image.new('RGB', (W, H), DARK), photo, veil(W, H, layout, story, y)).convert('RGBA')
    base.alpha_composite(layer)
    base = base.convert('RGB')
    d = ImageDraw.Draw(base)

    # números (logo acima do rodapé)
    foot_y = H - safe_bot - 76
    if spec.get('stats'):
        n = len(spec['stats']); g = 18; bw = (W - 2 * pad - (n - 1) * g) // n; bh = 132
        sy = foot_y - 40 - bh
        for i, (v, k) in enumerate(spec['stats']):
            x = pad + i * (bw + g)
            d.rounded_rectangle([x, sy, x + bw, sy + bh], radius=22, fill=DARK, outline=acc, width=3)
            fv = bebas(70)
            while d.textlength(v, font=fv) > bw - 40: fv = bebas(fv.size - 4)
            d.text((x + 26, sy + 16), v, font=fv, fill=acc)
            d.text((x + 26, sy + 90), k, font=poppins('Medium', 22), fill=MUTED)

    # rodapé: texto + pílula com WhatsApp
    fpill = poppins('Bold', 28 if not story else 30)
    pw = d.textlength(WHATS, font=fpill) + 64
    d.rounded_rectangle([W - pad - pw, foot_y, W - pad, foot_y + 76], radius=38, fill=GREEN)
    d.text((W - pad - pw / 2, foot_y + 38), WHATS, font=fpill, fill=DARK, anchor='mm')
    rod = spec.get('rodape', 'Economia média de 80% · Rio Preto e região')
    fr = poppins('Medium', 24 if not story else 26)
    while d.textlength(rod, font=fr) > W - 2 * pad - pw - 24 and fr.size > 16: fr = poppins('Medium', fr.size - 1)
    d.text((pad, foot_y + 38), rod, font=fr, fill=SOFT, anchor='lm')

    base.save(out, quality=90, optimize=True)

if __name__ == '__main__':
    spec = json.load(open(sys.argv[1])); o = sys.argv[2]
    render(spec, 1080, 1350, o + '_feed.jpg'); render(spec, 1080, 1920, o + '_story.jpg')
