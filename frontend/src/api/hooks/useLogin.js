import axios from '../axios';
import useAuth from './useAuth';
import { useNavigate } from 'react-router-dom';

const useLogin = () => {
  const { setToken } = useAuth();
  const navigate = useNavigate();

  const login = async (email, password) => {
    try {
      const response = await axios.post(
        '/login/access-token',
        new URLSearchParams({
          grant_type: '',
          username: email,
          password: password,
          scope: '',
          client_id: '',
          client_secret: ''
        }),
        {
          headers: {
            accept: 'application/json'
          }
        }
      );

      setToken(response.data.access_token);
      navigate('/');
      return true;
    } catch (err) {
      if (err.response && err.response.status === 401) {
        navigate('/verify');
        console.log('User non verified');
      }
      return false;
    }
  };

  return login;
};

export default useLogin;
