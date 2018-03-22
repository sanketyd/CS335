#!/usr/bin/env python
import sys
import ply.lex as lex
import ply.yacc as yacc
import lexer


rules_store = []
# Section 19.2

def p_Goal(p):
    '''Goal : CompilationUnit'''
    rules_store.append(p.slice)

# Section 19.3

def p_Literal(p):
    ''' Literal : INT_CONSTANT
    | FLOAT_CONSTANT
    | CHAR_CONSTANT
    | STR_CONSTANT
    | NULL
    '''
    rules_store.append(p.slice)
    # TODO: bool constant


# Section 19.4

def p_Type(p):
    ''' Type : PrimitiveType
    | ReferenceType
    '''
    rules_store.append(p.slice)

def p_PrimitiveType(p):
    ''' PrimitiveType : NumericType
    | BOOLEAN
    '''
    rules_store.append(p.slice)

def p_NumericType(p):
    ''' NumericType : IntegralType
    | FloatingPointType
    '''
    rules_store.append(p.slice)

def p_IntegralType(p):
    ''' IntegralType : BYTE
    | SHORT
    | INT
    | LONG
    | CHAR
    '''
    rules_store.append(p.slice)

def p_FloatingPointType(p):
    ''' FloatingPointType : FLOAT
    | DOUBLE
    '''
    rules_store.append(p.slice)

def p_ReferenceType(p):
    ''' ReferenceType : ArrayType
    | ClassType
    '''
    rules_store.append(p.slice)

def p_ClassType(p):
    '''
    ClassType : Name
    '''
    rules_store.append(p.slice)

def p_ArrayType(p):
    ''' ArrayType : PrimitiveType L_SQBR R_SQBR
    | Name L_SQBR R_SQBR
    | ArrayType L_SQBR R_SQBR
    '''
    rules_store.append(p.slice)

# Section 19.5

def p_Name(p):
    ''' Name : SimpleName
    | QualifiedName'''
    rules_store.append(p.slice)

def p_SimpleName(p):
    ''' SimpleName : IDENTIFIER'''
    rules_store.append(p.slice)

def p_QualifiedName(p):
    ''' QualifiedName : Name DOT IDENTIFIER'''
    rules_store.append(p.slice)



# Section 19.6

def p_CompilationUnit(p):
    '''
    CompilationUnit : PackageDeclaration ImportDeclarations TypeDeclarations
    | PackageDeclaration ImportDeclarations
    | PackageDeclaration TypeDeclarations
    | ImportDeclarations TypeDeclarations
    | PackageDeclaration
    | ImportDeclarations
    | TypeDeclarations
    |
    '''
    rules_store.append(p.slice)

def p_ImportDeclarations(p):
    '''
    ImportDeclarations : ImportDeclaration
    | ImportDeclarations ImportDeclaration
    '''
    rules_store.append(p.slice)

def p_TypeDeclarations(p):
    '''
    TypeDeclarations : TypeDeclaration
    | TypeDeclarations TypeDeclaration
    '''
    rules_store.append(p.slice)

def p_PackageDeclaration(p):
    '''
    PackageDeclaration : PACKAGE Name STMT_TERMINATOR
    '''
    rules_store.append(p.slice)

def p_ImportDeclaration(p):
    '''
    ImportDeclaration : SingleTypeImportDeclaration
    | TypeImportOnDemandDeclaration
    '''
    rules_store.append(p.slice)

def p_SingleTypeImportDeclaration(p):
    '''
    SingleTypeImportDeclaration : IMPORT Name STMT_TERMINATOR
    '''
    rules_store.append(p.slice)

def p_TypeImportOnDemandDeclaration(p):
    '''
    TypeImportOnDemandDeclaration : IMPORT Name DOT MULT STMT_TERMINATOR
    '''
    rules_store.append(p.slice)

def p_TypeDeclaration(p):
    '''
    TypeDeclaration : ClassDeclaration
    | STMT_TERMINATOR
    '''
    rules_store.append(p.slice)

def p_Modifiers(p):
    '''
    Modifiers : Modifier
    | Modifiers Modifier
    '''
    rules_store.append(p.slice)

