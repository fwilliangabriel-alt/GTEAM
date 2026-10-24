# Abrir a cópia de revisão no celular

A captura enviada pelo usuário mostrava o HTML sem CSS e imagens: links azuis, ícone SVG enorme e imagens ausentes. Isso é compatível com abrir o `index.html` isolado no visualizador de arquivos, sem acesso aos arquivos irmãos do projeto. Não é a aparência renderizada com os recursos completos.

## Arquivo para revisão

Baixe **ABRIR-NO-CELULAR.html** pela opção de download do GitHub. Ele contém os estilos, scripts, fotografias e vídeos no próprio documento. Não precisa das pastas `assets/`, de `styles.css` ou de `app.js` para apresentar o conteúdo.

Esse documento tem aproximadamente 47,2 MB, pois incorpora todas as mídias. É uma cópia autônoma de revisão, não a versão otimizada para hospedagem. Faça o download completo antes de abrir.

No iPhone, o aplicativo Arquivos pode usar o Quick Look, que tem limitações próprias para JavaScript e vídeos. A apresentação, as fotos, o FAQ e a seleção dos ciclos não dependem de JavaScript. Para a experiência completa com filtros, galeria e vídeos, utilize a versão hospedada em um navegador. Não foi realizado teste físico no Quick Look/iOS, portanto não há garantia de suas políticas específicas de pré-visualização.

## Versão de publicação

O `index.html` original, `styles.css`, `app.js` e `assets/` continuam separados para publicação e cache eficiente. Devem ser enviados juntos à hospedagem. Não abra apenas esse `index.html` isolado para avaliar o resultado no visualizador de arquivos.

## Validação realizada

- O navegador gerenciado bloqueou navegação `file://`; isso não foi contornado.
- Para testar isolamento, o HTML foi copiado sozinho para uma pasta temporária e servido por HTTP. Todos os pedidos de recursos adicionais foram bloqueados; após o carregamento do único documento, o contexto foi colocado offline.
- Em viewport mobile de 390 × 844, com e sem JavaScript: estilos aplicados, imagem de abertura carregada e quadrada, sem overflow horizontal.
- Sem dependências externas de CSS, JavaScript, imagens ou vídeos; uma única requisição observada, do documento HTML.
- FAQ e ciclos Premium funcionam sem JavaScript.
- Com JavaScript: filtros, ampliação e reprodução/pausa de um vídeo incorporado verificados com contexto offline.
- Nenhum erro de JavaScript observado. Evidências: `portable-validation.json` e capturas `portable-mobile-*.png`.

Para regenerar o arquivo autônomo após alterações: `python3 tools/build_portable.py`. Esse gerador usa somente a biblioteca padrão do Python. Execute `python3 tests/validate_portable.py` para repetir a validação; ele usa Playwright/Chromium e requer um servidor na porta 8003 apontando para `/tmp/gteam-single-file`, conforme o diretório temporário criado pelo teste.
