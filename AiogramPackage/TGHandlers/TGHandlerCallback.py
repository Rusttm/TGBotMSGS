import datetime
import logging
import os

import aiofiles
from aiogram import types, Router, F, Bot, flags
from aiogram.filters import CommandStart, Command, or_f, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile
from aiogram.utils.callback_answer import CallbackAnswer, CallbackAnswerMiddleware
from aiogram.utils.markdown import hbold
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from aiogram.utils.formatting import as_list, as_marked_section, Bold

from AiogramPackage.TGFilters.BOTFilter import BOTFilterChatType, BOTFilterFinList
from AiogramPackage.TGAlchemy.TGDbQueriesProd import db_get_prod
from AiogramPackage.TGConnectors.TGMSConnector import TGMSConnector
from AiogramPackage.TGMiddleWares.TGMWCallbackData import TGMWCallbackData

callback_router = Router()
callback_router.message.filter(BOTFilterChatType(["private"]))
callback_router.callback_query.middleware(CallbackAnswerMiddleware(pre=True, text="🤔dont press", cache_time=10))

@callback_router.callback_query(F.data.startswith("get_prod_info_"), BOTFilterFinList())
async def get_prod_info(callback: types.CallbackQuery, session: AsyncSession):
    prod_id = callback.data[14:]
    prod_data = await db_get_prod(prod_id=prod_id, session=session)
    prod_description = prod_data.description
    # await callback.answer(f"Описание товара: {prod_description}", show_alert=True)
    await callback.message.answer(f"Описание товара: {prod_description}")
    await callback.answer()

@callback_router.callback_query(F.data.startswith("rep_fin_profit_"), BOTFilterFinList())
async def get_rep_fin_profit(callback: types.CallbackQuery):
    """ profit report """
    extra_data = callback.data[15:]
    try:
        res_str = await TGMSConnector().get_profit_rep_str_async()
    except Exception as e:
        res_str = f"Can't form daily profit report, Error:\n {e}"
        logging.warning(res_str)
    else:
        await callback.message.answer(res_str)
    await callback.answer()

@callback_router.callback_query(F.data.startswith("rep_fin_balance_"), BOTFilterFinList())
# @flags.callback_answer(pre=False, cache_time=60)
async def get_rep_bal(callback: types.CallbackQuery):
    extra_data = callback.data[16:]
    try:
        res_str = await TGMSConnector().get_bal_rep_str_async()
    except Exception as e:
        res_str = f"Can't form balance report, Error:\n {e}"
        logging.warning(res_str)
    else:
        await callback.message.answer(res_str)
    await callback.answer()
@callback_router.callback_query(F.data.startswith("rep_fin_debt_"), BOTFilterFinList())
async def get_rep_debt(callback: types.CallbackQuery):
    extra_data = callback.data[13:]
    try:
        res_str = await TGMSConnector().get_debt_rep_str_async()
    except Exception as e:
        res_str = f"Can't form debt report, Error:\n {e}"
        logging.warning(res_str)
    else:
        await callback.message.answer(res_str)
    await callback.answer()
@callback_router.callback_query(F.data.startswith("rep_fin_margin_"), BOTFilterFinList())
async def get_rep_margins(callback: types.CallbackQuery):
    extra_data = callback.data[15:]
    try:
        res_str = await TGMSConnector().get_margins_rep_str_async()
    except Exception as e:
        res_str = f"Can't form margins report, Error:\n {e}"
        logging.warning(res_str)
    else:
        await callback.message.answer(res_str)
    await callback.answer()

@callback_router.callback_query(F.data.startswith("rep_fin_account_"), BOTFilterFinList())
async def get_rep_account(callback: types.CallbackQuery):
    extra_data = callback.data[16:]
    try:
        res_str = await TGMSConnector().get_account_rep_str_async()
    except Exception as e:
        res_str = f"Can't form accounts report, Error:\n {e}"
        logging.warning(res_str)
    else:
        await callback.message.answer(res_str)
    await callback.answer()


@callback_router.callback_query(F.data.startswith("rep_fin_daily_"), BOTFilterFinList())
@flags.callback_answer(pre=False, cache_time=10)
async def get_rep_daily(callback: types.CallbackQuery, callback_answer: CallbackAnswer):
    extra_data = callback.data[16:]  # recieve chat_id
    today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    res_str = str(f"Отчет на {today}\n")
    try:
        res_str += await TGMSConnector().get_summary_rep_str_async()
    except Exception as e:
        res_str = f"Can't form accounts report, Error:\n {e}"
        logging.warning(res_str)
    else:
        await callback.message.answer(res_str)
    callback_answer.text = str(f"Отчет на {today}\n отправлен")
    await callback.answer()