def p_Modifier(p):
    '''
    Modifier : STATIC
    | FINAL
    '''
    rules_store.append(p.slice)
# Section 19.8

def p_ClassDeclaration(p):
    '''
    ClassDeclaration : Modifiers CLASS IDENTIFIER Super ClassBody
    | Modifiers CLASS IDENTIFIER ClassBody
    | CLASS IDENTIFIER Super ClassBody
    | CLASS IDENTIFIER ClassBody
    '''
    rules_store.append(p.slice)

def p_Super(p):
    '''
    Super : EXTENDS ClassType
    '''
    rules_store.append(p.slice)

def p_ClassBody(p):
    '''
    ClassBody : BLOCK_OPENER BLOCK_CLOSER
    | BLOCK_OPENER ClassBodyDeclarations BLOCK_CLOSER
    '''
    rules_store.append(p.slice)

def p_ClassBodyDeclarations(p):
    '''
    ClassBodyDeclarations : ClassBodyDeclaration
    | ClassBodyDeclarations ClassBodyDeclaration
    '''
    rules_store.append(p.slice)

def p_ClassBodyDeclaration(p):
    '''
    ClassBodyDeclaration : ClassMemberDeclaration
    | ConstructorDeclaration
    | StaticInitializer
    '''
    rules_store.append(p.slice)

def p_ClassMemberDeclaration(p):
    '''
    ClassMemberDeclaration : FieldDeclaration
    | MethodDeclaration
    '''
    rules_store.append(p.slice)

def p_FieldDeclaration(p):
    '''
    FieldDeclaration : Modifiers Type VariableDeclarators STMT_TERMINATOR
    | Type VariableDeclarators STMT_TERMINATOR
    '''
    rules_store.append(p.slice)

def p_VariableDeclarators(p):
    '''
    VariableDeclarators : VariableDeclarator
    | VariableDeclarators COMMA VariableDeclarator
    '''
    rules_store.append(p.slice)

def p_VariableDeclarator(p):
    '''
    VariableDeclarator : VariableDeclaratorId
    | VariableDeclaratorId ASSIGN VariableInitializer
    '''
    rules_store.append(p.slice)

def p_VariableDeclaratorId(p):
    '''
    VariableDeclaratorId : IDENTIFIER
    | VariableDeclaratorId L_SQBR R_SQBR
    '''
    rules_store.append(p.slice)

def p_VariableInitializer(p):
    '''
    VariableInitializer : Expression
    | ArrayInitializer
    '''
    rules_store.append(p.slice)

def p_MethodDeclaration(p):
    '''
    MethodDeclaration : MethodHeader MethodBody
    '''
    rules_store.append(p.slice)

def p_MethodHeader(p):
    '''
    MethodHeader : Modifiers Type MethodDeclarator Throws
    | Modifiers Type MethodDeclarator
    | Type MethodDeclarator Throws
    | Type MethodDeclarator
    | Modifiers VOID MethodDeclarator Throws
    | Modifiers VOID MethodDeclarator
    | VOID MethodDeclarator Throws
    | VOID MethodDeclarator
    '''
    rules_store.append(p.slice)

def p_MethodDeclarator(p):
    '''
    MethodDeclarator : IDENTIFIER L_PAREN R_PAREN
    | IDENTIFIER L_PAREN FormalParameterList R_PAREN
    '''
    rules_store.append(p.slice)

def p_FormalParametersList(p):
    '''
    FormalParameterList : FormalParameter
    | FormalParameterList COMMA FormalParameter
    '''
    rules_store.append(p.slice)

def p_FormalParameter(p):
    '''
    FormalParameter : Type VariableDeclaratorId
    '''
    rules_store.append(p.slice)

def p_Throws(p):
    '''
    Throws : THROWS ClassTypeList
    '''
    rules_store.append(p.slice)

def p_ClassTypeList(p):
    '''
    ClassTypeList : ClassType
    | ClassTypeList COMMA ClassType
    '''
    rules_store.append(p.slice)

def p_MethodBody(p):
    '''
    MethodBody : Block
    | STMT_TERMINATOR
    '''
    rules_store.append(p.slice)

