from satella.threads import TQM
from kayoss.modbus import ModbusThread
from kayoss.modbus.netserial import NetSerial
from kayoss.saver import SaverThread
from kayoss.heating import HeatingThread
from kayoss.power import PowerThread
from kayoss.irrigation import IrrigationThread
from kayoss.alarm import AlarmThread
from kayoss.httpserver import HttpServerThread
from kayoss.sonos import SonosThread
from kayoss.failures import FailuresThread

if __name__ == '__main__':
    tqm = TQM()

    tqm.register_interface('saver', SaverThread.TQMInterface)
    tqm.register_interface('rs232', ModbusThread.TQMInterface)
    tqm.register_interface('rs485', ModbusThread.TQMInterface)
    tqm.register_interface('heating', HeatingThread.TQMInterface)
    tqm.register_interface('power', PowerThread.TQMInterface)
    tqm.register_interface('sonos', SonosThread.TQMInterface)
    tqm.register_interface('alarm', AlarmThread.TQMInterface)
    tqm.register_interface('irrigation', IrrigationThread.TQMInterface)
    tqm.register_interface('httpserver', HttpServerThread.TQMInterface)
    tqm.register_interface('failures', FailuresThread.TQMInterface)
    
    saver_t = SaverThread(tqm)
    rs232_t = ModbusThread(tqm, 'rs232', NetSerial('10.0.0.201'))
    rs485_t = ModbusThread(tqm, 'rs485', NetSerial('10.0.0.202'))
    heating_t = HeatingThread(tqm)
    power_t = PowerThread(tqm)
    alarm_t = AlarmThread(tqm)
    irrigation_t = IrrigationThread(tqm)
    httpserver_t = HttpServerThread(tqm)
    failures_t = FailuresThread(tqm)
    sonos_t = SonosThread(tqm)
    
    failures_t.start()
    saver_t.start()
    rs232_t.start()
    rs485_t.start()
    
    # Start handlers
    heating_t.start()
    power_t.start()
    alarm_t.start()
    irrigation_t.start()
    sonos_t.start()
    
    # Start interface
    httpserver_t.start()
