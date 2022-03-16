import { useState, useEffect } from 'react';
import { ConnectionService } from '../services/connection';

const connectionService = ConnectionService.getInstance();

export function useIsConnected() {
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    (async () => {
      connectionService.isConnected$.subscribe(isCon => setIsConnected(isCon));
    })()
  }, []);

  return isConnected;
}
