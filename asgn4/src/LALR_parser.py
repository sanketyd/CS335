#!/usr/bin/env python
import sys
import ply.lex as lex
import ply.yacc as yacc
import lexer
from three_address_code import TAC
from new_sym_table import ScopeTable

TAC = TAC()
ST = ScopeTable()

stackbegin = []
stackend = []

rules_store = []

def ResolveRHSArray(dictionary):
    return dictionary

# Section 19.2
def p_Goal(p):
    '''Goal : CompilationUnit'''
    rules_store.append(p.slice)

# Section 19.3
def p_Identfier(p):
    '''Identifier : IDENTIFIER'''
    p[0] = p[1]

def p_Literal(p):
    ''' Literal : IntegerConst
    | FloatConst
    | CharConst
    | StringConst
    | NullConst
    '''
    p[0] = p[1]
    p[0]['idVal'] = str(p[0]['idVal'])
    rules_store.append(p.slice)

def p_IntegerConst(p):
    '''
    IntegerConst : INT_CONSTANT
    '''
    p[0] = {
        'idVal' : p[1],
        'type' : 'INT'
    }


def p_FloatConst(p):
    '''
    FloatConst : FLOAT_CONSTANT
    '''
    p[0] = {
        'idVal' : p[1],
        'type' : 'FLOAT'
    }


def p_CharConst(p):
    '''
    CharConst : CHAR_CONSTANT
    '''
    p[0] = {
        'idVal' : p[1],
        'type' : 'CHAR'
    }


def p_StringConst(p):
    '''
    StringConst : STR_CONSTANT
    '''
    p[0] = {
        'idVal' : p[1],
        'type' : 'STR'
    }


def p_NullConst(p):
    '''
    NullConst : NULL
    '''
    p[0] = {
        'idVal' : p[1],
        'type' : 'NULL'
    }


# Section 19.4

def p_Type(p):
    ''' Type : PrimitiveType
    | ReferenceType
    '''
    p[0] = p[1]
    rules_store.append(p.slice)

def p_PrimitiveType(p):
    ''' PrimitiveType : NumericType
    | BOOLEAN
    '''
    if type(p[1]) != type({}):
        p[0] = {
            'type' : 'INT'  # treat boolean as integer for now
        }
    else:
        p[0] = p[1]
    rules_store.append(p.slice)

def p_NumericType(p):
    ''' NumericType : IntegralType
    | FloatingPointType
    '''
    p[0] = p[1]
    rules_store.append(p.slice)

def p_IntegralType(p):
    ''' IntegralType : BYTE
    | SHORT
    | INT
    | LONG
    | CHAR
    '''
    p[0] = {
        'type' : p[1]
    }
    rules_store.append(p.slice)

def p_FloatingPointType(p):
    ''' FloatingPointType : FLOAT
    | DOUBLE
    '''
    p[0] = {
        'type' : p[1]
    }
    rules_store.append(p.slice)

def p_ReferenceType(p):
    ''' ReferenceType : ArrayType
    | ClassType
    '''
    p[0] = p[1]
    rules_store.append(p.slice)

def p_ClassType(p):
    '''
    ClassType : Name
    '''
    p[0] = p[1]
    rules_store.append(p.slice)

def p_ArrayType(p):
    ''' ArrayType : PrimitiveType L_SQBR R_SQBR
    | Name L_SQBR R_SQBR Mark2
    | ArrayType L_SQBR R_SQBR
    '''
    if len(p) == 3:
        p[0] = {
            'type' : p[1]['type'] + p[2] + p[3]
        }
    else:
        p[0] = {
            'type' : p[1]['place'] + p[2] + p[3]
        }

    rules_store.append(p.slice)

def p_Mark2(p):
    ''' Mark2 : '''

# Section 19.5
def p_Name(p):
    ''' Name : SimpleName
    | QualifiedName'''
    p[0] = p[1]
    rules_store.append(p.slice)

