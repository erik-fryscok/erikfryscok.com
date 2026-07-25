import { defineConfig } from 'astro/config';
import tailwind from '@tailwindcss/vite';

export default defineConfig({
  // No integrations needed beyond Tailwind via Vite plugin.
  vite: {
    plugins: [tailwind()],
  },
});
