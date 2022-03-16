import { Config } from '../types/config';
import { Side } from '../types/side';
import { BodyParts } from './state';

type Action<T, P> = { type: T, payload: P };

function createAction<T, P>(type: T): (p: P) => Action<T, P> {
    return (payload) => ({ type, payload });
}

export const actions = {
    setConfig: createAction<'setConfig', Config>('setConfig'),
    changeChannel: createAction<'changeChannel', { side: Side, channel: number }>('changeChannel'),
    rotateChannel: createAction<'rotateChannel', Side>('rotateChannel'),
    swapChannels: createAction<'swapChannels', void>('swapChannels'),
    toggleIsRecording: createAction<'toggleIsRecording', void>('toggleIsRecording'),
    toggleIsReplaying: createAction<'toggleIsReplaying', void>('toggleIsReplaying'),
    setRecording: createAction<'setRecording', string>('setRecording'),
    toggleShowLandmarks: createAction<'toggleShowLandmarks', void>('toggleShowLandmarks'),
    toggleShowLines: createAction<'toggleShowLines', void>('toggleShowLines'),
    toggleUndistortion: createAction<'toggleUndistortion', void>('toggleUndistortion'),
    setUndistortionParams: createAction<'setUndistortionParams', any>('setUndistortionParams'),
    setHorizontalAngle: createAction<'setHorizontalAngle', number>('setHorizontalAngle'),
    setStereoBaseline: createAction<'setStereoBaseline', number>('setStereoBaseline'),
    setStereoScale: createAction<'setStereoScale', number>('setStereoScale'),
    toggleAlignGround: createAction<'toggleAlignGround', void>('toggleAlignGround'),
    toggleNormalizeHeight: createAction<'toggleNormalizeHeight', void>('toggleNormalizeHeight'),
    toggleMoveToCenter: createAction<'toggleMoveToCenter', void>('toggleMoveToCenter'),
    setAlignGroundParams: createAction<'setAlignGroundParams', { slope: number; bias: number; }>('setAlignGroundParams'),
    setNormalizeHeightParams: createAction<'setNormalizeHeightParams', { slope: number; bias: number; }>('setNormalizeHeightParams'),
    toggleOffsets: createAction<'toggleOffsets', void>('toggleOffsets'),
    setOffsetParams: createAction<'setOffsetParams', { x: number; z: number }>('setOffsetParams'),
    setRenderingLines: createAction<'setRenderingLines', BodyParts>('setRenderingLines'),
    setRenderingSpheres: createAction<'setRenderingSpheres', BodyParts>('setRenderingSpheres'),
    toggleRenderingBox: createAction<'toggleRenderingBox', void>('toggleRenderingBox'),
    toggleRenderingAxes: createAction<'toggleRenderingAxes', void>('toggleRenderingAxes'),
    toggleOrtographicCamera: createAction<'toggleOrtographicCamera', void>('toggleOrtographicCamera'),
    toggleShowSideBySide: createAction<'toggleShowSideBySide', void>('toggleShowSideBySide'),
}


export type Actions =
    ReturnType<typeof actions.setConfig> |
    ReturnType<typeof actions.changeChannel> |
    ReturnType<typeof actions.rotateChannel> |
    ReturnType<typeof actions.toggleIsRecording> |
    ReturnType<typeof actions.toggleIsReplaying> |
    ReturnType<typeof actions.setRecording> |
    ReturnType<typeof actions.toggleShowLandmarks> |
    ReturnType<typeof actions.toggleShowLines> |
    ReturnType<typeof actions.toggleUndistortion> |
    ReturnType<typeof actions.setUndistortionParams> |
    ReturnType<typeof actions.setHorizontalAngle> |
    ReturnType<typeof actions.setStereoBaseline> |
    ReturnType<typeof actions.setStereoScale> |
    ReturnType<typeof actions.toggleAlignGround> |
    ReturnType<typeof actions.toggleNormalizeHeight> |
    ReturnType<typeof actions.toggleMoveToCenter> |
    ReturnType<typeof actions.setAlignGroundParams> |
    ReturnType<typeof actions.setNormalizeHeightParams> |
    ReturnType<typeof actions.toggleOffsets> |
    ReturnType<typeof actions.setOffsetParams> |
    ReturnType<typeof actions.setRenderingLines> |
    ReturnType<typeof actions.setRenderingSpheres> |
    ReturnType<typeof actions.toggleRenderingBox> |
    ReturnType<typeof actions.toggleRenderingAxes> |
    ReturnType<typeof actions.toggleOrtographicCamera> |
    ReturnType<typeof actions.toggleShowSideBySide> |
    ReturnType<typeof actions.swapChannels>;