def p_StaticInitializer(p):
    '''
    StaticInitializer : STATIC Block
    '''
    rules_store.append(p.slice)

def p_ConstructorDeclaration(p):
    '''
    ConstructorDeclaration : Modifiers ConstructorDeclarator Throws ConstructorBody
    | Modifiers ConstructorDeclarator ConstructorBody
    | ConstructorDeclarator Throws ConstructorBody
    | ConstructorDeclarator ConstructorBody
    '''
    rules_store.append(p.slice)

def p_ConstructorDeclarator(p):
    '''
    ConstructorDeclarator : SimpleName L_PAREN FormalParameterList R_PAREN
    | SimpleName L_PAREN R_PAREN
    '''
    rules_store.append(p.slice)

def p_ConstructorBody(p):
    '''
    ConstructorBody : BLOCK_OPENER ExplicitConstructorInvocation BlockStatements BLOCK_CLOSER
    | BLOCK_OPENER ExplicitConstructorInvocation BLOCK_CLOSER
    | BLOCK_OPENER BlockStatements BLOCK_CLOSER
    | BLOCK_OPENER BLOCK_CLOSER
    '''
    rules_store.append(p.slice)

def p_ExplicitConstructorInvocation(p):
    '''
    ExplicitConstructorInvocation : THIS L_PAREN ArgumentList R_PAREN STMT_TERMINATOR
    | THIS L_PAREN R_PAREN STMT_TERMINATOR
    | SUPER L_PAREN ArgumentList R_PAREN STMT_TERMINATOR
    | SUPER L_PAREN R_PAREN STMT_TERMINATOR
    '''
    rules_store.append(p.slice)

# Section 19.9 is about Interfaces

# Section 19.10
def p_ArrayInitializer(p):
    '''
    ArrayInitializer : BLOCK_OPENER VariableInitializers BLOCK_CLOSER
    | BLOCK_OPENER BLOCK_CLOSER
    '''
    rules_store.append(p.slice)

def p_VariableInitializers(p):
    '''
    VariableInitializers : VariableInitializer
    | VariableInitializers COMMA VariableInitializer
    '''
    rules_store.append(p.slice)

# Section 19.11
def p_Block(p):
    '''
    Block : BLOCK_OPENER BLOCK_CLOSER
    | BLOCK_OPENER BlockStatements BLOCK_CLOSER
    '''
    rules_store.append(p.slice)

def p_BlockStatements(p):
    '''
    BlockStatements : BlockStatement
    | BlockStatements BlockStatement
    '''
    rules_store.append(p.slice)

def p_BlockStatement(p):
    '''
    BlockStatement : LocalVariableDeclarationStatement
    | Statement
    '''
    rules_store.append(p.slice)

def p_LocalVariableDeclarationStatement(p):
    '''
    LocalVariableDeclarationStatement : LocalVariableDeclaration STMT_TERMINATOR
    '''
    rules_store.append(p.slice)

def p_LocalVariableDeclaration(p):
    '''
    LocalVariableDeclaration : Type VariableDeclarators
    '''
    rules_store.append(p.slice)

def p_Statement(p):
    '''
    Statement : StatementWithoutTrailingSubstatement
    | LabeledStatement
    | IfThenStatement
    | IfThenElseStatement
    | WhileStatement
    | ForStatement
    '''
    rules_store.append(p.slice)

def p_StatementNoShortIf(p):
    '''
    StatementNoShortIf : StatementWithoutTrailingSubstatement
    | LabeledStatementNoShortIf
    | IfThenElseStatementNoShortIf
    | WhileStatementNoShortIf
    | ForStatementNoShortIf
    '''
    rules_store.append(p.slice)

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
    rules_store.append(p.slice)

def p_EmptyStatement(p):
    '''
    EmptyStatement : STMT_TERMINATOR
    '''
    rules_store.append(p.slice)

def p_LabeledStatement(p):
    '''
    LabeledStatement : IDENTIFIER COLON Statement
    '''
    rules_store.append(p.slice)

