extern printf

extern scanf

section	.data

print_int:	db	"%d",10,0
scan_int:	db	"%d",0
i	dd	0
a	times	1000	dd	0
j	dd	0
t1	dd	0
t2	dd	0
t3	dd	0
t4	dd	0
t5	dd	0
t6	dd	0

section .text
	global main
main:
	mov ebx, dword 1
	mov ecx, dword 1
	mov [i], ebx
	mov [j], ecx
line_no_4:
	mov ebx, dword 10
	imul ebx, [i]
	mov ecx, ebx
	add ecx, [j]
	mov esi, dword 8
	imul esi, ecx
	mov edi, esi
	sub edi, dword 88
	mov edx, dword 0
	mov [a,edi*4], edx
	mov edx, [j]
	add edx, dword 1
	cmp edx, dword 10
	mov [t1], ebx
	mov [t2], ecx
	mov [t3], esi
	mov [t4], edi
	mov [j], edx
	jle line_no_4
	mov ebx, [i]
	add ebx, dword 1
	cmp ebx, dword 10
	mov [i], ebx
	jle line_no_4
	mov ebx, dword 1
	mov [i], ebx
line_no_14:
	mov ebx, [i]
	sub ebx, dword 1
	mov ecx, dword 88
	imul ecx, ebx
	mov esi, dword 1
	mov [a,ecx*4], esi
	mov esi, [i]
	add esi, dword 1
	cmp esi, dword 10
	mov [t5], ebx
	mov [t6], ecx
	mov [i], esi
	jle line_no_14
	mov [a], dword 7
	mov eax, dword 0
	ret
