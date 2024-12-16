// /frontend/src/utils/authHelpers.ts
import apiClient from '../apiClient';
import { validateEnvVariables } from './envValidation';

validateEnvVariables();

export const authenticateUser = async (token: string): Promise<boolean> => {
  try {
    const response = await apiClient.get('/auth/verify-token', {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data.valid;
  } catch (error) {
    console.error('Authentication failed:', error);
    return false;
  }
};
