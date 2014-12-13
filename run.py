from satella.threads import TQM
from kayoss.modbus import ModbusThread
from kayoss.saver import SaverThread
from kayoss.heating import HeatingThread
from kayoss.power import PowerThread
from kayoss.irrigation import IrrigationThread
from kayoss.alarm import AlarmThread
from kayoss.httpserver import HttpServerThread
from kayoss.failures import FailuresThread
from serial import Serial

if __name__ == '__main__':
    tqm = TQM()

    tqm.register_interface('saver', SaverThread.TQMInterface)
    tqm.register_interface('rs232', ModbusThread.TQMInterface)
    tqm.register_interface('rs485', ModbusThread.TQMInterface)
    tqm.register_interface('heating', HeatingThread.TQMInterface)
    tqm.register_interface('power', PowerThread.TQMInterface)
    tqm.register_interface('alarm', AlarmThread.TQMInterface)
    tqm.register_interface('irrigation', IrrigationThread.TQMInterface)
    tqm.register_interface('httpserver', HttpServerThread.TQMInterface)
    tqm.register_interface('failures', FailuresThread.TQMInterface)
    
    saver_t = SaverThread(tqm)
    rs232_t = ModbusThread(tqm, 'rs232', Serial('COM1', baudrate=9600, parity='N', stopbits=1, timeout=1))
    rs485_t = ModbusThread(tqm, 'rs485', Serial('COM2', baudrate=9600, parity='N', stopbits=1, timeout=1))
    heating_t = HeatingThread(tqm)
    power_t = PowerThread(tqm)
    alarm_t = AlarmThread(tqm)
    irrigation_t = IrrigationThread(tqm)
    httpserver_t = HttpServerThread(tqm)
    failures_t = FailuresThread(tqm)
    
    failures_t.start()
    saver_t.start()
    rs232_t.start()
    rs485_t.start()
    
    # Start handlers
    heating_t.start()
    power_t.start()
    alarm_t.start()
    irrigation_t.start()
    
    # Start interface
    httpserver_t.start()
