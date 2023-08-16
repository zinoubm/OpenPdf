import axios from '../axios';
import useAuth from './useAuth';
import { useNavigate } from 'react-router-dom';

const useGoogleLogin = () => {
  const { setToken } = useAuth();
  const navigate = useNavigate();

  const googleLogin = async (token) => {
    try {
      const response = await axios.post('/login/google', token, {
        headers: {
          accept: 'application/json',
          'Content-Type': 'application/json'
        }
      });

      setToken(response.data.access_token);
      navigate('/');
      return true;
    } catch (err) {
      return false;
    }
  };

  return googleLogin;
};

export default useGoogleLogin;
