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
new_symbol_table.py : Contains scopetable class and associated function
three_address_code.py : Contains code necessary for generating three address code



Test Cases:

test1.java: Normal class Declaration and lambda
test2.java: Inheritance
test3.java: MergeSort to test on big programs 
test4.java: MergeSort with syntax errors
test5.java: To test ternary operator and array declaration with new
test6.java: To test big expressions

