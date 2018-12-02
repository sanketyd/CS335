extern printf

extern scanf

section	.data

print_int:	db	"%d",10,0
scan_int:	db	"%d",0
a	dd	0
b	dd	0
c	dd	0

section .text
	global main
main:
	mov ebx, dword 2
	mov ecx, ebx
	add ecx, dword 4
	cmp ecx, dword 7
	mov [a], ebx
	mov [b], ecx
	jle line_no_7
	mov ebx, [b]
	imul ebx, [a]
	cmp ebx, dword 10
	mov [c], ebx
	jle line_no_11
	jmp line_no_13
line_no_7:
	jmp line_no_9
	jmp line_no_13
line_no_9:
	push ebp
	mov ebp,esp
	push dword [a]
	push dword print_int
	call printf
	add esp, 8
	mov esp, ebp
	pop ebp
	jmp line_no_13
line_no_11:
	push ebp
	mov ebp,esp
	push dword [c]
	push dword print_int
	call printf
	add esp, 8
	mov esp, ebp
	pop ebp
	jmp line_no_13
line_no_13:
	mov eax, dword 0
	ret
