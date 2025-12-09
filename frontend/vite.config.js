import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  base: "/manager/",
  plugins: [react()],
  server: {
    host: true,
    port: 5173,
    proxy: {
      '/manager/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/manager\/api/, '/api'),
      },
    },
  },
})
