import errorHandler from 'request/errorHandler';
import axios from '../axios';
import useAuth from './useAuth';
import { useNavigate } from 'react-router-dom';
import successHandler from 'request/successHandler';
import { notification } from 'antd';
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

  const getPaymentSummary = async () => {
    try {
      const response = await axios.get('/stripe/summary', {
        headers: {
          accept: 'application/json',
          Authorization: 'Bearer ' + getToken()
        }
      });

      return successHandler(response);
    } catch (err) {
      return errorHandler(err);
    }
  };

  const getCustomerPortalUrl = async () => {
    try {
      const response = await axios.get('/stripe/customer-portal', {
        headers: {
          accept: 'application/json',
          Authorization: 'Bearer ' + getToken()
        }
      });

      return response.data.url;
    } catch (err) {
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
      if (err.status === 402) {
        notification.config({
          duration: 10
        });
        notification.info({
          message: `Plan Limits Reached.`,
          description: 'You reached your subscription limits, Please Upgrade to get more quotas.',
          placement: 'bottomRight'
        });
      }
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
      if (err.response.status === 402) {
        notification.config({
          duration: 10
        });
        notification.info({
          message: `Upload Limits Reached.`,
          description: 'You reached your subscription Uploads limits, Please Upgrade to get more quotas.',
          placement: 'bottomRight'
        });
      }
      return null;
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

  const queryDocument = async (query, messages, document_id) => {
    const headers = {
      'Content-Type': 'application/json',
      Accept: 'application/json',
      Authorization: 'Bearer ' + getToken()
    };

    const data = {
      query: query,
      messages: messages,
      document_id: document_id
    };

    try {
      const response = await fetch(process.env.REACT_APP_BACKEND_URL + '/api/v1/documents/query-stream', {
        body: JSON.stringify(data),
        headers: headers,
        method: 'POST'
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
        dispatch(updateMessages({ messages: { entity: 'system', message: accumulatedResponse }, accumulate: true }));
      }

      dispatch(updateIsLoading({ isLoading: false }));
    } catch (err) {
      console.error('Error:', err);
      if (err.status === 403) navigate('/login');
      if (err.status === 402) {
        notification.config({
          duration: 10
        });
        notification.info({
          message: `Plan Limits Reached.`,
          description: 'You reached your subscription limits, Please Upgrade to get more quotas.',
          placement: 'bottomRight'
        });
      }
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

  const getQuestionSuggestions = async (document_id) => {
    try {
      const response = await axios.get('/documents/question-suggestions', {
        params: {
          document_id: document_id
        },
        headers: {
          accept: 'application/json',
          Authorization: 'Bearer ' + getToken()
        }
      });

      return response.data.suggestions;
    } catch (err) {
      if (err.response.status === 403) navigate('/login');
      return errorHandler(err);
    }
  };

  const getDocumentStatus = async (document_id) => {
    try {
      const response = await axios.get('/documents/status', {
        params: {
          document_id: document_id
        },
        headers: {
          accept: 'application/json',
          Authorization: 'Bearer ' + getToken()
        }
      });

      return response.data.status;
    } catch (err) {
      if (err.response.status === 403) navigate('/login');
      return errorHandler(err);
    }
  };

  const redeemCode = async (code) => {
    try {
      const response = await axios.post('/users/code', '', {
        params: {
          code: code
        },
        headers: {
          accept: 'application/json',
          Authorization: 'Bearer ' + getToken(),
          'content-type': 'application/x-www-form-urlencoded'
        }
      });

      return successHandler(response, { notifyOnSuccess: true });
    } catch (err) {
      if (err.response.status === 403) navigate('/login');
      if (err.response.status === 422) {
        notification.config({
          duration: 10
        });
        notification.error({
          message: `Invalid Code.`,
          description: 'This code is not valid, please enter a valid one.',
          placement: 'bottomRight'
        });
      }
      if (err.response.status === 409) {
        notification.config({
          duration: 10
        });
        notification.error({
          message: `Code already used.`,
          description: 'This code is already used, please purchase more or use a fresh one.',
          placement: 'bottomRight'
        });
      }
      // return errorHandler(err);
    }
  };

  return {
    currentUser,
    getPaymentSummary,
    getCustomerPortalUrl,
    uploadDocument,
    uploadDocumentStream,
    getDocuments,
    getDocumentUrl,
    queryDocument,
    getQuestionSuggestions,
    deleteDocument,
    getDocumentStatus,
    redeemCode
  };
};

export default useApi;
