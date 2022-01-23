import './App.scss';
import Navigation from '../navigation/navigation';
import Notifications from '../notifications/notifications';
import { useEffect, useReducer } from 'react';
import { INITIAL_STATE } from '../../store/state';
import { appReducer, appReducerWithLogger } from '../../store/reducer';
import { ConnectionService } from '../../services/connection';
import { actions } from '../../store/actions';
import { StoreContext } from '../../store/store-context';
import { useIsConnected } from '../../hooks/use-is-connected';
import StatsContainer from '../stats/stats-container';

const connectionService = ConnectionService.getInstance();

function App() {
  const [state, dispatch] = useReducer(appReducerWithLogger, INITIAL_STATE);
  const isConnected = useIsConnected();

  useEffect(() => {
    async function getConfig() {
      const config = await connectionService.getConfig();
      dispatch(actions.setConfig(config));
    }

    if (isConnected) {
      getConfig()
    }
  }, [isConnected]);

  return <StoreContext.Provider value={{ state, dispatch }}>
    <div className="app">
      <Navigation />
      <Notifications />
      <StatsContainer />
    </div>
  </StoreContext.Provider>;
}

export default App;
