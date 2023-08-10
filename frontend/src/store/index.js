// third-party
import { configureStore } from '@reduxjs/toolkit';

// project import
import reducers from './reducers';

// ==============================|| REDUX TOOLKIT - MAIN STORE ||============================== //

// redux notes
// state -> vars
// action -> function trigger
// reducer -> function that updates the state based on payload trigered by the action

const store = configureStore({
  reducer: reducers
});

const { dispatch } = store;

export { store, dispatch };
