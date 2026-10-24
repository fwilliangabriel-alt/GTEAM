# Revisão — foco em celular

Esta revisão atende às correções pedidas após a primeira entrega e substitui as decisões de abertura e apresentação comercial descritas no relatório inicial.

- Retrato de Willian: filtro de preto e branco removido; cores originais preservadas.
- Abertura: fotografia da aluna na praia escolhida pelo usuário, já presente nos materiais originais (`media-10.webp`). A foto vem antes do texto, em um quadro 1:1 com cantos retos, sem distorção e sem alteração física. Enquadramento mantém mãos, cabeça e região de quadris visíveis.
- Composição da abertura em uma coluna, com imagem visível desde o início no celular, texto mais enxuto e CTA com área de toque ampla. A orientação vertical permanece também nas telas grandes.
- Navegação mobile com alvos de pelo menos 44 px de altura.
- Planos reconstruídos em cards verticais: Premium escuro com texto claro, Básica e Planos Prontos claros. Hierarquia, contraste e organização inspirados no PDF oficial.
- Premium: seleção em quatro botões grandes, organizados em 2 × 2 no celular; recursos do ciclo selecionado imediatamente abaixo. Removidas repetições de benefícios do anual nas descrições dos ciclos menores. As condições aprovadas do PDF permanecem iguais.
- Links internos abrem na própria página; corrigido o CTA de acompanhamento que abria uma nova aba.

## Verificação

- Revisão visual de screenshots de abertura, Premium, Básica, Planos Prontos e retrato em 390 px.
- Testes específicos em 320, 375, 390 e 430 px confirmam: foto quadrada, sem cantos arredondados, fonte correta, retrato sem filtro, planos em coluna e ausência de overflow horizontal.
- Regressão em 320, 375, 390, 430, 768, 1024, 1440 e 1920 px: sem títulos excedendo contêiner, imagens quebradas ou erros de JavaScript.
- Filtros, deslize, ampliação, seletores, FAQ, privacidade, movimento reduzido e conteúdo essencial sem JavaScript revalidados.
- Todos os nove vídeos reproduzidos e pausados novamente. Teste de toque confirmou deslocamento horizontal da galeria.
- axe-core: zero violações automáticas detectadas nas regras WCAG 2 A/AA e 2.1 AA avaliadas em 390 e 1440 px; permanecem os limites de avaliação humana descritos no relatório original.
- Rede lenta em viewport mobile de 390 px: veja `mobile-revision.json` para a medição desta revisão. Nenhuma requisição MP4 inicial, título visível na primeira tela. Medição local simulada, não indicador de desempenho de produção.

Testes executados no Chromium com emulação mobile e toque. Não representam testes físicos em aparelhos iOS/Android. A página não foi publicada em hospedagem; o código e as evidências estão na branch de entrega. `main` permanece intacta.

## Imagens para revisão no GitHub

- [Abertura no celular](mobile-revision-hero.png)
- [Premium completo](mobile-revision-premium-full.png)
- [Básica](mobile-revision-basic.png)
- [Planos Prontos](mobile-revision-ready.png)
- [Retrato em cores](mobile-revision-founder.png)

As imagens antigas `preview-*` documentavam a primeira versão; use as capturas `mobile-revision-*` para a versão atual.
