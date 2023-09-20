import axios from 'axios';

const BASE_URL = process.env.REACT_APP_BACKEND_URL + '/api/v1';
console.log('base url');
console.log(BASE_URL);
// const BASE_URL = 'http://localhost:8000/api/v1';

export default axios.create({
  baseURL: BASE_URL
});

export const axiosPrivate = axios.create({
  baseURL: BASE_URL,
  headers: { 'Content-Type': 'application/json' },
  withCredentials: true
});
