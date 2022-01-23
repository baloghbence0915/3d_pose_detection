import { AlertColor } from '@mui/material';
import { BehaviorSubject } from 'rxjs';

export enum NotificationItemType {
    CONNECTION,
    CONFIG,
    APPLY_BUTTON
}

export interface NotificationItem {
    label: string;
    severity: AlertColor;
    type?: NotificationItemType;
    delay?: number;
}

export class NotificationService {
    private static instance: NotificationService;
    public items$: BehaviorSubject<NotificationItem[]>;

    private constructor() {
        this.items$ = new BehaviorSubject<NotificationItem[]>([]);
    }

    public static getInstance() {
        if (!this.instance) {
            this.instance = new NotificationService();
        }

        return this.instance;
    }

    public push(item: NotificationItem): void {
        this.items$.next([...this.items$.value.filter(i => item.type !== undefined && item.type >= 0 ? i.type !== item.type : true), item]);
    }

    public remove(item: NotificationItem): void {
        this.items$.next(this.items$.value.filter(i => i !== item));
    }
}