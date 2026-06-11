import { ui, type Lang } from '../i18n/ui';

// Locale-neutral consultor data. Copy that changes per language
// (bio, cargo, WhatsApp messages, quote) lives in src/i18n/ui.ts.
export const consultor = {
  nome: 'Jaime Pena Cal Junior',
  primeiroNome: 'Jaime Pena',
  creci: 'CRECI-BA 13959',
  whatsapp: '5571999549495',
  whatsappFormatado: '(71) 99954-9495',
  email: 'jaime-construtora.mouradubeux@proton.me',
  cidade: 'Salvador, Bahia',
  foto: '/images/consultor/jaime.jpg',
};

/**
 * Build a wa.me URL with a locale-aware prefilled message.
 * Pass `extra` to override the default greeting (e.g. a property-specific text).
 */
export function whatsappUrl(lang: Lang = 'pt', extra?: string) {
  const msg = extra || ui[lang].whatsapp_msg_default;
  return `https://wa.me/${consultor.whatsapp}?text=${encodeURIComponent(msg)}`;
}