def p_LabeledStatementNoShortIf(p):
    '''
    LabeledStatementNoShortIf : IDENTIFIER COLON StatementNoShortIf
    '''
    rules_store.append(p.slice)

def p_ExpressionStatement(p):
    '''
    ExpressionStatement : StatementExpression STMT_TERMINATOR
    '''
    rules_store.append(p.slice)

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
    rules_store.append(p.slice)

def p_IfThenStatement(p):
    '''
    IfThenStatement : IF L_PAREN Expression R_PAREN Statement
    '''
    rules_store.append(p.slice)

def p_IfThenElseStatement(p):
    '''
    IfThenElseStatement : IF L_PAREN Expression R_PAREN StatementNoShortIf ELSE Statement
    '''
    rules_store.append(p.slice)

def p_IfThenElseStatementNoShortIf(p):
    '''
    IfThenElseStatementNoShortIf : IF L_PAREN Expression R_PAREN StatementNoShortIf ELSE StatementNoShortIf
    '''
    rules_store.append(p.slice)

def p_SwitchStatement(p):
    '''
    SwitchStatement : SWITCH L_PAREN Expression R_PAREN SwitchBlock
    '''
    rules_store.append(p.slice)

def p_SwitchBlock(p):
    '''
    SwitchBlock : BLOCK_OPENER BLOCK_CLOSER
    | BLOCK_OPENER SwitchBlockStatementGroups SwitchLabels BLOCK_CLOSER
    | BLOCK_OPENER SwitchBlockStatementGroups BLOCK_CLOSER
    | BLOCK_OPENER SwitchLabels BLOCK_CLOSER
    '''
    rules_store.append(p.slice)

def p_SwitchBlockStatementGroups(p):
    '''
    SwitchBlockStatementGroups : SwitchBlockStatementGroup
    | SwitchBlockStatementGroups SwitchBlockStatementGroup
    '''
    rules_store.append(p.slice)

def p_SwitchBlockStatementGroup(p):
    '''
    SwitchBlockStatementGroup : SwitchLabels BlockStatements
    '''
    rules_store.append(p.slice)

def p_SwitchLabels(p):
    '''
    SwitchLabels : SwitchLabel
    | SwitchLabels SwitchLabel
    '''
    rules_store.append(p.slice)

def p_SwitchLabel(p):
    '''
    SwitchLabel : CASE ConstantExpression COLON
    | DEFAULT COLON
    '''
    rules_store.append(p.slice)

def p_WhileStatement(p):
    '''
    WhileStatement : WHILE L_PAREN Expression R_PAREN Statement
    '''
    rules_store.append(p.slice)

def p_WhileStatementNoShortIf(p):
    '''
    WhileStatementNoShortIf : WHILE L_PAREN Expression R_PAREN StatementNoShortIf
    '''
    rules_store.append(p.slice)

def p_DoStatement(p):
    '''
    DoStatement : DO Statement WHILE L_PAREN Expression R_PAREN STMT_TERMINATOR
    '''
    rules_store.append(p.slice)

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
    rules_store.append(p.slice)

def p_ForStatementNoShortIf(p):
    '''
    ForStatementNoShortIf : FOR L_PAREN ForInit STMT_TERMINATOR Expression STMT_TERMINATOR ForUpdate R_PAREN StatementNoShortIf
    | FOR L_PAREN STMT_TERMINATOR Expression STMT_TERMINATOR ForUpdate R_PAREN StatementNoShortIf
    | FOR L_PAREN ForInit STMT_TERMINATOR STMT_TERMINATOR ForUpdate R_PAREN StatementNoShortIf
    | FOR L_PAREN ForInit STMT_TERMINATOR Expression STMT_TERMINATOR R_PAREN StatementNoShortIf
    | FOR L_PAREN ForInit STMT_TERMINATOR STMT_TERMINATOR R_PAREN StatementNoShortIf
    | FOR L_PAREN STMT_TERMINATOR Expression STMT_TERMINATOR R_PAREN StatementNoShortIf
    | FOR L_PAREN STMT_TERMINATOR STMT_TERMINATOR ForUpdate R_PAREN StatementNoShortIf
    | FOR L_PAREN STMT_TERMINATOR STMT_TERMINATOR R_PAREN StatementNoShortIf
    '''
    rules_store.append(p.slice)

