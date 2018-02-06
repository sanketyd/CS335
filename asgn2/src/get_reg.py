from utilities import *

def is_any_reg_empty():
    for reg in reg_descriptor.keys():
        if reg_descriptor[reg] == None:
            return reg
    return  None

def get_reg_by_replacement(var_list):
    next_use = 100000000
    reg = None
    for regi,var in reg_descriptor:
        if var not in var_list and symbol_table[var].next_use < next_use:
            next_use = symbol_table[var].next_use
            reg = regi
    symbol_table[reg_descriptor[reg]].address_descriptor_reg  = None
    #TODO: Save variable in m,emory if it's not alrready in there
    return reg


def get_reg(instr):
    inp1 = instr.inp1
    inp2 = instr.inp2
    out = instr.out

    if inp1 != None and not isdigit(inp1):
        if len(symbol_table[inp1].address_descriptor_reg) != 0:
            inp1_reg = next(iter(symbol_table[inp1].address_descriptor_reg))
        elif (empty_reg = is_any_reg_empty()) != None:
            inp1_reg = empty_reg
        else:
            # the difficult case
            inp1_reg = get_reg_by_replacement(inp1,inp2,out)

    if inp2 != None and not isdigit(inp2):
        if len(symbol_table[inp2].address_descriptor_reg) != 0:
            inp2_reg = next(iter(symbol_table[inp2].address_descriptor_reg))
        elif (empty_reg = is_any_reg_empty()) != None:
            inp2_reg = empty_reg
        else:
            # the difficult case
            inp2_reg = get_reg_by_replacement([inp1,inp2,out])

    if out != None and not isdigit(out):
