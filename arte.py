import sys, json, os
ROOT=os.path.dirname(os.path.abspath(__file__))
from PIL import Image, ImageOps, ImageDraw, ImageFilter, ImageFont
F=os.path.join(ROOT,'assets','fonts','Poppins-')
def font(w,s): return ImageFont.truetype(F+w+'.ttf',s)
DARK=(8,24,18); GREEN=(34,197,94); YELLOW=(250,204,21); WHITE=(255,255,255)

def cover(im,W,H,fy=0.5):
    r=max(W/im.width,H/im.height); im=im.resize((int(im.width*r)+1,int(im.height*r)+1),Image.LANCZOS)
    x=(im.width-W)//2; y=int((im.height-H)*fy); return im.crop((x,y,x+W,y+H))

def grad(W,H,start,alpha_max=245):
    g=Image.new('L',(1,H))
    for y in range(H):
        t=0 if y<start else min(1,(y-start)/(H-start)*2.0); g.putpixel((0,y),int(alpha_max*t))
    return g.resize((W,H))

def wrap(d,text,f,maxw):
    out=[]
    for para in text.split('\n'):
        line=''
        for w in para.split():
            t=(line+' '+w).strip()
            if d.textlength(t,font=f)<=maxw: line=t
            else: out.append(line); line=w
        out.append(line)
    return out

LOGO=Image.open(os.path.join(ROOT,'assets','logo_branco.png'))
def brand_img(base,h):
    lg=LOGO.resize((int(LOGO.width*h/LOGO.height),h),Image.LANCZOS)
    sh=Image.new('L',base.size,0); ImageDraw.Draw(sh).rounded_rectangle([30,24,50+lg.width+22,40+h+18],radius=28,fill=175)
    base.paste(Image.new('RGB',base.size,DARK),(0,0),sh.filter(ImageFilter.GaussianBlur(10)))
    base.paste(lg,(50,40),lg)
def brand(d,W,y,small=False):
    s=34 if not small else 28
    d.text((60,y),'GW',font=font('Bold',s+14),fill=GREEN)
    gx=60+d.textlength('GW',font=font('Bold',s+14))+12
    d.text((gx,y+10),'FOTOVOLTAICA',font=font('Bold',s-8),fill=WHITE)

TARIFA=0.89; KWH_POR_PLACA=75
def auto_stats(spec):
    if 'placas' in spec and not spec.get('stats'):
        p=spec['placas']; k=p*KWH_POR_PLACA
        fmt=lambda n:f'{n:,.0f}'.replace(',','.')
        spec['stats']=[[str(p),'placas'],[fmt(k),'kWh/mês'],['≈R$'+fmt(int(k*TARIFA+0.5)),'de energia/mês']]
    return spec
def render(spec,W,H,out):
    spec=auto_stats(spec)
    fp=spec['foto'] if os.path.isabs(spec['foto']) else os.path.join(ROOT,spec['foto'])
    im=ImageOps.exif_transpose(Image.open(fp)).convert('RGB')
    base=cover(im,W,H,spec.get('fy',0.5))
    top=Image.new('RGB',(W,H),DARK)
    base=Image.composite(top,base,grad(W,H,int(H*0.28) if H<1500 else int(H*0.38)))
    # faixa superior suave
    tg=Image.new('L',(W,H),0); td=ImageDraw.Draw(tg)
    for y in range(320): td.line([(0,y),(W,y)],fill=int(200*(1-y/320)))
    base=Image.composite(top,base,tg)
    d=ImageDraw.Draw(base)
    brand_img(base,200 if H<1500 else 220)
    # selo
    tag=spec['selo']; ft=font('Bold',30); tw=d.textlength(tag,font=ft)
    d.rounded_rectangle([W-60-tw-44,52,W-60,52+58],radius=29,fill=YELLOW); d.text((W-60-tw-22,58),tag,font=ft,fill=DARK)
    # bloco de texto
    ft_=font('Bold',spec.get('tsize',74)); fs_=font('Medium',34)
    hb=(56 if spec.get('kicker') else 0)+len(wrap(d,spec['titulo'],ft_,W-120))*int(ft_.size*1.12)+18
    hb+=160 if spec.get('stats') else (len(wrap(d,spec.get('sub',''),fs_,W-120))*46+20 if spec.get('sub') else 0)
    y=H-(190 if H<1500 else 400)-hb
    if spec.get('kicker'):
        d.text((60,y),spec['kicker'].upper(),font=font('Bold',30),fill=GREEN); y+=56
    ft=font('Bold',spec.get('tsize',74))
    for l in wrap(d,spec['titulo'],ft,W-120):
        hi=spec.get('destaque')
        d.text((60,y),l,font=ft,fill=YELLOW if hi and hi in l else WHITE); y+=int(ft.size*1.12)
    y+=18
    if spec.get('stats'):
        bw=(W-120-2*20)//3
        for i,(v,k) in enumerate(spec['stats']):
            x=60+i*(bw+20)
            d.rounded_rectangle([x,y,x+bw,y+130],radius=20,fill=(12,40,28),outline=GREEN,width=3)
            d.text((x+bw/2,y+48),v,font=font('Bold',44),fill=WHITE,anchor='mm')
            d.text((x+bw/2,y+98),k,font=font('Medium',24),fill=(190,220,200),anchor='mm')
        y+=160
    elif spec.get('sub'):
        fs=font('Medium',34)
        for l in wrap(d,spec['sub'],fs,W-120): d.text((60,y),l,font=fs,fill=(220,235,225)); y+=46
        y+=20
    # rodape CTA
    fy=H-120 if H<1500 else H-330
    d.rounded_rectangle([60,fy,W-60,fy+76],radius=38,fill=GREEN)
    d.text((W/2,fy+38),spec.get('cta','Simule sua economia: (17) 99671-7575'),font=font('Bold',32),fill=DARK,anchor='mm')
    d.text((W/2,fy-30),'Rio Preto e região  •  7 anos de mercado',font=font('Medium',24),fill=(170,200,180),anchor='mm')
    base.save(out,quality=88,optimize=True)

if __name__=='__main__':
    spec=json.load(open(sys.argv[1])); o=sys.argv[2]
    render(spec,1080,1350,o+'_feed.jpg'); render(spec,1080,1920,o+'_story.jpg')
