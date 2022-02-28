from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler, ConversationHandler
from functools import wraps
import telegram as tg
import logging
import serial
import json


ser = serial.Serial('COM4')
print(ser)

with open("settings.json", "r") as file:
    data = json.load(file)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def is_open():
    if not ser.isOpen():
        ser.open()
        print("Serial open")

def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in data['admins']:
            print(fr"Unauthorized access denied for {user_id}.")
            update.message.reply_markdown_v2(fr"Access denied for {update.effective_user.mention_markdown_v2()}\!")
            return
        return func(update, context, *args, **kwargs)
    return wrapped

def start(update: tg.Update, context: CallbackContext):
    is_open()
    
    user = update.effective_user
    id = update.effective_user.id
    print(fr'user: {id}')

    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=tg.ForceReply(selective=True),
    )

    reply_keyboard = [['/on', '/off', '/color', '/blink'], ['/disco', '/quit']]

    update.message.reply_text(
        'Choose an option:',
        reply_markup=tg.ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=False, input_field_placeholder='Option?'
        ),
    )

@restricted
def color(update: tg.Update, context: CallbackContext) -> None:
    inline_keyboard = [
        [
            tg.InlineKeyboardButton("Red", callback_data='Red'),
            tg.InlineKeyboardButton("Green", callback_data='Green'),
        ],
        [
            tg.InlineKeyboardButton("Blue", callback_data='Blue'),
            tg.InlineKeyboardButton("Yellow", callback_data='Yellow'),
            
        ],
        [
            tg.InlineKeyboardButton("Purple", callback_data='Purple'),
            tg.InlineKeyboardButton("Light Blue", callback_data='Light blue'),
        ]
    ]

    reply_markup = tg.InlineKeyboardMarkup(inline_keyboard)

    update.message.reply_text('Choose a color:', reply_markup=reply_markup)

def button(update: tg.Update, context: CallbackContext) -> None:
    query = update.callback_query

    query.answer()

    query.edit_message_text(text=f"{query.data} on")

    if query.data == "Red":
        red()
    elif query.data == "Green":
        green()
    elif query.data == "Blue":
        blue()
    elif query.data == "Purple":
        purple()
    elif query.data == "Yellow":
        yellow()
    elif query.data == "Light blue":
        light_blue()

def red() -> None:
    ser.write("red".encode())
    
def green() -> None:
    ser.write("green".encode())

def blue() -> None:
    ser.write("blue".encode())

def yellow() -> None:
    ser.write("yellow".encode())

def purple() -> None:
    ser.write("purple".encode())

def light_blue() -> None:
    ser.write("light blue".encode())

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
def quit(update: tg.Update, context: CallbackContext) -> None:
    ser.write("off".encode())
    ser.close()
    print("Serial closed")
    update.message.reply_text(
        fr"La seriale è stata chiusa\, per riaprirla usa il comando '\start'." "\n" "Ciao!"
    )


def main() -> None:
    update = Updater(data['TOKEN'], use_context=True)
    dispatcher = update.dispatcher

    dispatcher.add_handler(CommandHandler("start", start, Filters.user(user_id=data['admins'])))
    dispatcher.add_handler(CommandHandler("on", on))
    dispatcher.add_handler(CommandHandler("off", off))
    dispatcher.add_handler(CommandHandler("quit", quit))
    dispatcher.add_handler(CommandHandler("fastblink", fastblink))
    dispatcher.add_handler(CommandHandler("disco", disco))

    dispatcher.add_handler(CommandHandler("color", color))
    dispatcher.add_handler(CallbackQueryHandler(button))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    
    update.start_polling()

    update.idle()

if __name__ == "__main__":
    main()