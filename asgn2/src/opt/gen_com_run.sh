filename=$(echo $1 | sed 's/.csv/.asm/g')
python optimize.py ../../test/$1 > $filename
nasm -f elf32 $filename
filename=$(echo $filename | sed 's/.asm$/.o/g')
gcc -m32 $filename
./a.out
rm *.o
