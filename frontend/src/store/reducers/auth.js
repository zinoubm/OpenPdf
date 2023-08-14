// types
import { createSlice } from '@reduxjs/toolkit';

// initial state
const initialState = {
  userFullName: 'Test User',
  userEmail: 'user@test.com'
};

const auth = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    activeUserEmail: (state, action) => {
      state.userEmail = action.payload.userEmail;
    },
    activeUserFullName: (state, action) => {
      state.userFullName = action.payload.userFullName;
    }
  }
});

export default auth.reducer;

export const { activeUserEmail, activeUserFullName } = auth.actions;
