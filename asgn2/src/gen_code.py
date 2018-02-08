#!/usr/bin/env python
from get_reg import *
from utilities import *

class CodeGenerator:
    def gen_data_section(self):
        print("section\t.data")
        for symbol in symbol_table.keys():
            if symbol_table[symbol].array_size != None:
                # TODO: DUP required??
                print(str(symbol) + "\ttimes\t" + str(symbol_table[symbol].array_size) + "\tdd\t0")
            else:
                print(str(symbol) + "\tdd\t0")

    def gen_start_template(self):
        print()
        print("section .text")
        print("global _start")
        print("_start:")

    def gen_exit_template(self):
        print()
        print("\tmov eax,1")
        print("\tint 0x80")

    def op_add(self, instr):
        R1, R2, flag = get_reg(instr)
        if flag:
            print("\tmov "+ R1 + "," + instr.inp1)
        if R2 == None:
            R2 = instr.inp2
        print("\tadd " + R1 + "," + R2)


    def op_sub(self, instr):
        pass

    def op_mult(self, instr):
        pass

    def op_div(self, instr):
        pass

    def op_assign(self, instr):
        pass

    def op_logical(self, instr):
        pass

    def op_modulo(self, instr):
        pass

    def gen_code(self, instr):
        instr_type = instr.instr_type
        if instr_type == "arithmetic":
            if instr.operation == "+":
                self.op_add(instr)


def next_use(leader, IR_code):
    '''
    This function determines liveness and next
    use information for each statement in basic block

    Input: first line number of basic block
    '''
    generator = CodeGenerator()
    for b_start in range(len(leader) -  1):
        basic_block = IR_code[leader[b_start] - 1:leader[b_start + 1] - 1]
        # for x in basic_block:
            # print(x.line_no)
        # print()
        for instr in reversed(basic_block):
            if is_valid_sym(instr.out):
                instr.per_inst_next_use[instr.out].live = symbol_table[instr.out].live
                instr.per_inst_next_use[instr.out].next_use = symbol_table[instr.out].next_use
                symbol_table[instr.out].live = False
                symbol_table[instr.out].next_use = None

            if is_valid_sym(instr.inp1):
                instr.per_inst_next_use[instr.inp1].live = symbol_table[instr.inp1].live
                instr.per_inst_next_use[instr.inp1].next_use = symbol_table[instr.inp1].next_use
                symbol_table[instr.inp1].live = True
                symbol_table[instr.inp1].next_use = instr.line_no

            if is_valid_sym(instr.inp2):
                instr.per_inst_next_use[instr.inp2].live = symbol_table[instr.inp2].live
                instr.per_inst_next_use[instr.inp2].next_use = symbol_table[instr.inp2].next_use
                symbol_table[instr.inp2].live = True
                symbol_table[instr.inp2].next_use = instr.line_no

        for instr in basic_block:
            generator.gen_code(instr)

if __name__ == "__main__":
    leader, IR_code = read_three_address_code("../test/test1.csv")
    CodeGenerator().gen_data_section()
    next_use(leader, IR_code)
