// /frontend/src/components/LoadingIndicator.tsx
import React from 'react';
import styles from '../styles/LoadingIndicator.module.css';

const LoadingIndicator: React.FC = () => {
  return (
    <div className={styles.loadingContainer} role="status" aria-live="polite">
      <div className={styles.spinner}></div>
      <span>Loading...</span>
    </div>
  );
};

export default LoadingIndicator;
