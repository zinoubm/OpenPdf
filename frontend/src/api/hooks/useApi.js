import errorHandler from 'request/errorHandler';
import axios from '../axios';
import useAuth from './useAuth';
import { useNavigate } from 'react-router-dom';
import successHandler from 'request/successHandler';

import { useDispatch } from 'react-redux';

import { updateMessages, updateIsLoading } from 'store/reducers/chat';

const useApi = () => {
  const { getToken } = useAuth();
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const currentUser = async () => {
    try {
      const response = await axios.get('users/me', {
        headers: {
          accept: 'application/json',
          Authorization: 'Bearer ' + getToken()
        }
      });

      return successHandler(response);
    } catch (err) {
      if (err.response.status === 403) navigate('/login');
      return errorHandler(err);
    }
  };

  const uploadDocument = async (file) => {
    try {
      const form = new FormData();
      form.append('file', file);

      const response = await axios.post('/documents/upsert', form, {
        headers: {
          accept: 'application/json',
          Authorization: 'Bearer ' + getToken(),
          'Content-Type': 'multipart/form-data'
        }
      });

      return successHandler(response, { notifyOnSuccess: true });
    } catch (err) {
      if (err.response.status === 403) navigate('/login');
      return errorHandler(err);
    }
  };

  const uploadDocumentStream = async (file) => {
    try {
      const form = new FormData();
      form.append('file', file);
      form.append('data', '');

      const response = await axios.post('/documents/upsert-stream', form, {
        headers: {
          accept: 'application/json',
          Authorization: 'Bearer ' + getToken(),
          'Content-Type': 'multipart/form-data',
          Filename: file.name
        },
        timeout: 2000 * 1000 // 200 seconds
      });

      return successHandler(response, { notifyOnSuccess: true });
    } catch (err) {
      if (err.response.status === 403) navigate('/login');
      return errorHandler(err);
    }
  };

  const getDocuments = async () => {
    try {
      const response = await axios.get('/documents/', {
        params: {
          skip: '0',
          limit: '100'
        },
        headers: {
          accept: 'application/json',
          Authorization: 'Bearer ' + getToken()
        }
      });
      return response.data;
    } catch (err) {
      if (err.response.status === 403) navigate('/login');
      return errorHandler(err);
    }
  };

  const getDocumentUrl = async (document_id) => {
    try {
      const response = await axios.get('/documents/document-url', {
        params: {
          document_id: document_id
        },
        headers: {
          accept: 'application/json',
          Authorization: 'Bearer ' + getToken()
        }
      });

      return response.data.url;
    } catch (err) {
      if (err.response.status === 403) navigate('/login');
      return errorHandler(err);
    }
  };

  const queryDocument = async (query, document_id) => {
    dispatch(updateMessages({ messages: { entity: 'user', message: query }, accumulate: false }));

    const headers = {
      Accept: 'application/json',
      Authorization: 'Bearer ' + getToken()
    };

    const params = new URLSearchParams({
      query: query,
      document_id: document_id
    });

    try {
      const response = await fetch(process.env.REACT_APP_BACKEND_URL + '/api/v1/documents/query-stream?' + params.toString(), {
        method: 'POST',
        headers: headers
      });

      if (!response.ok) {
        const error = new Error(`HTTP error! Status: ${response.status}`);
        error.status = response.status;
        throw error;
      }

      const stream = response.body;
      const reader = stream.getReader();
      const decoder = new TextDecoder('utf-8');

      let streamingDone = false;
      let accumulatedResponse = '';

      dispatch(updateIsLoading({ isLoading: true }));

      while (!streamingDone) {
        const { done, value } = await reader.read();

        if (done) {
          streamingDone = true;
          break;
        }
        accumulatedResponse += decoder.decode(value);
        dispatch(updateMessages({ messages: { entity: 'bot', message: accumulatedResponse }, accumulate: true }));
      }

      dispatch(updateIsLoading({ isLoading: false }));
    } catch (err) {
      console.error('Error:', err);
      if (err.status === 403) navigate('/login');
      // return errorHandler(err, err.status);
    } finally {
      dispatch(updateIsLoading({ isLoading: false }));
    }
  };

  const deleteDocument = async (documentId) => {
    try {
      const response = await axios.delete('documents/' + documentId, {
        headers: {
          accept: 'application/json',
          Authorization: 'Bearer ' + getToken()
        }
      });

      return response;
    } catch (err) {
      if (err.response.status === 403) navigate('/login');
      return errorHandler(err);
    }
  };

  return { currentUser, uploadDocument, uploadDocumentStream, getDocuments, getDocumentUrl, queryDocument, deleteDocument };
};

export default useApi;