def p_SimpleName(p):
    ''' SimpleName : Identifier'''
    p[0] = {
        'place' : p[1],
        'isnotjustname' : False
    }
    rules_store.append(p.slice)

def p_QualifiedName(p):
    ''' QualifiedName : Name DOT Identifier'''
    p[0]= {
        'place' : p[1]['place'] + "." + p[3]
    }
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
    ClassDeclaration : Modifiers CLASS Identifier Inherit ClassBody
    | Modifiers CLASS Identifier ClassBody
    | CLASS Identifier Inherit ClassBody
    | CLASS Identifier ClassBody
    '''
    rules_store.append(p.slice)

def p_Inherit(p):
    '''
    Inherit : EXTENDS ClassType
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
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[3]

    rules_store.append(p.slice)

def p_VariableDeclarator(p):
    '''
    VariableDeclarator : VariableDeclaratorId
    | VariableDeclaratorId ASSIGN VariableInitializer
    '''
    if len(p) == 2:
        p[0] = p[1]
        return
    elif type(p[3]) != type({}):
        return
    if 'is_array' in p[3].keys() and p[3]['is_array']:
        TAC.emit('declare',p[1][0],p[3]['place'],p[3]['type'])
        p[0] = p[1]
    else:
        TAC.emit(p[1][0], p[3]['place'], '', p[2])
        p[0] = p[1]
    rules_store.append(p.slice)

def p_VariableDeclaratorId(p):
    '''
    VariableDeclaratorId : Identifier
    | VariableDeclaratorId L_SQBR R_SQBR
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    rules_store.append(p.slice)

def p_VariableInitializer(p):
    '''
    VariableInitializer : Expression
    | ArrayInitializer
    '''
    p[0] = p[1]
    rules_store.append(p.slice)

def p_MethodDeclaration(p):
    '''
    MethodDeclaration : MethodHeader MethodBody
    '''
    TAC.emit('ret','','','')
    # TAC.emit('label',p[1][0],'','')
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
    MethodDeclarator : Identifier L_PAREN R_PAREN Mark1
    | Identifier L_PAREN FormalParameterList R_PAREN
    '''
    if len(p) == 5:
        p[0] = [p[1]]
        stackbegin.append(p[1])
        stackend.append(p[1])
        TAC.emit('label', p[1], '', '')
    rules_store.append(p.slice)

def p_Mark1(p):
    '''Mark1 : '''

def p_FormalParametersList(p):
    '''
    FormalParameterList : FormalParameter
    | FormalParameterList COMMA FormalParameter
    '''
    if len(p) == 2:
        p[0] = p[1]
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
    p[0] = p[1]
    rules_store.append(p.slice)

def p_LocalVariableDeclarationStatement(p):
    '''
    LocalVariableDeclarationStatement : LocalVariableDeclaration STMT_TERMINATOR
    '''
    p[0] = p[1]
    rules_store.append(p.slice)

def p_LocalVariableDeclaration(p):
    '''
    LocalVariableDeclaration : Type VariableDeclarators
    '''
    for i in p[2]:
        ST.insert_in_sym_table('symbol', idName=i, idType=p[1]['type'])
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
    p[0] = p[1]
    rules_store.append(p.slice)

def p_StatementNoShortIf(p):
    '''
    StatementNoShortIf : StatementWithoutTrailingSubstatement
    | LabeledStatementNoShortIf
    | IfThenElseStatementNoShortIf
    | WhileStatementNoShortIf
    | ForStatementNoShortIf
    '''
    p[0] = p[1]
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
    LabeledStatement : Identifier COLON Statement
    '''
    rules_store.append(p.slice)

def p_LabeledStatementNoShortIf(p):
    '''
    LabeledStatementNoShortIf : Identifier COLON StatementNoShortIf
    '''
    rules_store.append(p.slice)

def p_ExpressionStatement(p):
    '''
    ExpressionStatement : StatementExpression STMT_TERMINATOR
    '''
    p[0] = p[1]
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
    BreakStatement : BREAK Identifier STMT_TERMINATOR
    | BREAK STMT_TERMINATOR
    '''
    if(len(p)==3 and p[1]=='break'):
        TAC.emit('goto', stackend[-1], '', '')
    rules_store.append(p.slice)

