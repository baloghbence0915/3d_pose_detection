import { Box, Checkbox, FormControlLabel, FormGroup, TextField } from '@mui/material';
import { useEffect, useState } from 'react';
import { actions } from '../../../store/actions';
import { useStore } from '../../../store/use-store';
import { ApplyButton } from './utils';

export default function AlignGroundPanel() {
    const { state, dispatch } = useStore();
    const [slope, setSlope] = useState('0');
    const [bias, setBias] = useState('0');

    useEffect(() => {
        const { slope, bias } = state.config.calculations.align_ground;
        setSlope(String(slope));
        setBias(String(bias));
    }, [state]);

    return <Box sx={{marginBottom: '16px'}}>
        <FormGroup>
            <FormControlLabel control={
                <Checkbox checked={state.config.calculations.align_ground.enabled}
                    onClick={() => dispatch(actions.toggleAlignGround())} />
            } label="Align to ground" />
        </FormGroup>
        {state.config.calculations.align_ground.enabled && <>
            <TextField id="outlined-basic"
                label="Slope"
                variant="outlined"
                size="small"
                value={slope}
                fullWidth
                sx={{ marginBottom: '8px' }}
                onChange={(e) => setSlope(e.target.value)} />
            <TextField id="outlined-basic"
                label="Bias"
                variant="outlined"
                size="small"
                value={bias}
                fullWidth
                sx={{ marginBottom: '8px' }}
                onChange={(e) => setBias(e.target.value)} />
            <ApplyButton onClick={() =>
                dispatch(actions.setAlignGroundParams({ slope: parseFloat(slope), bias: parseFloat(bias) }))
            } />
        </>}
    </Box>;
}
