// /frontend/src/utils/envValidation.ts

interface EnvConfig {
  VITE_API_BASE_URL: string;
  VITE_ENABLE_ANALYTICS?: string;
  VITE_ENABLE_STRIPE?: string;
  VITE_STRIPE_PUBLIC_KEY?: string;
  VITE_GOOGLE_ANALYTICS_ID?: string;
  VITE_ENABLE_HTTPS?: string;
  VITE_ENABLE_CSP?: string;
}

export const validateEnvVariables = () => {
  const requiredVars: (keyof EnvConfig)[] = ['VITE_API_BASE_URL'];
  const missingVars = requiredVars.filter(varName => !import.meta.env[varName]);
  
  if (missingVars.length > 0) {
    missingVars.forEach(varName => {
      console.error(`Missing required environment variable: ${varName}`);
    });
    throw new Error('One or more required environment variables are missing.');
  }

  // Validate API URL format
  const apiUrl = import.meta.env.VITE_API_BASE_URL;
  try {
    new URL(apiUrl);
  } catch (e) {
    throw new Error(`Invalid API URL format: ${apiUrl}`);
  }

  // Validate Stripe configuration if enabled
  if (import.meta.env.VITE_ENABLE_STRIPE === 'true') {
    if (!import.meta.env.VITE_STRIPE_PUBLIC_KEY) {
      throw new Error('Stripe is enabled but VITE_STRIPE_PUBLIC_KEY is missing');
    }
  }

  // Validate Analytics configuration if enabled
  if (import.meta.env.VITE_ENABLE_ANALYTICS === 'true') {
    if (!import.meta.env.VITE_GOOGLE_ANALYTICS_ID) {
      throw new Error('Analytics is enabled but VITE_GOOGLE_ANALYTICS_ID is missing');
    }
  }
};
  