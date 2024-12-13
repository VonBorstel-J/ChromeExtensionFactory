import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './routes/Home';
import Login from './routes/Login';
import Signup from './routes/Signup';
import Dashboard from './routes/Dashboard';
import TemplateLibrary from './routes/TemplateLibrary';
import ProjectEditor from './routes/ProjectEditor';
import Marketplace from './routes/Marketplace';
import { AuthProvider } from './AuthContext';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/templates" element={<TemplateLibrary />} />
          <Route path="/projects/:id" element={<ProjectEditor />} />
          <Route path="/marketplace" element={<Marketplace />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
