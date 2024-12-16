// /frontend/src/routes/NotFound.tsx
import React from 'react';
import { useNavigate } from 'react-router-dom';
import styles from '../styles/NotFound.module.css';

const NotFound: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className={styles.notFoundContainer}>
      <h1>404 - Page Not Found</h1>
      <p>Oops! The page you're looking for doesn't exist.</p>
      <div className={styles.buttonGroup}>
        <button onClick={() => navigate('/')}>Go to Homepage</button>
        <button onClick={() => navigate('/dashboard')}>Go to Dashboard</button>
      </div>
    </div>
  );
};

export default NotFound;
