import React from 'react';
import { Actions } from './actions';
import { State } from './state';

interface Store {
    state: State;
    dispatch: React.Dispatch<Actions>;
}

export const StoreContext = React.createContext<Store>({} as any);
