import {defineConfig} from 'vite';
export default defineConfig({server:{host:'0.0.0.0',allowedHosts:['terminal.local']},build:{rollupOptions:{output:{manualChunks:{genlayer:['genlayer-js','genlayer-js/chains']}}}}});
