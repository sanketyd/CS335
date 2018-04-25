from new_sym_table import ScopeTable
def is_valid_number(symbol):
    if symbol[0] == "-":
        return True
    elif symbol[0] == "'":
        return True
    return symbol.isdigit()

def is_valid_sym(symbol):
    if symbol != None and not is_valid_number(symbol) and symbol[0] != '_':
        return True
    return False

class TAC:
    def __init__(self):
        self.code_list = []
        self.label_count = 0
        self.prefix = ScopeTable().label_prefix

    def emit(self, dest, src1, src2, op, ST):
        # self.code_list.append([dest, src1, src2, op])
        if op in ['*', '/', '%', '+', '-', '>>', '<<', '&', '|', '^']:
            src1 = self.get_name(src1, ST)
            src2 = self.get_name(src2, ST)
            dest = self.get_name(dest, ST)
            self.code_list.append([dest, src1, src2, op])
        elif op == '=':
            src1 = self.get_name(src1, ST)
            dest = self.get_name(dest, ST)
            self.code_list.append([dest, src1, src2, op])
        elif op in ['&&', '||', 'xor']:
            src1 = self.get_name(src1, ST)
            src2 = self.get_name(src2, ST)
            dest = self.get_name(dest, ST)
            self.code_list.append([dest, src1, src2, op])
        elif dest == 'ifgoto':
            x = src2.split(' ')
            src2 = x[1]
            rel = x[0]
            src1 = self.get_name(src1, ST)
            src2 = self.get_name(src2, ST)
            src2 = rel + ' ' + src2
            self.code_list.append([dest, src1, src2, op])
        elif dest == 'param':
            src1 = self.get_name(src1, ST)
            self.code_list.append([dest, src1, src2, op])
        elif dest == 'print':
            src1 = self.get_name(src1, ST)
            self.code_list.append([dest, src1, src2, op])
        elif dest == 'input':
            src1 = self.get_name(src1, ST)
            self.code_list.append([dest, src1, src2, op])
        elif dest == 'scope':
            if src1 == 'begin':
                # ST.curr_scope = str(src2)
                self.code_list.append([dest, src1, src2, op])
            else:
                # ST.curr_scope = ST.get_parent_scope()
                self.code_list.append([dest, src1, src2, op])
        elif dest == 'arg':
            self.code_list.append([dest, self.get_name(src1,ST), src2, op])
        elif dest == 'declare':
            self.code_list.append([dest, self.get_name(src1,ST), self.get_name(src2,ST), op])
        elif dest == 'ret':
            if src1 != '':
                self.code_list.append([dest, self.get_name(src1, ST), src2, op])
            else:
                self.code_list.append([dest, src1, src2, op])
        else:
            self.code_list.append([dest, src1, src2, op])

    def get_name(self, symbol, ST):
        if is_valid_sym(symbol):
            to_return = ""
            if symbol[-1] == "]":
                arr_start = symbol.index('[')
                arr_symbol = symbol[:arr_start]
                index_symbol = symbol[arr_start + 1:-1]
                scope_1 = ST.tac_lookup(arr_symbol)
                if scope_1 != None:
                    to_return += arr_symbol + "_" + scope_1 + "["
                else:
                    to_return += arr_symbol + '['
                if is_valid_sym(index_symbol):
                    scope_2 = ST.tac_lookup(index_symbol)
                    to_return += index_symbol + "_" + scope_2 + "]"
                else:
                    to_return += index_symbol + "]"
                return to_return
            else:
                scope = ST.tac_lookup(symbol)
                if scope == None:
                    return str(symbol)
                return str(symbol) + "_" + str(scope)
        else:
            return symbol

    def generate(self):
        for line_no in range(1,len(self.code_list)+1):
            instruction = self.code_list[line_no - 1]
            dest = instruction[0]
            src1 = instruction[1]
            src2 = instruction[2]
            op = instruction[3]
            if op in ['*', '/', '%', '+', '-', '>>', '<<', '&', '|', '^']:
                if src2 == '1' and op in ['+','-'] and dest == src1:
                    print(str(line_no) + "," + str(op)*2  + "," + str(src1) + "," + str(src1))
                else:
                    print(str(line_no) + "," + str(op) +"," + str(dest) + "," + str(src1) + "," + str(src2))
            elif op == '=':
                print(str(line_no) + ",=," + str(dest) + "," + str(src1))
            elif dest == 'declare':
                print(str(line_no) + ",decl_array," + str(src1) + "[" + str(src2) + "]")
            elif op in ['&&', '||', 'xor']:
                print(str(line_no) + "," + str(op) +"," + str(dest) + "," + str(src1) + "," + str(src2))
            elif dest == 'goto':
                print(str(line_no) + "," + str(dest) + "," + str(src1))
            elif dest == 'ifgoto':
                x = src2.split(' ')
                src2 = x[1]
                rel = x[0]
                print(str(line_no) + "," + str(dest) + "," + rel + "," + str(src1) + "," + str(src2) + "," + str(op))
            elif dest == 'ret':
                if src1 == '':
                    print(str(line_no) + "," + str(dest))
                else:
                    print(str(line_no) + "," + str(dest) + "," + str(src1))
            elif dest == 'label':
                print(str(line_no) + ",label," + str(src1))
            elif dest == 'func':
                print(str(line_no) + ",func," + self.prefix + str(src1))
            elif dest == 'call':
                print(str(line_no) + ",call," + self.prefix + str(src1) + "," + str(src2) + "," + str(op))
            elif dest == 'param':
                print(str(line_no) + ",param," + str(src1))
            elif dest == 'print':
                print(str(line_no) + ",print" +str(op)+ "," + str(src1))
            elif dest == 'input':
                print(str(line_no) + ",input," + str(src1))
            elif dest == 'scope':
                if src1 == 'begin':
                    print(str(line_no) + ",begin," + str(src2))
                else:
                    print(str(line_no) + ",end," + str(src2))
            elif dest == 'arg':
                print(str(line_no) + ",arg," + str(src1))
