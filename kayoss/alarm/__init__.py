from __future__ import division
import time
from satella.threads import BaseThread
from kayoss.alarm.ifc import AlarmInterface, ArmCircuit, DisarmCircuit, ClearPersistence

class AlarmThread(BaseThread):
    
    TQMInterface = AlarmInterface
    
    def __init__(self, tqm):
        BaseThread.__init__(self)
        self.rs485 = tqm.get_interface_for('rs485')
        self.reader = tqm.get_reader_for('alarm')
        self.saver = tqm.get_interface_for('saver')

    def run(self):
        while True:         
            time.sleep(0.5)
       
            for msg in self.reader:     # Do we have anything to process?
                if isinstance(msg, ArmCircuit):
                    mask = self.rs485.readRegisters(1, 4071, 1)
                    mask = mask | (1 << msg.circuit_number)
                    self.rs485.writeRegister(1, 4071, mask)
                elif isinstance(msg, DisarmCircuit):
                    mask = self.rs485.readRegisters(1, 4071, 1)
                    mask = mask & (65535 - (1 << msg.circuit_number))
                    self.rs485.writeRegister(1, 4071, mask)
                elif isinstance(msg, ClearPersistence):
                    pass
                        
            # Read all relevanties
            pk = self.rs485.readRegisters(1, 4070, 3)
            if pk != None:
                presence, mask, statii = pk
                self.saver.save('alarm.presence', presence)
                self.saver.save('alarm.mask', mask)
                self.saver.save('alarm.statii', statii)
                
                self.saver.save('failures.alarm', statii & 1)
                    
                    
                self.rs485.writeRegister(1, 4070, 0)

            time.sleep(3)
                                         
            # Go and commit everything to storage
#            if l1v != None: self.saver.save('power.l1v', l1v)

                                         
                                         
                                         
#				 if (presence & 1) > 0:
#					alarms.append('SABOTAZ')
#				if (presence & 2) > 0:
#					alarms.append('KORYTARZ')
#				if (presence & 4) > 0:
#					alarms.append('DOM')
#				if (presence & 8) > 0:
#					alarms.append('PIWNICA')
#				if (presence & 16) > 0:
#					alarms.append('KOMORKA')                                        
                                         