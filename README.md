# Yaesu FT-897D CAT Display In Python
Python implementation of CAT system for Yaesu FT-897ND.

## Overview
According to Yaesu FT-897D's manual, the CAT System allows the transceiver to be controlled by a personal computer. The purpose of this project is to learn this system for later implementing it using an AVR microcontroller.

The program is written in Python and uses ```serial``` library to connect to the transceiver. It runs as console application in text mode.

## :warning: Important Warning!

1. This program is provided as is and I'm not responsible for any damage it may cause.
2. Before using this program make sure you completely understand what you are doing.
3. Before sending any commands to your transceiver make a backup copy of factory calibration settings in service menu. There are [sources](http://www.ka7oei.com/ft817_meow.html) which state that some commands may completely erase it. This may result in need to send the transceiver to Yaesu for realignment.

## Connecting to PC

Yaesu FT-897D's is connected to PC through a COM port. I used one of many USB to COM boards available on eBay and AliExpress for a couple of dollars. The port is connected to ```TXD``` and ```RXD``` pins of the ```ACC``` connector located on the rear panel of the transceiver. Refer to [Yaesu FT-817ND's Operation Manual](http://www.yaesu.co.uk/files/FT-817ND_Operating%20Manual.pdf) for more details.

![ACC plug](https://raw.githubusercontent.com/4x1md/ft817_cat_python/master/images/ft817_connection.png)

Programming cable can also be used and will work fine with this program.

## Program Structure

The program is implemented as ```FT897``` class with following methods:

```__init__(self, serial_port, serial_speed, serial_stopbits)```: constructor which starts serial connection and resets transceiver state variables ```self._frequency```, ```self._mode```, ```self._squelch```, ```self._s_meter```,  ```self._ctcss_dcs```,  ```self._discriminator```,  ```self._t_mod_t_power```,  ```self._t_alc```,  ```self._t_vswr``` and  ```self._t_mod```.

```read_frequency(self)```: reads frequency and mode data and stores it in ```self._freq``` and ```self._mode``` variables.

```read_rx_status(self)```: reads receiver status (S-level, squelch state, CTCSS/DCS code match and discriminator centering) and stores S-level in ```self._s_meter```, squelch state in  ```self._squelch```, ctcss/dcs state in ```self._ctcss_dcs``` and discriminator status in ```self._discriminator``` variables.

```get_s_meter_string(self, s_meter)```: generates S-meter string for second line of output.

```get_rx_state_string(self)```: generates some lines of text which include frequency, modulation, squelch level, ctcss/dcs status, discriminator status when modulation is FM and S-meter data.

```read_tx_status(self)```: reads trasmitter status (transmission power, alc, Vswr and modulation) and store trasmission power in ```self._t_power```, alc in ```self._t_alc```, vsvr in ```self._t_vswr``` and modulation in ```self._t_mod```.

```get_tx_state_string(self)```: generates some lines of text which include frequency, modulation, power, alc, vswr and modulation.

```read_receiving(self)```: check if the radio is transmitting or receiving, if it is transmitting return False, if is receiving return True.

```write_frequency(self)```: write a frequency to the radio, the frequency must be a 8 number string, return True if the radio accept the frequency False if the radio cannot set the desired frequency.

```write_mode(self)```: write the radio mode, the radio modes are string: LSB, USB, CW, CWR, AM, FM, DIG and PKT. Return True if the mode is correct and False otherwise.

IF THE RADIO DON'T RESPOND THE LIBRARY QUIT THE PROGRAM!

## Program Settings And Constants

### FT897() Class

```FT897``` class contains the following settings and constants:

```SERIAL_SPEED```, ```SERIAL_STOPBITS```: COM port speed and stopbits accordingly. By default FT-897 CAT interface is set to 4800 bps with two stop bits.

```SERIAL_TIMEOUT```: sets COM port reading timeout to avoid program blocking if the transceiver is not connected to the port or is turned off.

Byte sequences to send to the trasceiver to:

```CMD_READ_FREQ``` read frequency<br>
```CMD_READ_RX_STATUS```: RX status<br>
```CMD_SET_FREQ ```: set frequency<br>
```CMD_SET_MODE```: set radio mode<br>
```CMD_READ_TX_STATUS```: TX status<br>
```CMD_READ_TX_METER```: TX meters<br>

### trx_monitor.py

```SERIAL_PORT```: COM port name where FT-897D transceiver is connected.<br>
```SAMPLES_PER_SEC```: number of times per second to query the transceiver.

## Running the program

Run the ```trx_monitor.py``` file in Python interpreter.

## Program Output

The output consists of lines which are pretty self explanatory.

```Starting FT-897D monitor...```<br>
```Receiving```<br>
```145237500Hz```<br>
```FM```<br>
```SQL: ON```<br>
```DISCRIMINATOR: NOT CENTERED```<br>
```CTCSS-DCS: UNDETECTED```<br>
```S0+00 ...............```<br>

```Starting FT-897D monitor...```<br>
```Trasmitting```<br>
```14523750HZ```<br>
```FM```<br>
```Power: 9```<br>
```Alc: 3```<br>
```Vswr: 0```<br>
```Mod: 3```<br>

The first line shows frequency, mode (AM, FM, SSB, PKT etc.) and squelch state. The second line is S-Meter which shows S-level and dB over S9 and a simple scale where 15 dots correspond to S0 and 15 pipes correspond to S9+20dB.

## Questions? Suggestions?
You are more than welcome to contact me with any questions, suggestions or propositions regarding this project. You can:

1. Visit [my QRZ.COM page](https://www.qrz.com/db/4X1MD)
2. Visit [my Facebook profile](https://www.facebook.com/Dima.Meln)
3. :email: Write me an email to iosaaris =at= gmail dot com

73 de 4X1MD ex 4X5DM

![73's](https://raw.githubusercontent.com/4x1md/ft817_cat_python/master/images/73s.jpg)
