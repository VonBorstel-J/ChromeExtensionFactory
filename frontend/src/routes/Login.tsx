// /frontend/src/routes/Login.tsx
import React, { useState, useContext } from 'react';
import { AuthContext } from '../AuthContext';
import apiClient from '../apiClient';
import { useNavigate } from 'react-router-dom';
import LoadingIndicator from '../components/LoadingIndicator';
import styles from '../styles/Login.module.css';

const Login: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { setToken } = useContext(AuthContext);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    try {
      const response = await apiClient.post('/auth/login', { email, password });
      setToken(response.data.token);
      navigate('/dashboard');
    } catch (err: any) {
      if (err.response && err.response.status === 401) {
        setError('Invalid email or password. Please check your credentials.');
      } else {
        setError('An unexpected error occurred. Please try again later.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.loginContainer}>
      <h1>Login</h1>
      <form onSubmit={handleLogin} aria-describedby="error-message" className={styles.loginForm}>
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
        {error && (
          <p className={styles.error} id="error-message" role="alert">
            {error}
          </p>
        )}
        <button type="submit" disabled={isLoading}>
          {isLoading ? <LoadingIndicator /> : 'Login'}
        </button>
      </form>
    </div>
  );
};

export default Login;
