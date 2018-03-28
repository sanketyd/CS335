SymbolTable = dict()
curr_scope = 'main'
label_no = 0


class symbol_table:
    def __init__(self):
        self.scope_name = 'main'
        self.parent = None
        self.scopes = dict()
        self.symbols = dict()

    def make_table(self, previous):
        # new_scope = 'yoyo'
        new_scope = self.get_label()
        print(label_no)
        SymbolTable[new_scope] = symbol_table()
        SymbolTable[new_scope].scope_name = new_scope
        SymbolTable[new_scope].parent = previous
        return new_scope

    def enter(self, idName, idType, isArray=False, arr_size=None, offset=None):
        if idName in self.symbols.keys():
            raise Exception('Ae chutiye phle se hi hai!')
        self.symbols[idName] = {
            'type' : idType,
            'offset' : offset,
            'isArray' : isArray,
            'arr_size' : arr_size
        }

    def enterproc(self, func_name, params=[], ret_type=None, is_func=False):
        if is_func is True:
            # new block is due to functions
            if func_name in self.scopes.keys():
                raise Exception('Pehle se h bc!!')
            self.scopes[func_name] = {
                'category' : 'function',
                'n_params' : len(params),
                'params' : params,
                'ret_type' : ret_type
            }
        else:
            # new block is due to if/while/for...
            self.scopes[func_name] = {
                'category' : 'misc',
            }

    def end_scope(self):
        return SymbolTable[curr_scope].parent

    def look_up(self, symbol):
        scope = curr_scope
        while scope != None:
            if symbol in SymbolTable[scope].symbols:
                return True
            scope = SymbolTable[scope].parent
        return False

    def get_label(self):
        global label_no
        label_no += 1
        return "kuch_acha_naam_" + str(label_no)

SymbolTable['main'] = symbol_table()

if __name__ == "__main__":
    SymbolTable[curr_scope].enter('x', 'int')
    SymbolTable[curr_scope].enter('y', 'int')
    SymbolTable[curr_scope].enterproc('panda')
    curr_scope = SymbolTable[curr_scope].make_table(curr_scope)
    SymbolTable[curr_scope].enter('x','int')
    print(SymbolTable[curr_scope].look_up('y'))
    print(SymbolTable[curr_scope].end_scope())
