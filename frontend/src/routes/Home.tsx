import React from 'react';
import { useNavigate } from 'react-router-dom';
import styles from '../styles/Home.module.css';

const Home: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className={styles.homeContainer}>
      <header className={styles.header}>
        <p>Welcome to the Chrome Extension Factory! Explore the features to get started.</p>
      </header>
      <main className={styles.mainContent}>
        <h1 className={styles.title}>Welcome to the Chrome Extension Factory</h1>
        <p className={styles.description}>
          Create, manage, and publish your custom Chrome extensions with ease.
        </p>
        <button
          className={styles.getStartedButton}
          onClick={() => navigate('/dashboard')}
          aria-label="Get Started"
        >
          Get Started
        </button>
      </main>
    </div>
  );
};

export default Home;
