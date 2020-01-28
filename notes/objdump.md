# objdump

引数に与えたオブジェクトファイルの情報を表示する.

## ソースコード
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
gcc -c test.c
````

## 逆アセンブル
````bash
objdump -M intel -d test.o
````

````bash
test.o:     file format elf64-x86-64


Disassembly of section .text:

0000000000000000 <main>:
   0:	55                   	push   rbp
   1:	48 89 e5             	mov    rbp,rsp
   4:	48 83 ec 20          	sub    rsp,0x20
   8:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
   f:	00 00
  11:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
  15:	31 c0                	xor    eax,eax
  17:	c7 45 e8 0a 00 00 00 	mov    DWORD PTR [rbp-0x18],0xa
  1e:	48 b8 48 65 6c 6c 6f 	movabs rax,0x67202c6f6c6c6548
  25:	2c 20 67
  28:	48 89 45 ec          	mov    QWORD PTR [rbp-0x14],rax
  2c:	c7 45 f4 64 62 21 00 	mov    DWORD PTR [rbp-0xc],0x216264
  33:	48 8d 45 ec          	lea    rax,[rbp-0x14]
  37:	48 89 c7             	mov    rdi,rax
  3a:	e8 00 00 00 00       	call   3f <main+0x3f>
  3f:	b8 00 00 00 00       	mov    eax,0x0
  44:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
  48:	64 48 33 14 25 28 00 	xor    rdx,QWORD PTR fs:0x28
  4f:	00 00
  51:	74 05                	je     58 <main+0x58>
  53:	e8 00 00 00 00       	call   58 <main+0x58>
  58:	c9                   	leave  
  59:	c3                   	ret
````

## Options
```objdump <option(s)> <file(s)>```

| Option | Description |
| --- | --- |
| -d<br>--disassemble | 命令を含むと思われるセクションを逆アセンブルする |
| -D<br>--disassemble-all | すべてのセクションを逆アセンブルする |
| --endian={big\|little} | オブジェクトファイルのエンディアンを指定する |
| -C<br>--demangle | 低レベルのシンボル名をユーザレベルの名前に変換する. C++の関数名の可読性が向上する.|
| --file-headers | オブジェクトファイルのoverallヘッダ情報の要約を表示する |
| --section=name | 特性のセクションのみの情報を表示する |
| --architecture=machine | 逆アセンブルする際のアーキテクチャを指定する |
| -S<br>--source | 可能ならソースコードを逆アセンブル結果と併せて表示する |
| --no-show-raw-insn | 逆アセンブルする際に16進数のバイトコードを表示しない |
| --start-address=address | データの表示開始アドレスを指定したアドレスにする(-d, -r, -sに対して有効) |
| --stop-address=address | データの表示終了アドレスを指定したアドレスにする(-d, -r, -sに対して有効) |

