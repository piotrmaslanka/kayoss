from satella.threads import BaseThread
from kayoss.modbus.modbus import SerialCommunication
from kayoss.modbus.ifc import ModbusInterface, WriteRegister, ReadRegisters, ReadFlag, ReadLTE

class ModbusThread(BaseThread):
                   
    TQMInterface = ModbusInterface
                   
    def __init__(self, tqm, name, comport):
        BaseThread.__init__(self)
        self.sercom = SerialCommunication(comport)
        self.reader = tqm.get_reader_for(name, None)
        
    def run(self):
        for msg in self.reader:
            try:
                if isinstance(msg, WriteRegister):
                    self.sercom.setReg(msg.address, msg.port, msg.value)
#                    print 'WRITE REGISTER %s:%s <- %s' % (msg.address, msg.port, msg.value)
                    msg.deferred.completed(True)
                elif isinstance(msg, ReadRegisters):
                    regs = self.sercom.getReg(msg.address, msg.port, amount=msg.amount)
#                    print 'READ REGISTER (%s:%s) = [%s]' % (msg.address, msg.port, repr(regs))
                    msg.deferred.completed(regs)
                elif isinstance(msg, ReadFlag):
                    flg = self.sercom.getFlag(msg.address, msg.port)
#                    print 'READ FLAG %s:%s = %s' % (msg.address, msg.port, flg)
                    msg.deferred.completed(flg)
                elif isinstance(msg, ReadLTE):
                    lte = self.sercom.getLTEReg(msg.address, msg.port)
#                    print 'READ LTE %s:%s = %s' % (msg.address, msg.port, lte)
                    msg.deferred.completed(lte)
            except Exception as e:
                msg.deferred.completed(None)