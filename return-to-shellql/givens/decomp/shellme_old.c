typedef unsigned char   undefined;

typedef unsigned char    bool;
typedef unsigned char    byte;
typedef unsigned char    dwfenc;
typedef unsigned int    dword;
typedef unsigned long    qword;
typedef unsigned int    uint;
typedef unsigned long    ulong;
typedef unsigned char    undefined1;
typedef unsigned long    undefined8;
typedef unsigned short    word;
typedef struct eh_frame_hdr eh_frame_hdr, *Peh_frame_hdr;

struct eh_frame_hdr {
    byte eh_frame_hdr_version; // Exception Handler Frame Header Version
    dwfenc eh_frame_pointer_encoding; // Exception Handler Frame Pointer Encoding
    dwfenc eh_frame_desc_entry_count_encoding; // Encoding of # of Exception Handler FDEs
    dwfenc eh_frame_table_encoding; // Exception Handler Table Encoding
};

typedef struct fde_table_entry fde_table_entry, *Pfde_table_entry;

struct fde_table_entry {
    dword initial_loc; // Initial Location
    dword data_loc; // Data location
};

typedef ulong size_t;

typedef long __off_t;

typedef struct evp_pkey_ctx_st evp_pkey_ctx_st, *Pevp_pkey_ctx_st;

struct evp_pkey_ctx_st {
};

typedef struct evp_pkey_ctx_st EVP_PKEY_CTX;

typedef struct Value Value, *PValue;

struct Value { // PlaceHolder Class Structure
};

typedef struct Extension Extension, *PExtension;

struct Extension { // PlaceHolder Class Structure
};

typedef struct Argument Argument, *PArgument;

struct Argument { // PlaceHolder Class Structure
};

typedef struct _zval_struct _zval_struct, *P_zval_struct;

struct _zval_struct { // PlaceHolder Structure
};

typedef struct _zend_execute_data _zend_execute_data, *P_zend_execute_data;

struct _zend_execute_data { // PlaceHolder Structure
};

typedef struct Parameters Parameters, *PParameters;

struct Parameters { // PlaceHolder Structure
};

typedef struct Exception Exception, *PException;

struct Exception { // PlaceHolder Structure
};

typedef struct initializer_list initializer_list, *Pinitializer_list;

struct initializer_list { // PlaceHolder Structure
};

typedef enum Elf64_DynTag {
    DT_AUDIT=1879047932,
    DT_AUXILIARY=2147483645,
    DT_BIND_NOW=24,
    DT_CHECKSUM=1879047672,
    DT_CONFIG=1879047930,
    DT_DEBUG=21,
    DT_DEPAUDIT=1879047931,
    DT_ENCODING=32,
    DT_FEATURE_1=1879047676,
    DT_FILTER=2147483647,
    DT_FINI=13,
    DT_FINI_ARRAY=26,
    DT_FINI_ARRAYSZ=28,
    DT_FLAGS=30,
    DT_FLAGS_1=1879048187,
    DT_GNU_CONFLICT=1879047928,
    DT_GNU_CONFLICTSZ=1879047670,
    DT_GNU_HASH=1879047925,
    DT_GNU_LIBLIST=1879047929,
    DT_GNU_LIBLISTSZ=1879047671,
    DT_GNU_PRELINKED=1879047669,
    DT_HASH=4,
    DT_INIT=12,
    DT_INIT_ARRAY=25,
    DT_INIT_ARRAYSZ=27,
    DT_JMPREL=23,
    DT_MOVEENT=1879047674,
    DT_MOVESZ=1879047675,
    DT_MOVETAB=1879047934,
    DT_NEEDED=1,
    DT_NULL=0,
    DT_PLTGOT=3,
    DT_PLTPAD=1879047933,
    DT_PLTPADSZ=1879047673,
    DT_PLTREL=20,
    DT_PLTRELSZ=2,
    DT_POSFLAG_1=1879047677,
    DT_PREINIT_ARRAYSZ=33,
    DT_REL=17,
    DT_RELA=7,
    DT_RELACOUNT=1879048185,
    DT_RELAENT=9,
    DT_RELASZ=8,
    DT_RELCOUNT=1879048186,
    DT_RELENT=19,
    DT_RELSZ=18,
    DT_RPATH=15,
    DT_RUNPATH=29,
    DT_SONAME=14,
    DT_STRSZ=10,
    DT_STRTAB=5,
    DT_SYMBOLIC=16,
    DT_SYMENT=11,
    DT_SYMINENT=1879047679,
    DT_SYMINFO=1879047935,
    DT_SYMINSZ=1879047678,
    DT_SYMTAB=6,
    DT_TEXTREL=22,
    DT_TLSDESC_GOT=1879047927,
    DT_TLSDESC_PLT=1879047926,
    DT_VERDEF=1879048188,
    DT_VERDEFNUM=1879048189,
    DT_VERNEED=1879048190,
    DT_VERNEEDNUM=1879048191,
    DT_VERSYM=1879048176
} Elf64_DynTag;

