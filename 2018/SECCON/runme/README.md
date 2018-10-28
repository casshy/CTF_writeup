# Runme

## Problem
Run me.

## 回答
問題のファイルはどうやらWindows(32bit)の実行ファイルのよう
````
$ file runme.exe_b834d0ce1d709affeedb1ee4c2f9c5d8ca4aac68 
runme.exe_b834d0ce1d709affeedb1ee4c2f9c5d8ca4aac68: PE32 executable (console) Intel 80386, for MS Windows
````

ただ、以下のようにstringsで見てみるとBRj~のところにフラグっぽい文字列を見つけた。
````
$ strings runme.exe_b834d0ce1d709affeedb1ee4c2f9c5d8ca4aac68 
!This program cannot be run in DOS mode.
.text
 .data
@.import
j@h' @
h0 @
BRjC
BRj:
BRj\
BRjT
BRje
BRjm
BRjp
BRj\
BRjS
BRjE
BRjC
BRjC
BRjO
BRjN
BRj2
BRj0
BRj1
BRj8
BRjO
BRjn
BRjl
BRji
BRjn
BRje
BRj.
BRje
BRjx
BRje
BRj"
BRj 
BRjS
BRjE
BRjC
BRjC
BRjO
BRjN
BRj{
BRjR
BRju
BRjn
BRjn
BRj1
BRjn
BRj6
BRj_
BRjP
BRj4
BRj7
BRjh
BRj}^
Failed
The environment is not correct.
Congratz
You know the flag!
kernel32.dll
user32.dll
ExitProcess
GetCommandLineA
MessageBoxA
````

繋ぎ合わせてみると無事フラグを入手できた。(Runしてない)
````
flag = SECCON{Runn1n6_P47h}
````
