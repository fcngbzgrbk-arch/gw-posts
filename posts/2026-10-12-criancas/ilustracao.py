"""Gera a arte do Dia das Criancas (ilustracao familia + casa com energia solar).
Saidas: render HTML (feed/story) para PNG via Playwright e artboards .dc.html para o Claude Design."""
import os, sys
ROOT = '/home/claude/gw-posts'
OUT = os.path.dirname(os.path.abspath(__file__))

def person(x, ground, h, skin, shirt, pants, hair, arms='down', girl=False):
    head = h * 0.13; bw = h * 0.30; bh = h * 0.36; lh = h * 0.40
    top = ground - h
    hy = top + head
    by = hy + head * 0.9
    ly = by + bh - 6
    s = []
    # legs
    s.append(f'<rect x="{x-bw*0.36:.0f}" y="{ly:.0f}" width="{bw*0.28:.0f}" height="{lh:.0f}" rx="{bw*0.12:.0f}" fill="{pants}"/>')
    s.append(f'<rect x="{x+bw*0.08:.0f}" y="{ly:.0f}" width="{bw*0.28:.0f}" height="{lh:.0f}" rx="{bw*0.12:.0f}" fill="{pants}"/>')
    # arms
    if arms == 'up':
        s.append(f'<path d="M{x+bw*0.4:.0f} {by+12:.0f} L{x+bw*0.95:.0f} {by-h*0.22:.0f}" stroke="{skin}" stroke-width="{bw*0.2:.0f}" stroke-linecap="round"/>')
        s.append(f'<path d="M{x-bw*0.4:.0f} {by+12:.0f} L{x-bw*0.75:.0f} {by+bh*0.7:.0f}" stroke="{skin}" stroke-width="{bw*0.2:.0f}" stroke-linecap="round"/>')
    elif arms == 'wave':
        s.append(f'<path d="M{x+bw*0.4:.0f} {by+12:.0f} L{x+bw*0.9:.0f} {by-h*0.12:.0f}" stroke="{skin}" stroke-width="{bw*0.2:.0f}" stroke-linecap="round"/>')
        s.append(f'<path d="M{x-bw*0.4:.0f} {by+12:.0f} L{x-bw*0.62:.0f} {by+bh*0.75:.0f}" stroke="{skin}" stroke-width="{bw*0.2:.0f}" stroke-linecap="round"/>')
    else:
        for sgn in (-1, 1):
            s.append(f'<path d="M{x+sgn*bw*0.4:.0f} {by+12:.0f} L{x+sgn*bw*0.62:.0f} {by+bh*0.8:.0f}" stroke="{skin}" stroke-width="{bw*0.2:.0f}" stroke-linecap="round"/>')
    # body
    if girl:
        s.append(f'<path d="M{x-bw*0.42:.0f} {by:.0f} Q{x:.0f} {by-10:.0f} {x+bw*0.42:.0f} {by:.0f} L{x+bw*0.62:.0f} {by+bh+8:.0f} L{x-bw*0.62:.0f} {by+bh+8:.0f} Z" fill="{shirt}"/>')
    else:
        s.append(f'<rect x="{x-bw/2:.0f}" y="{by:.0f}" width="{bw:.0f}" height="{bh:.0f}" rx="{bw*0.3:.0f}" fill="{shirt}"/>')
    # head + hair
    s.append(f'<circle cx="{x:.0f}" cy="{hy:.0f}" r="{head:.0f}" fill="{skin}"/>')
    if girl:
        s.append(f'<path d="M{x-head*1.05:.0f} {hy+head*0.9:.0f} Q{x-head*1.3:.0f} {hy-head*1.3:.0f} {x:.0f} {hy-head*1.08:.0f} Q{x+head*1.3:.0f} {hy-head*1.3:.0f} {x+head*1.05:.0f} {hy+head*0.9:.0f} Q{x+head*0.8:.0f} {hy-head*0.2:.0f} {x:.0f} {hy-head*0.55:.0f} Q{x-head*0.8:.0f} {hy-head*0.2:.0f} {x-head*1.05:.0f} {hy+head*0.9:.0f} Z" fill="{hair}"/>')
    else:
        s.append(f'<path d="M{x-head:.0f} {hy-head*0.05:.0f} Q{x-head:.0f} {hy-head*1.15:.0f} {x:.0f} {hy-head*1.1:.0f} Q{x+head:.0f} {hy-head*1.15:.0f} {x+head:.0f} {hy-head*0.05:.0f} Q{x:.0f} {hy-head*0.6:.0f} {x-head:.0f} {hy-head*0.05:.0f} Z" fill="{hair}"/>')
    # smile
    s.append(f'<path d="M{x-head*0.35:.0f} {hy+head*0.3:.0f} Q{x:.0f} {hy+head*0.6:.0f} {x+head*0.35:.0f} {hy+head*0.3:.0f}" stroke="#7A3E1D" stroke-width="3" fill="none" stroke-linecap="round"/>')
    return '\n'.join(s)

