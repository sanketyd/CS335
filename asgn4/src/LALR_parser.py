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
    p[0]['is_var'] = False
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
        'type' : p[1].upper()
    }
    rules_store.append(p.slice)

def p_FloatingPointType(p):
    ''' FloatingPointType : FLOAT
    | DOUBLE
    '''
    p[0] = {
        'type' : p[1].upper()
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
    ''' ArrayType : PrimitiveType Dims
    | Name Dims
    '''
    if 'place' not in p[1].keys():
        p[0] = {
            'type' : p[1]['type']
        }
    else:
        p[0] = {
            'type' : p[1]['place'],
        }
    p[0]['is_array'] = True
    p[0]['arr_size'] = p[2]
    rules_store.append(p.slice)

# Section 19.5
def p_Name(p):
    ''' Name : SimpleName
    | QualifiedName'''
    p[0] = p[1]
    p[0]['is_var'] = True
    rules_store.append(p.slice)

def p_SimpleName(p):
    ''' SimpleName : Identifier'''
    p[0] = {
        'place' : p[1],
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
    if len(p) == 4:
        for i in p[2]:
            ST.insert_in_sym_table(idName=i, idType=p[1]['type'])
    rules_store.append(p.slice)

def p_VariableDeclarators(p):
    '''
    VariableDeclarators : VariableDeclarator
    | VariableDeclarators COMMA VariableDeclarator
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

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
        t = ST.get_temp_var()
        TAC.emit(t, '1', '', '=')
        for i in p[3]['place']:
            TAC.emit(t, t, i, '*')
        TAC.emit('declare', p[1], t, p[3]['type'])
        p[0] = (p[1], p[3]['place'])
    else:
        TAC.emit(p[1][0], p[3]['place'], '', p[2])
        p[0] = p[1]
    rules_store.append(p.slice)

def p_VariableDeclaratorId(p):
    '''
    VariableDeclaratorId : Identifier
    '''
    p[0] = p[1]
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
    ST.end_scope()
    ST.insert_in_sym_table(p[1]['name'], p[1]['type'], is_func=True, args=p[1]['args'])
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
    p[0] = {}
    if len(p) == 5:
        # ST.insert_in_sym_table(p[3]['name'], p[2]['type'], is_func=True, args=p[3]['args'])
        # TODO
        pass
    elif len(p) == 4:
        # TODO
        pass
    elif len(p) == 3:
        p[0]['name'] = p[2]['name']
        p[0]['args'] = p[2]['args']
        if type(p[1]) == type({}):
            if 'is_array' in p[1].keys():
                p[0]['type'] = (p[1]['type'], p[1]['arr_size'])
            else:
                p[0]['type'] = (p[1]['type'], 0)
        else:
            p[0]['type'] = 'VOID'
    rules_store.append(p.slice)

def p_MethodDeclarator(p):
    '''
    MethodDeclarator : Identifier L_PAREN MethodDeclMark1 R_PAREN
    | Identifier L_PAREN MethodDeclMark1 FormalParameterList R_PAREN
    '''
    p[0] = {
        'name' : p[1],
    }
    if len(p) == 6:
        p[0]['args'] = p[4]
    else:
        p[0]['args'] = []

    stackbegin.append(p[1])
    stackend.append(p[1])
    if len(p) == 6:
        for parameter in p[4]:
            ST.insert_in_sym_table(parameter['place'],parameter['type'].upper())
    TAC.emit('label', p[1], '', '')
    rules_store.append(p.slice)

def p_MehodDeclMark1(p):
    '''
    MethodDeclMark1 :
    '''
    ST.create_new_table(p[-2])

def p_FormalParametersList(p):
    '''
    FormalParameterList : FormalParameter
    | FormalParameterList COMMA FormalParameter
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]
    rules_store.append(p.slice)

def p_FormalParameter(p):
    '''
    FormalParameter : Type VariableDeclaratorId
    '''
    p[0] = {
        'place' : p[2][0],
        'type' : p[1]['type']
    }
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
        if 'is_array' not in p[1].keys():
            ST.insert_in_sym_table(idName=i, idType=p[1]['type'])
        else:
            if len(i[1]) != int(p[1]['arr_size']):
                raise Exception("Dimension mismatch for array: %s" %(i[0]))
            ST.insert_in_sym_table(idName=i[0], idType=p[1]['type'], is_array=True, arr_size=i[1])
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
    p[0] = p[1]
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
    p[0] = p[1]
    rules_store.append(p.slice)

def p_IfThenStatement(p):
    '''
    IfThenStatement : IF L_PAREN Expression R_PAREN IfMark1 Statement IfMark2
    '''
    rules_store.append(p.slice)

def p_IfThenElseStatement(p):
    '''
    IfThenElseStatement : IF L_PAREN Expression R_PAREN IfMark1 StatementNoShortIf ELSE IfMark3 Statement IfMark4
    '''
    rules_store.append(p.slice)

def p_IfThenElseStatementNoShortIf(p):
    '''
    IfThenElseStatementNoShortIf : IF L_PAREN Expression R_PAREN IfMark1 StatementNoShortIf ELSE IfMark3 StatementNoShortIf IfMark4
    '''
    rules_store.append(p.slice)

def p_IfMark1(p):
    ''' IfMark1 : '''
    l1 = ST.make_label()
    l2 = ST.make_label()
    TAC.emit('ifgoto', p[-2]['place'], 'eq 0', l2)
    TAC.emit('goto', l1, '', '')
    TAC.emit('label', l1, '', '')
    # TODO: Create new scope here
    p[0] = [l1, l2]

def p_IfMark2(p):
    ''' IfMark2 : '''
    ## TODO: End scope here
    TAC.emit('label', p[-2][1], '', '')

def p_IfMark3(p):
    ''' IfMark3 : '''
    l3 = ST.make_label()
    TAC.emit('goto', l3, '', '')
    TAC.emit('label', p[-3][1], '', '')
    p[0] = [l3]

def p_IfMark4(p):
    ''' IfMark4 : '''
    ## TODO: end scope here
    TAC.emit('label', p[-2][0], '', '')

def p_SwitchStatement(p):
    '''
    SwitchStatement : SWITCH L_PAREN Expression R_PAREN SwMark2 SwitchBlock SwMark3
    '''
    if not p[3]['type'] == 'INT':
        raise Exception("Switch clause only supports Integer types")
    rules_store.append(p.slice)

def p_SwMark2(p):
    ''' SwMark2 : '''
    l1 = ST.make_label()
    l2 = ST.make_label()
    stackend.append(l1)
    TAC.emit('goto', l2, '', '')
    p[0] = [l1, l2]

def p_SwMark3(p):
    ''' SwMark3 : '''
    TAC.emit('label', p[-2][1], '', '')
    for i in range(len(p[-1]['labels'])):
        label = p[-1]['labels'][i]
        exp = p[-1]['expressions'][i]
        if exp == '':
            TAC.emit('goto', label, '', '')
        else:
            TAC.emit('ifgoto', p[-4]['place'], 'eq ' + exp, label)
    TAC.emit('label', p[-2][0], '', '')

def p_SwitchBlock(p):
    '''
    SwitchBlock : BLOCK_OPENER BLOCK_CLOSER
    | BLOCK_OPENER SwitchBlockStatementGroups BLOCK_CLOSER
    '''
    ## TODO: Handle start and end of new scope
    p[0] = p[2]
    rules_store.append(p.slice)

def p_SwitchBlockStatementGroups(p):
    '''
    SwitchBlockStatementGroups : SwitchBlockStatementGroup
    | SwitchBlockStatementGroups SwitchBlockStatementGroup
    '''
    p[0] = {
        'expressions' : [],
        'labels' : []
    }
    if len(p) == 2:
        p[0]['expressions'].append(p[1]['expression'])
        p[0]['labels'].append(p[1]['label'])
    else:
        p[0]['expressions'] = p[1]['expressions'] + [p[2]['expression']]
        p[0]['labels'] = p[1]['labels'] + [p[2]['label']]
    rules_store.append(p.slice)

def p_SwitchBlockStatementGroup(p):
    '''
    SwitchBlockStatementGroup : SwitchLabel BlockStatements
    '''
    p[0] = p[1]
    rules_store.append(p.slice)

def p_SwitchLabel(p):
    '''
    SwitchLabel : SwMark1 CASE ConstantExpression COLON
    | SwMark1 DEFAULT COLON
    '''
    p[0] = {}
    if len(p) == 5:
        if not p[3]['type'] == 'INT':
            raise Exception("Only Integers allowed for case comparisions")
        p[0]['expression'] = p[3]['place']
    else:
        p[0]['expression'] = ''
    p[0]['label'] = p[1]
    rules_store.append(p.slice)

def p_SwMark1(p):
    ''' SwMark1 : '''
    l = ST.make_label()
    TAC.emit('label', l, '', '')
    p[0] = l

def p_WhileStatement(p):
    '''
    WhileStatement : WHILE WhMark1 L_PAREN Expression R_PAREN WhMark2 Statement WhMark3
    '''
    rules_store.append(p.slice)

def p_WhileStatementNoShortIf(p):
    '''
    WhileStatementNoShortIf : WHILE WhMark1 L_PAREN Expression R_PAREN WhMark2 StatementNoShortIf WhMark3
    '''
    rules_store.append(p.slice)

def p_WhMark1(p):
    '''WhMark1 : '''
    l1 = ST.make_label()
    l2 = ST.make_label()
    l3 = ST.make_label()
    stackbegin.append(l1)
    stackend.append(l3)
    ST.create_new_table(l1)
    TAC.emit('label',l1,'','')
    p[0]=[l1,l2,l3]

def p_WhMark2(p):
    '''WhMark2 : '''
    TAC.emit('ifgoto',p[-2]['place'],'eq 0', p[-4][2])
    TAC.emit('goto',p[-4][1],'','')
    TAC.emit('label',p[-4][1],'','')

def p_WhMark3(p):
    '''WhMark3 : '''
    TAC.emit('goto',p[-6][0],'','')
    TAC.emit('label',p[-6][2],'','')
    ST.end_scope()
    stackbegin.pop()
    stackend.pop()

def p_DoStatement(p):
    '''
    DoStatement : DO doWhMark1 Statement WHILE doWhMark2 L_PAREN Expression R_PAREN doWhMark3 STMT_TERMINATOR
    '''
    rules_store.append(p.slice)

def p_doWhMark1(p):
    '''doWhMark1 : '''
    l1 = ST.make_label()
    l2 = ST.make_label()
    l3 = ST.make_label()
    stackbegin.append(l1)
    stackend.append(l3)
    ST.create_new_table(l1)
    TAC.emit('label',l1,'','')
    p[0]=[l1,l2,l3]

def p_doWhMark3(p):
    '''doWhMark3 : '''
    TAC.emit('ifgoto',p[-2]['place'],'eq 0', p[-7][2])
    TAC.emit('goto',p[-7][1],'','')
    TAC.emit('label',p[-7][2],'','')

def p_doWhMark2(p):
    '''doWhMark2 : '''
    #TAC.emit('goto',p[-3][1],'','')
    TAC.emit('label',p[-3][1],'','')
    ST.end_scope()
    stackbegin.pop()
    stackend.pop()

def p_ForStatement(p):
    '''
    ForStatement : FOR FoMark0 L_PAREN ForInit STMT_TERMINATOR FoMark1 Expression STMT_TERMINATOR ForUpdate R_PAREN FoMark2 Statement FoMark3
    | FOR FoMark0 L_PAREN STMT_TERMINATOR FoMark1 Expression STMT_TERMINATOR ForUpdate R_PAREN FoMark2 Statement FoMark3
    | FOR FoMark0 L_PAREN ForInit STMT_TERMINATOR FoMark1 STMT_TERMINATOR ForUpdate R_PAREN FoMark2 Statement FoMark3
    | FOR FoMark0 L_PAREN ForInit STMT_TERMINATOR FoMark1 Expression STMT_TERMINATOR R_PAREN FoMark4 Statement FoMark5
    | FOR FoMark0 L_PAREN ForInit STMT_TERMINATOR FoMark1 STMT_TERMINATOR R_PAREN FoMark4 Statement FoMark5
    | FOR FoMark0 L_PAREN STMT_TERMINATOR FoMark1 Expression STMT_TERMINATOR R_PAREN FoMark4 Statement FoMark5
    | FOR FoMark0 L_PAREN STMT_TERMINATOR FoMark1 STMT_TERMINATOR ForUpdate R_PAREN FoMark2 Statement FoMark3
    | FOR FoMark0 L_PAREN STMT_TERMINATOR FoMark1 STMT_TERMINATOR R_PAREN FoMark4 Statement FoMark5
    '''
    rules_store.append(p.slice)

def p_ForStatementNoShortIf(p):
    '''
    ForStatementNoShortIf : FOR FoMark0 L_PAREN ForInit STMT_TERMINATOR FoMark1 Expression STMT_TERMINATOR ForUpdate R_PAREN FoMark2 StatementNoShortIf FoMark3
    | FOR FoMark0 L_PAREN STMT_TERMINATOR FoMark1 Expression STMT_TERMINATOR ForUpdate R_PAREN FoMark2 StatementNoShortIf FoMark3
    | FOR FoMark0 L_PAREN ForInit STMT_TERMINATOR FoMark1 STMT_TERMINATOR ForUpdate R_PAREN FoMark2 StatementNoShortIf FoMark3
    | FOR FoMark0 L_PAREN ForInit STMT_TERMINATOR FoMark1 Expression STMT_TERMINATOR R_PAREN FoMark4 StatementNoShortIf FoMark5
    | FOR FoMark0 L_PAREN ForInit STMT_TERMINATOR FoMark1 STMT_TERMINATOR R_PAREN FoMark4 StatementNoShortIf FoMark5
    | FOR FoMark0 L_PAREN STMT_TERMINATOR FoMark1 Expression STMT_TERMINATOR R_PAREN FoMark4 StatementNoShortIf FoMark5
    | FOR FoMark0 L_PAREN STMT_TERMINATOR FoMark1 STMT_TERMINATOR ForUpdate R_PAREN FoMark2 StatementNoShortIf FoMark3
    | FOR FoMark0 L_PAREN STMT_TERMINATOR FoMark1 STMT_TERMINATOR R_PAREN FoMark4 StatementNoShortIf FoMark5
    '''
    rules_store.append(p.slice)

def p_FoMark0(p):
    '''FoMark0 : '''
    l0 = ST.make_label()
    ST.create_new_table(l0)

def p_FoMark1(p):
    '''FoMark1 : '''
    l1 = ST.make_label()
    l2 = ST.make_label()
    l3 = ST.make_label()
    stackbegin.append(l1)
    stackend.append(l3)
    TAC.emit('label',l1,'','')
    p[0]=[l1,l2,l3]

def p_FoMark2(p):
    '''FoMark2 : '''
    TAC.emit('ifgoto',p[-4]['place'],'eq 0', p[-5][2])
    TAC.emit('goto',p[-5][1],'','')
    TAC.emit('label',p[-5][1],'','')

def p_FoMark4(p):
    '''FoMark4 : '''
    TAC.emit('ifgoto',p[-3]['place'],'eq 0', p[-4][2])
    TAC.emit('goto',p[-4][1],'','')
    TAC.emit('label',p[-4][1],'','')

def p_FoMark3(p):
    '''FoMark3 : '''
    TAC.emit('goto',p[-7][0],'','')
    TAC.emit('label',p[-7][2],'','')
    ST.end_scope()
    stackbegin.pop()
    stackend.pop()

def p_FoMark5(p):
    '''FoMark5 : '''
    TAC.emit('goto',p[-6][0],'','')
    TAC.emit('label',p[-6][2],'','')
    ST.end_scope()
    stackbegin.pop()
    stackend.pop()

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
    else:
        TAC.emit('ret', p[2]['place'], '', '')
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
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]
    rules_store.append(p.slice)

