import { useEffect, useRef, useState } from 'react';
import { useIsConnected } from '../../hooks/use-is-connected';
import { NOT_FOUND_PIC } from '../../not-found-pic';
import { ConnectionService } from '../../services/connection';
import { StatsService } from '../../services/stats.service';
import { Frame, Frames } from '../../types/frames';

import './camera-preview.scss';

const connectionService = ConnectionService.getInstance();
const statsService = StatsService.getInstance();

export default function CameraPreview() {
    const isConnected = useIsConnected();
    const [frames, setFrames] = useState<Frames>();
    const isLoadingRef = useRef(false);

    useEffect(() => {
        statsService.update();
    }, [frames]);

    async function getFrames() {
        isLoadingRef.current = true;
        const frames = await connectionService.getFrames()
        setFrames(frames);
        isLoadingRef.current = false;
    }

    useEffect(() => {
        if (isConnected && !isLoadingRef.current) {
            getFrames();
        }
    }, [isConnected, frames]);

    const renderSide = (frame?: Frame) => {
        if (!frame) {
            return null;
        }

        return <div className="camera-preview-container">
            <span className="camera-resolution">{frame?.res?.[0]}x{frame?.res?.[1]}</span>
            <img alt="frame" src={frame?.frame} />
        </div>;
    };

    return <div className="camera-preview">
        {renderSide(frames?.left)}
        {renderSide(frames?.right)}
    </div>
};
