// /frontend/src/routes/Dashboard.tsx
import React, { useEffect, useState, useContext } from 'react';
import apiClient from '../apiClient';
import { AuthContext } from '../AuthContext';
import { useNavigate } from 'react-router-dom';

interface Project {
  id: number;
  name: string;
  data: any;
  created_at: string;
}

const Dashboard: React.FC = () => {
  const { token } = useContext(AuthContext);
  const [projects, setProjects] = useState<Project[]>([]);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProjects = async () => {
      try {
        const response = await apiClient.get('/projects/', {
          headers: { Authorization: token },
        });
        setProjects(response.data);
      } catch (err) {
        setError('Failed to load projects.');
      }
    };
    fetchProjects();
  }, [token]);

  const handlePublish = async (projectId: number) => {
    try {
      const response = await apiClient.post(`/publish/publish/${projectId}`, null, {
        headers: { Authorization: token },
      });
      const downloadUrl = response.data.download_url;
      // Optionally, save the download URL to the project or state
      alert(`Extension published successfully! Download URL: ${downloadUrl}`);
    } catch (err) {
      alert('Failed to publish extension.');
    }
  };

  const handleDownload = async (projectId: number) => {
    try {
      const response = await apiClient.get(`/publish/download/${projectId}`, {
        headers: { Authorization: token },
        responseType: 'blob',
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `extension_${projectId}.zip`);
      document.body.appendChild(link);
      link.click();
      link.parentNode?.removeChild(link);
    } catch (err) {
      alert('Failed to download extension.');
    }
  };

  return (
    <div className="container">
      <h1>Dashboard</h1>
      {error && <p className="error">{error}</p>}
      <ul>
        {projects.map((project) => (
          <li key={project.id}>
            <h2>{project.name}</h2>
            <button onClick={() => navigate(`/projects/${project.id}`)}>Edit</button>
            <button onClick={() => handlePublish(project.id)}>Publish</button>
            <button onClick={() => handleDownload(project.id)}>Download</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Dashboard;
