import { ui, type Lang } from '../i18n/ui';

// Locale-neutral consultor data. Copy that changes per language
// (bio, cargo, WhatsApp messages, quote) lives in src/i18n/ui.ts.
export const consultor = {
  nome: 'Jaime Pena Cal Junior',
  primeiroNome: 'Jaime Pena',
  creci: 'CRECI-BA 13959',
  whatsapp: '5571999549495',
  whatsappFormatado: '(71) 99954-9495',
  whatsappFormatadoIntl: '+55 71 99954-9495',
  email: 'jaime-construtora.mouradubeux@proton.me',
  cidade: 'Salvador, Bahia',
  foto: '/images/consultor/jaime-novo.jpg',
};

/**
 * Build a wa.me URL with a locale-aware prefilled message.
 * The wa.me link uses the full international number (55…), so the WhatsApp
 * button works identically from any country.
 * Pass `extra` to override the default greeting (e.g. a property-specific text).
 */
export function whatsappUrl(lang: Lang = 'pt', extra?: string) {
  const msg = extra || ui[lang].whatsapp_msg_default;
  return `https://wa.me/${consultor.whatsapp}?text=${encodeURIComponent(msg)}`;
}

/**
 * Phone number for display. PT keeps the local Brazilian format;
 * every other language shows the international format with +55.
 */
export function phoneDisplay(lang: Lang = 'pt') {
  return lang === 'pt' ? consultor.whatsappFormatado : consultor.whatsappFormatadoIntl;
}
