from __future__ import division
import time
from satella.threads import BaseThread
from kayoss.alarm.ifc import AlarmInterface

class AlarmThread(BaseThread):
    
    TQMInterface = AlarmInterface
    
    def __init__(self, tqm):
        BaseThread.__init__(self)
        self.rs485 = tqm.get_interface_for('rs485')
        self.reader = tqm.get_reader_for('alarm')
        self.saver = tqm.get_interface_for('saver')

    def run(self):
        while True:            
            for msg in self.reader:     # Do we have anything to process?
                pass
                        
            # Read all relevanties
            pk = self.rs485.readRegisters(1, 4070, 3)
            if pk != None:
                presence, mask, statii = pk
                try:
                    self.rs485.writeRegister(1, 4070, 0)
                except:
                    pass
                self.saver.save('alarm.presence', presence)
                self.saver.save('alarm.mask', mask)
                self.saver.save('alarm.statii', statii)
                
                self.saver.save('failures.alarm', statii & 1)
                    

            time.sleep(2)

                                         
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
                                         