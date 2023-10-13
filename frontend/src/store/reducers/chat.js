// types
import { createSlice } from '@reduxjs/toolkit';

// initial state
const initialState = {
  messages: [],
  newMessage: '',
  inputValue: '',
  isLoading: false,
  isAlert: false
};

const chat = createSlice({
  name: 'chat',
  initialState,
  reducers: {
    updateMessages: (state, action) => {
      state.messages = action.payload.messages;
    },
    updateNewMessage: (state, action) => {
      state.newMessage = action.payload.newMessage;
    },
    updateInputValue: (state, action) => {
      state.inputValue = action.payload.inputValue;
    },
    updateIsLoading: (state, action) => {
      state.isLoading = action.payload.isLoading;
    },
    updateIsAlert: (state, action) => {
      state.isAlert = action.payload.isAlert;
    }
  }
});

export default chat.reducer;

export const { updateMessages, updateNewMessage, updateInputValue, updateIsLoading, updateIsAlert } = chat.actions;
