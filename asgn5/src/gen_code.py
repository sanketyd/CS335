#!/usr/bin/env python
import sys
import copy
from math import log
from get_reg import *
from utilities import *

class CodeGenerator:
    def gen_data_section(self):
        print("extern printf\n")
        print("extern scanf\n")
        print("section\t.data\n")
        print("print_int:\tdb\t\"%d\",10,0")
        print("scan_int:\tdb\t\"%d\",0")
        for symbol in symbol_table.keys():
            if symbol_table[symbol].array_size != None:
                print(str(symbol) + "\ttimes\t" + str(symbol_table[symbol].array_size) + "\tdd\t0")
            else:
                print(str(symbol) + "\tdd\t0")

    def gen_start_template(self):
        print()
        print("section .text")
        print("\tglobal main")
        print("main:")

    def op_print_int(self, instr):
        print("\tpush ebp")
        print("\tmov ebp,esp")
        loc = get_best_location(instr.inp1)
        save_context()
        print("\tpush dword " + str(loc))
        print("\tpush dword print_int")
        print("\tcall printf")
        print("\tadd esp, 8")
        print("\tmov esp, ebp")
        print("\tpop ebp")

    def op_scan_int(self, instr):
        save_context()
        print("\tpush ebp")
        print("\tmov ebp,esp")
        print("\tpush " + instr.out)
        print("\tpush scan_int")
        print("\tcall scanf")
        print("\tadd esp, 8")
        print("\tmov esp, ebp")
        print("\tpop ebp")

    def optimize_if_possible(self, out, inp1, inp2, op):
        '''
        If both inputs are integers; compute them beforehand
        '''
        if is_valid_number(inp1) and is_valid_number(inp2):
            inp1 = int(inp1)
            inp2 = int(inp2)
            if op == "+":
                res = inp1 + inp2
            elif op == "-":
                res = inp1 - inp2
            elif op == "*":
                res = inp1 * inp2
            elif op == "/":
                res = inp1 / inp2
            elif op == "%":
                res = inp1 % inp2
            elif op == "<<":
                res = inp1 << inp2
            elif op == ">>":
                res = inp1 >> inp2
            res = int(res)
            print("\tmov " + get_best_location(out) + ", " + get_best_location(str(res)))
            return True
        return False

    def op_add(self, instr):
        optimized = self.optimize_if_possible(instr.out, instr.inp1, instr.inp2, instr.operation)
        if optimized:
            return
        R1, flag = get_reg(instr)
        if flag:
            print("\tmov "+ R1 + ", " + get_best_location(instr.inp1))
        R2 = get_best_location(instr.inp2)
        print("\tadd " + R1 + ", " + R2)
        update_reg_descriptors(R1,instr.out)
        free_regs(instr)


    def op_sub(self, instr):
        optimized = self.optimize_if_possible(instr.out, instr.inp1, instr.inp2, instr.operation)
        if optimized:
            return
        R1, flag = get_reg(instr)
        if flag:
            print("\tmov "+ R1 + ", " + get_best_location(instr.inp1))
        R2 = get_best_location(instr.inp2)
        print("\tsub " + R1 + ", " + R2)
        update_reg_descriptors(R1,instr.out)
        free_regs(instr)


    def op_mult(self, instr):
        optimized = self.optimize_if_possible(instr.out, instr.inp1, instr.inp2, instr.operation)
        if optimized:
            return
        R1, flag = get_reg(instr)
        if flag:
            print("\tmov "+ R1 + ", " + get_best_location(instr.inp1))
        # handle cases when inp2 is a power of 2
        bitshift = False        # to avoid multiple operations
        if is_valid_number(instr.inp2):
            num = int(instr.inp2)
            if num & (num - 1) == 0 and num != 0:
                # use bitshift
                power = int(log(int(instr.inp2)))
                print("\tshl " + R1 + ", " + str(power))
                bitshift = False
        if not bitshift:
            R2 = get_best_location(instr.inp2)
            print("\timul " + R1 + ", " + R2)
        update_reg_descriptors(R1, instr.out)
        free_regs(instr)


    def op_div(self, instr):
        optimized = self.optimize_if_possible(instr.out, instr.inp1, instr.inp2, instr.operation)
        if optimized:
            return
        save_reg_contents("eax")
        print("\tmov eax, " + get_best_location(instr.inp1))
        save_reg_contents("edx")
        if is_valid_number(instr.inp2):
            R1, flag = get_reg(instr,exclude=["eax","edx"])
            print("\tmov " + R1 + ", " + get_best_location(instr.inp2))
            print("\tcdq")
            print("\tidiv " + R1)
        else:
            print("\tcdq")
            print("\tidiv dword " + get_best_location(instr.inp2))
        update_reg_descriptors("eax", instr.out)
        free_regs(instr)


    def op_modulo(self, instr):
        optimized = self.optimize_if_possible(instr.out, instr.inp1, instr.inp2, instr.operation)
        if optimized:
            return
        save_reg_contents("eax")
        print("\tmov eax, " + get_best_location(instr.inp1))
        save_reg_contents("edx")
        if is_valid_number(instr.inp2):
            R1, flag = get_reg(instr,exclude=["eax","edx"])
            print("\tmov " + R1 + ", " + get_best_location(instr.inp2))
            print("\tcdq")
            print("\tidiv " + R1)
        else:
            print("\tcdq")
            print("\tidiv dword" + get_best_location(instr.inp2))

        update_reg_descriptors("edx", instr.out)
        free_regs(instr)


    def op_lshift(self, instr):
        optimized = self.optimize_if_possible(instr.out, instr.inp1, instr.inp2, instr.operation)
        if optimized:
            return
        R1, flag = get_reg(instr)
        if flag:
            print("\tmov "+ R1 + ", " + get_best_location(instr.inp1))
        R2 = None
        if is_valid_number(instr.inp2):
            R2 = instr.inp2
        else:
            R2 = get_best_location(instr.inp2)
        print("\tshl " + R1 + ", " + R2)
        update_reg_descriptors(R1, instr.out)
        free_regs(instr)


    def op_rshift(self, instr):
        optimized = self.optimize_if_possible(instr.out, instr.inp1, instr.inp2, instr.operation)
        if optimized:
            return
        R1, flag = get_reg(instr)
        if flag:
            print("\tmov "+ R1 + ", " + get_best_location(instr.inp1))
        R2 = None
        if is_valid_number(instr.inp2):
            R2 = instr.inp2
        else:
            R2 = get_best_location(instr.inp2)
        print("\tshr " + R1 + ", " + R2)
        update_reg_descriptors(R1, instr.out)
        free_regs(instr)


    def op_assign(self, instr):
        if instr.array_index_i1 == None and instr.array_index_o == None and is_valid_number(instr.inp1):
            R1, flag = get_reg(instr, compulsory=False)
            print("\tmov " + R1 + ", " + get_best_location(instr.inp1))
            if R1 in reg_descriptor.keys():
                update_reg_descriptors(R1, instr.out)

        elif instr.array_index_i1 == None and instr.array_index_o == None:
            if len(symbol_table[instr.inp1].address_descriptor_reg) == 0:
                R1, flag = get_reg(instr)
                print("\tmov " + R1 +", " + get_best_location(instr.inp1))
                update_reg_descriptors(R1,instr.inp1)

            if len(symbol_table[instr.inp1].address_descriptor_reg):
                for regs in symbol_table[instr.out].address_descriptor_reg:
                    reg_descriptor[regs].remove(instr.out)
                symbol_table[instr.out].address_descriptor_reg.clear()
                symbol_table[instr.out].address_descriptor_reg = copy.deepcopy(symbol_table[instr.inp1].address_descriptor_reg)

                for reg in symbol_table[instr.out].address_descriptor_reg:
                    reg_descriptor[reg].add(instr.out)

                free_regs(instr)

        elif instr.array_index_i1 != None:
            assert len(symbol_table[instr.inp1].address_descriptor_reg) == 0
            R1, flag = get_reg(instr)
            print("\tmov " + R1 + ", " + get_best_location(instr.array_index_i1))
            print("\tshl " + R1 + ", 2")
            print("\tadd " + R1 + ", " + instr.inp1)
            print("\tmov " + R1 + ", [" + R1 + "]")
            update_reg_descriptors(R1, instr.out)

        else:
            index = instr.array_index_o
            R1 = None
            if is_valid_sym(index):
                if len(symbol_table[index].address_descriptor_reg) == 0:
                    R1, _ = get_reg(instr)
                    print("\tmov " + R1 + ", " + get_best_location(index))
                    update_reg_descriptors(R1, index)
                else:
                    R1 = get_best_location(index)

                inp_reg = R1
                if index != instr.inp1:
                    inp_reg, flag = get_reg(instr, exclude=[R1])
                    if flag:
                        print("\tmov " + inp_reg + ", " + get_best_location(instr.inp1))
                        update_reg_descriptors(inp_reg,instr.inp1)
                print("\tmov [" + instr.out + "," + R1 + "*4], " + inp_reg)
            else:
                index = 4 * int(index)
                inp_reg, flag = get_reg(instr)
                if flag:
                    print("\tmov " + inp_reg + ", " + get_best_location(instr.inp1))
                    update_reg_descriptors(inp_reg,instr.inp1)
                print("\tmov [" + instr.out + "+" + str(index) + "], " + inp_reg)


    def op_logical(self, instr):
        # TODO: logical &&, ||
        R1, flag = get_reg(instr)
        if flag:
            print("\tmov "+ R1 + ", " + get_best_location(instr.inp1))
        R2 = get_best_location(instr.inp2)
        def log_op(x):
            return {
                    "&" : "and ",
                    "|" : "or ",
                    "^" : "xor ",
                    # remove the following 2 lines after TODO
                    "&&": "and ",
                    "||": "or ",
            }[x]
        if (instr.operation != "~" and instr.operation != "!"):
            print("\t" + log_op(instr.operation) + R1 + ", " + R2)
        else:
            print("\tnot " + R1)
        update_reg_descriptors(R1,instr.out)
        free_regs(instr)

    def op_unary(self, instr):
        R1, flag = get_reg(instr,compulsory=False)
        if R1 not in reg_descriptor.keys():
            R1 = "dword " + R1
        if flag:
            print("\tmov "+ R1 + ", " + get_best_location(instr.inp1))
        if instr.operation == "!" or instr.operation == "~":
            print("\tnot "+ R1)
        elif instr.operation == "++":
            print("\tinc "+ R1)
        elif instr.operation == "--":
            print("\tdec "+ R1)
        if R1 in reg_descriptor.keys():
            update_reg_descriptors(R1,instr.out)
        free_regs(instr)

    def op_ifgoto(self, instr):
        inp1 = instr.inp1
        inp2 = instr.inp2
        out = None
        jmp_label = None
        if instr.jmp_to_line != None:
            jmp_label = "line_no_" + str(instr.jmp_to_line)
        else:
            jmp_label = "func_" + instr.jmp_to_label

        operator = instr.operation
        if is_valid_number(instr.inp1) and is_valid_number(instr.inp2):
            save_context()
            if operator == "geq":
                if inp1 >= inp2:
                    print("\tjmp " + jmp_label)
            elif operator == "gt":
                if inp1 > inp2:
                    print("\tjmp " + jmp_label)
            elif operator == "leq":
                if inp1 <= inp2:
                    print("\tjmp " + jmp_label)
            elif operator == "lt":
                if inp1 < inp2:
                    print("\tjmp " + jmp_label)
            elif operator == "eq":
                if inp1 == inp2:
                    print("\tjmp " + jmp_label)
            elif operator == "neq":
                if inp1 != inp2:
                    print("\tjmp " + jmp_label)
            return

        R1 = get_best_location(inp1)
        R2 = get_best_location(inp2)
        if R1 in reg_descriptor.keys():
            print("\tcmp " + R1 + ", " + R2)
        elif R2 in reg_descriptor.keys():
            print("\tcmp " + R1 + ", " + R2)
        else:
            instr.out = inp1
            instr.inp1 = None
            R, flag = get_reg(instr)
            print("\tmov " + R + ", " + R1)
            update_reg_descriptors(R,inp1)
            print("\tcmp " + R + ", " + R2)

        save_context()
        if operator == "geq":
            print("\tjge " + jmp_label)
        elif operator == "gt":
            print("\tjg " + jmp_label)
        elif operator == "leq":
            print("\tjle " + jmp_label)
        elif operator == "lt":
            print("\tjl " + jmp_label)
        elif operator == "eq":
            print("\tje " + jmp_label)
        elif operator == "neq":
            print("\tjne " + jmp_label)

        free_regs(instr)

    def op_goto(self, instr):
        save_context()
        jmp_label = None
        if instr.jmp_to_line != None:
            jmp_label = "line_no_" + str(instr.jmp_to_line)
        else:
            jmp_label = "func_" + instr.jmp_to_label
        print("\tjmp " + jmp_label)

    def op_label(self, instr):
        save_context()
        print("func_" + instr.label_name + ":")

    def op_call_function(self, instr):
        save_context()
        print("\tcall func_" + instr.jmp_to_label)
        if instr.out != None:
            update_reg_descriptors("eax",instr.out)

    def op_return(self, instr):
        if instr.inp1 != None:
            loc = get_best_location(instr.inp1)
            save_reg_contents("eax")
            if loc != "eax":
                print("\tmov eax, " + loc)
            save_context(exclude=["eax"])
        else:
            save_context()
        print("\tret")

    def gen_code(self, instr):
        '''
        Main function which calls other utility functions
        according to instruction type
        '''
        instr_type = instr.instr_type
        if instr.label_to_be_added == True:
            save_context()
            print("line_no_" + str(instr.line_no) + ":")

        if instr_type == "arithmetic":
            if instr.operation == "+":
                self.op_add(instr)
            elif instr.operation == "-":
                self.op_sub(instr)
            elif instr.operation == "*":
                self.op_mult(instr)
            elif instr.operation == "/":
                self.op_div(instr)
            elif instr.operation == "%":
                self.op_modulo(instr)
            elif instr.operation == "<<":
                self.op_lshift(instr)
            elif instr.operation == ">>":
                self.op_rshift(instr)

        elif instr_type == "logical":
            self.op_logical(instr)

        elif instr_type == "assignment":
            self.op_assign(instr)

        elif instr_type == "ifgoto":
            self.op_ifgoto(instr)

        elif instr_type == "goto":
            self.op_goto(instr)

        elif instr_type == "return":
            self.op_return(instr)

        elif instr_type == "label":
            self.op_label(instr)

        elif instr_type == "func_call":
            self.op_call_function(instr)

        elif instr_type == "print_int":
            self.op_print_int(instr)

        elif instr_type == "scan_int":
            self.op_scan_int(instr)

        elif instr_type == "unary":
            self.op_unary(instr)


