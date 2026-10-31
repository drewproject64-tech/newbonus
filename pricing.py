"""Pure, testable EUR discount calculations for the Especialista bot."""
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import re

CENT = Decimal('0.01')
MAX_PRICE = Decimal('100000000.00')


def parse_eur(text: str) -> Decimal:
    """Parse Portuguese prices: 19,99; 19.99; 1.234,50; 1234."""
    raw = text.strip().replace('€', '').replace('\u00a0', '').replace(' ', '')
    if re.fullmatch(r'\d{1,9}(?:[.,]\d{1,2})?', raw):
        normal = raw.replace(',', '.')
    elif re.fullmatch(r'\d{1,3}(?:\.\d{3})+(?:,\d{1,2})?', raw):
        normal = raw.replace('.', '').replace(',', '.')
    elif re.fullmatch(r'\d{1,3}(?:,\d{3})+(?:\.\d{1,2})?', raw):
        normal = raw.replace(',', '')
    else:
        raise ValueError('Formato de preço inválido.')
    try:
        amount = Decimal(normal)
    except InvalidOperation as exc:
        raise ValueError('Formato de preço inválido.') from exc
    if not (Decimal('0.00') < amount <= MAX_PRICE):
        raise ValueError('O preço deve ser superior a zero e dentro do limite permitido.')
    return amount.quantize(CENT)


def format_eur(amount: Decimal) -> str:
    result = f'{amount.quantize(CENT, rounding=ROUND_HALF_UP):,.2f}'
    return result.replace(',', '@').replace('.', ',').replace('@', '.') + ' €'


def calculate_discount(original: Decimal, final: Decimal) -> tuple[Decimal, Decimal]:
    if original <= 0 or final <= 0 or final > original:
        raise ValueError('O preço promocional deve ser positivo e não superior ao preço original.')
    saved = (original - final).quantize(CENT, rounding=ROUND_HALF_UP)
    percent = (saved * 100 / original).quantize(CENT, rounding=ROUND_HALF_UP)
    return saved, percent
