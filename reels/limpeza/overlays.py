from PIL import Image, ImageDraw, ImageFont
R='/home/claude/gw-posts'; FD=R+'/assets/fonts'
def pop(w,s): return ImageFont.truetype(f'{FD}/Poppins-{w}.ttf',s)
def beb(s): return ImageFont.truetype(f'{FD}/BebasNeue-Regular.ttf',s)
DARK=(8,24,18); GREEN=(34,197,94); YELLOW=(250,204,21); WHITE=(255,255,255); SOFT=(228,240,232)
W,H=1080,1920; VY=380; VH=1215
logo=Image.open(R+'/assets/logo_branco.png').convert('RGBA')
# base (fundo + cabeçalho + moldura), com buraco transparente para o vídeo
b=Image.new('RGBA',(W,H),DARK+(255,)); d=ImageDraw.Draw(b)
lg=logo.resize((150,int(logo.height*150/logo.width))); b.alpha_composite(lg,(W-60-150,90))
d.text((60,110),'SEU SISTEMA',font=beb(108),fill=WHITE)
d.text((60,215),'MERECE ESSE CUIDADO',font=beb(108),fill=YELLOW)
d.rounded_rectangle([54,VY-6,W-54,VY+VH+6],radius=34,fill=YELLOW)
hole=Image.new('L',(W,H),0); ImageDraw.Draw(hole).rounded_rectangle([60,VY,W-60,VY+VH],radius=28,fill=255)
b.putalpha(Image.eval(hole,lambda v:255-v)); b.save('base.png')
caps=['Já fez a limpeza anual\ndas suas placas?','Poeira e sujeira acumulada\nroubam geração todo dia','Com a limpeza, ganho de\naté 20% na geração*','Agende a sua pelo WhatsApp\n(17) 99671-7575']
for i,c in enumerate(caps):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im); f=pop('Bold',50)
    y=VY+VH+40
    for j,l in enumerate(c.split('\n')):
        col=YELLOW if (i==2 and j==1) or (i==3 and j==1) else WHITE
        d.text((W/2,y),l,font=f,fill=col,anchor='ma'); y+=66
    if i==2: d.text((W/2,y+8),'*dependendo da sujeira acumulada',font=pop('Medium',26),fill=SOFT,anchor='ma')
    im.save(f'cap{i}.png')
e=Image.new('RGB',(W,H),DARK); d=ImageDraw.Draw(e)
lg=logo.resize((380,int(logo.height*380/logo.width))); e.paste(lg,((W-380)//2,420),lg)
y=420+lg.height+70
d.text((W/2,y),'LIMPEZA DE PLACAS',font=beb(130),fill=WHITE,anchor='ma'); y+=130
d.text((W/2,y),'AGENDE A SUA',font=beb(130),fill=YELLOW,anchor='ma'); y+=170
d.rounded_rectangle([110,y,W-110,y+110],radius=55,fill=GREEN)
d.text((W/2,y+55),'(17) 99671-7575',font=pop('Bold',56),fill=DARK,anchor='mm'); y+=160
d.text((W/2,y),'Rio Preto e região',font=pop('Medium',36),fill=SOFT,anchor='ma')
e.save('end.png')