def p_ContinueStatement(p):
    '''
    ContinueStatement : CONTINUE Identifier STMT_TERMINATOR
    | CONTINUE STMT_TERMINATOR
    '''
    if(len(p)==3 and p[1]=='continue'):
        TAC.emit('goto', stackbegin[-1], '', '')
    rules_store.append(p.slice)

def p_ReturnStatement(p):
    '''
    ReturnStatement : RETURN Expression STMT_TERMINATOR
    | RETURN STMT_TERMINATOR
    '''
    if(len(p)==3 and p[1]=='return'):
        TAC.emit('ret', '', '', '')
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
    p[0] = p[1]
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
    if len(p) == 2:
        p[0] = p[1]
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
    if len(p) == 2:
        p[0] = p[1]
    rules_store.append(p.slice)

def p_ArrayCreationExpression(p):
    '''
    ArrayCreationExpression : NEW PrimitiveType DimExprs Dims
    | NEW PrimitiveType DimExprs
    | NEW ClassType DimExprs Dims
    | NEW ClassType DimExprs
    '''
    if len(p) == 4:
        p[0] = {
            'type' : p[2],
            'place'  : p[3]['place'],
            'is_array' : True
        }
    rules_store.append(p.slice)

def p_DimExprs(p):
    '''
    DimExprs : DimExpr
    | DimExprs DimExpr
    '''
    if len(p) == 2:
        p[0] = p[1]
    rules_store.append(p.slice)

def p_DimExpr(p):
    '''
    DimExpr : L_SQBR Expression R_SQBR
    '''
    if p[2]['type'] == 'INT':
        p[0] = p[2]
    else:
        TAC.error("Error : Array declaration requires a size as integer : " + p[2]['place'])
    rules_store.append(p.slice)

def p_Dims(p):
    '''
    Dims : L_SQBR R_SQBR
    | Dims L_SQBR R_SQBR
    '''
    if len(p) == 3:
        p[0] = 1
    else:
        p[0] = 1 + p[1]
    rules_store.append(p.slice)

def p_FieldAccess(p):
    '''
    FieldAccess : Primary DOT Identifier
    | SUPER DOT Identifier
    '''
    rules_store.append(p.slice)

def p_MethodInvocation(p):
    '''
    MethodInvocation : Name L_PAREN ArgumentList R_PAREN
    | Name L_PAREN R_PAREN
    | Primary DOT Identifier L_PAREN ArgumentList R_PAREN
    | Primary DOT Identifier L_PAREN R_PAREN
    | SUPER DOT Identifier L_PAREN ArgumentList R_PAREN
    | SUPER DOT Identifier L_PAREN R_PAREN
    '''
    if p[2] == '(':
        if(p[1]['place'] == 'System.out.println'):
            TAC.emit('print',p[3]['place'],'','')
            p[0] = p[1]
        else:
            TAC.emit('call',p[1]['place'],'','')
            p[0] = p[1]
    rules_store.append(p.slice)

def p_ArrayAccess(p):
    '''
    ArrayAccess : Name L_SQBR Expression R_SQBR
    | PrimaryNoNewArray L_SQBR Expression R_SQBR
    '''
    p[0] = p[1]
    p[0]['access_type'] = 'array_access'
    p[0]['type'] = ST.get_attribute(p[0]['idVal'], 'type')
    p[0]['place'] = ST.get_attribute(p[0]['idVal'], 'place')
    p[0]['index_place'] = p[3]['place']
    del p[0]['idVal']
    rules_store.append(p.slice)

