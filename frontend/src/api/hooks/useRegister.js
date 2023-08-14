import axios from '../axios';

const useRegister = () => {
  const register = async (email, password, full_name) => {
    try {
      await axios.post(
        'users/open',
        {
          password: password,
          email: email,
          full_name: full_name
        },
        {
          headers: {
            accept: 'application/json',
            'Content-Type': 'application/json'
          }
        }
      );
      return true;
    } catch (err) {
      return false;
    }
  };

  return register;
};

export default useRegister;
