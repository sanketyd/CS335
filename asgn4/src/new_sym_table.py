class ScopeTable:
    def __init__(self):
        '''
        Maintains a list of all symbol tables in program
        '''
        self.label_counter = 0
        self.curr_scope = 'start'
        self.curr_sym_table = SymbolTable(self.curr_scope, parent=None)
        self.symbol_and_table_map = dict()


    def create_new_table(self, new_label)
        '''
        Creates a new symbol table. If func_name is provided,
        that name is used for scope
        O/W, custom label is provided
        '''
        new_sym_table = SymbolTable(new_label, self.curr_scope)
        self.curr_scope = new_label
        self.scope_and_table_map[curr_cope] = new_sym_table


    def end_scope(self):
        # change the name for curr_cope only
        self.curr_scope = self.scope_and_table_map[self.curr_scope].parent


    def lookup(self, symbol, is_func=False):
        scope = self.curr_scope

        # TODO: may need to return dict instead of boolean
        while scope != None:
            if not is_func and symbol in self.symbol_and_table_map[scope].symbols:
                return True
            elif is_func and symbol in self.symbol_and_table_map[scope].functions:
                return True
            scope = self.symbol_and_table_map[scope].parent

        return False


    def make_label(self, func_name):
        prefix = "CS335_GROUP7_"
        self.label_counter = self.label_counter + 1
        return prefix + str(self.label_counter)


    def insert_in_sym_table(self, category, **kwargs):
        '''
        Universal function to insert any symbol into current symbol table
        Returns a string representing the new scope name if a new block is
        about to start; otherwise returns None
        '''
        if category == "symbol":
            self.symbol_and_table_map[self.curr_scope].add_symbol(
                    idName=kwargs[idName],
                    idType=kwargs[idType],
                    isArray=kwargs[isArray],
                    arr_size=kwargs[arr_size]
            )
            return None
        elif category == "function":
            self.symbol_and_table_map[self.curr_scope].add_function(
                    func_name=kwargs[func_name],
                    params=kwargs[param],
                    ret_type=kwargs[ret_type]
            )
            return kwargs[func_name]
        else:
            new_name = self.make_label(kwargs[block_name])
            self.symbol_and_table_map[self.curr_scope].add_block(
                    block_name=new_name
            )
            return new_name



class SymbolTable:
    def __init__(self, scope, parent):
        '''
        Symbol table class for each block in program
        '''
        self.scope = scope
        self.parent = parent
        self.symbols = dict()
        self.functions = dict()
        self.blocks = set()


    def add_symbol(self, idName, idType, isArray=False, arr_size=None):
        if idName in self.symbols.keys():
            raise Exception('Variable %s redeclared, check your program', %(idName))

        # add the ID to symbols dict if not present earlier
        self.symbols[idName] = {
            'type' : idType,
            'isArray' : isArray,
            'arr_size' : arr_size
        }


    def add_function(self, func_name, params=None, ret_type=None):
        if func_name in self.functions.keys():
            raise Exception('Function %s redeclared, check your program', %(func_name))

        self.functions[func_name] = {
            'n_params' : len(params),
            'params' : params,
            'ret_type' : ret_type
        }


    def add_block(self, block_name):
        self.blocks.add(block_name)
