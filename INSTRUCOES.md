# Rotina diária de posts – GW Fotovoltaica (Green World Energia Solar)

Este repositório é a base da rotina automática de posts do Instagram @gwfotovoltaica e da página do Facebook
"GW Fotovoltaica - Energia Solar Rio Preto". Dono: Maicon Silva. Ele só aprova as artes; o Claude monta e publica.

## Visão geral do dia
1. **Manhã (tarefa agendada):** escolher o tema do dia → escolher a foto → gerar arte (feed + stories) → escrever legenda → subir para `posts/AAAA-MM-DD/` → mandar para o Maicon aprovar.
2. **Aprovação:** o Maicon responde na mesma conversa ("ok", ou pede ajustes). Sem "ok" explícito, NADA é publicado.
3. **Publicação:** depois do "ok", agendar com `send_later` uma mensagem para esta mesma conversa no horário do dia (ver tabela). Quando ela chegar, publicar via Windsor.ai e registrar.

## Passo 0 – checar se o dia já está coberto
Ler `posts.json`. Se já existe entrada com a data de hoje (qualquer status diferente de `rejeitado`), não fazer nada e encerrar avisando em uma linha.

## Passo 1 – tema do dia (calendário)
| Dia | Modelo (selo) | Pilar | Público | Horário |
|---|---|---|---|---|
| Seg | OBRA REAL | Obras/cases | Não tem solar | 20:00 |
| Ter | MITO OU VERDADE? | Quebra de objeção | Não tem solar | 20:00 |
| Qua | JÁ TEM SOLAR? | Manutenção | Já tem solar | 20:00 |
| Qui | OBRA REAL | Obras/cases | Não tem solar | 20:00 |
| Sex | PARCELA × CONTA | Oferta/financiamento | Não tem solar | 12:00 |
| Sáb | JÁ TEM SOLAR? | Ampliação/bateria/monitoramento | Já tem solar | 20:00 |
| Dom | BASTIDORES | Confiança | Os dois | 20:00 |

Horários vêm dos "Horários ativos" do Meta Business Suite (IG ativo 19h–20h, FB 21h–22h). Fuso: America/Sao_Paulo.
Escolher a pauta em `pautas.md` que ainda não foi usada (ver `posts.json`). Pode criar pautas novas no mesmo espírito.

## Passo 2 – foto
`fotos.json` lista as fotos de `fotos/`. Usar só `status: disponivel` e `tipo: instalacao` (as `antes_sem_placas` servem só para posts de "antes e depois" ou bastidores).
- OBRA REAL: preferir foto com `placas` preenchido (os números aparecem na arte). Se não houver, usar foto de drone bonita e trocar os números por um texto (`sub`), sem inventar quantidade de placas.
- Não repetir a mesma `obra` dois dias seguidos. Olhar a foto antes de usar (abrir a imagem) e conferir: placas visíveis, sem pessoas identificáveis, sem placa de carro legível, sem marca de equipamento.
- Depois de publicar, marcar `status: usada` e `uso: AAAA-MM-DD`.

## Passo 3 – arte
`python3 arte.py spec.json posts/AAAA-MM-DD/arte` gera `arte_feed.jpg` (1080x1350) e `arte_story.jpg` (1080x1920).
Visual = padrão aprovado no Claude Design em 09/10 (foto no topo, painel escuro arredondado, selo, logo, caixas de números, botão verde). Campos do spec: foto, selo, kicker, titulo, destaque, sub, stats ou placas, cta, tsize, fy, acento. Ferramenta de criação: Claude Design (o Maicon não usa mais Canva); Reels são editados pelo Claude a partir dos vídeos que ele mandar.
Campos do spec: `foto` (ex. `fotos/097.jpg`), `fy` (0–1, enquadramento vertical), `selo`, `kicker`, `titulo`, `destaque` (trecho do título em amarelo), `tsize` (padrão 74; reduzir se o título for longo), e **um** dos dois: `placas` (calcula kWh e R$ sozinho) ou `sub` (texto de apoio).
Abrir as duas imagens geradas e conferir: texto legível, nada cortado, logo visível. Ajustar `fy`/`tsize` se precisar.

