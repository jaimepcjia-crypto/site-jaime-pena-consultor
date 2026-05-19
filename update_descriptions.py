"""Parse new structured descriptions and update empreendimentos.json with `sections` field."""
import json
import re
from pathlib import Path

JSON_PATH = Path(__file__).parent / "src" / "data" / "empreendimentos.json"

# Slug order matches the user-provided numbered list (1..15)
SLUG_ORDER = [
    "vivant-caminho-das-arvores", "rive", "poeme-horto",
    "mood-costa-azul", "mood-colina", "mood-club",
    "mirat-martins-de-sa", "infinity-salvador", "horto-essence",
    "dumare", "casa-sombreiros", "elleve-horto",
    "beach-class-rio-vermelho", "beach-class-jaguaribe", "beach-class-bahia",
]

# Raw content from user message - each entry is "DESCRIÇÃO + sections"
RAW = r"""@@@ 1
DESCRIÇÃO

VAGAS E ACESSOS

• 2 vagas de garagem por apartamento.
• Estacionamento para visitantes com 2 vagas dedicadas para carregamento de carro elétrico.
• Acesso de veículos por TAG.
• Controle de acesso em todas as áreas comuns.
• Bicicletário interno e bicicletário externo.
• Lobbies de acesso decorados: Lobby Energie e Lobby Harmonie.
• Estar gramado, Lounge 1, Lounge 2 e acesso a um minibosque exclusivo.


ÁREAS COMUNS E LAZER

• Piscina adulto com raia de 22 m e hidromassagem.
• Piscina infantil e solário.
• Gourmet da Piscina.
• Salão de Festas com praça externa dedicada.
• Confraria, espaço gourmet interno.
• Brinquedoteca e Parque Infantil.
• Quadra Esportiva com Quiosque Barbecue, churrasqueira e arquibancada.
• Platô Zen, Platô Kids e Platô Barbecue.
• Horta comunitária.


SAÚDE E BEM-ESTAR

• Academia, Espaço Fitness.
• Espaço Funcional.
• Área para CrossFit.
• Teen Lounge, espaço para adolescentes.


SERVIÇOS E CONVENIÊNCIAS

• Coworking mobiliado.
• Garden Office, escritório integrado ao jardim.
• Espaço E-commerce para recebimento de mercadorias.
• Pet Care, espaço para banho e cuidados.
• Platô Pet, área externa para animais.


SUSTENTABILIDADE

• Selo IPTU Verde - Categoria Ouro.
• Placas solares para geração de energia de parte das áreas comuns.
• Elevadores com sistema de regeneração de energia elétrica.
• Reuso de águas pluviais e águas de condensação de aparelhos de ar-condicionado.
• Medidores individuais de água.
• Sensores de presença para iluminação das áreas comuns.
• Bacias sanitárias com sistema de volume reduzido.


SEGURANÇA E TECNOLOGIA

• Guarita com vidro blindado.
• Sistema de clausura para pedestres.
• Infraestrutura para portaria remota.
• Infraestrutura para circuito interno de TV, CFTV.
• Fechadura eletrônica instalada nas portas sociais de todos os apartamentos.
• Wi-Fi, tomada USB e tomada convencional disponíveis nas áreas comuns.
• Acesso de veículos por TAG.
• Controle de acesso em todas as áreas comuns.


PROJETO, CONCEITO E AUTORIA

• Arquitetura: André Sá & Francisco Mota Arquitetos.
• Paisagismo: Cardim Arquitetura Paisagística, com Ricardo Cardim e Alessandra Cardim.
• Ambientação: Estúdio RM, Rogério Menezes.
• Conceito: o Vivant foi projetado para integrar natureza exuberante, paisagismo biofílico e acesso ao bosque com as facilidades urbanas do Caminho das Árvores, priorizando modernidade, conforto e sofisticação.


DIFERENCIAIS DAS UNIDADES E PERSONALIZAÇÃO

• Esquadrias com tratamento acústico.
• Fechadura eletrônica instalada nas portas sociais de todos os apartamentos.


DIFERENCIAIS DE MERCADO

• Acesso a um minibosque exclusivo, com estar gramado, Lounge 1, Lounge 2, paisagismo biofílico e integração com as facilidades urbanas do Caminho das Árvores.
• Piscina adulto com raia de 22 m e hidromassagem, piscina infantil, solário, Gourmet da Piscina, Salão de Festas, Confraria e quadra com Quiosque Barbecue.
• Coworking mobiliado, Garden Office integrado ao jardim, Espaço E-commerce, Pet Care e Platô Pet.
• Selo IPTU Verde - Categoria Ouro, placas solares, reuso de águas pluviais e de condensação, elevadores com regeneração de energia, medidores individuais e sensores de presença.
• Guarita com vidro blindado, clausura para pedestres, portaria remota, CFTV, TAG, controle de acesso e fechadura eletrônica nos apartamentos.

@@@ 2
DESCRIÇÃO

VAGAS E ACESSOS

• Unidades de 3 quartos com 2 vagas de garagem.
• Unidades de 4 quartos com 2 vagas de garagem.
• Acessos independentes para veículos nos níveis G1, G2 e G3.
• Acesso de pedestres com clausura no nível G2.
• Bicicletários equipados.
• Infraestrutura para tomada de carregamento de carro elétrico, sendo 1 para cada apartamento.


ÁREAS COMUNS E LAZER

• Rooftop com vista mar.
• Piscina adulto aquecida com borda infinita e vista panorâmica para o oceano.
• Piscina infantil aquecida.
• Espaço Gourmet de alto padrão.
• Salão de Festas com varanda externa dedicada.
• Playground Festas.
• Playground Mirante.
• Sala de Jogos.
• Brinquedoteca com áreas interna e externa.
• Quadra Esportiva.
• Espaço Gourmet de apoio à quadra.
• Pet Place dedicado ao lazer animal.
• Lobby social decorado.


SAÚDE E BEM-ESTAR

• Academia climatizada com 80 m² e equipamentos profissionais.
• Fitness Externo.


SERVIÇOS E CONVENIÊNCIAS

• Sala para Delivery e E-commerce.
• Minimarket interno, espaço sugerido para implantação.
• 5 bikes elétricas exclusivas do condomínio, Moura Dubeux Share.


SUSTENTABILIDADE

• Selo IPTU Verde.
• Reuso de águas de condensação de ar-condicionado.
• Bacias sanitárias com sistema dual flush para economia de água.
• Torneiras com temporizador nas áreas comuns.
• Infraestrutura para tomada de carregamento de carro elétrico, sendo 1 para cada apartamento.


SEGURANÇA E TECNOLOGIA

• Guarita com vidros blindados.
• Sistema de eclusa para pedestres.
• Infraestrutura para proteção perimetral.
• Sistema de CFTV projetado por especialistas.
• Fechadura eletrônica nas portas sociais de todos os apartamentos.


PROJETO, CONCEITO E AUTORIA

• Arquitetura e Ambientação: Sidney Quintela.
• Paisagismo: Guilherme Takeda, com conceito biofílico.
• Arte exclusiva: obra do artista Arthur Fraga integrada à fachada/acesso do empreendimento, retratando memórias afetivas do Rio Vermelho.


DIFERENCIAIS DAS UNIDADES E PERSONALIZAÇÃO

• Esquadria de correr entre sala e varanda para integração total.
• Personalização MD Store: possibilidade de personalizar o apartamento antes da entrega, incluindo alteração de plantas, cozinha aberta, suítes ampliadas, revestimentos de pisos e paredes, bancadas, metais, louças e acessórios.
• Fechadura eletrônica nas portas sociais de todos os apartamentos.
• Infraestrutura para tomada de carregamento de carro elétrico, sendo 1 para cada apartamento.


DIFERENCIAIS DE MERCADO

• Rooftop com vista mar, piscina adulto aquecida com borda infinita e vista panorâmica para o oceano.
• Academia climatizada com 80 m², equipamentos profissionais e Fitness Externo.
• Personalização MD Store antes da entrega, com alteração de plantas, cozinha aberta, suítes ampliadas, revestimentos, bancadas, metais, louças e acessórios.
• Arte exclusiva de Arthur Fraga integrada à fachada/acesso do empreendimento, retratando memórias afetivas do Rio Vermelho.
• Infraestrutura para tomada de carregamento de carro elétrico em cada apartamento, 5 bikes elétricas exclusivas do condomínio, bicicletários equipados, minimarket interno e sala para Delivery e E-commerce.

@@@ 3
DESCRIÇÃO

VAGAS E ACESSOS

• 235 vagas privativas no total.
• Unidades de 173,18 m² com 3 vagas de garagem.
• Unidades de 203,91 m², do 1º ao 17º andar, com 3 vagas de garagem.
• Unidades de 203,91 m², do 18º ao 36º andar, com 4 vagas de garagem.
• 13 vagas dedicadas para visitantes.
• Praça de acesso com áreas verdes preservadas.
• Bicicletário equipado.
• Guarita de acesso blindada com sistema de clausura para pedestres.
• Controle de acesso remoto na garagem 03.
• Infraestrutura pronta para carregador de carro elétrico.


ÁREAS COMUNS E LAZER

• Piscina adulto com raia de 25 m.
• Piscina infantil.
• Deck e deck molhado.
• SPA aquecido.
• Salão de Festas com 173 m².
• Espaço Gourmet Externo com churrasqueira.
• Quadra de Tênis / Poliesportiva.
• Playground, Parque Infantil.
• Brinquedoteca temática com 38 m².
• Espaço Jogos Teen.
• Espaço Gourmet com 63 m².
• Salão de Jogos com 70 m².
• Horta comunitária.
• Lobby / Hall de entrada com pé-direito imponente de 86 m².


SAÚDE E BEM-ESTAR

• Fitness com Espaço Funcional de 137 m² e vista para a cidade.
• Espaço de Massagem dedicado.
• SPA aquecido.


SERVIÇOS E CONVENIÊNCIAS

• Sala exclusiva para Delivery e E-commerce.
• Pet Care, espaço para banho e tosa.
• Pet Place localizado no nível G3.
• Depósito privativo individual de até 6 m² para todas as unidades.


SUSTENTABILIDADE

• Bacias sanitárias com sistema dual flush, duplo fluxo.
• Individualização de medidores de água, energia e gás.
• Aproveitamento de águas pluviais e águas de condensação de ar-condicionado.
• Sensores de presença para iluminação em áreas comuns.
• Torneiras com temporizadores em 90% das áreas comuns.
• Infraestrutura pronta para carregador de carro elétrico.


SEGURANÇA E TECNOLOGIA

• Guarita de acesso blindada com sistema de clausura para pedestres.
• Controle de acesso remoto na garagem 03.
• Fechadura eletrônica em todos os apartamentos.
• Infraestrutura completa para Circuito Interno de TV, CFTV.


PROJETO, CONCEITO E AUTORIA

• Arquitetura: Cássio Santana.
• Paisagismo: Benedito Abbud.
• Ambientação e Interiores: Bossa Arquitetura.
• Conceito: o projeto foca no equilíbrio entre o "viver urbano" e o "respirar natural", inspirado na topografia e no verde do Horto Florestal, priorizando ventilação, iluminação natural e sofisticação atemporal.


DIFERENCIAIS DAS UNIDADES E PERSONALIZAÇÃO

• Chuveiros com aquecimento a gás.
• Plantas flexíveis com opções de sala ampliada, cozinha aberta com ilha gourmet, suíte máster com dois banheiros ou dois closets.
• Personalização de acabamentos antes da entrega, com escolha de revestimentos de pisos e paredes, bancadas, metais, louças e acessórios de banheiro.
• Depósito privativo individual de até 6 m² para todas as unidades.


DIFERENCIAIS DE MERCADO

• Unidades de 203,91 m², do 18º ao 36º andar, com 4 vagas de garagem.
• Piscina adulto com raia de 25 m, SPA aquecido, Salão de Festas com 173 m², Fitness com Espaço Funcional de 137 m² e Espaço Gourmet com 63 m².
• Plantas flexíveis com opções de sala ampliada, cozinha aberta com ilha gourmet, suíte máster com dois banheiros ou dois closets.
• Personalização de acabamentos antes da entrega, com escolha de revestimentos de pisos e paredes, bancadas, metais, louças e acessórios de banheiro.
• Projeto com arquitetura de Cássio Santana, paisagismo de Benedito Abbud, ambientação/interiores da Bossa Arquitetura e conceito inspirado na topografia e no verde do Horto Florestal.

@@@ 4
DESCRIÇÃO

VAGAS E ACESSOS

• 407 vagas para automóveis no total, sendo 1 vaga por unidade, com direito de uso rotativo.
• 11 vagas exclusivas para motos.
• 96 vagas para bicicletas, com bicicletário equipado.
• 2 vagas de carga e descarga na portaria.
• Acesso de veículos através de Porte-Cochère para maior segurança.
• Vagas dedicadas para visitantes e aplicativos.
• 2 vagas equipadas com carregadores para carros elétricos, destinadas a visitantes.
• Controle de acesso eletrônico em todas as áreas comuns.


ÁREAS COMUNS E LAZER

• Piscina com borda infinita e vista permanente para o mar.
• Piscina infantil com fonte interativa integrada.
• Quiosque da Piscina.
• Espaço Gourmet equipado.
• Quadra recreativa.
• Área para Street Ball.
• Quiosque exclusivo de apoio à quadra com churrasqueira.
• Salão de Festas amplo.
• Salão de Festas Infantil com palco/teatrinho decorado.
• Brinquedoteca temática.
• Playground externo com balanço, escorregador e cama elástica.
• Praça Central com projeto paisagístico biofílico.
• Praça Pomar.
• Sala de Jogos com mesa de sinuca, pebolim e mesas para jogos de tabuleiro.
• Espaço Teen/Game Station equipado com monitores e pufes para jogos eletrônicos.
• Pet Place, área externa de lazer animal.
• Pet Care, sala interna para banho e higiene.
• Lobby de entrada monumental com pé-direito duplo e decoração contemporânea.


SAÚDE E BEM-ESTAR

• Academia entregue climatizada, decorada, equipada e com vista mar.


SERVIÇOS E CONVENIÊNCIAS

• Espaço Coworking mobiliado com mesas de reunião e estações de trabalho individuais.
• Mini Market interno, espaço para conveniência rápida.
• Sala para armazenamento de compras, Delivery e E-commerce.
• Lavanderia coletiva entregue equipada.


SUSTENTABILIDADE

• Certificação IPTU Verde.
• Reutilização da água da chuva para irrigação dos jardins.
• Aproveitamento de águas de condensação dos aparelhos de ar-condicionado.
• Iluminação automatizada com sensores de presença em partes das áreas comuns.
• Placas solares para geração de energia de parte do condomínio.
• Elevadores com sistema de regeneração de energia elétrica.
• Uso de dispositivos de redução de vazão em torneiras e vasos sanitários.
• 2 vagas equipadas com carregadores para carros elétricos, destinadas a visitantes.


SEGURANÇA E TECNOLOGIA

• Guarita blindada com sistema de clausura para pedestres.
• Controle de acesso eletrônico em todas as áreas comuns.
• Fechadura eletrônica nas portas sociais de todos os apartamentos.
• Infraestrutura seca para projeto de segurança condominial por CFTV.
• Wi-Fi nas áreas comuns.
• Esquadrias com tratamento acústico superior.


PROJETO, CONCEITO E AUTORIA

• Arquitetura: Carlos Campelo, com foco na ventilação natural e valorização da paisagem.
• Paisagismo: Takeda Design, com conceito biofílico para reconexão com a natureza.
• Interiores e Fachada: Todos Arquitetura, Fábio Mota e Maurício Arruda, priorizando transparências na fachada e paleta de cores neutras e solares.


DIFERENCIAIS DAS UNIDADES E PERSONALIZAÇÃO

• Apartamentos entregues com esquadria de correr entre sala e varanda, permitindo integração total.
• Infraestrutura para bancada gourmet nas varandas, com água e esgoto.
• Esquadrias com tratamento acústico superior.
• Fechadura eletrônica nas portas sociais de todos os apartamentos.
• MD Store: programa de personalização que permite alterações de planta, como sala ampliada, e escolha de acabamentos antes da entrega.


DIFERENCIAIS DE MERCADO

• Piscina com borda infinita e vista permanente para o mar.
• Academia climatizada, decorada, equipada e com vista mar.
• Lazer com mais de 15 itens, incluindo Salão de Festas amplo, Salão de Festas Infantil, brinquedoteca temática, playground externo, Espaço Teen/Game Station, quadra recreativa, Street Ball, Sala de Jogos, Pet Place e Pet Care.
• Certificação IPTU Verde, com reutilização da água da chuva, aproveitamento de águas de condensação, placas solares, elevadores com regeneração de energia e sensores de presença.
• Apartamentos com esquadria de correr entre sala e varanda, infraestrutura para bancada gourmet nas varandas, esquadrias com tratamento acústico superior e MD Store para personalização antes da entrega.

@@@ 5
DESCRIÇÃO

VAGAS E ACESSOS

• 1 vaga de estacionamento privativa por apartamento.
• Edifício Garagem dedicado, Deck Park.
• Vagas para visitantes e carga/descarga na portaria.
• Bicicletário estruturado.
• Vagas de visitante com carregador para carro elétrico.
• Controle de acesso em áreas comuns.
• Acesso de veículos por TAG.


ÁREAS COMUNS E LAZER

• Infraestrutura de lazer completa, com mais de 15 itens.
• Piscina adulto com raia de 20 m e deck molhado.
• Piscina infantil integrada ao conjunto aquático.
• Gourmet Piscina, quiosque equipado junto às piscinas.
• Quadra Recreativa localizada no 6º pavimento do Deck Park, com quiosque Barbecue de apoio.
• Salão de Festas amplo com terraço integrado.
• Salão de Festas Infantil dedicado.
• Brinquedoteca com área externa.
• Playground infantil equipado.
• Sala de Jogos.
• Sala Funcional para atividades diversas.
• Horta comunitária.
• Pomar para os moradores.
• Lounges de convivência.
• Praça Pública integrada ao projeto.
• Pet Care, espaço interno de banho e cuidados.
• Pet Place, área externa de recreação animal.
• Lobby de entrada com pé-direito duplo e arquitetura minimalista.


SAÚDE E BEM-ESTAR

• Academia, Fitness, entregue climatizada, decorada e equipada.
• Academia com painéis de vidro para valorização da vista.


SERVIÇOS E CONVENIÊNCIAS

• Espaço Coworking mobiliado para trabalho e reuniões.
• Espaço E-commerce.
• Infraestrutura para recebimento de Delivery na guarita.
• Mini Market interno para compras de conveniência.
• Lavanderia coletiva entregue equipada.


SUSTENTABILIDADE

• Projeto Certificado IPTU Verde.
• Reutilização da água da chuva para irrigação de jardins.
• Aproveitamento de águas de condensação dos aparelhos de ar-condicionado.
• Iluminação automatizada com sensores de presença em áreas comuns.
• Placas solares para geração de energia limpa em parte das áreas comuns.
• Elevadores com sistema de regeneração de energia elétrica.
• Calçadas com pavimentação 100% drenante.
• Uso de dispositivos de redução de vazão de água em torneiras e bacias sanitárias.
• Vagas de visitante com carregador para carro elétrico.


SEGURANÇA E TECNOLOGIA

• Guarita com vidros blindados.
• Sistema de clausura para pedestres.
• Controle de acesso em áreas comuns.
• Acesso de veículos por TAG.
• Fechadura eletrônica na porta social de todos os apartamentos.
• Infraestrutura seca para Wi-Fi em áreas comuns.
• Infraestrutura seca para projeto de segurança por CFTV.


PROJETO, CONCEITO E AUTORIA

• Arquitetura: Alessandro Grimaldi, com foco na topografia elevada e ventilação eficiente.
• Paisagismo: Takeda Design, com metodologia biofílica para reconexão com a natureza.
• Ambientação e Fachada: Todos Arquitetura, Fábio Mota e Maurício Arruda, utilizando paleta de cores solar e neutra, inspirada na essência praiana de Patamares.


DIFERENCIAIS DAS UNIDADES E PERSONALIZAÇÃO

• Todas as unidades possuem varanda gourmet, entregue com infraestrutura de água e esgoto.
• Apartamentos entregues com esquadria de correr entre sala e varanda para integração plena.
• Esquadrias com tratamento acústico.
• Fechadura eletrônica na porta social de todos os apartamentos.
• MD Store: possibilidade de personalização de acabamentos, incluindo pisos, paredes, bancadas e louças, antes da entrega.


DIFERENCIAIS DE MERCADO

• Infraestrutura de lazer completa, com mais de 15 itens, incluindo piscina adulto com raia de 20 m, piscina infantil, quadra recreativa, salão de festas, salão infantil, brinquedoteca, playground, sala de jogos, horta, pomar, lounges e praça pública integrada ao projeto.
• Academia entregue climatizada, decorada e equipada, com painéis de vidro para valorização da vista.
• Projeto Certificado IPTU Verde, com reutilização da água da chuva, aproveitamento de águas de condensação, placas solares, elevadores com regeneração de energia, sensores de presença, pavimentação 100% drenante e carregador para carro elétrico em vagas de visitante.
• Todas as unidades com varanda gourmet entregue com infraestrutura de água e esgoto, esquadria de correr entre sala e varanda, tratamento acústico e MD Store para personalização de acabamentos antes da entrega.
• Segurança e tecnologia com guarita blindada, clausura para pedestres, controle de acesso, TAG, fechadura eletrônica, Wi-Fi em áreas comuns e infraestrutura para CFTV.

@@@ 6
DESCRIÇÃO

VAGAS E ACESSOS

• Edifício Garagem, Deck Park, exclusivo com 6 pavimentos e circulação vertical.
• Total de 544 vagas, sendo 1 vaga de estacionamento por apartamento.
• 3 vagas exclusivas para aplicativos.
• 1 vaga de carga e descarga.
• 84 vagas para bicicletas, com bicicletário.
• Porte-Cochère para embarque e desembarque seguro.
• Controle de acesso eletrônico nas áreas comuns.
• Acesso de veículos por TAG.


ÁREAS COMUNS E LAZER

• Piscina adulto com raia de 20 m e deck molhado.
• Piscina infantil.
• Solário.
• Espaço Gourmet Piscina.
• Gourmet Interno.
• Salão de Festas com terraço integrado.
• Quadra Recreativa localizada no 6º pavimento do Deck Park, com Apoio Gourmet.
• Parque Infantil.
• Praça Pomar.
• Horta Comunitária.
• Salão de Jogos.
• Brinquedoteca.
• Teen Lounge.
• Pet Place, lazer externo.
• Pet Care, espaço para banho e higiene animal.
• Praça de convívio.
• Lounges externos.
• Lobby individual por torre.
• Lobby principal de recepção.


SAÚDE E BEM-ESTAR

• Academia profissional climatizada e equipada.


SERVIÇOS E CONVENIÊNCIAS

• Espaço Coworking mobiliado.
• Mini Market com sistema Grab and Go.
• Lavanderia coletiva, espaço entregue pela construtora para futura operação.
• Espaço E-commerce.
• Gestão de Delivery na guarita.


SUSTENTABILIDADE

• Selo IPTU Verde - Categoria Ouro.
• Reutilização de água de condensação dos aparelhos de ar-condicionado das áreas comuns.
• Geração de energia por fontes renováveis, com placas solares para parte das áreas comuns.
• Iluminação automatizada com sensores de presença.
• Medidores individuais de água.
• Pavimentação 100% drenante na calçada.
• Elevadores com sistema de regeneração de energia elétrica.
• Gestão eficiente de resíduos durante a obra.
• Uso de dispositivos de redução de vazão de água em torneiras e bacias sanitárias.


SEGURANÇA E TECNOLOGIA

• Guarita com vidro blindado.
• Sistema de clausura para pedestres.
• Controle de acesso eletrônico nas áreas comuns.
• Acesso de veículos por TAG.
• Fechadura eletrônica na porta social de todos os apartamentos.
• Infraestrutura seca para projeto de segurança condominial.
• Wi-Fi nas áreas comuns.


PROJETO, CONCEITO E AUTORIA

• Arquitetura: Carlos Campelo, com foco no resgate histórico do endereço e na renovação urbana.
• Paisagismo: Takeda Design, com conceito de conexão fluida e orgânica entre as torres.


DIFERENCIAIS DAS UNIDADES E PERSONALIZAÇÃO

• Esquadrias com tratamento acústico.
• Fechadura eletrônica na porta social de todos os apartamentos.
• Diferencial MD Store: possibilidade de personalização de plantas e acabamentos diretamente com a Moura Dubeux antes da entrega.


DIFERENCIAIS DE MERCADO

• Edifício Garagem, Deck Park, exclusivo com 6 pavimentos, circulação vertical, 544 vagas, 3 vagas para aplicativos, 1 vaga de carga e descarga e 84 vagas para bicicletas.
• Lazer com piscina adulto com raia de 20 m, piscina infantil, solário, espaços gourmet, salão de festas, quadra recreativa no 6º pavimento do Deck Park, parque infantil, salão de jogos, brinquedoteca, Teen Lounge, Pet Place e Pet Care.
• Serviços com Espaço Coworking mobiliado, Mini Market Grab and Go, lavanderia coletiva, Espaço E-commerce e Gestão de Delivery na guarita.
• Selo IPTU Verde - Categoria Ouro, com placas solares, reuso de água de condensação, sensores de presença, medidores individuais, pavimentação 100% drenante, elevadores regenerativos e gestão eficiente de resíduos durante a obra.
• Segurança, tecnologia e personalização com guarita blindada, clausura para pedestres, controle eletrônico, TAG, fechadura eletrônica, Wi-Fi nas áreas comuns, esquadrias com tratamento acústico e MD Store.

@@@ 7
DESCRIÇÃO

VAGAS E ACESSOS

• Praça de acesso com projeto paisagístico.
• 11 vagas internas exclusivas para visitantes.
• Bicicletário equipado.
• 2 tomadas dedicadas para carregamento de carros elétricos.


ÁREAS COMUNS E LAZER

• Edifício de torre única com design arrojado e 3 pavimentos inteiramente dedicados ao lazer.
• Piscina adulto com raia de 20 metros e hidromassagem integrada.
• Piscina infantil.
• Deck seco.
• Salão de Festas climatizado e mobiliado.
• Espaço Confraria / Salão de Jogos com terraço gourmet privativo.
• Brinquedoteca temática.
• Playground externo.
• Minicampo de futebol gramado e cercado.
• Área de Lutas e Dança.
• Pet Play, espaço externo de recreação.
• Pet Care, espaço para banho e cuidados.
• Lobby / Hall Social com decoração de alto padrão e pé-direito duplo.


SAÚDE E BEM-ESTAR

• Espaço Wellness completo.
• SPA com ofurô.
• Salas de massagem.
• Terraço relax.
• Academia, Fitness profissional, com 130 m².
• Terraço funcional.


SERVIÇOS E CONVENIÊNCIAS

• Depósito privativo individual para cada unidade.


SUSTENTABILIDADE

• Gerador de energia dimensionado para atender ao sistema de emergência e todas as áreas comuns.
• Bacias sanitárias com sistema dual flush para economia de água.
• Torneiras com temporizador.
• Sensores de presença para iluminação nas áreas comuns.


SEGURANÇA E TECNOLOGIA

• Guarita com vidros blindados.
• Eclusa de segurança para pedestres.
• Proteção perimetral monitorada com sistema de CFTV.
• Fechadura eletrônica instalada na porta social de todos os apartamentos.
• Gerador de energia dimensionado para atender ao sistema de emergência e todas as áreas comuns.
• 2 tomadas dedicadas para carregamento de carros elétricos.


PROJETO, CONCEITO E AUTORIA

• Arquitetura: projeto assinado por Cassio Santana, focado em exclusividade e integração ao verde.
• Interiores e Lazer: áreas comuns e de lazer projetadas e decoradas por Flávio Moura.
• Conceito: o Mirat foi concebido para ser um marco no segmento de alto luxo do Horto Florestal, priorizando a vista planejada e definitiva para o mar e a sofisticação em cada detalhe construtivo.
• O projeto segue o padrão de sofisticação de marcos imobiliários como o Mansão Bahiano de Tênis e o Undae Ocean.


DIFERENCIAIS DAS UNIDADES E PERSONALIZAÇÃO

• Esquadrias acústicas para maior conforto térmico e sonoro.
• Fechadura eletrônica instalada na porta social de todos os apartamentos.
• Depósito privativo individual para cada unidade.


DIFERENCIAIS DE MERCADO

• Edifício de torre única com design arrojado e 3 pavimentos inteiramente dedicados ao lazer.
• Piscina adulto com raia de 20 metros, hidromassagem integrada, Espaço Wellness completo, SPA com ofurô, salas de massagem, terraço relax e academia profissional com 130 m².
• Projeto assinado por Cassio Santana, com interiores e lazer projetados e decorados por Flávio Moura.
• Conceito de alto luxo no Horto Florestal, com vista planejada e definitiva para o mar.
• Segurança e tecnologia com guarita blindada, eclusa para pedestres, proteção perimetral com CFTV, fechadura eletrônica, gerador para emergência e áreas comuns, além de 2 tomadas para carregamento de carros elétricos.

@@@ 8
DESCRIÇÃO

VAGAS E ACESSOS

• Mix de lojas com acesso independente.
• Área de embarque e desembarque, Porte-Cochère.
• Acesso exclusivo para Garagem de Visitantes, G1.
• Acessos de garagem exclusivos para proprietários, G2, G3 e G4.
• Acesso de pedestres de serviço independente.


ÁREAS COMUNS E LAZER

• 2º Pavimento com salas e pavimento de lazer completo.
• Piscina ampla com borda infinita e vista para o oceano.
• Restaurante exclusivo.
• Lounge Bar.
• Estar Gourmet.
• Espaço Gourmet dedicado.
• Spa e área de relaxamento.
• Quadra de Tênis.
• Quadra de Beach Tênis.
• Quadra Recreativa.
• Brinquedoteca.
• Espaço de Jogos.
• Pet Place.
• Praça de convivência externa.
• Lobby exclusivo para o pavimento de lazer.


SAÚDE E BEM-ESTAR

• Fitness, academia profissional climatizada.
• Spa e área de relaxamento.


SERVIÇOS E CONVENIÊNCIAS

• Lobby e Recepção Social com concierge.
• Sistema Grab and Go, conveniência rápida.
• Mix de lojas com acesso independente.


BUSINESS E CORPORATIVO

• Infinity Business: setor voltado para negócios com frente para a Avenida Oceânica.
• Salas Garden com áreas privativas somadas a jardins externos exclusivos.
• Lâminas corporativas de 430 m² para grandes empresas.
• Infraestrutura moderna para escritórios e consultórios.


DISTRIBUIÇÃO E ESTRUTURA DO EMPREENDIMENTO

• Complexo dividido em três torres/setores integrados.
• Infinity Apartments: torre central em formato "Y".
• Infinity Residence: torre lateral voltada para moradia.
• Infinity Business: setor voltado para negócios com frente para a Avenida Oceânica.
• Térreo / Recepção / G1.
• G2 e G3, incluindo Salas Garden.
• 1º Pavimento Sala / G4.
• 2º Pavimento: salas e pavimento de lazer completo.
• 3º ao 15º Pavimento: pavimentos tipo.
• 16º Pavimento: cobertura.


SEGURANÇA E TECNOLOGIA

• Infraestrutura para climatização.
• Infraestrutura para automação.
• Alto padrão de acabamento nos lobbies e áreas comuns.


PROJETO, CONCEITO E AUTORIA

• Conceito e histórico: o projeto é uma releitura do antigo Salvador Othon Palace, inaugurado em 1975.
• O projeto une a história do turismo de luxo do Nordeste a um novo conceito de uso misto: residencial, hoteleiro e comercial.
• Empreendimento único e moderno.
• Arquitetura: Sidney Quintela.
• Paisagismo: Alex Hanazaky.
• Interiores: Zirpoli Arquitetura.


DIFERENCIAIS DAS UNIDADES E PERSONALIZAÇÃO

• Piso em porcelanato nas unidades residenciais.
• Infraestrutura para climatização.
• Infraestrutura para automação.


DIFERENCIAIS DE MERCADO

• Releitura do antigo Salvador Othon Palace, inaugurado em 1975, unindo a história do turismo de luxo do Nordeste a um novo conceito de uso misto.
• Complexo integrado com Infinity Apartments, Infinity Residence e Infinity Business, reunindo residencial, hoteleiro e comercial.
• Piscina ampla com borda infinita e vista para o oceano, restaurante exclusivo, Lounge Bar, Spa, quadras, brinquedoteca, Espaço de Jogos, Pet Place e praça externa.
• Infinity Business com salas Garden, jardins externos exclusivos, lâminas corporativas de 430 m², infraestrutura moderna para escritórios e consultórios e frente para a Avenida Oceânica.
• Projeto com arquitetura de Sidney Quintela, paisagismo de Alex Hanazaky e interiores da Zirpoli Arquitetura.

@@@ 9
DESCRIÇÃO

VAGAS E ACESSOS

• Unidades de 133 m² com 2 vagas de garagem.
• Unidades de 167 m² com 3 vagas de garagem.
• Vagas exclusivas para visitantes.
• Acesso de veículos por TAG.
• Bicicletário disponível.
• Acesso exclusivo e direto ao Parque Lucaia.
• Boulevard de acesso com projeto paisagístico de bambus.
• Guarita de acesso pela Rua Sapucaia com estar de espera e reconhecimento facial.
• Lobby de acesso secundário.
• 2 vagas equipadas para carregamento de carro elétrico.


ÁREAS COMUNS E LAZER

• Piscina com raia de 25 m.
• Piscina infantil.
• Lounge Bar.
• Gourmet da Piscina.
• Salão de Festas com apoio de Garden Office.
• Quadra Poliesportiva com dimensões para tênis.
• Gourmet da Quadra dedicado.
• Brinquedoteca conectada ao Parque Infantil externo.
• Pocket Parque, com áreas verdes de convivência.
• Redário.
• Estar sob a copa.
• Pet Parque, área de lazer externa para pets.
• Horta comunitária.
• Lobby social com pé-direito imponente.
• Hall de elevadores sociais e de emergência/serviço.


SAÚDE E BEM-ESTAR

• Espaço Musculação e Espaço Funcional integrados.
• Espaço CrossFit dedicado.
• Fitness Externo.
• Área de relaxamento com Sauna Seca.
• Sala de Massagem.
• Beauty Space, espaço beleza/salão.


SERVIÇOS E CONVENIÊNCIAS

• Espaço E-commerce para recebimento de encomendas.
• Pet Care, espaço para banho e cuidados.
• Casa do Gás.
• Casa de Lixo.
• Áreas técnicas de manutenção.
• Automação de serviços nas áreas comuns.


SUSTENTABILIDADE

• Selo IPTU Verde.
• Placas solares para geração de energia de parte das áreas comuns.
• Irrigação automatizada.
• Sensores de presença para iluminação em áreas técnicas/serviço.
• Infraestrutura para medição individual de água, energia e gás.
• Iluminação em LED em todas as áreas comuns.
• 2 vagas equipadas para carregamento de carro elétrico.


SEGURANÇA E TECNOLOGIA

• Guarita de acesso pela Rua Sapucaia com estar de espera e reconhecimento facial.
• Acesso de veículos por TAG.
• Wi-Fi distribuído nas áreas comuns.
• Tomadas USB e convencionais distribuídas nas áreas comuns.
• Automação de serviços nas áreas comuns.


PROJETO, CONCEITO E AUTORIA

• Arquitetura e Projeto: Sidney Quintela, SQ+ Arquitetos Associados.
• Paisagismo: Takeda Design.
• Conceito: inspirado no bambu, simbolizando leveza, resistência e flexibilidade, focado em criar um refúgio de tranquilidade e sofisticação em meio ao verde urbano.


DIFERENCIAIS DAS UNIDADES E PERSONALIZAÇÃO

• Possibilidades de planta com opções de personalização como cozinha aberta, integração de sala e suítes ampliadas, além de espaço para Home Office/Gabinete conforme a terminação.


DIFERENCIAIS DE MERCADO

• Acesso exclusivo e direto ao Parque Lucaia, com Boulevard de acesso e projeto paisagístico de bambus.
• Piscina com raia de 25 m, quadra poliesportiva com dimensões para tênis, Lounge Bar, Gourmet da Piscina, Salão de Festas, Brinquedoteca conectada ao Parque Infantil externo, Pocket Parque, redário e estar sob a copa.
• Pavimento Wellness com Espaço Musculação, Espaço Funcional, Espaço CrossFit, Fitness Externo, Sauna Seca, Sala de Massagem e Beauty Space.
• Guarita com reconhecimento facial, acesso por TAG, Wi-Fi, tomadas USB/convencionais e automação de serviços nas áreas comuns.
• Selo IPTU Verde, placas solares, irrigação automatizada, sensores de presença, medição individual de água/energia/gás, iluminação em LED e 2 vagas para carregamento de carro elétrico.

@@@ 10
DESCRIÇÃO

VAGAS E ACESSOS

• 2 vagas de garagem privativas por unidade.
• Estacionamento para visitantes com vagas dedicadas.
• Acessos independentes para veículos e pedestres.
• Bicicletário equipado.
• Bicicletário com tomada dedicada para recarga de bicicletas elétricas.
• Infraestrutura para carregamento de carro elétrico, sendo 1 tomada por apartamento.
• Elevadores sociais e elevador de serviço/transbordo.


ÁREAS COMUNS E LAZER

• Piscina adulto com borda infinita e raia de 25 metros.
• Piscina infantil.
• Piscina de Biribol.
• Deck molhado.
• Deck seco.
• Sunbeds, espreguiçadeiras.
• Cabanas de repouso.
• Yacht Bar.
• Poolside Bar integrado ao conjunto aquático.
• Gourmet da Piscina.
• Gourmet Externo com churrasqueira e forno de pizza.
• Quadra Recreativa.
• Área para Street Ball.
• Salão de Festas com varanda e área de apoio.
• Sala de Jogos.
• Game Station, espaço gamer.
• Brinquedoteca temática.
• Parque Infantil.
• Espaço Multiuso Infantil.
• Teen Lounge, estar exclusivo para adolescentes.
• Lounge externo com cascata.
• Praça arborizada.
• Guarderia para pranchas, espaço para armazenamento de pranchas de surf/SUP.
• Pet Place, área externa gramada para pets.
• Horta comunitária para moradores.
• Lobby social de entrada com ambientação de alto padrão.


SAÚDE E BEM-ESTAR

• Academia, Fitness, completa com vista mar.
• Espaço Funcional.
• Terraço dedicado para CrossFit.
• Sala de Massagem privativa.


SERVIÇOS E CONVENIÊNCIAS

• Sala para armazenamento de compras, Delivery e E-commerce, incluindo refrigeração.
• Mini Market, conveniência interna.
• Lavanderia coletiva equipada.
• Pet Care, espaço banho.


SUSTENTABILIDADE

• Selo IPTU Verde.
• Painéis de energia solar para atendimento das áreas comuns.
• Elevadores inteligentes com sistema de regeneração de energia elétrica.
• Reúso de águas pluviais e águas de condensação de aparelhos de ar-condicionado.
• Dispositivos economizadores: torneiras com temporizador e bacias sanitárias dual flush.
• Medidores individuais de água, gás e energia.
• Bicicletário com tomada dedicada para recarga de bicicletas elétricas.
• Infraestrutura para carregamento de carro elétrico, sendo 1 tomada por apartamento.
• Equipamentos de gestão: compactador de lixo e triturador de papel.


SEGURANÇA E TECNOLOGIA

• Guarita de segurança com vidros blindados.
• Sistema de clausura, eclusa, para pedestres.
• Proteção perimetral integrada com sistema de CFTV.
• Fechadura eletrônica nas portas sociais de todas as unidades.
• Gerador para atender ao sistema de emergência e todas as áreas comuns.
• Elevadores inteligentes com sistema de regeneração de energia elétrica.


PROJETO, CONCEITO E AUTORIA

• Arquitetura: Ricardo Farias, com estilo contemporâneo e fachada diferenciada.
• Paisagismo: Takeda Design, com conceito biofílico e integração com o mar.
• Interiores das áreas comuns: Thais Abreu, com foco em fluidez e conforto emocional.
• Interiores dos apartamentos: Thais Braga, com foco em tons neutros e integração.
• Lobby social de entrada com ambientação de alto padrão.


DIFERENCIAIS DAS UNIDADES E PERSONALIZAÇÃO

• Apartamentos entregues com esquadria de correr entre sala e varanda para integração total dos ambientes.
• Infraestrutura completa para bancada gourmet nas varandas.
• Esquadrias com tratamento acústico.
• Fechadura eletrônica nas portas sociais de todas as unidades.
• Infraestrutura para carregamento de carro elétrico, sendo 1 tomada por apartamento.


DIFERENCIAIS DE MERCADO

• Piscina adulto com borda infinita e raia de 25 metros, Yacht Bar, Poolside Bar, cabanas de repouso e vista mar na academia.
• Lazer com piscina infantil, piscina de Biribol, Gourmet Externo com churrasqueira e forno de pizza, quadra recreativa, Street Ball, Game Station, brinquedoteca, parque infantil, espaço multiuso infantil e Teen Lounge.
• Wellness com academia completa com vista mar, Espaço Funcional, terraço dedicado para CrossFit e Sala de Massagem privativa.
• Sustentabilidade com Selo IPTU Verde, energia solar, elevadores regenerativos, reúso de águas, medidores individuais, tomada para carro elétrico por apartamento e tomada para recarga de bicicletas elétricas.
• Apartamentos com esquadria de correr entre sala e varanda, infraestrutura completa para bancada gourmet nas varandas, esquadrias com tratamento acústico e fechadura eletrônica nas portas sociais.

@@@ 11
DESCRIÇÃO

VAGAS E ACESSOS

• 3 vagas de garagem por unidade tipo.
• Estacionamento para visitantes com 11 vagas internas.
• Infraestrutura para carregamento de carros elétricos nas vagas de visitante.
• Vagas exclusivas para motocicletas.
• Bicicletário interno e externo.
• Acesso exclusivo ao minibosque.
• Acesso de veículos por TAG.


ÁREAS COMUNS E LAZER

• Piscina adulto com raia de 25 m.
• Hidromassagem integrada.
• Piscina infantil.
• Conjunto aquático com decks molhados e ilhas de vegetação iluminadas.
• SPA externo.
• Terraço Relax.
• Quadra recreativa para todas as idades.
• Espaço Gourmet da Piscina.
• Espaço Barbecue da Quadra, apoio gourmet.
• Salão de Festas amplo com varanda externa exclusiva.
• Confraria, espaço gourmet interno/jogos gourmet.
• Sala de Jogos.
• Teen Lounge, estar dedicado a adolescentes.
• Brinquedoteca temática.
• Playground pedagógico.
• Praça Central integrada ao paisagismo.
• Pet Care, espaço banho.
• Pet Place, área de lazer externa/Platô Pet.
• Horta comunitária para os moradores.
• Lobby Energie e Lobby Harmonie, halls sociais decorados com pé-direito duplo.


SAÚDE E BEM-ESTAR

• Academia, Fitness, de alto padrão e totalmente equipada.
• Espaço Funcional.
• Área para CrossFit.
• Sala de Massagem dedicada.
• SPA externo.
• Terraço Relax.


SERVIÇOS E CONVENIÊNCIAS

• Coworking mobiliado.
• Garden Office, escritório imerso no verde.
• E-commerce e Sala Delivery para gestão de encomendas.
• Depósito privativo individual para cada unidade.


SUSTENTABILIDADE

• Selo IPTU Verde.
• Placas solares para geração de energia de parte das áreas comuns.
• Reuso de águas pluviais e águas de condensação de aparelhos de ar-condicionado.
• Equipamentos economizadores de água, com torneiras com temporizador em 90% das áreas comuns.
• Bacias sanitárias com sistema dual flush.
• Medidores individuais de água, energia e gás.
• Elevadores com sistema de regeneração de energia elétrica.
• Infraestrutura para carregamento de carros elétricos nas vagas de visitante.


SEGURANÇA E TECNOLOGIA

• Guarita com vidro blindado.
• Sistema de eclusa/clausura para pedestres.
• Fechadura eletrônica instalada nas portas sociais de todos os apartamentos.
• Infraestrutura para portaria remota.
• Sistema de CFTV condominial.
• Wi-Fi disponível em todas as áreas comuns.
• Acesso de veículos por TAG.
• Elevadores com sistema de regeneração de energia elétrica.


PROJETO, CONCEITO E AUTORIA

• Conceito e Arquitetura: inspirado nas sombras e no frescor das alamedas do bairro.
• Arquitetura limpa e contemporânea assinada pelo escritório Architects + Co.
• Paisagismo sensorial e biofílico projetado por Benedito Abbud.
• Ambientação e interiores das áreas comuns assinados por Lais Galvão.


DIFERENCIAIS DAS UNIDADES E PERSONALIZAÇÃO

• Esquadrias com tratamento acústico.
• Chuveiros com aquecimento a gás.
• Fechadura eletrônica instalada nas portas sociais de todos os apartamentos.
• Depósito privativo individual para cada unidade.
• Personalização MD Store: possibilidade de personalização de plantas e escolha assistida de acabamentos, incluindo revestimentos, metais, louças e bancadas, antes da entrega da unidade.


DIFERENCIAIS DE MERCADO

• 3 vagas de garagem por unidade tipo, 11 vagas internas para visitantes, vagas exclusivas para motocicletas, bicicletário interno e externo e infraestrutura para carregamento de carros elétricos.
• Acesso exclusivo ao minibosque, Garden Office imerso no verde, Praça Central integrada ao paisagismo, horta comunitária e conceito inspirado nas sombras e no frescor das alamedas do bairro.
• Piscina adulto com raia de 25 m, hidromassagem integrada, SPA externo, Terraço Relax, academia totalmente equipada, Espaço Funcional, CrossFit e Sala de Massagem.
• Selo IPTU Verde, placas solares, reuso de águas pluviais e de condensação, medidores individuais, bacias dual flush, torneiras com temporizador e elevadores com regeneração de energia.
• Esquadrias com tratamento acústico, chuveiros com aquecimento a gás, fechadura eletrônica, depósito privativo individual e personalização MD Store antes da entrega.

@@@ 12
DESCRIÇÃO

VAGAS E ACESSOS

• 191 vagas internas no total.
• 2 vagas de garagem para os apartamentos de 3 suítes.
• 3 vagas de garagem para os apartamentos de 4 suítes.
• 1 vaga condominial dedicada.
• Estacionamento para visitantes com vagas externas.
• Infraestrutura para carregamento de carro elétrico, com 2 vagas com carregador.
• Acesso controlado ao Loteamento Jardim Teresópolis.
• Acesso à Rua Piratancará.
• Bicicletário equipado.
• Acesso de veículos por TAG.


ÁREAS COMUNS E LAZER

• Piscina adulto com raia de 25 metros e hidromassagem integrada.
• Piscina infantil.
• Solário / Deck.
• Lounge externo com cascata.
• Salão de Festas com copa de apoio.
• Praça externa dedicada.
• Espaço Gourmet Piscina.
• Espaço Apoio Quadra.
• Quadra Recreativa.
• Parque Infantil com brinquedos de impacto social positivo.
• Brinquedoteca temática.
• Sala de Jogos.
• Teen Lounge.
• Lobby Social Energie e Lobby Harmonie, com pé-direito imponente e halls de elevadores decorados.


SAÚDE E BEM-ESTAR

• Academia, Espaço Fitness, desenvolvida por especialistas.
• Espaço Funcional.
• Área para CrossFit.


SERVIÇOS E CONVENIÊNCIAS

• Coworking mobiliado.
• Sala de reuniões.
• Pet Care, espaço para banho e tosa.
• Pet Place externo.
• Espaço Delivery e E-commerce para gestão de encomendas.
• Lavanderia compartilhada.
• Pet Wash.
• Áreas operacionais: copa e vestiários de funcionários, administração e áreas técnicas.


SUSTENTABILIDADE

• Selo IPTU Verde - Categoria Ouro.
• Placas solares para geração de energia de parte das áreas comuns.
• Reuso de águas pluviais.
• Reuso de águas de condensação de aparelhos de ar-condicionado.
• Uso de dispositivos economizadores de água, com vazão reduzida em torneiras e bacias sanitárias.
• Iluminação automatizada com sensores de presença em áreas comuns e técnicas.
• Elevadores com sistema de regeneração de energia elétrica.
• Pavimentação 100% drenante na calçada.
• Gestão eficiente de resíduos e descarte responsável durante a obra.
• Infraestrutura para carregamento de carro elétrico, com 2 vagas com carregador.


SEGURANÇA E TECNOLOGIA

• Guarita com vidros blindados.
• Sistema de clausura para pedestres.
• Fechadura eletrônica na porta social de todos os apartamentos.
• Infraestrutura seca para instalação de segurança condominial.
• Wi-Fi nas áreas comuns.
• Acesso de veículos por TAG.


PROJETO, CONCEITO E AUTORIA

• Arquitetura: GAM Arquitetos, com foco em ventilação cruzada, iluminação natural e linhas elegantes.
• Paisagismo: Benedito Abbud, com conceito sensorial, frutíferas e ilhas de vegetação.
• Ambientação: Taís Abreu e Luiza Buratto, com foco em materiais naturais e design brasileiro atemporal.


DIFERENCIAIS DAS UNIDADES E PERSONALIZAÇÃO

• Esquadrias com tratamento acústico.
• Fechadura eletrônica na porta social de todos os apartamentos.
• MD Store: possibilidade de personalização total da planta e escolha assistida de acabamentos, incluindo revestimentos, bancadas, metais e louças, antes da entrega do imóvel.


DIFERENCIAIS DE MERCADO

• 191 vagas internas no total, com 2 vagas para apartamentos de 3 suítes, 3 vagas para apartamentos de 4 suítes, vaga condominial dedicada, vagas externas para visitantes e 2 vagas com carregador para carro elétrico.
• Piscina adulto com raia de 25 metros e hidromassagem integrada, piscina infantil, lounge externo com cascata, salão de festas, espaço gourmet, quadra recreativa, brinquedoteca, sala de jogos e Teen Lounge.
• Academia desenvolvida por especialistas, Espaço Funcional e área para CrossFit.
• Selo IPTU Verde - Categoria Ouro, com placas solares, reuso de águas pluviais e de condensação, dispositivos economizadores de água, sensores de presença, elevadores regenerativos, calçada 100% drenante e gestão eficiente de resíduos.
• MD Store com personalização total da planta e escolha assistida de acabamentos, arquitetura da GAM Arquitetos, paisagismo de Benedito Abbud e ambientação de Taís Abreu e Luiza Buratto.

@@@ 13
DESCRIÇÃO

VAGAS E ACESSOS

• Praça de acesso integrada à via urbana.
• Estacionamento para moradores e visitantes.
• Clausura para pedestre no acesso de serviço.
• Infraestrutura para controle de acesso nas áreas comuns do condomínio.
• Controle de acesso restrito e digital para a torre residencial.
• 2 vagas de garagem equipadas com carregadores dedicados para carros elétricos.
• Sistema de Bike e Scooter Share, com compartilhamento interno de bicicletas e patinetes elétricos.
• Paraciclo.
• Espaço Bike & Scooter Space, oficina e suporte para bikes e patinetes.
• App Car Point, ponto de embarque e desembarque exclusivo para carros de aplicativo.


ÁREAS COMUNS E LAZER

• Coffee Shop, Coffee Shop Lounge e Coworking integrados em amplo espaço de convivência e trabalho.
• Lounge Garden, espaço verde externo com gramado e lounge para descompressão.
• Rooftop com lazer e wellness com vista mar.
• Piscina aquecida com raia e borda infinita de frente para o mar.
• Hidromassagem aquecida.
• Solário com espreguiçadeiras.
• Sky Lounge, estar externo contemplativo no ponto mais alto da torre.
• Lounge externo.
• Gourmet externo com churrasqueira.
• Espaço Confraria no Rooftop, área gourmet fechada e climatizada com sofás e ilha para recepções.
• Mirante com luneta para observação da orla do Rio Vermelho.
• Sanitários sociais de apoio ao rooftop.
• Copa de apoio ao rooftop.


SAÚDE E BEM-ESTAR

• Sky Fitness, academia profissional climatizada e com vista panorâmica para o oceano.
• Hidromassagem aquecida.
• Solário.
• Lounge Garden.


SERVIÇOS E CONVENIÊNCIAS

• Lobby com Hall do Concierge.
• Concierge dedicado.
• Mini Market integrado ao sistema Grab and Go.
• Laundry OMO, lavanderia coletiva montada e operada por empresa terceirizada, no sistema pay-per-use.
• Pet Care, área dedicada ao banho e bem-estar animal.
• Espaço E-commerce.
• Governança.
• Administração/TI.
• Espaço Delivery.
• Coffee Shop.
• Coffee Shop Lounge.
• Coworking.


SUSTENTABILIDADE

• Selo IPTU Verde - Categoria Ouro.
• Infraestrutura para medidores individuais de água.
• Sistema de aproveitamento de águas pluviais para limpeza das áreas comuns.
• Aproveitamento de águas de condensação de aparelhos de ar-condicionado.
• Sensores de presença para iluminação inteligente nas áreas comuns.
• Placas solares fotovoltaicas para geração de energia de parte das áreas comuns.
• Bacias sanitárias ecológicas de volume reduzido.
• 2 vagas de garagem equipadas com carregadores dedicados para carros elétricos.
• Sistema de Bike e Scooter Share.


SEGURANÇA E TECNOLOGIA

• Guarita de serviço para controle.
• Guarita com vidros blindados.
• Clausura para pedestre no acesso de serviço.
• Infraestrutura completa para circuito fechado de TV, CFTV.
• Fechadura eletrônica instalada nas portas sociais de todas as unidades.
• Infraestrutura para controle de acesso nas áreas comuns do condomínio.
• Controle de acesso restrito e digital para a torre residencial.


PROJETO, CONCEITO E AUTORIA

• Arquitetura: GAM Arquitetos, com foco em conceito forte, personalidade arquitetônica e diálogo constante com o entorno histórico do bairro.
• Paisagismo e Rooftop: Takeda Design, com proposta de integração total entre as retas da arquitetura, a borda infinita da piscina e o horizonte do mar.
• Arquitetura de Interiores: IDE Studio, com foco na união entre arte, sofisticação contemporânea, fluidez de linhas e otimização dinâmica para o bem-estar e o convívio dos usuários.
• Conceito do empreendimento: desenvolvido pela Moura Dubeux para atender à tendência de moradia flexível e investimento com alta rentabilidade.
• Foco em trazer comodidade e conveniência, "morar onde tudo acontece", no bairro mais boêmio, artístico e plural de Salvador.


DIFERENCIAIS DAS UNIDADES E PERSONALIZAÇÃO

• Planta Studio de 26 m²: sala/dormitório integrado com 16,60 m², sanitário com 3,20 m² e varanda com 5,70 m².
• Planta Quarto e Sala de 37 m²: sala/kit com 15,00 m², suíte com 10,48 m², sanitário com 3,67 m² e varanda com 8,37 m².
• Planta de 2 Quartos de 67 m²: sala com 18,32 m², cozinha com 8,17 m², suíte com 13,80 m², quarto com 8,87 m², dois sanitários de 3,37 m² cada, varanda com 8,79 m² e área técnica com 2,44 m².
• Piso em porcelanato em todas as dependências das unidades.
• Ponto dedicado para cooktop elétrico.
• Bancada com cuba e tomada para instalação de cooktop elétrico e geladeira.
• Sistema de aquecimento de água por central a gás nos sanitários.
• Previsão estrutural para tanque nas unidades de Quarto e Sala.
• Fechadura eletrônica instalada nas portas sociais de todas as unidades.


DIFERENCIAIS DE MERCADO

• Rooftop com vista mar, piscina aquecida com raia e borda infinita de frente para o mar, hidromassagem aquecida, Sky Lounge, Espaço Confraria, Sky Fitness e mirante com luneta para observação da orla do Rio Vermelho.
• Conveniência com concierge dedicado, Mini Market Grab and Go, Laundry OMO pay-per-use, Pet Care, Espaço E-commerce, Espaço Delivery, Coffee Shop, Coffee Shop Lounge e Coworking.
• Mobilidade com App Car Point, sistema de Bike e Scooter Share, Bike & Scooter Space, paraciclo e 2 vagas com carregadores dedicados para carros elétricos.
• Selo IPTU Verde - Categoria Ouro, com medidores individuais de água, aproveitamento de águas pluviais, águas de condensação, sensores de presença, placas solares e bacias sanitárias ecológicas.
• Plantas flexíveis para moradia e investimento, com Studio de 26 m², Quarto e Sala de 37 m² e 2 Quartos de 67 m², além de conceito voltado à moradia flexível e investimento com alta rentabilidade.

@@@ 14
DESCRIÇÃO

VAGAS E ACESSOS

• 194 vagas de garagem totais.
• 10 vagas exclusivas para veículos elétricos.
• 19 vagas destinadas a bicicletas.
• Estação para carregamento de bicicleta elétrica.
• Acesso para pedestres e veículos.
• Acesso de pedestre por biometria ou TAG.


ÁREAS COMUNS E LAZER

• Piscina com borda infinita e vista panorâmica para o mar.
• Piscina infantil.
• Prainha, deck molhado.
• Solarium.
• SPA.
• Salão de Festas Gourmet com copa de apoio.
• Terraço do Salão de Festas.
• Gourmet Externo.
• Playground infantil.
• Lounge externo.
• Estar externo com projeto paisagístico.
• Pet Place, área externa de lazer para pets no G2.
• Lobby / Hall Social decorado.


SAÚDE E BEM-ESTAR

• Fitness, academia completa com vista mar.
• SPA.
• Solarium.


SERVIÇOS E CONVENIÊNCIAS

• Coliving e Coworking integrados.
• Sistema Grab and Go, conveniência rápida.
• Minimarket para compras essenciais.
• Lavanderia coletiva equipada.
• Guarderia de pranchas e equipamentos náuticos.
• Salas específicas para recebimento de Delivery e E-commerce.
• Área de administração do condomínio.
• Sala de Reuniões exclusiva.
• Pet Care, espaço para banho e tosa.


SUSTENTABILIDADE

• Certificação IPTU Verde - Categoria Ouro.
• Reaproveitamento de águas pluviais.
• Aproveitamento de drenos de ar-condicionado.
• Medição individual de água.
• Louças e metais com dispositivos economizadores.
• Sistema inteligente de iluminação em áreas comuns.
• Placas solares para fonte de energia renovável.
• Pavimentação permeável no passeio.
• 10 vagas exclusivas para veículos elétricos.
• Estação para carregamento de bicicleta elétrica.
• Área para lixo orgânico e reciclável.


SEGURANÇA E TECNOLOGIA

• Portaria blindada.
• Guarita com sistema de clausura para pedestres e veículos.
• Acesso de pedestre por biometria ou TAG.
• Fechadura eletrônica nas portas de todas as unidades.
• Projeto de segurança integrada.
• 4 elevadores de última geração.


PROJETO, CONCEITO E AUTORIA

• Arquitetura e Interiores: GAM Arquitetos.
• Paisagismo: Takeda.
• Conceito arquitetônico: design que integra o estilo mediterrâneo ao "dendê" baiano, focado em ventilação natural, iluminação e conexão permanente com o mar.


DISTRIBUIÇÃO E ESTRUTURA DO EMPREENDIMENTO

• 1 torre única.
• 73 metros de altura total.
• 21 pavimentos.
• 202 unidades residenciais no total.
• 4 elevadores de última geração.
• Do 1º ao 16º andar: 10 apartamentos por andar, Pavimento Tipo 1.
• 17º andar: 10 apartamentos, Pavimento Tipo 2 - Escalonado.
• 18º andar: 8 apartamentos, Pavimento Tipo 3 - Escalonado.
• Do 19º ao 21º andar: 8 apartamentos por andar, Pavimento Tipo 4 - Escalonado.


DIFERENCIAIS DAS UNIDADES E PERSONALIZAÇÃO

• Fechadura eletrônica nas portas de todas as unidades.


DIFERENCIAIS DE MERCADO

• Piscina com borda infinita e vista panorâmica para o mar, piscina infantil, prainha, solarium, SPA, Salão de Festas Gourmet, Gourmet Externo e Fitness com vista mar.
• Mobilidade com 10 vagas exclusivas para veículos elétricos, 19 vagas para bicicletas, estação para carregamento de bicicleta elétrica, guarderia de pranchas e equipamentos náuticos.
• Serviços com Coliving, Coworking, Grab and Go, Minimarket, lavanderia coletiva, Delivery, E-commerce, administração do condomínio e Sala de Reuniões exclusiva.
• Certificação IPTU Verde - Categoria Ouro, com reaproveitamento de águas pluviais, drenos de ar-condicionado, medição individual de água, dispositivos economizadores, placas solares e pavimentação permeável.
• Torre única com 73 metros de altura, 21 pavimentos, 202 unidades, 4 elevadores de última geração e conceito arquitetônico com conexão permanente com o mar.

@@@ 15
DESCRIÇÃO

EXCLUSIVIDADE

• Conexão direta ao Shopping da Bahia através de uma nova passarela exclusiva.
• Primeiro empreendimento do Nordeste localizado dentro de um shopping.


VAGAS E ACESSOS

• 1º ao 5º Pavimento: Deckpark, estacionamento.
• 484 vagas no total.
• Direito de uso de 1 vaga rotativa para todas as unidades.
• 24 vagas de garagem exclusivas para visitantes, incluindo carga/descarga e aplicativos.
• 8 vagas dedicadas para motos.
• Bicicletário estruturado.
• Embarque e desembarque coberto, Porte-Cochère.
• Acesso exclusivo ao estacionamento do Shopping da Bahia, Estacionamento F.
• Controle de acesso eletrônico para pessoas e veículos, com infraestrutura seca.
• Fechadura eletrônica na porta de acesso de todos os apartamentos.
• 2 vagas com carregadores para carros elétricos no estacionamento de visitantes.


ÁREAS COMUNS E LAZER

• 6º Pavimento: lazer e recepção.
• Infraestrutura de lazer no 6º Pavimento, com 3.600 m².
• Piscina adulto com raia de 25 m.
• Prainha.
• Piscina infantil.
• Deck/Solário.
• Gourmet Piscina.
• Quadra de Beach Tennis com lounge de apoio.
• Espaço para Restaurante privativo.
• Salão de Festas com varanda externa.
• Brinquedoteca com salão multiuso e varanda dedicada.
• Espaço para operação de Mini Market e sistema Grab and Go.
• Pet Wash, espaço para banho e higiene de pets.
• Piscina aquecida.
• Hidromassagem aquecida com vista panorâmica.
• Sauna Úmida.
• Banheira de imersão para banho de gelo.
• Coliving com espaço gourmet.
• Alameda interna ao empreendimento com paisagismo.
• Grand Lobby com recepção monumental.
• Lobby Individual da Torre.


SAÚDE E BEM-ESTAR

• 42º Andar, correspondente ao 49º pavimento: Rooftop Wellness.
• Sala de Relaxamento.
• Academia de 200 m² com equipamentos de última geração e vista para a cidade.
• Piscina aquecida.
• Hidromassagem aquecida com vista panorâmica.
• Sauna Úmida.
• Banheira de imersão para banho de gelo.


SERVIÇOS E CONVENIÊNCIAS

• Mezanino e Serviços no 7º Pavimento.
• Amplo Coworking.
• Sala de Reunião privativa.
• Lavanderia compartilhada.
• Estrutura preparada para serviços de Concierge e check-in.
• Maleiro para hóspedes e moradores.
• Espaço para operação de Mini Market e sistema Grab and Go.
• Espaço para Restaurante privativo.
• Áreas administrativas e operacionais: gerência, refeitório, vestiários e descanso de funcionários.


SUSTENTABILIDADE

• Selo IPTU Verde - Categoria Ouro.
• Medidores individuais de água.
• Reaproveitamento de água de gotejamento de condensadoras de ar-condicionado.
• Sensores de presença para iluminação em parte das áreas comuns.
• Placas solares para geração de energia de parte das áreas comuns.
• Elevadores com sistema de regeneração de energia elétrica.
• Bacias sanitárias com redução de vazão.
• Louças e metais com economia de água.
• 2 vagas com carregadores para carros elétricos no estacionamento de visitantes.


SEGURANÇA E TECNOLOGIA

• Guarita com vidro blindado.
• Clausura para pedestres.
• Infraestrutura para portaria remota.
• Sistema de câmeras, CFTV, nas áreas comuns e elevadores.
• Infraestrutura seca de Wi-Fi para as áreas comuns sociais.
• Controle de acesso eletrônico para pessoas e veículos, com infraestrutura seca.
• Fechadura eletrônica na porta de acesso de todos os apartamentos.


PROJETO, CONCEITO E AUTORIA

• Arquitetura: Ricardo Farias.
• Design da Fachada: Daniel Arruda.
• Paisagismo: Benedito Abbud.
• Interiores: Zirpoli Arquitetura.
• Conceito: o projeto é o primeiro do Nordeste localizado dentro de um shopping.
• O empreendimento é alinhado a tendências mundiais como Brickell City Center, em Miami, e Cidade Jardim, em São Paulo.
• O projeto foca na rentabilidade para investidores, short stay, e na praticidade urbana extrema para moradores.


DISTRIBUIÇÃO E ESTRUTURA DO EMPREENDIMENTO

• 7º Pavimento: Mezanino e comodidades.
• 8º ao 34º Pavimento: Apartments, com studios e 1 quarto.
• 35º ao 48º Pavimento: Residences, com 2 quartos.
• 42º Andar, correspondente ao 49º pavimento: Rooftop Wellness.
• Lobby Individual da Torre.


DIFERENCIAIS DAS UNIDADES E PERSONALIZAÇÃO

• Esquadrias com tratamento acústico.
• Fechadura eletrônica na porta de acesso de todos os apartamentos.


DIFERENCIAIS DE MERCADO

• Conexão direta ao Shopping da Bahia por nova passarela exclusiva e acesso exclusivo ao estacionamento do Shopping da Bahia, Estacionamento F.
• Primeiro empreendimento do Nordeste localizado dentro de um shopping, alinhado a tendências mundiais como Brickell City Center e Cidade Jardim, com foco em short stay e praticidade urbana extrema.
• Lazer de 3.600 m² no 6º Pavimento, com piscina adulto com raia de 25 m, prainha, piscina infantil, quadra de Beach Tennis, restaurante privativo, salão de festas, brinquedoteca, Mini Market, Grab and Go, Pet Wash e coliving.
• Rooftop Wellness no 42º andar, correspondente ao 49º pavimento, com academia de 200 m², sala de relaxamento, piscina aquecida, hidromassagem aquecida, sauna úmida e banheira de imersão para banho de gelo.
• Selo IPTU Verde - Categoria Ouro, com medidores individuais de água, reaproveitamento de água de condensadoras, sensores de presença, placas solares, elevadores regenerativos, louças/metais economizadores, carregadores para carros elétricos, portaria remota, CFTV, Wi-Fi e fechadura eletrônica.
"""

