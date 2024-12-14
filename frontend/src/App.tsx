// /frontend/src/App.tsx
import React, { Suspense } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './AuthContext';
import ErrorBoundary from './components/ErrorBoundary';
import TooltipGuide from './components/TooltipGuide';
import LoadingIndicator from './components/LoadingIndicator';

// Lazy loaded routes
const Home = React.lazy(() => import('./routes/Home'));
const Login = React.lazy(() => import('./routes/Login'));
const Signup = React.lazy(() => import('./routes/Signup'));
const Dashboard = React.lazy(() => import('./routes/Dashboard'));
const TemplateLibrary = React.lazy(() => import('./routes/TemplateLibrary'));
const ProjectEditor = React.lazy(() => import('./routes/ProjectEditor'));
const Marketplace = React.lazy(() => import('./routes/Marketplace'));

function App() {
  return (
    <AuthProvider>
      <Router>
        <ErrorBoundary>
          <TooltipGuide />
          <Suspense fallback={<LoadingIndicator />}>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/login" element={<Login />} />
              <Route path="/signup" element={<Signup />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/templates" element={<TemplateLibrary />} />
              <Route path="/projects/:id" element={<ProjectEditor />} />
              <Route path="/marketplace" element={<Marketplace />} />
            </Routes>
          </Suspense>
        </ErrorBoundary>
      </Router>
    </AuthProvider>
  );
}

export default App;
