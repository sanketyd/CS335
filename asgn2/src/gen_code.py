from get_reg import *
from utilities import *

def gen_data_section():
    print("section\t.data")
    for symbol in symbol_table.keys():
        if symbol_table[symbol].array_size:
            print(str(symbol) + "\tdd\t" + str(symbol_table[symbol].array_size) + "(0)")
        else:
            print(str(symbol) + "\tdd\t0")

def gen_code(instr):
    if instr.instr_type == "arithmetic":
        reg = get_reg(instr)
        print("mov "+str(reg)+","+str(instr.inp1))
        print("add "+str(reg) + "," + str(instr.inp2))

def next_use(leader, IR_code):
    '''
    This function determines liveness and next
    use information for each statement in basic block

    Input: first line number of basic block
    '''
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

            gen_code(instr)

if __name__ == "__main__":
    leader, IR_code = read_three_address_code("../test/test1.csv")
    gen_data_section()
    next_use(leader, IR_code)
