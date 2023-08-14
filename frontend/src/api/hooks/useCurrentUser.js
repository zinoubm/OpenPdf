import axios from '../axios';
// import react from 'react';
import useAuth from './useAuth';
import { useNavigate } from 'react-router-dom';

const useCurrentUser = () => {
  const { getToken } = useAuth();
  const navigate = useNavigate();

  const currentUser = async () => {
    try {
      const response = await axios.get('users/me', {
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

  return currentUser;
};

export default useCurrentUser;
