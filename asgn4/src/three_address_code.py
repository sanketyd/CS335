class TAC:
    def __init__(self):
        self.code_list = []
        self.label_count = 0

    def emit(self, dest, src1, src2, op):
        self.code_list.append([dest, src1, src2, op])

    def error(self, msg):
        pass

    def generate(self):
        for line_no in range(1,len(self.code_list)+1):
            instruction = self.code_list[line_no - 1]
            if instruction[3] in ['*', '/', '%', '+', '-', '>>', '<<', '&', '|', '^']:
                if instruction[2] == '1':
                    print(str(line_no) + ", ++ , " + str(instruction[1]) + ", " + str(instruction[1]))
                else:
                    print(str(line_no) + ", " + str(instruction[3]) +", " + str(instruction[0]) + ", " + str(instruction[1]) + ", " + str(instruction[2]))
            elif instruction[3] == '=':
                print(str(line_no) + ", = , " + str(instruction[0]) + ", " + str(instruction[1]))
            elif instruction[0] == 'declare':
                print("Currently unimplemented: DECLARATION")
            elif instruction[3] in ['and', 'or', 'xor']:
                print("Currently unimplemented: LOGICAL OPS")
            elif instruction[0] == 'goto':
                print(str(line_no) + ", " + str(instruction[0]) + ", " + str(instruction[1]))
            elif instruction[0] == 'ifgoto':
                ## TODO: Check formatting; seems like we need to add extra arguments
                print(str(line_no) + ", " + str(instruction[0]) + ", " + str(instruction[1]) + ", " + str(instruction[2]) + ", " + str(instruction[3]))
            elif instruction[0] == 'ret':
                # There are 2 cases return a or just return type
                # TODO: HAndle in both code generator and IR generator
                print(str(line_no) + ", " + str(instruction[0]) + ", " + str(instruction[1]))
            elif instruction[0] == 'label' or instruction[0] == 'func':
                print(str(line_no) + ", label, " + str(instruction[1]))
            elif instruction[0] == 'call':
                print(str(line_no) + ", call, " + str(instruction[1]) + ", " + str(instruction[2]))
            elif instruction[0] == 'param':
                print(str(line_no) + ", param, " + str(instruction[1]))
            elif instruction[0] == 'print':
                print(str(line_no) + ", print, " + str(instruction[1]))
