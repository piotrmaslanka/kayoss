kayoss
======

This is a core server for my "smart home" installation.
It monitors a couple of things using MODBUS serials, 
utilizing the [smok-client](https://github.com/smok-serwis/smok-client)
library for these.
It has an implementation of MODBUS. It depends on
[smok](https://smok.co) to send notifications about changing states or 
triggering of the alarm.

It serves all collected stuff through HTTP and allows viewing/modification of that.

Of course, requires [Satella](https://github.com/piotrmaslanka/satella).


recent
------
2019: 
There were a lost of changes. Kamkorder, PALHOST and SEALHOST were totally ditched because CCTV was dedicated to other hardware. Tibbo's Virtual Serial Port drivers were also removed, as they proved to be uncompilable to latest Raspberry Pi hardware. Therefore, a Tibbo Basic application called _P/6680_ (source will be attached later) was created which emulates a serial port (with preset baudrate and stuff) using simple TCP stream. Kayoss has now no dependencies, save for _soco_ and _satella_

2021:
Kayoss was rewritten as a living showcase of `smok-client`'s capabilities.
Now entire house, including blinds, is controlled via a panel
on [smok.co](https://smok.co).
 

