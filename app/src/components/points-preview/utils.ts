import * as THREE from 'three';
import { BodyParts } from '../../store/state';
import { PointsArray } from '../../types/points';
import { BODY_CONNECTIONS, BODY_POINTS, FACE_POINTS, LIMB_POINTS } from './consts/body-parts';

import './points-preview.scss';

export function getPerspectiveCam() {
    const camera = new THREE.PerspectiveCamera(
        75,
        window.innerWidth / window.innerHeight,
        0.001,
        1000
    );
    camera.position.set(1, 1, 4);
    camera.lookAt(0, 0, 0);
    return camera;
}

export function getOrtographicCam() {
    const divider = 600
    const camera = new THREE.OrthographicCamera(
        window.innerWidth / - divider,
        window.innerWidth / divider,
        window.innerHeight / divider,
        window.innerHeight / - divider,
        -1000,
        1000
    );
    camera.position.set(0.8, 0, 0);
    return camera;
}

export function getBox(ratio: number = 1) {
    const boxPoints = [
        new THREE.Vector3(0, 0, 0),
        new THREE.Vector3(0, 0, 1),
        new THREE.Vector3(1, 0, 1),
        new THREE.Vector3(1, 0, 0),
        new THREE.Vector3(0, ratio, 0),
        new THREE.Vector3(0, ratio, 1),
        new THREE.Vector3(1, ratio, 1),
        new THREE.Vector3(1, ratio, 0),
    ];

    const borders = [];
    borders.push(getLine(boxPoints[0], boxPoints[1]));
    borders.push(getLine(boxPoints[1], boxPoints[2]));
    borders.push(getLine(boxPoints[2], boxPoints[3]));
    borders.push(getLine(boxPoints[3], boxPoints[0]));

    borders.push(getLine(boxPoints[4], boxPoints[5]));
    borders.push(getLine(boxPoints[5], boxPoints[6]));
    borders.push(getLine(boxPoints[6], boxPoints[7]));
    borders.push(getLine(boxPoints[7], boxPoints[4]));

    borders.push(getLine(boxPoints[0], boxPoints[4]));
    borders.push(getLine(boxPoints[1], boxPoints[5]));
    borders.push(getLine(boxPoints[2], boxPoints[6]));
    borders.push(getLine(boxPoints[3], boxPoints[7]));

    return borders;
}

export function getAxes() {
    return new THREE.AxesHelper(2);
}

export function getLine(v1: THREE.Vector3, v2: THREE.Vector3, color: number = 0x00ffff) {
    const material = new THREE.LineBasicMaterial({ color });
    const points = [];

    points.push(v1);
    points.push(v2);

    const geometry = new THREE.BufferGeometry().setFromPoints(points);
    const line = new THREE.Line(geometry, material);

    return line;
}

export function getSphere(v: THREE.Vector3, color: number = 0xffff00) {
    const geometry = new THREE.SphereGeometry(0.01, 32, 16);
    const material = new THREE.MeshBasicMaterial({ color });
    const sphere = new THREE.Mesh(geometry, material);
    sphere.position.set(v.x, v.y, v.z);

    return sphere;
}

export function getRigidBody(points: any, bodyParts: BodyParts, color?: number): THREE.Object3D[] {
    const lineSet = new Set<string>();
    const allowed = getAllowedPoints(bodyParts);

    return Object.entries(BODY_CONNECTIONS)
        .map(([id, next]) =>
            Object.keys(next).map((idd) => {
                const id1 = +id;
                const id2 = +idd;

                if (!allowed.includes(id1) || !allowed.includes(id2)) {
                    return null;
                }

                if (lineSet.has(`${id}_${idd}`)) {
                    return null;
                } else {
                    lineSet.add(`${id}_${idd}`);
                    lineSet.add(`${idd}_${id}`);
                }

                const v1 = points[id1];
                const v2 = points[id2];
                return v1 && v2 && getLine(new THREE.Vector3(v1.x, v1.y, v1.z), new THREE.Vector3(v2.x, v2.y, v2.z), color);
            })
        )
        .flat()
        .filter(Boolean) as any;
}

export function getBodySpheres(points: PointsArray, bodyParts: BodyParts): THREE.Object3D[] {
    const allowed = getAllowedPoints(bodyParts);

    return Object.entries(points)
        .filter(([id]) => allowed.includes(+id))
        .map(([id, p]) => getSphere(new THREE.Vector3(p.x, p.y, p.z)));
}

function getAllowedPoints(bodyParts: BodyParts): number[] {
    return [
        ...(bodyParts.face ? FACE_POINTS : []),
        ...(bodyParts.body ? BODY_POINTS : []),
        ...(bodyParts.limbs ? LIMB_POINTS : []),
    ];
}
