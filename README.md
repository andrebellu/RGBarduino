# RGB Arduino Project <img src="https://brandslogos.com/wp-content/uploads/images/large/arduino-logo-1.png" alt="Arduino Logo" width="50" height="50" style="vertical-align:top">
*Progetto realizzato da [Andrea Bellu](https://github.com/andrebellu), [Stefano Longhena](https://github.com/StefanoLonghena), [Leonardo Baccalario](https://github.com/LeonardoBaccalario).*

Il progetto consisteva nel realizzare un circuito con un led RGB utilizzabile tramite un telecomando. Abbiamo poi realizzato un bot di telegram interfacciato con arduino tramite python e la sua libreria pyserial.
---
#### Componenti utilizzati
- [Elegoo Mega2560](https://www.amazon.it/Elegoo-ATmega2560-ATMEGA16U2-Compatibile-Arduino/dp/B071W7WP35). 
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

