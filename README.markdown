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


kamkorder
=========
It's a program to fetch JPG's from HTTP somewhere (a camera, hopefully) - optionally using authentication - and storing
them in folders. It will automatically whack a folder if too low space is detected. Disk
should be large enough to support 2+ days of recording, as entire day is pruned at once
on low disk space.

For Windows.

palhost & sealhost
==================
They are applications to adapt either a TV card input (palhost) or a webcam (sealhost) to HTTP IP interface, collectible by kamkorder.

They are written using DSPack in Delphi7.