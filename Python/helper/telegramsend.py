import telegram
import telegram.constants
import helper.config
import logging
import asyncio

def send(text):
    asyncio.run(send2(text))


async def send2(text):
    conf = helper.config.initconfig()

    async with telegram.Bot(token=conf['telegramtoken']) as bot:
        try:
            await bot.send_message(conf['telegramid'], text=text, parse_mode=telegram.constants.ParseMode.HTML)
        except Exception as e:
            logging.error("Fehler beim senden des Telegram-Nachrichten: " + str(e))
            print("Fehler beim senden des Telegram-Nachrichten: " + str(e))
