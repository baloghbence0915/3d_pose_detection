import { Box, Checkbox, FormControl, FormControlLabel, FormGroup, InputLabel, MenuItem, Select, SelectChangeEvent } from '@mui/material';
import React, { useEffect, useState } from 'react';
import { useIsConnected } from '../../../hooks/use-is-connected';
import { ConnectionService } from '../../../services/connection';
import { actions } from '../../../store/actions';
import { useStore } from '../../../store/use-store';

const connectionService = ConnectionService.getInstance();

export default function ReplayingPanel() {
    const isConnected = useIsConnected();
    const { state, dispatch } = useStore();
    const [recordings, setRecordings] = useState<string[]>([]);
    const isReplaying = state.config.playback.playing.enabled;

    useEffect(() => {
        if (isConnected && isReplaying) {
            connectionService.getRecordings().then(r => !!r && setRecordings(r));
        }
    }, [isConnected, isReplaying]);

    return <Box>
        <FormGroup>
            <FormControlLabel control={
                <Checkbox checked={isReplaying}
                    onClick={() => dispatch(actions.toggleIsReplaying())} />
            } label="Is replaying?" />
        </FormGroup>
        {isReplaying && <FormControl fullWidth>
            <InputLabel id="demo-simple-select-label">Select recording</InputLabel>
            <Select
                labelId="demo-simple-select-label"
                id="demo-simple-select"
                value={state.config.playback.playing.file}
                label="Select recording"
                autoWidth
                size="small"
                onChange={(e) => dispatch(actions.setRecording(e.target.value))}
            >
                <MenuItem value={0}>(null)</MenuItem>
                {recordings.map((r, i) => <MenuItem key={i} value={r}>{r}</MenuItem>)}
            </Select>
        </FormControl>}
    </Box>
}