typedef enum Elf_ProgramHeaderType {
    PT_DYNAMIC=2,
    PT_GNU_EH_FRAME=1685382480,
    PT_GNU_RELRO=1685382482,
    PT_GNU_STACK=1685382481,
    PT_INTERP=3,
    PT_LOAD=1,
    PT_NOTE=4,
    PT_NULL=0,
    PT_PHDR=6,
    PT_SHLIB=5,
    PT_TLS=7
} Elf_ProgramHeaderType;

typedef struct Elf64_Shdr Elf64_Shdr, *PElf64_Shdr;

typedef enum Elf_SectionHeaderType {
    SHT_CHECKSUM=1879048184,
    SHT_DYNAMIC=6,
    SHT_DYNSYM=11,
    SHT_FINI_ARRAY=15,
    SHT_GNU_ATTRIBUTES=1879048181,
    SHT_GNU_HASH=1879048182,
    SHT_GNU_LIBLIST=1879048183,
    SHT_GNU_verdef=1879048189,
    SHT_GNU_verneed=1879048190,
    SHT_GNU_versym=1879048191,
    SHT_GROUP=17,
    SHT_HASH=5,
    SHT_INIT_ARRAY=14,
    SHT_NOBITS=8,
    SHT_NOTE=7,
    SHT_NULL=0,
    SHT_PREINIT_ARRAY=16,
    SHT_PROGBITS=1,
    SHT_REL=9,
    SHT_RELA=4,
    SHT_SHLIB=10,
    SHT_STRTAB=3,
    SHT_SUNW_COMDAT=1879048187,
    SHT_SUNW_move=1879048186,
    SHT_SUNW_syminfo=1879048188,
    SHT_SYMTAB=2,
    SHT_SYMTAB_SHNDX=18
} Elf_SectionHeaderType;

struct Elf64_Shdr {
    dword sh_name;
    enum Elf_SectionHeaderType sh_type;
    qword sh_flags;
    qword sh_addr;
    qword sh_offset;
    qword sh_size;
    dword sh_link;
    dword sh_info;
    qword sh_addralign;
    qword sh_entsize;
};

typedef struct Elf64_Dyn Elf64_Dyn, *PElf64_Dyn;

struct Elf64_Dyn {
    enum Elf64_DynTag d_tag;
    qword d_val;
};

typedef struct Elf64_Phdr Elf64_Phdr, *PElf64_Phdr;

struct Elf64_Phdr {
    enum Elf_ProgramHeaderType p_type;
    dword p_flags;
    qword p_offset;
    qword p_vaddr;
    qword p_paddr;
    qword p_filesz;
    qword p_memsz;
    qword p_align;
};

typedef struct Elf64_Rela Elf64_Rela, *PElf64_Rela;

struct Elf64_Rela {
    qword r_offset; // location to apply the relocation action
    qword r_info; // the symbol table index and the type of relocation
    qword r_addend; // a constant addend used to compute the relocatable field value
};

typedef struct Elf64_Sym Elf64_Sym, *PElf64_Sym;

struct Elf64_Sym {
    dword st_name;
    byte st_info;
    byte st_other;
    word st_shndx;
    qword st_value;
    qword st_size;
};

typedef struct Elf64_Ehdr Elf64_Ehdr, *PElf64_Ehdr;

struct Elf64_Ehdr {
    byte e_ident_magic_num;
    char e_ident_magic_str[3];
    byte e_ident_class;
    byte e_ident_data;
    byte e_ident_version;
    byte e_ident_pad[9];
    word e_type;
    word e_machine;
    dword e_version;
    qword e_entry;
    qword e_phoff;
    qword e_shoff;
    dword e_flags;
    word e_ehsize;
    word e_phentsize;
    word e_phnum;
    word e_shentsize;
    word e_shnum;
    word e_shstrndx;
};




int _init(EVP_PKEY_CTX *ctx)

{
  int iVar1;
  
  iVar1 = __gmon_start__();
  return iVar1;
}



void FUN_00101260(void)

{
                    // WARNING: Treating indirect jump as call
  (*(code *)(undefined *)0x0)();
  return;
}



void __thiscall _Value(Value *this)

{
  _Value(this);
  return;
}



// WARNING: Unknown calling convention yet parameter storage is locked

void parameters(_zend_execute_data *param_1)

{
  parameters(param_1);
  return;
}



// WARNING: Unknown calling convention yet parameter storage is locked

