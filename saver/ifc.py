from satella.threads import TQM
from threading import Lock
from collections import namedtuple

class SaverInterface(TQM.Interface):

    class Deferred(object):
        def __init__(self):
            self.lock = Lock()
            self.lock.acquire()
            self.result = None
            
        def completed(self, result):
            self.result = result
            self.lock.release()
            
        def wait(self):
            self.lock.acquire()
            return self.result
        
    # in all cases, operation has failed if result is None
        
    def save(self, key, value):
        self.queue.put(Save(key, value))

    def get(self, keys):
        # result is a dict (key => value)
        d = SaverInterface.Deferred()
        self.queue.put(Get(d, keys))
        return d.wait()
    
Save = namedtuple('Save', ('key', 'value'))
Get = namedtuple('Get', ('deferred', 'keys'))
