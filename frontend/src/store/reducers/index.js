// third-party
import { combineReducers } from 'redux';

// project import
import menu from './menu';
import auth from './auth';
import app from './app';

// ==============================|| COMBINE REDUCERS ||============================== //

const reducers = combineReducers({ menu, auth, app });

export default reducers;