def p_PostfixExpression(p):
    '''
    PostfixExpression : Primary
    | Name
    | PostIncrementExpression
    | PostDecrementExpression
    '''
    p[0] = {}
    if 'idVal' in p[1].keys():
        p[0]['place'] = p[1]['idVal']
        p[0]['type'] = p[1]['type']
    elif 'place' in p[1].keys():
        if p[1]['isnotjustname'] == False:
            attributes = ST.lookup(p[1]['place'])
            if attributes == None:
                raise Exception("Undeclared Variable Used: %s)" %(p[1]['idVal']))
            else:
                p[0]['type'] = attributes['type']
                p[0]['place'] = p[1]['place']
    rules_store.append(p.slice)

def p_PostIncrementExpression(p):
    '''
    PostIncrementExpression : PostfixExpression INCREMENT
    '''
    if p[1]['type'].upper() == 'INT':
        TAC.emit(p[1]['place'], p[1]['place'], '1', '+')
        p[0] = {
            'place' : p[1]['place'],
            'type' : 'INT'
        }
    else:
        TAC.error("Error: increment operator can be used with integers only")
    rules_store.append(p.slice)

def p_PostDecrementExpression(p):
    '''
    PostDecrementExpression : PostfixExpression DECREMENT
    '''
    if p[1]['type'].upper() == 'INT':
        TAC.emit(p[1]['place'], p[1]['place'], '1', '-')
        p[0] = {
            'place' : p[1]['place'],
            'type' : 'INT'
        }
    else:
        TAC.error("Error: decrement operator can be used with integers only")
    rules_store.append(p.slice)

def p_UnaryExpression(p):
    '''
    UnaryExpression : PreIncrementExpression
    | PreDecrementExpression
    | PLUS UnaryExpression
    | MINUS UnaryExpression
    | UnaryExpressionNotPlusMinus
    '''
    if len(p) == 2:
        p[0] = p[1]
        return
    rules_store.append(p.slice)

def p_PreIncrementExpression(p):
    '''
    PreIncrementExpression : INCREMENT UnaryExpression
    '''
    if(p[2]['type']=='INT'):
        TAC.emit(p[2]['place'],p[2]['place'],'1','+')
        p[0] = {
            'place' : p[2]['place'],
            'type' : 'INT'
        }
    else:
        TAC.error("Error: increment operator can be used with integers only")

    rules_store.append(p.slice)

def p_PreDecrementExpression(p):
    '''
    PreDecrementExpression : DECREMENT UnaryExpression
    '''
    if(p[2]['type']=='INT'):
        TAC.emit(p[2]['place'],p[2]['place'],'1','-')
        p[0] = {
            'place' : p[2]['place'],
            'type' : 'INT'
        }
    else:
        TAC.error("Error: decrement operator can be used with integers only")
    rules_store.append(p.slice)

def p_UnaryExpressionNotPlusMinus(p):
    '''
    UnaryExpressionNotPlusMinus : PostfixExpression
    | BITWISE_NOT UnaryExpression
    | LOGICAL_NOT UnaryExpression
    | CastExpression
    '''
    if(len(p)==2):
        p[0] = p[1]
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
    if(len(p)==2):
        p[0] = p[1]
        return
    newPlace = ST.get_temp_var()
    p[0] = {
        'place' : newPlace,
        'type' : 'TYPE_ERROR'
    }
    if p[1]['type'] == 'TYPE_ERROR' or p[3]['type'] == 'TYPE_ERROR':
        return
    if p[2] == '*':
        print(p[1])
        print(p[3])
        if p[1]['type'].upper() == 'INT' and p[3]['type'].upper() == 'INT' :
            p[3] = ResolveRHSArray(p[3])
            p[1] = ResolveRHSArray(p[1])
            TAC.emit(newPlace,p[1]['place'], p[3]['place'], p[2])
            p[0]['type'] = 'INT'
        else:
            TAC.error('Error: Type is not compatible'+p[1]['place']+','+p[3]['place']+'.')
    elif p[2] == '/' :
        if p[1]['type'] == 'INT' and p[3]['type'] == 'INT' :
            p[3] = ResolveRHSArray(p[3])
            p[1] = ResolveRHSArray(p[1])
            TAC.emit(newPlace, p[1]['place'], p[3]['place'], p[2])
            p[0]['type'] = 'INT'
        else:
            TAC.error('Error: Type is not compatible' + p[1]['place'] + ',' + p[3]['place'] + '.')
    elif p[2] == '%':
        if p[1]['type'] == 'INT' and p[3]['type'] == 'INT' :
            p[3] =ResolveRHSArray(p[3])
            p[1] =ResolveRHSArray(p[1])
            TAC.emit(newPlace,p[1]['place'],p[3]['place'],p[2])
            p[0]['type'] = 'INT'
        else:
            TAC.error('Error: Type is not compatible' + p[1]['place'] + ',' + p[3]['place'] + '.')
    rules_store.append(p.slice)

