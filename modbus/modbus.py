import struct
from datetime import datetime
# ----------------------------------- MODBUS

class ModbusManager(object):
	def __init__(self):
		'''Przygotowuje tablice CRC'''
		lst = []
		i = 0
		while (i<256):
			data = i<<1
			crc = 0
			j = 8
			while (j>0):
				data >>= 1
				if ((data^crc)&0x1):
					crc = (crc>>1) ^ 0xA001
				else:
					crc >>= 1
				j -= 1
			lst.append (crc)
			i += 1
		self.table = lst   		
	def cCRC(self,st):
		'''Liczy MODBUS-CRC z podanego stringa'''
		crc = 0xFFFF
		for ch in st:
			crc = (crc>>8)^self.table[(crc^ord(ch))&0xFF]
		return struct.pack('<H',crc)
	def getReadFlag(self, address, flag):
		flag = flag & 0xFFF8
		msg = chr(address)+'\x01'+struct.pack('>HH', flag, 8)
		return msg + self.cCRC(msg)
	def parseReadFlag(self, msg, flag):
		data =  ord(msg[3])
		bflag = flag & 0xFFF8
		while (bflag <> flag):
			data = data >> 1
			bflag = bflag+1
		return data & 1
	def getReadQuery(self, address, register, amount=1):
		msg = chr(address)+'\x03'+struct.pack('>HH', register, amount)
		return msg + self.cCRC(msg)
	def getWriteQuery(self, address, register, value):
		msg = chr(address)+'\x06'+struct.pack('>HH', register, value)
		return msg + self.cCRC(msg)
	def getWriteFlagQuery(self, address, flag, value):
		msg = struct.pack('>BBHH', address, 5, flag, 0xFF00 if value else 0x0000)
		return msg + self.cCRC(msg)
		
	def getReadInputLTEQuery(self, address, register):
		msg = chr(address)+'\x04'+struct.pack('>HH', register, 2)
		return msg + self.cCRC(msg)		
	def parseReadRequest(self, msg, amount=1):
		lst = []
		for x in xrange(0, amount):
			lst.append(ord(msg[3+x*2]) * 256 + ord(msg[4+x*2]))
		return lst
	def parseReadInputLTERequest(self, msg):
		return ord(msg[3]) * 256 + ord(msg[4]), ord(msg[5]) * 256 + ord(msg[6])
	def validate(self, msg):
		crc = msg[-2:]
		precrc = msg[:-2]
		return self.cCRC(precrc) == crc

class SerialCommunication(object):
	def __init__(self, socket):
		self.mm = ModbusManager()
		self.socket = socket
		
	def getFlag(self, a, r):
		mmr = self.mm.getReadFlag(a, r)
		self.socket.flushInput()
		self.socket.flushOutput()
		self.socket.write(mmr)
		msg = self.socket.read(6)
		if self.mm.validate(msg):
			msg = self.mm.parseReadFlag(msg, r)
			return msg
		else:
			raise Exception, 'CRC - '+str(map(ord, msg))
		
	def getReg(self, a, r, amount=1, filter=True):
		mmr = self.mm.getReadQuery(a, r, amount)
		self.socket.flushInput()
		self.socket.flushOutput()
		self.socket.write(mmr)
		msg = self.socket.read(5+amount*2)
		if self.mm.validate(msg):
			msg = self.mm.parseReadRequest(msg, amount)
			if filter:
				msg = map(lambda x: 65535-x if x > 65535 else x, msg)
			return msg
		else:
			raise Exception, 'CRC - '+str(map(ord, msg))

	def getLTEReg(self, a, r):
		mmr = self.mm.getReadInputLTEQuery(a, r)
		self.socket.flushInput()
		self.socket.flushOutput()
		self.socket.write(mmr)
		msg = self.socket.read(9)
		if self.mm.validate(msg):
			a, b = self.mm.parseReadInputLTERequest(msg)
			lte = a * 65536 + b
		
			dbl, = struct.unpack('f',struct.pack('<L',lte))
		
			return dbl
		else:
			raise Exception, 'CRC - '+str(map(ord, msg))

	def setFlag(self, a, r, v):
		self.socket.flushInput()
		self.socket.flushOutput()
		x = self.mm.getWriteFlagQuery(a, r, v)
		self.socket.write(x)
		msg = self.socket.read(8)

	def setReg(self, a, r, v):
		self.socket.flushInput()
		self.socket.flushOutput()
		self.socket.write(self.mm.getWriteQuery(a, r, v))
		msg = self.socket.read(8)		
