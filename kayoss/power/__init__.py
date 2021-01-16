from __future__ import division
import time
from satella.threads import BaseThread
from kayoss.power.ifc import PowerInterface

class PowerThread(BaseThread):
    
    TQMInterface = PowerInterface
    
    def __init__(self, tqm):
        BaseThread.__init__(self)
        self.rs485 = tqm.get_interface_for('rs485')
        self.reader = tqm.get_reader_for('heating')
        self.saver = tqm.get_interface_for('saver')

    def run(self):
        while True:
            time.sleep(0.5)
        
            for msg in self.reader:     # Do we have anything to process?
                pass
                        
            # Read all relevanties
            rster = lambda port: self.rs485.readRegisters(31, port)            
            
            l1v, l2v, l3v = rster(1), rster(3), rster(5)
            l1w, l2w, l3w = rster(19), rster(21), rster(23)
            l1vif, l2vif, l3vif = rster(7), rster(9), rster(11)
            l1va, l2va, l3va = rster(27), rster(29), rster(31)
            l1var, l2var, l3var = rster(35), rster(37), rster(39)
            l1hz, l2hz, l3hz = rster(51), rster(53), rster(55)

            try:
                consumption = int(self.rs485.readLTE(31, 79))    # in Watt*hour
            except TypeError:
                consumption = None

            # Go and commit everything to storage
            if l1v != None: self.saver.save('power.l1v', l1v)
            if l2v != None: self.saver.save('power.l2v', l2v)
            if l3v != None: self.saver.save('power.l3v', l3v)

            if l1w != None: self.saver.save('power.l1w', l1w)
            if l2w != None: self.saver.save('power.l2w', l2w)
            if l3w != None: self.saver.save('power.l3w', l3w)

            if l1vif != None: self.saver.save('power.l1vif', l1vif)
            if l2vif != None: self.saver.save('power.l2vif', l2vif)
            if l3vif != None: self.saver.save('power.l3vif', l3vif)

            if l1va != None: self.saver.save('power.l1va', l1va)
            if l2va != None: self.saver.save('power.l2va', l2va)
            if l3va != None: self.saver.save('power.l3va', l3va)

            if l1var != None: self.saver.save('power.l1var', l1var)
            if l2var != None: self.saver.save('power.l2var', l2var)
            if l3var != None: self.saver.save('power.l3var', l3var)

            if l1hz != None: self.saver.save('power.l1hz', l1hz)
            if l2hz != None: self.saver.save('power.l2hz', l2hz)
            if l3hz != None: self.saver.save('power.l3hz', l3hz)

            if consumption != None: self.saver.save('power.consumption', consumption)
