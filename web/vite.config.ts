import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vitest/config';
import fs from 'fs';

export default defineConfig({
  plugins: [sveltekit()],
  server: {
    host: '0.0.0.0',
    port: 8080,
    strictPort: true,
    https: {
      key: fs.readFileSync('../ssl/weblog.local-key.pem'),
      cert: fs.readFileSync('../ssl/weblog.local-cert.pem')
    }
  },
  test: {
    include: ['src/**/*.{test,spec}.{js,ts}']
  }
});
