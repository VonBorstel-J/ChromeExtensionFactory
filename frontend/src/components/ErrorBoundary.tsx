// /frontend/src/components/ErrorBoundary.tsx
import React, { Component, ErrorInfo, ReactNode } from 'react';
import styles from '../styles/ErrorBoundary.module.css';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export default class ErrorBoundary extends Component<Props, State> {
  state: State = {
    hasError: false,
    error: undefined
  };

  static getDerivedStateFromError(error: Error): State {
    console.error("Caught error in ErrorBoundary:", error);
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error("ErrorBoundary caught error:", error, info);
    // Optionally, send error details to a monitoring service
  }

  handleRetry = () => {
    this.setState({ hasError: false, error: undefined });
    window.location.reload();
  };

  handleGoBack = () => {
    window.history.back();
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className={styles.errorContainer}>
          <h1>Oops! Something went wrong.</h1>
          <p>We're sorry for the inconvenience. Please try one of the options below:</p>
          <div className={styles.buttonGroup}>
            <button onClick={this.handleRetry}>Refresh Page</button>
            <button onClick={this.handleGoBack}>Go Back</button>
            <button onClick={() => window.location.href = '/'}>Go to Homepage</button>
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}
