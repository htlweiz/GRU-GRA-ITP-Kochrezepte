import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import mkcert from 'vite-plugin-mkcert'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue(), mkcert()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    strictPort: true,
   
  },
  optimizeDeps: {
    include: ['@azure/msal-browser'],
  },
  
});

