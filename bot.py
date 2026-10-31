"""Especialista: Portuguese Telegram consumer-education bot (aiogram 3)."""
import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F, Router
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    BotCommand, CallbackQuery, InlineKeyboardButton,
    InlineKeyboardMarkup, Message,
)
from dotenv import load_dotenv

from content import (
    BOT_NAME, BOT_USERNAME, CHECK_QUESTIONS, DESCRIPTION, SHORT_DESCRIPTION, TIPS, WELCOME,
)
from pricing import calculate_discount, format_eur, parse_eur

logger = logging.getLogger(__name__)
router = Router()


class Discount(StatesGroup):
    original = State()
    final = State()


class Checklist(StatesGroup):
    answering = State()


def menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Calcular desconto', callback_data='menu:discount')],
        [InlineKeyboardButton(text='Checklist da oferta', callback_data='menu:checklist')],
        [InlineKeyboardButton(text='Dicas de consumo', callback_data='menu:tips')],
    ])


def back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Voltar ao menu', callback_data='menu:home')],
    ])


def check_keyboard(step: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Sim', callback_data=f'check:{step}:yes'),
            InlineKeyboardButton(text='Não', callback_data=f'check:{step}:no'),
            InlineKeyboardButton(text='Não sei', callback_data=f'check:{step}:unknown'),
        ],
        [InlineKeyboardButton(text='Voltar ao menu', callback_data='menu:home')],
    ])


def tips_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Próxima dica', callback_data='tip:next')],
        [InlineKeyboardButton(text='Voltar ao menu', callback_data='menu:home')],
    ])


@router.message(CommandStart())
@router.message(Command('menu'))
async def start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(WELCOME, reply_markup=menu_keyboard())


@router.message(Command('ajuda', 'help'))
async def help_cmd(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        'O Especialista disponibiliza três funções:\n'
        '• Calcular desconto: introduz dois preços em euros.\n'
        '• Checklist da oferta: responde a quatro perguntas úteis.\n'
        '• Dicas de consumo: consulta informações educativas.\n\n'
        'Envia /menu para voltar ao início ou /cancelar para interromper uma operação.\n'
        'Não verificamos lojas nem disponibilizamos ofertas atuais.',
        reply_markup=menu_keyboard(),
    )


