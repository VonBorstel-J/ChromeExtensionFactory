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
  withCredentials: true,
  timeout: 30000, // 30 seconds timeout
});

// Retry configuration for transient errors
axiosRetry(apiClient, {
  retries: 3,
  retryDelay: (retryCount) => axiosRetry.exponentialDelay(retryCount),
  retryCondition: (error: AxiosError) => {
    // Retry on network errors or 5xx status codes
    return axiosRetry.isNetworkError(error) || 
           (error.response?.status && error.response.status >= 500) ||
           error.code === 'ECONNABORTED';
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
    
    // Add CSRF token if available
    const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
    if (csrfToken && config.headers) {
      config.headers['X-CSRF-Token'] = csrfToken;
    }
    
    return config;
  },
  (error: AxiosError) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    // Handle specific error cases
    if (error.response?.status === 401) {
      // Clear token and redirect to login
      localStorage.removeItem('jwt');
      window.location.href = '/login';
      return Promise.reject(new Error('Authentication required'));
    }

    if (error.response?.status === 403) {
      return Promise.reject(new Error('Access denied'));
    }

    if (error.response?.status === 429) {
      return Promise.reject(new Error('Too many requests. Please try again later.'));
    }

    const errorMessage =
      error.response?.data && typeof error.response?.data === 'object'
        ? (error.response?.data as { error?: string; message?: string }).error ?? 
          (error.response?.data as { error?: string; message?: string }).message ?? 
          error.message
        : error.message;

    console.error('API Error:', {
      message: errorMessage,
      status: error.response?.status,
      url: error.config?.url,
      method: error.config?.method
    });

    return Promise.reject(new Error(errorMessage));
  }
);

export default apiClient;
