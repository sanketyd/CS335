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
	push ebp
	mov ebp,esp
	push n
	push scan_int
	call scanf
	add esp, 8
	mov esp, ebp
	pop ebp
	mov ebx, dword 2
	mov ecx, dword 1
	mov [b], ebx
	mov [a], ecx
	call func_prime
	push ebp
	mov ebp,esp
	push dword [n]
	push dword print_int
	call printf
	add esp, 8
	mov esp, ebp
	pop ebp
	push ebp
	mov ebp,esp
	push dword [b]
	push dword print_int
	call printf
	add esp, 8
	mov esp, ebp
	pop ebp
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
func_prime:
	mov ebx, [b]
	cmp ebx, [n]
	mov [b], ebx
	je line_no_15
	mov eax, [n]
	cdq
	idiv dword[b]
	cmp edx, dword 0
	mov [a], edx
	je line_no_15
	mov ebx, [b]
	add ebx, dword 1
	mov [b], ebx
	call func_prime
line_no_15:
	ret
