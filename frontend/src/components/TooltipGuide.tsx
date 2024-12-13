// /frontend/src/components/TooltipGuide.tsx 
import React from 'react';
import Joyride, { CallBackProps, STATUS } from 'react-joyride';

const steps = [
  {
    target: '.container',
    content: 'Welcome to the Chrome Extension Factory! Let us guide you through the features.',
  },
  {
    target: '#login-button',
    content: 'Click here to log into your account.',
  },
  {
    target: '#signup-button',
    content: 'New user? Sign up here to create an account.',
  },
  // Add more steps as needed
];

const TooltipGuide: React.FC = () => {
  const handleJoyrideCallback = (data: CallBackProps) => {
    const { status } = data;
    if ([STATUS.FINISHED, STATUS.SKIPPED].includes(status)) {
      // Handle completion or skipping of the tour
      console.log('Tour finished or skipped');
    }
  };

  return (
    <Joyride
      steps={steps}
      continuous
      showSkipButton
      callback={handleJoyrideCallback}
      styles={{
        options: {
          zIndex: 10000,
        },
      }}
    />
  );
};

export default TooltipGuide;
