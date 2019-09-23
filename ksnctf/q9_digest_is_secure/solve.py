# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
from hashlib import md5

url = 'http://ctfq.sweetduet.info:10080/~q9/flag.html'
headers = {
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.162 Safari/535.19',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'ja,en-US;q=0.8,en;q=0.6',
    'Accept-Charset': 'Shift_JIS,utf-8;q=0.7,*;q=0.3'
}
r = requests.get(url)

auth = r.headers['WWW-Authenticate']
m = re.match('Digest realm="(.*)", nonce="(.*)", algorithm=(.*), qop="(.*)"', auth)

realm = m.group(1)
nonce = m.group(2)
algorithm = m.group(3)
qop = m.group(4)
username = 'q9'
nc = '00000001'
cnonce = '9691c249745d94fc'
uri = '/~q9/flag.html'
a2 = 'GET:'+uri
a1_hash = 'c627e19450db746b739f41b64097d449'
a2_hash = md5(a2.encode('ascii')).hexdigest()

def md5_hash(text):
    return md5(text.encode('ascii')).hexdigest()

text = a1_hash + ':' + nonce + ':' + nc + ':' + cnonce + ':' + qop + ':' + a2_hash
response = md5_hash(text)
print('response: {}'.format(response))

headers['Authorization'] = 'Digest username="{}", realm="{}", nonce="{}", uri="{}", algorithm={}, response="{}", qop={}, nc={}, cnonce="{}"'.format(username, realm, nonce, uri, algorithm, response, qop, nc, cnonce)

r = requests.get(url, headers=headers)
print(r.text)
