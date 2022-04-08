import React from 'react';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Box from '@mui/material/Box';
import TabPanel from '../tab-panel/tab-panel';
import ConfigTab from '../config-tab/config-tab';
import ConnectionControllPanel from '../connection-controll-panel/connection-controll-panel';
import PointsPreview from '../points-preview/points-preview';
import Playground from '../playground/playground';

export default function Navigation() {
    const [tabIndex, setTabIndex] = React.useState(0);

    const handleChange = (event: React.SyntheticEvent, newValue: number) => {
        setTabIndex(newValue);
    };

    return (
        <Box sx={{ width: '100%' }}>
            <Box sx={{ borderBottom: 1, borderColor: 'divider', display: 'flex', justifyContent: 'space-between',
                padding: '0 4rem' }}>
                <Tabs value={tabIndex} sx={{ width: '50%' }} onChange={handleChange}>
                    <Tab label="Config" />
                    <Tab label="Playground" />
                </Tabs>
                <ConnectionControllPanel />
            </Box>
            <TabPanel value={tabIndex} index={0}>
                <ConfigTab />
            </TabPanel>
            <TabPanel value={tabIndex} index={1}>
                <Playground />
            </TabPanel>
        </Box>
    );
}
