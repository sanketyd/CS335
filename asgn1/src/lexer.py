#! /usr/bin/env python
import ply.lex as lex
import sys

class Tokens(object):
    def __init__(self):
        self.num_types = 0
        self.num_keywords = 0
        self.num_operators = 0
        self.num_separators = 0
        self.num_misc = 0
        self.tokens = self._get_tokens()
        self.total_reserved_words = self._get_total_reserved_words()


    def _get_total_reserved_words(self):
        return self.num_types + self.num_keywords + self.num_operators + \
                self.num_separators + self.num_misc


    def _get_types(self):
        types = {
                'int'             : 'INT',
                'long'            : 'LONG',
                'float'           : 'FLOAT',
                'double'          : 'DOUBLE',
                'char'            : 'CHAR',
                'void'            : 'VOID',
                'boolean'         : 'BOOLEAN',
                'short'           : 'SHORT'
                }
        self.num_types = len(types)
        return types


    def _get_keywords(self):
        keywords = {
                'abstract'        : 'ABSTRACT',
                'assert'          : 'ASSERT',
                'break'           : 'BREAK',
                'byte'            : 'BYTE',
                'case'            : 'CASE',
                'catch'           : 'CATCH',
                'class'           : 'CLASS',
                'const'           : 'CONST',
                'continue'        : 'CONTINUE',
                'default'         : 'DEFAULT',
                'do'              : 'DO',
                'else'            : 'ELSE',
                'extends'         : 'EXTENDS',
                'final'           : 'FINAL',
                'finally'         : 'FINALLY',
                'for'             : 'FOR',
                'if'              : 'IF',
                'implements'      : 'IMPLEMENTS',
                'import'          : 'IMPORT',
                'instanceof'      : 'INSTANCEOF',
                'interface'       : 'INTERFACE',
                'native'          : 'NATIVE',
                'new'             : 'NEW',
                'package'         : 'PACKAGE',
                'private'         : 'PRIVATE',
                'protected'       : 'PROTECTED',
                'public'          : 'PUBLIC',
                'return'          : 'RETURN',
                'static'          : 'STATIC',
                'super'           : 'SUPER',
                'switch'          : 'SWITCH',
                'this'            : 'THIS',
                'throw'           : 'THROW',
                'throws'          : 'THROWS',
                'try'             : 'TRY',
                'while'           : 'WHILE'
                }
        self.num_keywords = len(keywords)
        return keywords


    def _get_operators(self):
        operators = {
                'EQUALS'          : '==',
                'ASSIGN'          : '=',
                'GRT'             : '>',
                'LST'             : '<',
                'GEQ'             : '>=',
                'LEQ'             : '<=',
                'PLUS'            : '+',
                'MINUS'           : '-',
                'MULT'            : '*',
                'DIVIDE'          : '/',
                'LOGICAL_AND'     : '&&',
                'LOGICAL_OR'      : '||',
                'LOGICAL_NOT'     : '!',
                'NOT_EQUAL'       : '!=',
                'BITWISE_AND'     : '&',
                'BITWISE_OR'      : '|',
                'BITWISE_NOT'     : '~',
                'BITWISE_XOR'     : '^',
                'MODULO'          : '%',
                'INCREMENT'       : '++',
                'DECREMENT'       : '--'
                }
        self.num_operators = len(operators)
        return operators


    def _get_separators(self):
        separators = {
                'STMT_TERMINATOR' : ';',
                'COMMA'           : ',',
                'DOT'             : '.',
                'L_PAREN'         : '(',
                'R_PAREN'         : ')',
                'BLOCK_OPENER'    : '{',
                'BLOCK_CLOSER'    : '}',
                'L_SQBR'          : '[',
                'R_SQBR'          : ']'
                }
        self.num_separators = len(separators)
        return separators


    def _get_misc_words(self):
        misc = [
                'IDENTIFIER',
                'INT_CONSTANT',
                'FLOAT_CONSTANT',
                'CHAR_CONSTANT',
                'STR_CONSTANT',
                'COMMENT',
                'NULL'
               ]
        self.num_misc = len(misc)
        return misc


    def _get_tokens(self):
        types = self._get_types()
        operators = self._get_operators()
        separators = self._get_separators()
        keywords = self._get_keywords()
        misc = self._get_misc_words()
        tokens = list(types.values()) + list(operators.keys()) + \
                list(separators.keys()) + list(keywords.values()) + \
                misc
        return tokens

def main():
    toks = Tokens()
    tokens = toks._get_tokens()
################################ Rules for Tokens #######################################

    t_BLOCK_OPENER = r'\{'
    t_BLOCK_CLOSER = r'\}'

    def t_INT_CONSTANT(t):
        r'\d+'
        t.value = int(t.value)
        return t

    t_STR_CONSTANT = r'\".*?\"'
    t_CHAR_CONSTANT = r'\".?\"'

    def t_IDENTIFIER(t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = toks._get_keywords().get(t.value,'IDENTIFIER')
        if t.type == 'IDENTIFIER':
            t.type = toks._get_types().get(t.value,'IDENTIFIER')
        return t

    def t_error(t):
        print("Illegal Character '%s'" % t.value[0])
        t.lexer.skip(1)

    t_ignore = ' \t'

    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)

#########################################################################################

    code = open(sys.argv[1],"r").read()

    lexer = lex.lex()

    lexer.input(code)

    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)

    print(lexer.lineno)

if __name__ == '__main__':
    main()
