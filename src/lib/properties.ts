import dataRaw from '../data/empreendimentos.json';
import dataEn from '../data/empreendimentos.en.json';
import dataEs from '../data/empreendimentos.es.json';
import { ui, type Lang } from '../i18n/ui';

export interface SectionBlock {
  heading: string;
  items: string[];
}

export interface VideoBlock {
  provider: 'youtube' | 'vimeo';
  id: string;
  title: string;
}

export type StatusClassification = 'last_units' | 'delivery_first_half_2031';

export interface Empreendimento {
  slug: string;
  title: string;
  construtora: string;
  localizacao: string;
  statusObra: string;
  metragens: string;
  tipologia: string;
  description: string;
  /** Bedroom typologies offered (e.g. [1, 2] → 1 and 2 quartos). */
  quartos?: number[];
  /** Whether the development also offers Studio units. */
  studio?: boolean;
  statusClassifications?: StatusClassification[];
  heroImage?: string;
  images: string[];
  videos?: VideoBlock[];
  sections?: SectionBlock[];
}

/** Fields that get translated per locale (keyed by slug in the .en/.es JSON). */
type TranslatableFields = Partial<
  Pick<Empreendimento, 'localizacao' | 'statusObra' | 'metragens' | 'tipologia' | 'description' | 'sections'>
>;

// PT is the master dataset (full structure incl. images/videos/proper nouns).
export const empreendimentos: Empreendimento[] = dataRaw as Empreendimento[];

const ptBySlug = new Map(empreendimentos.map((e) => [e.slug, e]));
const overrides: Record<Lang, Record<string, TranslatableFields>> = {
  pt: {},
  en: dataEn as Record<string, TranslatableFields>,
  es: dataEs as Record<string, TranslatableFields>,
};

/** A property merged with its locale overrides (falls back to PT per-field). */
export function getEmpreendimento(slug: string, lang: Lang = 'pt'): Empreendimento | undefined {
  const base = ptBySlug.get(slug);
  if (!base) return undefined;
  if (lang === 'pt') return base;
  const tr = overrides[lang]?.[slug];
  return tr ? { ...base, ...tr } : base;
}

/** Full localized list, preserving the master order. */
export function getEmpreendimentos(lang: Lang = 'pt'): Empreendimento[] {
  if (lang === 'pt') return empreendimentos;
  return empreendimentos.map((e) => getEmpreendimento(e.slug, lang)!);
}

export type StatusTone = 'soon' | 'ready' | 'sold' | 'building' | 'available';
export interface StatusBadge {
  label: string;
  tone: StatusTone;
}

/**
 * Status badge derived ALWAYS from the canonical PT `statusObra` text
 * (the parser keys on PT words), with the label localized per `lang`.
 * The PT branch reproduces the original output exactly.
 */
export function statusBadge(rawPt: string, lang: Lang = 'pt'): StatusBadge {
  const t = ui[lang];
  const s = rawPt.toUpperCase();
  if (s.includes('PRONTO')) return { label: t.status_pronto, tone: 'ready' };
  if (s.includes('ENTREGUE')) return { label: t.status_entregue, tone: 'sold' };
  if (s.includes('VENDIDO')) return { label: t.status_vendido, tone: 'sold' };
  if (s.includes('PREVISÃO') || s.includes('CONCLUSÃO')) {
    const m = rawPt.match(/(JANEIRO|FEVEREIRO|MARÇO|ABRIL|MAIO|JUNHO|JULHO|AGOSTO|SETEMBRO|OUTUBRO|NOVEMBRO|DEZEMBRO)[\/\s]*(\d{2,4})/i);
    if (m) {
      const month = lang === 'pt' ? m[1] : localizeMonth(m[1], lang);
      return { label: `${t.status_entrega} ${month}/${m[2]}`, tone: 'building' };
    }
    return { label: t.status_obras, tone: 'building' };
  }
  return { label: rawPt, tone: 'soon' };
}

