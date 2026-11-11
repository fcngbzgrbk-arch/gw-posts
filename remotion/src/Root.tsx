import React from 'react';
import {Composition} from 'remotion';
import {ObraReel, obraDefaults} from './ObraReel';
export const Root: React.FC = () => (
  <Composition id="ObraReel" component={ObraReel} durationInFrames={360} fps={30} width={1080} height={1920} defaultProps={obraDefaults} />
);
