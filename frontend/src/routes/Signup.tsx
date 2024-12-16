// /frontend/src/routes/Signup.tsx
import React, { useState } from 'react';
import styles from '../styles/Signup.module.css';
import apiClient from '../apiClient';
import { useNavigate } from 'react-router-dom';
import LoadingIndicator from '../components/LoadingIndicator';

const Signup: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      setError('Passwords do not match.');
      return;
    }
    setIsLoading(true);
    setError('');
    try {
      await apiClient.post('/auth/signup', { email, password });
      navigate('/login');
    } catch (err: any) {
      setError(err.response?.data?.error || 'Signup failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.signupContainer}>
      <h1>Signup</h1>
      <form onSubmit={handleSignup} aria-describedby="error-message" className={styles.signupForm}>
        <label htmlFor="email">Email:</label>
        <input
          id="email"
          type="email"
          placeholder="you@example.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          aria-required="true"
        />

        <label htmlFor="password">Password:</label>
        <input
          id="password"
          type="password"
          placeholder="********"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          aria-required="true"
        />

        <label htmlFor="confirm-password">Confirm Password:</label>
        <input
          id="confirm-password"
          type="password"
          placeholder="********"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          required
          aria-required="true"
        />

        {error && (
          <p className={styles.error} id="error-message" role="alert">
            {error}
          </p>
        )}

        <button type="submit" disabled={isLoading}>
          {isLoading ? <LoadingIndicator /> : 'Signup'}
        </button>
      </form>
    </div>
  );
};

export default Signup;
