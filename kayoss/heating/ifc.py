from satella.threads import TQM
from collections import namedtuple

class HeatingInterface(TQM.Interface):
    def adjust_night_settings(self, nightCO, nightCWU):
        self.queue.put(AdjustNightSettings(nightCO, nightCWU))
        
    def load_cwu(self):
        self.queue.put(LoadCWU())
        
    def forbid_cwu(self):
        self.queue.put(ForbidCWU())

AdjustNightSettings = namedtuple('AdjustNightSettings', ('nightCO', 'nightCWU'))
LoadCWU = namedtuple('LoadCWU', ())
ForbidCWU = namedtuple('ForbidCWU', ())
