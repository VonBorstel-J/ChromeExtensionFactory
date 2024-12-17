import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    fs: {
      allow: ['src'], // Allow serving files from the src directory
    },
  },
  resolve: {
    alias: {
      '@': '/src', // Alias for cleaner imports
    },
  },
  css: {
    modules: {
      generateScopedName: '[name]__[local]___[hash:base64:5]',
    },
  },
  build: {
    outDir: 'dist', // Specify the build output directory
    sourcemap: true, 
    cssCodeSplit: true,
  },
});
