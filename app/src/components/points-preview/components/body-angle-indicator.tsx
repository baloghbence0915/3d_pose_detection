import { Box } from '@mui/system';

interface PointsPreview {
    angle?: number;
}

export default function BodyAngleIndicator({ angle }: PointsPreview) {
    const degree = (angle || 0) * (180 / Math.PI);

    return (
        <Box sx={{
            position: 'fixed',
            top: '50px',
            left: '32px',
            fontSize: '32px'
        }}>
            <Box
                sx={{
                    color: 'white',
                }}>
                Angle: {degree}°
            </Box>
            <Box sx={{
                width: '100px',
                height: '10px',
                transform: `rotate(${degree + 180}deg)`,
                display: 'flex',
                justifyContent: 'center',
                position: 'relative',
                top: '50px'
            }}>
                <Box sx={{
                    height: '50px',
                    width: '4px',
                    backgroundColor: 'white',
                }} />
                <Box sx={{
                    width: '10px',
                    height: '10px',
                    backgroundColor: 'white',
                    borderRadius: '50%',
                    position: 'absolute'
                }} />
            </Box>
        </Box>
    );
}
