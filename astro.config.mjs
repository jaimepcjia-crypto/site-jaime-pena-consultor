import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://www.jaimepena-mouradubeux.com',
  i18n: {
    defaultLocale: 'pt',
    locales: ['pt', 'en', 'es'],
    routing: {
      // PT stays at the root ("master URL"); en/es are served under /en, /es.
      prefixDefaultLocale: false,
    },
  },
  integrations: [
    tailwind(),
    sitemap({
      i18n: {
        defaultLocale: 'pt',
        locales: { pt: 'pt-BR', en: 'en', es: 'es' },
      },
    }),
  ],
  build: {
    inlineStylesheets: 'auto',
  },
  image: {
    service: { entrypoint: 'astro/assets/services/sharp' },
  },
});
