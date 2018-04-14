from utilities import *

#TODO: in function get reg remove outfrom reg_descripto all regs
def communitative_opt(instr):
    if instr.out == instr.inp2:
        return instr.inp2, instr.inp1

    return instr.inp1, instr.inp2

def update_reg_descriptors(reg,symbol):
    reg_descriptor[reg].clear()
    if not is_valid_sym(symbol):
        return
    for register in symbol_table[symbol].address_descriptor_reg:
        if register != reg:
            reg_descriptor[register].remove(symbol)
    symbol_table[symbol].address_descriptor_reg.clear()
    symbol_table[symbol].address_descriptor_reg.add(reg)
    reg_descriptor[reg].add(symbol)

def free_regs(instr):
    if is_valid_sym(instr.inp1):
        if instr.per_inst_next_use[instr.inp1].next_use == None\
                and instr.per_inst_next_use[instr.inp1].live == False:
            for register in symbol_table[instr.inp1].address_descriptor_reg:
                reg_descriptor[register].remove(instr.inp1)
            symbol_table[instr.inp1].address_descriptor_reg.clear()

    if is_valid_sym(instr.inp2):
        if instr.per_inst_next_use[instr.inp2].next_use == None\
                and instr.per_inst_next_use[instr.inp2].live == False:
            for register in symbol_table[instr.inp2].address_descriptor_reg:
                reg_descriptor[register].remove(instr.inp2)
            symbol_table[instr.inp2].address_descriptor_reg.clear()

def get_best_location(symbol,exclude_reg=[]):
    if is_valid_sym(symbol):
        for reg in symbol_table[symbol].address_descriptor_reg:
            if reg not in exclude_reg:
                return reg
        return "[" + symbol + "]"
    elif symbol:
        return "dword " + symbol

def save_context(exclude=[]):
    saved_symbols = set()
    for reg, symbols in reg_descriptor.items():
        if reg not in exclude:
            for symbol in symbols:
                if symbol not in saved_symbols:
                    print("\tmov [" + str(symbol) + "], " + str(reg))
                    symbol_table[symbol].address_descriptor_reg.clear()
                    saved_symbols.add(symbol)
            reg_descriptor[reg].clear()


def save_reg_contents(reg):
    symbols = reg_descriptor[reg]
    for symbol in symbols:
        for location in symbol_table[symbol].address_descriptor_mem:
            print("\tmov ["+ location + "], " + reg)
        symbol_table[symbol].address_descriptor_reg.remove(reg)
    reg_descriptor[reg].clear()


def get_reg(instr, compulsory=True, exclude=[]):
    '''
    Uses next use heuristic to allocate registers
    Returns 2 values:
    1. R1: The best register for inp1
    2. flag: boolean to know whether a register has to be allocated to inp1
    '''
    inp1 = instr.inp1
    inp2 = instr.inp2
    out = instr.out

    if is_valid_sym(out):
        # allocate register for inp1
        if is_valid_sym(inp1):
            for reg_name in symbol_table[inp1].address_descriptor_reg:
                if reg_name not in exclude:
                    if len(reg_descriptor[reg_name]) == 1 \
                            and instr.per_inst_next_use[inp1].next_use == None\
                            and not instr.per_inst_next_use[inp1].live:
                        return reg_name, False

        for key, value in reg_descriptor.items():
            if key not in exclude:
                if len(value) == 0:
                    return key, True

        if compulsory or instr.per_inst_next_use[out].next_use:
            R1 = None
            next_use = -1000000000
            for reg, content in reg_descriptor.items():
                if reg not in exclude:
                    for var in content:
                        n_use = instr.per_inst_next_use[var].next_use
                        if n_use and n_use > next_use:
                            if n_use:
                                next_use = n_use
                            R1 = reg
                        if not n_use:
                            R1 = reg
                            break
            save_reg_contents(R1)
            return R1, True

        else:
            return "[" + out + "]", False
