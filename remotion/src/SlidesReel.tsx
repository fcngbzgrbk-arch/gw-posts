// Modelo genérico de Reels da GW: sequência de cenas (foto + título grande + cartões) e fechamento com WhatsApp.
import React from 'react';
import {AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig, Sequence} from 'remotion';

const DARK = '#081812', GREEN = '#22C55E', YELLOW = '#FACC15', SOFT = '#cfe3d6';
const fonts = `
@font-face{font-family:Bebas;src:url(${staticFile('fonts/BebasNeue-Regular.ttf')})}
@font-face{font-family:Poppins;font-weight:500;src:url(${staticFile('fonts/Poppins-Medium.ttf')})}
@font-face{font-family:Poppins;font-weight:700;src:url(${staticFile('fonts/Poppins-Bold.ttf')})}`;

export type Cena = {
  foto: string; dur: number;          // segundos
  selo?: string;
  titulo: string[];                   // linhas; "*linha*" = amarelo
  texto?: string;
  cartoes?: [string, string][];       // [valor, rótulo]
  rodape?: string;                    // letra miúda
};
export type SlidesProps = {cenas: Cena[]; fim: {titulo: string; texto: string}; whatsapp: string};
export const FIM_SEG = 3.2;
export const totalFrames = (p: SlidesProps, fps = 30) => Math.round((p.cenas.reduce((a, c) => a + c.dur, 0) + FIM_SEG) * fps);

const Line: React.FC<{t: string; d: number; size: number}> = ({t, d, size}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const p = spring({frame: f - d, fps, config: {damping: 14, stiffness: 160}});
  const hl = t.startsWith('*');
  return <div style={{fontFamily: 'Bebas', fontSize: size, lineHeight: .92, color: hl ? YELLOW : '#fff', opacity: p, transform: `translateY(${(1 - p) * 70}px)`, textShadow: '0 6px 0 rgba(0,0,0,.35)'}}>{t.replace(/\*/g, '')}</div>;
};

const CenaView: React.FC<{c: Cena; frames: number}> = ({c, frames}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const zoom = interpolate(f, [0, frames], [1.06, 1.2]);
  const out = interpolate(f, [frames - 6, frames], [1, 0], {extrapolateLeft: 'clamp'});
  const nLines = c.titulo.length;
  const size = Math.max(...c.titulo.map((t) => t.length)) > 14 ? 128 : 150;
  return (
    <AbsoluteFill style={{opacity: out}}>
      <Img src={staticFile(c.foto)} style={{width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${zoom})`}} />
      <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(8,24,18,.94) 0%, rgba(8,24,18,.75) 40%, rgba(8,24,18,.2) 62%, rgba(8,24,18,.92) 100%)'}} />
      <AbsoluteFill style={{padding: '220px 70px 0'}}>
        <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', minHeight: 120}}>
          <div style={{fontWeight: 700, fontSize: 30, letterSpacing: 3, color: GREEN, maxWidth: 700}}>{c.selo || ''}</div>
          <Img src={staticFile('logo_branco.png')} style={{width: 160}} />
        </div>
        <div style={{marginTop: 20}}>{c.titulo.map((t, i) => <Line key={i} t={t} d={4 + i * 7} size={size} />)}</div>
        {c.texto && <div style={{marginTop: 30, fontSize: 40, lineHeight: 1.35, color: '#eef6f0', fontWeight: 500, maxWidth: 900, opacity: interpolate(f, [10 + nLines * 7, 22 + nLines * 7], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})}}>{c.texto}</div>}
      </AbsoluteFill>
      {c.cartoes && (
        <AbsoluteFill style={{justifyContent: 'flex-end', padding: '0 70px 330px', gap: 22, display: 'flex', flexDirection: 'column'}}>
          {c.cartoes.map(([v, k], i) => {
            const s = spring({frame: f - 18 - i * 10, fps, config: {damping: 15}});
            const last = i === c.cartoes!.length - 1;
            return <div key={i} style={{transform: `translateX(${(1 - s) * -1000}px)`, background: 'rgba(8,24,18,.9)', border: `4px solid ${last ? YELLOW : GREEN}`, borderRadius: 28, padding: '14px 36px', display: 'flex', alignItems: 'baseline', gap: 26}}>
              <span style={{fontFamily: 'Bebas', fontSize: 110, lineHeight: .95, color: last ? YELLOW : '#fff'}}>{v}</span>
              <span style={{fontSize: 36, fontWeight: 500, color: SOFT}}>{k}</span></div>;
          })}
        </AbsoluteFill>)}
      {c.rodape && <div style={{position: 'absolute', left: 70, right: 70, bottom: 250, fontSize: 24, color: SOFT}}>{c.rodape}</div>}
    </AbsoluteFill>);
};

export const SlidesReel: React.FC<SlidesProps> = (p) => {
  const {fps} = useVideoConfig(); const f = useCurrentFrame();
  let t = 0;
  const seqs = p.cenas.map((c, i) => { const from = t; const d = Math.round(c.dur * fps); t += d; return <Sequence key={i} from={from} durationInFrames={d}><CenaView c={c} frames={d} /></Sequence>; });
  const s = spring({frame: f - t, fps, config: {damping: 13}});
  return (
    <AbsoluteFill style={{background: DARK, fontFamily: 'Poppins', color: '#fff'}}>
      <style>{fonts}</style>
      {seqs}
      <Sequence from={t}>
        <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', opacity: s, transform: `scale(${1.15 - .15 * s})`, textAlign: 'center', padding: 60}}>
          <Img src={staticFile('logo_branco.png')} style={{width: 380}} />
          <div style={{fontFamily: 'Bebas', fontSize: 120, marginTop: 60, color: YELLOW, lineHeight: .95}}>{p.fim.titulo}</div>
          <div style={{marginTop: 34, background: GREEN, color: DARK, fontWeight: 700, fontSize: 64, padding: '24px 60px', borderRadius: 999}}>{p.whatsapp}</div>
          <div style={{marginTop: 40, fontSize: 36, color: SOFT}}>{p.fim.texto}</div>
        </AbsoluteFill>
      </Sequence>
    </AbsoluteFill>);
};
