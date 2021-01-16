from satella.threads import TQM
from collections import namedtuple

class AlarmInterface(TQM.Interface):
    
    def arm(self, cno):
        self.queue.put(ArmCircuit(cno))        
        
    def disarm(self, cno):
        self.queue.put(DisarmCircuit(cno))
        
    def clear_persistence(self):
        self.queue.put(ClearPersistence())
    

# cname is
#   1 - sabotage
#   2 - pir1   
#   3 - pir2
#   4 - basement
#   5 - shed


ArmCircuit = namedtuple('ArmCircuit', ('circuit_number', ))
DisarmCircuit = namedtuple('DisarmCircuit', ('circuit_number', ))
ClearPersistence = namedtuple('ClearPersistence', ())