import { Box, Button, TextField, capitalize } from '@mui/material';
import Rotate90DegreesCcwIcon from '@mui/icons-material/Rotate90DegreesCcw';
import { Side } from '../../../types/side';
import { useStore } from '../../../store/use-store';
import { actions } from '../../../store/actions';

interface ChannelSettingsProps {
    side: Side;
}

export default function ChannelSettings({ side }: ChannelSettingsProps) {
    const { state, dispatch } = useStore();



    return (
        <Box sx={{ display: 'flex', width: '350px', justifyContent: 'space-between' }}>
            <TextField id="outlined-basic"
                label={`${capitalize(side)} channel`}
                variant="outlined"
                size="small"
                value={state.config.camera.channels[side]}
                onChange={(e) => dispatch(actions.changeChannel({ side, channel: parseFloat(e.target.value) || 0 }))} />
            <Button variant="contained"
                startIcon={<Rotate90DegreesCcwIcon />}
                onClick={() => dispatch(actions.rotateChannel(side))}>
                Rotate
            </Button>
        </Box>
    );
}
