import sys, os, subprocess
from playwright.sync_api import sync_playwright
here=os.path.dirname(os.path.abspath(__file__))
mode=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1920})
    pg.goto('file://'+here+'/reel.html'); pg.wait_for_timeout(800)
    total=pg.evaluate('TOTAL')
    if mode=='test':
        for t in [0.4,2.0,3.6,6.0,8.5,21.5,T if (T:=total-1) else 0]:
            pg.evaluate(f'render({t})'); pg.screenshot(path=f'{here}/test_{t:.1f}.jpg',type='jpeg',quality=70)
    else:
        fps=30; os.makedirs(here+'/frames',exist_ok=True); n=int(total*fps)
        for i in range(n):
            pg.evaluate(f'render({i/fps})'); pg.screenshot(path=f'{here}/frames/f{i:05d}.jpg',type='jpeg',quality=90)
        print('frames',n,total)
    b.close()
