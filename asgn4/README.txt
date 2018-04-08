Group 7
Name, Roll No
Abhisek Panda, 150026
Raktim Mitra, 150562
Sanket, 150634

Build and Run Description:

Run make in asgn4 directory, then bin/irgen test/<testcase>



Src Description:
We have used emit based method for IR generation.

LALR_parser.py: Contains the parsers and all the semantic actions associated with each rule.
new_sym_table.py : Contains scopetable class and associated function
three_address_code.py : Contains code necessary for generating three address code



Test Cases:

dowhile.java: do while loop
for.java: for loop
while.java: while loop 
break_continue.java: if-else, break, continue
func_arr.java: function and array
logops.java: logical ops
matmult.java: Multiplication of 2d matrices

