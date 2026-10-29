import os,sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
R='/home/claude/gw-posts'; D=R+'/posts/obra-11placas'
FD=R+'/assets/fonts'
def pop(w,s): return ImageFont.truetype(f'{FD}/Poppins-{w}.ttf',s)
def beb(s): return ImageFont.truetype(f'{FD}/BebasNeue-Regular.ttf',s)
DARK=(8,24,18); GREEN=(34,197,94); YELLOW=(250,204,21); WHITE=(255,255,255); SOFT=(228,240,232); MUTED=(190,220,200)
logo=Image.open(R+'/assets/logo_branco.png').convert('RGBA')
cima=Image.open(D+'/foto_cima.png').convert('RGB')
frente=Image.open(D+'/foto_frente.png').convert('RGB')
# desfoca a frente dos carros (privacidade de placa)
for box in []:
    reg=frente.crop(box).filter(ImageFilter.GaussianBlur(6)); frente.paste(reg,box[:2])
def cover(im,W,H,fx=0.5,fy=0.5):
    r=max(W/im.width,H/im.height); im=im.resize((int(im.width*r)+1,int(im.height*r)+1),Image.LANCZOS)
    x=int((im.width-W)*fx); y=int((im.height-H)*fy); return im.crop((x,y,x+W,y+H))
def rounded(im,rad):
    m=Image.new('L',im.size,0); ImageDraw.Draw(m).rounded_rectangle([0,0,im.width-1,im.height-1],radius=rad,fill=255)
    out=Image.new('RGBA',im.size); out.paste(im,(0,0),m); return out
def frame(base,im,x,y,w,h,fx=0.5,fy=0.5):
    d=ImageDraw.Draw(base); d.rounded_rectangle([x-4,y-4,x+w+4,y+h+4],radius=30,fill=YELLOW)
    p=rounded(cover(im,w,h,fx,fy),26); base.paste(p,(x,y),p)
def render(W,H,out):
    story=H>1500; pad=60
    base=Image.new('RGB',(W,H),DARK); d=ImageDraw.Draw(base)
    # brilho sutil
    top=170 if story else 50
    lg=logo.resize((150,int(logo.height*150/logo.width)),Image.LANCZOS); base.paste(lg,(W-pad-150,top),lg)
    d.text((pad,top+6),'OBRA ENTREGUE · RIO PRETO E REGIÃO',font=pop('Bold',24),fill=GREEN)
    ft=beb(118 if not story else 130)
    d.text((pad,top+44),'LIGUE O AR SEM',font=ft,fill=WHITE)
    d.text((pad,top+44+int(ft.size*0.9)),'MEDO DA CONTA',font=ft,fill=YELLOW)
    y=top+44+int(ft.size*1.85)+24
    if story:
        fw=W-2*pad; h1=410; h2=410
        frame(base,cima,pad,y,fw,h1,0.5,0.4); y+=h1+28
        frame(base,frente,pad,y,fw,h2,0.5,0.55); y+=h2+36
    else:
        gap=24; fw=(W-2*pad-gap)//2; fh=570
        frame(base,cima,pad,y,fw,fh,0.57,0.4)
        frame(base,frente,pad+fw+gap,y,fw,fh,0.45,0.5); y+=fh+36
    stats=[('11','placas de 620 W'),('825','kWh por mês'),('+R$ 700','de economia/mês')]
    n=3; g=18; bw=(W-2*pad-2*g)//3; bh=140
    for i,(v,k) in enumerate(stats):
        x=pad+i*(bw+g)
        d.rounded_rectangle([x,y,x+bw,y+bh],radius=22,fill=(14,38,28),outline=YELLOW if i==2 else GREEN,width=3)
        fv=beb(78)
        while d.textlength(v,font=fv)>bw-40: fv=beb(fv.size-4)
        d.text((x+24,y+14),v,font=fv,fill=YELLOW if i==2 else WHITE)
        d.text((x+24,y+96),k,font=pop('Medium',22),fill=MUTED)
    y+=bh+26
    d.text((pad,y),'E você, está esperando o quê? Economia média de 80%.',font=pop('Medium',22 if not story else 26),fill=SOFT)
    fy=H-(64 if not story else 200)-80
    t='Simulação gratuita · (17) 99671-7575'; fc=pop('Bold',32)
    d.rounded_rectangle([pad,fy,W-pad,fy+80],radius=40,fill=GREEN)
    d.text((W/2,fy+40),t,font=fc,fill=DARK,anchor='mm')
    base.save(out,quality=92)
render(1080,1350,D+'/arte_feed.jpg'); render(1080,1920,D+'/arte_story.jpg')
