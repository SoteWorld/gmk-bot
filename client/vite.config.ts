import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    proxy: {
      // '/api': 'http://localhost:8000',
      '/api': {
        target: 'http://localhost:8080', // Адрес вашего API-сервера
        changeOrigin: true, // Перезаписывает заголовок Origin
        secure: false, // Если сервер работает через HTTPS с самоподписанным сертификатом
        //rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
    allowedHosts: [
        "6676b6d12c1c1de3513ccda9e337cbdb.serveo.net",
      ]
  },
})
