#! /usr/bin/env python
import ply.lex as lex
import sys

class Tokens(object):
    def __init__(self):
        self.reserved = self._get_reserved()
        self.tokens = self._get_tokens()


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
              ##  'implements'      : 'IMPLEMENTS', removed interface
                'import'          : 'IMPORT',
                'instanceof'      : 'INSTANCEOF',
              ##  'interface'       : 'INTERFACE',  removed interface
                'native'          : 'NATIVE',
                'new'             : 'NEW',
                'package'         : 'PACKAGE',
              #  'private'         : 'PRIVATE',  removed Data Hiding
              #  'protected'       : 'PROTECTED',
              #  'public'          : 'PUBLIC',
                'return'          : 'RETURN',
                'static'          : 'STATIC',
                'super'           : 'SUPER',
                'switch'          : 'SWITCH',
                'this'            : 'THIS',
                'throw'           : 'THROW',
                'throws'          : 'THROWS',
                'try'             : 'TRY',
                'while'           : 'WHILE',
                'lambda'          : 'LAMBDA'    #New lambda feature in java
                }
        return keywords


    def _get_operators(self):
        operators = [
                'EQUALS',
                'ASSIGN',
                'GRT',
                'LST',
                'GEQ',
                'LEQ',
                'PLUS',
                'MINUS',
                'MULT',
                'DIVIDE',
                'LOGICAL_AND',
                'LOGICAL_OR',
                'LOGICAL_NOT',
                'NOT_EQUAL',
                'BITWISE_AND',
                'BITWISE_OR',
                'BITWISE_NOT',
                'BITWISE_XOR',
                'MODULO',
                'INCREMENT',
                'DECREMENT',
                'DOT',
                'INSTANCEOF',
                'PLUSEQ',
                'MINUSEQ',
                'MULTEQ',
                'DIVEQ',
                'MODEQ',
                'L_SHIFT',
                'R_SHIFT'
                ]
        return operators


    def _get_separators(self):
        separators = [
                'STMT_TERMINATOR',
                'COMMA',
                'L_PAREN',
                'R_PAREN',
                'BLOCK_OPENER',
                'BLOCK_CLOSER',
                'L_SQBR',
                'R_SQBR'
                ]
        return separators


    def _get_misc_words(self):
        misc = [
                'IDENTIFIER',
                'INT_CONSTANT',
                'FLOAT_CONSTANT',
                'CHAR_CONSTANT',
                'STR_CONSTANT',
                'INLINE_COMMENT',
                'BLOCK_COMMENT',
                'NULL',
                'LAMBDA_TOKEN',
               ]
        return misc


    def _get_reserved(self):
        types = self._get_types()
        keywords = self._get_keywords()
        reserved = dict(list(types.items()) + list(keywords.items()))
        return reserved


    def _get_tokens(self):
        operators = self._get_operators()
        separators = self._get_separators()
        misc = self._get_misc_words()
        reserved = list(self.reserved.values())
        tokens = operators + separators + misc + reserved
        return tokens


def main():
    toks = Tokens()
    tokens = toks._get_tokens()

    ################################ Rules for Tokens #######################################
    # Other Identifiers
    def t_FLOAT_CONSTANT(t):
        r'\d*\.\d+'
        t.value = float(t.value)
        return t

    def t_INT_CONSTANT(t):
        r'\d+'
        t.value = int(t.value)
        return t

    t_STR_CONSTANT = r'\"([^\\\n]|(\\.))*?\"' #[^\\\n]: Matches everything except \ and newline.
                                              #(\\.): Anything with escape char
    t_CHAR_CONSTANT = r"\'([^\\\n]|(\\.))?\'"

    def t_IDENTIFIER(t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = toks.reserved.get(t.value,'IDENTIFIER')
        return t

    t_LAMBDA_TOKEN    = r'\->'

    # Separators
    t_STMT_TERMINATOR = r';'
    t_COMMA           = r','
    t_L_PAREN         = r'\('
    t_R_PAREN         = r'\)'
    t_BLOCK_OPENER    = r'\{'
    t_BLOCK_CLOSER    = r'\}'
    t_L_SQBR          = r'\['
    t_R_SQBR          = r'\]'

    # Operators
    t_EQUALS          = r'=='
    t_ASSIGN          = r'='
    t_GRT             = r'>'
    t_LST             = r'<'
    t_GEQ             = r'>='
    t_LEQ             = r'<='
    t_PLUS            = r'\+'
    t_MINUS           = r'\-'
    t_MULT            = r'\*'
    t_DIVIDE          = r'/'
    t_LOGICAL_AND     = r'&&'
    t_LOGICAL_OR      = r'\|\|'
    t_LOGICAL_NOT     = r'!'
    t_NOT_EQUAL       = r'!='
    t_BITWISE_AND     = r'&'
    t_BITWISE_OR      = r'\|'
    t_BITWISE_NOT     = r'~'
    t_BITWISE_XOR     = r'\^'
    t_MODULO          = r'%'
    t_INCREMENT       = r'\+\+'
    t_DECREMENT       = r'\-\-'
    t_DOT             = r'\.'
    t_INSTANCEOF      = r'instanceof'
    t_PLUSEQ          = r'\+= '
    t_MINUSEQ         = r'-='
    t_MULTEQ          = r'\*='
    t_DIVEQ           = r'/='
    t_MODEQ           = r'%='
    t_L_SHIFT         = r'<<'
    t_R_SHIFT         = r'>>'


    t_ignore = ' \t'

    def t_error(t):
        print("Illegal Character '%s'" % t.value[0])
        t.lexer.skip(1)

    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_INLINE_COMMENT(t):
        r'//.*'
        return t

    def t_BLOCK_COMMENT(t):
        r'/\*(.|\n)*?\*/'
        t.lexer.lineno += t.value.count('\n')
        return t
    #########################################################################################

    code = open(sys.argv[1],"r").read()
    # print(code)
    lexer = lex.lex()
    lexer.input(code)

    tokenDict = dict()
    for token in tokens:
        tokenDict[token] = [0,[]]
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokenDict[tok.type][0] += 1
        if tok.value not in tokenDict[tok.type][1]:
            tokenDict[tok.type][1].append(str(tok.value))

    # print(tokenDict)
    print("Token" + 20 * " " + "Occurences" + 16 * " " + "Lexemes" )
    print("-----------------------------------------------------------------------")
    for key in tokenDict:
        if(tokenDict[key][0]!=0):
            print(key + " " * (25 - len(key)) + str(tokenDict[key][0]) + " " * (26 - len(str(tokenDict[key][0]))) + ",".join(tokenDict[key][1]))
    print(lexer.lineno)


if __name__ == '__main__':
    main()
