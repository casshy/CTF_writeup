# unzip
## Problem
Unzip flag.zip.

## 回答
問題文ではzipファイルが与えられており、解凍してみるとmakefile.shとflag.zipが出てくる。  
makefile.shは以下のような内容で、フラグを作成して暗号化zipに圧縮した際のスクリプトっぽい。暗号化のキーにはperlのtime関数が使用されている。

````
echo 'SECCON{'`cat key`'}' > flag.txt
zip -e --password=`perl -e "print time()"` flag.zip flag.txt
````

time関数をローカルで実行してみると現在時刻を10桁の数字で出力するものらしい。
````
$ perl -e "print time()"
1540734407
````

そこで、この情報をもとに暗号化zipのパスワード解析ツールのfcrackzipで解析して見たところ無事パスワードを特定できた。
````
$ fcrackzip -u -l 10 -c 1 -p 1540000000 flag.zip


PASSWORD FOUND!!!!: pw == 1540566641
````
このパスワードをもとにflag.zipを解凍してフラグを得た。
````
$ unzip flag.zip
Archive:  flag.zip
[flag.zip] flag.txt password: 
  inflating: flag.txt
$ cat flag.txt 
SECCON{We1c0me_2_SECCONCTF2o18}
````
フラグのメッセージ的にもこのCTFの導入的な位置付けの問題だろうか。
