import { Config, DEFAULT_CONFIG } from '../types/config';

export interface BodyParts {
    face?: boolean;
    body?: boolean;
    limbs?: boolean;
}

export interface State {
    config: Config;
    renderOptions: {
        showLines: BodyParts;
        showSpheres: BodyParts;
        showBox: boolean;
        showAxes: boolean;
        ortographic: boolean;
    }
}

export const INITIAL_STATE: State = {
    config: DEFAULT_CONFIG,
    renderOptions: {
        showLines: {
            face: false,
            body: true,
            limbs: false
        },
        showSpheres: {
            face: false,
            body: true,
            limbs: false
        },
        showAxes: true,
        showBox: true,
        ortographic: false
    }
};
