#include <stdio.h>
#include <unistd.h>

#define ADDR_MIN   0x0000100000000000UL
#define ADDR_MASK  0x00000ffffffff000UL


void *shellcode()
{
    // 1. Find the secret in memory (starts with "OOO:")
    // 2. Print it
    // 3. ...
    // 4. PROFIT!

    printf("Hi! Soon I'll be your shellcode!\n");

    return (void*) 0x123456; // For this simplified test it's also OK to return the address
}
