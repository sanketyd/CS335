#! /usr/bin/env python
import ply.lex as lex

class Lexer(object):
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
                'INT'             : 'int',
                'LONG'            : 'long',
                'FLOAT'           : 'float',
                'DOUBLE'          : 'double',
                'CHAR'            : 'char',
                'VOID'            : 'void',
                'BOOLEAN'         : 'boolean',
                'SHORT'           : 'short'
                }
        self.num_types = len(types)
        return types


    def _get_keywords(self):
        keywords = {
                'ABSTRACT'        : 'abstract',
                'ASSERT'          : 'assert',
                'BREAK'           : 'break',
                'BYTE'            : 'byte',
                'CASE'            : 'case',
                'CATCH'           : 'catch',
                'CLASS'           : 'class',
                'CONST'           : 'const',
                'CONTINUE'        : 'continue',
                'DEFAULT'         : 'default',
                'DO'              : 'do',
                'ELSE'            : 'else',
                'EXTENDS'         : 'extends',
                'FINAL'           : 'final',
                'FINALLY'         : 'finally',
                'FOR'             : 'for',
                'IF'              : 'if',
                'IMPLEMENTS'      : 'implements',
                'IMPORT'          : 'import',
                'INSTANCEOF'      : 'instanceof',
                'INTERFACE'       : 'interface',
                'NATIVE'          : 'native',
                'NEW'             : 'new',
                'PACKAGE'         : 'package',
                'PRIVATE'         : 'private',
                'PROTECTED'       : 'protected',
                'PUBLIC'          : 'public',
                'RETURN'          : 'return',
                'STATIC'          : 'static',
                'SUPER'           : 'super',
                'SWITCH'          : 'switch',
                'THIS'            : 'this',
                'THROW'           : 'throw',
                'THROWS'          : 'throws',
                'TRY'             : 'try',
                'WHILE'           : 'while'
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
        tokens = list(types.keys()) + list(operators.keys()) + \
                list(separators.keys()) + list(keywords.keys()) + \
                misc
        return tokens


lexer = Lexer()
