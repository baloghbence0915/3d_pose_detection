import { useEffect, useRef } from 'react';
import { useIsConnected } from '../../hooks/use-is-connected';
import { NOT_FOUND_PIC } from '../../not-found-pic';
import { ConnectionService } from '../../services/connection';

import './camera-preview.scss';

const connectionService = ConnectionService.getInstance()

export default function CameraPreview() {
    const isConnected = useIsConnected();
    const leftFrameRef = useRef<HTMLImageElement>(null);
    const rightFrameRef = useRef<HTMLImageElement>(null);

    useEffect(() => {
        if (leftFrameRef.current && rightFrameRef.current) {
            if (isConnected) {
                leftFrameRef.current.src = `http://${connectionService.getHost()}/api/stream/frame/left`;
                rightFrameRef.current.src = `http://${connectionService.getHost()}/api/stream/frame/right`;
            } else {
                leftFrameRef.current.src = NOT_FOUND_PIC;
                rightFrameRef.current.src = NOT_FOUND_PIC;
            }
        }
    }, [isConnected]);

    useEffect(() => {
        const imgLeft = leftFrameRef.current;
        const imgRight = rightFrameRef.current;

        return () => {
            if (imgLeft && imgRight) {
                imgLeft.src = null as any;
                imgRight.src = null as any;
            }
        };
    }, []);

    return <div className="camera-preview">
        <div className="camera-preview-container">
            <img alt="left-frame" src={NOT_FOUND_PIC} ref={leftFrameRef} />
        </div>
        <div className="camera-preview-container">
            <img alt="right-frame" src={NOT_FOUND_PIC} ref={rightFrameRef} />
        </div>
    </div>
};