###################################global generator############################
generator = CodeGenerator()
###################################global generator############################

def next_use(leader, IR_code):
    '''
    This function determines liveness and next
    use information for each statement in basic block by
    performing a backward pass

    Then, it generates assembly code for each basic block
    by making a forward pass

    Finally, it saves all register contents into memory and
    resets the liveness and next use info in symbol table.

    '''
    generator = CodeGenerator()
    for b_start in range(len(leader) -  1):
        # iterate through all basic blocks
        basic_block = IR_code[leader[b_start] - 1:leader[b_start + 1] - 1]
        # for x in basic_block:
            # print(x.line_no)
        # print()
        for instr in reversed(basic_block):
            instr.per_inst_next_use = copy.deepcopy(symbol_table)

            if is_valid_sym(instr.out):
                symbol_table[instr.out].live = False
                symbol_table[instr.out].next_use = None

            if is_valid_sym(instr.inp1):
                symbol_table[instr.inp1].live = True
                symbol_table[instr.inp1].next_use = instr.line_no

            if is_valid_sym(instr.inp2):
                symbol_table[instr.inp2].live = True
                symbol_table[instr.inp2].next_use = instr.line_no

            if instr.array_index_o and is_valid_sym(instr.array_index_o):
                symbol_table[instr.array_index_o].live = True
                symbol_table[instr.array_index_o].next_use = instr.line_no

            if instr.array_index_i1 and is_valid_sym(instr.array_index_i1):
                symbol_table[instr.array_index_i1].live = True
                symbol_table[instr.array_index_i1].next_use = instr.line_no

        for instr in basic_block:
            generator.gen_code(instr)
        # save_context()
        reset_live_and_next_use()

if __name__ == "__main__":
    leader, IR_code = read_three_address_code(sys.argv[1])
    generator.gen_data_section()
    generator.gen_start_template()
    next_use(leader, IR_code)

