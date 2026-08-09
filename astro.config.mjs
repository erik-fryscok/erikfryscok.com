import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import tailwind from '@tailwindcss/vite';

export default defineConfig({
  site: 'https://erikfryscok.com',
  integrations: [
    sitemap({
      filter: (page) => {
        const { pathname } = new URL(page);
        return pathname !== '/404' && pathname !== '/404/';
      },
    }),
  ],
  vite: {
    plugins: [tailwind()],
  },
});
