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

## ELFヘッダを表示
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

## セクション一覧を表示
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
