import { Box, Checkbox, FormControlLabel, FormGroup, Switch } from '@mui/material';
import { actions } from '../../../store/actions';
import { useStore } from '../../../store/use-store';
import { BodyPartsCheckbox } from './utils';

export default function ThreePanel() {
    const { state, dispatch } = useStore();

    return <Box>
        <FormGroup>
            <FormControlLabel control={
                <Switch checked={state.renderOptions.ortographic} onChange={() => dispatch(actions.toggleOrtographicCamera())} />
            } label="Orthographic camera" />
        </FormGroup>
        <BodyPartsCheckbox label="Show lines"
            bodyParts={state.renderOptions.showLines}
            onChange={(bp) => dispatch(actions.setRenderingLines(bp))} />
        <BodyPartsCheckbox label="Show spheres"
            bodyParts={state.renderOptions.showSpheres}
            onChange={(bp) => dispatch(actions.setRenderingSpheres(bp))} />
        <FormGroup>
            <FormControlLabel control={
                <Checkbox checked={state.renderOptions.showAxes} onChange={() => dispatch(actions.toggleRenderingAxes())} />
            } label="Show axes" />
            <FormControlLabel control={
                <Checkbox checked={state.renderOptions.showBox} onChange={() => dispatch(actions.toggleRenderingBox())} />
            } label="Show box" />
        </FormGroup>
    </Box>;
}
