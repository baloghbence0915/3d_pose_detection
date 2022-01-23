import { Reducer } from 'react';
import { Actions } from './actions';
import { State } from './state';

export const appReducer: Reducer<State, Actions> = (state, action) => {
    switch (action.type) {
        case 'setConfig':
            return {
                ...state,
                config: action.payload,
            };
        case 'changeChannel':
            return {
                ...state,
                config: {
                    ...state.config,
                    camera: {
                        ...state.config.camera,
                        channels: {
                            ...state.config.camera.channels,
                            [action.payload.side]: action.payload.channel
                        }
                    }
                }
            };
        case 'rotateChannel':
            return {
                ...state,
                config: {
                    ...state.config,
                    camera: {
                        ...state.config.camera,
                        mods: {
                            ...state.config.camera.mods,
                            [action.payload]: {
                                ...state.config.camera.mods[action.payload],
                                rot: (state.config.camera.mods[action.payload].rot + 1) % 4
                            }
                        }
                    }
                }
            };
        case 'swapChannels':
            return {
                ...state,
                config: {
                    ...state.config,
                    camera: {
                        ...state.config.camera,
                        channels: {
                            left: state.config.camera.channels.right,
                            right: state.config.camera.channels.left,
                        }
                    }
                }
            };
        case 'toggleIsRecording':
            return {
                ...state,
                config: {
                    ...state.config,
                    playback: {
                        ...state.config.playback,
                        recoding: !state.config.playback.recoding
                    }
                }
            };
        case 'toggleIsReplaying':
            return {
                ...state,
                config: {
                    ...state.config,
                    playback: {
                        ...state.config.playback,
                        playing: {
                            ...state.config.playback.playing,
                            enabled: !state.config.playback.playing.enabled
                        }
                    }
                }
            };
        case 'setRecording':
            return {
                ...state,
                config: {
                    ...state.config,
                    playback: {
                        ...state.config.playback,
                        playing: {
                            ...state.config.playback.playing,
                            file: action.payload
                        }
                    }
                }
            };
        case 'toggleShowLandmarks':
            return {
                ...state,
                config: {
                    ...state.config,
                    debug: {
                        ...state.config.debug,
                        show_landmarks: !state.config.debug.show_landmarks
                    }
                }
            };
        case 'toggleShowLines':
            return {
                ...state,
                config: {
                    ...state.config,
                    debug: {
                        ...state.config.debug,
                        show_vert_hor_line: !state.config.debug.show_vert_hor_line
                    }
                }
            };
        case 'toggleUndistortion':
            return {
                ...state,
                config: {
                    ...state.config,
                    camera: {
                        ...state.config.camera,
                        mods: {
                            ...state.config.camera.mods,
                            all: {
                                ...state.config.camera.mods.all,
                                undistortion: {
                                    ...state.config.camera.mods.all.undistortion,
                                    enabled: !state.config.camera.mods.all.undistortion.enabled
                                }
                            }
                        }
                    }
                }
            };
        case 'setUndistortionParams':
            return {
                ...state,
                config: {
                    ...state.config,
                    camera: {
                        ...state.config.camera,
                        mods: {
                            ...state.config.camera.mods,
                            all: {
                                ...state.config.camera.mods.all,
                                undistortion: {
                                    ...state.config.camera.mods.all.undistortion,
                                    ...action.payload
                                }
                            }
                        }
                    }
                }
            };
        case 'setHorizontalAngle':
            return {
                ...state,
                config: {
                    ...state.config,
                    calculations: {
                        ...state.config.calculations,
                        horizontal_angle: action.payload
                    }
                }
            };
        case 'setStereoBaseline':
            return {
                ...state,
                config: {
                    ...state.config,
                    calculations: {
                        ...state.config.calculations,
                        stereo_baseline: action.payload
                    }
                }
            };
        case 'setStereoScale':
            return {
                ...state,
                config: {
                    ...state.config,
                    calculations: {
                        ...state.config.calculations,
                        stereo_scale: action.payload
                    }
                }
            };
        case 'toggleAlignGround':
            return {
                ...state,
                config: {
                    ...state.config,
                    calculations: {
                        ...state.config.calculations,
                        align_ground: {
                            ...state.config.calculations.align_ground,
                            enabled: !state.config.calculations.align_ground.enabled
                        }
                    }
                }
            };
        case 'toggleNormalizeHeight':
            return {
                ...state,
                config: {
                    ...state.config,
                    calculations: {
                        ...state.config.calculations,
                        normalize_height: {
                            ...state.config.calculations.normalize_height,
                            enabled: !state.config.calculations.normalize_height.enabled
                        }
                    }
                }
            };
        case 'toggleMoveToCenter':
            return {
                ...state,
                config: {
                    ...state.config,
                    calculations: {
                        ...state.config.calculations,
                        move_points_to_center: !state.config.calculations.move_points_to_center
                    }
                }
            };
        case 'setAlignGroundParams':
            return {
                ...state,
                config: {
                    ...state.config,
                    calculations: {
                        ...state.config.calculations,
                        align_ground: {
                            ...state.config.calculations.align_ground,
                            ...action.payload
                        }
                    }
                }
            };
        case 'setNormalizeHeightParams':
            return {
                ...state,
                config: {
                    ...state.config,
                    calculations: {
                        ...state.config.calculations,
                        normalize_height: {
                            ...state.config.calculations.normalize_height,
                            ...action.payload
                        }
                    }
                }
            };
        case 'toggleOffsets':
            return {
                ...state,
                config: {
                    ...state.config,
                    calculations: {
                        ...state.config.calculations,
                        offset: {
                            ...state.config.calculations.offset,
                            enabled: !state.config.calculations.offset.enabled
                        }
                    }
                }
            };
        case 'setOffsetParams':
            return {
                ...state,
                config: {
                    ...state.config,
                    calculations: {
                        ...state.config.calculations,
                        offset: {
                            ...state.config.calculations.offset,
                            ...action.payload
                        }
                    }
                }
            };
        case 'setRenderingLines': {
            return {
                ...state,
                renderOptions: {
                    ...state.renderOptions,
                    lines: action.payload
                }
            };
        }
        case 'setRenderingSpheres': {
            return {
                ...state,
                renderOptions: {
                    ...state.renderOptions,
                    spheres: action.payload
                }
            };
        }
        case 'toggleRenderingBox': {
            return {
                ...state,
                renderOptions: {
                    ...state.renderOptions,
                    showBox: !state.renderOptions.showBox
                }
            };
        }
        case 'toggleRenderingAxes': {
            return {
                ...state,
                renderOptions: {
                    ...state.renderOptions,
                    showAxes: !state.renderOptions.showAxes
                }
            };
        }
        default:
            return state;
    }
}

export const appReducerWithLogger: Reducer<State, Actions> = (state, action) => {
    const newState = appReducer(state, action);

    console.groupCollapsed(action.type);
    console.groupCollapsed('Payload');
    console.log(action.payload);
    console.groupEnd();
    console.groupCollapsed('Old State');
    console.log(state);
    console.groupEnd();

    if (state !== newState) {
        console.groupCollapsed('New State');
        console.log(newState);
        console.groupEnd();
    }

    console.groupEnd();

    return newState;
}