/** Status badges for a slug, supporting explicit multiple classifications. */
export function statusBadgesFor(slug: string, lang: Lang = 'pt'): StatusBadge[] {
  const base = ptBySlug.get(slug);
  const t = ui[lang];
  const explicit: Record<StatusClassification, StatusBadge> = {
    last_units: { label: t.status_ultimas_unidades, tone: 'available' },
    delivery_first_half_2031: { label: t.status_entrega_primeiro_semestre_2031, tone: 'building' },
  };
  return base?.statusClassifications?.map((classification) => explicit[classification])
    ?? [statusBadge(base?.statusObra ?? '', lang)];
}

/** Primary status retained for consumers that only support one badge. */
export function statusBadgeFor(slug: string, lang: Lang = 'pt') {
  return statusBadgesFor(slug, lang)[0];
}

const PT_MONTHS = ['JANEIRO', 'FEVEREIRO', 'MARÇO', 'ABRIL', 'MAIO', 'JUNHO', 'JULHO', 'AGOSTO', 'SETEMBRO', 'OUTUBRO', 'NOVEMBRO', 'DEZEMBRO'];
function localizeMonth(ptMonth: string, lang: Lang): string {
  const idx = PT_MONTHS.indexOf(ptMonth.toUpperCase());
  if (idx === -1) return ptMonth;
  const key = `month_${String(idx + 1).padStart(2, '0')}` as keyof typeof ui.pt;
  return ui[lang][key];
}

/** Neighborhood name — a proper noun, so parsed from the canonical PT text. */
export function shortLocation(raw: string): string {
  const patterns = [
    /–\s*([A-Za-zÀ-ú\s().]+?)\s*,\s*Salvador/i,
    /–\s*([A-Za-zÀ-ú\s().]+?)\s*–\s*Salvador/i,
    /•\s*([A-Za-zÀ-ú\s().]+?)\s*–\s*Salvador/i,
  ];
  for (const p of patterns) {
    const m = raw.match(p);
    if (m) return m[1].trim().replace(/\s+/g, ' ');
  }
  const fallback = raw.match(/no\s+([A-Za-zÀ-ú\s]+?)(?:,|\.)/);
  if (fallback) return fallback[1].trim();
  return 'Salvador';
}

/** Convenience: neighborhood for a slug from the canonical PT localizacao. */
export function shortLocationFor(slug: string): string {
  const base = ptBySlug.get(slug);
  return shortLocation(base?.localizacao ?? '');
}

export interface LocalizedSection {
  /** Canonical PT heading — stable key for findSection across locales. */
  key: string;
  heading: string;
  items: string[];
}

/**
 * Sections paired by position: canonical PT heading as the lookup key,
 * with localized heading/items. en/es JSON must mirror PT order & length.
 */
export function getLocalizedSections(slug: string, lang: Lang = 'pt'): LocalizedSection[] {
  const base = ptBySlug.get(slug);
  const baseSections = base?.sections ?? [];
  const locSections =
    lang === 'pt' ? baseSections : (overrides[lang]?.[slug]?.sections ?? baseSections);
  return baseSections.map((s, i) => ({
    key: s.heading,
    heading: locSections[i]?.heading ?? s.heading,
    items: locSections[i]?.items ?? s.items,
  }));
}

export function findSection(sections: LocalizedSection[], key: string): LocalizedSection | undefined {
  return sections.find((s) => s.key.toLowerCase() === key.toLowerCase());
}

export function formatBlock(raw: string): { heading: string; items: string[] }[] {
  if (!raw) return [];
  const lines = raw.split('\n').map((l) => l.trim()).filter(Boolean);
  const blocks: { heading: string; items: string[] }[] = [];
  let current: { heading: string; items: string[] } | null = null;
  for (const line of lines) {
    if (line.startsWith('•')) {
      if (!current) current = { heading: 'Detalhes', items: [] };
      current.items.push(line.replace(/^•\s*/, ''));
    } else {
      if (current) blocks.push(current);
      current = { heading: line, items: [] };
    }
  }
  if (current) blocks.push(current);
  return blocks;
}
