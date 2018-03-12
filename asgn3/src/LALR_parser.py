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

def p_Primary(p):
    '''
    Primary : PrimaryNoNewArray
    | ArrayCreationExpression
    '''

def p_PrimaryNoNewArray(p):
    '''
    PrimaryNoNewArray : Literal
    | THIS
    | L_PAREN Expression R_PAREN
    | ClassInstanceCreationExpression
    | FieldAccess
    | MethodInvocation
    | ArrayAccess
    '''

def p_ClassInstanceCreationExpression(p):
    '''
    ClassInstanceCreationExpression : NEW ClassType L_PAREN R_PAREN
    | NEW ClassType L_PAREN ArgumentList R_PAREN
    '''

def p_ArgumentList(p):
    '''
    ArgumentList : Expression
    | ArgumentList COMMA Expression
    '''

def p_ArrayCreationExpression(p):
    '''
    ArrayCreationExpression : NEW PrimitiveType DimExprs Dims
    | NEW PrimitiveType DimExprs
    | new ClassOrInterfaceType DimExprs Dims
    | new ClassOrInterfaceType DimExprs
    '''

def p_DimExprs(p):
    '''
    DimExprs : DimExpr
    | DimExprs DimExpr
    '''

def p_DimExpr(p):
    '''
    DimExpr : L_SQBR Expression R_SQBR
    '''

def p_Dims(p):
    '''
    Dims : L_SQBR R_SQBR
    | Dims L_SQBR R_SQBR
    '''

def p_FieldAccess(p):
    '''
    FieldAccess : Primary DOT Identifier
    | SUPER DOT Identifier
    '''

def p_MethodInvocation(p):
    '''
    MethodInvocation : Name L_PAREN ArgumentList R_PAREN
    | Name L_PAREN R_PAREN
    | Primary DOT Identifier L_PAREN ArgumentList R_PAREN
    | Primary DOT Identifier L_PAREN R_PAREN
    | SUPER DOT Identifier L_PAREN ArgumentList R_PAREN
    | SUPER DOT Identifier L_PAREN R_PAREN
    '''

def p_ArrayAccess(p):
    '''
    ArrayAccess : Name L_SQBR Expression R_SQBR
    | PrimaryNoNewArray L_SQBR Expression R_SQBR
    '''

def p_PostfixExpression(p):
    '''
    PostfixExpression : Primary
    | Name
    | PostIncrementExpression
    | PostDecrementExpression
    '''

def p_PostIncrementExpression(p):
    '''
    PostIncrementExpression : PostfixExpression INCREMENT
    '''

def p_PostDecrementExpression(p):
    '''
    PostDecrementExpression : PostfixExpression DECREMENT
    '''

def p_UnaryExpression(p):
    '''
    UnaryExpression : PreIncrementExpression
    | PreIncrementExpression
    | PLUS UnaryExpression
    | MINUS UnaryExpression
    | UnaryExpressionNotPlusMinus
    '''

def p_PreIncrementExpression(p):
    '''
    PreIncrementExpression : INCREMENT UnaryExpression
    '''

def p_PreDecrementExpression(p):
    '''
    PreDecrementExpression : DECREMENT UnaryExpression
    '''

def p_UnaryExpressionNotPlusMinus(p):
    '''
    UnaryExpressionNotPlusMinus : PostfixExpression
    | BITWISE_NOT UnaryExpression
    | NOT UnaryExpression
    | CastExpression
    '''

def p_CastExpression(p):
    '''
    CastExpression : L_PAREN PrimitiveType Dims R_PAREN UnaryExpression
    | L_PAREN PrimitiveType R_PAREN UnaryExpression
    | L_PAREN Expression R_PAREN UnaryExpressionNotPlusMinus
    | L_PAREN Name Dims R_PAREN UnaryExpressionNotPlusMinus
    '''

def p_MultiplicativeExpression(p):
    '''
    MultiplicativeExpression : UnaryExpression
    | MultiplicativeExpression MULT UnaryExpression
    | MultiplicativeExpression DIVIDE UnaryExpression
    | MultiplicativeExpression MODULO UnaryExpression
    '''

def p_AdditiveExpression(p):
    '''
    AdditiveExpression : MultiplicativeExpression
    | AdditiveExpression PLUS MultiplicativeExpression
    | AdditiveExpression MINUS MultiplicativeExpression
    '''

def p_ShiftExpression(p):
    '''
    ShiftExpression : AdditiveExpression
    | ShiftExpression L_SHIFT AdditiveExpression
    | ShiftExpression R_SHIFT AdditiveExpression
    '''
    #Ek chod diya >>> wala

def p_RelationalExpression(p):
    '''
    RelationalExpression : ShiftExpression
    | RelationalExpression LST ShiftExpression
    | RelationalExpression GRT ShiftExpression
    | RelationalExpression LEQ ShiftExpression
    | RelationalExpression GEQ ShiftExpression
    | RelationalExpression INSTANCEOF ReferenceType
    '''

def p_EqualityExpression(p):
    '''
    EqualityExpression : RelationalExpression
    | EqualityExpression EQUALS RelationalExpression
    | EqualityExpression NOT_EQUAL RelationalExpression
    '''

def p_AndExpression(p):
    '''
    AndExpression : EqualityExpression
    AndExpression BITWISE_AND EqualityExpression
    '''

def p_ExclusiveOrExpression(p):
    '''
    ExclusiveOrExpression : AndExpression
    | ExclusiveOrExpression BITWISE_XOR AndExpression
    '''

def p_InclusiveOrExpression(p):
    '''
    InclusiveOrExpression : ExclusiveOrExpression
    | InclusiveOrExpression BITWISE_OR ExclusiveOrExpression
    '''

def p_ConditionalAndExpression(p):
    '''
    ConditionalAndExpression : InclusiveOrExpression
    | ConditionalAndExpression LOGICAL_AND InclusiveOrExpression
    '''

def p_ConditionalOrExpression(p):
    '''
    ConditionalOrExpression : ConditionalAndExpression
    | ConditionalOrExpression BITWISE_OR ConditionalAndExpression
    '''

def p_ConditionalExpression(p):
    '''
    ConditionalExpression : ConditionalOrExpression
    ConditionalOrExpression QUESTION Expression COLON ConditionalExpression
    '''

def p_AssignmentExpression(p):
    '''
    AssignmentExpression : ConditionalExpression
    | Assignment
    '''

def p_Assignment(p):
    '''
    Assignment : LeftHandSide AssignmentOperator AssignmentExpression
    '''

def p_LeftHandSide(p):
    '''
    LeftHandSide : Name
    | FieldAccess
    | ArrayAccess
    '''

def p_AssignmentOperator(p):
    '''
    AssignmentOperator : ASSIGN
    | MULTEQ
    | DIVEQ
    | MODEQ
    | PLUSEQ
    | MINUSEQ
    | LSHIFTEQ
    | RSHIFTEQ
    '''
    #To check if I missed something

def p_Expression(p):
    '''
    Expression : AssignmentExpression
    '''

def p_ConstantExpression(p):
    '''
    ConstantExpression : Expression
    '''

def main():
    parser = yacc.yacc()
    inputfile = open(sys.argv[1],'r').read()
    inputfile += "\n"
    parser.parse(inputfile, debug=0)


if __name__ == "__main__":
    main()
