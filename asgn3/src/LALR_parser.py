#!/usr/bin/env python
import sys
import ply.lex as lex
import ply.yacc as yacc
import lexer

# Section 19.8
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
    | VariableDeclarators COMMA VariableDeclarator
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
    | Identifier L_PAREN FormalParameterList R_PAREN
    '''

def p_FormalParametersList(p):
    '''
    FormalParameterList : FormalParameter
    | FormalParameterList COMMA FormalParameter
    '''

def p_FormalParameter(p):
    '''
    FormalParameter : Type VariableDeclaratorId
    '''

def p_Throws(p):
    '''
    Throws : THROWS ClassTypeList
    '''

def p_ClassTypeList(p):
    '''
    ClassTypeList : ClassType
    | ClassTypeList COMMA ClassType
    '''

def p_MethodBody(p):
    '''
    MethodBody : Block
    | STMT_TERMINATOR
    '''

def p_StaticInitializer(p):
    '''
    StaticInitializer : STATIC Block
    '''

def p_ConstructorDeclaration(p):
    '''
    ConstructorDeclaration : Modifiers ConstructorDeclarator Throws ConstructorBody
    | Modifiers ConstructorDeclarator ConstructorBody
    | ConstructorDeclarator Throws ConstructorBody
    | ConstructorDeclarator ConstructorBody
    '''

def p_ConstructorDeclarator(p):
    '''
    ConstructorDeclarator : SimpleName L_PAREN FormalParameterList R_PAREN
    | SimpleName L_PAREN R_PAREN
    '''

def p_ConstructorBody(p):
    '''
    ConstructorBody : BLOCK_OPENER ExplicitConstructorInvocation BlockStatements BLOCK_CLOSER
    | BLOCK_OPENER ExplicitConstructorInvocation BLOCK_CLOSER
    | BLOCK_OPENER BlockStatements BLOCK_CLOSER
    | BLOCK_OPENER BLOCK_CLOSER
    '''

def p_ExplicitConstructorInvocation(p):
    '''
    ExplicitConstructorInvocation : THIS L_PAREN ArgumentList R_PAREN STMT_TERMINATOR
    | THIS L_PAREN R_PAREN STMT_TERMINATOR
    | SUPER L_PAREN ArgumentList R_PAREN STMT_TERMINATOR
    | SUPER L_PAREN R_PAREN STMT_TERMINATOR
    '''

# Section 19.9 is about Interfaces

# Seection 19.10
def p_ArrayInitializer(p):
    '''
    ArrayInitializer : BLOCK_OPENER VariableInitializers BLOCK_CLOSER
    | BLOCK_OPENER BLOCK_CLOSER
    '''

def p_VariableInitializers(p):
    '''
    VariableInitializers : VariableInitializer
    | VariableInitializers COMMA VariableInitializer
    '''


def main():
    parser = yacc.yacc()
    inputfile = open(sys.argv[1],'r').read()
    inputfile += "\n"
    parser.parse(inputfile, debug=0)


if __name__ == "__main__":
    main()
