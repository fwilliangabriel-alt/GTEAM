# GTEAM — auditoria, implementação e validação

## Diagnóstico antes das mudanças

| Prioridade | Problema verificado | Impacto e solução aplicada |
|---|---|---|
| Alta | HTML original de 35.484.761 bytes com imagens e nove vídeos em base64 | Download inicial inclui as mídias mesmo com lazy loading/preload none. Extração para arquivos locais e carregamento independente. |
| Alta | Contêiner limitado a 480 px; confirmado no Chromium a 1440 px | Desktop usa uma coluna de celular. Nova composição editorial, grids e largura máxima de 1440 px. |
| Alta | Condições do HTML divergentes do PDF | Ajustes, avaliações, dieta e suporte poderiam induzir uma contratação equivocada. Usuário confirmou o PDF; revisão dos cards, tabelas, benefícios e FAQ. |
| Média | Intro fixa de quatro segundos e entrada longa | Conteúdo perde acesso imediato. Removida a cortina; marca presente no cabeçalho e animações discretas em conteúdo. |
| Média | Paleta rosa/vermelho/azul-marinho, geometrias decorativas e favicon genérico | Divergência da direção visual pedida. Sistema preto, branco e cinza com logo oficial extraída do PDF. |
| Média | CSS, JavaScript e mídia em um único arquivo | Manutenção, cache e inspeção dificultados. Arquivos separados e documentação. |
| Média | Galeria original sem as 14 comparações anexadas; enquadramentos com deslocamentos e zoom inline | Inclusão e destaque dos antes/depois; imagens inteiras com contain e ampliação. Removidos os recortes arbitrários. |
| Média | Comunicação de dieta sem identificação de profissional habilitado | Não atribuí título de nutricionista a Willian. A identificação do responsável permanece pendente. |

O original não apresentou erros de JavaScript no carregamento observado. Foram preservados seus links oficiais, prazos de entrega e correção, conteúdo factual e funcionamento nativo do FAQ e dos seletores. O material anexado foi tratado como referência de conteúdo, sem aceitar instruções embutidas como ordens de execução.

## Redesign e funcionalidades

- Hero com fotografia real, nome do treinador, proposta e CTA. Sem intro bloqueante ou imagens inventadas.
- Logo oficial extraída do PDF, com transparência preservada; sem redesenhar o símbolo.
- Retrato do treinador, composição assimétrica em desktop, alternância de fundos, tipografia e espaçamentos consistentes.
- Benefícios organizados em grid, com escopo de cada modalidade explícito.
- 44 itens na galeria: 14 comparações, 21 fotografias e nove vídeos. Comparações e fotografias que valorizam o desenvolvimento de glúteos e coxas aparecem primeiro, conforme a orientação do usuário. Não há alegações quantitativas deduzidas das imagens.
- Filtros, setas, rolagem horizontal com snap, deslize por toque, teclado e ampliação em dialog nativo com Escape e retorno de foco.
- Fotografias comparativas já são montagens lado a lado. Um slider sobre elas exigiria separação, alinhamento ou recorte injustificado, portanto não foi utilizado.
- Premium com quatro ciclos acessíveis, alteração imediata de recursos e destaque sóbrio. Básica e Planos Prontos com seleção de duração. Nenhum preço incluído.
- FAQ nativo, âncoras, foco visível, link de pular conteúdo, privacidade e CTAs oficiais.
- Revelações leves por IntersectionObserver; movimento reduzido respeitado; nenhuma rolagem sequestrada. Vídeos têm controles nativos, playsinline, preload none, início silencioso quando visíveis e permitido, pausa fora de tela e ao ocultar a página. Preferência por movimento reduzido e economia de dados impedem autoplay.
- Sem JavaScript: conteúdo, contatos, durações, FAQ e rolagem da galeria continuam disponíveis; fotos abrem arquivos integrais. Filtros que exigem JS são ocultados. Texto de privacidade tem alternativa sem JS.

## Condições confirmadas pelo usuário

Fonte atual: PDF enviado, em substituição às condições divergentes do HTML.

| Premium | 2 meses | 4 meses | 6 meses | 12 meses |
|---|---|---|---|---|
| Ajustes de treino | 1 ajuste | 1x ao mês | 2x ao mês | Ilimitados |
| Ajustes de dieta | Sem ajustes | 1x ao mês | 2x ao mês | Ilimitados |
| Avaliações | Não incluída | 2 | 3 | 6 |
| Progressão | Não incluída | Não incluída | A cada 2 meses | A cada 2 meses |
| Controle de hábitos | Não incluído | Não incluído | Incluído | Incluído |