SECTION_HEADERS = {
    "EXCLUSIVIDADE": "Exclusividade",
    "VAGAS E ACESSOS": "Vagas e Acessos",
    "ÁREAS COMUNS E LAZER": "Áreas Comuns e Lazer",
    "SAÚDE E BEM-ESTAR": "Saúde e Bem-Estar",
    "SERVIÇOS E CONVENIÊNCIAS": "Serviços e Conveniências",
    "BUSINESS E CORPORATIVO": "Business e Corporativo",
    "DISTRIBUIÇÃO E ESTRUTURA DO EMPREENDIMENTO": "Distribuição e Estrutura",
    "SUSTENTABILIDADE": "Sustentabilidade",
    "SEGURANÇA E TECNOLOGIA": "Segurança e Tecnologia",
    "PROJETO, CONCEITO E AUTORIA": "Projeto, Conceito e Autoria",
    "DIFERENCIAIS DAS UNIDADES E PERSONALIZAÇÃO": "Diferenciais das Unidades e Personalização",
    "DIFERENCIAIS DE MERCADO": "Diferenciais de Mercado",
}

def parse_entry(text: str) -> list:
    """Parse a single entry's text into a list of {heading, items}."""
    sections = []
    current = None
    for raw_line in text.split("\n"):
        line = raw_line.rstrip()
        if not line.strip():
            continue
        stripped = line.strip()
        if stripped == "DESCRIÇÃO":
            continue
        # Section header?
        if stripped in SECTION_HEADERS:
            if current and current["items"]:
                sections.append(current)
            current = {"heading": SECTION_HEADERS[stripped], "items": []}
        elif stripped.startswith("•"):
            if current is None:
                current = {"heading": "Detalhes", "items": []}
            current["items"].append(stripped.lstrip("•").strip())
        else:
            # continuation - append to last item
            if current and current["items"]:
                current["items"][-1] += " " + stripped
    if current and current["items"]:
        sections.append(current)
    return sections

# Split RAW by @@@ markers
parts = re.split(r'@@@\s*(\d+)', RAW)
# parts: ['', '1', text1, '2', text2, ...]
entries = {}
for i in range(1, len(parts), 2):
    num = int(parts[i])
    text = parts[i + 1]
    slug = SLUG_ORDER[num - 1]
    entries[slug] = parse_entry(text)
    print(f"#{num} {slug}: {len(entries[slug])} sections, {sum(len(s['items']) for s in entries[slug])} bullets")

# Update JSON
data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
for entry in data:
    if entry["slug"] in entries:
        entry["sections"] = entries[entry["slug"]]
JSON_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\n[DONE] Updated {JSON_PATH.name}")