def p_AdditiveExpression(p):
    '''
    AdditiveExpression : MultiplicativeExpression
    | AdditiveExpression PLUS MultiplicativeExpression
    | AdditiveExpression MINUS MultiplicativeExpression
    '''
    if len(p) == 2:
        p[0] = p[1]
        return
    newPlace = ST.get_temp_var()
    p[0] = {
        'place' : newPlace,
        'type' : 'TYPE_ERROR'
    }
    if p[1]['type'] == 'TYPE_ERROR' or p[3]['type'] == 'TYPE_ERROR':
        return

    if p[1]['type'].upper() == 'INT' and p[3]['type'].upper() == 'INT':
        p[3] = ResolveRHSArray(p[3])
        p[1] = ResolveRHSArray(p[1])
        TAC.emit(newPlace, p[1]['place'], p[3]['place'], p[2])
        p[0]['type'] = 'INT'
    else:
        TAC.error("Error: integer value is needed")
    rules_store.append(p.slice)

def p_ShiftExpression(p):
    '''
    ShiftExpression : AdditiveExpression
    | ShiftExpression L_SHIFT AdditiveExpression
    | ShiftExpression R_SHIFT AdditiveExpression
    '''
    if len(p) == 2:
        p[0] = p[1]
        return

    newPlace = ST.get_temp_var()
    p[0] = {
        'place' : newPlace,
        'type' : 'TYPE_ERROR'
    }
    if p[1]['type'] == 'TYPE_ERROR' or p[3]['type'] == 'TYPE_ERROR':
        return

    if p[1]['type'].upper() == 'INT' and p[3]['type'].upper() == 'INT':
        p[3] = ResolveRHSArray(p[3])
        p[1] = ResolveRHSArray(p[1])
        TAC.emit(newPlace, p[1]['place'], p[3]['place'], p[2])
        p[0]['type'] = 'INT'
    else:
        TAC.error("Error: integer value is needed")

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
    if len(p) == 2:
        p[0] = p[1]
        return
    l1 = ST.make_label()
    l2 = ST.make_label()
    l3 = ST.make_label()
    newPlace = ST.get_temp_var()
    p[0] = {
        'place' : newPlace,
        'type' : 'TYPE_ERROR'
    }
    if p[1]['type']=='TYPE_ERROR' or p[3]['type']=='TYPE_ERROR':
        return
    print(p[1])
    print(p[3])

    if p[1]['type'].upper() == 'INT' and p[3]['type'].upper() == 'INT' :
        if p[2]=='>':
            p[3] = ResolveRHSArray(p[3])
            p[1] = ResolveRHSArray(p[1])
            TAC.emit('ifgoto', p[1]['place'], 'gt ' + p[3]['place'], l2)
            TAC.emit('goto', l1, '', '')
            TAC.emit('label', l1, '', '')
            TAC.emit(newPlace, '0', '', '=')
            TAC.emit('goto', l3, '', '')
            TAC.emit('label', l2, '', '')
            TAC.emit(newPlace, '1', '', '=')
            TAC.emit('label', l3, '', '')
            p[0]['type'] = 'INT'
        elif p[2]=='>=':
            p[3] = ResolveRHSArray(p[3])
            p[1] = ResolveRHSArray(p[1])
            TAC.emit('ifgoto', p[1]['place'], 'geq ' + p[3]['place'], l2)
            TAC.emit('goto', l1, '', '')
            TAC.emit('label', l1, '', '')
            TAC.emit(newPlace, '0', '', '=')
            TAC.emit('goto', l3, '', '')
            TAC.emit('label', l2, '', '')
            TAC.emit(newPlace, '1', '', '=')
            TAC.emit('label', l3, '', '')
            p[0]['type'] = 'INT'
        elif p[2]=='<':
            p[3] = ResolveRHSArray(p[3])
            p[1] = ResolveRHSArray(p[1])
            TAC.emit('ifgoto', p[1]['place'], 'lt ' + p[3]['place'], l2)
            TAC.emit('goto', l1, '', '')
            TAC.emit('label', l1, '', '')
            TAC.emit(newPlace, '0', '', '=')
            TAC.emit('goto', l3, '', '')
            TAC.emit('label', l2, '', '')
            TAC.emit(newPlace, '1', '', '=')
            TAC.emit('label', l3, '', '')
            p[0]['type'] = 'INT'
        elif p[2]=='<=':
            p[3] = ResolveRHSArray(p[3])
            p[1] = ResolveRHSArray(p[1])
            TAC.emit('ifgoto', p[1]['place'], 'leq ' + p[3]['place'], l2)
            TAC.emit('goto', l1, '', '')
            TAC.emit('label', l1, '', '')
            TAC.emit(newPlace, '0', '', '=')
            TAC.emit('goto', l3, '', '')
            TAC.emit('label', l2, '', '')
            TAC.emit(newPlace, '1', '', '=')
            TAC.emit('label', l3, '', '')
            p[0]['type'] = 'INT'
    else:
        TAC.error('Error: Type is not compatible' + p[1]['place'] + ',' + p[3]['place'] + '.')
    rules_store.append(p.slice)

