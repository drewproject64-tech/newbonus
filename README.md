# Especialista — @Bonus_Specialist_Bot

Bot educativo em português de Portugal. Três funções reais: cálculo de descontos, checklist interativa de ofertas e dicas de consumo. **Não tem ligação a lojas, não anuncia ofertas atuais e não oferece bónus.**

## Preparação

1. Abre o [@BotFather](https://t.me/BotFather) e confirma que controlas o bot **@Bonus_Specialist_Bot**.
2. Obtém um token com `/token` no BotFather. **Nunca partilhes o token publicamente nem o coloques no GitHub.**
3. Mantém a imagem de perfil atual, ou define outra imagem em `/setuserpic`.
4. O programa valida a identidade do bot pelo token via `getMe` e define descrições e comandos apenas quando estão diferentes dos textos estáveis do código. Se necessário, define-as também através de `/setabouttext` e `/setdescription` no BotFather.

## Iniciar localmente (Python 3.12)

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edita .env e atribui o BOT_TOKEN real
python bot.py
```

## Publicar no Render

1. Coloca estes ficheiros num repositório GitHub **privado ou público sem o ficheiro .env**.
2. No Render, cria um **Background Worker** com runtime Docker ou usa o `render.yaml` via Blueprint.
3. Define a variável de ambiente secreta `BOT_TOKEN` com o token fornecido pelo BotFather.
4. Mantém **uma única instância** do bot a executar polling. Não uses simultaneamente outro serviço de polling ou um webhook ativo.
5. Após a publicação, abre `https://t.me/Bonus_Specialist_Bot` e testa `/start`, cada botão, `/menu`, `/ajuda` e `/cancelar`.
6. Confirma se o nome **Especialista**, a bio e a imagem aparecem corretamente na página de perfil.

**Nota:** Render Background Worker é normalmente um serviço pago; confirma as condições e custos antes de implementar.

## Testes

```bash
python -m unittest discover -s tests -v
```

## Texto de anúncio proposto

**Título:** Especialista — Ferramentas de Compras

**Texto:** `No Especialista, calcula descontos com os preços que introduzes, consulta uma checklist de compra e lê dicas práticas de consumo.`

**Destino:** `https://t.me/Bonus_Specialist_Bot`

O texto descreve apenas funcionalidades existentes. Usa canais adequados em português e evita prometer prémios, ofertas atuais ou descontos garantidos.

## Privacidade e limitações

- Os preços introduzidos e as respostas à checklist são mantidos apenas na memória da sessão durante a execução; não são guardados numa base de dados.
- As sessões podem ser perdidas quando o processo reinicia.
- Não são solicitados dados bancários, dados pessoais, identificação ou acesso a contas de lojas.
- O bot não verifica vendedores, promoções ou preços em tempo real.
- Não existe uma promessa de aprovação de anúncios; o Telegram decide na revisão.

## Nota sobre a rejeição do anúncio

O código foi conferido contra o bot real em execução no Render: `@Bonus_Specialist_Bot`. A apresentação pública tem de refletir as três ferramentas disponíveis em permanência. Não troques conteúdos, perfis, comandos ou funções consoante visitas de revisão e utilizadores. A rejeição por 'Manipulation of content' é decidida pelo Telegram e estas correções não garantem aprovação. Revê a imagem e histórico do bot e pede esclarecimento/revisão ao suporte de Telegram Ads se a rejeição persistir.