void yield(_zval_struct *param_1,Value *param_2)

{
  yield(param_1,param_2);
  return;
}



void __cxa_begin_catch(void)

{
  __cxa_begin_catch();
  return;
}



void __cxa_finalize(void)

{
  __cxa_finalize();
  return;
}



// WARNING: Unknown calling convention yet parameter storage is locked

size_t strlen(char *__s)

{
  size_t sVar1;
  
  sVar1 = strlen(__s);
  return sVar1;
}



// WARNING: Unknown calling convention yet parameter storage is locked

void stringValue_abi_cxx11_(void)

{
  stringValue_abi_cxx11_();
  return;
}



// WARNING: Unknown calling convention yet parameter storage is locked

void add(char *param_1,FuncDef1 *param_2,initializer_list *param_3)

{
  add(param_1,param_2,param_3);
  return;
}



void __cxa_guard_abort(void)

{
  __cxa_guard_abort();
  return;
}



void __cxa_guard_release(void)

{
  __cxa_guard_release();
  return;
}



void shell_this(char *pcParm1)

{
  size_t sVar1;
  code *UNRECOVERED_JUMPTABLE;
  
  sVar1 = strlen(pcParm1);
  UNRECOVERED_JUMPTABLE = (code *)mmap((void *)0x0,(long)(int)sVar1,7,0x22,-1,0);
  memcpy(UNRECOVERED_JUMPTABLE,pcParm1,(long)(int)sVar1);
  alarm(0x1e);
  prctl(0x16,1);
                    // WARNING: Could not recover jumptable at 0x001014af. Too many branches
                    // WARNING: Treating indirect jump as call
  (*UNRECOVERED_JUMPTABLE)();
  return;
}



// WARNING: Unknown calling convention yet parameter storage is locked

void * memcpy(void *__dest,void *__src,size_t __n)

{
  void *pvVar1;
  
  pvVar1 = memcpy(__dest,__src,__n);
  return pvVar1;
}



void __cxa_atexit(void)

{
  __cxa_atexit();
  return;
}



// WARNING: Unknown calling convention yet parameter storage is locked

void module(void)

{
  module();
  return;
}



// WARNING: Unknown calling convention yet parameter storage is locked

void operator_delete(void *param_1)

{
  operator_delete(param_1);
  return;
}



void __stack_chk_fail(void)

{
                    // WARNING: Subroutine does not return
  __stack_chk_fail();
}



Parameters * shellme(Parameters *param_1)

{
  long in_FS_OFFSET;
  undefined *puStack72;
  undefined auStack56 [24];
  long lStack32;
  
  lStack32 = *(long *)(in_FS_OFFSET + 0x28);
  stringValue_abi_cxx11_();
  shell_this(puStack72);
  Value((Value *)param_1,true);
  if (puStack72 != auStack56) {
    operator_delete(puStack72);
  }
  if (lStack32 != *(long *)(in_FS_OFFSET + 0x28)) {
                    // WARNING: Subroutine does not return
    __stack_chk_fail();
  }
  return param_1;
}



// WARNING: Unknown calling convention yet parameter storage is locked

int prctl(int __option,...)

{
  int iVar1;
  
  iVar1 = prctl(__option);
  return iVar1;
}



// WARNING: Unknown calling convention yet parameter storage is locked

void handle(Exception *param_1)

{
  handle(param_1);
  return;
}



void __thiscall Value(Value *this,bool param_1)

{
  Value(this,param_1);
  return;
}



void __thiscall Extension(Extension *this,char *param_1,char *param_2,int param_3)

{
  Extension(this,param_1,param_2,param_3);
  return;
}



// WARNING: Unknown calling convention yet parameter storage is locked

void valid(_zend_execute_data *param_1,_zval_struct *param_2)

{
  valid(param_1,param_2);
  return;
}



void __cxa_end_catch(void)

{
  __cxa_end_catch();
  return;
}



void _Unwind_Resume(void)

{
                    // WARNING: Subroutine does not return
  _Unwind_Resume();
}



// WARNING: Unknown calling convention yet parameter storage is locked

void * mmap(void *__addr,size_t __len,int __prot,int __flags,int __fd,__off_t __offset)

{
  void *pvVar1;
  
  pvVar1 = mmap(__addr,__len,__prot,__flags,__fd,__offset);
  return pvVar1;
}



void __cxa_guard_acquire(void)

{
  __cxa_guard_acquire();
  return;
}



void __gmon_start__(void)

{
  __gmon_start__();
  return;
}



// WARNING: Unknown calling convention yet parameter storage is locked

uint alarm(uint __seconds)

{
  uint uVar1;
  
  uVar1 = alarm(__seconds);
  return uVar1;
}



