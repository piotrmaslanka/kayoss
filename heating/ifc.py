from satella.threads import TQM
from collections import namedtuple

class HeatingInterface(TQM.Interface):
    def adjust_night_settings(self, nightCO, nightCWU):
        self.queue.put(AdjustNightSettings(nightCO, nightCWU))

AdjustNightSettings = namedtuple('AdjustNightSettings', ('nightCO', 'nightCWU'))