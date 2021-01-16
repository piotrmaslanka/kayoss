from satella.threads import TQM
from collections import namedtuple

class IrrigationInterface(TQM.Interface):
    def set_forbid_drop(self, value): self.queue.put(SetForbidDrop(value))
        
    def set_forbid_irrig(self, value): self.queue.put(SetForbidIrrig(value))
        
    def set_overrideS1(self, value): self.queue.put(SetOverrideS1(value))
    def set_overrideS2(self, value): self.queue.put(SetOverrideS2(value))
    def set_overrideS3(self, value): self.queue.put(SetOverrideS3(value))
    def set_overrideS4(self, value): self.queue.put(SetOverrideS4(value))
    def set_overrideS5(self, value): self.queue.put(SetOverrideS5(value))
    def set_overrideS6(self, value): self.queue.put(SetOverrideS6(value))
        
    def set_overrideNakr(self, value): self.queue.put(SetOverrideNakr(value))
        
    def set_overrideKos(self, value): self.queue.put(SetOverrideKos(value))
    def set_forbidKos(self, value): self.queue.put(SetForbidKos(value))

SetForbidDrop = namedtuple('SetForbidDrop', ('value', ))
SetForbidIrrig = namedtuple('SetForbidIrrig', ('value', ))

SetOverrideS1 = namedtuple('SetOverrideS1', ('value', ))
SetOverrideS2 = namedtuple('SetOverrideS2', ('value', ))
SetOverrideS3 = namedtuple('SetOverrideS3', ('value', ))
SetOverrideS4 = namedtuple('SetOverrideS4', ('value', ))
SetOverrideS5 = namedtuple('SetOverrideS5', ('value', ))
SetOverrideS6 = namedtuple('SetOverrideS6', ('value', ))

SetOverrideNakr = namedtuple('SetOverrideNakr', ('value', ))
SetOverrideKos = namedtuple('SetOverrideKos', ('value', ))
SetForbidKos = namedtuple('SetForbidKos', ('value', ))
                                                 