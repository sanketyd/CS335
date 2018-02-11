import sys
import csv

leader_instructions = [
    "ifgoto",
    "ret",
    "label",
    "call",
    "print_int",
    "scan_int",
    "goto"
]

symbol_table = dict()
reg_descriptor = dict()

reg_descriptor["ebx"] = set()
reg_descriptor["ecx"] = set()
reg_descriptor["esi"] = set()
reg_descriptor["edi"] = set()
reg_descriptor["edx"] = set()
reg_descriptor["eax"] = set()

def reset_live_and_next_use():
    for symbol in symbol_table.keys():
        symbol_table[symbol].live = True
        symbol_table[symbol].next_use = None

def is_valid_number(symbol):
    if symbol[0] == "-":
        return True
    return symbol.isdigit()

def is_valid_sym(symbol):
    if symbol != None and not is_valid_number(symbol):
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
        self.per_inst_next_use = dict()
        self.build(statement)
        self.populate_per_inst_next_use()

    def add_to_symbol_table(self, symbols, is_array_dec=False):
        '''
        Add the symbol into symbol table if not already exists
        '''
        if not is_array_dec:
            for symbol in symbols:
                if is_valid_sym(symbol):
                    if symbol not in symbol_table.keys():
                        symbol_table[symbol] = SymbolTableEntry()
                        symbol_table[symbol].address_descriptor_mem.add(symbol)
        else:
            # an array is declared: arr[100]
            # store 'symbols[0]` in symbol table if not already present
            # set size  of array to `symbols[1]`
            if is_valid_sym(symbols[0]):
                if symbols[0] not in symbol_table.keys():
                    symbol_table[symbols[0]] = SymbolTableEntry()
                    symbol_table[symbols[0]].address_descriptor_mem.add(symbols[0])
                    symbol_table[symbols[0]].array_size = symbols[1]


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
            self.inp1, self.array_index_i1 = self.handle_array_notation(statement[-1].strip())
            self.add_to_symbol_table([self.inp1, self.array_index_i1])

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
        elif instr_type == "call":
            # 10, call, label_name
            # OR
            # 10, call, label_name, optional_return
            self.instr_type = "func_call"
            if len(statement) == 3:
                self.jmp_to_label = statement[-1].strip()
            else:
                self.jmp_to_label = statement[2].strip()
                self.out = statement[-1].strip()
                self.add_to_symbol_table(self.out)

        elif instr_type == "label":
            # 10, label, label_name
            self.instr_type = "label"
            self.label_name = statement[-1].strip()

        elif instr_type == "ret":
            self.instr_type = "return"
            if len(statement) == 3:
                self.out = statement[-1].strip()

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
    with open(filename, 'r') as csvfile:
        instruction_set = csv.reader(csvfile, delimiter=',')
        index_label_to_be_added = set()
        for statement in instruction_set:
            if len(statement) == 0:
                continue
            IR = Instruction(statement)
            IR_code.append(IR)
            line_no = IR.line_no
            instr_type = IR.instr_type
            if instr_type in leader_instructions:
                if instr_type != "label" and instr_type != "print_int":
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