def p_EqualityExpression(p):
    '''
    EqualityExpression : RelationalExpression
    | EqualityExpression EQUALS RelationalExpression
    | EqualityExpression NOT_EQUAL RelationalExpression
    '''
    if(len(p)==2):
        p[0] = p[1]
        return
    l1 = ST.make_label()
    l2 = ST.make_label()
    l3 = ST.make_label()
    newPlace = ST.get_temp_var()
    p[0]={
        'place' : newPlace,
        'type' : 'TYPE_ERROR'
    }
    if p[1]['type']=='TYPE_ERROR' or p[3]['type']=='TYPE_ERROR':
        return
    if p[1]['type'] == 'INT' and p[3]['type'] == 'INT' :
        if(p[2][0]=='='):
            p[3] = ResolveRHSArray(p[3])
            p[1] = ResolveRHSArray(p[1])
            TAC.emit('ifgoto', p[1]['place'], 'eq ' + p[3]['place'], l2)
            ##### TODO: May delete the line below; I think!!
            TAC.emit('goto', l1, '', '')
            #####
            TAC.emit('label', l1, '', '')
            TAC.emit(newPlace, '0', '', '=')
            TAC.emit('goto', l3, '', '')
            TAC.emit('label', l2, '', '')
            TAC.emit(newPlace, '1', '', '=')
            TAC.emit('label', l3, '', '')
            p[0]['type'] = 'INT'
        else:
            p[3] = ResolveRHSArray(p[3])
            p[1] = ResolveRHSArray(p[1])
            TAC.emit('ifgoto', p[1]['place'], 'neq '+ p[3]['place'], l2)
            ###
            TAC.emit('goto', l1, '', '')
            ###
            TAC.emit('label', l1, '', '')
            TAC.emit(newPlace, '0', '', '=')
            TAC.emit('goto', l3, '', '')
            TAC.emit('label', l2, '', '')
            TAC.emit(newPlace, '1', '', '=')
            TAC.emit('label', l3, '', '')
            p[0]['type'] = 'INT'
    else:
        TAC.error('Error: Type is not compatible' + p[1]['place'] + ',' + p[3]['place'] + '.')
    rules_store.append(p.slice)