def p_ForInit(p):
    '''
    ForInit : StatementExpressionList
    | LocalVariableDeclaration
    '''
    rules_store.append(p.slice)

def p_ForUpdate(p):
    '''
    ForUpdate : StatementExpressionList
    '''
    rules_store.append(p.slice)

def p_StatementExpressionList(p):
    '''
    StatementExpressionList : StatementExpression
    | StatementExpressionList COMMA StatementExpression
    '''
    rules_store.append(p.slice)

def p_BreakStatement(p):
    '''
    BreakStatement : BREAK IDENTIFIER STMT_TERMINATOR
    | BREAK STMT_TERMINATOR
    '''
    rules_store.append(p.slice)

def p_ContinueStatement(p):
    '''
    ContinueStatement : CONTINUE IDENTIFIER STMT_TERMINATOR
    | CONTINUE STMT_TERMINATOR
    '''
    rules_store.append(p.slice)

def p_ReturnStatement(p):
    '''
    ReturnStatement : RETURN Expression STMT_TERMINATOR
    | RETURN STMT_TERMINATOR
    '''
    rules_store.append(p.slice)

def p_ThrowStatement(p):
    '''
    ThrowStatement : THROW Expression STMT_TERMINATOR
    '''
    rules_store.append(p.slice)

def p_TryStatement(p):
    '''
    TryStatement : TRY Block Catches
    | TRY Block Catches Finally
    | TRY Block Finally
    '''
    rules_store.append(p.slice)

def p_Catches(p):
    '''
    Catches : CatchClause
    | Catches CatchClause
    '''
    rules_store.append(p.slice)

def p_CatchClause(p):
    '''
    CatchClause : CATCH L_PAREN FormalParameter R_PAREN Block
    '''
    rules_store.append(p.slice)

def p_Finally(p):
    '''
    Finally : FINALLY Block
    '''
    rules_store.append(p.slice)


# Section 19.12

def p_Primary(p):
    '''
    Primary : PrimaryNoNewArray
    | ArrayCreationExpression
    '''
    rules_store.append(p.slice)

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
    rules_store.append(p.slice)

def p_ClassInstanceCreationExpression(p):
    '''
    ClassInstanceCreationExpression : NEW ClassType L_PAREN R_PAREN
    | NEW ClassType L_PAREN ArgumentList R_PAREN
    '''
    rules_store.append(p.slice)

def p_ArgumentList(p):
    '''
    ArgumentList : Expression
    | ArgumentList COMMA Expression
    '''
    rules_store.append(p.slice)

def p_ArrayCreationExpression(p):
    '''
    ArrayCreationExpression : NEW PrimitiveType DimExprs Dims
    | NEW PrimitiveType DimExprs
    | NEW ClassType DimExprs Dims
    | NEW ClassType DimExprs
    '''
    rules_store.append(p.slice)

def p_DimExprs(p):
    '''
    DimExprs : DimExpr
    | DimExprs DimExpr
    '''
    rules_store.append(p.slice)

def p_DimExpr(p):
    '''
    DimExpr : L_SQBR Expression R_SQBR
    '''
    rules_store.append(p.slice)

def p_Dims(p):
    '''
    Dims : L_SQBR R_SQBR
    | Dims L_SQBR R_SQBR
    '''
    rules_store.append(p.slice)

def p_FieldAccess(p):
    '''
    FieldAccess : Primary DOT IDENTIFIER
    | SUPER DOT IDENTIFIER
    '''
    rules_store.append(p.slice)

def p_MethodInvocation(p):
    '''
    MethodInvocation : Name L_PAREN ArgumentList R_PAREN
    | Name L_PAREN R_PAREN
    | Primary DOT IDENTIFIER L_PAREN ArgumentList R_PAREN
    | Primary DOT IDENTIFIER L_PAREN R_PAREN
    | SUPER DOT IDENTIFIER L_PAREN ArgumentList R_PAREN
    | SUPER DOT IDENTIFIER L_PAREN R_PAREN
    '''
    rules_store.append(p.slice)

