import axios from 'axios';

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL as string;

const api = axios.create({
  baseURL: apiBaseUrl,
});

export default api;
