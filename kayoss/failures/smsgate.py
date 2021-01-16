# coding=UTF-8
import urllib
from hashlib import sha1
import unicodedata
import httplib, urllib

def send_sms(target, content):

    target = target.strip()
    content = content.strip()

    content = content.replace(u'ł', 'l').replace(u'Ł', 'L') # because normalize NFD sucks at this char
    
    content = unicodedata.normalize('NFD', content).encode('ascii', 'ignore')

    if len(target) == 9:
        target = '48'+target
    
    conn = httplib.HTTPSConnection('api1.multiinfo.plus.pl', '443', cert_file="C:\\kayoss\\failures\\key.pem")
    
    data = urllib.urlencode({
                       'login': "READY",
                        'password': "STEADY",
                        'serviceId': "GO",
                        'text': content,
                        'dest': target,
                        'orig': "LIMUZINA"
                    })
    
    conn.request('GET', '/sendsms.aspx?'+data)
    conn.getresponse()
 