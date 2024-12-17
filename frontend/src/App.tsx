import React, { Suspense } from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import { AuthProvider } from './AuthContext';
import ErrorBoundary from './components/ErrorBoundary';
import TooltipGuide from './components/TooltipGuide';
import LoadingIndicator from './components/LoadingIndicator';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const Home = React.lazy(() => import('./routes/Home'));
const Login = React.lazy(() => import('./routes/Login'));
const Signup = React.lazy(() => import('./routes/Signup'));
const Dashboard = React.lazy(() => import('./routes/Dashboard'));
const TemplateLibrary = React.lazy(() => import('./routes/TemplateLibrary'));
const ProjectEditor = React.lazy(() => import('./routes/ProjectEditor'));
const Marketplace = React.lazy(() => import('./routes/Marketplace'));
const NotFound = React.lazy(() => import('./routes/NotFound'));

function AppContent() {
  const location = useLocation();
  const hideNavbar = location.pathname === '/login' || location.pathname === '/signup';

  const Navbar = React.lazy(() => import('./components/Navbar'));

  return (
    <ErrorBoundary>
      <ToastContainer position="top-right" autoClose={3000} hideProgressBar={false} />
      <TooltipGuide />
      {!hideNavbar && (
        <Suspense fallback={<div />}>
          <Navbar />
        </Suspense>
      )}
      <Suspense fallback={<LoadingIndicator />}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/templates" element={<TemplateLibrary />} />
          <Route path="/projects/:id" element={<ProjectEditor />} />
          <Route path="/marketplace" element={<Marketplace />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </Suspense>
    </ErrorBoundary>
  );
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <AppContent />
      </Router>
    </AuthProvider>
  );
}

export default App;
