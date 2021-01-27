from satella.coding.structures import Singleton
from smok.basics import StorageLevel
from smok.client import SMOKDevice
import sys
import os

from .modbus import SerialCommunication, NetSerial
from .modbus_pathpoints import MODBUSPathpoint, PATHPOINT_RE


@Singleton
class MyDevice(SMOKDevice):
    def provide_unknown_pathpoint(self, name: str,
                                  storage_level: StorageLevel = StorageLevel.TREND):
        match = PATHPOINT_RE.match(name)
        if not match:
            raise KeyError()
        if match.group(1) == '1':
            return MODBUSPathpoint(self.modbus_232, name, self)
        else:
            return MODBUSPathpoint(self.modbus_485, name, self)

    def __init__(self):
        if sys.platform == 'win32':
            base_dir = 'c:\\projects\\kayoss\\certificates'
        else:
            base_dir = '/home/pi/kayoss/certificates'
        super().__init__(os.path.join(base_dir, 'cert.crt'),
                         os.path.join(base_dir, 'cert.key'),
                         evt_database='evt.pkl')
        # self.modbus_232 = SerialCommunication(NetSerial('10.0.0.201'))
        # self.modbus_485 = SerialCommunication(NetSerial('10.0.0.202'))
        self.modbus_232 = SerialCommunication(NetSerial('10.0.0.201'))
        self.modbus_485 = SerialCommunication(NetSerial('10.0.0.202'))
