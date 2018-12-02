extern printf

extern scanf

section	.data

print_int:	db	"%d",10,0
scan_int:	db	"%d",0
a	dd	0
b	dd	0
r	dd	0
y	dd	0
t	dd	0

section .text
	global main
main:
	push ebp
	mov ebp,esp
	push a
	push scan_int
	call scanf
	add esp, 8
	mov esp, ebp
	pop ebp
	push ebp
	mov ebp,esp
	push b
	push scan_int
	call scanf
	add esp, 8
	mov esp, ebp
	pop ebp
	mov ebx, [a]
	and ebx, [b]
	mov ecx, [a]
	or ecx, [b]
	mov esi, [a]
	xor esi, [b]
	mov [r], ebx
	mov [y], ecx
	mov [t], esi
	push ebp
	mov ebp,esp
	push dword [r]
	push dword print_int
	call printf
	add esp, 8
	mov esp, ebp
	pop ebp
	push ebp
	mov ebp,esp
	push dword [y]
	push dword print_int
	call printf
	add esp, 8
	mov esp, ebp
	pop ebp
	push ebp
	mov ebp,esp
	push dword [t]
	push dword print_int
	call printf
	add esp, 8
	mov esp, ebp
	pop ebp
	mov ebx, [r]
	not ebx
	mov [t], ebx
	push ebp
	mov ebp,esp
	push dword [t]
	push dword print_int
	call printf
	add esp, 8
	mov esp, ebp
	pop ebp
	push ebp
	mov ebp,esp
	push dword [r]
	push dword print_int
	call printf
	add esp, 8
	mov esp, ebp
	pop ebp
	mov eax, dword 0
	ret
