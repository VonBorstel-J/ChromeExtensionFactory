// /frontend/src/routes/TemplateLibrary.tsx
import React, { useState, useEffect, useContext } from 'react';
import apiClient from '../apiClient';
import { AuthContext } from '../AuthContext';

interface Template {
  name: string;
}

const TemplateLibrary: React.FC = () => {
  const { token } = useContext(AuthContext);
  const [availableTemplates, setAvailableTemplates] = useState<Template[]>([]);
  const [myTemplates, setMyTemplates] = useState<Template[]>([]);
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    const fetchTemplates = async () => {
      try {
        const response = await apiClient.get('/templates/', {
          headers: { Authorization: token }
        });
        const templates = response.data.map((t: string) => ({name: t}));
        setAvailableTemplates(templates);

        // Fetch user’s uploaded templates (for demonstration assume /templates/my)
        const myRes = await apiClient.get('/templates/my', {
          headers: { Authorization: token }
        });
        const myTmpls = myRes.data.map((t: string) => ({name: t}));
        setMyTemplates(myTmpls);

      } catch (error) {
        console.error('Failed to fetch templates:', error);
      }
    };
    fetchTemplates();
  }, [token]);

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) return;
    setUploading(true);
    const formData = new FormData();
    Array.from(e.target.files).forEach(file => formData.append('file', file));
    try {
      await apiClient.post('/templates/upload', formData, {
        headers: {
          Authorization: token,
          'Content-Type': 'multipart/form-data'
        }
      });
      // After upload, re-fetch my templates
      const myRes = await apiClient.get('/templates/my', {
        headers: { Authorization: token }
      });
      const myTmpls = myRes.data.map((t: string) => ({name: t}));
      setMyTemplates(myTmpls);
    } catch (err) {
      console.error('Upload failed:', err);
    } finally {
      setUploading(false);
      e.target.value = ''; // reset file input
    }
  };

  return (
    <div className="container">
      <h1>Template Library</h1>
      <p>Browse and select templates to kickstart your extension project.</p>

      <h2>Available Templates</h2>
      <ul>
        {availableTemplates.map((t) => (
          <li key={t.name}>{t.name}</li>
        ))}
      </ul>

      <h2>My Templates</h2>
      <p>These are templates you've uploaded:</p>
      <ul>
        {myTemplates.map((t) => (
          <li key={t.name}>{t.name}</li>
        ))}
      </ul>

      <div style={{marginTop: '1rem'}}>
        <label htmlFor="upload-input">Upload Your Templates:</label><br/>
        <input 
          id="upload-input"
          type="file" 
          multiple 
          onChange={handleUpload} 
          disabled={uploading} 
        />
        {uploading && <p>Uploading...</p>}
      </div>
    </div>
  );
};

export default TemplateLibrary;
