#!/usr/bin/env python
import sys
import ply.lex as lex
import ply.yacc as yacc
import lexer

tokens = lexer.tokens

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

def p_Block(p):
    '''
    Block : BLOCK_OPENER BLOCK_CLOSER
    | BLOCK_OPENER BlockStatements BLOCK_CLOSER
    '''

def p_BlockStatements(p):
    '''
    BlockStatements : BlockStatement
    | BlockStatements BlockStatement
    '''

def p_BlockStatement(p):
    '''
    BlockStatement : LocalVariableDeclarationStatement
    | Statement
    '''

def p_LocalVariableDeclarationStatement(p):
    '''
    LocalVariableDeclarationStatement : LocalVariableDeclaration STMT_TERMINATOR
    '''

def p_LocalVariableDeclaration(p):
    '''
    LocalVariableDeclaration : Type VariableDeclarators
    '''

def p_Statement(p):
    '''
    Statement : StatementWithoutTrailingSubstatement
    | LabeledStatement
    | IfThenStatement
    | IfThenElseStatement
    | WhileStatement
    | ForStatement
    '''

def p_StatementNoShortIf(p):
    '''
    StatementNoShortIf : StatementWithoutTrailingSubstatement
    | LabeledStatementNoShortIf
    | IfThenElseStatementNoShortIf
    | WhileStatementNoShortIf
    | ForStatementNoShortIf
    '''

def p_StatementWithoutTrailingSubstatement(p):
    '''
    StatementWithoutTrailingSubstatement : Block
    | EmptyStatement
    | ExpressionStatement
    | SwitchStatement
    | DoStatement
    | BreakStatement
    | ContinueStatement
    | ReturnStatement
    | ThrowStatement
    | TryStatement
    '''
    #Skipped SynchoronizedStatemetn

def p_EmptyStatement(p):
    '''
    EmptyStatement : STMT_TERMINATOR
    '''

def p_LabeledStatement(p):
    '''
    LabeledStatement : Identifier COLON Statement
    '''

def p_LabeledStatementNoShortIf(p):
    '''
    LabeledStatementNoShortIf : Identifier COLON StatementNoShortIf
    '''

def p_ExpressionStatement(p):
    '''
    ExpressionStatement : StatementExpression STMT_TERMINATOR
    '''

def p_StatementExpression(p):
    '''
    StatementExpression : Assignment
    | PreIncrementExpression
    | PreDecrementExpression
    | PostIncrementExpression
    | PostDecrementExpression
    | MethodInvocation
    | ClassInstanceCreationExpression
    '''

def p_IfThenStatement(p):
    '''
    IfThenStatement : IF L_PAREN Expression R_PAREN Statement
    '''

def p_IfThenElseStatement(p):
    '''
    IfThenElseStatement : IF L_PAREN Expression R_PAREN StatementNoShortIf ELSE Statement
    '''

def p_IfThenElseStatementNoShortIf(p):
    '''
    IfThenElseStatementNoShortIf : IF L_PAREN Expression R_PAREN StatementNoShortIf ELSE StatementNoShortIf
    '''

def p_SwitchStatement(p):
    '''
    SwitchStatement : SWITCH L_PAREN Expression R_PAREN SwitchBlock
    '''

def p_SwitchBlock(p):
    '''
    SwitchBlock : BLOCK_OPENER BLOCK_CLOSER
    | BLOCK_OPENER SwitchBlockStatementGroups SwitchLabels BLOCK_CLOSER
    | BLOCK_OPENER SwitchBlockStatementGroups BLOCK_CLOSER
    | BLOCK_OPENER SwitchLabels BLOCK_CLOSER
    '''

def p_SwitchBlockStatementGroups(p):
    '''
    SwitchBlockStatementGroups : SwitchBlockStatementGroup
    | SwitchBlockStatementGroups SwitchBlockStatementGroup
    '''

def p_SwitchBlockStatementGroup(p):
    '''
    SwitchBlockStatementGroup : SwitchLabels BlockStatements
    '''

def p_SwitchLabels(p):
    '''
    SwitchLabels : SwitchLabel
    | SwitchLabels SwitchLabel
    '''

def p_SwitchLabel(p):
    '''
    SwitchLabel : CASE ConstantExpression COLON
    | DEFAULT COLON
    '''

