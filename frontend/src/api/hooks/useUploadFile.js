import axios from '../axios';
// import react from 'react';
import useAuth from './useAuth';
import { useNavigate } from 'react-router-dom';

const useUploadFile = () => {
  const { getToken } = useAuth();
  const navigate = useNavigate();

  const uploadFile = async (file) => {
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

      return response;
    } catch (err) {
      navigate('/login');
      navigate('/');
      return null;
    }
  };

  return uploadFile;
};

export default useUploadFile;
