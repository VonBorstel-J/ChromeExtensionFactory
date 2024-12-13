import axios from 'axios';

const apiClient = axios.create({
  baseURL: '/api', // Assuming backend is proxied
});

// Append JWT token, etc.
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('jwt');
  if (token && config.headers) {
    config.headers['Authorization'] = token;
  }
  return config;
});

export default apiClient;
