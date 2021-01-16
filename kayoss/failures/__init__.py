from __future__ import division
import time
from datetime import datetime
from satella.threads import BaseThread
from kayoss.failures.ifc import FailuresInterface
from kayoss.failures.smsgate import send_sms

class FailuresThread(BaseThread):
    
    TQMInterface = FailuresInterface
    
    def __init__(self, tqm):
        BaseThread.__init__(self)
        self.reader = tqm.get_reader_for('failures')
        self.saver = tqm.get_interface_for('saver')
        self.sonos = tqm.get_interface_for('sonos')
        self.statedict = dict(((k, False) for k in FailuresThread.LABEL_DICT.iterkeys()))
        
    LABEL_DICT = {
        'failures.water.leak.irrigation': 'przeciek wody',
        'failures.power.fuse.l1': 'bezpiecznik L1',
        'failures.power.fuse.l2': 'bezpiecznik L2',
        'failures.power.fuse.l3': 'bezpiecznik L3',
        'failures.power.fuse.12v': 'bezpiecznik 12V',
        'failures.power.230v': 'brak 230V',
        'failures.power.fuse.socks': 'bezpiecznik gniazdek',
        'failures.alarm': 'alarm',
    }
        
    def run(self):
        
        
        last_komorka_on = datetime.now().hour
        
        while True:
            time.sleep(1)
            for msg in self.reader:     # Do we have anything to process?
                pass

            s = self.saver.get(['failures.water.leak.irrigation',
                                'failures.power.fuse.l1',
                                'failures.power.fuse.l2',
                                'failures.power.fuse.l3',
                                'failures.power.fuse.socks',
                                'failures.power.fuse.12v',
                                'failures.power.230v',
                                'failures.alarm']) or {}            

            for k, v in s.iteritems():
                if v and not self.statedict[k]:
                    # Alarm occurred
                    msg = 'Wystapil '+FailuresThread.LABEL_DICT[k]
                    send_sms('xxxxxxxxx', msg)
                              
                elif not v and self.statedict[k]:
                    # Alarm out
                    msg = 'Odwoluje '+FailuresThread.LABEL_DICT[k]
                    send_sms('xxxxxxxxx', msg)
                              
                self.statedict[k] = v

            s = self.saver.get(['alarm.presence']) or {}
            if 'alarm.presence' in s:
                komorka = s['alarm.presence'] & 16
                if komorka:
                    if datetime.now().hour != last_komorka_on:
                        if datetime.now().hour in (21, 22, 23, 0, 1, 2, 3, 4, 5):
                            last_komorka_on = datetime.now().hour
                            self.sonos.komorka()
            