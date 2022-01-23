export const UPPER_ARM_LENGTH = (69 / 365);
export const LOWER_ARM_LENGTH = (54 / 365);
export const UPPBER_BODY_LENGTH = (88 / 365); // ?!
export const THIGH_LENGTH = (112 / 365);
export const SHIN_LENGTH = (85 / 365);
export const HEEL_HEIGHT = (11 / 365);
export const HIPS_WIDTH = (59 / 365);
export const SHOULDERS_WIDTH = (89 / 365);
export const LEFT_SHOULDER = 11;
export const RIGHT_SHOULDER = 12;
export const LEFT_ELBOW = 13;
export const RIGHT_ELBOW = 14;
export const LEFT_WIRST = 15;
export const RIGHT_WIRST = 16;
export const LEFT_HIP = 23;
export const RIGHT_HIP = 24;
export const LEFT_KNEE = 25;
export const RIGHT_KNEE = 26;
export const LEFT_ANKLE = 27;
export const RIGHT_ANKLE = 28;
export const LEFT_HEEL = 29;
export const RIGHT_HEEL = 30;

export const VALID_POINTS = [LEFT_SHOULDER, RIGHT_SHOULDER, LEFT_ELBOW, RIGHT_ELBOW, LEFT_WIRST, RIGHT_WIRST, LEFT_HIP, RIGHT_HIP, LEFT_KNEE,
    RIGHT_KNEE, LEFT_ANKLE, RIGHT_ANKLE, LEFT_HEEL, RIGHT_HEEL];

export const BODY_CONNECTIONS = {
    [LEFT_SHOULDER]: {
        [RIGHT_SHOULDER]: SHOULDERS_WIDTH,
        [LEFT_ELBOW]: UPPER_ARM_LENGTH,
        [LEFT_HIP]: UPPBER_BODY_LENGTH,
    },
    [RIGHT_SHOULDER]: {
        // [LEFT_SHOULDER]: SHOULDERS_WIDTH,
        [RIGHT_ELBOW]: UPPER_ARM_LENGTH,
        [RIGHT_HIP]: UPPBER_BODY_LENGTH,
    },
    [LEFT_ELBOW]: {
        // [LEFT_SHOULDER]: UPPER_ARM_LENGTH,
        [LEFT_WIRST]: LOWER_ARM_LENGTH,
    },
    [RIGHT_ELBOW]: {
        // [RIGHT_SHOULDER]: UPPER_ARM_LENGTH,
        [RIGHT_WIRST]: LOWER_ARM_LENGTH,
    },
    // [LEFT_WIRST]: {
    //     [LEFT_ELBOW]: LOWER_ARM_LENGTH,
    // },
    // [RIGHT_WIRST]: {
    //     [RIGHT_ELBOW]: LOWER_ARM_LENGTH,
    // },
    [LEFT_HIP]: {
        // [LEFT_SHOULDER]: UPPBER_BODY_LENGTH,
        [RIGHT_HIP]: HIPS_WIDTH,
        [LEFT_KNEE]: THIGH_LENGTH,
    },
    [RIGHT_HIP]: {
        // [RIGHT_SHOULDER]: UPPBER_BODY_LENGTH,
        // [LEFT_HIP]: HIPS_WIDTH,
        [RIGHT_KNEE]: THIGH_LENGTH,
    },
    [LEFT_KNEE]: {
        // [LEFT_HIP]: THIGH_LENGTH,
        [LEFT_ANKLE]: SHIN_LENGTH,
    },
    [RIGHT_KNEE]: {
        // [RIGHT_HIP]: THIGH_LENGTH,
        [RIGHT_ANKLE]: SHIN_LENGTH,
    },
    [LEFT_ANKLE]: {
        // [LEFT_KNEE]: SHIN_LENGTH,
        [LEFT_HEEL]: HEEL_HEIGHT,
    },
    [RIGHT_ANKLE]: {
        // [RIGHT_KNEE]: SHIN_LENGTH,
        [RIGHT_HEEL]: HEEL_HEIGHT,
    },
    // [LEFT_HEEL]: {
    //     [LEFT_ANKLE]: HEEL_HEIGHT
    // },
    // [RIGHT_HEEL]: {
    //     [RIGHT_ANKLE]: HEEL_HEIGHT
    // }
};

export const TEST_POINTS: Record<number, { x: number, y: number, z: number }> = {
    [LEFT_SHOULDER]: {
        x: 0.64561,
        y: 0.65577,
        z: 0.5
    },
    [RIGHT_SHOULDER]: {
        x: 0.39777,
        y: 0.6539,
        z: 0.5
    },
    [LEFT_ELBOW]: {
        x: 0.77141,
        y: 0.52998,
        z: 0.5
    },
    [RIGHT_ELBOW]: {
        x: 0.25113,
        y: 0.55758,
        z: 0.5
    },
    [LEFT_WIRST]: {
        x: 0.77141,
        y: 0.30654,
        z: 0.5
    },
    [RIGHT_WIRST]: {
        x: 0.1,
        y: 0.7,
        z: 0.5
    },
    [LEFT_HIP]: {
        x: 0.58985,
        y: 0.36963,
        z: 0.5
    },
    [RIGHT_HIP]: {
        x: 0.42406,
        y: 0.37226,
        z: 0.5
    },
    [LEFT_KNEE]: {
        x: 0.6,
        y: 0.2,
        z: 0.5
    },
    [RIGHT_KNEE]: {
        x: 0.42218,
        y: 0.19765,
        z: 0.5
    },
    [LEFT_ANKLE]: {
        x: 0.60994,
        y: 0.07185,
        z: 0.5
    },
    [RIGHT_ANKLE]: {
        x: 0.41655,
        y: 0.05683,
        z: 0.5
    },
    [LEFT_HEEL]: {
        x: 0.60994,
        y: 0.02866,
        z: 0.5
    },
    [RIGHT_HEEL]: {
        x: 0.41091,
        y: 0.02303,
        z: 0.5
    }
}
