from satella.threads import BaseThread
from kayoss.saver.ifc import SaverInterface, Save, Get

class SaverThread(BaseThread):
    
    TQMInterface = SaverInterface
    
    def __init__(self, tqm):
        BaseThread.__init__(self)
        self.reader = tqm.get_reader_for('saver', None)
        self.db = {}
        
    def run(self):
        for msg in self.reader:
            if isinstance(msg, Save):
                self.db[msg.key] = msg.value
            elif isinstance(msg, Get):
                try:
                    k = dict(((k, self.db[k]) for k in msg.keys))
                    msg.deferred.completed(k)
                except KeyError:
                    msg.deferred.completed(None)
                    
        
        
    
                                         
                                         
                            