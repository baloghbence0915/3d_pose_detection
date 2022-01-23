import { Box, Checkbox, FormControlLabel, FormGroup, TextField } from '@mui/material';
import { useEffect, useState } from 'react';
import { actions } from '../../../store/actions';
import { useStore } from '../../../store/use-store';
import { ApplyButton } from './utils';

export default function OffsetPanel() {
    const { state, dispatch } = useStore();
    const [x, setX] = useState('0');
    const [z, setZ] = useState('0');

    useEffect(() => {
        const { x, z } = state.config.calculations.offset;
        setX(String(x));
        setZ(String(z));
    }, [state]);

    return <Box sx={{marginBottom: '16px'}}>
        <FormGroup>
            <FormControlLabel control={
                <Checkbox checked={state.config.calculations.offset.enabled}
                    onClick={() => dispatch(actions.toggleOffsets())} />
            } label="Apply offset" />
        </FormGroup>
        {state.config.calculations.offset.enabled && <>
            <TextField id="outlined-basic"
                label="x offset"
                variant="outlined"
                size="small"
                value={x}
                fullWidth
                sx={{ marginBottom: '8px' }}
                onChange={(e) => setX(e.target.value)} />
            <TextField id="outlined-basic"
                label="z offset"
                variant="outlined"
                size="small"
                value={z}
                fullWidth
                sx={{ marginBottom: '8px' }}
                onChange={(e) => setZ(e.target.value)} />
            <ApplyButton onClick={() =>
                dispatch(actions.setOffsetParams({ x: parseFloat(x), z: parseFloat(z) }))
            } />
        </>}
    </Box>;
}
