import sys
import csv

class Instruction:
    def __init__(self):
        self.line_no = -1
        self.op = None
        self.inp1 = None
        self.inp2 = None
        self.out = None
        self.label = None

    def build(self, line):
        '''
        Given a string in 3 Address Codde form,
        build the required structure for IR
        representation
        '''
        pass


def read_three_address_code(filename):
    '''
    Given a csv file `filename`, read the file
    and store it as a list of Instruction objects
    '''
    with open(filename, 'r') as csvfile:
        instruction_set = csv.reader(csvfile, delimiter=',')
        for line in instruction_set:
            instruction = Instruction()
            instruction.build(line)
            IR_code.append(instruction)
    return IR_code
