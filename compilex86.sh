nasm -f elf64 $1
filename=$(echo $1 | sed 's/.asm$/.o/g')
ld -s -o a.out $filename
