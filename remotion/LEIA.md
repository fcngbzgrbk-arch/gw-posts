# Reels com Remotion (instalado em 11/11/2026)

Modelo "Obra entregue" em src/ObraReel.tsx (12 s, 1080x1920): foto 1 + título → números → as duas fotos + frase → fechamento com WhatsApp.

Uso:
1. `cd remotion && npm install`
2. Coloque as fotos em `public/obra/` (ou outro caminho dentro de public/).
3. Renderize trocando os textos por props:
   `npx remotion render src/index.ts ObraReel out/reel.mp4 --props='{"fotos":["obra/b.png","obra/a.png"],"selo":"OBRA ENTREGUE · RIO PRETO E REGIÃO","titulo":["LIGUE O AR SEM","MEDO DA CONTA"],"stats":[["11","placas de 620 W"],["825","kWh por mês"],["+R$ 700","de economia/mês"]],"frase":"E você, está esperando o quê?","whatsapp":"(17) 99671-7575"}'`
4. Confira os números com as regras de INSTRUCOES.md (75 kWh/placa, R$ 0,89/kWh).

O navegador usado é o Chromium já instalado (remotion.config.ts; variável REMOTION_CHROME para trocar).
Licença: grátis para empresas com até 3 funcionários; acima disso a Remotion exige licença de empresa (remotion.dev/license).
Música: o Reels sai sem música para o Maicon escolher um áudio em alta no app do Instagram.
