from new_sym_table import ScopeTable
class TAC:
    def __init__(self):
        self.code_list = []
        self.label_count = 0
        self.prefix = ScopeTable().label_prefix

    def emit(self, dest, src1, src2, op):
        self.code_list.append([dest, src1, src2, op])

    def error(self, msg):
        pass

    def generate(self):
        for line_no in range(1,len(self.code_list)+1):
            instruction = self.code_list[line_no - 1]
            if instruction[3] in ['*', '/', '%', '+', '-', '>>', '<<', '&', '|', '^']:
                if instruction[2] == '1' and instruction[3] in ['+','-']:
                    print(str(line_no) + ", " + str(instruction[3])*2  + " , " + str(instruction[1]) + ", " + str(instruction[1]))
                else:
                    print(str(line_no) + ", " + str(instruction[3]) +", " + str(instruction[0]) + ", " + str(instruction[1]) + ", " + str(instruction[2]))
            elif instruction[3] == '=':
                print(str(line_no) + ", = , " + str(instruction[0]) + ", " + str(instruction[1]))
            elif instruction[0] == 'declare':
                print("Currently unimplemented: DECLARATION")
            elif instruction[3] in ['&&', '||', 'xor']:
                print(str(line_no) + ", " + str(instruction[3]) +", " + str(instruction[0]) + ", " + str(instruction[1]) + ", " + str(instruction[2]))
            elif instruction[0] == 'goto':
                print(str(line_no) + ", " + str(instruction[0]) + ", " + str(instruction[1]))
            elif instruction[0] == 'ifgoto':
                ## TODO: Check formatting; seems like we need to add extra arguments
                print(str(line_no) + ", " + str(instruction[0]) + ", " + str(instruction[1]) + ", " + str(instruction[2]) + ", " + str(instruction[3]))
            elif instruction[0] == 'ret':
                print(str(line_no) + ", " + str(instruction[0]) + ", " + str(instruction[1]))
            elif instruction[0] == 'label':
                print(str(line_no) + ", label, " + str(instruction[1]))
            elif instruction[0] == 'func':
                print(str(line_no) + ", label, " + self.prefix + str(instruction[1]))
            elif instruction[0] == 'call':
                print(str(line_no) + ", call, " + self.prefix + str(instruction[1]) + ", " + str(instruction[2]))
            elif instruction[0] == 'param':
                print(str(line_no) + ", param, " + str(instruction[1]))
            elif instruction[0] == 'print':
                print(str(line_no) + ", print, " + str(instruction[1]))
