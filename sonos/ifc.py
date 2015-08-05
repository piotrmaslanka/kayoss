from satella.threads import TQM
from collections import namedtuple

class SonosInterface(TQM.Interface):
    def doorbell(self): self.queue.put(Doorbell())
    def komorka(self): self.queue.put(Komorka())
        
    def hot_water_available(self): pass
        
Doorbell = namedtuple('Doorbell', ())
Komorka = namedtuple('Komorka', ())
