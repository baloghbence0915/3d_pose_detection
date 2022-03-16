import { IconButton } from '@mui/material';
import { ConnectionService } from '../../services/connection';
import { NotificationItemType, NotificationService } from '../../services/notification-service';
import SaveIcon from '@mui/icons-material/Save';
import { useStore } from '../../store/use-store';
import { actions } from '../../store/actions';

const connectionService = ConnectionService.getInstance();
const notificationService = NotificationService.getInstance();

export default function SaveButton() {
    const { state, dispatch } = useStore();

    const handleSaveConfig = async () => {
        const newConfig = await connectionService.setConfig(state.config).catch(() => null);

        if (newConfig) {
            notificationService.push({
                label: 'Config was saved',
                severity: 'success',
                delay: 3000,
                type: NotificationItemType.CONFIG
            });

            dispatch(actions.setConfig(newConfig));
        } else {
            notificationService.push({
                label: 'Failed to save config',
                severity: 'error',
                delay: 10000,
                type: NotificationItemType.CONFIG
            });
        }
    };

    return (
        <IconButton color="primary" component="span" sx={{ marginRight: '8px' }}
            onClick={handleSaveConfig}>
            <SaveIcon />
        </IconButton>
    );
}
