## Imports

import logging
import traceback

from telegram import Message, __version__ as TG_VER

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
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from SnL.Game import Game
from Validation.Validator import Validator

## Enable Logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


class Bot:

    __TOKEN = "5510418274:AAHsT0vGU74axHd7dCPVMTsx3TVySPIjtT8"
    
    def __init__(self) -> None:
       self.__GAME = Game()
       self.__gameStarted = False
       self.__imageUpdated = False
       self.__imageLink = None
       self.__VALIDATOR = Validator()
       self.__registering = False
       
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("Hello " + update.effective_user.first_name 
                + ", please register before usage if you are an OGL/GM, else /show to see the current board")
        
    async def register(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self.__registering:
            await update.message.reply_text("Currently Not Registering")
            return
        
        if len(context.args) < 3 or len(context.args) > 4:
            await update.message.reply_text("Invalid Argument Number")
            return
        
        uid = update.effective_user.id
        uname = update.effective_user.username
        
        if len(context.args) == 4 and context.args[1] == "OGL":       
            passphrase = context.args[0]
            house = context.args[2].lower()
            og = context.args[3]
            if og.isdigit():
                ogInt = int(og) - 1
                if self.__VALIDATOR.regOGL(passphrase, str(uid), uname, house, ogInt):
                    await update.message.reply_text("Successfully Registered as " + house + " " + og + " OGL")
                    return
        
        elif len(context.args) == 3 and context.args[1] == "GM":       
            passphrase = context.args[0]
            station = context.args[2]
            if station.isdigit():
                stationInt = int(station)
                if self.__VALIDATOR.regGM(passphrase, str(uid), uname, stationInt):
                    await update.message.reply_text("Successfully Registered as Station " + station + " GM")
                    return
                
        await update.message.reply_text("Invalid Credentials")  
        
    
    async def points(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not (ogl := self.__VALIDATOR.getOGL(str(update.effective_user.id))):
            await update.message.reply_text("Not A Registered OGL")
            return 
        house = ogl[0].lower()
        og = ogl[1]
        
        if True:
            await update.message.reply_text(house + " " + str(og + 1) + " Points: " + str(self.__GAME.getPoints(house, og)))
            
    
    async def addPoints(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self.__gameStarted:
            await update.message.reply_text("Game is Currently Paused")
            return
        
        if not self.__VALIDATOR.getGM(str(update.effective_user.id)):
            await update.message.reply_text("Invalid User")
            return

        if len(context.args) != 3:
            await update.message.reply_text("Invalid Argument Number")
            return
        house = context.args[0].lower()
        og = context.args[1]
        points = context.args[2]
        
        if not og.isdigit():
            await update.message.reply_text("Invalid OG")
            return
        og = int(og) - 1
        
        if not points.isdigit():
            await update.message.reply_text("Invalid Amount")
            return
        points = int(points)
        
        try:
            if self.__GAME.incrementPoints(house, og, points):
                await update.message.reply_text("Added " + str(points) + " Points to " +  house + " " + str(og + 1) 
                        + ", Total Points: " + str(self.__GAME.getPoints(house, og)))
                return
        except:
            traceback.print_exc()
        await update.message.reply_text("Invalid Addition")
            
        
    async def position(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not (ogl := self.__VALIDATOR.getOGL(str(update.effective_user.id))):
            await update.message.reply_text("Not A Registered OGL")
            return 
        house = ogl[0].lower()
        
        if True:
            await update.message.reply_text(house + " Current Position: " + str(self.__GAME.currPosition(house) + 1))

    
    async def roll(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self.__gameStarted:
            await update.message.reply_text("Game is Currently Paused")
            return

        if not (ogl := self.__VALIDATOR.getOGL(str(update.effective_user.id))):
            await update.message.reply_text("Not A Registered OGL")
            return 
        house = ogl[0].lower()
        og = ogl[1]
        
        msg: Message = await update.message.reply_dice()
        dice = msg.dice.value
        try:
            if self.__GAME.roll(house, og, dice):
                self.__imageUpdated = False
                await update.message.reply_text(house + " " + str(og + 1) + " Rolls, Your New Position: " + str(self.__GAME.currPosition(house) + 1)
                        + " Points: " + str(self.__GAME.getPoints(house, og)))
                return
        except:
            traceback.print_exc()
        await update.message.reply_text("Invalid Roll, check if you have enough points of if you are at the endpoint")        
            
    
    async def move(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self.__gameStarted:
            await update.message.reply_text("Game is Currently Paused")
            return
        
        if not (ogl := self.__VALIDATOR.getOGL(str(update.effective_user.id))):
            await update.message.reply_text("Not A Registered OGL")
            return 
        house = ogl[0].lower()
        og = ogl[1]
               
        try:
            if self.__GAME.move(house, og):
                self.__imageUpdated = False
                await update.message.reply_text(house + " " + str(og + 1) + " Moved, Your New Position: " + str(self.__GAME.currPosition(house) + 1)
                        + " Points: " + str(self.__GAME.getPoints(house, og)))
                return
                
        except:
            traceback.print_exc()
        await update.message.reply_text("Invalid Move, check if you have enough points of if you are at the endpoint")
    
    async def sabo(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self.__gameStarted:
            await update.message.reply_text("Game is Currently Paused")
            return
        
        if not (ogl := self.__VALIDATOR.getOGL(str(update.effective_user.id))):
            await update.message.reply_text("Not A Registered OGL")
            return 
        house = ogl[0].lower()
        og = ogl[1]
        
        if len(context.args) != 1:
            await update.message.reply_text("Invalid Argument Number")
            return
        target = context.args[0]
        
        if self.__GAME.sabo(house, target, og):
            self.__imageUpdated = False
            await update.message.reply_text(target + " Sabotaged to Position: " + str(self.__GAME.currPosition(target) + 1) + ", "
                    + " Your Remaining Points: " + str(self.__GAME.getPoints(house, og)))
        
        else:
            await update.message.reply_text("Invalid Sabotage, Check if you have enough points or if the target is at the start")
    
    async def show(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if self.__imageUpdated:
            await update.message.reply_photo(self.__imageLink)
                    
        else:
            msg : Message = await update.message.reply_photo(open("./renderedImg.png", "rb"))
            self.__imageLink = msg.photo[0].file_id
            self.__imageUpdated = True


    async def adminStartGame(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self.__VALIDATOR.isAdmin(str(update.effective_user.id)):
            await update.message.reply_text("Not A Registered Admin")
            return

        if self.__gameStarted:
            await update.message.reply_text("Game Already Started")
            return
        self.__gameStarted = True
        await update.message.reply_text("Starting Game")


    async def adminStopGame(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self.__VALIDATOR.isAdmin(str(update.effective_user.id)):
            await update.message.reply_text("Not A Registered Admin")
            return

        if not self.__gameStarted:
            await update.message.reply_text("Game Already Stopped")
            return
        self.__gameStarted = False
        await update.message.reply_text("Stopping Game")

    async def adminStartReg(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self.__VALIDATOR.isAdmin(str(update.effective_user.id)):
            await update.message.reply_text("Not A Registered Admin")
            return

        if self.__registering:
            await update.message.reply_text("Already Accepting Registrations")
            return
        self.__registering = True
        await update.message.reply_text("Starting Registrations")

    async def adminStopReg(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self.__VALIDATOR.isAdmin(str(update.effective_user.id)):
            await update.message.reply_text("Not A Registered Admin")
            return

        if not self.__registering:
            await update.message.reply_text("Already Not Accepting Registrations")
            return
        self.__registering = False
        await update.message.reply_text("Stopping Registrations")
    
    async def adminView(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self.__VALIDATOR.isAdmin(str(update.effective_user.id)):
            await update.message.reply_text("Not A Registered Admin")
            return

        if len(context.args) != 1:
            await update.message.reply_text("Invalid Argument Number")
            return
        house = context.args[0].lower()

        info: tuple = self.__GAME.adminView(house)
        await update.message.reply_text(house + " is at " + str(info[0] + 1) + " with OG Points " + str(info[1:]))


    async def adminSetPoints(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self.__VALIDATOR.isAdmin(str(update.effective_user.id)):
            await update.message.reply_text("Not A Registered Admin")
            return

        if len(context.args) != 3:
            await update.message.reply_text("Invalid Argument Number")
            return
        house = context.args[0].lower()
        og = context.args[1]
        points = context.args[2]

        if not og.isdigit():
            await update.message.reply_text("Invalid OG")
            return
        og = int(og) - 1

        if not points.isdigit():
            await update.message.reply_text("Invalid Points")
            return
        points = int(points)

        if self.__GAME.adminSetPoints(house, og, points):
            await update.message.reply_text(house + " " + str(og + 1) + " has been set to " + str(points) + " points")
            return

        await update.message.reply_text("Invalid Points Setting")


    async def adminSetPos(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self.__VALIDATOR.isAdmin(str(update.effective_user.id)):
            await update.message.reply_text("Not A Registered Admin")
            return

        if len(context.args) != 2:
            await update.message.reply_text("Invalid Argument Number")
            return
        house = context.args[0].lower()
        position = context.args[1]

        if not position.isdigit():
            await update.message.reply_text("Invalid Position")
            return
        position = int(position) - 1

        if self.__GAME.adminSetPos(house, position):
            self.__imageUpdated = False
            await update.message.reply_text(house + " has been set to " + str(position + 1) + " position")
            return

        await update.message.reply_text("Invalid Position Setting")

    def main(self) -> None:
       app = Application.builder().token(self.__TOKEN).build()
       app.add_handler(CommandHandler("start", self.start))
       app.add_handler(CommandHandler("register", self.register))
       app.add_handler(CommandHandler("points", self.points))
       app.add_handler(CommandHandler("addpoints", self.addPoints))
       app.add_handler(CommandHandler("position", self.position))
       app.add_handler(CommandHandler("roll", self.roll))
       app.add_handler(CommandHandler("move", self.move))
       app.add_handler(CommandHandler("sabo", self.sabo))
       app.add_handler(CommandHandler("show", self.show))
       app.add_handler(CommandHandler("adminview", self.adminView))
       app.add_handler(CommandHandler("adminsetpoints", self.adminSetPoints))
       app.add_handler(CommandHandler("adminsetpos", self.adminSetPos))
       app.add_handler(CommandHandler("adminstartgame", self.adminStartGame))
       app.add_handler(CommandHandler("adminstopgame", self.adminStopGame))
       app.add_handler(CommandHandler("adminstartreg", self.adminStartReg))
       app.add_handler(CommandHandler("adminstopreg", self.adminStopReg))
       
       app.run_polling()
  

if __name__ == "__main__":
  bot = Bot()
  bot.main()