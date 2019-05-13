In this challenge, `know_your_mem.c` is the meat.

However, remember that timeouts are strict -- it's suggested to first try locally in C.

Basically:

  # First solve it in 'standard' C without triggering alarm()
  sudo apt install libseccomp-dev libseccomp2
  edit simplified_shellcode.so.c
  make check

  # Switch syscalls to Google's linux_syscall_support
  edit shellcode.c
  make check

  # If all goes well, shellcode.bin.pkt will be ready to submit as-is!

Solution:
  We need a way of searching memory for the target string. We are unable to
  install a segfault handler, and thus need another way of checking an address.
  We used a two step approach. First, we mmap a large range (1<<14 pages), and
  check if it's at the requested address. If it is, we try the next one. If not,
  there is a page mapped in there already. We reduce the size of our mmap, and
  try again. When we get to a small number of pages, we try mprotect on each
  page. It's unclear right now why mmap does not work on single pages.
