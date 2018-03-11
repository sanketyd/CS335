#!/usr/bin/env python
import sys
import ply.lex as lex
import ply.yacc as yacc
import lexer

def p_ClassDeclaration(p):
    '''
    ClassDeclaration : Modifiers CLASS Identifier Super ClassBody
    | Modifiers CLASS Identifier ClassBody
    | CLASS Identifier Super ClassBody
    '''

def p_Super(p):
    '''
    Super : EXTENDS ClassType
    '''

def p_ClassBody(p):
    '''
    ClassBody : BLOCK_OPENER BLOCK_CLOSER
    | BLOCK_OPENER ClassBodyDeclarations BLOCK_CLOSER
    '''

def p_ClassBodyDeclarations(p):
    '''
    ClassBodyDeclarations : ClassBodyDeclaration
    | ClassBodyDeclarations ClassBodyDeclaration
    '''

def p_ClassBodyDeclaration(p):
    '''
    ClassBodyDeclaration : ClassMemberDeclaration
    | ConstructorDeclaration
    | StaticInitializer
    '''

def p_ClassMemberDeclaration(p):
    '''
    ClassMemberDeclaration : FieldDeclaration
    | MethodDeclaration
    '''

def p_FieldDeclaration(p):
    '''
    FieldDeclaration : Modifiers Type VariableDeclarators STMT_TERMINATOR
    | Type VariableDeclarators STMT_TERMINATOR
    '''

def p_VariableDeclarators(p):
    '''
    VariableDeclarators : VariableDeclarator
    | VariableDeclarators VariableDeclarator
    '''

def p_VariableDeclarator(p):
    '''
    VariableDeclarator : VariableDeclaratorId
    | VariableDeclaratorId ASSIGN VariableInitializer
    '''

def p_VariableDeclaratorId(p):
    '''
    VariableDeclaratorId : Identifier
    | VariableDeclaratorId L_SQBR R_SQBR
    '''

def p_VariableInitializer(p):
    '''
    VariableInitializer : Expression
    | ArrayInitializer
    '''

def p_MethodDeclaration(p):
    '''
    MethodDeclaration : MethodHeader MethodBody
    '''

def p_MethodHeader(p):
    '''
    MethodHeader : Modifier Type MethodDeclarator Throws
    | Modifier Type MethodDeclarator
    | Type MethodDeclarator Throws
    | Type MethodDeclarator
    | Modifier VOID MethodDeclarator Throws
    | Modifier VOID MethodDeclarator
    | VOID MethodDeclarator Throws
    | VOID MethodDeclarator
    '''

def p_MethodDeclarator(p):
    '''
    MethodDeclarator : Identifier L_PAREN R_PAREN
    | Identifier L_PAREN FormalParametersList R_PAREN
    '''



def main():
    parser = yacc.yacc()
    inputfile = open(sys.argv[1],'r').read()
    inputfile += "\n"
    parser.parse(inputfile, debug=0)


if __name__ == "__main__":
    main()
