import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  userFullName: ' ',
  userEmail: ' '
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
