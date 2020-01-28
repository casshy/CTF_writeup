# readelf

ELFファイルの情報を表示する

## サンプルソースコード
test.c
````c
#include <stdio.h>

int main() {
  int hoge = 10;
  char fuga[] = "Hello, gdb!";
  printf("%s\n", fuga);
}
`````
````bash
gcc test.c -o test
````

## ヘッダを表示

- [ELFヘッダ(-h)](#ELFヘッダ-h)
- [プログラムヘッダ(-l)](#プログラムヘッダ-l)
- [セクションヘッダ(-S)](#セクションヘッダ-s)
- シンボルテーブル(-s)
- 動的シンボルテーブル(--dyn-syms)
- リロケーション情報(-r)
- 動的セクション(-d)

### ELFヘッダ(-h)
````
$ readelf -h test
ELF Header:
  Magic:   7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00
  Class:                             ELF64
  Data:                              2's complement, little endian
  Version:                           1 (current)
  OS/ABI:                            UNIX - System V
  ABI Version:                       0
  Type:                              DYN (Shared object file)
  Machine:                           Advanced Micro Devices X86-64
  Version:                           0x1
  Entry point address:               0x5a0
  Start of program headers:          64 (bytes into file)
  Start of section headers:          6496 (bytes into file)
  Flags:                             0x0
  Size of this header:               64 (bytes)
  Size of program headers:           56 (bytes)
  Number of program headers:         9
  Size of section headers:           64 (bytes)
  Number of section headers:         29
  Section header string table index: 28
````
### プログラムヘッダ(-l)
````
$ readelf -l -W test

Elf file type is DYN (Shared object file)
Entry point 0x5a0
There are 9 program headers, starting at offset 64

Program Headers:
  Type           Offset   VirtAddr           PhysAddr           FileSiz  MemSiz   Flg Align
  PHDR           0x000040 0x0000000000000040 0x0000000000000040 0x0001f8 0x0001f8 R   0x8
  INTERP         0x000238 0x0000000000000238 0x0000000000000238 0x00001c 0x00001c R   0x1
      [Requesting program interpreter: /lib64/ld-linux-x86-64.so.2]
  LOAD           0x000000 0x0000000000000000 0x0000000000000000 0x0008d8 0x0008d8 R E 0x200000
  LOAD           0x000db0 0x0000000000200db0 0x0000000000200db0 0x000260 0x000268 RW  0x200000
  DYNAMIC        0x000dc0 0x0000000000200dc0 0x0000000000200dc0 0x0001f0 0x0001f0 RW  0x8
  NOTE           0x000254 0x0000000000000254 0x0000000000000254 0x000044 0x000044 R   0x4
  GNU_EH_FRAME   0x000794 0x0000000000000794 0x0000000000000794 0x00003c 0x00003c R   0x4
  GNU_STACK      0x000000 0x0000000000000000 0x0000000000000000 0x000000 0x000000 RW  0x10
  GNU_RELRO      0x000db0 0x0000000000200db0 0x0000000000200db0 0x000250 0x000250 R   0x1

 Section to Segment mapping:
  Segment Sections...
   00     
   01     .interp
   02     .interp .note.ABI-tag .note.gnu.build-id .gnu.hash .dynsym .dynstr .gnu.version .gnu.version_r .rela.dyn .rela.plt .init .plt .plt.got .text .fini .rodata .eh_frame_hdr .eh_frame
   03     .init_array .fini_array .dynamic .got .data .bss
   04     .dynamic
   05     .note.ABI-tag .note.gnu.build-id
   06     .eh_frame_hdr
   07     
   08     .init_array .fini_array .dynamic .got
````

### セクションヘッダ(-S)
````
$ readelf -S -W test
There are 29 section headers, starting at offset 0x1960:

Section Headers:
  [Nr] Name              Type            Address          Off    Size   ES Flg Lk Inf Al
  [ 0]                   NULL            0000000000000000 000000 000000 00      0   0  0
  [ 1] .interp           PROGBITS        0000000000000238 000238 00001c 00   A  0   0  1
  [ 2] .note.ABI-tag     NOTE            0000000000000254 000254 000020 00   A  0   0  4
  [ 3] .note.gnu.build-id NOTE            0000000000000274 000274 000024 00   A  0   0  4
  [ 4] .gnu.hash         GNU_HASH        0000000000000298 000298 00001c 00   A  5   0  8
  [ 5] .dynsym           DYNSYM          00000000000002b8 0002b8 0000c0 18   A  6   1  8
  [ 6] .dynstr           STRTAB          0000000000000378 000378 00009d 00   A  0   0  1
  [ 7] .gnu.version      VERSYM          0000000000000416 000416 000010 02   A  5   0  2
  [ 8] .gnu.version_r    VERNEED         0000000000000428 000428 000030 00   A  6   1  8
  [ 9] .rela.dyn         RELA            0000000000000458 000458 0000c0 18   A  5   0  8
  [10] .rela.plt         RELA            0000000000000518 000518 000030 18  AI  5  22  8
  [11] .init             PROGBITS        0000000000000548 000548 000017 00  AX  0   0  4
  [12] .plt              PROGBITS        0000000000000560 000560 000030 10  AX  0   0 16
  [13] .plt.got          PROGBITS        0000000000000590 000590 000008 08  AX  0   0  8
  [14] .text             PROGBITS        00000000000005a0 0005a0 0001e2 00  AX  0   0 16
  [15] .fini             PROGBITS        0000000000000784 000784 000009 00  AX  0   0  4
  [16] .rodata           PROGBITS        0000000000000790 000790 000004 04  AM  0   0  4
  [17] .eh_frame_hdr     PROGBITS        0000000000000794 000794 00003c 00   A  0   0  4
  [18] .eh_frame         PROGBITS        00000000000007d0 0007d0 000108 00   A  0   0  8
  [19] .init_array       INIT_ARRAY      0000000000200db0 000db0 000008 08  WA  0   0  8
  [20] .fini_array       FINI_ARRAY      0000000000200db8 000db8 000008 08  WA  0   0  8
  [21] .dynamic          DYNAMIC         0000000000200dc0 000dc0 0001f0 10  WA  6   0  8
  [22] .got              PROGBITS        0000000000200fb0 000fb0 000050 08  WA  0   0  8
  [23] .data             PROGBITS        0000000000201000 001000 000010 00  WA  0   0  8
  [24] .bss              NOBITS          0000000000201010 001010 000008 00  WA  0   0  1
  [25] .comment          PROGBITS        0000000000000000 001010 00002b 01  MS  0   0  1
  [26] .symtab           SYMTAB          0000000000000000 001040 000600 18     27  43  8
  [27] .strtab           STRTAB          0000000000000000 001640 00021e 00      0   0  1
  [28] .shstrtab         STRTAB          0000000000000000 00185e 0000fe 00      0   0  1
Key to Flags:
  W (write), A (alloc), X (execute), M (merge), S (strings), I (info),
  L (link order), O (extra OS processing required), G (group), T (TLS),
  C (compressed), x (unknown), o (OS specific), E (exclude),
  l (large), p (processor specific)
````

### シンボルテーブル(-s)
````
$ readelf -s -W test

Symbol table '.dynsym' contains 8 entries:
   Num:    Value          Size Type    Bind   Vis      Ndx Name
     0: 0000000000000000     0 NOTYPE  LOCAL  DEFAULT  UND
     1: 0000000000000000     0 NOTYPE  WEAK   DEFAULT  UND _ITM_deregisterTMCloneTable
     2: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND puts@GLIBC_2.2.5 (2)
     3: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND __stack_chk_fail@GLIBC_2.4 (3)
     4: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND __libc_start_main@GLIBC_2.2.5 (2)
     5: 0000000000000000     0 NOTYPE  WEAK   DEFAULT  UND __gmon_start__
     6: 0000000000000000     0 NOTYPE  WEAK   DEFAULT  UND _ITM_registerTMCloneTable
     7: 0000000000000000     0 FUNC    WEAK   DEFAULT  UND __cxa_finalize@GLIBC_2.2.5 (2)

Symbol table '.symtab' contains 64 entries:
   Num:    Value          Size Type    Bind   Vis      Ndx Name
     0: 0000000000000000     0 NOTYPE  LOCAL  DEFAULT  UND
     1: 0000000000000238     0 SECTION LOCAL  DEFAULT    1
     2: 0000000000000254     0 SECTION LOCAL  DEFAULT    2
     3: 0000000000000274     0 SECTION LOCAL  DEFAULT    3
     4: 0000000000000298     0 SECTION LOCAL  DEFAULT    4
     5: 00000000000002b8     0 SECTION LOCAL  DEFAULT    5
     6: 0000000000000378     0 SECTION LOCAL  DEFAULT    6
     7: 0000000000000416     0 SECTION LOCAL  DEFAULT    7
     8: 0000000000000428     0 SECTION LOCAL  DEFAULT    8
     9: 0000000000000458     0 SECTION LOCAL  DEFAULT    9
    10: 0000000000000518     0 SECTION LOCAL  DEFAULT   10
    11: 0000000000000548     0 SECTION LOCAL  DEFAULT   11
    12: 0000000000000560     0 SECTION LOCAL  DEFAULT   12
    13: 0000000000000590     0 SECTION LOCAL  DEFAULT   13
    14: 00000000000005a0     0 SECTION LOCAL  DEFAULT   14
    15: 0000000000000784     0 SECTION LOCAL  DEFAULT   15
    16: 0000000000000790     0 SECTION LOCAL  DEFAULT   16
    17: 0000000000000794     0 SECTION LOCAL  DEFAULT   17
    18: 00000000000007d0     0 SECTION LOCAL  DEFAULT   18
    19: 0000000000200db0     0 SECTION LOCAL  DEFAULT   19
    20: 0000000000200db8     0 SECTION LOCAL  DEFAULT   20
    21: 0000000000200dc0     0 SECTION LOCAL  DEFAULT   21
    22: 0000000000200fb0     0 SECTION LOCAL  DEFAULT   22
    23: 0000000000201000     0 SECTION LOCAL  DEFAULT   23
    24: 0000000000201010     0 SECTION LOCAL  DEFAULT   24
    25: 0000000000000000     0 SECTION LOCAL  DEFAULT   25
    26: 0000000000000000     0 FILE    LOCAL  DEFAULT  ABS crtstuff.c
    27: 00000000000005d0     0 FUNC    LOCAL  DEFAULT   14 deregister_tm_clones
    28: 0000000000000610     0 FUNC    LOCAL  DEFAULT   14 register_tm_clones
    29: 0000000000000660     0 FUNC    LOCAL  DEFAULT   14 __do_global_dtors_aux
    30: 0000000000201010     1 OBJECT  LOCAL  DEFAULT   24 completed.7697
    31: 0000000000200db8     0 OBJECT  LOCAL  DEFAULT   20 __do_global_dtors_aux_fini_array_entry
    32: 00000000000006a0     0 FUNC    LOCAL  DEFAULT   14 frame_dummy
    33: 0000000000200db0     0 OBJECT  LOCAL  DEFAULT   19 __frame_dummy_init_array_entry
    34: 0000000000000000     0 FILE    LOCAL  DEFAULT  ABS test.c
    35: 0000000000000000     0 FILE    LOCAL  DEFAULT  ABS crtstuff.c
    36: 00000000000008d4     0 OBJECT  LOCAL  DEFAULT   18 __FRAME_END__
    37: 0000000000000000     0 FILE    LOCAL  DEFAULT  ABS
    38: 0000000000200db8     0 NOTYPE  LOCAL  DEFAULT   19 __init_array_end
    39: 0000000000200dc0     0 OBJECT  LOCAL  DEFAULT   21 _DYNAMIC
    40: 0000000000200db0     0 NOTYPE  LOCAL  DEFAULT   19 __init_array_start
    41: 0000000000000794     0 NOTYPE  LOCAL  DEFAULT   17 __GNU_EH_FRAME_HDR
    42: 0000000000200fb0     0 OBJECT  LOCAL  DEFAULT   22 _GLOBAL_OFFSET_TABLE_
    43: 0000000000000780     2 FUNC    GLOBAL DEFAULT   14 __libc_csu_fini
    44: 0000000000000000     0 NOTYPE  WEAK   DEFAULT  UND _ITM_deregisterTMCloneTable
    45: 0000000000201000     0 NOTYPE  WEAK   DEFAULT   23 data_start
    46: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND puts@@GLIBC_2.2.5
    47: 0000000000201010     0 NOTYPE  GLOBAL DEFAULT   23 _edata
    48: 0000000000000784     0 FUNC    GLOBAL DEFAULT   15 _fini
    49: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND __stack_chk_fail@@GLIBC_2.4
    50: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND __libc_start_main@@GLIBC_2.2.5
    51: 0000000000201000     0 NOTYPE  GLOBAL DEFAULT   23 __data_start
    52: 0000000000000000     0 NOTYPE  WEAK   DEFAULT  UND __gmon_start__
    53: 0000000000201008     0 OBJECT  GLOBAL HIDDEN    23 __dso_handle
    54: 0000000000000790     4 OBJECT  GLOBAL DEFAULT   16 _IO_stdin_used
    55: 0000000000000710   101 FUNC    GLOBAL DEFAULT   14 __libc_csu_init
    56: 0000000000201018     0 NOTYPE  GLOBAL DEFAULT   24 _end
    57: 00000000000005a0    43 FUNC    GLOBAL DEFAULT   14 _start
    58: 0000000000201010     0 NOTYPE  GLOBAL DEFAULT   24 __bss_start
    59: 00000000000006aa    90 FUNC    GLOBAL DEFAULT   14 main
    60: 0000000000201010     0 OBJECT  GLOBAL HIDDEN    23 __TMC_END__
    61: 0000000000000000     0 NOTYPE  WEAK   DEFAULT  UND _ITM_registerTMCloneTable
    62: 0000000000000000     0 FUNC    WEAK   DEFAULT  UND __cxa_finalize@@GLIBC_2.2.5
    63: 0000000000000548     0 FUNC    GLOBAL DEFAULT   11 _init
````

### 動的シンボルテーブル(--dyn-syms)
````
$ readelf --dyn-syms -W test

Symbol table '.dynsym' contains 8 entries:
   Num:    Value          Size Type    Bind   Vis      Ndx Name
     0: 0000000000000000     0 NOTYPE  LOCAL  DEFAULT  UND
     1: 0000000000000000     0 NOTYPE  WEAK   DEFAULT  UND _ITM_deregisterTMCloneTable
     2: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND puts@GLIBC_2.2.5 (2)
     3: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND __stack_chk_fail@GLIBC_2.4 (3)
     4: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND __libc_start_main@GLIBC_2.2.5 (2)
     5: 0000000000000000     0 NOTYPE  WEAK   DEFAULT  UND __gmon_start__
     6: 0000000000000000     0 NOTYPE  WEAK   DEFAULT  UND _ITM_registerTMCloneTable
     7: 0000000000000000     0 FUNC    WEAK   DEFAULT  UND __cxa_finalize@GLIBC_2.2.5 (2)
````

### リロケーション情報(-r)
````
$ readelf -r -W test

Relocation section '.rela.dyn' at offset 0x458 contains 8 entries:
    Offset             Info             Type               Symbol's Value  Symbol's Name + Addend
0000000000200db0  0000000000000008 R_X86_64_RELATIVE                         6a0
0000000000200db8  0000000000000008 R_X86_64_RELATIVE                         660
0000000000201008  0000000000000008 R_X86_64_RELATIVE                         201008
0000000000200fd8  0000000100000006 R_X86_64_GLOB_DAT      0000000000000000 _ITM_deregisterTMCloneTable + 0
0000000000200fe0  0000000400000006 R_X86_64_GLOB_DAT      0000000000000000 __libc_start_main@GLIBC_2.2.5 + 0
0000000000200fe8  0000000500000006 R_X86_64_GLOB_DAT      0000000000000000 __gmon_start__ + 0
0000000000200ff0  0000000600000006 R_X86_64_GLOB_DAT      0000000000000000 _ITM_registerTMCloneTable + 0
0000000000200ff8  0000000700000006 R_X86_64_GLOB_DAT      0000000000000000 __cxa_finalize@GLIBC_2.2.5 + 0

Relocation section '.rela.plt' at offset 0x518 contains 2 entries:
    Offset             Info             Type               Symbol's Value  Symbol's Name + Addend
0000000000200fc8  0000000200000007 R_X86_64_JUMP_SLOT     0000000000000000 puts@GLIBC_2.2.5 + 0
0000000000200fd0  0000000300000007 R_X86_64_JUMP_SLOT     0000000000000000 __stack_chk_fail@GLIBC_2.4 + 0
````

### 動的セクション(-d)
````
$ readelf -d -W test

Dynamic section at offset 0xdc0 contains 27 entries:
  Tag        Type                         Name/Value
 0x0000000000000001 (NEEDED)             Shared library: [libc.so.6]
 0x000000000000000c (INIT)               0x548
 0x000000000000000d (FINI)               0x784
 0x0000000000000019 (INIT_ARRAY)         0x200db0
 0x000000000000001b (INIT_ARRAYSZ)       8 (bytes)
 0x000000000000001a (FINI_ARRAY)         0x200db8
 0x000000000000001c (FINI_ARRAYSZ)       8 (bytes)
 0x000000006ffffef5 (GNU_HASH)           0x298
 0x0000000000000005 (STRTAB)             0x378
 0x0000000000000006 (SYMTAB)             0x2b8
 0x000000000000000a (STRSZ)              157 (bytes)
 0x000000000000000b (SYMENT)             24 (bytes)
 0x0000000000000015 (DEBUG)              0x0
 0x0000000000000003 (PLTGOT)             0x200fb0
 0x0000000000000002 (PLTRELSZ)           48 (bytes)
 0x0000000000000014 (PLTREL)             RELA
 0x0000000000000017 (JMPREL)             0x518
 0x0000000000000007 (RELA)               0x458
 0x0000000000000008 (RELASZ)             192 (bytes)
 0x0000000000000009 (RELAENT)            24 (bytes)
 0x000000000000001e (FLAGS)              BIND_NOW
 0x000000006ffffffb (FLAGS_1)            Flags: NOW PIE
 0x000000006ffffffe (VERNEED)            0x428
 0x000000006fffffff (VERNEEDNUM)         1
 0x000000006ffffff0 (VERSYM)             0x416
 0x000000006ffffff9 (RELACOUNT)          3
 0x0000000000000000 (NULL)               0x0
 ````

## 特定のセクションヘッダの情報を表示する
### 16進数で表示
16進数で表示させるためには、-x オプションにセクション番号かセクション名を入力する
````
$ readelf -x 14 test

Hex dump of section '.text':
  0x000005a0 31ed4989 d15e4889 e24883e4 f050544c 1.I..^H..H...PTL
  0x000005b0 8d05ca01 0000488d 0d530100 00488d3d ......H..S...H.=
  0x000005c0 e6000000 ff15160a 2000f40f 1f440000 ........ ....D..
  0x000005d0 488d3d39 0a200055 488d0531 0a200048 H.=9. .UH..1. .H
  0x000005e0 39f84889 e5741948 8b05ea09 20004885 9.H..t.H.... .H.
  0x000005f0 c0740d5d ffe0662e 0f1f8400 00000000 .t.]..f.........
  0x00000600 5dc30f1f 4000662e 0f1f8400 00000000 ]...@.f.........
  0x00000610 488d3df9 09200048 8d35f209 20005548 H.=.. .H.5.. .UH
  0x00000620 29fe4889 e548c1fe 034889f0 48c1e83f ).H..H...H..H..?
  0x00000630 4801c648 d1fe7418 488b05b1 09200048 H..H..t.H.... .H
  0x00000640 85c0740c 5dffe066 0f1f8400 00000000 ..t.]..f........
  0x00000650 5dc30f1f 4000662e 0f1f8400 00000000 ]...@.f.........
  0x00000660 803da909 20000075 2f48833d 87092000 .=.. ..u/H.=.. .
  0x00000670 00554889 e5740c48 8b3d8a09 2000e80d .UH..t.H.=.. ...
  0x00000680 ffffffe8 48ffffff c6058109 2000015d ....H....... ..]
  0x00000690 c30f1f80 00000000 f3c3660f 1f440000 ..........f..D..
  0x000006a0 554889e5 5de966ff ffff5548 89e54883 UH..].f...UH..H.
  0x000006b0 ec206448 8b042528 00000048 8945f831 . dH..%(...H.E.1
  0x000006c0 c0c745e8 0a000000 48b84865 6c6c6f2c ..E.....H.Hello,
  0x000006d0 20674889 45ecc745 f4646221 00488d45  gH.E..E.db!.H.E
  0x000006e0 ec4889c7 e887feff ffb80000 0000488b .H............H.
  0x000006f0 55f86448 33142528 00000074 05e87efe U.dH3.%(...t..~.
  0x00000700 ffffc9c3 662e0f1f 84000000 00006690 ....f.........f.
  0x00000710 41574156 4989d741 5541544c 8d258e06 AWAVI..AUATL.%..
  0x00000720 20005548 8d2d8e06 20005341 89fd4989  .UH.-.. .SA..I.
  0x00000730 f64c29e5 4883ec08 48c1fd03 e807feff .L).H...H.......
  0x00000740 ff4885ed 742031db 0f1f8400 00000000 .H..t 1.........
  0x00000750 4c89fa4c 89f64489 ef41ff14 dc4883c3 L..L..D..A...H..
  0x00000760 014839dd 75ea4883 c4085b5d 415c415d .H9.u.H...[]A\A]
  0x00000770 415e415f c390662e 0f1f8400 00000000 A^A_..f.........
  0x00000780 f3c3
````

### 文字列で表示
文字列で表示させるためには、-p オプションにセクション番号かセクション名を入力する
````
$ readelf -p 27 test

String dump of section '.strtab':
  [     1]  crtstuff.c
  [     c]  deregister_tm_clones
  [    21]  __do_global_dtors_aux
  [    37]  completed.7697
  [    46]  __do_global_dtors_aux_fini_array_entry
  [    6d]  frame_dummy
  [    79]  __frame_dummy_init_array_entry
  [    98]  test.c
  [    9f]  __FRAME_END__
  [    ad]  __init_array_end
  [    be]  _DYNAMIC
  [    c7]  __init_array_start
  [    da]  __GNU_EH_FRAME_HDR
  [    ed]  _GLOBAL_OFFSET_TABLE_
  [   103]  __libc_csu_fini
  [   113]  _ITM_deregisterTMCloneTable
  [   12f]  puts@@GLIBC_2.2.5
  [   141]  _edata
  [   148]  __stack_chk_fail@@GLIBC_2.4
  [   164]  __libc_start_main@@GLIBC_2.2.5
  [   183]  __data_start
  [   190]  __gmon_start__
  [   19f]  __dso_handle
  [   1ac]  _IO_stdin_used
  [   1bb]  __libc_csu_init
  [   1cb]  __bss_start
  [   1d7]  main
  [   1dc]  __TMC_END__
  [   1e8]  _ITM_registerTMCloneTable
  [   202]  __cxa_finalize@@GLIBC_2.2.5
````

## Options
````
readelf: Warning: Nothing to do.
Usage: readelf <option(s)> elf-file(s)
 Display information about the contents of ELF format files
 Options are:
  -a --all               Equivalent to: -h -l -S -s -r -d -V -A -I
  -h --file-header       Display the ELF file header
  -l --program-headers   Display the program headers
     --segments          An alias for --program-headers
  -S --section-headers   Display the sections' header
     --sections          An alias for --section-headers
  -g --section-groups    Display the section groups
  -t --section-details   Display the section details
  -e --headers           Equivalent to: -h -l -S
  -s --syms              Display the symbol table
     --symbols           An alias for --syms
  --dyn-syms             Display the dynamic symbol table
  -n --notes             Display the core notes (if present)
  -r --relocs            Display the relocations (if present)
  -u --unwind            Display the unwind info (if present)
  -d --dynamic           Display the dynamic section (if present)
  -V --version-info      Display the version sections (if present)
  -A --arch-specific     Display architecture specific information (if any)
  -c --archive-index     Display the symbol/file index in an archive
  -D --use-dynamic       Use the dynamic section info when displaying symbols
  -x --hex-dump=<number|name>
                         Dump the contents of section <number|name> as bytes
  -p --string-dump=<number|name>
                         Dump the contents of section <number|name> as strings
  -R --relocated-dump=<number|name>
                         Dump the contents of section <number|name> as relocated bytes
  -z --decompress        Decompress section before dumping it
  -w[lLiaprmfFsoRtUuTgAckK] or
  --debug-dump[=rawline,=decodedline,=info,=abbrev,=pubnames,=aranges,=macro,=frames,
               =frames-interp,=str,=loc,=Ranges,=pubtypes,
               =gdb_index,=trace_info,=trace_abbrev,=trace_aranges,
               =addr,=cu_index,=links,=follow-links]
                         Display the contents of DWARF debug sections
  --dwarf-depth=N        Do not display DIEs at depth N or greater
  --dwarf-start=N        Display DIEs starting with N, at the same depth
                         or deeper
  -I --histogram         Display histogram of bucket list lengths
  -W --wide              Allow output width to exceed 80 characters
  @<file>                Read options from <file>
  -H --help              Display this information
  -v --version           Display the version number of readelf
````
