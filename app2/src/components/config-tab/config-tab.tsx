import { Box, Button } from '@mui/material';
import ChannelSettings from './components/channel-settings';
import SwapHorizIcon from '@mui/icons-material/SwapHoriz';
import CameraPreview from '../camera-preview/camera-preview';
import { useStore } from '../../store/use-store';
import { actions } from '../../store/actions';
import ConfigPanel from '../config-panel/config-panel';

export default function ConfigTab() {
    const { dispatch } = useStore();

    return (
        <Box>
            <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                <ChannelSettings side='left' />
                <Button variant="contained"
                    startIcon={<SwapHorizIcon />}
                    onClick={() => dispatch(actions.swapChannels())}>
                    Swap channels
                </Button>
                <ChannelSettings side='right' />
            </Box>
            <Box sx={{ position: 'relative' }}>
                <ConfigPanel mode="config" />
                <CameraPreview />
            </Box>
        </Box>
    );
}
