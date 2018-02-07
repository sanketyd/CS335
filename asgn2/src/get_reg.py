from utilities import *

#TODO: update address descriptor and register descriptor in both
def save_reg_contents(reg):
    symbols = reg_descriptor[reg]
    for symbol in symbols:
        for location in symbol_table[symbol].address_descriptor_mem:
            print("mov "+ "reg," + str(location))


def get_reg(instr):
    inp1 = instr.inp1
    inp2 = instr.inp2
    out = instr.out

    if is_valid_sym(out):
        print("Hi there!")
        if is_valid_sym(inp1):
            for reg_name in symbol_table[inp1].address_descriptor_reg:
                if len(reg_descriptor[reg_name]) == 1 and instr.per_inst_next_use[inp1].next_use == None:
                    return reg_name

        for key, value in reg_descriptor.items():
            if len(value) == 0:
                return key

        next_use = -1000000000
        R = None
        for reg,content in reg_descriptor:
            for var in content:
                n_use = symbol_table[var].next_use
                if n_use > next_use:
                    next_use = n_use
                    R = reg
        save_reg_contents(R)
        return R
