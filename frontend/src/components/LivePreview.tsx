// /frontend/src/components/LivePreview.tsx
import React, { useEffect, useRef } from 'react';

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
          if (iframe.contentDocument && iframe.contentDocument.body) {
            const height = iframe.contentDocument.body.scrollHeight;
            iframe.style.height = `${height + 20}px`; // Add some padding
          }
        } catch (e) {
          console.error("Error adjusting iframe height:", e);
        }
      };

      // Wait a bit for content to render, then adjust
      setTimeout(adjustHeight, 200);

      // Listen for changes: you can also use a MutationObserver inside the iframe if needed.
      // For simplicity, just call again after a timeout if code changes frequently.
    }
  }, [code]);

  return (
    <iframe
      ref={iframeRef}
      title="Live Preview"
      style={{ width: '100%', border: '1px solid #ccc', transition: 'height 0.2s ease' }}
    />
  );
};

export default LivePreview;
