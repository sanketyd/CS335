extern printf

extern scanf

section	.data

print_int:	db	"%d",10,0
scan_int:	db	"%d",0
n	dd	0
b	dd	0
a	dd	0

section .text
	global main
main:
	mov ebx, dword 5
	mov ecx, dword 4
	mov esi, dword 1
	mov [n], ebx
	mov [b], ecx
	mov [a], esi
	call func_power
	push ebp
	mov ebp,esp
	push dword [a]
	push dword print_int
	call printf
	add esp, 8
	mov esp, ebp
	pop ebp
	mov eax, dword 0
	ret
func_power:
	mov ebx, [b]
	cmp ebx, dword 0
	mov [b], ebx
	je line_no_12
	mov ebx, [n]
	imul ebx, [a]
	mov ecx, [b]
	sub ecx, dword 1
	mov [a], ebx
	mov [b], ecx
	call func_power
line_no_12:
	ret