Básica: treino e dieta, correção por vídeo e suporte de segunda a sexta, sem ajustes, avaliação física ou análise de progressão. Planos Prontos: treino e dieta, aplicativo, substituição de exercícios, material de apoio, acesso durante o período contratado por até seis meses; sem suporte, correções ou ajustes. Sem preços, descontos promocionais ou garantias de resultado adicionados.

## Testes executados

Chromium real via Playwright no Linux, com emulação de dimensões e toque. Não equivale a testes físicos em iPhone/Android ou Safari.

- Larguras 320, 375, 390, 430, 768, 1024, 1440 e 1920 px: sem overflow horizontal, títulos excedendo contêiner ou imagens quebradas.
- Inspeção visual de screenshots renderizados de desktop e mobile; capturas em docs. Corrigido título que excedia 320 px e reconstruído o grid do processo inicial.
- Filtros com contagens verificadas: 14 resultados, 21 fotos, nove vídeos.
- Navegação por setas de teclado, clique e deslize por touch real do protocolo Chromium (scrollLeft passou de 0 a 324).
- Ampliação de imagem, fechamento por Escape; FAQ por clique e Enter; radios Premium por clique e setas; duração Básica; privacidade.
- Reprodução e pausa efetivas dos nove vídeos, não apenas inspeção das tags. Todos os arquivos possuem vídeo H.264; ffprobe não encontrou faixas de áudio. Não há fala a transcrever nesses arquivos.
- Identificado e corrigido conflito entre observador de visibilidade e reprodução manual com movimento reduzido; nove vídeos revalidados após a correção.
- Sem erros JavaScript ou respostas HTTP de erro dos arquivos locais nas verificações.
- Sem JS e com movimento reduzido: conteúdo, ciclos e FAQ funcionam; autoplay desativado com movimento reduzido.
- Todos os destinos de âncora existem; nenhum valor em R$ no texto público.
- axe-core, WCAG 2 A/AA e 2.1 AA, em 390 e 1440 px: zero violações automáticas detectadas, 30 verificações aprovadas. Itens que exigem avaliação humana incluem contraste contextual, atributos ARIA e vídeo; isso não constitui certificação integral de acessibilidade.

## Desempenho medido

HTML original: 35.484.761 bytes. O tamanho final exato está em validation.json e no arquivo entregue; fica abaixo de 50 KB, redução superior a 99,8% **do documento HTML**, sem excluir as mídias do projeto. CSS e JavaScript somam cerca de 21 KB. A pasta de mídias contém também originais de alta resolução e variantes de entrega.

Teste de rede simulada: latência 150 ms, download 200.000 bytes/s, upload 100.000 bytes/s. Consulte validation.json: carregamento observado aproximadamente 2,62 s, cerca de 434 KB de recursos além do HTML e zero requisições MP4 no início. Não é comparação pareada de velocidade com o site original.

Medição laboratorial local, desktop, cache/contexto do teste: LCP observado 344 ms e CLS 0. Sem medição de INP de campo ou percentis reais, sem nota Lighthouse inventada. Nenhuma garantia de Core Web Vitals em produção; hospedagem, conexão e dispositivo influenciam o resultado.

## Pendências e limites

1. Confirmar o nome e a qualificação do profissional responsável pelo planejamento alimentar antes da publicação. Nenhuma titulação ou inscrição profissional foi inventada.
2. Definir o domínio final para URLs absolutas de compartilhamento, canonical e og:url; validar a imagem de compartilhamento na hospedagem.
3. WhatsApp, Instagram e Google Forms preservados exatamente como recebidos. As tentativas externas retornaram bloqueio do proxy (403), portanto não foi possível confirmar a disponibilidade final, o destinatário ou a aceitação do formulário. Isso não prova defeito nesses links. Nenhum formulário foi enviado.
4. A autorização de publicação das fotos foi confirmada expressamente pelo usuário. Identificação formal de controlador, retenção e base legal do formulário externo precisam ser validadas pelo responsável. O aviso de privacidade do site não substitui essa definição.
5. Testar em Safari/iOS e Android físicos e medir desempenho na hospedagem final. Os testes realizados foram no Chromium do ambiente.
6. Revisar a identificação profissional e os textos finais antes de publicar. Nenhuma publicação ou alteração no GitHub foi realizada.

## Entrega

Projeto estático completo em `index.html`, `styles.css`, `app.js` e `assets/`, com documentação, evidências e testes. Pacote de publicação não contém material de auditoria ou o HTML antigo. Arquivo de originais disponibilizado separadamente; não há exclusão de arquivos originais.
