# RGB Arduino Project <img src="https://brandslogos.com/wp-content/uploads/images/large/arduino-logo-1.png" alt="Arduino Logo" width="50" height="50" style="vertical-align:top">
*Progetto realizzato da [Andrea Bellu](https://github.com/andrebellu), [Stefano Longhena](https://github.com/StefanoLonghena), [Leonardo Baccalario](https://github.com/LeonardoBaccalario).*

Il progetto consisteva nel realizzare un circuito con un led RGB utilizzabile tramite un telecomando. Abbiamo poi realizzato un bot di telegram interfacciato con arduino tramite python e la sua libreria pyserial.

#### Componenti utilizzati
- [Elegoo Mega2560](https://www.amazon.it/Elegoo-ATmega2560-ATMEGA16U2-Compatibile-Arduino/dp/B071W7WP35)
- RGB led
- 3x Resistenze 220Ω
- LCD1602 Module
- Potentiometer 10kΩ
- IR Receiver Module
- Remote Control
- Cavi
---
#### Librerie utilizzate
- C++ <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/ISO_C%2B%2B_Logo.svg/306px-ISO_C%2B%2B_Logo.svg.png" alt="Arduino Logo" width="25" height="30" style="vertical-align:middle">:
	- [IRremote.h](https://www.arduino.cc/reference/en/libraries/irremote/)
	- [LiquidCrystal.h](https://www.arduino.cc/en/Reference/LiquidCrystal)
	- [time.h](https://it.wikipedia.org/wiki/Time.h)
- Python <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1200px-Python-logo-notext.svg.png" alt="Arduino Logo" width="20" height="20" style="vertical-align:middle">:
	- [telegram e telegram.ext](https://python-telegram-bot.readthedocs.io/en/stable/)
	- [functools](https://docs.python.org/3/library/functools.html)
	- [logging](https://docs.python.org/3/library/logging.html)
	- [pyserial](https://pythonhosted.org/pyserial/)
	- [json](https://docs.python.org/3/library/json.html)
---
#### Interfacciare arduino con python
Utilizzando la libreria PySerial possiamo semplicemente mettere in "collegamento" arduino e python mediante una sola riga di codice: 
```py
ser = serial.Serial('nome porta')
```
Per passare dei comandi da python e arduino basterà eseguire: 
```py
ser.write("nome comando".encode())
``` 
che verrà letto da arduino utilizzando la funzione:
```cpp
Serial.readStringUntil('\n');
```  
---
#### Bot Telegram
Esempio del funzionamento del bot:
```py
#main
def main() -> None:
	update = Updater(data['TOKEN'], use_context=True)
	dispatcher = update.dispatcher

	dispatcher.add_handler(CommandHandler("disco", disco))
```
L'**Updater** è l'elemento che ci permette di interfacciarci direttamente col bot, mentre il **dispatcher** fa da "controllore". In questo snippet di codice vediamo come, nel caso ricevessimo dall'utente su telegram il comando '**\disco**', verrebbe chiamata la funzione **disco**.
```py
#funzione disco
@restricted
def disco(update: tg.Update, context: CallbackContext) -> None:
	update.message.reply_markdown_v2(
		fr"DISCO MODE\!✨"

	)

	ser.write("disco".encode())
```
Quando la funzione **disco** viene chiamata il bot manda semplicemente un messaggio di feedback e la funzione manda la keyword ad arduino.
> *@restricted* perchè le funzioni, e di conseguenza il bot, sono utilizzabili solo dagli utenti autorizzati. 
> ```py
> def restricted(func):
>     @wraps(func)
>     def wrapped(update, context, *args, **kwargs):
 >          user_id = update.effective_user.id
 >          if user_id not in data['admins']:
 >               print(fr"Unauthorized access denied for {user_id}.")
 >               update.message.reply_markdown_v2(fr"Access denied for 
 >               {update.effective_user.mention_markdown_v2()}\!")
 >               return
 >          return func(update, context, *args, **kwargs)
 >     return wrapped
> ```
#### Custom keyboard
Inizializzata quando il bot viene startato. **Codice:**
```py
def start(update: tg.Update, context: CallbackContext):
	...
	reply_keyboard = [['/on', '/off', '/color', '/blink'], ['/disco', '/quit']]
	update.message.reply_text(
		'Choose an option:',
		reply_markup=tg.ReplyKeyboardMarkup(
		     reply_keyboard, one_time_keyboard=False, 
             input_field_placeholder='Option?'),
		)
```
**Output:**

<img src="https://raw.githubusercontent.com/andrebellu/RGBarduino/main/RGBarduino/kb.png" alt="kb" width="" height="" style="vertical-align:top">

#### Inline keyboard
Inizializzata quando viene chimato il comando '/color'. **Codice:**
```py
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
```
**Output:**

<img src="https://raw.githubusercontent.com/andrebellu/RGBarduino/main/RGBarduino/inkb.png" alt="inkb" width="" height="" style="vertical-align:top">

#### Bot commands
*Tutti i comandi sono preceduti dallo '/'*
- start: starta il bot;
- on: accende il led (luce bianca);
- off: spegne il led;
- color: (menù per cambiare colori);
	- **Colori disponibili:**
		- rosso;
		- verde;
		- blu;
		- giallo;
		- viola;
		- azzurro;
- fastblink: lampeggio led (150ms delay);
- disco: sequenza casuale colori.
- quit: chiude la comunicazione con la seriale
---
