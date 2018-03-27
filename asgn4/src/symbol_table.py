SymbolTable = dict()
curr_scope = 'main'

class symbol_table:
    def __init__(self):
        self.scope_name = 'main'
        self.parent = None
        self.scopes = set()
        self.symbols = dict()

    def make_table(self, previous):
        new_scope = 'yoyo'
        SymbolTable[new_scope] = symbol_table()
        SymbolTable[new_scope].scope_name = new_scope
        SymbolTable[new_scope].parent = previous
        return new_scope

    def enter(self, idName, idType, offset=None):
        if idName in self.symbols.keys():
            raise Exception('Ae chutiye phle se hi hai!')
        self.symbols[idName] = {
            'type' : idType,
            'offset' : offset
        }

    def enterproc(self, func_name):
        self.scopes.add(func_name)

    def end_scope(self):
        return SymbolTable[curr_scope].parent

SymbolTable['main'] = symbol_table()

if __name__ == "__main__":
    SymbolTable[curr_scope].enter('x', 'int')
    SymbolTable[curr_scope].enter('y', 'int')
    SymbolTable[curr_scope].enterproc('panda')
    curr_scope = SymbolTable[curr_scope].make_table(curr_scope)
    SymbolTable[curr_scope].enter('x','int')
    print(SymbolTable[curr_scope].end_scope())
