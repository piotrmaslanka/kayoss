import time

from satella.os import hang_until_sig
import logging
from kayoss.device import MyDevice
from kayoss.modbus import ModbusError


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    d = MyDevice()
    d.modbus_485.setReg(28, 4113, 0)

    import kayoss.corridor_backlight

    # d.modbus_485.setReg(28, 41 00, 0)
    #     val = d.modbus_485.getReg(28, adr)[0]
    #     if val == 0:
    #         print('Setting ', adr)
    #         d.modbus_485.setReg(28, adr, 1)
    #         input()
    #         d.modbus_485.setReg(28, adr, 0)
    #     else:
    #         print('Value of ', adr, ' is ', val)

    hang_until_sig()
    d.close()
