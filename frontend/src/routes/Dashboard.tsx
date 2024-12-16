// /frontend/src/routes/Dashboard.tsx
import React, { useEffect, useState, useContext } from 'react';
import apiClient from '../apiClient';
import { AuthContext } from '../AuthContext';
import { useNavigate } from 'react-router-dom';
import Subscription from '../components/Subscription'; 
import styles from '../styles/Dashboard.module.css'; 

interface Project {
  id: number;
  name: string;
  data: any;
  created_at: string;
}

interface PopularTemplate {
  template: string;
  count: number;
}

const Dashboard: React.FC = () => {
  const { token } = useContext(AuthContext);
  const [projects, setProjects] = useState<Project[]>([]);
  const [popularTemplates, setPopularTemplates] = useState<PopularTemplate[]>([]);
  const [error, setError] = useState('');
  const [userTier, setUserTier] = useState<'free'|'pro'|'enterprise'>('free'); // Assume we can fetch the user's tier
  const [earnings, setEarnings] = useState<number>(0); // Dummy data
  const [animating, setAnimating] = useState<boolean>(false);

  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [projRes, tempRes] = await Promise.all([
          apiClient.get('/projects/', { headers: { Authorization: `Bearer ${token}` } }),
          apiClient.get('/analytics/popular-templates', { headers: { Authorization: `Bearer ${token}` } })
        ]);
        setProjects(projRes.data);
        setPopularTemplates(tempRes.data);
        // Dummy logic for user tier and earnings:
        // In a real scenario, you'd fetch this from a user endpoint.
        setUserTier('pro'); // Example: set to 'pro' to display earnings
        setEarnings(123.45); // Dummy earnings data
        setAnimating(true);
      } catch (err) {
        setError('Failed to load dashboard data.');
      }
    };
    fetchData();
  }, [token]);

  const handlePublish = async (projectId: number) => {
    try {
      const response = await apiClient.post(`/publish/publish/${projectId}`, null, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const downloadUrl = response.data.download_url;
      alert(`Extension published successfully! Download URL: ${downloadUrl}`);
    } catch (err) {
      alert('Failed to publish extension.');
    }
  };

  const handleDownload = async (projectId: number) => {
    try {
      const response = await apiClient.get(`/publish/download/${projectId}`, {
        headers: { Authorization: `Bearer ${token}` },
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
    <div className={styles.dashboardContainer}>
      <h1>Dashboard</h1>
      {error && <p className={styles.error}>{error}</p>}

      {/* Analytics Dashboard Cards */}
      <div className={`${styles.dashboardCards} ${animating ? styles.fadeIn : ''}`}>
        <div className={styles.card}>
          <h2>Total Projects</h2>
          <p>{projects.length}</p>
        </div>
        <div className={styles.card}>
          <h2>Popular Templates</h2>
          <ul className={styles.popularTemplates}>
            {popularTemplates.map((pt) => (
              <li key={pt.template}>{pt.template} ({pt.count})</li>
            ))}
          </ul>
        </div>
        {userTier !== 'free' && (
          <div className={styles.card}>
            <h2>Earnings Summary</h2>
            <p>${earnings.toFixed(2)}</p>
          </div>
        )}
      </div>

      {/* Subscription Component */}
      <div className={styles.subscriptionSection}>
        <h2>Upgrade Your Plan</h2>
        <Subscription currentTier={userTier} />
      </div>

      {/* Projects List */}
      <h2>Your Projects</h2>
      <ul className={styles.projectsList}>
        {projects.map((project) => (
          <li key={project.id} className={styles.projectItem}>
            <h3>{project.name}</h3>
            <div className={styles.projectButtons}>
              <button onClick={() => navigate(`/projects/${project.id}`)}>Edit</button>
              {userTier !== 'free' && (
                <>
                  <button onClick={() => handlePublish(project.id)}>Publish</button>
                  <button onClick={() => handleDownload(project.id)}>Download</button>
                </>
              )}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Dashboard;
