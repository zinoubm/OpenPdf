// third-party
import { combineReducers } from 'redux';

// project import
import menu from './menu';
import auth from './auth';
import app from './app';
import chat from './chat';

// ==============================|| COMBINE REDUCERS ||============================== //

const reducers = combineReducers({ menu, auth, app, chat });

export default reducers;
