import { Box } from '@mui/material';

interface SpeedIndicatorProps {
    speed?: number;
}

export default function SpeedIndicator({ speed = 0 }: SpeedIndicatorProps) {
    return (
        <Box sx={{
            position: 'fixed',
            top: '150px',
            left: '32px',

        }}>
            <Box
                sx={{
                    color: 'white',
                }}>
                Speed: {speed}
            </Box>
            <Box sx={{
                width: '100px',
                height: '50px',
                display: 'flex',
                justifyContent: 'center',
                position: 'relative',
                top: '8px'
            }}>
                <Box sx={{
                    height: '50px',
                    width: '10px',
                    border: '1px white solid'
                }} />
                <Box sx={{
                    height: `${speed * 50}px`,
                    width: '10px',
                    background: 'red',
                    position: 'absolute',
                    bottom: '-1px'
                }} />
            </Box>
        </Box>
    );
}