from satella.threads import BaseThread
from kayoss.sonos.ifc import SonosInterface, Doorbell, Komorka
import soco, datetime, time

BELL = ('http://10.0.0.200/bell.mp3', 35, 7)
KOMU = ('http://10.0.0.200/komorka.mp3', 30, 7)

class SonosThread(BaseThread):

    TQMInterface = SonosInterface

    def __init__(self, tqm):
        BaseThread.__init__(self)
        self.reader = tqm.get_reader_for('sonos', None)
        self.devices = []
        self.zones = set()

    def _rediscover_sonos_devices(self):
        zones = soco.discover()
        while zones is None:
            zones = soco.discover()

        for zone in zones:
            self.zones.add(zone)

        self.last_rediscovered = time.time()

    class DingDongThread(BaseThread):
        """
        Ooh.

        The player thread"""
        def __init__(self, device, soundarg):
            BaseThread.__init__(self)
            self.device = device
            self.arg = soundarg

        def run(self):
            print(u'Playing %s on %s' % (self.arg[0], self.device.player_name))
            VOL = self.arg[1]
            URI = self.arg[0]
            DELAY = self.arg[2]

            cpe = self.device.get_current_track_info()

            was_playing = self.device.get_current_transport_info()['current_transport_state'] == 'PLAYING'
            was_radioing = cpe['uri'].startswith('aac://')

            last_volume = self.device.volume

            self.device.volume = VOL
            self.device.play_uri(URI)
            time.sleep(DELAY)

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
        print( '[SonosThread] Found %s devices' % (len(self.zones), ))

        last_dong_on = time.time()

        while True:
            if time.time() - self.last_rediscovered > 3600:
                self._rediscover_sonos_devices()

            for msg in self.reader:
                if isinstance(msg, Doorbell):
                    if (time.time() - last_dong_on) < 10:
                        continue
                    else:
                        last_dong_on = time.time()
                        for device in self.zones:
                            SonosThread.DingDongThread(device, BELL).start()
                if isinstance(msg, Komorka):
                    for device in self.zones:
                        SonosThread.DingDongThread(device, KOMU).start()

