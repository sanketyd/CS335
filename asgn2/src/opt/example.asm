extern printf

extern scanf

section	.data

print_int:	db	"%d",10,0
scan_int:	db	"%d",0
a	dd	0
b	dd	0

section .text
	global main
main:
	mov ebx, dword 2
	mov [a], ebx
line_no_2:
	mov ebx, dword 7
	mov ecx, [a]
	add ecx, ebx
	cmp ecx, dword 50
	mov [b], ebx
	mov [a], ecx
	jle line_no_2
	call func_foo
	ret
func_foo:
	push ebp
	mov ebp,esp
	push dword [a]
	push dword print_int
	call printf
	add esp, 8
	mov esp, ebp
	pop ebp
	ret
