import {Config} from '@remotion/cli/config';
Config.setBrowserExecutable(process.env.REMOTION_CHROME || '/opt/pw-browsers/chromium-1243/chrome-linux64/chrome');
Config.setVideoImageFormat('jpeg');
