import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

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
      '/api': {
        target: 'http://localhost:8080', // Адрес вашего API-сервера
        changeOrigin: true, // Перезаписывает заголовок Origin
        secure: false, // Если сервер работает через HTTPS с самоподписанным сертификатом
      },
    },
    allowedHosts: [
        "intractably-wealthy-squeaker.cloudpub.ru",
      ]
  },
})
