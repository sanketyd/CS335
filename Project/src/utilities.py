import sys
import csv
from LALR_parser import *
import global_vars as g

leader_instructions = [
    "ifgoto",
    "return",
    "label",
    "call",
    "print_int",
    "scan_int",
    "goto",
    "func",
    "begin_func",
    "end_func"
]

reg_descriptor = dict()


reg_descriptor["ebx"] = set()
reg_descriptor["ecx"] = set()
reg_descriptor["esi"] = set()
reg_descriptor["edi"] = set()
reg_descriptor["edx"] = set()
reg_descriptor["eax"] = set()

func_symbol_table = None

def is_temp_var(symbol):
    if symbol[0] == "_":
        return True
    return False

def reset_live_and_next_use():
    for symbol in g.symbol_table.keys():
        g.symbol_table[symbol].live = True
        g.symbol_table[symbol].next_use = None
    return g.symbol_table

def is_valid_number(symbol):
    if symbol[0] == "-":
        return True
    return symbol.isdigit()

def is_valid_sym(symbol):
    if type(symbol) != type(''):
        return False
    elif symbol != None and not is_valid_number(symbol):
        return True
    return False

class SymbolTableEntry:
    def __init__(self):
        # self.value = None
        self.live = True
        self.next_use = None
        self.array_size = None
        self.address_descriptor_mem = set()
        self.address_descriptor_reg = set()


class Instruction:
    def __init__(self, statement):
        self.line_no = int(statement[0].strip())
        self.label_to_be_added = False
        self.inp1 = None
        self.array_index_i1 = None
        self.inp2 = None
        self.array_index_i2 = None
        self.out = None
        self.array_index_o = None
        self.operation = None
        self.instr_type = None
        self.label_name = None
        self.jmp_to_line = None
        self.jmp_to_label = None
        self.table = None
        self.per_inst_next_use = dict()
        self.build(statement)
        self.populate_per_inst_next_use()
        self.arg_set = []

    def add_to_symbol_table(self, symbols, is_array_dec=False):
        '''
        Add the symbol into symbol table if not already exists
        '''
        if not is_array_dec:
            for symbol in symbols:
                if is_valid_sym(symbol):
                    if is_temp_var(symbol):
                        g.temp_var_count += 1
                    global func_symbol_table
                    if symbol not in func_symbol_table.keys():
                        func_symbol_table[symbol] = SymbolTableEntry()
                        if is_temp_var(symbol):
                            func_symbol_table[symbol].address_descriptor_mem.add(symbol)
        else:
            # an array is declared: arr[100]
            # store 'symbols[0]` in symbol table if not already present
            # set size  of array to `symbols[1]`
            if is_valid_sym(symbols[0]):
                if symbols[0] not in g.symbol_table.keys():
                    g.symbol_table[symbols[0]] = SymbolTableEntry()
                    g.symbol_table[symbols[0]].address_descriptor_mem.add(symbols[0])
                    g.symbol_table[symbols[0]].array_size = symbols[1]


    def handle_array_notation(self, symbol):
        '''
        Given a symbol, possibly in the form of a[i],
        split into `a` and index `i`
        '''
        index = symbol.find("[")
        if index != -1:
            return symbol[:index], symbol[index + 1:-1]
        else:
            return symbol, None


    def build(self, statement):
        '''
        Populate appropriate entries of Instruction class
        according to instruction type
        '''
        instr_type = statement[1].strip()
        if instr_type == "ifgoto":
            # 10, ifgoto, leq, a, 50, 2
            self.instr_type = "ifgoto"
            self.operation = statement[2].strip()

            self.inp1, self.array_index_i1 = self.handle_array_notation(statement[3].strip())
            self.inp2, self.array_index_i2 = self.handle_array_notation(statement[4].strip())
            self.add_to_symbol_table([
                self.inp1, self.array_index_i1,
                self.inp2, self.array_index_i2
            ])

            jmp_location = statement[-1].strip()
            if jmp_location.isdigit():
                self.jmp_to_line = jmp_location
            else:
                self.jmp_to_label = jmp_location

        elif instr_type == "goto":
            self.instr_type = "goto"

            jmp_location = statement[-1].strip()
            if jmp_location.isdigit():
                self.jmp_to_line = jmp_location
            else:
                self.jmp_to_label = jmp_location

        elif instr_type == "print":
            # 10, print, variable
            self.instr_type = "print_int"
            self.inp1, self.array_index_i1 = self.handle_array_notation(statement[-1].strip())
            self.add_to_symbol_table([self.inp1, self.array_index_i1])

        elif instr_type == "input":
            # 10, input, variable
            self.instr_type = "scan_int"
            self.out, self.array_index_o = self.handle_array_notation(statement[-1].strip())
            self.add_to_symbol_table([self.out, self.array_index_o])

        elif instr_type in ["~","!","++","--"]:
            #10, ++, out, variable
            self.operation = instr_type
            self.instr_type = "unary"
            self.inp1, self.array_index_i1 = self.handle_array_notation(statement[-1].strip())
            self.out, self.array_index_o = self.handle_array_notation(statement[2].strip())
            self.add_to_symbol_table([
                self.inp1, self.array_index_i1,
                self.out, self.array_index_o
            ])
        elif instr_type == "param":
            self.instr_type = "param"
            self.inp1 = statement[-1].strip()

        elif instr_type == "call":
            # 10, call, label_name
            # OR
            # 10, call, label_name, optional_return, no.of params
            self.instr_type = "func_call"
            if len(statement) == 3:
                self.jmp_to_label = statement[-1].strip()
            else:
                self.jmp_to_label = statement[2].strip()
                self.out = statement[3].strip()
                self.inp1 = statement[-1].strip()
                self.add_to_symbol_table(self.out)

        elif instr_type == "label":
            # 10, label, label_name
            self.instr_type = "label"
            self.label_name = statement[-1].strip()

        elif instr_type == "func":
            self.instr_type = "func"
            self.label_name = statement[-1].strip()

        elif instr_type == "begin":
            self.instr_type = "begin_scope"
            self.label_name = statement[-1].strip()

        elif instr_type == "arg":
            self.instr_type = "arg"
            self.inp1 = statement[-1].strip()

        elif instr_type == "end":
            self.instr_type = "end_scope"
            self.label_name = statement[-1].strip()

        elif instr_type == "ret":
            self.instr_type = "return"
            if len(statement) == 3:
                self.inp1 = statement[-1].strip()

        elif instr_type == "=":
            # 10, =, a, 2
            self.instr_type = "assignment"
            self.operation = "="
            self.inp1, self.array_index_i1 = self.handle_array_notation(statement[-1].strip())
            self.out, self.array_index_o = self.handle_array_notation(statement[2].strip())
            self.add_to_symbol_table([
                self.inp1, self.array_index_i1,
                self.out, self.array_index_o
            ])

        elif instr_type == "decl_array":
            self.instr_type = "array_declaration"
            self.inp1, self.array_index_i1 = self.handle_array_notation(statement[-1].strip())
            self.add_to_symbol_table([self.inp1, self.array_index_i1], True)

        elif instr_type in ["|", "||", "&", "&&", "^", "~", "!"]:
            # 10, &&, a, a, b
            self.instr_type = "logical"
            self.inp1, self.array_index_i1 = self.handle_array_notation(statement[3].strip())
            self.inp2, self.array_index_i2 = self.handle_array_notation(statement[4].strip())
            self.out, self.array_index_o = self.handle_array_notation(statement[2].strip())
            self.add_to_symbol_table([
                self.inp1, self.array_index_i1,
                self.inp2, self.array_index_i2,
                self.out, self.array_index_o
            ])
            self.operation = statement[1].strip()

        else:
            # 10, +, a, a, b
            self.instr_type = "arithmetic"
            self.inp1, self.array_index_i1 = self.handle_array_notation(statement[3].strip())
            self.inp2, self.array_index_i2 = self.handle_array_notation(statement[4].strip())
            self.out, self.array_index_o = self.handle_array_notation(statement[2].strip())
            self.add_to_symbol_table([
                self.inp1, self.array_index_i1,
                self.inp2, self.array_index_i2,
                self.out, self.array_index_o
            ])
            self.operation = statement[1].strip()


    def populate_per_inst_next_use(self):
        return
        '''
        for each symbol in instruction, initialize the next use
        and liveness parameters
        '''
        symbols = [
                self.inp1, self.array_index_i1,
                self.inp2, self.array_index_i2,
                self.out, self.array_index_o
            ]
        for symbol in symbols:
            if is_valid_sym(symbol):
                self.per_inst_next_use[symbol] = SymbolTableEntry()


