// /frontend/src/utils/envValidation.ts

export const validateEnvVariables = () => {
    const requiredVars = ['VITE_API_BASE_URL'];
    const missingVars = requiredVars.filter(varName => !import.meta.env[varName]);
  
    if (missingVars.length > 0) {
      missingVars.forEach(varName => {
        console.error(`Missing required environment variable: ${varName}`);
      });
      throw new Error('One or more required environment variables are missing.');
    }
  };
  