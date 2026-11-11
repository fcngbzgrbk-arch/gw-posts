// Modelo de Reels "Obra entregue" da GW — estilo título grande (Bebas + Poppins, verde escuro/amarelo)
import React from 'react';
import {AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig, Sequence, Easing} from 'remotion';

const DARK = '#081812', GREEN = '#22C55E', YELLOW = '#FACC15';
const fonts = `
@font-face{font-family:Bebas;src:url(${staticFile('fonts/BebasNeue-Regular.ttf')})}
@font-face{font-family:Poppins;font-weight:500;src:url(${staticFile('fonts/Poppins-Medium.ttf')})}
@font-face{font-family:Poppins;font-weight:700;src:url(${staticFile('fonts/Poppins-Bold.ttf')})}`;

export type ObraProps = {
  fotos: string[];            // caminhos em public/ (2 fotos)
  selo: string;
  titulo: [string, string];   // linha branca, linha amarela
  stats: [string, string][];  // [valor, rótulo]
  frase: string;
  whatsapp: string;
};
export const obraDefaults: ObraProps = {
  fotos: ['obra/b.png', 'obra/a.png'],
  selo: 'OBRA ENTREGUE · RIO PRETO E REGIÃO',
  titulo: ['LIGUE O AR SEM', 'MEDO DA CONTA'],
  stats: [['11', 'placas de 620 W'], ['825', 'kWh por mês'], ['+R$ 700', 'de economia/mês']],
  frase: 'E você, está esperando o quê?',
  whatsapp: '(17) 99671-7575',
};

const KenBurns: React.FC<{src: string; dur: number; from?: number; to?: number}> = ({src, dur, from = 1.08, to = 1.22}) => {
  const f = useCurrentFrame();
  const s = interpolate(f, [0, dur], [from, to]);
  return <Img src={staticFile(src)} style={{width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${s})`}} />;
};

const Veil: React.FC = () => (
  <AbsoluteFill style={{background: `linear-gradient(180deg, rgba(8,24,18,.92) 0%, rgba(8,24,18,.55) 38%, rgba(8,24,18,.15) 60%, rgba(8,24,18,.9) 100%)`}} />
);

const Word: React.FC<{text: string; color: string; delay: number; size: number}> = ({text, color, delay, size}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const p = spring({frame: f - delay, fps, config: {damping: 14, stiffness: 160}});
  return <div style={{fontFamily: 'Bebas', fontSize: size, lineHeight: .92, color, transform: `translateY(${(1 - p) * 80}px) scale(${.85 + .15 * p})`, opacity: p, textShadow: '0 6px 0 rgba(0,0,0,.35)'}}>{text}</div>;
};

const Logo: React.FC<{w: number}> = ({w}) => <Img src={staticFile('logo_branco.png')} style={{width: w}} />;

export const ObraReel: React.FC<ObraProps> = (p) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const A = 0, B = 100, C = 210, D = 285, END = 360;
  return (
    <AbsoluteFill style={{background: DARK, fontFamily: 'Poppins', color: '#fff'}}>
      <style>{fonts}</style>
      {/* Cena 1: foto 1 + título */}
      <Sequence from={A} durationInFrames={B - A + 10}>
        <AbsoluteFill><KenBurns src={p.fotos[0]} dur={B} /></AbsoluteFill><Veil />
        <AbsoluteFill style={{padding: '230px 70px 0'}}>
          <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start'}}>
            <div style={{fontWeight: 700, fontSize: 30, letterSpacing: 3, color: GREEN, maxWidth: 700}}>{p.selo}</div>
            <Logo w={170} />
          </div>
          <div style={{marginTop: 40}}>
            <Word text={p.titulo[0]} color="#fff" delay={6} size={150} />
            <Word text={p.titulo[1]} color={YELLOW} delay={16} size={150} />
          </div>
        </AbsoluteFill>
      </Sequence>
      {/* Cena 2: foto 2 + números */}
      <Sequence from={B} durationInFrames={C - B + 10}>
        <AbsoluteFill><KenBurns src={p.fotos[1]} dur={C - B} from={1.2} to={1.06} /></AbsoluteFill><Veil />
        <AbsoluteFill style={{padding: '260px 70px 0', gap: 26, display: 'flex', flexDirection: 'column'}}>
          {p.stats.map(([v, k], i) => {
            const fr = useCurrentFrame();
            const s = spring({frame: fr - 8 - i * 14, fps, config: {damping: 15}});
            const last = i === p.stats.length - 1;
            return (
              <div key={i} style={{transform: `translateX(${(1 - s) * -900}px)`, opacity: s, background: 'rgba(8,24,18,.88)', border: `4px solid ${last ? YELLOW : GREEN}`, borderRadius: 32, padding: '22px 40px', display: 'flex', alignItems: 'baseline', gap: 28}}>
                <span style={{fontFamily: 'Bebas', fontSize: 150, lineHeight: .9, color: last ? YELLOW : '#fff'}}>{v}</span>
                <span style={{fontSize: 40, fontWeight: 500, color: '#cfe3d6'}}>{k}</span>
              </div>);
          })}
        </AbsoluteFill>
      </Sequence>
      {/* Cena 3: as duas fotos + frase */}
      <Sequence from={C} durationInFrames={D - C + 10}>
        <AbsoluteFill style={{padding: '240px 60px 0', gap: 24, display: 'flex', flexDirection: 'column'}}>
          {p.fotos.map((src, i) => {
            const fr = useCurrentFrame();
            const s = spring({frame: fr - i * 8, fps, config: {damping: 16}});
            return <div key={i} style={{height: 560, borderRadius: 30, overflow: 'hidden', border: `5px solid ${YELLOW}`, transform: `scale(${.8 + .2 * s})`, opacity: s}}><KenBurns src={src} dur={D - C} /></div>;
          })}
          <div style={{fontFamily: 'Bebas', fontSize: 110, textAlign: 'center', marginTop: 20, opacity: interpolate(useCurrentFrame(), [20, 35], [0, 1], {extrapolateRight: 'clamp'})}}>{p.frase}</div>
        </AbsoluteFill>
      </Sequence>
      {/* Cena 4: fechamento */}
      <Sequence from={D} durationInFrames={END - D}>
        {(() => {
          const s = spring({frame: f - D, fps, config: {damping: 13}});
          return (
            <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', transform: `scale(${1.15 - .15 * s})`, opacity: s}}>
              <Logo w={400} />
              <div style={{fontFamily: 'Bebas', fontSize: 120, marginTop: 60, color: YELLOW}}>SIMULAÇÃO GRATUITA</div>
              <div style={{marginTop: 30, background: GREEN, color: DARK, fontWeight: 700, fontSize: 64, padding: '24px 60px', borderRadius: 999}}>{p.whatsapp}</div>
              <div style={{marginTop: 40, fontSize: 36, color: '#cfe3d6'}}>Economia média de 80% · Rio Preto e região</div>
            </AbsoluteFill>);
        })()}
      </Sequence>
    </AbsoluteFill>
  );
};
