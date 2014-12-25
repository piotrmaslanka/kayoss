from __future__ import division
from satella.threads import BaseThread
from kayoss.httpserver.ifc import HttpServerInterface
import BaseHTTPServer
import urlparse, json

class HttpServerThread(BaseThread):
    
    TQMInterface = HttpServerInterface    
    
    class HTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
        def __init__(self, request, client_address, server):
            BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, request, client_address, server)
            self.request = request
            x = urlparse.urlparse(self.path)
            self.path = x.path
            self.args = dict(((k, v[0]) for k, v in urlparse.parse_qs(x.query).iteritems()))
    
        def do_POST(self):
            print 'POSTed %s' % (self.path, )
            if self.path == '/get/temperatures/':
                s = self.server.saver.get(['heating.external', 'heating.internal',
                                       'heating.internal_ref', 'heating.co', 'heating.co_ref',
                                       'heating.cwu', 'heating.cwu_ref', 'heating.boiler',
                                       'heating.pump_circ', 'heating.pump_load',
                                       'heating.pump_co', 'heating.set_co_day', 
                                       'heating.set_co_day', 'heating.up', 'heating.mid',
                                       'irrigation.rainMinutes']) or {}  
            elif self.path == '/get/power/':
                s = self.server.saver.get(['power.l1v', 'power.l2v', 'power.l3v', 'power.l1w',
                                           'power.l2w', 'power.l3w', 'power.l1vif', 
                                           'power.l2vif', 'power.l3vif', 'power.l1va',
                                           'power.l2va', 'power.l3va', 'power.l1var',
                                           'power.l2var', 'power.l3var', 'power.l1hz',
                                           'power.l2hz', 'power.l3hz', 
                                           'power.consumption']) or {}
            elif self.path == '/get/alarm/':
                s = self.server.saver.get(['alarm.presence', 'alarm.mask', 'alarm.statii']) or {}
                
            elif self.path == '/get/irrigation/':
                s = self.server.saver.get(['irrigation.dailyCounter',
                                           'irrigation.sectionCounter',
                                           'irrigation.prevdayCounter',
                                           'irrigation.visStan',
                                           'irrigation.leakDetected',
                                           'irrigation.forbidDrop',
                                           'irrigation.forbidIrrig', 
                                           'irrigation.overrideS1',
                                           'irrigation.overrideS2',
                                           'irrigation.overrideS3',
                                           'irrigation.overrideS4',
                                           'irrigation.overrideS5',
                                           'irrigation.overrideS6',
                                           'irrigation.overrideNakr',
                                           'irrigation.rainMinutes',
                                           'irrigation.overrideKos',
                                           'irrigation.forbidKos']) or {}
            elif self.path == '/get/failures/':
                s = self.server.saver.get(['failures.water.leak.irrigation',
                                           'failures.power.fuse.l1',
                                           'failures.power.fuse.l2',
                                           'failures.power.fuse.l3',
                                           'failures.power.fuse.socks',
                                           'failures.power.fuse.12v',
                                           'failures.power.fuse.230v',
                                           'failures.alarm']) or {}
                is_fail = 0
                for val in s.itervalues():
                    is_fail = is_fail | val
                    
                s['failures.collective'] = is_fail
            else:
                s = {'error': 'unrecognized command'}
                
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            s = dict(((k.replace('.', '-'), v) for k, v in s.iteritems()))
            self.wfile.write(json.dumps(s))
                
                
    def __init__(self, tqm):
        BaseThread.__init__(self)
        self.tqm = tqm

    def run(self):
        httpd = BaseHTTPServer.HTTPServer(('', 8080), HttpServerThread.HTTPRequestHandler)
        httpd.reader = self.tqm.get_reader_for('httpserver')
        httpd.saver = self.tqm.get_interface_for('saver')
        httpd.serve_forever()
