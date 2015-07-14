from satella.threads import TQM
from collections import namedtuple

class SonosInterface(TQM.Interface):
    def doorbell(self): self.queue.put(Doorbell())

Doorbell = namedtuple('Doorbell', ())
