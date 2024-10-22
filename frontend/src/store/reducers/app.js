import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  documentId: null,
  documentName: 'Please select a document.',
  refreshKey: 0,
  selectedKeys: null,
  paymentSummary: null
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
    },
    activeSelectedKeys: (state, action) => {
      state.selectedKeys = action.payload.selectedKeys;
    },
    activePaymentSummary: (state, action) => {
      state.paymentSummary = action.payload.paymentSummary;
    }
  }
});

export default app.reducer;

export const { activeDocumentId, activeDocumentName, updateRefresKey, activeSelectedKeys, activePaymentSummary } = app.actions;
