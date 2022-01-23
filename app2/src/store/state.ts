import { Config, DEFAULT_CONFIG } from '../types/config';

export interface BodyParts {
    face?: boolean;
    body?: boolean;
    limbs?: boolean;
}

export interface State {
    config: Config;
    renderOptions: {
        lines: BodyParts;
        spheres: BodyParts;
        showBox: boolean;
        showAxes: boolean;
    }
}

export const INITIAL_STATE: State = {
    config: DEFAULT_CONFIG,
    renderOptions: {
        lines: {
            face: false,
            body: true,
            limbs: false
        },
        spheres: {
            face: false,
            body: true,
            limbs: false
        },
        showAxes: true,
        showBox: true
    }
};
