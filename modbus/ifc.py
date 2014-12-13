from satella.threads import TQM
from threading import Lock
from collections import namedtuple

class ModbusInterface(TQM.Interface):

    class Deferred(object):
        def __init__(self):
            self.lock = Lock()
            self.lock.acquire()
            self.result = None
            
        def completed(self, result):
            self.result = result
            self.lock.release()
            
        def wait(self):
            self.lock.acquire()
            return self.result
        
    # in all cases, operation has failed if result is None
        
    def readRegisters(self, address, port, amount=1):
        # result will be sequence of ints or single int if amount was 1
        d = ModbusInterface.Deferred()
        self.queue.put(ReadRegisters(d, address, port, amount))
        k = d.wait()
        if amount == 1:
            if k == None:
                return k
            else:
                return k[0]
        else:
            return k
    def readLTE(self, address, port):
        # result is a float
        d = ModbusInterface.Deferred()
        self.queue.put(ReadLTE(d, address, port))
        return d.wait()
    def readFlag(self, address, port):
        # result will be int 0 or 1
        d = ModbusInterface.Deferred()
        self.queue.put(ReadFlag(d, address, port))
        return d.wait()
    def writeRegister(self, address, port, value, deferred=False, enforce=False):
        # result will be True
        
        if enforce:
            while True:
                d = ModbusInterface.Deferred()
                self.queue.put(WriteRegister(d, address, port, value))
                if d.wait() == True:
                    return
        else:                                             
            d = ModbusInterface.Deferred()
            self.queue.put(WriteRegister(d, address, port, value))
            if deferred:
                return d
            else:
                return d.wait()
    
WriteRegister = namedtuple('WriteRegister', ('deferred', 'address', 'port', 'value'))
ReadRegisters = namedtuple('ReadRegister', ('deferred', 'address', 'port', 'amount'))
ReadLTE = namedtuple('ReadLTE', ('deferred', 'address', 'port'))
ReadFlag = namedtuple('ReadFlag', ('deferred', 'address', 'port'))