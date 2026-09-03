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
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000/',rewrite:(p)=>p.replace(/^\/api/, ''), // Vite dev server 内置 http-proxy 能力。在 vite.config.ts 的 server.proxy 里声明规则后，dev server 把匹配前缀的请求转发到 target 指定的地址，再把响应原路带回。浏览器只和 5174 通信。
        // 即我需在5174号 找一个跑腿的到8000号拿东西转交给我，我只和5174号通信，门卫看到的是"5174 出、5174 进"，全程同源，无话可说。
        changeOrigin: true, // 跑腿的去 8000 敲门时，自报家门说"我是 5174 来的"。有的门卫（后端）会看这个来头，觉得不对就把人轰走。changeOrigin: true 就是让跑腿的改口说"我是 8000 自己人"。
      }
    }
  }
})
