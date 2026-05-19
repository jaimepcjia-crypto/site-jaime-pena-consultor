export const consultor = {
  nome: 'Jaime Pena Cal Junior',
  primeiroNome: 'Jaime Pena',
  cargo: 'Especialista em Imóveis · Moura Dubeux',
  creci: 'CRECI-BA 13959',
  whatsapp: '5571999549495',
  whatsappFormatado: '(71) 99954-9495',
  email: 'jaime-construtora.mouradubeux@proton.me',
  cidade: 'Salvador, Bahia',
  bio: 'Especialista em imóveis em Salvador, dedicado aos empreendimentos Moura Dubeux. Atuo na curadoria de residências que unem localização privilegiada, arquitetura assinada e valorização patrimonial — do Horto Florestal ao Caminho das Árvores, do Rio Vermelho à orla atlântica.',
  bioCurta: 'Especialista em empreendimentos Moura Dubeux em Salvador.',
  foto: '/images/consultor/jaime.jpg',
  whatsappMensagem: 'Olá Jaime, vi seu site e gostaria de mais informações sobre os empreendimentos Moura Dubeux.',
};

export function whatsappUrl(extra?: string) {
  const msg = extra || consultor.whatsappMensagem;
  return `https://wa.me/${consultor.whatsapp}?text=${encodeURIComponent(msg)}`;
}
