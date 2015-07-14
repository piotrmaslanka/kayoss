from satella.threads import BaseThread
from kayoss.sonos.ifc import SonosInterface, Doorbell
import soco, datetime, time

BELL_URI = 'http://10.0.0.200/bell.mp3'
BELL_VOLUME = 30
BELL_DURATION = 5

class SonosThread(BaseThread):
    
    TQMInterface = SonosInterface
                
    def __init__(self, tqm):
        BaseThread.__init__(self)
        self.reader = tqm.get_reader_for('sonos', None)
        self.devices = []
        
    def _rediscover_sonos_devices(self):
        zones = soco.discover()
        while zones is None:
            zones = soco.discover()
        self.zones = list(zones)
        self.last_rediscovered = time.time()

    class DingDongThread(BaseThread):
        """
        Ooh.
        
        The player thread"""
        def __init__(self, device):
            BaseThread.__init__(self)
            self.device = device
        
        def run(self):
            cpe = self.device.get_current_track_info()
            
            was_playing = self.device.get_current_transport_info()['current_transport_state'] == 'PLAYING'
            was_radioing = cpe['uri'].startswith('aac://')
            
            last_volume = self.device.volume
            
            self.device.volume = BELL_VOLUME
            self.device.play_uri(BELL_URI)
            time.sleep(BELL_DURATION)
            
            if not was_playing:
                self.device.stop()
            else:
                if was_radioing:
                    self.device.play_uri(cpe['uri'], meta=cpe['metadata'])
                else:
                    self.device.play_from_queue(int(cpe['playlist_position'])-1)
                    self.device.seek(cpe['position'])
                    
            self.device.volume = last_volume
        
    def run(self):
        self._rediscover_sonos_devices()
        self.last_rediscovered = time.time()
        print '[SonosThread] Found %s devices' % (len(self.zones), )
        
        for msg in self.reader:
            
            if datetime.datetime.now().hour == 3 and (time.time() - self.last_rediscovered) > 3600:
                self._rediscover_sonos_devices()
            
            if isinstance(msg, Doorbell):
                for device in self.zones:
                    SonosThread.DingDongThread(device).start()
                                         
                                         
                            