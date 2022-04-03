/* eslint-disable @typescript-eslint/no-unused-vars */
import { Box } from '@mui/system';
import React, { useEffect, useMemo, useRef, useState } from 'react';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import { useIsConnected } from '../../hooks/use-is-connected';
import { ConnectionService } from '../../services/connection';
import { StatsService } from '../../services/stats.service';
import { useStore } from '../../store/use-store';
import { Points } from '../../types/points';
import BodyAngleIndicator from './components/body-angle-indicator';
import SpeedIndicator from './components/speed-indicator';

import './points-preview.scss';
import { getBox, getAxes, getOrtographicCam, getPerspectiveCam, getBodySpheres, getRigidBody } from './utils';

const connectionService = ConnectionService.getInstance();
const statsService = StatsService.getInstance();

export default function PointsPreview() {
    const { state } = useStore();
    const [points, setPoints] = useState<Points | null>();

    const { ortographic, showAxes, showBox, showLines, showSpheres } = state.renderOptions;

    const selfRef = useRef<HTMLDivElement>();

    const scene = useMemo(() => new THREE.Scene(), []);
    const renderer = useMemo(() => new THREE.WebGLRenderer(), []);
    const box = useMemo(() => getBox(), []);
    const axes = useMemo(() => getAxes(), []);
    const ortographicCam = useMemo(() => getOrtographicCam(), []);
    const perspectiveCam = useMemo(() => getPerspectiveCam(), []);
    const camera = useMemo(() => ortographic ? ortographicCam : perspectiveCam, [ortographic, ortographicCam, perspectiveCam]);
    useMemo(() => new OrbitControls(camera, renderer.domElement), [renderer, camera]);

    const cameraRef = useRef<THREE.Camera>();
    const isLoadingRef = useRef(false);
    const humanObjects = useRef<THREE.Object3D[]>([]);
    const boxObjects = useRef<THREE.Object3D[]>([]);

    useEffect(() => {
        cameraRef.current = camera;
    }, [camera]);

    useEffect(() => {
        if (showAxes) {
            scene.add(axes);
        } else {
            scene.remove(axes);
        }
    }, [scene, axes, showAxes]);

    useEffect(() => {
        if (showBox) {
            if (boxObjects.current.length) {
                scene.remove(...boxObjects.current);
            }

            scene.add(...box);

            boxObjects.current = box;
        } else {
            scene.remove(...boxObjects.current);
        }
    }, [scene, box, showBox]);

    useEffect(() => {
        renderer.setSize(window.innerWidth, window.innerHeight);

        if (selfRef.current) {
            selfRef.current.appendChild(renderer.domElement);
        }

        function onWindowResize() {
            if (cameraRef.current) {
                if (cameraRef.current instanceof THREE.PerspectiveCamera) {
                    cameraRef.current.aspect = window.innerWidth / window.innerHeight;
                    cameraRef.current.updateProjectionMatrix();
                }
            }
            renderer.setSize(window.innerWidth, window.innerHeight);
        }
        window.addEventListener('resize', onWindowResize, false);


        function animate() {
            requestAnimationFrame(animate);
            if (cameraRef.current) {
                renderer.render(scene, cameraRef.current);
            }
        }
        animate();
    }, [renderer, scene]);

    useEffect(() => {
        connectionService.startKeyPoints((k)=>{
            setPoints(k);
            statsService.update();
        });

        return () => {
            connectionService.stopStreamingKeypoints();
        };
    }, []);


    useEffect(() => {
        if (points?.points) {
            const objects = [
                ...getBodySpheres(points.points, showSpheres),
                ...getRigidBody(points.points, showLines),
                ...(state.config.debug.show_points_per_side && points.debug?.left
                    ? getRigidBody(points.debug?.left, { face: true, body: true, limbs: true }, 0xff0000)
                    : []),
                ...(state.config.debug.show_points_per_side && points.debug?.right
                    ? getRigidBody(points.debug?.right, { face: true, body: true, limbs: true }, 0x0000ff)
                    : [])
            ];

            if (humanObjects.current.length) {
                scene.remove(...humanObjects.current);
            }
            if (objects.length) {
                humanObjects.current = objects;
                scene.add(...objects);
            }
        }
    }, [scene, points, showSpheres, showLines, state.config.debug.show_points_per_side]);

    return (
        <>
            <div className="point-view" ref={selfRef as any} />
            <BodyAngleIndicator angle={points?.angle} />
            <SpeedIndicator speed={points?.speed} />
            {/* <SpeedIndicator speed={(points?.speed as any)?.[1]} asd={true} /> */}
        </>
    );
}
