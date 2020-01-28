# gcc

## Disable stack smash protector
```bash
gcc overflow.c -o overflow -fno-stack-protector
```
[stackoverflow](https://stackoverflow.com/questions/2340259/how-to-turn-off-gcc-compiler-optimization-to-enable-buffer-overflow)

## Compile a 32-bit application
```
gcc -m32 -o test test.c
```
