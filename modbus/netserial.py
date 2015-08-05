"""
A P/6680-enabled serial.Serial replacement
This object is completely replaceable with serial.Serial as far as kayoss is concerned
"""
from socket import socket, AF_INET, SOCK_STREAM, error as SocketError, timeout as SocketTimeoutError
import time

EWOULDBLOCK = 10035

class NetSerial(object):
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
                print 'Transient problems connecting to %s' % (self.addr[0], )
            break
    
    def flushInput(self):
        pass
        
    def flushOutput(self):
        self.sock.setblocking(0)
        try:
            self.sock.recv(512)
        except SocketTimeoutError:
            pass
        except SocketError as e:
            if e.errno != EWOULDBLOCK:
                raise
    
    def write(self, data):
        try:
            self.sock.send(data)
        except SocketError:
            print 'write(): reconnect'
            self.__recon()
            self.write(data)
        
    def read(self, data):
        elapsed = time.time()
        
        self.sock.settimeout(3)
        p = ''
        while len(p) < data:
            try:
                s = self.sock.recv(data-len(p))
                if s == '':
                    print 'read(): reconnect'
                    self.__recon()                    
                p = p + s
            except SocketTimeoutError:
                print 'somewhat timeoutish'
                break
            if time.time() - elapsed > 3:
                print 'superelapse'
                break
                
        return p
