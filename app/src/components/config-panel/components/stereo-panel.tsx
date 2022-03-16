import { Box, TextField } from '@mui/material';
import { useEffect, useState } from 'react';
import { actions } from '../../../store/actions';
import { useStore } from '../../../store/use-store';
import { ApplyButton } from './utils';

export default function StereoPanel() {
    const { state, dispatch } = useStore();
    const [angle, setAngle] = useState('0');
    const [baseline, setBaseline] = useState('0');
    const [scale, setScale] = useState('0');

    useEffect(() => {
        const { horizontal_angle, stereo_baseline, stereo_scale } = state.config.calculations;
        setAngle(String(horizontal_angle));
        setBaseline(String(stereo_baseline));
        setScale(String(stereo_scale));
    }, [state]);

    return <Box>
        <TextField id="outlined-basic"
            label="Horizontal angle"
            variant="outlined"
            size="small"
            value={angle}
            fullWidth
            sx={{ marginBottom: '8px' }}
            onChange={(e) => setAngle(e.target.value)} />
        <TextField id="outlined-basic"
            label="Stereo baseline"
            variant="outlined"
            size="small"
            value={baseline}
            fullWidth
            sx={{ marginBottom: '8px' }}
            onChange={(e) => setBaseline(e.target.value)} />
        <TextField id="outlined-basic"
            label="Stereo multiplier"
            variant="outlined"
            size="small"
            value={scale}
            fullWidth
            sx={{ marginBottom: '8px' }}
            onChange={(e) => setScale(e.target.value)} />
        <ApplyButton onClick={() => {
            dispatch(actions.setHorizontalAngle(parseFloat(angle)));
            dispatch(actions.setStereoBaseline(parseFloat(baseline)));
            dispatch(actions.setStereoScale(parseFloat(scale)));
        }} />
    </Box>;
}
