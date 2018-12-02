extern printf

extern scanf

section	.data

print_int:	db	"%d",10,0
scan_int:	db	"%d",0
a	dd	0
b	dd	0
c	dd	0
d	dd	0
e	dd	0
f	dd	0
g	dd	0
h	dd	0
y	dd	0
z	dd	0
u	dd	0
t	dd	0

section .text
	global main
main:
	mov ebx, dword 5
	mov ecx, dword 7
	mov esi, dword 8
	mov edi, dword 9
	mov edx, dword 10
	mov eax, dword 11
	mov [g], dword 12
	mov [h], dword 13
	mov ebx, dword 17
	mov [a], ebx
	mov [b], ecx
	mov [c], esi
	mov [d], edi
	mov [e], edx
	mov [f], eax
	push ebp
	mov ebp,esp
	push dword [a]
	push dword print_int
	call printf
	add esp, 8
	mov esp, ebp
	pop ebp
	mov [a], dword 5
	push ebp
	mov ebp,esp
	push dword [a]
	push dword print_int
	call printf
	add esp, 8
	mov esp, ebp
	pop ebp
	mov ebx, [a]
	add ebx, dword 6
	mov [a], ebx
	push ebp
	mov ebp,esp
	push dword [a]
	push dword print_int
	call printf
	add esp, 8
	mov esp, ebp
	pop ebp
	mov ebx, dword 6
	add ebx, [a]
	mov [a], ebx
	push ebp
	mov ebp,esp
	push dword [a]
	push dword print_int
	call printf
	add esp, 8
	mov esp, ebp
	pop ebp
	mov ebx, [b]
	sub ebx, dword 1
	mov [b], ebx
	push ebp
	mov ebp,esp
	push dword [b]
	push dword print_int
	call printf
	add esp, 8
	mov esp, ebp
	pop ebp
	mov ebx, dword 1
	sub ebx, [b]
	mov [b], ebx
	push ebp
	mov ebp,esp
	push dword [b]
	push dword print_int
	call printf
	add esp, 8
	mov esp, ebp
	pop ebp
	mov ebx, [e]
	sub ebx, [c]
	mov [b], ebx
	push ebp
	mov ebp,esp
	push dword [b]
	push dword print_int
	call printf
	add esp, 8
	mov esp, ebp
	pop ebp
	mov ebx, dword 6
	sub ebx, [c]
	mov [b], ebx
	push ebp
	mov ebp,esp
	push dword [b]
	push dword print_int
	call printf
	add esp, 8
	mov esp, ebp
	pop ebp
	mov ebx, [c]
	sub ebx, dword 6
	mov [b], ebx
	push ebp
	mov ebp,esp
	push dword [b]
	push dword print_int
	call printf
	add esp, 8
	mov esp, ebp
	pop ebp
	mov ebx, [f]
	imul ebx, [g]
	mov [y], ebx
	push ebp
	mov ebp,esp
	push dword [y]
	push dword print_int
	call printf
	add esp, 8
	mov esp, ebp
	pop ebp
	mov ebx, [y]
	shl ebx, 0
	imul ebx, dword 2
	mov [y], ebx
	push ebp
	mov ebp,esp
	push dword [y]
	push dword print_int
	call printf
	add esp, 8
	mov esp, ebp
	pop ebp
	mov ebx, dword 2
	imul ebx, [y]
	mov [y], ebx
	push ebp
	mov ebp,esp
	push dword [y]
	push dword print_int
	call printf
	add esp, 8
	mov esp, ebp
	pop ebp
	mov ebx, dword 2
	imul ebx, [y]
	mov [z], ebx
	push ebp
	mov ebp,esp
	push dword [z]
	push dword print_int
	call printf
	add esp, 8
	mov esp, ebp
	pop ebp
	mov ebx, [y]
	shl ebx, 0
	imul ebx, dword 2
	mov [z], ebx
	push ebp
	mov ebp,esp
	push dword [z]
	push dword print_int
	call printf
	add esp, 8
	mov esp, ebp
	pop ebp
	mov [u], dword 6
	push ebp
	mov ebp,esp
	push dword [u]
	push dword print_int
	call printf
	add esp, 8
	mov esp, ebp
	pop ebp
	mov ebx, [u]
	imul ebx, [u]
	mov [u], ebx
	push ebp
	mov ebp,esp
	push dword [u]
	push dword print_int
	call printf
	add esp, 8
	mov esp, ebp
	pop ebp
	mov [d], dword 81
	push ebp
	mov ebp,esp
	push dword [d]
	push dword print_int
	call printf
	add esp, 8
	mov esp, ebp
	pop ebp
	mov [t], dword 1
	push ebp
	mov ebp,esp
	push dword [t]
	push dword print_int
	call printf
	add esp, 8
	mov esp, ebp
	pop ebp
	mov eax, [h]
	cdq
	idiv dword[f]
	mov [t], edx
	push ebp
	mov ebp,esp
	push dword [t]
	push dword print_int
	call printf
	add esp, 8
	mov esp, ebp
	pop ebp
	mov eax, [h]
	mov ebx, dword 7
	cdq
	idiv ebx
	mov [t], edx
	push ebp
	mov ebp,esp
	push dword [t]
	push dword print_int
	call printf
	add esp, 8
	mov esp, ebp
	pop ebp
	mov eax, dword 7
	cdq
	idiv dword[h]
	mov [t], edx
	push ebp
	mov ebp,esp
	push dword [t]
	push dword print_int
	call printf
	add esp, 8
	mov esp, ebp
	pop ebp
	mov eax, [t]
	mov ebx, dword 3
	cdq
	idiv ebx
	mov [t], edx
	push ebp
	mov ebp,esp
	push dword [t]
	push dword print_int
	call printf
	add esp, 8
	mov esp, ebp
	pop ebp
	mov eax, dword 11
	cdq
	idiv dword[t]
	mov [t], edx
	push ebp
	mov ebp,esp
	push dword [t]
	push dword print_int
	call printf
	add esp, 8
	mov esp, ebp
	pop ebp
	mov eax, [t]
	cdq
	idiv dword[h]
	mov [t], edx
	push ebp
	mov ebp,esp
	push dword [t]
	push dword print_int
	call printf
	add esp, 8
	mov esp, ebp
	pop ebp
	mov eax, dword 0
	ret
