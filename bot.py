from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from functools import wraps
import telegram as tg
import logging
import serial
import json


ser = serial.Serial('COM4')

with open("RGBarduino\settings.json", "r") as file:
    data = json.load(file)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in data['admins']:
            print("Unauthorized access denied for {}.".format(user_id))
            return
        return func(update, context, *args, **kwargs)
    return wrapped

def start(update: tg.Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    id = update.effective_user.id
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=tg.ForceReply(selective=True),
    )

    if id not in data['admins']:
        update.message.reply_markdown_v2("Non sei autorizzato\, scimmia!")

@restricted  
def on(update: tg.Update, context: CallbackContext) -> None:
    update.message.reply_markdown_v2(
        fr"led acceso🔆"
    )
    ser.write("on".encode())

@restricted
def echo(update: tg.Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)

@restricted
def off(update: tg.Update, context: CallbackContext) -> None:
    update.message.reply_markdown_v2(
        fr"led spento❌"
    )
    ser.write("off".encode())

@restricted
def fastblink(update: tg.Update, context: CallbackContext) -> None:
    update.message.reply_markdown_v2(
        fr"fast blink👀"
    )
    ser.write("fastblink".encode())

@restricted
def disco(update: tg.Update, context: CallbackContext) -> None:
    update.message.reply_markdown_v2(
        fr"DISCO MODE\!✨"
    )
    ser.write("disco".encode())

@restricted
def done(update: tg.Update, context: CallbackContext) -> None:
    ser.close()
    print("Serial closed")

def main() -> None:
    update = Updater(data['TOKEN'], use_context=True)
    dispatcher = update.dispatcher

    dispatcher.add_handler(CommandHandler("start", start, Filters.user(user_id=data['admins'])))
    dispatcher.add_handler(CommandHandler("on", on))
    dispatcher.add_handler(CommandHandler("off", off))
    dispatcher.add_handler(CommandHandler("done", done))
    dispatcher.add_handler(CommandHandler("fastblink", fastblink))
    dispatcher.add_handler(CommandHandler("disco", disco))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    
    update.start_polling()

    update.idle()

if __name__ == "__main__":
    main()