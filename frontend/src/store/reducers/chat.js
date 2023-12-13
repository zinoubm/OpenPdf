// types
import { createSlice } from '@reduxjs/toolkit';

// initial state
const initialState = {
  messages: [],
  inputValue: '',
  isLoading: false,
  isAlert: false
};

const chat = createSlice({
  name: 'chat',
  initialState,
  reducers: {
    updateMessages: (state, action) => {
      if (action.payload.accumulate) {
        const lastMessage = state.messages.pop();
        if (lastMessage.entity === 'user') {
          state.messages = [...state.messages, lastMessage, action.payload.messages];
        } else {
          state.messages = [...state.messages, action.payload.messages];
        }
      } else {
        state.messages = [...state.messages, action.payload.messages];
      }
    },
    updateInputValue: (state, action) => {
      state.inputValue = action.payload.inputValue;
    },
    resetMessages: (state) => {
      state.messages = [];
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

export const { updateMessages, updateInputValue, updateIsLoading, updateIsAlert, resetMessages } = chat.actions;
