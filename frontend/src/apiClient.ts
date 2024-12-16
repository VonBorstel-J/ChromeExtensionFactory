import axios, { AxiosInstance, AxiosError, InternalAxiosRequestConfig } from 'axios';

// Base Axios instance configuration
const apiClient: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('jwt');
    if (token && config.headers) {
      config.headers.set('Authorization', token);
    }
    return config;
  },
  (error: AxiosError) => Promise.reject(error)
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    const errorMessage =
      error.response?.data && typeof error.response?.data === 'object'
        ? (error.response?.data as { error?: string }).error ?? error.message
        : error.message;

    return Promise.reject(new Error(errorMessage));
  }
);

export default apiClient;