// WARNING: Removing unreachable block (ram,0x0010136b)
// WARNING: Removing unreachable block (ram,0x00101377)

void deregister_tm_clones(void)

{
  return;
}



// WARNING: Removing unreachable block (ram,0x001013b8)
// WARNING: Removing unreachable block (ram,0x001013c4)

void register_tm_clones(void)

{
  return;
}



void __do_global_dtors_aux(void)

{
  if (completed_7594 == 0) {
    __cxa_finalize(__dso_handle);
    deregister_tm_clones();
    completed_7594 = 1;
  }
  return;
}



void frame_dummy(void)

{
  if (__JCR_END__ == 0) {
    register_tm_clones();
    return;
  }
  _Jv_RegisterClasses();
  register_tm_clones();
  return;
}



void shell_this(char *pcParm1)

{
  size_t sVar1;
  code *UNRECOVERED_JUMPTABLE;
  
  sVar1 = strlen(pcParm1);
  UNRECOVERED_JUMPTABLE = (code *)mmap((void *)0x0,(long)(int)sVar1,7,0x22,-1,0);
  memcpy(UNRECOVERED_JUMPTABLE,pcParm1,(long)(int)sVar1);
  alarm(0x1e);
  prctl(0x16,1);
                    // WARNING: Could not recover jumptable at 0x001014af. Too many branches
                    // WARNING: Treating indirect jump as call
  (*UNRECOVERED_JUMPTABLE)();
  return;
}



// shellme(Php::Parameters&)

Parameters * shellme(Parameters *param_1)

{
  long in_FS_OFFSET;
  undefined *local_48;
  undefined auStack56 [24];
  long local_20;
  
  local_20 = *(long *)(in_FS_OFFSET + 0x28);
  stringValue_abi_cxx11_();
                    // try { // try from 001014eb to 001014fc has its CatchHandler @ 0010152e
  shell_this(local_48);
  Value((Value *)param_1,true);
  if (local_48 != auStack56) {
    operator_delete(local_48);
  }
  if (local_20 == *(long *)(in_FS_OFFSET + 0x28)) {
    return param_1;
  }
                    // WARNING: Subroutine does not return
  __stack_chk_fail();
}



void get_module(void)

{
  undefined1 myExtension [144];
  undefined8 myExtension;
  int iVar1;
  
  if ((char)myExtension == 0) {
    iVar1 = __cxa_guard_acquire(0x3020d0);
    if (iVar1 != 0) {
                    // try { // try from 0010160a to 0010160e has its CatchHandler @ 0010163a
      Extension((Extension *)0x302040,"shellme","1.0",0x133776e);
      __cxa_guard_release(0x3020d0);
      __cxa_atexit(_Extension,0x302040,&__dso_handle);
    }
  }
  add((undefined1 *)&ram0x00302040,(FuncDef1 *)"shellme",
      (initializer_list *)invoke___shellme_Php__Parameters____);
  module();
  return;
}



// Php::Argument::~Argument()

void __thiscall _Argument(Argument *this)

{
  return;
}



// WARNING: Unknown calling convention yet parameter storage is locked

void _ZN3Php8ArgumentD0Ev(void *param_1)

{
  operator_delete(param_1);
  return;
}



// void Php::ZendCallable::invoke<&(shellme(Php::Parameters&))>(_zend_execute_data*, _zval_struct*)

void invoke___shellme_Php__Parameters____(_zend_execute_data *param_1,_zval_struct *param_2)

{
  code **ppcVar1;
  code **ppcVar2;
  char cVar3;
  long in_FS_OFFSET;
  code **local_68;
  code **local_60;
  Parameters local_48 [40];
  long local_20;
  
  local_20 = *(long *)(in_FS_OFFSET + 0x28);
  cVar3 = valid(param_1,param_2);
  if (cVar3 != 0) {
    parameters((_zend_execute_data *)&local_68);
                    // try { // try from 001016d6 to 001016da has its CatchHandler @ 00101729
    shellme(local_48);
                    // try { // try from 001016e1 to 001016e5 has its CatchHandler @ 0010172b
    yield(param_2,(Value *)local_48);
    _Value((Value *)local_48);
    ppcVar1 = local_68;
    ppcVar2 = local_60;
    while (local_60 != ppcVar1) {
      (**(code **)*ppcVar1)(ppcVar1);
      ppcVar1 = ppcVar1 + 4;
      ppcVar2 = local_68;
    }
    if (ppcVar2 != (code **)0x0) {
      operator_delete(ppcVar2);
    }
  }
  if (local_20 == *(long *)(in_FS_OFFSET + 0x28)) {
    return;
  }
                    // WARNING: Subroutine does not return
  __stack_chk_fail();
}



void _fini(void)

{
  return;
}


