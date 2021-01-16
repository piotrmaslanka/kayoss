"""
A P/6680-enabled serial.Serial replacement
This object is completely replaceable with serial.Serial as far as kayoss is concerned
"""
from socket import socket, AF_INET, SOCK_STREAM, error as SocketError, timeout as SocketTimeoutError
import time
import logging

EWOULDBLOCK = (10035, 11)

logger = logging.getLogger(__name__)


class NetSerial:
    def __init__(self, ip):
        self.addr = (ip, 6680)
        self.__recon()

    def __recon(self):
        while True:
            try:
                self.sock = socket(AF_INET, SOCK_STREAM)
                self.sock.settimeout(10)
                self.sock.connect(self.addr)
            except (SocketError, SocketTimeoutError):
                logger.warning('Transient problems connecting to %s', self.addr[0])
            break

    def flushInput(self):
        pass

    def flushOutput(self):
        self.sock.setblocking(0)
        try:
            self.sock.recv(512)
        except ConnectionResetError:
            self.__recon()
        except SocketTimeoutError:
            pass
        except SocketError as e:
            if e.errno not in EWOULDBLOCK:
                raise

    def write(self, data):
        try:
            self.sock.send(data)
        except SocketError:
            logger.info('write(): reconnect')
            self.__recon()
            self.write(data)

    def read(self, data):
        elapsed = time.time()

        self.sock.settimeout(3)
        p = b''
        while len(p) < data:
            try:
                s = self.sock.recv(data-len(p))
                if s == b'':
                    logger.info('read(): reconnect')
                    self.__recon()
                p = p + s
            except ConnectionResetError:
                self.__recon()
            except SocketTimeoutError:
                logger.info('somewhat timeoutish')
                break
            if time.time() - elapsed > 3:
                logger.info('superelapse')
                break

        return p
