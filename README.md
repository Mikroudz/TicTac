# Ristinollapeli UR5 robotille


## Kuinka käyttää

Tarvitset pythonin ja UR5 robotin. Eikä muuta nih. Peli alkaa kun ajat prog.py tiedoston. 

### Tarvittavat jutut nih

Python 3.5 tai uudempi

Paho MQTT:

```
pip install paho-mqtt
```
### Ei pakollinen:

Mosquitto broker:

```
sudo apt install mosquitto
```
Mosquitto asetukset:
```
sudo nano /etc/mosquitto/mosquitto.conf
```
Lisää tiedoston loppuun
```
port 1883
listener 9001
protocol websockets
```

## License

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                    Version 2, December 2004

 Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>

 Everyone is permitted to copy and distribute verbatim or modified
 copies of this license document, and changing it is allowed as long
 as the name is changed.

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

  0. You just DO WHAT THE FUCK YOU WANT TO.

