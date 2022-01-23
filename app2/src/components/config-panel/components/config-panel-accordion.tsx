import { Accordion, AccordionDetails, AccordionSummary, Typography } from '@mui/material';
import React from 'react';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

interface ConfigPanelAccordionProps {
    title: string;
    expanded?: boolean;
}

export default function ConfigPanelAccordion({ title, expanded, children }: React.PropsWithChildren<ConfigPanelAccordionProps>) {
    return <Accordion className="config-panel-accordion" defaultExpanded={expanded}>
        <AccordionSummary
            expandIcon={<ExpandMoreIcon />}>
            <Typography>{title}</Typography>
        </AccordionSummary>
        <AccordionDetails>
            {children}
        </AccordionDetails>
    </Accordion>
}
