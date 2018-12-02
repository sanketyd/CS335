extern printf

extern scanf

section	.data

print_int:	db	"%d",10,0
scan_int:	db	"%d",0
n	dd	0
a	times	50	dd	0
i	dd	0
f	dd	0
b	dd	0
fib	dd	0
t1	dd	0
t2	dd	0
t3	dd	0
t4	dd	0
t5	dd	0
t	dd	0

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
	mov ebx, dword 1
	mov [a+4], ebx
	mov ebx, dword 2
	mov [i], ebx
	call func_calc_fib
	mov [fib], eax
	push ebp
	mov ebp,esp
	push dword [fib]
	push dword print_int
	call printf
	add esp, 8
	mov esp, ebp
	pop ebp
	call func_print_arr
	mov eax, dword 0
	ret
func_calc_fib:
	mov ebx, [i]
	sub ebx, dword 2
	mov ecx, [i]
	sub ecx, dword 1
	mov esi, ecx
	shl esi, 2
	add esi, a
	mov esi, [esi]
	mov edi, ebx
	shl edi, 2
	add edi, a
	mov edi, [edi]
	mov edx, esi
	add edx, edi
	mov eax, [i]
	mov [t5], edx
	mov edx, [t5]
	mov [a,eax*4], edx
	mov [i], eax
	mov eax, [i]
	inc eax
	cmp eax, [n]
	mov [t1], ebx
	mov [t2], ecx
	mov [t3], esi
	mov [t4], edi
	mov [t5], edx
	mov [i], eax
	jle func_calc_fib
	mov ebx, [i]
	dec ebx
	mov ecx, ebx
	shl ecx, 2
	add ecx, a
	mov ecx, [ecx]
	mov eax, ecx
	mov [i], ebx
	mov [t], ecx
	ret
func_print_arr:
	mov ebx, dword 0
	mov [i], ebx
line_no_23:
	mov ebx, [i]
	shl ebx, 2
	add ebx, a
	mov ebx, [ebx]
	mov [t], ebx
	push ebp
	mov ebp,esp
	push dword [t]
	push dword print_int
	call printf
	add esp, 8
	mov esp, ebp
	pop ebp
	mov ebx, [i]
	inc ebx
	cmp ebx, [n]
	mov [i], ebx
	jle line_no_23
	mov eax, dword 0
	ret
