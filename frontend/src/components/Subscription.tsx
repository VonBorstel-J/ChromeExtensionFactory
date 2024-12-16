// /frontend/src/components/Subscription.tsx
import React from 'react';
import apiClient from '../apiClient';
import styles from '../styles/Subscription.module.css';

interface SubscriptionProps {
  currentTier: 'free' | 'pro' | 'enterprise';
}

const Subscription: React.FC<SubscriptionProps> = ({ currentTier }) => {
  const handleSubscribe = async (tier: 'free'|'pro'|'enterprise') => {
    // Example pricing: free = $0, pro = $15, enterprise = $50
    let amount = 0;
    if (tier === 'pro') amount = 1500; // in cents
    if (tier === 'enterprise') amount = 5000;

    try {
      const response = await apiClient.post('/payments/checkout-session', {
        tier,
        amount,
        currency: 'usd'
      });
      const { sessionId } = response.data;
      // Redirect user to Stripe Checkout page or handle however needed
      alert(`Checkout session created with ID: ${sessionId}. Redirect to payment page here.`);
    } catch (err) {
      console.error('Subscription error:', err);
      alert('Failed to create checkout session.');
    }
  };

  return (
    <div className={styles.subscriptionOptions}>
      <div className={styles.subscriptionTier}>
        <h3>Free</h3>
        <p>Limited projects, no publishing.</p>
        {currentTier === 'free' ? (
          <button disabled>Current Plan</button>
        ) : (
          <button onClick={() => handleSubscribe('free')}>Subscribe</button>
        )}
      </div>
      <div className={styles.subscriptionTier}>
        <h3>Pro</h3>
        <p>Unlimited projects, publishing.</p>
        <p>$15/month</p>
        {currentTier === 'pro' ? (
          <button disabled>Current Plan</button>
        ) : (
          <button onClick={() => handleSubscribe('pro')}>Subscribe</button>
        )}
      </div>
      <div className={styles.subscriptionTier}>
        <h3>Enterprise</h3>
        <p>Includes analytics and more advanced features.</p>
        <p>$50/month</p>
        {currentTier === 'enterprise' ? (
          <button disabled>Current Plan</button>
        ) : (
          <button onClick={() => handleSubscribe('enterprise')}>Subscribe</button>
        )}
      </div>
    </div>
  );
};

export default Subscription;
