# Especialista — @bonusespecialistabot

Bot educativo em português de Portugal. Três funções reais: cálculo de descontos, checklist interativa de ofertas e dicas de consumo. **Não tem ligação a lojas, não anuncia ofertas atuais e não oferece bónus.**

## Preparação

1. Abre o [@BotFather](https://t.me/BotFather) e confirma que controlas o bot **@bonusespecialistabot**.
2. Obtém um token com \`/token\` no BotFather. **Nunca partilhes o token publicamente nem o coloques no GitHub.**
3. Mantém a imagem de perfil atual, ou define outra imagem em \`/setuserpic\`.
4. As descrições do perfil e comandos são configurados automaticamente pelo programa quando arranca. Se necessário, define-as também através de \`/setabouttext\` e \`/setdescription\` no BotFather.

## Iniciar localmente (Python 3.12)

\`\`\`bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edita .env e atribui o BOT_TOKEN real
python bot.py
\`\`\`

## Publicar no Render

1. Coloca estes ficheiros num repositório GitHub **privado ou público sem o ficheiro .env**.
2. No Render, cria um **Background Worker** com runtime Docker ou usa o \`render.yaml\` via Blueprint.
3. Define a variável de ambiente secreta \`BOT_TOKEN\` com o token fornecido pelo BotFather.
4. Mantém **uma única instância** do bot a executar polling. Não uses simultaneamente outro serviço de polling ou um webhook ativo.
5. Após a publicação, abre \`https://t.me/bonusespecialistabot\` e testa \`/start\`, cada botão, \`/menu\`, \`/ajuda\` e \`/cancelar\`.
6. Confirma se o nome **Especialista**, a bio e a imagem aparecem corretamente na página de perfil.

**Nota:** Render Background Worker é normalmente um serviço pago; confirma as condições e custos antes de implementar.

## Testes

\`\`\`bash
python -m unittest discover -s tests -v
\`\`\`

## Texto de anúncio proposto

**Título:** Especialista — Ferramentas de Compras

**Texto:** \`Calcula descontos em euros, consulta uma checklist de promoções e lê dicas de consumo em português no bot Especialista.\`

**Destino:** \`https://t.me/bonusespecialistabot\`

O texto descreve apenas funcionalidades existentes. Usa canais adequados em português e evita prometer prémios, ofertas atuais ou descontos garantidos.

## Privacidade e limitações

- Os preços introduzidos e as respostas à checklist são mantidos apenas na memória da sessão durante a execução; não são guardados numa base de dados.
- As sessões podem ser perdidas quando o processo reinicia.
- Não são solicitados dados bancários, dados pessoais, identificação ou acesso a contas de lojas.
- O bot não verifica vendedores, promoções ou preços em tempo real.
- Não existe uma promessa de aprovação de anúncios; o Telegram decide na revisão.