def p_WhileStatement(p):
    '''
    WhileStatement : WHILE L_PAREN Expression R_PAREN Statement
    '''

def p_WhileStatementNoShortIf(p):
    '''
    WhileStatementNoShortIf : WHILE L_PAREN Expression R_PAREN StatementNoShortIf
    '''

def p_DoStatement(p):
    '''
    DoStatement : DO Statement WHILE L_PAREN Expression R_PAREN STMT_TERMINATOR
    '''

def p_ForStatement(p):
    '''
    ForStatement : FOR L_PAREN ForInit STMT_TERMINATOR Expression STMT_TERMINATOR ForUpdate R_PAREN Statement
    | FOR L_PAREN STMT_TERMINATOR Expression STMT_TERMINATOR ForUpdate R_PAREN Statement
    | FOR L_PAREN ForInit STMT_TERMINATOR STMT_TERMINATOR ForUpdate R_PAREN Statement
    | FOR L_PAREN ForInit STMT_TERMINATOR Expression STMT_TERMINATOR R_PAREN Statement
    | FOR L_PAREN ForInit STMT_TERMINATOR STMT_TERMINATOR R_PAREN Statement
    | FOR L_PAREN STMT_TERMINATOR Expression STMT_TERMINATOR R_PAREN Statement
    | FOR L_PAREN STMT_TERMINATOR STMT_TERMINATOR ForUpdate R_PAREN Statement
    | FOR L_PAREN STMT_TERMINATOR STMT_TERMINATOR R_PAREN Statement
    '''

def p_ForStatementNoShortIf(p):
    '''
    ForStatement : FOR L_PAREN ForInit STMT_TERMINATOR Expression STMT_TERMINATOR ForUpdate R_PAREN StatementNoShortIf
    | FOR L_PAREN STMT_TERMINATOR Expression STMT_TERMINATOR ForUpdate R_PAREN StatementNoShortIf
    | FOR L_PAREN ForInit STMT_TERMINATOR STMT_TERMINATOR ForUpdate R_PAREN StatementNoShortIf
    | FOR L_PAREN ForInit STMT_TERMINATOR Expression STMT_TERMINATOR R_PAREN StatementNoShortIf
    | FOR L_PAREN ForInit STMT_TERMINATOR STMT_TERMINATOR R_PAREN StatementNoShortIf
    | FOR L_PAREN STMT_TERMINATOR Expression STMT_TERMINATOR R_PAREN StatementNoShortIf
    | FOR L_PAREN STMT_TERMINATOR STMT_TERMINATOR ForUpdate R_PAREN StatementNoShortIf
    | FOR L_PAREN STMT_TERMINATOR STMT_TERMINATOR R_PAREN StatementNoShortIf
    '''

def p_ForInit(p):
    '''
    ForInit : StatementExpressionList
    | LocalVariableDeclaration
    '''

def p_ForUpdate(p):
    '''
    ForUpdate : StatementExpressionList
    '''

def p_StatementExpressionList(p):
    '''
    StatementExpressionList : StatementExpression
    | StatementExpressionList COMMA StatementExpression
    '''

def p_BreakStatement(p):
    '''
    BreakStatement : BREAK Identifier STMT_TERMINATOR
    | BREAK STMT_TERMINATOR
    '''

def p_ContinueStatement(p):
    '''
    ContinueStatement : CONTINUE Identifier STMT_TERMINATOR
    | CONTINUE STMT_TERMINATOR
    '''

def p_ReturnStatement(p):
    '''
    ReturnStatement : RETURN Expression STMT_TERMINATOR
    | RETURN STMT_TERMINATOR
    '''

def p_ThrowStatement(p):
    '''
    ThrowStatement : THROW Expression STMT_TERMINATOR
    '''

def p_TryStatement(p):
    '''
    TryStatement : TRY Block Catches
    | TRY Block Catches Finally
    | TRY Block Finally
    '''

def p_Catches(p):
    '''
    Catches : CatchClause
    | Catches CatchClause
    '''

def p_CatchClause(p):
    '''
    CatchClause : CATCH L_PAREN FormalParameter R_PAREN Block
    '''

def p_Finally(p):
    '''
    FINALLY Block
    '''

def main():
    parser = yacc.yacc()
    inputfile = open(sys.argv[1],'r').read()
    inputfile += "\n"
    parser.parse(inputfile, debug=0)


if __name__ == "__main__":
    main()
