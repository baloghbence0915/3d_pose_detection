import { Box, Checkbox, FormControlLabel, FormGroup } from '@mui/material';
import { actions } from '../../../store/actions';
import { useStore } from '../../../store/use-store';

export default function PointsDebugPanel() {
    const { state, dispatch } = useStore();

    return <Box>
        <FormGroup>
            <FormControlLabel control={
                <Checkbox checked={state.config.debug.show_points_per_side}
                    onClick={() => dispatch(actions.toggleShowSideBySide())} />
            } label="Show side-by-side information" />
        </FormGroup>
    </Box>;
}
