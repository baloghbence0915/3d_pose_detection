
export const NOSE = 0;
export const LEFT_EYE_INNER = 1;
export const LEFT_EYE = 2;
export const LEFT_EYE_OUTER = 3;
export const RIGHT_EYE_INNER = 4;
export const RIGHT_EYE = 5;
export const RIGHT_EYE_OUTER = 6;
export const LEFT_EAR = 7;
export const RIGHT_EAR = 8;
export const LEFT_MOUTH = 9;
export const RIGHT_MOUTH = 10;
export const LEFT_SHOULDER = 11;
export const RIGHT_SHOULDER = 12;
export const LEFT_ELBOW = 13;
export const RIGHT_ELBOW = 14;
export const LEFT_WIRST = 15;
export const RIGHT_WIRST = 16;
export const LEFT_PINKY = 17;
export const RIGHT_PINKY = 18;
export const LEFT_INDEX = 19;
export const RIGHT_INDEX = 20;
export const LEFT_THUMB = 21;
export const RIGHT_THUMB = 22;
export const LEFT_HIP = 23;
export const RIGHT_HIP = 24;
export const LEFT_KNEE = 25;
export const RIGHT_KNEE = 26;
export const LEFT_ANKLE = 27;
export const RIGHT_ANKLE = 28;
export const LEFT_HEEL = 29;
export const RIGHT_HEEL = 30;
export const LEFT_FOOT_INDEX = 31;
export const RIGHT_FOOT_INDEX = 32;

export const BODY_CONNECTIONS = {
    [NOSE]: {
        [LEFT_EYE_INNER]: 1,
        [RIGHT_EYE_INNER]: 1,
    },
    [LEFT_EYE_INNER]: {
        [NOSE]: 1,
        [LEFT_EYE]: 1,
    },
    [LEFT_EYE]: {
        [LEFT_EYE_INNER]: 1,
        [LEFT_EYE_OUTER]: 1,
    },
    [LEFT_EYE_OUTER]: {
        [LEFT_EYE]: 1,
        [LEFT_EAR]: 1,
    },
    [RIGHT_EYE_INNER]: {
        [NOSE]: 1,
        [RIGHT_EYE]: 1,
    },
    [RIGHT_EYE]: {
        [RIGHT_EYE_INNER]: 1,
        [RIGHT_EYE_OUTER]: 1,
    },
    [RIGHT_EYE_OUTER]: {
        [RIGHT_EYE]: 1,
        [RIGHT_EAR]: 1,
    },
    [LEFT_EAR]: {
        [LEFT_EYE_OUTER]: 1
    },
    [RIGHT_EAR]: {
        [RIGHT_EYE_OUTER]: 1
    },
    [LEFT_MOUTH]: {
        [RIGHT_MOUTH]: 1
    },
    [RIGHT_MOUTH]: {
        [LEFT_MOUTH]: 1
    },
    [LEFT_SHOULDER]: {
        [RIGHT_SHOULDER]: 1,
        [LEFT_ELBOW]: 1,
        [LEFT_HIP]: 1,
    },
    [RIGHT_SHOULDER]: {
        [LEFT_SHOULDER]: 1,
        [RIGHT_ELBOW]: 1,
        [RIGHT_HIP]: 1,
    },
    [LEFT_ELBOW]: {
        [LEFT_SHOULDER]: 1,
        [LEFT_WIRST]: 1,
    },
    [RIGHT_ELBOW]: {
        [RIGHT_SHOULDER]: 1,
        [RIGHT_WIRST]: 1,
    },
    [LEFT_WIRST]: {
        [LEFT_ELBOW]: 1,
        [LEFT_PINKY]: 1,
        [LEFT_INDEX]: 1,
        [LEFT_THUMB]: 1,
    },
    [RIGHT_WIRST]: {
        [RIGHT_ELBOW]: 1,
        [RIGHT_PINKY]: 1,
        [RIGHT_INDEX]: 1,
        [RIGHT_THUMB]: 1,
    },
    [LEFT_PINKY]: {
        [LEFT_WIRST]: 1,
        [LEFT_INDEX]: 1,
    },
    [RIGHT_PINKY]: {
        [RIGHT_WIRST]: 1,
        [RIGHT_INDEX]: 1,
    },
    [LEFT_INDEX]: {
        [LEFT_WIRST]: 1,
        [LEFT_PINKY]: 1
    },
    [RIGHT_INDEX]: {
        [RIGHT_WIRST]: 1,
        [RIGHT_PINKY]: 1
    },
    [LEFT_THUMB]: {
        [LEFT_WIRST]: 1
    },
    [RIGHT_THUMB]: {
        [RIGHT_WIRST]: 1
    },
    [LEFT_HIP]: {
        [LEFT_SHOULDER]: 1,
        [RIGHT_HIP]: 1,
        [LEFT_KNEE]: 1,
    },
    [RIGHT_HIP]: {
        [RIGHT_SHOULDER]: 1,
        [LEFT_HIP]: 1,
        [RIGHT_KNEE]: 1,
    },
    [LEFT_KNEE]: {
        [LEFT_HIP]: 1,
        [LEFT_ANKLE]: 1,
    },
    [RIGHT_KNEE]: {
        [RIGHT_HIP]: 1,
        [RIGHT_ANKLE]: 1,
    },
    [LEFT_ANKLE]: {
        [LEFT_KNEE]: 1,
        [LEFT_HEEL]: 1,
        [LEFT_FOOT_INDEX]: 1,
    },
    [RIGHT_ANKLE]: {
        [RIGHT_KNEE]: 1,
        [RIGHT_HEEL]: 1,
        [RIGHT_FOOT_INDEX]: 1
    },
    [LEFT_HEEL]: {
        [LEFT_ANKLE]: 1,
        [LEFT_FOOT_INDEX]: 1
    },
    [RIGHT_HEEL]: {
        [RIGHT_ANKLE]: 1,
        [RIGHT_FOOT_INDEX]: 1
    },
    [LEFT_FOOT_INDEX]: {
        [LEFT_ANKLE]: 1,
        [LEFT_HEEL]: 1,
    },
    [RIGHT_FOOT_INDEX]: {
        [RIGHT_ANKLE]: 1,
        [RIGHT_HEEL]: 1,
    }
};

export const FACE_POINTS = [
    NOSE,
    LEFT_EYE_INNER,
    LEFT_EYE,
    LEFT_EYE_OUTER,
    RIGHT_EYE_INNER,
    RIGHT_EYE,
    RIGHT_EYE_OUTER,
    LEFT_EAR,
    RIGHT_EAR,
    LEFT_MOUTH,
    RIGHT_MOUTH
];

export const BODY_POINTS = [
    LEFT_SHOULDER,
    RIGHT_SHOULDER,
    LEFT_ELBOW,
    RIGHT_ELBOW,
    LEFT_WIRST,
    RIGHT_WIRST,
    LEFT_HIP,
    RIGHT_HIP,
    LEFT_KNEE,
    RIGHT_KNEE,
    LEFT_ANKLE,
    RIGHT_ANKLE,
    LEFT_HEEL,
    RIGHT_HEEL
];

export const LIMB_POINTS = [
    LEFT_PINKY,
    RIGHT_PINKY,
    LEFT_INDEX,
    RIGHT_INDEX,
    LEFT_THUMB,
    RIGHT_THUMB,
    LEFT_WIRST,
    RIGHT_WIRST,
    LEFT_FOOT_INDEX,
    RIGHT_FOOT_INDEX,
    LEFT_HEEL,
    RIGHT_HEEL,
    LEFT_ANKLE,
    RIGHT_ANKLE
];