def p_AndExpression(p):
    '''
    AndExpression : EqualityExpression
    | AndExpression BITWISE_AND EqualityExpression
    '''
    if(len(p)==2):
        p[0] = p[1]
        return
    newPlace = ST.get_temp_var()
    p[0] = {
        'place' : newPlace,
        'type' : 'TYPE_ERROR'
    }
    if p[1]['type']=='TYPE_ERROR' or p[3]['type']=='TYPE_ERROR':
        return
    if p[1]['type'] == 'INT' and p[3]['type'] == 'INT' :
        p[3] =ResolveRHSArray(p[3])
        p[1] =ResolveRHSArray(p[1])
        TAC.emit(newPlace,p[1]['place'],p[3]['place'],'and')
        p[0]['type'] = 'INT'
    else:
        TAC.error('Error: Type is not compatible' + p[1]['place'] + ',' + p[3]['place'] + '.')
    rules_store.append(p.slice)

def p_ExclusiveOrExpression(p):
    '''
    ExclusiveOrExpression : AndExpression
    | ExclusiveOrExpression BITWISE_XOR AndExpression
    '''
    if(len(p)==2):
        p[0] = p[1]
        return
    newPlace = ST.get_temp_var()
    p[0] = {
        'place' : newPlace,
        'type' : 'TYPE_ERROR'
    }
    if p[1]['type']=='TYPE_ERROR' or p[3]['type']=='TYPE_ERROR':
        return
    if p[1]['type'] == 'INT' and p[3]['type'] == 'INT' :
        p[3] =ResolveRHSArray(p[3])
        p[1] =ResolveRHSArray(p[1])
        TAC.emit(newPlace,p[1]['place'],p[3]['place'],'xor')
        p[0]['type'] = 'INT'
    else:
        TAC.error('Error: Type is not compatible' + p[1]['place'] + ',' + p[3]['place'] + '.')
    rules_store.append(p.slice)

def p_InclusiveOrExpression(p):
    '''
    InclusiveOrExpression : ExclusiveOrExpression
    | InclusiveOrExpression BITWISE_OR ExclusiveOrExpression
    '''
    if(len(p)==2):
        p[0] = p[1]
        return
    newPlace = ST.get_temp_var()
    p[0] = {
        'place' : newPlace,
        'type' : 'TYPE_ERROR'
    }
    if p[1]['type']=='TYPE_ERROR' or p[3]['type']=='TYPE_ERROR':
        return
    if p[1]['type'] == 'INT' and p[3]['type'] == 'INT' :
        p[3] = ResolveRHSArray(p[3])
        p[1] = ResolveRHSArray(p[1])
        TAC.emit(newPlace, p[1]['place'], p[3]['place'], 'or')
        p[0]['type'] = 'INT'
    else:
        TAC.error('Error: Type is not compatible' + p[1]['place'] + ',' + p[3]['place'] + '.')
    rules_store.append(p.slice)

def p_ConditionalAndExpression(p):
    '''
    ConditionalAndExpression : InclusiveOrExpression
    | ConditionalAndExpression LOGICAL_AND InclusiveOrExpression
    '''
    if(len(p)==2):
        p[0] = p[1]
        return
    newPlace = ST.get_temp_var()
    p[0] = {
        'place' : newPlace,
        'type' : 'TYPE_ERROR'
    }
    if p[1]['type']=='TYPE_ERROR' or p[3]['type']=='TYPE_ERROR':
        p[0]=p[1]
        return
    if p[1]['type'] == 'INT' and p[3]['type'] == 'INT' :
        p[3] =ResolveRHSArray(p[3])
        p[1] =ResolveRHSArray(p[1])
        TAC.emit(newPlace, p[1]['place'], p[3]['place'], 'and')
        p[0]['type'] = 'INT'
    else:
        TAC.error('Error: Type is not compatible' + p[1]['place'] + ',' + p[3]['place'] + '.')
    rules_store.append(p.slice)

