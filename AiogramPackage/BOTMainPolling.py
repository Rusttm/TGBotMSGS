# from https://docs.aiogram.dev/en/latest/
import asyncio
import aioschedule
import os
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.utils.callback_answer import CallbackAnswerMiddleware

from AiogramPackage.TGAlchemy.TGModelProd import create_table_async, drop_table_async, async_session
from AiogramPackage.TGConnectors.BOTMainClass import BOTMainClass
import logging

from AiogramPackage.TGHandlers.TGHandlerCallback import callback_router
from AiogramPackage.TGHandlers.TGHandlerUser import user_router
from AiogramPackage.TGHandlers.TGHandlerGroup import user_group_router
from AiogramPackage.TGHandlers.TGHandlerAdmin import admin_private_router
from AiogramPackage.TGHandlers.TGHandlerFin import fin_group_router
from AiogramPackage.TGCommon.TGBotCommandsList import private_commands
from AiogramPackage.TGMiddleWares.TGMWDatabase import DBMiddleware
# from AiogramPackage.TGConnectors.TGMSConnector import TGMSConnector

logging.basicConfig(level=logging.INFO)
logging.info("logging starts")
bot_class = BOTMainClass()
_config = bot_class.get_main_config_json_data_sync()
logger = bot_class.logger
logger.brand = f"{os.path.basename(__file__)}"
logger.info(f"logger {os.path.basename(__file__)} starts logging")

ALLOWED_UPDATES = ["message", "edited_message", "callback_query"]

bot = Bot(token=_config.get("bot_config").get("token"), parse_mode=ParseMode.HTML)
dp = Dispatcher()

# version1 work after filter middleware
# admin_group_router.message.middleware(CounterMiddleware())
# version2 update in outer middleware all events before filters
# dp.update.outer_middleware(CounterMiddleware())

#0 router
dp.include_router(callback_router)
#1 router
dp.include_router(admin_private_router)
#2 router
dp.include_router(fin_group_router)
#3 router
dp.include_router(user_router)
#4 router
dp.include_router(user_group_router)



bot.admins_list = [731370983]
bot.chat_group_admins_list = [731370983]
bot.fins_list = [731370983]
bot.restricted_words = ['idiot']
bot.filters_dict = dict()
async def on_startup(bot):
    print("bot runs")
    # run_param = False

    # if run_param:
    #     await drop_table_async()
    #
    # await create_table_async()
    asyncio.create_task(scheduler())

async def on_shutdown():
    print("Бот закрылся")

# from https://ru.stackoverflow.com/questions/1144849/%D0%9A%D0%B0%D0%BA-%D1%81%D0%BE%D0%B2%D0%BC%D0%B5%D1%81%D1%82%D0%B8%D1%82%D1%8C-%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D1%83-aiogram-%D0%B8-schedule-%D0%BD%D0%B0-%D0%A2elegram-bot
async def scheduler():
    aioschedule.every().day.at("17:00").do(scheduller_sends)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def scheduller_sends():
    from AiogramPackage.TGConnectors.TGMSConnector import TGMSConnector
    connector = TGMSConnector()
    prepare_rep_string = await connector.get_summary_rep_str_async()
    # admins_list = bot.admins_list
    fins_list = bot.fins_list
    for fin_id in fins_list:
        await bot.send_message(chat_id=fin_id, text="Время ежедневного отчета")
        await bot.send_message(chat_id=fin_id, text=prepare_rep_string)
    print("It's noon!")

async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    # version3
    dp.update.middleware(DBMiddleware(session_pool=async_session))
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private_commands, scope=types.BotCommandScopeAllPrivateChats())
    # version1 wuth list of updates
    # await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)
    # version2 with all uodates
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    logger.info(f"logger {os.path.basename(__file__)} starts logging")


if __name__ == '__main__':
    asyncio.run(main())
