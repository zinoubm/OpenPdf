import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  userFullName: ' ',
  userEmail: ' ',
  userId: 0
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
    },
    activeUserId: (state, action) => {
      state.userId = action.payload.userId;
    }
  }
});

export default auth.reducer;

export const { activeUserEmail, activeUserFullName, activeUserId } = auth.actions;
