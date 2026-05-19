import dataRaw from '../data/empreendimentos.json';

export interface SectionBlock {
  heading: string;
  items: string[];
}

export interface Empreendimento {
  slug: string;
  title: string;
  construtora: string;
  localizacao: string;
  statusObra: string;
  metragens: string;
  tipologia: string;
  description: string;
  heroImage?: string;
  images: string[];
  sections?: SectionBlock[];
}

export const empreendimentos: Empreendimento[] = dataRaw as Empreendimento[];

export function getEmpreendimento(slug: string): Empreendimento | undefined {
  return empreendimentos.find((e) => e.slug === slug);
}

export function statusBadge(raw: string): { label: string; tone: 'soon' | 'ready' | 'sold' | 'building' } {
  const s = raw.toUpperCase();
  if (s.includes('PRONTO')) return { label: 'Pronto para Morar', tone: 'ready' };
  if (s.includes('VENDIDO') || s.includes('ENTREGUE')) return { label: 'Entregue', tone: 'sold' };
  if (s.includes('PREVISÃO') || s.includes('CONCLUSÃO')) {
    const m = raw.match(/(JANEIRO|FEVEREIRO|MARÇO|ABRIL|MAIO|JUNHO|JULHO|AGOSTO|SETEMBRO|OUTUBRO|NOVEMBRO|DEZEMBRO)[\/\s]*(\d{2,4})/i);
    if (m) return { label: `Entrega ${m[1]}/${m[2]}`, tone: 'building' };
    return { label: 'Em Obras', tone: 'building' };
  }
  return { label: raw, tone: 'soon' };
}

export function shortLocation(raw: string): string {
  const m = raw.match(/–\s*([A-Za-zÀ-ú\s]+?),\s*Salvador/i) || raw.match(/–\s*([A-Za-zÀ-ú\s]+)\s*–\s*Salvador/i);
  if (m) return m[1].trim();
  const fallback = raw.match(/no\s+([A-Za-zÀ-ú\s]+?)(?:,|\.)/);
  if (fallback) return fallback[1].trim();
  return 'Salvador';
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