def scene():
    W, H = 1080, 900
    g = []
    g.append(f'<rect width="{W}" height="{H}" fill="#BEE6FB"/>')
    # sun
    g.append('<g transform="translate(180 170)">' + ''.join(
        f'<rect x="-8" y="-150" width="16" height="44" rx="8" fill="#FACC15" transform="rotate({a})"/>' for a in range(0, 360, 30)) +
        '<circle r="88" fill="#FACC15"/><circle r="70" fill="#FDE047"/></g>')
    # clouds
    for cx, cy, sc in [(470, 110, 0.9), (930, 330, 0.7)]:
        g.append(f'<g transform="translate({cx} {cy}) scale({sc})" fill="#FFFFFF"><ellipse cx="0" cy="20" rx="90" ry="34"/><circle cx="-34" cy="0" r="40"/><circle cx="26" cy="-10" r="50"/></g>')
    # sun rays hitting panels (light beams)
    g.append('<path d="M250 230 L470 360" stroke="#FDE047" stroke-width="6" stroke-dasharray="4 16" stroke-linecap="round"/>')
    g.append('<path d="M270 200 L560 330" stroke="#FDE047" stroke-width="6" stroke-dasharray="4 16" stroke-linecap="round"/>')
    # hills
    g.append('<path d="M0 640 Q270 560 560 620 T1080 600 L1080 900 L0 900 Z" fill="#86D46B"/>')
    g.append('<path d="M0 720 Q300 680 600 715 T1080 705 L1080 900 L0 900 Z" fill="#5DBB4A"/>')
    # tree
    g.append('<rect x="890" y="520" width="34" height="200" rx="10" fill="#8B5A2B"/><circle cx="907" cy="480" r="92" fill="#3FA34D"/><circle cx="860" cy="520" r="60" fill="#4CB35A"/><circle cx="955" cy="520" r="60" fill="#4CB35A"/>')
    # house
    g.append('<rect x="400" y="470" width="400" height="250" fill="#FFF4E0"/>')
    g.append('<rect x="400" y="470" width="400" height="18" fill="#F3E2C3"/>')
    g.append('<polygon points="360,485 455,320 745,320 840,485" fill="#B9461B"/>')
    # solar panels on roof plane
    rows = [(336, 476, 724), (378, 452, 748), (420, 428, 772)]
    for y, x0, x1 in rows:
        n = 6; gap = 6; w = (x1 - x0 - 30 - gap * (n - 1)) / n
        for i in range(n):
            x = x0 + 15 + i * (w + gap)
            g.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="36" rx="3" fill="#1E3A8A" stroke="#93C5FD" stroke-width="2"/>')
            g.append(f'<line x1="{x+w/2:.1f}" y1="{y+2}" x2="{x+w/2:.1f}" y2="{y+34}" stroke="#3B5BB5" stroke-width="2"/>')
            g.append(f'<line x1="{x+2:.1f}" y1="{y+18}" x2="{x+w-2:.1f}" y2="{y+18}" stroke="#3B5BB5" stroke-width="2"/>')
    # door + windows
    g.append('<rect x="565" y="575" width="74" height="145" rx="8" fill="#22C55E"/><circle cx="625" cy="650" r="5" fill="#FACC15"/>')
    for wx in (440, 690):
        g.append(f'<rect x="{wx}" y="540" width="76" height="70" rx="6" fill="#FDE68A" stroke="#FFFFFF" stroke-width="8"/><line x1="{wx+38}" y1="540" x2="{wx+38}" y2="610" stroke="#FFFFFF" stroke-width="5"/>')
    # path
    g.append('<path d="M565 720 L639 720 L690 900 L520 900 Z" fill="#E9D9B4"/>')
    # kite
    g.append('<path d="M760 760 Q800 450 720 250" stroke="#6B7280" stroke-width="3" fill="none"/>')
    g.append('<g transform="translate(720 215) rotate(-12)"><polygon points="0,-60 42,0 0,70 -42,0" fill="#EF4444"/><polygon points="0,-60 42,0 0,0" fill="#FACC15"/><polygon points="0,0 -42,0 0,70" fill="#22C55E"/><path d="M0 70 q-14 30 6 50 q18 22 -4 46" stroke="#EF4444" stroke-width="4" fill="none"/></g>')
    # family (front-left) + kid with kite (right)
    g.append(person(150, 790, 300, '#C68642', '#2563EB', '#1F2937', '#2B1B12', arms='wave'))
    g.append(person(250, 790, 280, '#F1C27D', '#F97316', '#1E3A8A', '#6B3E26', girl=True))
    g.append(person(335, 792, 170, '#E0AC69', '#FACC15', '#2563EB', '#3B2416', arms='up', girl=True))
    g.append(person(760, 792, 185, '#C68642', '#22C55E', '#1F2937', '#2B1B12', arms='up'))
    return f'<svg viewBox="0 0 {W} {H}" width="1080" height="{H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Ilustração de família em frente a uma casa com placas solares, criança soltando pipa">' + '\n'.join(g) + '</svg>'

