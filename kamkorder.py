import random, urllib2, threading, time, base64
import os, collections, ctypes, sys, datetime, shutil

CAMPATH = 'E:\\kamery\\'

CAMERAS = {

    'front': {
        'url': 'http://127.0.0.1:12000/~',
        'randstr': '~',
    },

    'mimo': {
        'url': 'http://127.0.0.1:13000/~',
        'randstr': '~',
    },

    'taras': {
        'url': 'http://10.0.0.209/snapshot.cgi?user=admin&pwd=x&~',
        'randstr': '~',
    },

    'ogrod': {
        'url': 'http://10.0.0.207/snapshot.cgi?user=admin&pwd=x&~',
        'randstr': '~',
    },

    'parking': {
        'url': 'http://10.0.0.208/snapshot.cgi?user=admin&pwd=x&~',
        'randstr': '~',        
    },

    'duzypokoj': {
        'url': 'http://10.0.0.214:8080/shot.jpg?rnd=~',
        'randstr': '~',
        'auth_login': 'admin',
        'auth_password': 'x',
    },

    'kuchnia': {
        'url': 'http://10.0.0.213/image.jpeg?~',
        'randstr': '~',
        'auth_login': '',
        'auth_password': 'x',        
    }
}

class CameraGetter(object):
    def __init__(self, name, rec):
        """@param rec: a record from config file"""
        self.name = name
        self.url = rec['url']
        if 'randstr' in rec:
            self.randstr = '~'
        else:
            self.randstr = '\x00'
        if 'auth_login' in rec:
            self.headers = {'Authorization': 
                            'Basic '+base64.b64encode(rec['auth_login']+':'+rec['auth_password'])}
        else:
            self.headers = {}
            
            
    def get_url(self):
        return self.url.replace(self.randstr, str(random.randint(0, 1000000000)))
    
    def get_image(self):
        u = urllib2.Request(self.get_url(), None, self.headers)
        try:
            img = urllib2.urlopen(u).read()
        except:
            raise ValueError, 'Error happened'
        return img

def disk_usage(path):
    _, total, free = ctypes.c_ulonglong(), ctypes.c_ulonglong(), \
                       ctypes.c_ulonglong()
    if sys.version_info >= (3,) or isinstance(path, unicode):
        fun = ctypes.windll.kernel32.GetDiskFreeSpaceExW
    else:
        fun = ctypes.windll.kernel32.GetDiskFreeSpaceExA
    ret = fun(path, ctypes.byref(_), ctypes.byref(total), ctypes.byref(free))
    if ret == 0:
        raise ctypes.WinError()
    return free.value

FREE_SPACE_REQUIRED = 50        # in megabytes


class DirectoryNukingThread(threading.Thread):
    def __init__(self, directory):
        threading.Thread.__init__(self)
        self.directory = directory
        
    def run(self):
        shutil.rmtree(self.directory)

class CameraThread(threading.Thread):
    def __init__(self, camera):
        threading.Thread.__init__(self)
        self.camera = camera # CameraGetter
        self.cpath = '%s%s' % (CAMPATH, camera.name)
        try:
            os.mkdir(self.cpath)
        except OSError:
            pass        
        
    def run(self):
        while True:
            try:
                img = self.camera.get_image()
            except ValueError:
                time.sleep(5)
                continue
                
            # check disk space
            if disk_usage(CAMPATH) < FREE_SPACE_REQUIRED * 1024 * 1024:
                files = sorted(os.listdir(self.cpath))
                DirectoryNukingThread(files[0]).start()
                time.sleep(5)

            while True:
                dt = datetime.datetime.now()
                dirname = dt.strftime("%Y-%m-%d")
                dirname = '%s\\%s' % (self.cpath, dirname)
                filname = dt.strftime("%H-%M-%S") + '.jpg'
                filname = '%s\\%s.jpg' % (dirname, filname)
                
                if not os.path.exists(dirname): os.mkdir(dirname)                    
                if not os.path.exists(filname): break

                time.sleep(0.3)
            
            with open(filname, 'wb') as out:
                out.write(img)

try:                
    os.mkdir(CAMPATH)
except OSError:
    pass

for name, rec in CAMERAS.iteritems():
    CameraThread(CameraGetter(name, rec)).start()