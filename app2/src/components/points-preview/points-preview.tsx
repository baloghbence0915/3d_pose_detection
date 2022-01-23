/* eslint-disable @typescript-eslint/no-unused-vars */
import React, { useEffect, useMemo, useRef } from 'react';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import { StatsService } from '../../services/stats.service';
import { BODY_CONNECTIONS, LEFT_SHOULDER } from './consts/body-parts';

import './points-preview.scss';

export default function PointsPreview() {
    const stats = useMemo(() => StatsService.getInstance(), []);

    const selfRef = useRef<HTMLDivElement>();

    useEffect(() => {
        const boxPoints = [
            new THREE.Vector3(0,0,0),
            new THREE.Vector3(0,0,1),
            new THREE.Vector3(1,0,1),
            new THREE.Vector3(1,0,0),
            new THREE.Vector3(0,1,0),
            new THREE.Vector3(0,1,1),
            new THREE.Vector3(1,1,1),
            new THREE.Vector3(1,1,0),
        ];
        const scene = new THREE.Scene();

        // const camera = new THREE.PerspectiveCamera(
        //     75,
        //     window.innerWidth / window.innerHeight,
        //     0.001,
        //     1000
        // );
        const asd = 600
        const camera = new THREE.OrthographicCamera(
            window.innerWidth / - asd,
            window.innerWidth / asd,
            window.innerHeight / asd,
            window.innerHeight / - asd,
            // -1,
            // 1,
            // -1,
            // 1,
            0.0001,
            1000
        );
        // camera.position.set(1, 1, 4);
        camera.position.set(0, 0, -0.6);
        // camera.lookAt(0, 0, 0);

        const renderer = new THREE.WebGLRenderer();
        renderer.setSize(window.innerWidth, window.innerHeight);
        (selfRef.current as any).appendChild(renderer.domElement);

        const controls = new OrbitControls(camera, renderer.domElement);

        const axesHelper = new THREE.AxesHelper(2);
        scene.add(axesHelper);

        scene.add(getLine(boxPoints[0], boxPoints[1]));
        scene.add(getLine(boxPoints[1], boxPoints[2]));
        scene.add(getLine(boxPoints[2], boxPoints[3]));
        scene.add(getLine(boxPoints[3], boxPoints[0]));

        scene.add(getLine(boxPoints[4], boxPoints[5]));
        scene.add(getLine(boxPoints[5], boxPoints[6]));
        scene.add(getLine(boxPoints[6], boxPoints[7]));
        scene.add(getLine(boxPoints[7], boxPoints[4]));

        scene.add(getLine(boxPoints[0], boxPoints[4]));
        scene.add(getLine(boxPoints[1], boxPoints[5]));
        scene.add(getLine(boxPoints[2], boxPoints[6]));
        scene.add(getLine(boxPoints[3], boxPoints[7]));


        window.addEventListener('resize', onWindowResize, false);
        function onWindowResize() {
            // camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }


        function animate() {
            requestAnimationFrame(animate);
            renderer.render(scene, camera);
        }

        animate();

        let lines: any[] = [];

        async function reguestPoints() {
            const json = await fetch('http://192.168.100.24:8080/api/points').then(r => r.json());
            if (json?.left?.[0] && json?.right?.[0]) {
                scene.remove(...lines);
                lines = [
                    // ...(json.left ? renderRigidBody(json.left, 0x00ffff) : []),
                    // ...(json.right ? renderRigidBody(json.right, 0xffff00) : []),
                    ...(!!Object.keys(json.middle).length ? renderRigidBody(json.middle, 0xff0000) : []),
                ];
                scene.add(...lines);    
            }
        }

        let isCancelled = { value: false };

        (async () => {
            while (!isCancelled.value) {
                await reguestPoints()
                stats.update();
            }
        })()

        return () => {
            isCancelled.value = true;
        };
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    return (
        <div className="point-view" ref={selfRef as any} />
    );
}

function getLine(v1: THREE.Vector3, v2: THREE.Vector3, color: number = 0x00ffff) {
    const material = new THREE.LineBasicMaterial({ color });
    const points = [];

    points.push(v1);
    points.push(v2);

    const geometry = new THREE.BufferGeometry().setFromPoints(points);
    const line = new THREE.Line(geometry, material);

    return line;
}

function getSphere(v: THREE.Vector3) {
    const geometry = new THREE.SphereGeometry( 0.01, 32, 16 );
    const material = new THREE.MeshBasicMaterial( { color: 0xffff00 } );
    const sphere = new THREE.Mesh( geometry, material );
    sphere.position.set(v.x, v.y, v.z);

    return sphere;
}

function renderRigidBody(points: any, color: number) {
    const lines: any[] = [];

    Object.entries(BODY_CONNECTIONS).forEach(([id, neighb]) => {
        // const nn = Object.entries(n).filter(([idd]) => +idd > +id).map(([idd, l]) => ({ [idd]: l })).reduce((a, b) => ({ ...a, ...b }), {});
        // const nnId = Object.keys(nn);

        Object.keys(neighb).forEach((idd) => {
            const v1 = points[+id];
            const v2 = points[+idd];
            lines.push(getLine(new THREE.Vector3(v1.x, v1.y, v1.z), new THREE.Vector3(v2.x, v2.y, v2.z), color));
            lines.push(getSphere(new THREE.Vector3(v1.x, v1.y, v1.z)));
            lines.push(getSphere(new THREE.Vector3(v2.x, v2.y, v2.z)));
        });
    });

    // Object.values(points).map((v: any) => {
    //     lines.push(getSphere(new THREE.Vector3(v.x, v.y, v.z)));
    // });

    return lines;
}

function renderNormalizedRigidBody(points: any, color: number) {
    const basePoint = LEFT_SHOULDER;
    const newPoints: any = {
        [LEFT_SHOULDER]: points[LEFT_SHOULDER]
    };

    Object.entries(BODY_CONNECTIONS).forEach(([id, neighb]) => {
        Object.entries(neighb).forEach(([idd, length]) => {
            let v1 = points[+id]; // From
            const vv1 = new THREE.Vector3(v1.x, v1.y, v1.z);
            let v2 = points[+idd]; // To
            const vv2 = new THREE.Vector3(v2.x, v2.y, v2.z);
            vv2.sub(vv1);
            vv2.setLength(length);

            vv2.add(newPoints[+id]);
            newPoints[idd] = vv2;
        });
    });


    return renderRigidBody(newPoints, color);
}
