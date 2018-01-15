#! /usr/bin/python

import ply.lex as lex

# List of token names used:
misc = [
        'IDENTIFIER',
        'INT_CONSTANT',
        'FLOAT_CONSTANT',
        'CHAR_CONSTANT',
        'STR_CONSTANT',
        'COMMENT',
        'NULL'
       ]

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
        'SYNCHRONIZED'    : 'synchronized',
        'SWITCH'          : 'switch',
        'THIS'            : 'this',
        'THROW'           : 'throw',
        'THROWS'          : 'throws',
        'TRANSIENT'       : 'transient',
        'TRY'             : 'try',
        'VOLATILE'        : 'volatile',
        'WHILE'           : 'while'
        }

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

tokens = misc + list(types.keys()) + list(separators.keys()) + list(keywords.keys()) + list(operators.keys())
