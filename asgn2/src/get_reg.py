from utilities import *

#TODO: in function get reg remove outfrom reg_descripto all regs
def get_best_location(symbol):
    if is_valid_sym(symbol):
        if len(symbol_table[symbol].address_descriptor_reg):
            return next(iter(symbol_table[symbol].address_descriptor_reg))
        else:
            return "[" + symbol + "]"
    elif symbol:
        return "dword " + symbol

def save_context():
    for reg, symbols in reg_descriptor.items():
        for symbol in symbols:
            print("\tmov [" + str(symbol) + "], " + str(reg))
            symbol_table[symbol].address_descriptor_reg.clear()
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
    Returns 3 values:
    1. R1: The best register for inp1
    2. R2: if inp2 is already in a register, returns it, otherwise None
    3. flag: boolean to know whether a register has to be allocated to inp1
    '''
    inp1 = instr.inp1
    inp2 = instr.inp2
    out = instr.out

    if is_valid_sym(out):
        # allocate register for inp1
        if is_valid_sym(inp1):
            for reg_name in symbol_table[inp1].address_descriptor_reg:
                if reg_name not in exclude:
                    if len(reg_descriptor[reg_name]) == 1 and instr.per_inst_next_use[inp1].next_use == None:
                        ###############
                        reg_descriptor[reg_name].remove(inp1)
                        symbol_table[inp1].address_descriptor_reg.remove(reg_name)
                        if instr.operation != "/" and instr.operation != "%":
                            reg_descriptor[reg_name].add(out)
                            symbol_table[out].address_descriptor_reg.add(reg_name)
                        ##############
                        return reg_name, False

        for key, value in reg_descriptor.items():
            if key not in exclude:
                if len(value) == 0:
                    ###############
                    if instr.operation != "/" and instr.operation != "%":
                        reg_descriptor[key].add(out)
                        symbol_table[out].address_descriptor_reg.add(key)
                    ##############
                    return key, True

        if compulsory or per_inst_next_use[out].next_use:
            R1 = None
            next_use = -1000000000
            for reg, content in reg_descriptor.items():
                if reg not in exclude:
                    for var in content:
                        n_use = symbol_table[var].next_use
                        if n_use and n_use > next_use:
                            next_use = n_use
                            R1 = reg
            save_reg_contents(R1)


            if instr.operation != "/" and instr.operation != "%":
                reg_descriptor[R1].add(out)
                symbol_table[out].address_descriptor_reg.add(R1)

            return R1, True

        else:
            return "[" + out +"]", False