## Regras fixas (do Maicon)
- Economia prometida: "média de 80%" na conta (nunca "até 95%").
- Geração: SEMPRE 75 kWh/mês por placa. Tarifa CPFL: R$ 0,89/kWh. Economia = placas × 75 × 0,89 (o arte.py já faz).
- WhatsApp: (17) 99671-7575 (nunca o antigo 3363-5028). Rio Preto e região. 7 anos de mercado.
- NUNCA citar marca de equipamento (painel, inversor, microinversor, bateria).
- NUNCA citar nome de cliente nem endereço.
- Não inventar números (percentuais de perda, preços, prazos de payback) sem fonte; preferir afirmações gerais e verdadeiras.
- Preços e parcelas: usar SOMENTE `financiamento.json` (tabela da Sol + simulação de 09/10). Nos posts, mostrar a menor parcela (96x) ou 84x, sempre com "a partir de" e "taxa de 1,95% a.m. mediante simulação e aprovação de crédito" (na arte, um asterisco; na legenda, a frase completa). Kits da campanha (8, 12 e 16 placas, com microinversor) têm prioridade nos posts de oferta. Comparar a parcela com o valor da energia gerada (`energia_gerada_vale_R$_mes`), sem prometer conta zerada (sempre sobra a taxa mínima da CPFL).

## Passo 4 – legenda
Tom próximo, regional, direto. Estrutura: gancho na 1ª linha (com 1 emoji) → 2–3 frases de valor → CTA com WhatsApp (17) 99671-7575 → 4–6 hashtags (#energiasolar #riopreto #sjriopreto + específicas + #gwfotovoltaica). Máx. ~600 caracteres. Salvar em `posts/AAAA-MM-DD/legenda.txt`.

## Passo 5 – subir e pedir aprovação
`git add`, commit e push. Os arquivos ficam públicos em
`https://raw.githubusercontent.com/fcngbzgrbk-arch/gw-posts/main/posts/AAAA-MM-DD/arte_feed.jpg` (idem `arte_story.jpg`).
Registrar em `posts.json` com status `aguardando_aprovacao`.
Mandar ao Maicon (SendUserFile com as 2 imagens + SendUserMessage com a legenda) e perguntar: "Aprova para hoje às HH:MM? Responda ok ou diga o que mudar."

## Passo 6 – após o "ok"
Agendar `send_later` (initiation `human_request`) para o horário do dia com a mensagem
"PUBLICAR post AAAA-MM-DD agora (aprovado pelo Maicon)". Atualizar `posts.json` → `aprovado`. Push.
Se o "ok" chegar depois do horário, publicar na hora.

## Passo 7 – publicar (quando a mensagem agendada chegar)
Windsor.ai `execute_action`:
1. connector `instagram`, account `17841428432441084`, action `create_image_post`, params `{image_url: <arte_feed raw URL>, caption: <legenda>}`
2. connector `instagram`, mesma conta, action `create_story`, params `{image_url: <arte_story raw URL>}`
3. connector `facebook_organic`, action `create_photo_post`, params `{image_url: <arte_feed raw URL>, caption: <legenda>}` — publicar nas DUAS páginas (decisão do Maicon em 09/10, até ele escolher a oficial):
   - account `110901733778456` ("GW Fotovoltáica", facebook.com/gwfotovoltaica, página antiga com o público)
   - account `430641700123072` ("GW Fotovoltaica - Energia Solar Rio Preto", ligada ao Instagram)
Registrar os IDs retornados em `posts.json` (status `publicado`), marcar a foto como usada em `fotos.json`, push, e avisar o Maicon em uma linha. Se alguma ação falhar, avisar qual e por quê; não repetir uma ação que já deu certo.
