import { Box, Checkbox, FormControlLabel, FormGroup } from '@mui/material';
import { actions } from '../../../store/actions';
import { useStore } from '../../../store/use-store';
import { BodyPartsCheckbox } from './utils';

export default function ThreePanel() {
    const { state, dispatch } = useStore();

    return <Box>
        <BodyPartsCheckbox label="Show lines"
            bodyParts={state.renderOptions.lines}
            onChange={(bp) => dispatch(actions.setRenderingLines(bp))} />
        <BodyPartsCheckbox label="Show spheres"
            bodyParts={state.renderOptions.spheres}
            onChange={(bp) => dispatch(actions.setRenderingSpheres(bp))} />
        <FormGroup>
            <FormControlLabel control={
                <Checkbox checked={state.renderOptions.showAxes} onChange={()=>dispatch(actions.toggleRenderingAxes())}/>
            } label="Show axes" />
            <FormControlLabel control={
                <Checkbox checked={state.renderOptions.showBox} onChange={()=>dispatch(actions.toggleRenderingBox())}/>
            } label="Show box" />
        </FormGroup>
    </Box>;
}