def p_ArrayAccess(p):
    '''
    ArrayAccess : Name L_SQBR Expression R_SQBR
    | PrimaryNoNewArray L_SQBR Expression R_SQBR
    '''
    rules_store.append(p.slice)

def p_PostfixExpression(p):
    '''
    PostfixExpression : Primary
    | Name
    | PostIncrementExpression
    | PostDecrementExpression
    '''
    rules_store.append(p.slice)

def p_PostIncrementExpression(p):
    '''
    PostIncrementExpression : PostfixExpression INCREMENT
    '''
    rules_store.append(p.slice)

def p_PostDecrementExpression(p):
    '''
    PostDecrementExpression : PostfixExpression DECREMENT
    '''
    rules_store.append(p.slice)

def p_UnaryExpression(p):
    '''
    UnaryExpression : PreIncrementExpression
    | PreDecrementExpression
    | PLUS UnaryExpression
    | MINUS UnaryExpression
    | UnaryExpressionNotPlusMinus
    '''
    rules_store.append(p.slice)

def p_PreIncrementExpression(p):
    '''
    PreIncrementExpression : INCREMENT UnaryExpression
    '''
    rules_store.append(p.slice)

def p_PreDecrementExpression(p):
    '''
    PreDecrementExpression : DECREMENT UnaryExpression
    '''
    rules_store.append(p.slice)

def p_UnaryExpressionNotPlusMinus(p):
    '''
    UnaryExpressionNotPlusMinus : PostfixExpression
    | BITWISE_NOT UnaryExpression
    | LOGICAL_NOT UnaryExpression
    | CastExpression
    '''
    rules_store.append(p.slice)

def p_CastExpression(p):
    '''
    CastExpression : L_PAREN PrimitiveType Dims R_PAREN UnaryExpression
    | L_PAREN PrimitiveType R_PAREN UnaryExpression
    | L_PAREN Expression R_PAREN UnaryExpressionNotPlusMinus
    | L_PAREN Name Dims R_PAREN UnaryExpressionNotPlusMinus
    '''
    rules_store.append(p.slice)

def p_MultiplicativeExpression(p):
    '''
    MultiplicativeExpression : UnaryExpression
    | MultiplicativeExpression MULT UnaryExpression
    | MultiplicativeExpression DIVIDE UnaryExpression
    | MultiplicativeExpression MODULO UnaryExpression
    '''
    rules_store.append(p.slice)

def p_AdditiveExpression(p):
    '''
    AdditiveExpression : MultiplicativeExpression
    | AdditiveExpression PLUS MultiplicativeExpression
    | AdditiveExpression MINUS MultiplicativeExpression
    '''
    rules_store.append(p.slice)

def p_ShiftExpression(p):
    '''
    ShiftExpression : AdditiveExpression
    | ShiftExpression L_SHIFT AdditiveExpression
    | ShiftExpression R_SHIFT AdditiveExpression
    '''
    rules_store.append(p.slice)

def p_RelationalExpression(p):
    '''
    RelationalExpression : ShiftExpression
    | RelationalExpression LST ShiftExpression
    | RelationalExpression GRT ShiftExpression
    | RelationalExpression LEQ ShiftExpression
    | RelationalExpression GEQ ShiftExpression
    | RelationalExpression INSTANCEOF ReferenceType
    '''
    rules_store.append(p.slice)

def p_EqualityExpression(p):
    '''
    EqualityExpression : RelationalExpression
    | EqualityExpression EQUALS RelationalExpression
    | EqualityExpression NOT_EQUAL RelationalExpression
    '''
    rules_store.append(p.slice)

def p_AndExpression(p):
    '''
    AndExpression : EqualityExpression
    | AndExpression BITWISE_AND EqualityExpression
    '''
    rules_store.append(p.slice)

def p_ExclusiveOrExpression(p):
    '''
    ExclusiveOrExpression : AndExpression
    | ExclusiveOrExpression BITWISE_XOR AndExpression
    '''
    rules_store.append(p.slice)

