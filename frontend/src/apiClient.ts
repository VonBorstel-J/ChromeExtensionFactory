// /frontend/src/apiClient.ts
import axios, { AxiosInstance, AxiosError, InternalAxiosRequestConfig } from 'axios';
import axiosRetry from 'axios-retry';
import { validateEnvVariables } from './utils/envValidation';

// Validate environment variables at runtime
validateEnvVariables();

// Base Axios instance configuration
const apiClient: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Include credentials for cross-origin requests if needed
});

// Retry configuration for transient errors
axiosRetry(apiClient, {
  retries: 3,
  retryDelay: (retryCount) => axiosRetry.exponentialDelay(retryCount),
  retryCondition: (error: AxiosError) => {
    // Retry on network errors or 5xx status codes
    return axiosRetry.isNetworkError(error) || axiosRetry.isRetryableError(error);
  },
  onRetry: (retryCount, error, requestConfig) => {
    console.warn(`Retrying request to ${requestConfig.url} (${retryCount} attempt(s))`);
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('jwt');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
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

    console.error('API Error:', errorMessage);
    return Promise.reject(new Error(errorMessage));
  }
);

export default apiClient;
