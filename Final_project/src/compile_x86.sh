python LALR_parser.py $1 > temp.ir
python gen_code.py temp.ir > gen.asm
nasm -f elf32 gen.asm
gcc -m32 gen.o
