from __future__ import division
import time
from satella.threads import BaseThread
from kayoss.heating.ifc import HeatingInterface, AdjustNightSettings

class HeatingThread(BaseThread):
    
    TQMInterface = HeatingInterface
    
    def __init__(self, tqm):
        BaseThread.__init__(self)
        self.rs232 = tqm.get_interface_for('rs232')
        self.rs485 = tqm.get_interface_for('rs485')
        self.reader = tqm.get_reader_for('heating')
        self.saver = tqm.get_interface_for('saver')
        self.heating = tqm.get_interface_for('heating')
        
        
    def run(self):
        
        cur_zad_mode = 0        # 0: zadajnik_up is 0: everything normal
                                # 1: zadajnik_up is 5, engage hot water
                                # 2: zadajnik_up is 10, engage central heating
        
        while True:
            for msg in self.reader:     # Do we have anything to process?
                if isinstance(msg, AdjustNightSettings):
                    self.rs232.writeRegister(2, 4174, msg.nightCWU, deferred=False, enforce=True)
                    self.rs232.writeRegister(2, 4169, msg.nightCO, deferred=False, enforce=True)                 
            
            # Read all relevanties
            tempify = lambda temp: (-(temp-32768) if temp > 32768 else temp)/10
            rster = lambda port: self.rs232.readRegisters(2, port)
            rflg = lambda port: self.rs232.readFlag(2, port)
            
            p_external, p_internal, p_internal_ref = rster(4089), rster(4136), rster(4132)
            p_co, p_co_ref = rster(4134), rster(4135)
            p_cwu, p_cwu_ref = rster(4104), rster(4102)
            p_boiler = rster(4103)
                        
            f_pump_circ, f_pump_load = rflg(7077), rflg(7078)
            f_pump_co, f_heating = rflg(7115), rflg(7129)
            
            r_co_day, r_co_night = rster(4167), rster(4169)
            # Nocna CWU is 4174
            
            try:
                p_temp_up, p_zadajnik_up = self.rs485.readRegisters(14, 4000, 2)
                if p_zadajnik_up == 10000: raise TypeError
            except TypeError:
                p_temp_up = None
                p_zadajnik_up = None
                
            try:
                p_temp_mid = self.rs485.readRegisters(14, 4002, 1)
                if p_temp_mid == 10000: raise TypeError
            except TypeError:
                p_temp_mid = None

            
            # Go and commit everything to storage
            if p_external != None: self.saver.save('heating.external', tempify(p_external))
            if p_internal != None: self.saver.save('heating.internal', tempify(p_internal))
            if p_internal_ref != None: self.saver.save('heating.internal_ref', tempify(p_internal_ref))
            if p_co != None: self.saver.save('heating.co', tempify(p_co))
            if p_co_ref != None: self.saver.save('heating.co_ref', tempify(p_co_ref))
            if p_cwu != None: self.saver.save('heating.cwu', tempify(p_cwu))
            if p_cwu_ref != None: self.saver.save('heating.cwu_ref', tempify(p_cwu_ref))
            if p_boiler != None: self.saver.save('heating.boiler', tempify(p_boiler))
                
            if f_pump_circ != None: self.saver.save('heating.pump_circ', f_pump_circ)
            if f_pump_load != None: self.saver.save('heating.pump_load', f_pump_load)
            if f_pump_co != None: self.saver.save('heating.pump_co', f_pump_co)
            if f_heating != None: self.saver.save('heating.burner', f_heating)
                
            if r_co_day != None: self.saver.save('heating.set_co_day', r_co_day)
            if r_co_night != None: self.saver.save('heating.set_co_night', r_co_night)
            
            if p_temp_up != None: self.saver.save('heating.up', tempify(p_temp_up))
            if p_temp_mid != None: self.saver.save('heating.mid', tempify(p_temp_mid))
            
            # Analyze zadajnik changes
            if p_zadajnik_up == 0 and cur_zad_mode != 0:
                # Set normal mode
                cur_zad_mode = 0
                self.heating.adjust_night_settings(nightCO=19, nightCWU=15)
                print 'Zadajnik 0.0: CO=19, CWU=15'                
            elif p_zadajnik_up == 5 and cur_zad_mode != 1:
                cur_zad_mode = 1
                self.heating.adjust_night_settings(nightCO=19, nightCWU=40)
                print 'Zadajnik 0.5: CO=19, CWU=40'
            elif p_zadajnik_up == 10 and cur_zad_mode != 2:
                cur_zad_mode = 2
                self.heating.adjust_night_settings(nightCO=23, nightCWU=15)
                print 'Zadajnik 1.0: CO=23, CWU=15'