@router.message(Command('cancelar', 'cancel'))
async def cancel_cmd(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer('Operação cancelada. Seleciona outra opção.', reply_markup=menu_keyboard())


@router.callback_query(F.data == 'menu:home')
async def home_cb(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.answer()
    if callback.message:
        await callback.message.answer(WELCOME, reply_markup=menu_keyboard())


@router.callback_query(F.data == 'menu:discount')
async def discount_cb(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(Discount.original)
    await callback.answer()
    if callback.message:
        await callback.message.answer(
            'Calculadora de descontos\n\nQual é o preço original do produto?\n'
            'Exemplo: 79,90\n\nEnvia /cancelar para interromper.',
            reply_markup=back_keyboard(),
        )


@router.message(Discount.original)
async def original_price(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.answer('Introduz um preço em texto, por exemplo: 79,90.')
        return
    try:
        original = parse_eur(message.text)
    except ValueError:
        await message.answer('Preço inválido. Escreve um valor positivo, por exemplo: 79,90 ou 1.234,50.')
        return
    await state.update_data(original=str(original))
    await state.set_state(Discount.final)
    await message.answer(
        f'Preço original: {format_eur(original)}\n\n'
        'Qual é o preço promocional?\nExemplo: 59,90',
        reply_markup=back_keyboard(),
    )


@router.message(Discount.final)
async def final_price(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.answer('Introduz um preço em texto, por exemplo: 59,90.')
        return
    try:
        final = parse_eur(message.text)
        data = await state.get_data()
        original = parse_eur(data['original'])
        saved, percent = calculate_discount(original, final)
    except (ValueError, KeyError):
        await message.answer('Preço inválido. O valor deve ser positivo e não superior ao preço original.')
        return
    await state.clear()
    await message.answer(
        'Resultado do cálculo\n\n'
        f'Preço original: {format_eur(original)}\n'
        f'Preço promocional: {format_eur(final)}\n'
        f'Poupança: {format_eur(saved)}\n'
        f'Desconto: {str(percent).replace(".", ",")}%\n\n'
        'Cálculo baseado nos valores introduzidos. O bot não confirma preços de lojas.',
        reply_markup=menu_keyboard(),
    )


@router.callback_query(F.data == 'menu:checklist')
async def checklist_cb(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(Checklist.answering)
    await state.update_data(step=0, answers=[])
    await callback.answer()
    if callback.message:
        await callback.message.answer(
            f'Checklist da oferta (1/{len(CHECK_QUESTIONS)})\n\n{CHECK_QUESTIONS[0]}',
            reply_markup=check_keyboard(0),
        )


@router.callback_query(Checklist.answering, F.data.startswith('check:'))
async def checklist_answer(callback: CallbackQuery, state: FSMContext) -> None:
    try:
        _, raw_step, answer = (callback.data or '').split(':')
        requested_step = int(raw_step)
    except (ValueError, TypeError):
        await callback.answer('Resposta inválida.', show_alert=True)
        return
    if answer not in {'yes', 'no', 'unknown'}:
        await callback.answer('Resposta inválida.', show_alert=True)
        return
    data = await state.get_data()
    step = data.get('step', 0)
    if requested_step != step:
        await callback.answer('Esta pergunta já foi respondida.', show_alert=True)
        return
    answers = data.get('answers', []) + [answer]
    step += 1
    await callback.answer()
    if callback.message:
        await callback.message.edit_reply_markup(reply_markup=None)
    if step < len(CHECK_QUESTIONS):
        await state.update_data(step=step, answers=answers)
        if callback.message:
            await callback.message.answer(
                f'Checklist da oferta ({step + 1}/{len(CHECK_QUESTIONS)})\n\n{CHECK_QUESTIONS[step]}',
                reply_markup=check_keyboard(step),
            )
        return
    await state.clear()
    positives = answers.count('yes')
    if positives == len(CHECK_QUESTIONS):
        advice = 'Todos os pontos foram assinalados. Continua a ler as condições antes de comprar.'
    elif positives >= 2:
        advice = 'Há informações por confirmar. Revê os pontos marcados como Não ou Não sei.'
    else:
        advice = 'Existem vários pontos por esclarecer. Reúne mais informação antes de decidir.'
    if callback.message:
        await callback.message.answer(
            f'Checklist concluída: {positives} de {len(CHECK_QUESTIONS)} pontos confirmados.\n\n'
            f'{advice}\n\nEsta checklist é educativa e não certifica vendedores ou promoções.',
            reply_markup=menu_keyboard(),
        )


async def show_tip(message: Message, state: FSMContext, next_tip: bool = False) -> None:
    data = await state.get_data()
    idx = int(data.get('tip_idx', -1))
    idx = (idx + 1) % len(TIPS) if next_tip else 0
    await state.update_data(tip_idx=idx)
    title, body = TIPS[idx]
    await message.answer(
        f'Dica {idx + 1}/{len(TIPS)} — {title}\n\n{body}',
        reply_markup=tips_keyboard(),
    )


@router.callback_query(F.data == 'menu:tips')
async def tips_cb(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.answer()
    if callback.message:
        await show_tip(callback.message, state)


@router.callback_query(F.data == 'tip:next')
async def tips_next_cb(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    if callback.message:
        await show_tip(callback.message, state, next_tip=True)


@router.callback_query(F.data.startswith('check:'))
async def stale_check_cb(callback: CallbackQuery) -> None:
    await callback.answer('Esta sessão terminou. Abre uma nova checklist no menu.', show_alert=True)


@router.message()
async def fallback(message: Message) -> None:
    await message.answer('Escolhe uma das três ferramentas no menu.', reply_markup=menu_keyboard())


async def verify_bot_identity(bot: Bot) -> None:
    """Do not use a token belonging to a different public ad destination."""
    me = await bot.get_me()
    actual = me.username or ''
    if actual.casefold() != BOT_USERNAME.casefold():
        raise RuntimeError(
            f'BOT_TOKEN belongs to @{actual}, but this project expects '
            f'@{BOT_USERNAME}. Verify the bot in @BotFather and the ad URL.'
        )
    logger.info('Verified Telegram destination: @%s (id=%s)', actual, me.id)


async def configure_profile(bot: Bot) -> None:
    """Publish accurate, stable profile text; update only when it differs."""
    checks = (
        ('nome', bot.get_my_name, 'name', BOT_NAME, bot.set_my_name),
        ('descrição', bot.get_my_description, 'description', DESCRIPTION, bot.set_my_description),
        (
            'biografia', bot.get_my_short_description, 'short_description',
            SHORT_DESCRIPTION, bot.set_my_short_description,
        ),
    )
    for label, getter, key, expected, setter in checks:
        try:
            current = await getter()
            if getattr(current, key) != expected:
                await setter(**{key: expected})
                logger.info('Profile field updated for consistency: %s', label)
        except TelegramAPIError as exc:
            logger.warning('Não foi possível confirmar/atualizar %s: %s', label, exc)

    commands = [
        BotCommand(command='start', description='Iniciar o Especialista'),
        BotCommand(command='menu', description='Ver as três ferramentas'),
        BotCommand(command='ajuda', description='Como utilizar o bot'),
        BotCommand(command='cancelar', description='Cancelar a operação'),
    ]
    try:
        if await bot.get_my_commands() != commands:
            await bot.set_my_commands(commands=commands)
            logger.info('Bot commands updated for consistency')
    except TelegramAPIError as exc:
        logger.warning('Não foi possível confirmar/atualizar comandos: %s', exc)


async def main() -> None:
    load_dotenv()
    token = os.getenv('BOT_TOKEN', '').strip()
    if not token:
        raise RuntimeError('BOT_TOKEN em falta. Configura a variável de ambiente.')

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s: %(message)s')
    bot = Bot(token=token)
    dispatcher = Dispatcher()
    dispatcher.include_router(router)
    try:
        await verify_bot_identity(bot)
        await configure_profile(bot)
        await bot.delete_webhook(drop_pending_updates=False)
        logger.info('Especialista iniciado com polling. Usa apenas uma instância ativa.')
        await dispatcher.start_polling(bot, allowed_updates=dispatcher.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
