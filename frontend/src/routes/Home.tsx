import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from '../styles/Home.module.css';

const Home: React.FC = () => {
  const navigate = useNavigate();
  const [fadeIn, setFadeIn] = useState(false);

  useEffect(() => {
    // Trigger fade-in animation on mount
    const timeout = setTimeout(() => {
      setFadeIn(true);
    }, 50);
    return () => clearTimeout(timeout);
  }, []);

  return (
    <div className={`${styles.homeContainer} ${fadeIn ? styles.fadeIn : ''}`}>
      <header className={styles.header}>
        <h1 className={styles.headline}>Your Chrome Extension Hub</h1>
        <p className={styles.subtext}>
          Supercharge your browser experience by crafting, customizing, and launching your own Chrome extensions.
        </p>
        <button
          className={styles.getStartedButton}
          onClick={() => navigate('/dashboard')}
          aria-label="Get Started"
        >
          Get Started
        </button>
      </header>
      <section className={styles.featureSection}>
        <h2 className={styles.sectionTitle}>Why Chrome Extension Factory?</h2>
        <ul className={styles.featureList}>
          <li className={styles.featureItem}>
            <strong>Seamless Editing:</strong> Build and edit with an intuitive code editor.
          </li>
          <li className={styles.featureItem}>
            <strong>Instant Previews:</strong> See changes as you type.
          </li>
          <li className={styles.featureItem}>
            <strong>Easy Publishing:</strong> Launch to the Chrome Web Store with a few clicks.
          </li>
        </ul>
      </section>
      <footer className={styles.footer}>
        <p className={styles.footerText}>Ready to create something amazing?</p>
      </footer>
    </div>
  );
};

export default Home;
