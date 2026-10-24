# GTEAM — site da consultoria

A versão atual prioriza o celular: foto de abertura quadrada, retrato do fundador em cores e cards verticais de planos inspirados no PDF. Confira [a revisão mobile e as capturas atualizadas](docs/REVISAO-MOBILE.md).

Projeto estático: HTML, CSS, JavaScript e mídias locais. Não exige Node, framework, build, conta externa ou instalação de dependências para funcionar.

## Executar

Na pasta do projeto, execute:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Abra o servidor pelo seu navegador no seu computador. Para publicação, envie `index.html`, `styles.css`, `app.js` e a pasta `assets/` para uma hospedagem estática com HTTPS. Preserve a estrutura das pastas. Os testes usam HTTP; abrir com duplo clique não substitui a validação no servidor.

**Não publique `originals/`, `docs/` ou `tests/`.** Esses diretórios contêm materiais de referência, documentação e validação, não são necessários ao site publicado. Os originais foram preservados separadamente no pacote de arquivo, sem alteração de corpos, rostos ou composição das comparações.

## Conteúdo e condições

Condições do PDF “GTEAM — Seu guia da consultoria”, confirmado pelo usuário como fonte atual. Sem preços publicados. A autorização de utilização pública das fotos foi confirmada pelo usuário nesta conversa. Confira `docs/RELATORIO.md` para pendências e limites de validação.

A logo foi extraída do PDF oficial com sua máscara de transparência. A variante de exibição escura usa CSS, preservando a geometria. As fotos originais extraídas do HTML permanecem em `assets/media-*.webp`; as variantes `-640` e `-1000` são redimensionamentos conservadores para entrega. Os arquivos de antes/depois são cópias integrais, sem recortes. Os vídeos H.264 foram preservados sem reencodificação.

## Manutenção

- `index.html`: textos, serviços, durações, comparações e metadados.
- `styles.css`: sistema visual, grids, breakpoints, estados e movimento reduzido.
- `app.js`: filtros, navegação da galeria, ampliação, privacidade e reprodução visível dos vídeos.
- `assets/`: logo, imagens responsivas, comparações, pôsteres e vídeos.
- Os seletores Premium usam radios nativos e CSS; FAQ usa `details/summary`. Funcionam sem JavaScript. Sem JS, as fotos abrem seus arquivos e a galeria continua navegável por deslize/rolagem; os filtros são ocultados.
- Atualize `og:image` para uma URL HTTPS absoluta e adicione canonical/og:url quando o domínio final for definido. Configure cache e suporte a HTTP Range de vídeos na hospedagem. HTML deve revalidar; use cache com revalidação nos assets enquanto os nomes não tiverem hash.

## Testes de desenvolvimento

Requer Python com Playwright e Chromium. Com o servidor acima ativo, execute `python3 tests/validate.py` e `python3 tests/validate_extra.py`. Os scripts usam a pasta do projeto como raiz; devem ser executados nesta estrutura. A validação axe-core e as medições efetivamente executadas estão documentadas em `docs/`.

A aplicação não contém trackers, banco de dados, cookies de marketing ou dependências remotas. Os serviços de contato e anamnese são externos.
