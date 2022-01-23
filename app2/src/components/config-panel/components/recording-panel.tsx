import { Box, Checkbox, FormControlLabel, FormGroup } from '@mui/material';
import React from 'react';
import { actions } from '../../../store/actions';
import { useStore } from '../../../store/use-store';

export default function RecordingPanel() {
    const { state, dispatch } = useStore();

    return <Box>
        <FormGroup>
            <FormControlLabel control={
                <Checkbox checked={state.config.playback.recoding}
                    disabled={state.config.playback.playing.enabled}
                    onClick={() => dispatch(actions.toggleIsRecording())} />
            } label="Is recording?" />
        </FormGroup>
    </Box>;
}
