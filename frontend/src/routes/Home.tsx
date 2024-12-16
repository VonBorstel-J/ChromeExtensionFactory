// /frontend/src/routes/Home.tsx
import React from 'react';
import styles from '../styles/Home.module.css';

const Home: React.FC = () => {
  return (
    <div className={styles.homeContainer}>
      <h1>Welcome to the Chrome Extension Factory</h1>
      <p>Create, manage, and publish your custom Chrome extensions with ease.</p>
    </div>
  );
};

export default Home;
