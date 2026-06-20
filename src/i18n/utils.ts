import { ui, type Lang } from './ui';

export const LOCALES: Lang[] = ['pt', 'en', 'es', 'de'];
export const DEFAULT_LOCALE: Lang = 'pt';

/** Locales that live under a path prefix (everything except the default PT). */
export const NON_DEFAULT_LOCALES: Lang[] = LOCALES.filter((l) => l !== DEFAULT_LOCALE);

/** <html lang="…"> value per locale */
export const htmlLang: Record<Lang, string> = {
  pt: 'pt-BR',
  en: 'en',
  es: 'es',
  de: 'de',
};

/** Human label for the language (used in the switcher tooltips). */
export const langLabel: Record<Lang, string> = {
  pt: 'Português',
  en: 'English',
  es: 'Español',
  de: 'Deutsch',
};

/**
 * Extract the active locale from a URL pathname.
 * PT lives at the root, the others are prefixed (`/en/…`, `/de/…`, …).
 */
export function getLangFromUrl(url: URL): Lang {
  const [, seg] = url.pathname.split('/');
  if ((NON_DEFAULT_LOCALES as string[]).includes(seg)) return seg as Lang;
  return DEFAULT_LOCALE;
}

/**
 * Remove the locale segment from a pathname, returning the canonical (PT) path.
 *   stripLocalePath('/en/sobre/') -> '/sobre/'
 *   stripLocalePath('/de')        -> '/'
 */
export function stripLocalePath(pathname: string): string {
  for (const l of NON_DEFAULT_LOCALES) {
    if (pathname === `/${l}`) return '/';
    if (pathname.startsWith(`/${l}/`)) return pathname.slice(l.length + 1);
  }
  return pathname.startsWith('/') ? pathname : `/${pathname}`;
}

/**
 * Prefix a root-relative path with the locale segment.
 * PT (default) keeps the bare path; the others get `/en` / `/de` / …
 *   localizePath('/sobre/', 'en') -> '/en/sobre/'
 *   localizePath('/', 'es')       -> '/es/'
 */
export function localizePath(path: string, lang: Lang): string {
  const clean = path.startsWith('/') ? path : `/${path}`;
  if (lang === DEFAULT_LOCALE) return clean;
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
