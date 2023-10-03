// types
import { createSlice } from '@reduxjs/toolkit';

// initial state
const initialState = {
  documentId: null,
  documentName: 'Please select a document.',
  refreshKey: 0
};

const app = createSlice({
  name: 'app',
  initialState,
  reducers: {
    activeDocumentId: (state, action) => {
      state.documentId = action.payload.documentId;
    },
    activeDocumentName: (state, action) => {
      state.documentName = action.payload.documentName;
    },
    updateRefresKey: (state) => {
      state.refreshKey += 1;
    }
  }
});

export default app.reducer;

export const { activeDocumentId, activeDocumentName, updateRefresKey } = app.actions;
