import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    // WHY a proxy?
    // In development, your React app runs on port 5173 and your FastAPI on 8003.
    // To avoid CORS (security) issues, we can tell Vite to forward /api calls to the backend.
    // However, for simplicity for a beginner, we used the full URL in urlService.ts.
  }
})