def read_three_address_code(filename):
    '''
    Given a csv file `filename`, read the file
    and find the basic blocks. Also store each instruction
    as an instance of Instruction class in a list `IR_code`
    '''
    leader = set()
    leader.add(1)
    IR_code = []
    last_func = None
    arg_set = None
    with open(filename, 'r') as csvfile:
        instruction_set = list(csv.reader(csvfile, delimiter=','))
        index_label_to_be_added = set()
        for i,statement in enumerate(instruction_set):
            if len(statement) == 0:
                continue
            IR = Instruction(statement)
            IR_code.append(IR)
            line_no = IR.line_no
            instr_type = IR.instr_type

            if instr_type == "begin_scope":
                if instruction_set[i+1][1].strip() == "func":
                    IR_code[i].instr_type = "begin_func"
                    arg_set = []
                    global func_symbol_table
                    func_symbol_table = dict()
                    last_func = {
                        'label' : statement[2],
                        'index' : i
                    }

            if instr_type == "arg":
                arg_set.append(IR.inp1)

            if instr_type == "end_scope":
                if statement[2] == last_func['label']:
                    IR_code[i].instr_type = "end_func"
                    IR_code[last_func['index']].table = func_symbol_table
                    IR_code[last_func['index']].arg_set = arg_set
                    last_func = None
                    func_symbol_table = None

            instr_type = IR_code[i].instr_type
            if instr_type in leader_instructions:
                if instr_type != "label" and instr_type != "print_int" and instr_type != "scan_int" and instr_type != "func":
                    line_no += 1

                leader.add(line_no)

            if instr_type == "ifgoto" or instr_type == "goto":
                goto_line = statement[-1].strip()
                if goto_line.isdigit():
                    goto_line = int(goto_line)
                    leader.add(goto_line)
                    index_label_to_be_added.add(goto_line - 1)
                    # IR_code[goto_line - 1].label_to_be_added = True
        for index in index_label_to_be_added:
            IR_code[index].label_to_be_added = True
    leader.add(len(IR_code)+1)

    return (sorted(leader), IR_code)
