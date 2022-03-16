import { Box, Checkbox, FormControlLabel, FormGroup } from '@mui/material';
import { actions } from '../../../store/actions';
import { useStore } from '../../../store/use-store';

export default function MoveCenterPanel() {
    const { state, dispatch } = useStore();

    return <Box>
        <FormGroup>
            <FormControlLabel control={
                <Checkbox checked={state.config.calculations.move_points_to_center}
                    onClick={() => dispatch(actions.toggleMoveToCenter())} />
            } label="Move points to center" />
        </FormGroup>
    </Box>;
}
