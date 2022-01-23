import { Box } from '@mui/material';
import React from 'react';
import RecordingPanel from './components/recording-panel';
import ReplayingPanel from './components/replaying-panel';
import './config-panel.scss';
import ConfigPanelAccordion from './components/config-panel-accordion';
import LandmarksPanel from './components/landmarks-panel';
import LinesPanel from './components/lines-panel';
import UndistortionPanel from './components/undistortion-panel';
import StereoPanel from './components/stereo-panel';
import AlignGroundPanel from './components/align-ground-panel';
import NormalizeHeightPanel from './components/normalize-height-panel';
import MoveCenterPanel from './components/move-center-panel';
import OffsetPanel from './components/offset-panel';
import ThreePanel from './components/three-panel';

interface ConfigPanelProps {
    mode: 'config' | 'threejs'
}

export default function ConfigPanel({ mode }: ConfigPanelProps) {
    const isConfigMode = mode === 'config';

    return <Box className={`config-panel ${mode}`}>
        {isConfigMode && <ConfigPanelAccordion title="Playback & recording">
            <ReplayingPanel />
            <RecordingPanel />
        </ConfigPanelAccordion>}
        {isConfigMode && <ConfigPanelAccordion title="Debug settings">
            <LandmarksPanel />
            <LinesPanel />
        </ConfigPanelAccordion>}
        {isConfigMode && <ConfigPanelAccordion title="Undistortion settings">
            <UndistortionPanel />
        </ConfigPanelAccordion>}
        {!isConfigMode && <ConfigPanelAccordion title="Stereo settings">
            <StereoPanel />
        </ConfigPanelAccordion>}
        {!isConfigMode && <ConfigPanelAccordion title="Tools">
            <AlignGroundPanel />
            <NormalizeHeightPanel />
            <OffsetPanel />
            <MoveCenterPanel />
        </ConfigPanelAccordion>}
        {!isConfigMode && <ConfigPanelAccordion title="Three.js settings" expanded>
            <ThreePanel />
        </ConfigPanelAccordion>}
    </Box>
}