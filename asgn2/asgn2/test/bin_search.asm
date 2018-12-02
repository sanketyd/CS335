extern printf

extern scanf

section	.data

print_int:	db	"%d",10,0
scan_int:	db	"%d",0
arr	times	500	dd	0
n	dd	0
l	dd	0
r	dd	0
i	dd	0
key	dd	0
t	dd	0
d	dd	0
e	dd	0
x	dd	0
index	dd	0
m	dd	0

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
	mov ebx, [n]
	dec ebx
	mov ecx, dword 0
	mov esi, dword 0
	mov [n], ebx
	mov [r], ebx
	mov [l], ecx
	mov [i], esi
	push ebp
	mov ebp,esp
	push key
	push scan_int
	call scanf
	add esp, 8
	mov esp, ebp
	pop ebp
line_no_8:
	push ebp
	mov ebp,esp
	push t
	push scan_int
	call scanf
	add esp, 8
	mov esp, ebp
	pop ebp
	mov ebx, [i]
	mov ecx, [t]
	mov [arr,ebx*4], ecx
	mov esi, ebx
	inc esi
	cmp esi, [n]
	mov [t], ecx
	mov [i], esi
	jle line_no_8
	call func_binary_search
	push ebp
	mov ebp,esp
	mov [index], eax
	push dword eax
	push dword print_int
	call printf
	add esp, 8
	mov esp, ebp
	pop ebp
	mov eax, dword 0
	ret
func_binary_search:
	mov ebx, [l]
	add ebx, [r]
	mov eax, ebx
	mov ecx, dword 2
	cdq
	idiv ecx
	mov ebx, eax
	shl ebx, 2
	add ebx, arr
	mov ebx, [ebx]
	cmp ebx, [key]
	mov [t], ebx
	mov [m], eax
	je line_no_25
	mov ebx, [t]
	cmp ebx, [key]
	mov [t], ebx
	jle line_no_23
	mov ebx, [m]
	sub ebx, dword 1
	mov [r], ebx
	call func_binary_search
line_no_23:
	mov ebx, [m]
	add ebx, dword 1
	mov [l], ebx
	call func_binary_search
line_no_25:
	mov eax, [m]
	ret
