from __future__ import division
import time
from datetime import datetime
from satella.threads import BaseThread
from kayoss.heating.ifc import HeatingInterface, AdjustNightSettings, LoadCWU, ForbidCWU

class HeatingThread(BaseThread):
    
    TQMInterface = HeatingInterface
    
   
    def __init__(self, tqm):
        BaseThread.__init__(self)
        self.rs232 = tqm.get_interface_for('rs232')
        self.rs485 = tqm.get_interface_for('rs485')
        self.reader = tqm.get_reader_for('heating')
        self.saver = tqm.get_interface_for('saver')
        self.sonos = tqm.get_interface_for('sonos')
        self.heating = tqm.get_interface_for('heating')
        
        
    def run(self):
        cur_wh_mode = 0         # 0: not actively heating the water up, temperatures are 10/10
                                # 1: heating the water up, temperatures are 40/40
                                # 2: don't heat the water until end of day
        
        while True:
            time.sleep(0.5)
        
            for msg in self.reader:     # Do we have anything to process?
                if isinstance(msg, AdjustNightSettings):
                    self.rs232.writeRegister(1, 4174, msg.nightCWU, deferred=False, enforce=True)
                    self.rs232.writeRegister(1, 4169, msg.nightCO, deferred=False, enforce=True)     

                if isinstance(msg, LoadCWU):
                    self.rs232.writeRegister(1, 4174, 40, deferred=False, enforce=True)
                    self.rs232.writeRegister(1, 4143, 40, deferred=False, enforce=True)
                    cur_wh_mode = 1
  
                if isinstance(msg, ForbidCWU):
                    self.rs232.writeRegister(1, 4174, 10, deferred=False, enforce=True)
                    self.rs232.writeRegister(1, 4143, 10, deferred=False, enforce=True)
                    cur_wh_mode = 2
            
            # Read all relevanties
            tempify = lambda temp: (-(temp-32768) if temp > 32768 else temp)/10
            rster = lambda port: self.rs232.readRegisters(1, port)
            rflg = lambda port: self.rs232.readFlag(1, port)
            
            p_external, p_internal, p_internal_ref = rster(4089), rster(4136), rster(4132)
            p_co, p_co_ref = rster(4134), rster(4135)
            p_cwu, p_cwu_ref = rster(4104), rster(4102)
            p_boiler = rster(4103)
                        
            f_pump_circ, f_pump_load = rflg(7077), rflg(7078)
            f_pump_co, f_heating = rflg(7115), rflg(7129)
            
            r_co_day, r_co_night = rster(4167), rster(4169)
            
            p_temp_up = self.rs485.readRegisters(14, 4000, 1)
            if p_temp_up == 10000: p_temp_up = None

            p_temp_mid = self.rs485.readRegisters(14, 4002, 1)
            if p_temp_mid == 10000: p_temp_mid = None

            
            # Go and commit everything to storage
            if p_external is not None: self.saver.save('heating.external', tempify(p_external))
            if p_internal is not None: self.saver.save('heating.internal', tempify(p_internal))
            if p_internal_ref is not None: self.saver.save('heating.internal_ref', tempify(p_internal_ref))
            if p_co is not None: self.saver.save('heating.co', tempify(p_co))
            if p_co_ref is not None: self.saver.save('heating.co_ref', tempify(p_co_ref))
            if p_cwu is not None: self.saver.save('heating.cwu', tempify(p_cwu))
            if p_cwu_ref is not None: self.saver.save('heating.cwu_ref', tempify(p_cwu_ref))
            if p_boiler is not None: self.saver.save('heating.boiler', tempify(p_boiler))
                
            if f_pump_circ is not None: self.saver.save('heating.pump_circ', f_pump_circ)
            if f_pump_load is not None: self.saver.save('heating.pump_load', f_pump_load)
            if f_pump_co is not None: self.saver.save('heating.pump_co', f_pump_co)
                
            if r_co_day is not None: self.saver.save('heating.set_co_day', r_co_day)
            if r_co_night is not None: self.saver.save('heating.set_co_night', r_co_night)
            
            if p_temp_up is not None: self.saver.save('heating.up', tempify(p_temp_up))
            if p_temp_mid is not None: self.saver.save('heating.mid', tempify(p_temp_mid))
            
            
            self.saver.save('heating.cwu.system_state', cur_wh_mode)

            # Analyze automatic heating
            if (p_cwu > 380) and (cur_wh_mode == 1):
                cur_wh_mode = 0
                self.rs232.writeRegister(1, 4174, 15, deferred=False, enforce=True)
                self.rs232.writeRegister(1, 4143, 40, deferred=False, enforce=True)            
                self.sonos.hot_water_available()

            if (datetime.now().hour >= 23) and (cur_wh_mode == 2):
                self.rs232.writeRegister(1, 4143, 40, deferred=False, enforce=True)            
                self.rs232.writeRegister(1, 4174, 15, deferred=False, enforce=True)
                cur_wh_mode = 0
                    
