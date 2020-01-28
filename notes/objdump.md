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
| --endian={big|little} | オブジェクトファイルのエンディアンを指定する |
| --file-headers | オブジェクトファイルのoverallヘッダ情報の要約を表示する |
| --section=name | 特性のセクションのみの情報を表示する |
| --architecture=machine | 逆アセンブルする際のアーキテクチャを指定する |
| -S<br>--source | 可能ならソースコードを逆アセンブル結果と併せて表示する |
| --no-show-raw-insn | 逆アセンブルする際に16進数のバイトコードを表示しない |
| --start-address=address | データの表示開始アドレスを指定したアドレスにする(-d, -r, -sに対して有効) |
| --stop-address=address | データの表示終了アドレスを指定したアドレスにする(-d, -r, -sに対して有効) |
