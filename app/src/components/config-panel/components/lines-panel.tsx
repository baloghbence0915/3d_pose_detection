import { Box, Checkbox, FormControlLabel, FormGroup } from '@mui/material';
import { actions } from '../../../store/actions';
import { useStore } from '../../../store/use-store';

export default function LinesPanel() {
    const { state, dispatch } = useStore();

    return <Box>
        <FormGroup>
            <FormControlLabel control={
                <Checkbox checked={state.config.debug.show_vert_hor_line}
                    onClick={() => dispatch(actions.toggleShowLines())} />
            } label="Show lines" />
        </FormGroup>
    </Box>;
}
