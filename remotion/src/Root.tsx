import React from 'react';
import {Composition} from 'remotion';
import {ObraReel, obraDefaults} from './ObraReel';
import {SlidesReel, totalFrames, SlidesProps} from './SlidesReel';
import {KineticReel, kineticFrames, KineticProps} from './KineticReel';
const slidesDefault: SlidesProps = {cenas: [{foto: 'obra/a.png', dur: 3, titulo: ['TESTE', '*GW*']}], fim: {titulo: 'SIMULAÇÃO GRATUITA', texto: 'Economia média de 80% · Rio Preto e região'}, whatsapp: '(17) 99671-7575'};
export const Root: React.FC = () => (<>
  <Composition id="ObraReel" component={ObraReel} durationInFrames={360} fps={30} width={1080} height={1920} defaultProps={obraDefaults} />
  <Composition id="SlidesReel" component={SlidesReel} durationInFrames={300} fps={30} width={1080} height={1920} defaultProps={slidesDefault}
    calculateMetadata={({props}) => ({durationInFrames: totalFrames(props as SlidesProps)})} />
  <Composition id="KineticReel" component={KineticReel} durationInFrames={300} fps={30} width={1080} height={1920}
    defaultProps={{beats: [{t: 'TESTE *GW*'}], cta: {palavra: 'CONTA', texto: 'e a gente te manda a simulação gratuita'}, whatsapp: '(17) 99671-7575'} as KineticProps}
    calculateMetadata={({props}) => ({durationInFrames: kineticFrames(props as KineticProps)})} />
</>);
