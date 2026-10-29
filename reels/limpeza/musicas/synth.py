import numpy as np, wave, sys
SR=44100; DUR=17.7
def note(f): return 440*2**((f-69)/12)
def env(n,a=0.005,r=0.2):
    t=np.arange(n)/SR; e=np.minimum(1,t/a)*np.exp(-t/r); return e
def tone(f,d,kind='saw',a=0.005,r=0.3,det=0.0):
    n=int(d*SR); t=np.arange(n)/SR; out=0
    for dd in ([0] if det==0 else [-det,0,det]):
        ph=(f*(1+dd))*t
        if kind=='saw': w=2*(ph%1)-1
        elif kind=='sq': w=np.sign(np.sin(2*np.pi*ph))
        elif kind=='tri': w=2*np.abs(2*(ph%1)-1)-1
        else: w=np.sin(2*np.pi*ph)
        out=out+w
    return out/ (1 if det==0 else 3)*env(n,a,r)
def lp(x,c):
    # simples passa-baixa de 1 polo
    a=np.exp(-2*np.pi*c/SR); y=np.zeros_like(x); s=0.0
    from scipy.signal import lfilter
    return lfilter([1-a],[1,-a],x)
def kick(): n=int(0.35*SR); t=np.arange(n)/SR; f=50+120*np.exp(-t*30); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*9)
def hat(d=0.05): n=int(d*SR); return np.random.randn(n)*np.exp(-np.arange(n)/SR*60)*0.3
def clap(): n=int(0.2*SR); x=np.random.randn(n)*np.exp(-np.arange(n)/SR*25); return lp(x,3000)*0.6
def put(buf,x,t,g=1.0):
    i=int(t*SR); j=min(len(buf),i+len(x));
    if i<len(buf): buf[i:j]+=x[:j-i]*g
def build(style):
    buf=np.zeros(int(DUR*SR)+SR)
    if style=='house':
        bpm=122; prog=[[57,60,64],[53,57,60],[48,52,55],[55,59,62]]; bass=[45,41,36,43]
    elif style=='lofi':
        bpm=84; prog=[[62,65,69,72],[60,64,67,71],[57,60,64,67],[59,62,65,69]]; bass=[50,48,45,47]
    else: # motivacional
        bpm=128; prog=[[60,64,67],[55,59,62],[57,60,64],[53,57,60]]; bass=[48,43,45,41]
    b=60/bpm; bar=4*b; t=0; k=0
    while t<DUR:
        ch=prog[k%4]; bs=bass[k%4]
        for beat in range(4):
            tb=t+beat*b
            if style=='lofi':
                if beat in (0,2): put(buf,kick(),tb,0.7)
                if beat in (1,3): put(buf,clap(),tb,0.35)
                for e in range(2): put(buf,hat(0.04),tb+e*b/2+ (0.03 if e else 0),0.25)
            else:
                put(buf,kick(),tb,0.9)
                put(buf,hat(),tb+b/2,0.5)
                if style=='motiv' and beat in (1,3): put(buf,clap(),tb,0.6)
                if style=='house' and beat in (1,3): put(buf,clap(),tb,0.4)
        if style=='lofi':
            for f in ch: put(buf,lp(tone(note(f),bar,'tri',a=0.05,r=2.5),1800),t,0.12)
            put(buf,tone(note(bs),bar*0.9,'sine',a=0.02,r=1.5),t,0.35)
            # melodia simples
            mel=[ch[-1]+12,ch[1]+12,ch[2]+12,ch[0]+12]
            for i,m in enumerate(mel): put(buf,tone(note(m),b*0.9,'sine',a=0.01,r=0.4),t+i*b+b*0.5,0.08)
        elif style=='house':
            for e in range(8):
                if e%2==1:
                    for f in ch: put(buf,lp(tone(note(f+12),b*0.45,'saw',r=0.12,det=0.006),2600),t+e*b/2,0.07)
                put(buf,lp(tone(note(bs),b*0.45,'saw',r=0.15),500),t+e*b/2,0.25 if e%2 else 0.12)
        else:
            for f in ch: put(buf,lp(tone(note(f),bar,'saw',a=0.2,r=3,det=0.008),1600),t,0.07)
            for e in range(16):
                f=ch[e%3]+12; put(buf,lp(tone(note(f),b/4*0.8,'sq',r=0.06),3000),t+e*b/4,0.04)
            for e in range(4): put(buf,lp(tone(note(bs),b*0.9,'saw',r=0.3),400),t+e*b,0.3)
        t+=bar; k+=1
    buf=buf[:int(DUR*SR)]
    n=int(1.5*SR); buf[-n:]*=np.linspace(1,0,n); buf[:int(0.3*SR)]*=np.linspace(0,1,int(0.3*SR))
    buf=np.tanh(buf*1.2); buf/=np.abs(buf).max()/0.85
    st=np.stack([buf,buf],1)
    with wave.open(f'{style}.wav','wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st*32767).astype('<i2').tobytes())
for s in ['house','lofi','motiv']: build(s)
