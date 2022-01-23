import { Box } from '@mui/material';
import { useEffect, useRef } from 'react';
import { StatsService } from '../../services/stats.service';

function StatsContainer() {
    const selfRef = useRef<HTMLDivElement>();

    useEffect(() => {
        const statService = StatsService.getInstance();
        const stats = statService.getStatsObject();
        selfRef.current?.appendChild(stats.dom);
        (stats.dom.style as any) = {};
    }, []);

    return <Box sx={{ position: 'fixed', bottom: '0', right: '0' }} ref={selfRef as any} />
}

export default StatsContainer;
