// /frontend/src/utils/paymentHelpers.ts
import apiClient from '../apiClient';

interface PaymentData {
  amount: number;
  currency: string;
  paymentMethodId: string;
}

interface CheckoutSession {
  sessionId: string;
}

export const processPayment = async (paymentData: PaymentData): Promise<CheckoutSession> => {
  try {
    const response = await apiClient.post('/payments/checkout-session', paymentData);
    return response.data;
  } catch (error: any) {
    console.error('Payment processing failed:', error.response?.data || error.message);
    throw new Error(error.response?.data?.error || 'Payment processing failed');
  }
};