def p_InclusiveOrExpression(p):
    '''
    InclusiveOrExpression : ExclusiveOrExpression
    | InclusiveOrExpression BITWISE_OR ExclusiveOrExpression
    '''
    rules_store.append(p.slice)

def p_ConditionalAndExpression(p):
    '''
    ConditionalAndExpression : InclusiveOrExpression
    | ConditionalAndExpression LOGICAL_AND InclusiveOrExpression
    '''
    rules_store.append(p.slice)

def p_ConditionalOrExpression(p):
    '''
    ConditionalOrExpression : ConditionalAndExpression
    | ConditionalOrExpression LOGICAL_OR ConditionalAndExpression
    '''
    rules_store.append(p.slice)

def p_ConditionalExpression(p):
    '''
    ConditionalExpression : ConditionalOrExpression
    | ConditionalOrExpression QUESTION Expression COLON ConditionalExpression
    '''
    rules_store.append(p.slice)

def p_AssignmentExpression(p):
    '''
    AssignmentExpression : ConditionalExpression
    | Assignment
    | LambdaExpression
    '''
    rules_store.append(p.slice)

def p_Assignment(p):
    '''
    Assignment : LeftHandSide AssignmentOperator AssignmentExpression
    '''
    rules_store.append(p.slice)

def p_LeftHandSide(p):
    '''
    LeftHandSide : Name
    | FieldAccess
    | ArrayAccess
    '''
    rules_store.append(p.slice)

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
    rules_store.append(p.slice)
    #To check if I missed something

def p_Expression(p):
    '''
    Expression : AssignmentExpression
    '''
    rules_store.append(p.slice)

def p_LambdaExpression(p):
    '''
    LambdaExpression : LAMBDA L_PAREN FormalParameterList R_PAREN LAMBDA_TOKEN Block
    | LAMBDA L_PAREN R_PAREN LAMBDA_TOKEN Block
    '''
    rules_store.append(p.slice)

def p_ConstantExpression(p):
    '''
    ConstantExpression : Expression
    '''
    rules_store.append(p.slice)

def p_error(p):
    print("Syntax Error in line %d" %(p.lineno))


def format_print(LHS, RHS, index):
    print("<p>")
    for i in range(len(LHS)):
        if i == index:
            print("<span style='color:red; font-weight:bold'>" + str(LHS[i]) + "</span>")
        else:
            if str(type(LHS[i])) == "<class 'ply.yacc.YaccSymbol'>":
                print(str(LHS[i]), end=" ")
            else:
                print("<span style='color:blue'>" + str(LHS[i].value) + "</span>", end=" ")

    print("&emsp;<span style='color:black; font-weight:bold;'>----></span>&emsp;", end=" ")

    for i in range(len(RHS)):
        if str(type(RHS[i])) == "<class 'ply.yacc.YaccSymbol'>":
            print(str(RHS[i]), end=" ")
        else:
            print("<span style='color:blue'>" + str(RHS[i].value) + "</span>", end=" ")

    print("</p>")


def html_output(rules_store):
    print("<head><title> Parser for JAVA </title></head>")
    print("<body style='padding: 20px'> <h1> Rightmost Derrivation </h1> <hr>")
    LHS = [rules_store[-1][0]]
    RHS = []
    # print the derivation
    for rule in rules_store[::-1]:
        try:
            index = LHS.index(rule[0])
        except ValueError:
            print("Some Error occured")
            return

        # store the derrivation of the current rule
        part_RHS = [symbol for symbol in rule[1:]]
        RHS = RHS[:index] + part_RHS + RHS[index + 1:]
        format_print(LHS, RHS, index)
        LHS = RHS

    print("</body>")


def main():
    tokens = lexer.tokens
    parser = yacc.yacc()
    inputfile = sys.argv[1]
    file_out = inputfile.split('/')[-1].split('.')[0]
    code = open(inputfile, 'r').read()
    code += "\n"
    parser.parse(code, debug=0)
    sys.stdout = open(file_out + ".html", 'w')
    html_output(rules_store)
    # for i in rules_store:
        # print(i)


if __name__ == "__main__":
    main()
