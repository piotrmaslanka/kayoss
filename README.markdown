kayoss
======

This is a core server for my "smart home" installation.
It monitors a couple of things using MODBUS serials, 
coordinating them in nice thread-oriented ways communicating through interfaces.
Simply a system's engineer wet dream.

It has an implementation of MODBUS, and Polish GSM provider's, "Plus GSM", SMS-sending
gate implementation. 

It serves all collected stuff through HTTP and allows viewing/modification of that.

Of course, requires [Satella](https://github.com/piotrmaslanka/satella).


recent
------
There were a lost of changes. Kamkorder, PALHOST and SEALHOST were totally ditched because CCTV was dedicated to other hardware. Tibbo's Virtual Serial Port drivers were also removed, as they proved to be uncompilable to latest Raspberry Pi hardware. Therefore, a Tibbo Basic application called _P/6680_ (source will be attached later) was created which emulates a serial port (with preset baudrate and stuff) using simple TCP stream. Kayoss has now no dependencies, save for _soco_ and _satella_
