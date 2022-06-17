## Imports

import logging

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    InvalidCallbackData,
    PicklePersistence,
)

from Game import Game

## Enable Logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


class Bot:

    __TOKEN = "5510418274:AAHsT0vGU74axHd7dCPVMTsx3TVySPIjtT8"
    
    __GAME = None
    
    def __init__(self) -> None:
       self.__GAME = Game()
       
    def start(self):
       Application.builder().token(self.TOKEN).build()
  

if __name__ == "__main__":
  bot = Bot()
  bot.start