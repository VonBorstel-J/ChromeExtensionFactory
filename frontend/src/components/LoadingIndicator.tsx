// /frontend/src/components/LoadingIndicator.tsx
import React from 'react';
import './LoadingIndicator.css';

const LoadingIndicator: React.FC = () => {
  return (
    <div className="loading-container" role="status" aria-live="polite">
      <div className="spinner"></div>
      <span>Loading...</span>
    </div>
  );
};

export default LoadingIndicator;
