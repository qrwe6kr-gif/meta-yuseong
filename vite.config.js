import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// base: './' lets the built site run from any folder (GitHub Pages, Netlify, a USB stick).
export default defineConfig({
  plugins: [react()],
  base: './',
  build: { chunkSizeWarningLimit: 2000 },   // Phaser alone is ~1.5MB
});
