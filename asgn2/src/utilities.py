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


class SymbolTableEntry:
    def __init__():
        self.live = False #Made it false
        self.next_use = None

    def add_address_descriptor(): #Added this because we don't need it in per instruction page table
        self.address_descriptor = set()


class Instruction:
    def __init__(self, statement):
        self.line_no = int(statement[0].strip())
        self.label_to_be_added = False
        self.inp1 = None
        self.inp2 = None
        self.out = None
        self.operation = None
        self.instr_type = None
        self.label_name = None
        self.jmp_to_line = None
        self.jmp_to_label = None
        self.per_inst_next_use = dict()
        self.build(statement)

    def build(self, statement):
        # TODO:
        # analyse the statement and split it
        # add to symbol table
        # Also intialize per instruction next use details as nextuse = None & live = False
        pass



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
            instr_type = statement[1].strip()
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
            if not isdigit(instr.out) and not instr.out == None:
                instr.per_inst_next_use[instr.out].live = symbol_table[instr.out].live
                instr.per_inst_next_use[instr.out].next_use = symbol_table[instr.out].next_use
                symbol_table[instr.out].live = False
                symbol_table[instr.out].next_use = None

            if not isdigit(instr.inp1) and not instr.inp1 == None:
                instr.per_inst_next_use[instr.inp1].live = symbol_table[instr.inp1].live
                instr.per_inst_next_use[instr.inp1].next_use = symbol_table[instr.inp1].next_use
                symbol_table[instr.inp1].live = True
                symbol_table[instr.inp1].next_use = instr.line_no

            if not isdigit(instr.inp2) and not instr.inp2 == None:
                instr.per_inst_next_use[instr.inp2].live = symbol_table[instr.inp2].live
                instr.per_inst_next_use[instr.inp2].next_use = symbol_table[instr.inp2].next_use
                symbol_table[instr.inp2].live = True
                symbol_table[instr.inp2].next_use = instr.line_no




leader, IR_code = read_three_address_code("../test/test1.csv")
print(leader)
next_use(leader, IR_code)
