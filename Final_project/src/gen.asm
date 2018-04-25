extern printf

extern scanf

extern malloc

section	.data

print_int:	db	"%d",10,0
print_char:	db	"%c",0
scan_int:	db	"%d",0
_6	dd	0
_7	dd	0
_5	dd	0
_2	dd	0
_3	dd	0
_4	dd	0
_1	dd	0
_8	dd	0

section .text
	global main
main:
func__lmain:
	push ebp
	mov ebp, esp
	sub esp, 16
	lea eax, [ebp-4]
	push ebp
	mov ebp,esp
	push eax
	push scan_int
	call scanf
	add esp, 8
	mov esp, ebp
	pop ebp
	mov ebx, dword 1
	mov ecx, ebx
	imul ecx, [ebp-4]
	mov [_1], ecx
	push ebp
	mov ebp, esp
	shl ecx, 2
	push ecx
	call malloc
	add esp, 4
	mov esp, ebp
	pop ebp
	mov ebx, dword 0
	mov [ebp-12], ebx
	mov [ebp-8], eax
func__l2:
	mov ebx, [ebp-12]
	cmp ebx, [ebp-4]
	mov [ebp-12], ebx
	jl func__l7
func__l6:
	mov ebx, dword 0
	mov [_2], ebx
	jmp func__l8
func__l7:
	mov ebx, dword 1
	mov [_2], ebx
func__l8:
	jmp func__l3
func__l4:
	mov ebx, [ebp-12]
	inc ebx
	mov [ebp-12], ebx
	jmp func__l2
func__l3:
	mov ebx, [_2]
	cmp ebx, dword 0
	mov [_2], ebx
	je func__l5
	mov ebx, [ebp-12]
	mov ecx, ebx
	shl ecx, 2
	add ecx, [ebp-8]
	mov ecx, [ecx]
	mov esi, dword 'a'
	add esi, ebx
	mov edi, ebx
	shl edi, 2
	add edi, [ebp-8]
	mov [edi], esi
	mov [_3], ebx
	mov [ebp-12], ebx
	mov [_4], ecx
	mov [_5], esi
	jmp func__l4
func__l5:
	mov ebx, dword 0
	mov [ebp-16], ebx
func__l10:
	mov ebx, [ebp-16]
	cmp ebx, [ebp-4]
	mov [ebp-16], ebx
	jl func__l15
func__l14:
	mov ebx, dword 0
	mov [_6], ebx
	jmp func__l16
func__l15:
	mov ebx, dword 1
	mov [_6], ebx
func__l16:
	jmp func__l11
func__l12:
	mov ebx, [ebp-16]
	inc ebx
	mov [ebp-16], ebx
	jmp func__l10
func__l11:
	mov ebx, [_6]
	cmp ebx, dword 0
	mov [_6], ebx
	je func__l13
	mov ebx, [ebp-16]
	mov ecx, ebx
	shl ecx, 2
	add ecx, [ebp-8]
	mov ecx, [ecx]
	mov [ebp-16], ebx
	mov [_7], ebx
	mov [_8], ecx
	push ebp
	mov ebp,esp
	push dword ecx
	push dword print_char
	call printf
	add esp, 8
	mov esp, ebp
	pop ebp
	mov eax, dword ' '
	push ebp
	mov ebp,esp
	push dword eax
	push dword print_char
	call printf
	add esp, 8
	mov esp, ebp
	pop ebp
	jmp func__l12
func__l13:
	mov eax, dword 0
	mov esp, ebp
	pop ebp
	ret
	mov esp, ebp
	pop ebp
	ret
