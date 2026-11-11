// Reels "texto rápido" da GW: 2 a 4 palavras por tela, trocando a cada ~1,5 s, uma palavra em destaque,
// foto de obra escurecida ao fundo, barra de progresso em segmentos no topo e fechamento "Comenta CONTA".
import React from 'react';
import {AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig, Sequence} from 'remotion';

const DARK = '#081812', GREEN = '#22C55E', YELLOW = '#FACC15', SOFT = '#cfe3d6';
const fonts = `
@font-face{font-family:Bebas;src:url(${staticFile('fonts/BebasNeue-Regular.ttf')})}
@font-face{font-family:Poppins;font-weight:500;src:url(${staticFile('fonts/Poppins-Medium.ttf')})}
@font-face{font-family:Poppins;font-weight:700;src:url(${staticFile('fonts/Poppins-Bold.ttf')})}`;

export type Beat = {t: string; sub?: string; foto?: string; dur?: number; nota?: string};
export type KineticProps = {beats: Beat[]; cta: {palavra: string; texto: string}; whatsapp: string};
export const CTA_SEG = 3.4;
const DEF = 1.6;
export const kineticFrames = (p: KineticProps, fps = 30) => Math.round((p.beats.reduce((a, b) => a + (b.dur ?? DEF), 0) + CTA_SEG) * fps);

// "SUA CONTA DE *R$ 800*" -> partes, com *destaque*
const parts = (t: string) => t.split(/(\*[^*]+\*)/).filter(Boolean).map((s) => ({s: s.replace(/\*/g, ''), hl: s.startsWith('*')}));

const Bar: React.FC<{n: number; i: number; prog: number}> = ({n, i, prog}) => (
  <div style={{position: 'absolute', top: 120, left: 70, right: 70, display: 'flex', gap: 8}}>
    {Array.from({length: n}).map((_, k) => (
      <div key={k} style={{flex: 1, height: 12, borderRadius: 6, background: 'rgba(255,255,255,.18)', overflow: 'hidden'}}>
        <div style={{height: '100%', width: `${k < i ? 100 : k === i ? prog * 100 : 0}%`, background: k === i ? YELLOW : GREEN}} />
      </div>))}
  </div>);

const BeatView: React.FC<{b: Beat; frames: number; bg?: string}> = ({b, frames, bg}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const ps = parts(b.t);
  const words = ps.reduce((a, p) => a + p.s.length, 0);
  const size = words > 22 ? 120 : words > 14 ? 150 : 190;
  return (
    <AbsoluteFill>
      {bg && <Img src={staticFile(bg)} style={{width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${1.1 + f / frames * 0.06})`, filter: 'brightness(.38) saturate(.9)'}} />}
      <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', padding: '0 70px', textAlign: 'center'}}>
        <div style={{fontFamily: 'Bebas', fontSize: size, lineHeight: .95, color: '#fff', textShadow: '0 8px 0 rgba(0,0,0,.4)'}}>
          {ps.map((p, k) => {
            const s = spring({frame: f - k * 3, fps, config: {damping: 12, stiffness: 220}});
            return <span key={k} style={{display: 'inline-block', color: p.hl ? DARK : '#fff', background: p.hl ? YELLOW : 'transparent', padding: p.hl ? '4px 18px 0' : 0, borderRadius: 14, margin: '0 6px', transform: `scale(${.6 + .4 * s}) rotate(${p.hl ? (1 - s) * -6 : 0}deg)`, opacity: s}}>{p.s}</span>;
          })}
        </div>
        {b.sub && <div style={{marginTop: 34, fontSize: 44, fontWeight: 500, color: SOFT, opacity: interpolate(f, [6, 14], [0, 1], {extrapolateRight: 'clamp'})}}>{b.sub}</div>}
      </AbsoluteFill>
      {b.nota && <div style={{position: 'absolute', left: 70, right: 70, bottom: 260, fontSize: 26, color: SOFT, textAlign: 'center'}}>{b.nota}</div>}
    </AbsoluteFill>);
};

export const KineticReel: React.FC<KineticProps> = (p) => {
  const {fps} = useVideoConfig(); const f = useCurrentFrame();
  let t = 0, bg: string | undefined, cur = 0, curProg = 0;
  const seqs = p.beats.map((b, i) => {
    const d = Math.round((b.dur ?? DEF) * fps); const from = t; t += d;
    if (b.foto) bg = b.foto;
    if (f >= from && f < from + d) { cur = i; curProg = (f - from) / d; }
    return <Sequence key={i} from={from} durationInFrames={d}><BeatView b={b} frames={d} bg={bg} /></Sequence>;
  });
  const end = t; const inEnd = f >= end;
  const s = spring({frame: f - end, fps, config: {damping: 12}});
  return (
    <AbsoluteFill style={{background: DARK, fontFamily: 'Poppins', color: '#fff'}}>
      <style>{fonts}</style>
      {seqs}
      {!inEnd && <Bar n={p.beats.length} i={cur} prog={curProg} />}
      {!inEnd && <Img src={staticFile('logo_branco.png')} style={{position: 'absolute', top: 160, right: 70, width: 130}} />}
      <Sequence from={end}>
        <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', textAlign: 'center', padding: 60, opacity: s}}>
          <Img src={staticFile('logo_branco.png')} style={{width: 300}} />
          <div style={{fontFamily: 'Bebas', fontSize: 150, marginTop: 50, lineHeight: .95}}>COMENTA</div>
          <div style={{fontFamily: 'Bebas', fontSize: 220, lineHeight: .95, background: YELLOW, color: DARK, padding: '10px 50px 0', borderRadius: 24, transform: `scale(${.7 + .3 * s}) rotate(${(1 - s) * -8}deg)`}}>{p.cta.palavra}</div>
          <div style={{marginTop: 40, fontSize: 42, fontWeight: 500, color: SOFT, maxWidth: 900}}>{p.cta.texto}</div>
          <div style={{marginTop: 40, background: GREEN, color: DARK, fontWeight: 700, fontSize: 56, padding: '20px 50px', borderRadius: 999}}>{p.whatsapp}</div>
        </AbsoluteFill>
      </Sequence>
    </AbsoluteFill>);
};
