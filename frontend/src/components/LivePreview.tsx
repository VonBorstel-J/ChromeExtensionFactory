// /frontend/src/components/LivePreview.tsx
import React, { useEffect } from 'react';

type Props = {
  code: string;
};

const LivePreview: React.FC<Props> = ({ code }) => {
  useEffect(() => {
    const iframe = document.getElementById('live-preview') as HTMLIFrameElement;
    iframe.srcdoc = code;
  }, [code]);

  return <iframe id="live-preview" title="Live Preview" style={{ width: '100%', height: '400px', border: '1px solid #ccc' }} />;
};

export default LivePreview;
