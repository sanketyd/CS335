from utilities import *

def save_reg_contents(variables):
    pass

def get_reg(instr):
    inp1 = instr.inp1
    inp2 = instr.inp2
    out = instr.out

    # if inp1 != None and not isdigit(inp1):
        # if len(symbol_table[inp1].address_descriptor_reg) != 0:
            # inp1_reg = next(iter(symbol_table[inp1].address_descriptor_reg))
        # elif (empty_reg = is_any_reg_empty()) != None:
            # inp1_reg = empty_reg
        # else:
            # # the difficult case
            # inp1_reg = get_reg_by_replacement(inp1,inp2,out)

    # if inp2 != None and not isdigit(inp2):
        # if len(symbol_table[inp2].address_descriptor_reg) != 0:
            # inp2_reg = next(iter(symbol_table[inp2].address_descriptor_reg))
        # elif (empty_reg = is_any_reg_empty()) != None:
            # inp2_reg = empty_reg
        # else:
            # # the difficult case
            # inp2_reg = get_reg_by_replacement([inp1,inp2,out])

    if is_valid_sym(out):
        for reg_name in symbol_table[inp1].address_descriptor_reg:
            if len(reg_descriptor[reg_name]) == 1 and instr.per_inst_next_use[inp1].next_use == None:
                return reg_name
        for key, value in reg_descriptor:
            if len(value) == 0:
                return key

        if instr.per_inst_next_use[out].next_use != None:
            next_use = -1000000000
            R = None
            for reg,content in reg_descriptor:
                for var in content:
                    n_use = symbol_table[var].next_use
                    if n_use > next_use:
                        next_use = n_use
                        R = reg
            save_reg_contents(reg_descriptor[R])
            return R

        return None
