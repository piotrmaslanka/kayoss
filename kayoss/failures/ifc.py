from satella.threads import TQM
from collections import namedtuple

class FailuresInterface(TQM.Interface):
    def doorbell(self):
        self.queue.put(Doorbell())

Doorbell = namedtuple('Doorbell', ())

