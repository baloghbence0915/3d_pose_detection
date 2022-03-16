import { Box, Checkbox, FormControlLabel, FormGroup, TextField } from '@mui/material';
import { ChangeEventHandler, useEffect, useState } from 'react';
import { actions } from '../../../store/actions';
import { useStore } from '../../../store/use-store';
import { ApplyButton } from './utils';

const KEYS = ['DIM', 'K', 'D'] as const;
type Keys = typeof KEYS[0] | typeof KEYS[1] | typeof KEYS[2];

function getStringifiedProps(obj: any): any {
    return Object.entries(obj)
        .filter(([k]) => !!KEYS.includes(k as Keys))
        .map(([k, v]) => ({ [k]: JSON.stringify(v) }))
        .reduce((a, b) => ({ ...a, ...b }), {});
}

function getParsedProps(obj: any): any {
    return Object.entries(obj)
        .map(([k, v]) => ({ [k]: JSON.parse(v as any) }))
        .reduce((a, b) => ({ ...a, ...b }), {});
}

export default function UndistortionPanel() {
    const { state, dispatch } = useStore();
    const { undistortion } = state.config.camera.mods.all;

    const [params, setParams] = useState<Record<Keys, string>>(getStringifiedProps(undistortion));
    const [errors, setErrors] = useState<Record<Keys, boolean>>({ D: false, DIM: false, K: false });

    useEffect(() => {
        setParams(getStringifiedProps(undistortion));
    }, [undistortion]);

    const handleParamChange = (key: Keys): ChangeEventHandler<HTMLInputElement | HTMLTextAreaElement> => {
        return (e) => {
            const value = e.target.value;

            setParams({
                ...params,
                [key]: value
            });

            try {
                JSON.parse(value)
                setErrors({
                    ...errors,
                    [key]: false
                });
            } catch {
                setErrors({
                    ...errors,
                    [key]: true
                });
            }
        };
    };

    return <Box>
        <FormGroup>
            <FormControlLabel control={
                <Checkbox checked={undistortion.enabled}
                    onClick={() => dispatch(actions.toggleUndistortion())} />
            } label="Apply undistortion" />
        </FormGroup>
        {undistortion.enabled && <>
            {KEYS.map((k, i) => <TextField
                key={i}
                label={k}
                variant="outlined"
                size="small"
                sx={{ marginBottom: '8px' }}
                value={params[k as Keys]}
                onChange={handleParamChange(k as Keys)}
                error={errors[k as Keys]}
                helperText={errors[k as Keys] ? 'Failed to parse json' : undefined}
                fullWidth
            />)}
            <ApplyButton disabled={Object.values(errors).some(e => !!e)}
                onClick={() => dispatch(actions.setUndistortionParams(getParsedProps(params)))} />
        </>}
    </Box>;
}
