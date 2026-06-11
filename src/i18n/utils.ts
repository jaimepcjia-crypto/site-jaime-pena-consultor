import { ui, type Lang } from './ui';

export const LOCALES: Lang[] = ['pt', 'en', 'es'];
export const DEFAULT_LOCALE: Lang = 'pt';

/** <html lang="…"> value per locale */
export const htmlLang: Record<Lang, string> = {
  pt: 'pt-BR',
  en: 'en',
  es: 'es',
};

/** Human label for the language (used in the switcher tooltips). */
export const langLabel: Record<Lang, string> = {
  pt: 'Português',
  en: 'English',
  es: 'Español',
};

/**
 * Extract the active locale from a URL pathname.
 * PT lives at the root, EN/ES are prefixed (`/en/…`, `/es/…`).
 */
export function getLangFromUrl(url: URL): Lang {
  const [, seg] = url.pathname.split('/');
  if (seg === 'en' || seg === 'es') return seg;
  return 'pt';
}

/**
 * Prefix a root-relative path with the locale segment.
 * PT (default) keeps the bare path; EN/ES get `/en` / `/es`.
 *   localizePath('/sobre/', 'en') -> '/en/sobre/'
 *   localizePath('/', 'es')       -> '/es/'
 */
export function localizePath(path: string, lang: Lang): string {
  const clean = path.startsWith('/') ? path : `/${path}`;
  if (lang === 'pt') return clean;
  if (clean === '/') return `/${lang}/`;
  return `/${lang}${clean}`;
}

/**
 * Translator bound to a locale. Falls back to PT, then to the key itself,
 * so a missing string is visible but never crashes the build.
 */
export function useTranslations(lang: Lang) {
  const dict = ui[lang] ?? ui.pt;
  return function t(key: keyof typeof ui.pt): string {
    return (dict[key] as string) ?? (ui.pt[key] as string) ?? String(key);
  };
}

export type { Lang };
