nasm -f elf64 $1
ld -s -o a.out $1.o
