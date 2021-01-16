import logging
from concurrent.futures._base import Future

from satella.coding import rethrow_as, log_exceptions
from satella.coding.concurrent import call_in_separate_thread
from satella.coding.decorators import retry
from satella.instrumentation import Traceback
from smok.client import SMOKDevice
from smok.exceptions import OperationFailedError, OperationFailedReason
from smok.pathpoint import AdviseLevel, Pathpoint, PathpointValueType
import re
from kayoss.modbus.modbus import ModbusManager, SerialCommunication, ModbusError

PATHPOINT_RE = re.compile('(w|W|f|B|d)(\d+)(r|f|l)(\d+)')
logger = logging.getLogger(__name__)


class MODBUSPathpoint(Pathpoint):
    @call_in_separate_thread()
    @retry(3, ModbusError, swallow_exception=False)
    def on_write(self, value: PathpointValueType, advise: AdviseLevel) -> Future:
        if self.match.group(1) in ('f', 'd'):
            value = value * 10
        if self.match.group(1) in ('w', 'f', 'd'):
            if value < 0:
                value = abs(value) | 0x8000
        if self.match.group(2) == 'r':
            self.mm.setReg(int(self.match.group(1)), int(self.match.group(3)), value)
        elif self.match.group(2) == 'f':
            self.mm.setFlag(int(self.match.group(1)), int(self.match.group(3)), value)

    def __init__(self, mm: SerialCommunication, name: str, sd: SMOKDevice):
        super().__init__(sd, name)
        self.mm = mm
        self.match = PATHPOINT_RE.match(self.name)
        if not self.match:
            raise KeyError()

    @call_in_separate_thread()
    @rethrow_as(ModbusError, OperationFailedError,
                exception_preprocessor=lambda e: OperationFailedReason.TIMEOUT)
    @log_exceptions(logger, logging.ERROR)
    @retry(5, ModbusError, swallow_exception=False)
    def on_read(self, advise: AdviseLevel):
        address = int(self.match.group(2))
        register = int(self.match.group(4))

        signed = self.match.group(1) in ('w', 'f', 'd')

        if self.match.group(3) == 'r':
            def call(a, r, s):
                v = self.mm.getReg(a, r, signed=s)
                logger.warning(str(v))
                if isinstance(v, (tuple, list)):
                    return v[0]
                else:
                    return v
        elif self.match.group(3) == 'f':
            call = lambda a, r, s: self.mm.getFlag(a, r)
        elif self.match.group(3) == 'l':
            call = lambda a, r, s: self.mm.getLTEReg(a, r)
        else:
            raise ValueError(f'Should not have a match {self.match.group(3)}')

        value = call(address, register, signed)
        if self.match.group(1) in ('f', 'd'):
            value = value / 10
        return value
