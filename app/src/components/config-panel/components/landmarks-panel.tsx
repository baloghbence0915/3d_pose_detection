import { Box, Checkbox, FormControlLabel, FormGroup } from '@mui/material';
import { actions } from '../../../store/actions';
import { useStore } from '../../../store/use-store';

export default function LandmarksPanel() {
    const { state, dispatch } = useStore();

    return <Box>
        <FormGroup>
            <FormControlLabel control={
                <Checkbox checked={state.config.debug.show_landmarks}
                    onClick={() => dispatch(actions.toggleShowLandmarks())} />
            } label="Show landmarks" />
        </FormGroup>
    </Box>;
}
