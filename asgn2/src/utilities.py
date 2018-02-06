import sys
import csv

leader_instructions = [
    "ifgoto",
    "ret",
    "label",
    "call"
]

library_funcs = [
    "print",
    "input"
]

symbol_table = dict()

reg_descriptor = dict()

reg_descriptor["eax"] = set()
reg_descriptor["ebx"] = set()
reg_descriptor["ecx"] = set()
reg_descriptor["edx"] = set()
reg_descriptor["esi"] = set()
reg_descriptor["edi"] = set()


class SymbolTableEntry:
    def __init__(self):
        self.live = False #Made it false
        self.next_use = None
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

    def add_to_symbol_table(self, symbols):
        '''
        Add the symbol into symbol table if not already exists
        '''
        for symbol in symbols:
            if symbol != None and not symbol.isdigit():
                if symbol not in symbol_table:
                    symbol_table[symbol] = SymbolTableEntry()


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
        # analyse the statement and split it
        # add to symbol table
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

        elif instr_type == "print":
            # 10, print, variable
            self.instr_type = "library_func"
            self.inp1, self.array_index_i1 = self.handle_array_notation(statement[-1].strip())
            self.add_to_symbol_table([self.inp1, self.array_index_i1])

        elif instr_type == "call":
            # 10, call, label_name
            self.instr_type = "func_call"
            self.jmp_to_label = statement[-1].strip()

        elif instr_type == "label":
            # 10, label, label_name
            self.instr_type = "label"
            self.label_name = statement[-1].strip()

        elif instr_type == "ret":
            self.instr_type = "return"

        elif instr_type == "=":
            # 10, =, a, 2
            self.instr_type = "assignment"
            self.inp1, self.array_index_i1 = self.handle_array_notation(statement[-1].strip())
            self.out, self.array_index_o = self.handle_array_notation(statement[2].strip())
            self.add_to_symbol_table([
                self.inp1, self.array_index_i1,
                self.out, self.array_index_o
            ])

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
        symbols = [
                self.inp1, self.array_index_i1,
                self.inp2, self.array_index_i2,
                self.out, self.array_index_o
            ]
        for symbol in symbols:
            if symbol != None and not symbol.isdigit():
                self.per_inst_next_use[symbol] = SymbolTableEntry()


def read_three_address_code(filename):
    '''
    Given a csv file `filename`, read the file
    and find the basic blocks
    '''
    leader = set()
    leader.add(1)
    IR_code = []
    with open(filename, 'r') as csvfile:
        instruction_set = csv.reader(csvfile, delimiter=',')
        for statement in instruction_set:
            IR = Instruction(statement)
            IR_code.append(IR)
            line_no = IR.line_no
            instr_type = IR.instr_type
            if instr_type in leader_instructions:
                if instr_type != "label":
                    line_no += 1
                leader.add(line_no)
            if instr_type == "ifgoto":
                goto_line = statement[-1].strip()
                if goto_line.isdigit():
                    goto_line = int(goto_line)
                    leader.add(goto_line)
                    IR_code[goto_line - 1].label_to_be_added = True

    return (sorted(leader), IR_code)


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
            if not instr.out == None and not instr.out.isdigit():
                instr.per_inst_next_use[instr.out].live = symbol_table[instr.out].live
                instr.per_inst_next_use[instr.out].next_use = symbol_table[instr.out].next_use
                symbol_table[instr.out].live = False
                symbol_table[instr.out].next_use = None

            if not instr.inp1 == None and not instr.inp1.isdigit():
                instr.per_inst_next_use[instr.inp1].live = symbol_table[instr.inp1].live
                instr.per_inst_next_use[instr.inp1].next_use = symbol_table[instr.inp1].next_use
                symbol_table[instr.inp1].live = True
                symbol_table[instr.inp1].next_use = instr.line_no

            if not instr.inp2 == None and not instr.inp2.isdigit():
                instr.per_inst_next_use[instr.inp2].live = symbol_table[instr.inp2].live
                instr.per_inst_next_use[instr.inp2].next_use = symbol_table[instr.inp2].next_use
                symbol_table[instr.inp2].live = True
                symbol_table[instr.inp2].next_use = instr.line_no


leader, IR_code = read_three_address_code("../test/test1.csv")
print(leader)
next_use(leader, IR_code)
