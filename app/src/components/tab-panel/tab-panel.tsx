import React from 'react';
import Box from '@mui/material/Box';

interface TabPanelProps {
    index: number;
    value: number;
}

export default function TabPanel(props: React.PropsWithChildren<TabPanelProps>) {
    const { children, value, index, ...other } = props;

    return (
        <div
            role="tabpanel"
            hidden={value !== index}
            id={`simple-tabpanel-${index}`}
            aria-labelledby={`simple-tab-${index}`}
            {...other}
        >
            {value === index && (
                <Box sx={{ p: 3 }}>
                    {children}
                </Box>
            )}
        </div>
    );
}
