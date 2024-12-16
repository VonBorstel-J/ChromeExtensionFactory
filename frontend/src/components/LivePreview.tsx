// /frontend/src/components/LivePreview.tsx
import React, { useEffect, useRef } from 'react';
import styles from '../styles/LivePreview.module.css';

type Props = {
  code: string;
};

const LivePreview: React.FC<Props> = ({ code }) => {
  const iframeRef = useRef<HTMLIFrameElement>(null);

  useEffect(() => {
    const iframe = iframeRef.current;
    if (iframe) {
      iframe.srcdoc = code;
      // Adjust height after loading the content
      const adjustHeight = () => {
        try {
          if (iframe.contentDocument?.body) {
            const height = iframe.contentDocument.body.scrollHeight;
            iframe.style.height = `${height + 20}px`; // Add some padding
          }
        } catch (e) {
          console.error("Error adjusting iframe height:", e);
        }
      };

      // Wait a bit for content to render, then adjust
      setTimeout(adjustHeight, 200);
    }
  }, [code]);

  return (
    <iframe
      ref={iframeRef}
      title="Live Preview"
      className={styles.livePreview}
    />
  );
};

export default LivePreview;
