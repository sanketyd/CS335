extern printf

extern scanf

section	.data

print_int:	db	"%d",10,0
scan_int:	db	"%d",0
i	dd	0
j	dd	0
t1	dd	0
t2	dd	0
t3	dd	0
t4	dd	0
t5	dd	0
t6	dd	0
a	dd	0
k	dd	0

section .text
	global main
main:
	mov ebx, dword 1
	mov [i], ebx
line_no_2:
	mov ebx, dword 1
	mov [j], ebx
line_no_3:
	mov ebx, dword 10
	imul ebx, [i]
	mov ecx, ebx
	add ecx, [j]
	mov esi, dword 8
	imul esi, ecx
	mov edi, esi
	sub edi, dword 88
	mov edx, [j]
	add edx, dword 1
	cmp edx, dword 10
	mov [t1], ebx
	mov [t2], ecx
	mov [t3], esi
	mov [t4], edi
	mov [j], edx
	jle line_no_3
	mov ebx, [i]
	add ebx, dword 1
	cmp ebx, dword 10
	mov [i], ebx
	jle line_no_2
	mov ebx, dword 1
	mov ecx, ebx
	sub ecx, dword 1
	mov [i], ebx
	mov [t5], ecx
line_no_13:
	mov ebx, dword 88
	imul ebx, [t5]
	mov ecx, [i]
	add ecx, dword 1
	cmp ecx, dword 10
	mov [t6], ebx
	mov [i], ecx
	jle line_no_13
	mov [a], dword 7
	mov ebx, dword 1
	or ebx, dword 2
	mov ecx, dword 3
	mov eax, dword 0
	mov [a], ebx
	mov [k], ecx
	mov [j], ecx
	ret
