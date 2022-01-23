import React, { useEffect, useRef, useState } from 'react';
import Alert from '@mui/material/Alert';
import Stack from '@mui/material/Stack';
import { NotificationItem, NotificationService } from '../../services/notification-service';

const notificationService = NotificationService.getInstance();

export default function Notifications() {
  const [items, setItems] = useState<NotificationItem[]>([]);
  const timers = useRef(new Set<NotificationItem>());

  const handleRemove = (item: NotificationItem) => {
    notificationService.remove(item);
  };

  useEffect(() => {
    notificationService.items$.subscribe(items => setItems([...items].reverse()));
  }, []);

  useEffect(() => {
    for (const i of items) {
      if (i.delay && !timers.current.has(i)) {
        timers.current.add(i);

        setTimeout(() => {
          handleRemove(i);
          timers.current.delete(i);
        }, i.delay);
      }
    }
  }, [items]);

  return (
    <Stack sx={{ width: '400px', position: 'fixed', top: '6rem', right: '6rem' }} spacing={2}>
      {items.map((item, i) => <Alert key={i}
        severity={item.severity}
        onClose={() => handleRemove(item)}>
        {item.label}
      </Alert>)}
    </Stack>
  );
}