def p_ConditionalOrExpression(p):
    '''
    ConditionalOrExpression : ConditionalAndExpression
    | ConditionalOrExpression LOGICAL_OR ConditionalAndExpression
    '''
    if(len(p)==2):
        p[0] = p[1]
        return
    newPlace = ST.get_temp_var()
    p[0] = {
        'place' : newPlace,
        'type' : 'TYPE_ERROR'
    }
    if p[1]['type']=='TYPE_ERROR' or p[3]['type']=='TYPE_ERROR':
        return
    if p[1]['type'] == 'INT' and p[3]['type'] == 'INT' :
        p[3] = ResolveRHSArray(p[3])
        p[1] = ResolveRHSArray(p[1])
        TAC.emit(newPlace, p[1]['place'], p[3]['place'], 'or')
        p[0]['type'] = 'INT'
    else:
        TAC.error('Error: Type is not compatible' + p[1]['place'] + ',' + p[3]['place'] + '.')
    rules_store.append(p.slice)

def p_ConditionalExpression(p):
    '''
    ConditionalExpression : ConditionalOrExpression
    | ConditionalOrExpression QUESTION Expression COLON ConditionalExpression
    '''
    if len(p) == 2:
        p[0] = p[1]
    rules_store.append(p.slice)

def p_AssignmentExpression(p):
    '''
    AssignmentExpression : ConditionalExpression
    | Assignment
    | LAMBDA LambdaExpression
    '''
    if len(p) == 2:
        p[0] = p[1]
    rules_store.append(p.slice)

def p_Assignment(p):
    '''
    Assignment : LeftHandSide AssignmentOperator AssignmentExpression
    '''
    print(p[1])
    print(p[3])
    if 'access_type' not in p[1].keys():
        # LHS is a simple ID
        attributes = ST.lookup(p[1]['place'])
        if attributes == None:
            raise Exception('Undeclared Variable Used: %s' %(p[1]['place']))

        if 'place' in p[3].keys():
            TAC.emit(p[1]['place'], p[3]['place'], '', p[2])
        else:
            if attributes['type'].upper() == p[3]['type'].upper():
                TAC.emit(p[1]['idVal'], p[3]['place'], '', p[2])
            else:
                raise Exception("Type Mismatch for symbol: %s" %(p[3]['place']))
    elif p[1]['access_type'] == 'array_access':
        # LHS is array
        pass
    rules_store.append(p.slice)

def p_LeftHandSide(p):
    '''
    LeftHandSide : Name
    | FieldAccess
    | ArrayAccess
    '''
    p[0] = p[1]
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
    p[0] = p[1]

    rules_store.append(p.slice)
    #To check if I missed something

def p_Expression(p):
    '''
    Expression : AssignmentExpression
    '''
    p[0] = p[1]
    rules_store.append(p.slice)

def p_LambdaExpression(p):
    '''
    LambdaExpression : L_PAREN FormalParameterList R_PAREN LAMBDA_TOKEN Block
    | L_PAREN R_PAREN LAMBDA_TOKEN Block
    '''
    rules_store.append(p.slice)

def p_ConstantExpression(p):
    '''
    ConstantExpression : Expression
    '''
    p[0] = p[1]
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

    try:
        d = int(sys.argv[2])
    except:
        d = 0
    parser.parse(code, debug=d)

    print("******************")
    for i in TAC.code_list:
        print(i)
    TAC.generate()


if __name__ == "__main__":
    main()
