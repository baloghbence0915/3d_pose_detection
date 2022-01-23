import { Box, Button, Checkbox, FormControlLabel } from '@mui/material';
import CheckIcon from '@mui/icons-material/Check';
import { NotificationItemType, NotificationService } from '../../../services/notification-service';
import { BodyParts } from '../../../store/state';
import React, { useEffect, useState } from 'react';

const notificatonService = NotificationService.getInstance();

interface ApplyButtonProps {
    onClick?: VoidFunction;
    disabled?: boolean;
}

export function ApplyButton({ onClick, disabled }: ApplyButtonProps) {
    return <Button variant="contained" startIcon={<CheckIcon />} disabled={disabled}
        onClick={() => {
            onClick && onClick();

            notificatonService.push({
                label: `Don't forget to save changes on top, in order to propagate config to server`,
                severity: 'warning',
                delay: 5000,
                type: NotificationItemType.APPLY_BUTTON
            });
        }}>
        Apply
    </Button>
}

interface BodyPartsCheckboxProps {
    label: string;
    bodyParts: BodyParts;
    onChange: (bodyParts: BodyParts) => void;
}

export function BodyPartsCheckbox({ label, bodyParts, onChange }: BodyPartsCheckboxProps) {
    const handleChangeRoot = (event: React.ChangeEvent<HTMLInputElement>) => {
        const checked = event.target.checked;
        onChange({ face: checked, body: checked, limbs: checked });
    };

    const handleChangePart = (part: keyof BodyParts) => (event: React.ChangeEvent<HTMLInputElement>) => {
        onChange({ ...bodyParts, [part]: event.target.checked });
    };

    return (
        <Box>
            <FormControlLabel
                label={label}
                control={
                    <Checkbox
                        checked={bodyParts.face && bodyParts.body && bodyParts.limbs}
                        indeterminate={Object.values(bodyParts).some(ch => !!ch) && Object.values(bodyParts).some(ch => !ch)}
                        onChange={handleChangeRoot}
                    />
                }
            />
            <Box sx={{ display: 'flex', flexDirection: 'column', ml: 3 }}>
                <FormControlLabel
                    label="Face"
                    control={<Checkbox checked={bodyParts.face} onChange={handleChangePart('face')} />}
                />
                <FormControlLabel
                    label="Body"
                    control={<Checkbox checked={bodyParts.body} onChange={handleChangePart('body')} />}
                />
                <FormControlLabel
                    label="Limbs"
                    control={<Checkbox checked={bodyParts.limbs} onChange={handleChangePart('limbs')} />}
                />
            </Box>
        </Box>
    );
}