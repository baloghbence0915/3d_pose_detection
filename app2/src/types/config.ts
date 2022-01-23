import { Side } from './side';

export interface Config {
    camera: {
        resolution: [number, number];
        channels: Record<Side, number>;
        mods: Record<Side, { rot: number }> & {
            all: {
                undistortion: {
                    enabled: boolean;
                    DIM: [number, number];
                    K: number[][];
                    D: number[][];
                };
            }
        };
    };
    debug: {
        show_landmarks: boolean;
        show_vert_hor_line: boolean;
        show_points_per_side: boolean;
    };
    calculations: {
        horizontal_angle: number;
        stereo_baseline: number;
        stereo_scale: number;
        move_points_to_center: boolean;
        align_ground: {
            enabled: boolean;
            slope: number;
            bias: number;
        };
        normalize_height: {
            enabled: boolean;
            slope: number;
            bias: number;
        };
        offset: {
            enabled: boolean,
            x: number,
            z: number
        }
    };
    playback: {
        recoding: boolean;
        playing: {
            enabled: boolean;
            file: string;
        };
    };
}

export const DEFAULT_CONFIG: Config = {
    camera: {
        resolution: [0, 0],
        channels: {
            left: 0,
            right: 0
        },
        mods: {
            left: {
                rot: 0
            },
            right: {
                rot: 0
            },
            all: {
                undistortion: {
                    enabled: false,
                    DIM: [0, 0],
                    D: [],
                    K: []
                }
            }
        }
    },
    calculations: {
        horizontal_angle: 0,
        stereo_baseline: 0,
        stereo_scale: 0,
        move_points_to_center: false,
        align_ground: {
            enabled: false,
            slope: 0,
            bias: 0
        },
        normalize_height: {
            enabled: false,
            slope: 0,
            bias: 0
        },
        offset: {
            enabled: false,
            x: 0,
            z: 0
        }
    },
    debug: {
        show_landmarks: false,
        show_vert_hor_line: false,
        show_points_per_side: false
    },
    playback: {
        recoding: false,
        playing: {
            enabled: false,
            file: ''
        }
    }
};