def p_ArrayCreationExpression(p):
    '''
    ArrayCreationExpression : NEW PrimitiveType DimExprs
    | NEW ClassType DimExprs
    '''
    if len(p) == 4:
        p[0] = {
            'type' : p[2]['type'],
            'arr_size' : p[3],
            'is_array' : True,
        }
    rules_store.append(p.slice)

def p_DimExprs(p):
    '''
    DimExprs : DimExpr
    | DimExprs DimExpr
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]
    rules_store.append(p.slice)

def p_DimExpr(p):
    '''
    DimExpr : L_SQBR Expression R_SQBR
    '''
    if p[2]['type'] == 'INT':
        p[0] = p[2]['place']
    else:
        raise Exception("Array declaration requires a size as integer : " + p[2]['place'])
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
    #TODO: Other types of invocation
    #Check return type of function in symbol table
    #Check in symbol table
    if p[2] == '(':
        if p[1]['place'] == 'System.out.println':
            if len(p) == 5:
                for parameter in p[3]:
                    TAC.emit('print',parameter['place'],'','')
        else:
            temp_var = ST.get_temp_var()
            if len(p) == 5:
                for parameter in p[3]:
                    TAC.emit('param',parameter['place'],'','')
            TAC.emit('call',p[1]['place'],temp_var,'')
            p[0] = {
                'place' : temp_var
            }
    rules_store.append(p.slice)

def p_ArrayAccess(p):
    '''
    ArrayAccess : Name DimExprs
    '''
    p[0] = {}
    attributes = ST.lookup(p[1]['place'])
    if attributes == None:
        raise Exception("Undeclared Symbol Used: %s" %(p[1]['place']))
    if not 'is_array' in attributes or not attributes['is_array']:
        raise Exception("Only array type can be indexed : %s" %(p[1]['place']))

    indexes = p[2]
    if not len(indexes) == len(attributes['arr_size']):
        raise Exception("Not a valid indexing for array %s" %(p[1]['place']))

    arr_size = attributes['arr_size']
    address_indices = p[2]
    t2 = ST.get_temp_var()
    TAC.emit(t2, address_indices[0], '', '=')
    for i in range(1, len(address_indices)):
        TAC.emit(t2, t2, arr_size[i], '*')
        TAC.emit(t2, t2, address_indices[i], '+')
    index = t2

    src = p[1]['place'] + '[' + str(index) + ']'
    t1 = ST.get_temp_var()
    TAC.emit(t1, src, '', '=')

    p[0]['type'] = attributes['type']
    p[0]['place'] = t1
    p[0]['access_type'] = 'array'
    p[0]['name'] = p[1]['place']
    p[0]['index'] = str(index)

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
        p[0]['is_var'] = False

    elif 'place' in p[1].keys() and 'is_var' in p[1].keys() and p[1]['is_var']:
        attributes = ST.lookup(p[1]['place'])
        if attributes == None:
            raise Exception("Undeclared Variable Used: %s" %(p[1]['place']))
        else:
            p[0]['type'] = attributes['type']
            p[0]['place'] = p[1]['place']

    elif 'place' in p[1].keys():
        p[0] = p[1]
        #TODO: Temporarily removing to run method invocation
        # p[0]['type'] = p[1]['type']
        # p[0]['place'] = p[1]['place']

    elif 'is_array' in p[1].keys():
        p[0]['place'] = p[1]['arr_size']
        p[0]['type'] = p[1]['type']
        p[0]['is_array'] = True
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

# Checked
def p_PreIncrementExpression(p):
    '''
    PreIncrementExpression : INCREMENT UnaryExpression
    '''
    if(p[2]['type'].upper() == 'INT'):
        TAC.emit(p[2]['place'],p[2]['place'],'1','+')
        p[0] = {
            'place' : p[2]['place'],
            'type' : 'INT'
        }
    else:
        TAC.error("Error: increment operator can be used with integers only")

    rules_store.append(p.slice)

# Checked
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

# Checked
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
        if p[1]['type'].upper() == 'INT' and p[3]['type'].upper() == 'INT' :
            # p[3] = ResolveRHSArray(p[3])
            # p[1] = ResolveRHSArray(p[1])
            TAC.emit(newPlace,p[1]['place'], p[3]['place'], p[2])
            p[0]['type'] = 'INT'
        else:
            TAC.error('Error: Type is not compatible'+p[1]['place']+','+p[3]['place']+'.')
    elif p[2] == '/' :
        if p[1]['type'] == 'INT' and p[3]['type'] == 'INT' :
            # p[3] = ResolveRHSArray(p[3])
            # p[1] = ResolveRHSArray(p[1])
            TAC.emit(newPlace, p[1]['place'], p[3]['place'], p[2])
            p[0]['type'] = 'INT'
        else:
            TAC.error('Error: Type is not compatible' + p[1]['place'] + ',' + p[3]['place'] + '.')
    elif p[2] == '%':
        if p[1]['type'] == 'INT' and p[3]['type'] == 'INT' :
            # p[3] =ResolveRHSArray(p[3])
            # p[1] =ResolveRHSArray(p[1])
            TAC.emit(newPlace,p[1]['place'],p[3]['place'],p[2])
            p[0]['type'] = 'INT'
        else:
            TAC.error('Error: Type is not compatible' + p[1]['place'] + ',' + p[3]['place'] + '.')
    rules_store.append(p.slice)

# Checked
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
        # p[3] = ResolveRHSArray(p[3])
        # p[1] = ResolveRHSArray(p[1])
        TAC.emit(newPlace, p[1]['place'], p[3]['place'], p[2])
        p[0]['type'] = 'INT'
    else:
        TAC.error("Error: integer value is needed")
    rules_store.append(p.slice)

# Checked
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
        # p[3] = ResolveRHSArray(p[3])
        # p[1] = ResolveRHSArray(p[1])
        TAC.emit(newPlace, p[1]['place'], p[3]['place'], p[2])
        p[0]['type'] = 'INT'
    else:
        TAC.error("Error: integer value is needed")

    rules_store.append(p.slice)

# Checked
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

    if p[1]['type'].upper() == 'INT' and p[3]['type'].upper() == 'INT' :
        if p[2]=='>':
            # p[3] = ResolveRHSArray(p[3])
            # p[1] = ResolveRHSArray(p[1])
            TAC.emit('ifgoto', p[1]['place'], 'gt ' + p[3]['place'], l2)
            TAC.emit('label', l1, '', '')
            TAC.emit(newPlace, '0', '', '=')
            TAC.emit('goto', l3, '', '')
            TAC.emit('label', l2, '', '')
            TAC.emit(newPlace, '1', '', '=')
            TAC.emit('label', l3, '', '')
            p[0]['type'] = 'INT'
        elif p[2]=='>=':
            # p[3] = ResolveRHSArray(p[3])
            # p[1] = ResolveRHSArray(p[1])
            TAC.emit('ifgoto', p[1]['place'], 'geq ' + p[3]['place'], l2)
            TAC.emit('label', l1, '', '')
            TAC.emit(newPlace, '0', '', '=')
            TAC.emit('goto', l3, '', '')
            TAC.emit('label', l2, '', '')
            TAC.emit(newPlace, '1', '', '=')
            TAC.emit('label', l3, '', '')
            p[0]['type'] = 'INT'
        elif p[2]=='<':
            # p[3] = ResolveRHSArray(p[3])
            # p[1] = ResolveRHSArray(p[1])
            TAC.emit('ifgoto', p[1]['place'], 'lt ' + p[3]['place'], l2)
            TAC.emit('label', l1, '', '')
            TAC.emit(newPlace, '0', '', '=')
            TAC.emit('goto', l3, '', '')
            TAC.emit('label', l2, '', '')
            TAC.emit(newPlace, '1', '', '=')
            TAC.emit('label', l3, '', '')
            p[0]['type'] = 'INT'
        elif p[2]=='<=':
            # p[3] = ResolveRHSArray(p[3])
            # p[1] = ResolveRHSArray(p[1])
            TAC.emit('ifgoto', p[1]['place'], 'leq ' + p[3]['place'], l2)
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

# Checked
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
            # p[3] = ResolveRHSArray(p[3])
            # p[1] = ResolveRHSArray(p[1])
            TAC.emit('ifgoto', p[1]['place'], 'eq ' + p[3]['place'], l2)
            TAC.emit('label', l1, '', '')
            TAC.emit(newPlace, '0', '', '=')
            TAC.emit('goto', l3, '', '')
            TAC.emit('label', l2, '', '')
            TAC.emit(newPlace, '1', '', '=')
            TAC.emit('label', l3, '', '')
            p[0]['type'] = 'INT'
        else:
            # p[3] = ResolveRHSArray(p[3])
            # p[1] = ResolveRHSArray(p[1])
            TAC.emit('ifgoto', p[1]['place'], 'neq '+ p[3]['place'], l2)
            TAC.emit('label', l1, '', '')
            TAC.emit(newPlace, '0', '', '=')
            TAC.emit('goto', l3, '', '')
            TAC.emit('label', l2, '', '')
            TAC.emit(newPlace, '1', '', '=')
            TAC.emit('label', l3, '', '')
            p[0]['type'] = 'INT'
    else:
        raise Exception('Only INT type comparisions supported: ' + p[1]['place'] + ' and' + p[3]['place'])
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
        # p[3] =ResolveRHSArray(p[3])
        # p[1] =ResolveRHSArray(p[1])
        TAC.emit(newPlace,p[1]['place'],p[3]['place'],'&')
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
        # p[3] =ResolveRHSArray(p[3])
        # p[1] =ResolveRHSArray(p[1])
        TAC.emit(newPlace,p[1]['place'],p[3]['place'],'^')
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
        # p[3] = ResolveRHSArray(p[3])
        # p[1] = ResolveRHSArray(p[1])
        TAC.emit(newPlace, p[1]['place'], p[3]['place'], '|')
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
        # p[3] =ResolveRHSArray(p[3])
        # p[1] =ResolveRHSArray(p[1])
        l1 = ST.make_label()
        TAC.emit(newPlace,p[1]['place'],'','=')
        TAC.emit('ifgoto',p[1]['place'],'eq 0',l1)
        TAC.emit(newPlace, p[1]['place'], p[3]['place'], '&')
        TAC.emit('label',l1,'','')
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
        # p[3] = ResolveRHSArray(p[3])
        # p[1] = ResolveRHSArray(p[1])
        l1 = ST.make_label()
        TAC.emit(newPlace,p[1]['place'],'','=')
        TAC.emit('ifgoto',p[1]['place'],'eq 1',l1)
        TAC.emit(newPlace, p[1]['place'], p[3]['place'], '|')
        TAC.emit('label',l1,'','')
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
    if 'access_type' not in p[1].keys():
        attributes = ST.lookup(p[1]['place'])
        if attributes['type'] == p[3]['type']:
            TAC.emit(p[1]['place'], p[3]['place'], '', p[2])
        else:
            raise Exception("Type Mismatch for symbol: %s" %(p[3]['place']))
    else:
        dest = p[1]['name'] + '[' + p[1]['index'] + ']'
        TAC.emit(dest, p[3]['place'], '', '=')


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
    ST.print_scope_table()


if __name__ == "__main__":
    main()
