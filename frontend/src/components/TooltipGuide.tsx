import React, { useEffect, useState } from 'react';
import Joyride, { CallBackProps, STATUS, Step } from 'react-joyride';
import styles from '../styles/TooltipGuide.module.css';

const TooltipGuide: React.FC = () => {
  const [isReady, setIsReady] = useState(false);
  const [showFallback, setShowFallback] = useState(false);
  const steps: Step[] = [
    { target: '.homeContainer', content: 'Welcome to the Chrome Extension Factory!' },
    { target: '#login-button', content: 'Click here to log into your account.' },
    { target: '#signup-button', content: 'New user? Sign up here to create an account.' },
  ];

  useEffect(() => {
    const checkTargets = () => steps.every(step => typeof step.target === 'string' && document.querySelector(step.target));
    const maxAttempts = 50; // e.g., wait up to 5 seconds
    let attempts = 0;

    const interval = setInterval(() => {
      attempts += 1;
      if (checkTargets()) {
        setIsReady(true);
        clearInterval(interval);
        console.log('All Joyride targets are mounted.');
      } else if (attempts >= maxAttempts) {
        clearInterval(interval);
        console.error('One or more Joyride targets failed to mount.');
        setShowFallback(true); // Show fallback UI
      } else {
        console.warn('Waiting for Joyride targets to mount...');
      }
    }, 100); // check every 100ms

    return () => clearInterval(interval);
  }, [steps]);

  const handleJoyrideCallback = (data: CallBackProps) => {
    const { status } = data;
    if (status === STATUS.FINISHED || status === STATUS.SKIPPED) {
      console.log('Tour finished or skipped');
    }
  };

  if (showFallback) {
    return (
      <div className={styles.fallbackContainer}>
        <p>Welcome to the Chrome Extension Factory! Explore the features to get started.</p>
      </div>
    );
  }

  if (!isReady) {
    // Optionally, display a loading indicator or nothing
    return null;
  }

  return (
    <Joyride
      steps={steps}
      callback={handleJoyrideCallback}
      showSkipButton
      continuous
      run={isReady}
      styles={{
        options: {
          zIndex: 10000,
        },
      }}
    />
  );
};

export default TooltipGuide;
