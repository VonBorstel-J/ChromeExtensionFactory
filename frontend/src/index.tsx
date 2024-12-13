// /frontend/src/index.tsx
import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';
import './styles/App.module.css';

const container = document.getElementById('root');
const root = createRoot(container!);
root.render(<App />);