````
Usage: objdump <option(s)> <file(s)>
 Display information from object <file(s)>.
 At least one of the following switches must be given:
  -a, --archive-headers    Display archive header information
  -f, --file-headers       Display the contents of the overall file header
  -p, --private-headers    Display object format specific file header contents
  -P, --private=OPT,OPT... Display object format specific contents
  -h, --[section-]headers  Display the contents of the section headers
  -x, --all-headers        Display the contents of all headers
  -d, --disassemble        Display assembler contents of executable sections
  -D, --disassemble-all    Display assembler contents of all sections
  -S, --source             Intermix source code with disassembly
  -s, --full-contents      Display the full contents of all sections requested
  -g, --debugging          Display debug information in object file
  -e, --debugging-tags     Display debug information using ctags style
  -G, --stabs              Display (in raw form) any STABS info in the file
  -W[lLiaprmfFsoRtUuTgAckK] or
  --dwarf[=rawline,=decodedline,=info,=abbrev,=pubnames,=aranges,=macro,=frames,
          =frames-interp,=str,=loc,=Ranges,=pubtypes,
          =gdb_index,=trace_info,=trace_abbrev,=trace_aranges,
          =addr,=cu_index,=links,=follow-links]
                           Display DWARF info in the file
  -t, --syms               Display the contents of the symbol table(s)
  -T, --dynamic-syms       Display the contents of the dynamic symbol table
  -r, --reloc              Display the relocation entries in the file
  -R, --dynamic-reloc      Display the dynamic relocation entries in the file
  @<file>                  Read options from <file>
  -v, --version            Display this program's version number
  -i, --info               List object formats and architectures supported
  -H, --help               Display this information

 The following switches are optional:
  -b, --target=BFDNAME           Specify the target object format as BFDNAME
  -m, --architecture=MACHINE     Specify the target architecture as MACHINE
  -j, --section=NAME             Only display information for section NAME
  -M, --disassembler-options=OPT Pass text OPT on to the disassembler
  -EB --endian=big               Assume big endian format when disassembling
  -EL --endian=little            Assume little endian format when disassembling
      --file-start-context       Include context from start of file (with -S)
  -I, --include=DIR              Add DIR to search list for source files
  -l, --line-numbers             Include line numbers and filenames in output
  -F, --file-offsets             Include file offsets when displaying information
  -C, --demangle[=STYLE]         Decode mangled/processed symbol names
                                  The STYLE, if specified, can be `auto', `gnu',
                                  `lucid', `arm', `hp', `edg', `gnu-v3', `java'
                                  or `gnat'
  -w, --wide                     Format output for more than 80 columns
  -z, --disassemble-zeroes       Do not skip blocks of zeroes when disassembling
      --start-address=ADDR       Only process data whose address is >= ADDR
      --stop-address=ADDR        Only process data whose address is <= ADDR
      --prefix-addresses         Print complete address alongside disassembly
      --[no-]show-raw-insn       Display hex alongside symbolic disassembly
      --insn-width=WIDTH         Display WIDTH bytes on a single line for -d
      --adjust-vma=OFFSET        Add OFFSET to all displayed section addresses
      --special-syms             Include special symbols in symbol dumps
      --inlines                  Print all inlines for source line (with -l)
      --prefix=PREFIX            Add PREFIX to absolute paths for -S
      --prefix-strip=LEVEL       Strip initial directory names for -S
      --dwarf-depth=N        Do not display DIEs at depth N or greater
      --dwarf-start=N        Display DIEs starting with N, at the same depth
                             or deeper
      --dwarf-check          Make additional dwarf internal consistency checks.      

objdump: supported targets: elf64-x86-64 elf32-i386 elf32-iamcu elf32-x86-64 a.out-i386-linux pei-i386 pei-x86-64 elf64-l1om elf64-k1om elf64-little elf64-big elf32-little elf32-big pe-x86-64 pe-bigobj-x86-64 pe-i386 plugin srec symbolsrec verilog tekhex binary ihex
objdump: supported architectures: i386 i386:x86-64 i386:x64-32 i8086 i386:intel i386:x86-64:intel i386:x64-32:intel i386:nacl i386:x86-64:nacl i386:x64-32:nacl iamcu iamcu:intel l1om l1om:intel k1om k1om:intel plugin

The following i386/x86-64 specific disassembler options are supported for use
with the -M switch (multiple options should be separated by commas):
  x86-64      Disassemble in 64bit mode
  i386        Disassemble in 32bit mode
  i8086       Disassemble in 16bit mode
  att         Display instruction in AT&T syntax
  intel       Display instruction in Intel syntax
  att-mnemonic
              Display instruction in AT&T mnemonic
  intel-mnemonic
              Display instruction in Intel mnemonic
  addr64      Assume 64bit address size
  addr32      Assume 32bit address size
  addr16      Assume 16bit address size
  data32      Assume 32bit data size
  data16      Assume 16bit data size
  suffix      Always display instruction suffix in AT&T syntax
  amd64       Display instruction in AMD64 ISA
  intel64     Display instruction in Intel64 ISA
Report bugs to <http://www.sourceware.org/bugzilla/>.
````
