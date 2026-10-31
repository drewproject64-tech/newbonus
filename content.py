"""Portuguese (Portugal) text consistent with the bot's actual features."""

BOT_NAME = 'Especialista'
BOT_USERNAME = 'Bonus_Specialist_Bot'
SHORT_DESCRIPTION = (
    'Calcula descontos e consulta dicas para avaliar promoções em Portugal. Ferramentas informativas.'
)
DESCRIPTION = (
    'O Especialista é um bot informativo em português de Portugal. '
    'Permite calcular descontos em euros, utilizar uma checklist para analisar promoções '
    'e consultar dicas práticas de consumo. Não vende produtos, não apresenta '
    'ofertas em tempo real e não atribui prémios ou bónus.'
)
WELCOME = (
    'Bem-vindo ao Especialista!\n\n'
    'Explora três ferramentas úteis para compreender descontos e tomar decisões '
    'de compra mais informadas em Portugal.\n\n'
    'Escolhe uma opção abaixo. O bot é gratuito e não vende produtos, '
    'não atribui prémios nem apresenta promoções em tempo real.'
)

CHECK_QUESTIONS = [
    'É possível identificar claramente a loja ou o vendedor?',
    'O preço final, incluindo portes e outros custos, está indicado?',
    'As condições e as datas da promoção estão acessíveis?',
    'Comparaste o preço com alternativas antes de decidir?',
]

TIPS = [
    ('Preço de referência', 'Compara o preço atual com o preço habitual do produto. Um desconto anunciado não indica, por si só, que seja a opção mais económica.'),
    ('Custos totais', 'Antes de comprar, confirma os portes de envio e eventuais taxas. Compara sempre o custo total, não apenas o preço em destaque.'),
    ('Condições da promoção', 'Lê as condições: datas de validade, produtos incluídos, limites por pessoa e requisitos de utilização de códigos.'),
    ('Informação do vendedor', 'Confirma a identificação e os contactos da loja, os meios de pagamento disponíveis e as políticas de entrega e devolução.'),
    ('Compras por impulso', 'Uma contagem decrescente não substitui uma comparação. Verifica se o produto responde a uma necessidade real antes de decidir.'),
    ('Guardar informação', 'Conserva o comprovativo da compra e as condições comunicadas no momento da encomenda. Podem ser úteis em pedidos de assistência.'),
]
