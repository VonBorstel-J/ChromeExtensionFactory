import React, { useEffect, useState } from 'react';
import Joyride, { CallBackProps, STATUS } from 'react-joyride';

const TooltipGuide: React.FC = () => {
    const [targetsMounted, setTargetsMounted] = useState(false);

    const steps = [
        { target: '.container', content: 'Welcome to the Chrome Extension Factory!' },
        { target: '#login-button', content: 'Click here to log into your account.' },
        { target: '#signup-button', content: 'New user? Sign up here to create an account.' }
    ];

    useEffect(() => {
        const checkTargets = () => steps.every(step => document.querySelector(step.target));
        const interval = setInterval(() => {
            if (checkTargets()) {
                setTargetsMounted(true);
                clearInterval(interval);
            } else {
                console.warn('One or more Joyride targets not mounted.');
            }
        }, 100);

        return () => clearInterval(interval);
    }, [steps]);

    if (!targetsMounted) return null;

    const handleJoyrideCallback = (data: CallBackProps) => {
        const { status } = data;
        if (status === STATUS.FINISHED || status === STATUS.SKIPPED) {
            console.log('Tour finished or skipped');
        }
    };

    return (
        <Joyride
            steps={steps}
            callback={handleJoyrideCallback}
            showSkipButton
            continuous
            styles={{
                options: {
                    zIndex: 10000,
                },
            }}
        />
    );
};

export default TooltipGuide;
