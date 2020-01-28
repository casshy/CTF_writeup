# Environment setup

## Tool list

- file
- readelf
- strings
- strace
- ltrace
- gdb
- objdump
- radare2
- rp++
- checksec.sh
- peda
- socat
- pwntools
- binwalk

## checksec.sh

````bash
cd ~/Downloads
wget https://github.com/slimm609/checksec.sh/archive/1.6.tar.gz
tar zxvf 1.6.tar.gz
cp checksec.sh-1.6/checksec ~/bin/checksec.sh
````

## socat
````bash
sudo apt install socat
````

## binwalk
````bash
sudo apt intall binwalk
````

## radare2
````bash
sudo apt install radare2
````

## rp++
````bash
cd ~/Downloads
wget https://github.com/downloads/0vercl0k/rp/rp-lin-x64 -O ~/bin/rp
chmod +x ~/bin/rp
````

## peda
````bash
sudo apt install install binutils python2.7 perl socat git build-essential gdb gdbserver
git clone https://github.com/longld/peda.git ~/peda
echo "source ~/peda/peda.py" >> ~/.gdbinit
````

## pwntools
````bash
sudo apt install openssl libssl-dev libbz2-dev libreadline-dev libsqlite3-dev
sudo apt-get install libncurses5 libncurses5-dev libncursesw5
pyenv install 2.7.17
pyenv local 2.7.17
pip install --upgrade pip
pip install pwntools
# When error occur
sudo apt install libffi-dev
pip install cryptography
````

## IDA Free
Download install file from following url  
https://www.hex-rays.com/products/ida/support/download_freeware.shtml
````bash
chmod +x idafree70_linux.run
./idafree70_linux.run
````

## References
- http://nonkuru.hateblo.jp/entry/2016/06/24/233622
- https://7me.oji.0j0.jp/2017/python-curses-pyenv-no-module.html
