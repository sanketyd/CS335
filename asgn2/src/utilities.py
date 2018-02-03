import sys
import csv

typee_of_ops = [
        "cond_jump"
        ]

class Instruction:
    def __init__(self):
        self.line_no           = -1     # line number of instr
        self.op                = None   # operator
        self.inp1              = None   # operand1
        self.inp2              = None   # operand2
        self.out               = None   # output var
        self.label             = None   # label name, if any
        self.jmp_to_line       = None   # jump(if any) to which line number
        self.jmp_to_label      = None   # jump(if any) to which label name
        self.library_func_name = None   # which library func is used(if any)

    def build(self, line):
        '''
        Given a string in 3 Address Codde form,
        build the required structure for IR
        representation
        '''
        self.line_no = int(line[0].strip())
        op_type = line[1].strip()
        # possibilities for op_type
        #     ->  +, -, *, /
        #     ->  =
        #     ->  ifgoto
        #     ->  call
        #     ->  ret
        #     ->  label
        #     ->  print
        if op_type == "ifgoto":
            self.op = line[2].strip()
            self.inp1 = line[3].strip()
            self.inp2 = line[4].strip()
            self.jmp_to_line = line[5].strip()
        elif op_type == "call":
            self.jmp_to_label = line[2].strip()
        elif op_type == "ret":
            self.library_func_name = "return"
        elif op_type == "label":
            self.label = param[2].strip()
        elif op_type == "print":
            self.inp1 = line[2].strip()
            self.library_func_name = "print"
        elif op_type == "=":
            self.op = op_type
            # TODO
        else:
            self.op = op_type
            self.out = line[2].strip()
            self.inp1 = line[3].strip()
            self.inp2 = line[4].strip()


def read_three_address_code(filename):
    '''
    Given a csv file `filename`, read the file
    and store it as a list of Instruction objects
    '''
    IR_code = []
    with open(filename, 'r') as csvfile:
        instruction_set = csv.reader(csvfile, delimiter=',')
        for line in instruction_set:
            instruction = Instruction()
            instruction.build(line)
            IR_code.append(instruction)
    return IR_code
