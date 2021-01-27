import threading
import time
import logging
from threading import Thread
from .signals import register_signal
from .device import MyDevice

backlight = None


logger = logging.getLogger(__name__)


class HandleBacklight(Thread):
    def __init__(self):
        super().__init__()
        global backlight
        backlight = self
        self.cancel_on = time.time() + 3*60

    def run(self):
        global backlight
        MyDevice().modbus_485.setReg(28, 4113, 20)
        while time.time() < self.cancel_on:
            time.sleep(5)
        MyDevice().modbus_485.setReg(28, 4113, 0)
        backlight = None


def handle_presence():
    d = MyDevice()
    p = d.get_pathpoint('W1r4070')
    ts, v = p.get()
    if v & 6:
        if backlight is None:
            HandleBacklight().start()
        else:
            backlight.cancel_on = time.time() + 60


class RefreshBacklight(Thread):
    def run(self):
        while True:
            order = MyDevice().get_pathpoint('W1r4070').read()
            MyDevice().execute(order)
            time.sleep(5)


register_signal('alarm.presence', handle_presence)


RefreshBacklight().start()