SVG = scene()

def body(W, H, logo_src, story):
    pad = 72 if story else 64
    top = 250 if story else 40
    scene_h = 1150 if story else 860
    panel_top = scene_h - 50
    bottom_pad = 260 if story else 56
    title = 84 if story else 72
    sub = 36 if story else 32
    return f'''<div style="width: {W}px; height: {H}px; position: relative; overflow: hidden; background: #081812; font-family: Poppins, sans-serif; color: #FFFFFF">
<div style="position: absolute; top: 0; left: 0; width: 1080px; height: {scene_h}px; overflow: hidden; background: #BEE6FB">
<div style="position: absolute; left: 0; bottom: 0; width: 1080px; height: 900px; transform-origin: bottom center; transform: none">{SVG}</div>
</div>
<div style="position: absolute; top: {top+8}px; left: 48px; display: flex; align-items: center; gap: 12px; background: #081812; padding: 14px 26px; border-radius: 999px">
<div style="width: 14px; height: 14px; border-radius: 999px; background: #FACC15"></div>
<span style="font-size: 26px; font-weight: 700; letter-spacing: 2px">DIA DAS CRIANÇAS</span>
</div>
<div style="position: absolute; top: {top}px; right: 30px; background: rgba(8,24,18,0.8); border-radius: 24px; padding: 14px 18px">
<img src="{logo_src}" alt="GW Fotovoltaica" style="display: block; width: {220 if story else 200}px; height: auto">
</div>
<div style="position: absolute; top: {panel_top}px; left: 0; width: 1080px; height: {H-panel_top+60}px; background: #081812; border-radius: 52px 52px 0 0; box-sizing: border-box; padding: {pad}px {pad}px 0; display: flex; flex-direction: column; gap: 22px">
<span style="font-size: 26px; font-weight: 700; letter-spacing: 3px; color: #FACC15">12 DE OUTUBRO</span>
<h1 style="margin: 0; font-size: {title}px; line-height: 1.05; font-weight: 700">Feliz Dia das <span style="color: #FACC15">Crianças!</span></h1>
<p style="margin: 0; font-size: {sub}px; line-height: 1.4; color: #D4E6DA">Energia limpa hoje é um planeta melhor para eles amanhã.</p>
</div>
<div style="position: absolute; left: {pad}px; right: {pad}px; bottom: {bottom_pad}px; height: 104px; border-radius: 999px; background: #FACC15; color: #081812; display: flex; align-items: center; justify-content: center">
<span style="font-size: 34px; font-weight: 700">Simule grátis · (17) 99671-7575</span>
</div>
</div>'''

FONTS = f'''@font-face{{font-family:Poppins;font-weight:500;src:url(file://{ROOT}/assets/fonts/Poppins-Medium.ttf)}}
@font-face{{font-family:Poppins;font-weight:700;src:url(file://{ROOT}/assets/fonts/Poppins-Bold.ttf)}}'''

def plain(W, H, story):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{FONTS} body{{margin:0}}</style></head><body>{body(W,H,"file://"+ROOT+"/assets/logo_branco.png",story)}</body></html>'

def dc(W, H, story, logo_blob):
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>Dia das Crianças — {'Story' if story else 'Feed'}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;700&amp;display=swap">
<style>
body{{margin:0}}
a{{color:#22C55E}}a:hover{{color:#FACC15}}
</style>
</helmet>
{body(W,H,logo_blob,story)}
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{W},"height":{H}}}}}'>
class Component extends DCLogic {{
renderVals() {{
return {{}};
}}
}}
</script>
</body>
</html>
'''

if __name__ == '__main__':
    from playwright.sync_api import sync_playwright
    dest = sys.argv[1]
    os.makedirs(dest, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        for name, W, H, story in [('arte_feed', 1080, 1350, False), ('arte_story', 1080, 1920, True)]:
            f = os.path.join(OUT, name + '.html'); open(f, 'w').write(plain(W, H, story))
            pg = b.new_page(viewport={'width': W, 'height': H})
            pg.goto('file://' + f); pg.wait_for_timeout(400)
            pg.screenshot(path=os.path.join(dest, name + '.png'))
        b.close()
    d = os.path.join(OUT, '..', 'design', 'project')
    open(os.path.join(d, 'Criancas.dc.html'), 'w').write(dc(1080, 1350, False, '/_blob/a24c0336c5905f4c40fca1973e728f60'))
    open(os.path.join(d, 'CriancasStory.dc.html'), 'w').write(dc(1080, 1920, True, '/_blob/a24c0336c5905f4c40fca1973e728f60'))
