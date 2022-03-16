import React, { useEffect, useState } from 'react';
import Box from '@mui/material/Box';
import { Button, TextField } from '@mui/material';
import { ConnectionService } from '../../services/connection';
import LiveIcon from '../live-icon/live-icon';
import { NotificationItemType, NotificationService } from '../../services/notification-service';
import SaveButton from '../save-button/save-button';

const connectionService = ConnectionService.getInstance();
const notificationService = NotificationService.getInstance();

export default function ConnectionControllPanel() {
    const [isConnected, setIsConnected] = useState(false);
    const [host, setHost] = useState('');

    const setUpConnection = async () => {
        await connectionService.startConntection();

        if (connectionService.isConnected$.value) {
            notificationService.push({
                label: 'Connection done',
                severity: 'success',
                type: NotificationItemType.CONNECTION,
                delay: 3000
            });
        } else {
            notificationService.push({
                label: 'Connection failed',
                severity: 'error',
                type: NotificationItemType.CONNECTION,
                delay: 10000
            });
        }
    };

    useEffect(() => {
        (async () => {
            connectionService.isConnected$.subscribe(isCon => setIsConnected(isCon));

            setUpConnection();
        })()

        setHost(connectionService.getHost());
    }, []);

    const handleChangeHost = (event: React.ChangeEvent<HTMLInputElement>) => {
        setHost(event.target.value);
    };

    const handleConnect = async () => {
        ConnectionService.getInstance(host);
        setUpConnection();
    };

    const handleDisconnect = () => {
        connectionService.stopConntection();
    };

    return (
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
            {isConnected && <SaveButton />}
            {isConnected && <LiveIcon />}
            <TextField id="standard-basic" label="Host" variant="standard" value={host} onChange={handleChangeHost} />
            <Box sx={{ width: '150px', textAlign: 'center', margin: 'auto' }}>
                {isConnected
                    ? <Button variant="outlined" onClick={handleDisconnect}>Disconnect</Button>
                    : <Button variant="contained" onClick={handleConnect}>Connect</Button>}
            </Box>
        </Box>
    );
}
