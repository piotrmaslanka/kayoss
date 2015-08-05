from __future__ import division
import time
from satella.threads import BaseThread
from kayoss.irrigation.ifc import IrrigationInterface, SetForbidDrop, SetForbidIrrig, \
                                  SetOverrideS1, SetOverrideS2, SetOverrideS3, \
                                  SetOverrideS4, SetOverrideS5, SetOverrideS6, \
                                  SetOverrideNakr, SetOverrideKos, SetForbidKos

class IrrigationThread(BaseThread):
    
    TQMInterface = IrrigationInterface
    
    def __init__(self, tqm):
        BaseThread.__init__(self)
        self.rs485 = tqm.get_interface_for('rs485')
        self.reader = tqm.get_reader_for('irrigation')
        self.saver = tqm.get_interface_for('saver')
        self.sonos = tqm.get_interface_for('sonos')

    def run(self):
        while True:
            time.sleep(0.5)
            
            for msg in self.reader:     # Do we have anything to process?
                ltd = {SetForbidDrop: 4091,
                       SetForbidIrrig: 4092,
                       SetOverrideS1: 4100, 
                       SetOverrideS2: 4101, 
                       SetOverrideS3: 4102, 
                       SetOverrideS4: 4103, 
                       SetOverrideS5: 4104, 
                       SetOverrideS6: 4105, 
                       SetOverrideNakr: 4106,
                       SetOverrideKos: 4110,
                       SetForbidKos: 4111}
                
                self.rs485.writeRegister(28, ltd[type(msg)], msg.value, False, True) 
                                             
            # Read all relevanties
            pk = self.rs485.readRegisters(28, 4085, 8)
            if pk != None:                
                dailyCounter, sectionCounter, _, prevDayCounter, visStan, \
                leakDetected, forbidDrop, forbidIrrig = pk
                self.saver.save('irrigation.dailyCounter', dailyCounter)
                self.saver.save('irrigation.sectionCounter', sectionCounter)
                self.saver.save('irrigation.prevdayCounter', prevDayCounter)
                self.saver.save('irrigation.visStan', visStan)
                self.saver.save('failures.water.leak.irrigation', leakDetected)
                self.saver.save('irrigation.leakDetected', leakDetected)
                self.saver.save('irrigation.forbidDrop', forbidDrop)
                self.saver.save('irrigation.forbidIrrig', forbidIrrig)
            
            pk = self.rs485.readRegisters(28, 4100, 7)
            if pk != None:
                ovS1, ovS2, ovS3, ovS4, ovS5, ovS6, ovNakr = pk
                
                self.saver.save('irrigation.overrideS1', ovS1)
                self.saver.save('irrigation.overrideS2', ovS2)
                self.saver.save('irrigation.overrideS3', ovS3)
                self.saver.save('irrigation.overrideS4', ovS4)
                self.saver.save('irrigation.overrideS5', ovS5)
                self.saver.save('irrigation.overrideS6', ovS6)
                self.saver.save('irrigation.overrideNakr', ovNakr)                
                
            pk = self.rs485.readRegisters(28, 4107, 5)
            if pk != None:
                minTrwaDeszcz, kosMinPad, kosWybieg, ovKos, forbKos = pk
    
                self.saver.save('irrigation.rainMinutes', minTrwaDeszcz)
                self.saver.save('irrigation.overrideKos', ovKos)
                self.saver.save('irrigation.forbidKos', forbKos)
                
            # check Doorbell
            pk = self.rs485.readRegisters(28, 4112, 1)
            if pk != None:
                if pk == 1:
                    print 'pk engaged'				
                    while pk in (1, None):                        
                        self.rs485.writeRegister(28, 4112, 0, deferred=False, enforce=True)
                        pk = self.rs485.readRegisters(28, 4112)
                        print 'pk is %s' % (pk, )

                    self.sonos.doorbell()
    
            f_labels = (
                (7082, 'L2', 'failures.power.fuse.l2'),
                (7083, 'L1', 'failures.power.fuse.l1'),
                (7084, 'L3', 'failures.power.fuse.l3'),
                (7085, 'Gniazda', 'failures.power.fuse.socks'),
                (7086, 'Zas. 12V', 'failures.power.fuse.12v'),
                (7087, 'Brak zas. 230V', 'failures.power.230v'),
            )
    
            for flagno, label, savervar in f_labels:
                try:
                    pk = self.rs485.readFlag(28, flagno)
                except TypeError:
                    continue
                    
                self.saver.save(savervar, pk)
