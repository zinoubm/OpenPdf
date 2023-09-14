import axios from '../axios';
import useAuth from './useAuth';
import { useNavigate } from 'react-router-dom';

const useApi = () => {
  const { getToken } = useAuth();
  const navigate = useNavigate();

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
      navigate('/login');
      return null;
    }
  };

  const queryDocument = async (query, document_id, messages, setMessages, setIsLoading) => {
    const headers = {
      Accept: 'application/json',
      Authorization: 'Bearer ' + getToken()
    };

    const params = new URLSearchParams({
      query: query,
      document_id: document_id
    });

    try {
      const response = await fetch('http://localhost:8000/api/v1/documents/query-stream?' + params.toString(), {
        method: 'POST',
        headers: headers
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const stream = response.body;
      const reader = stream.getReader();
      const decoder = new TextDecoder('utf-8');

      let streamingDone = false;
      let accumulatedResponse = '';
      setIsLoading(true);
      while (!streamingDone) {
        const { done, value } = await reader.read();

        if (done) {
          streamingDone = true;
          break;
        }
        accumulatedResponse += decoder.decode(value);

        setMessages([...messages, { entity: 'bot', message: accumulatedResponse }]);
      }
      setIsLoading(false);
    } catch (error) {
      console.error('Error:', error);
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
      navigate('/login');
      return null;
    }
  };

  return { getDocuments, queryDocument, deleteDocument };
};

export default useApi;
