
type Point = { x: number, y: number, z: number };

export type PointsArray = Record<number, Point>

export interface Points {
    points: PointsArray;
    angle: number;
    debug?: {
        ratio: number,
        left: PointsArray,
        right: PointsArray
    }
}