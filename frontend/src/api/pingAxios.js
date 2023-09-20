import axios from './axios';

async function ping() {
  const res = await axios.get('users/sanity');
}

export default ping;
