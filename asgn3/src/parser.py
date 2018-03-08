#!/usr/bin/env python
import sys
import ply.lex as lex
import ply.yacc as yacc
import lexer

def main():
    tokens = lexer.Tokens().get_tokens()
    non_terminals = []
    ###########################################################################

    def p_CompileUnit(p):
        ''' CompileUnit : PackageDeclaration ImportDeclarations TypeDeclaration
            | PackageDeclaration TypeDeclaration
            | ImportDeclarations TypeDeclaration
            | ImportDeclarations
            | TypeDeclaration
        '''
        non_terminals.append(p.slice)

    def p_PackageDeclaration(p):
        ''' PackageDeclaration :
            | PACKAGE QualifiedIdentifier STMT_TERMINATOR'''
        non_terminals.append(p.slice)

    def p_ImportDeclarations(p):
        ''' ImportDeclarations : ImportDeclaration
            | ImportDeclarations ImportDeclaration'''
        non_terminals.append(p.slice)

    def p_ImportDeclaration(p):
        '''
        ImportDeclaration : ImportType STMT_TERMINATOR
        '''
        non_terminals.append(p.slice)

    def p_ImportType(p):
        '''
        ImportType : SingleTypeImport
        | TypeOnDemandImport
        '''
        non_terminals.append(p.slice)

    def p_SingleTypeImport(p):
        ''' SingleTypeImport : IMPORT QualifiedIdentifier'''
        non_terminals.append(p.slice)

    def p_TypeOnDemandImport(p):
        ''' TypeOnDemandImport : IMPORT QualifiedIdentifier DOT MULT'''
        non_terminals.append(p.slice)

    def p_TypeDeclaration(p):
        ''' TypeDeclaration : ClassDeclaration'''
        non_terminals.append(p.slice)

    def p_ClassDeclaration(p):
        ''' ClassDeclaration : NormalClassDeclaration
            | EnumDeclaration'''
        non_terminals.append(p.slice)

    def p_NormalClassDeclaration(p):
        ''' NormalClassDeclaration : CLASS IDENTIFIER ClassBody
            | CLASS IDENTIFIER TypeParameters ClassBody
            | CLASS IDENTIFIER TypeParameters EXTENDS TypeList ClassBody
            | CLASS IDENTIFIER EXTENDS TypeList ClassBody'''
        non_terminals.append(p.slice)

    def p_EnumDeclaration(p):
        ''' EnumDeclaration : ENUM IDENTIFIER EnumBody '''
        non_terminals.append(p.slice)

    #####################################################################################

    def p_Identifier(p):
        '''Identifier : IDENTIFIER'''
        non_terminals.append(p.slice)

    def p_QualifiedIdentifier(p):
        '''QualifiedIdentifier : Identifier
            | QualifiedIdentifier DOT Identifier'''
        non_terminals.append(p.slice)

    def p_ArrSignList(p):
        '''ArrSignList :
            | ArrSignList L_SQBR R_SQBR '''
        non_terminals.append(p.slice)

    def p_Types(p):
        '''Types : Type ArrSignList'''
        non_terminals.append(p.slice)

    def p_PrimType(p):
        '''PrimType : BOOLEAN
            | CHAR
            | DOUBLE
            | BYTE
            | SHORT
            | INT
            | LONG
            | VOID
            | FLOAT '''
        non_terminals.append(p.slice)

    def p_Type(p):
        '''Type : PrimType
            | ReferenceType '''
        non_terminals.append(p.slice)

    def p_ReferenceType(p):
        '''ReferenceType : RefTypeComponent
            | ReferenceType DOT RefTypeComponent '''
        non_terminals.append(p.slice)

    def p_RefTypeComponent(p):
        '''RefTypeComponent : Identifier
            | Identifier TypeArguments '''
        non_terminals.append(p.slice)

    def p_TypeArguments(p):
        ''' TypeArguments : LST TypeArgumentList GRT'''
        non_terminals.append(p.slice)

    def p_TypeArgumentList(p):
        ''' TypeArgumentList : TypeArgument
            | TypeArgumentList COMMA TypeArgument '''
        non_terminals.append(p.slice)

    def p_TypeArgument(p):
        ''' TypeArgument : ReferenceType
            | ''' ## CONFUSION HERE
        non_terminals.append(p.slice)

################################################################################

    def p_NonWildcardTypeArguments(p):
        ''' NonWildcardTypeArguments : LST TypeList GRT '''
        non_terminals.append(p.slice)

    def p_TypeList(p):
        ''' TypeList : ReferenceType
            | TypeList COMMA ReferenceType '''
        non_terminals.append(p.slice)

    def p_TypeArgumentsOrDiamond(p):
        ''' TypeArgumentsOrDiamond : LST GRT
            | TypeArguments '''
        non_terminals.append(p.slice)

    def p_NonWildcardTypeArgumentsOrDiamond(p):
        ''' NonWildcardTypeArgumentsOrDiamond : LST GRT
            | NonWildcardTypeArguments '''
        non_terminals.append(p.slice)

    def p_TypeParameters(p):
        ''' TypeParameters : LST TypeParameterList GRT '''
        non_terminals.append(p.slice)

    def p_TypeParameterList(p):
        ''' TypeParameterList : TypeParameter
            | TypeParameterList COMMA TypeParameter '''
        non_terminals.append(p.slice)

    def p_TypeParameter(p):
        ''' TypeParameter : Identifier
            | Identifier EXTENDS Bound '''
        non_terminals.append(p.slice)
    def p_Bound(p):
        ''' Bound : ReferenceType
            | Bound BITWISE_AND ReferenceType '''
        non_terminals.append(p.slice)

    ##################################################################################

    def p_ClassBody(p):
        ''' ClassBody : BLOCK_OPENER ClassBodyDeclarations BLOCK_CLOSER '''
        non_terminals.append(p.slice)

    def p_ClassDeclarations(p):
        '''
        ClassBodyDeclarations : ClassBodyDeclaration
        | ClassBodyDeclarations ClassBodyDeclaration
        '''
        non_terminals.append(p.slice)

    def p_ClassBodyDeclaration(p):
        ''' ClassBodyDeclaration : STMT_TERMINATOR
            | STATIC Block
            | Block
            | MemberDeclaration
            | ModifierList MemberDeclaration '''
        non_terminals.append(p.slice)

    def p_ModifierList(p):
        ''' ModifierList : Modifier
            | ModifierList Modifier '''
        non_terminals.append(p.slice)

    def p_Modifier(p):
        ''' Modifier : STATIC
            | FINAL '''
        non_terminals.append(p.slice)
            # ABSTRACT

    def p_MemberDeclaration(p):
        ''' MemberDeclaration : MethodOrFieldDeclaration
            | VOID Identifier VoidMethodDeclaratorRest
            | Identifier ConstructorDeclaratorRest
            | GenericMethodOrConstructorDecl
            | ClassDeclaration
        '''
        non_terminals.append(p.slice)

    def p_MethodOrFieldDeclaration(p):
        ''' MethodOrFieldDeclaration : Type Identifier MethodOrFieldRest '''
        non_terminals.append(p.slice)

    def p_MethodOrFieldRest(p):
        ''' MethodOrFieldRest : FieldDeclaration STMT_TERMINATOR
            | STMT_TERMINATOR
            | MethodDeclaratorRest '''
        non_terminals.append(p.slice)

    def p_FieldDeclaration(p):
        ''' FieldDeclaration : VariableDeclaratorRest VariableDeclaratorList '''
        non_terminals.append(p.slice)

    def p_VariableDeclaratorList(p):
        ''' VariableDeclaratorList : VariableDeclarator
            | VariableDeclaratorList COMMA VariableDeclarator '''
        non_terminals.append(p.slice)

    def p_MethodDeclaratorRest(p):
        ''' MethodDeclaratorRest : FormalParameters ArrSignList STMT_TERMINATOR
            | FormalParameters ArrSignList THROWS QualifiedIdentifierList STMT_TERMINATOR
            | FormalParameters ArrSignList Block
            | FormalParameters ArrSignList THROWS QualifiedIdentifierList Block '''
        non_terminals.append(p.slice)

    def p_ConstructorDeclaratorRest(p):
        ''' ConstructorDeclaratorRest : FormalParameters Block
            | FormalParameters THROWS QualifiedIdentifierList Block '''
        non_terminals.append(p.slice)

    def p_VoidMethodDeclaratorRest(p):
        ''' VoidMethodDeclaratorRest : FormalParameters STMT_TERMINATOR
            | FormalParameters THROWS QualifiedIdentifierList STMT_TERMINATOR
            | FormalParameters Block
            | FormalParameters THROWS QualifiedIdentifierList Block '''
        non_terminals.append(p.slice)

    def p_GenericMethodOrConstructorDecl(p):
        ''' GenericMethodOrConstructorDecl : TypeParameters GenericMethodOrConstructorRest'''
        non_terminals.append(p.slice)

    def p_GenericMethodOrConstructorRest(p):
        ''' GenericMethodOrConstructorRest : Type Identifier MethodDeclaratorRest
            | VOID Identifier MethodDeclaratorRest
            | Identifier ConstructorDeclaratorRest '''
        non_terminals.append(p.slice)

    def p_QualifiedIdentifierList(p):
        '''
        QualifiedIdentifierList : QualifiedIdentifier
        | QualifiedIdentifier COMMA QualifiedIdentifierList
        '''
        non_terminals.append(p.slice)

    ###########################################################################################

    def p_ConstantDeclaratorsRest(p):
        ''' ConstantDeclaratorsRest : ConstantDeclaratorRest ConstantDeclaratorList'''
        non_terminals.append(p.slice)

    def p_ConstantDeclaratorList(p):
        ''' ConstantDeclaratorList :
            | ConstantDeclaratorList COMMA ConstantDeclarator '''
        non_terminals.append(p.slice)

    def p_ConstantDeclaratorRest(p):
        ''' ConstantDeclaratorRest : ArrSignList ASSIGN VariableInitializer'''
        non_terminals.append(p.slice)

    def p_ConstantDeclarator(p):
        ''' ConstantDeclarator : Identifier ConstantDeclaratorRest'''
        non_terminals.append(p.slice)

##########################################################################################

    def p_FormalParameters(p):
        ''' FormalParameters : L_PAREN R_PAREN
            | L_PAREN FormalParameterDecls R_PAREN '''
        non_terminals.append(p.slice)

    def p_FormalParameterDecls(p):
        ''' FormalParameterDecls : VariableModifierList Type FormalParameterDeclsRest '''
        non_terminals.append(p.slice)

    def p_VariableModifierList(p):
        ''' VariableModifierList :
            | VariableModifierList VariableModifier '''
        non_terminals.append(p.slice)

    def p_VariableModifier(p):
        '''
        VariableModifier : FINAL
        '''
        non_terminals.append(p.slice)

    def p_FormalParameterDeclsRest(p):
        ''' FormalParameterDeclsRest : VariableDeclaratorId COMMA FormalParameterDecls
            | VariableDeclaratorId
            | DOT DOT DOT VariableDeclaratorId ''' #TODO what is this!!!
        non_terminals.append(p.slice)

    def p_VariableDeclaratorId(p):
        '''VariableDeclaratorId : Identifier ArrSignList '''
        non_terminals.append(p.slice)

    def p_VariableDeclarators(p):
        ''' VariableDeclarators : VariableDeclarator
            | VariableDeclarators COMMA VariableDeclarator '''
        non_terminals.append(p.slice)

    def p_VariableDeclarator(p):
        ''' VariableDeclarator : Identifier VariableDeclaratorRest'''
        non_terminals.append(p.slice)

    def p_VariableDeclaratorRest(p):
        ''' VariableDeclaratorRest : ArrSignList
            | ArrSignList ASSIGN VariableInitializer '''
        non_terminals.append(p.slice)

    def p_VariableInitializer(p):
        ''' VariableInitializer : ArrayInitializer
            | Expression '''
        non_terminals.append(p.slice)

    def p_ArrayInitializer(p):
        ''' ArrayInitializer : '''      #TODO
        non_terminals.append(p.slice)

    #########################################################################

    def p_Block(p):
        ''' Block : BLOCK_OPENER BlockStatements BLOCK_CLOSER '''
        non_terminals.append(p.slice)

    def p_BlockStatements(p):
        ''' BlockStatements :
            | BlockStatements BlockStatement '''
        non_terminals.append(p.slice)

    def p_BlockStatement(p):
        ''' BlockStatement : LocalVariableDeclarationStatement
            | ClassDeclaration
            | Statement
            | Identifier COLON Statement ''' #TODO Check COLON token in lexer
        non_terminals.append(p.slice)

    def p_LocalVariableDeclarationStatement(p):
        '''LocalVariableDeclarationStatement : VariableModifierList Type VariableDeclarators STMT_TERMINATOR '''
        non_terminals.append(p.slice)

    def p_Statement(p):
        ''' Statement : Block
            | STMT_TERMINATOR
            |
            | Identifier COLON Statement
            | StatementExpression STMT_TERMINATOR
            | IF ParExpression Statement
            | IF ParExpression Statement ELSE Statement
            | ASSERT Expression STMT_TERMINATOR
            | ASSERT Expression COLON Expression STMT_TERMINATOR
            | SWITCH ParExpression BLOCK_OPENER SwitchBlockStatementGroups BLOCK_CLOSER
            | WHILE ParExpression Statement
            | DO Statement WHILE ParExpression STMT_TERMINATOR
            | FOR L_PAREN ForControl R_PAREN Statement
            | BREAK STMT_TERMINATOR
            | BREAK Identifier STMT_TERMINATOR
            | CONTINUE STMT_TERMINATOR
            | CONTINUE Identifier STMT_TERMINATOR
            | RETURN STMT_TERMINATOR
            | RETURN QualifiedIdentifier STMT_TERMINATOR
            | THROW Expression STMT_TERMINATOR
            | TRY Block Catches
            | TRY Block FINALLY
            | TRY Block Catches FINALLY '''
        non_terminals.append(p.slice)

    def p_StatementExpression(p):
        ''' StatementExpression : Expression '''
        non_terminals.append(p.slice)

    ###############################################################################

    def p_Catches(p):
        ''' Catches : CatchClause
            | Catches CatchClause '''
        non_terminals.append(p.slice)

    def p_CatchClause(p):
        ''' CatchClause : CATCH L_PAREN VariableModifierList CatchType Identifier R_PAREN Block '''
        non_terminals.append(p.slice)

    def p_CatchType(p):
        ''' CatchType : QualifiedIdentifier
            | CatchType  QualifiedIdentifier '''
        non_terminals.append(p.slice)

    def p_Finally(p):
        ''' Finally : FINALLY Block '''
        non_terminals.append(p.slice)

    #################################################################################

    def p_SwitchBlockStatementGroups(p):
        ''' SwitchBlockStatementGroups :
            | SwitchBlockStatementGroups SwitchBlockStatementGroup '''
        non_terminals.append(p.slice)

    def p_SwitchBlockStatementGroup(p):
        ''' SwitchBlockStatementGroup : SwitchLabels BlockStatements '''
        non_terminals.append(p.slice)

    def p_SwitchLabels(p):
        ''' SwitchLabels : SwitchLabel
            | SwitchLabels SwitchLabel '''
        non_terminals.append(p.slice)

    def p_SwitchLabel(p):
        ''' SwitchLabel : CASE Expression COLON
            | CASE EnumConstantName COLON
            | DEFAULT COLON  ''' #TODO CheckToken
        non_terminals.append(p.slice)

    def p_EnumConstantName(p):
        ''' EnumConstantName : Identifier '''
        non_terminals.append(p.slice)

    def p_ForControl(p):
        ''' ForControl : ForVarControl
            | ForInit STMT_TERMINATOR STMT_TERMINATOR
            | ForInit STMT_TERMINATOR Expression STMT_TERMINATOR ForUpdate
            | ForInit STMT_TERMINATOR STMT_TERMINATOR ForUpdate
            | ForInit STMT_TERMINATOR Expression STMT_TERMINATOR '''
        non_terminals.append(p.slice)

    def p_ForVarControl(p):
        ''' ForVarControl : VariableModifierList Type VariableDeclaratorId ForVarControlRest '''
        non_terminals.append(p.slice)

    def p_ForVarControlRest(p):
        ''' ForVarControlRest : ForVariableDeclaratorRest STMT_TERMINATOR STMT_TERMINATOR
            | ForVariableDeclaratorRest STMT_TERMINATOR Expression STMT_TERMINATOR ForUpdate
            | ForVariableDeclaratorRest STMT_TERMINATOR STMT_TERMINATOR ForUpdate
            | ForVariableDeclaratorRest STMT_TERMINATOR Expression STMT_TERMINATOR
            | COLON Expression '''
        non_terminals.append(p.slice)
    def p_ForVariableDeclaratorRest(p):
        ''' ForVariableDeclaratorRest : ASSIGN VariableInitializer
            |
            | ForVariableDeclaratorRest COMMA VariableDeclarator '''
        non_terminals.append(p.slice)

    def p_ForInit(p):
        ''' ForInit : StatementExpression
            | ForInit COMMA StatementExpression '''
        non_terminals.append(p.slice)

    def p_ForUpdate(p):
        ''' ForUpdate : StatementExpression
            | ForInit COMMA StatementExpression '''
        non_terminals.append(p.slice)

    ###############################################################################################

    def p_Expression(p):
        ''' Expression : Expression1
            | Expression1 AssignmentOperator Expression1 '''
        non_terminals.append(p.slice)
            # | LambdaExpression '''

    # def p_LambdaExpression(p):
        # ''' LambdaExpression : LambdaParameters LAMBDA_TOKEN LambdaBody'''
        non_terminals.append(p.slice)

    # def p_LambdaParameters(p):
        # ''' LambdaParameters : Identifier
            # | L_PAREN R_PAREN
            # | L_PAREN FormalParameters R_PAREN
            # | L_PAREN QualifieIdentifierList R_PAREN '''
        non_terminals.append(p.slice)

    # def p_LambdaBody(p):
        # ''' LambdaBody : Expression
            # | Block '''
        non_terminals.append(p.slice)

    def p_AssignmentOperator(p):
        ''' AssignmentOperator : ASSIGN
            | PLUSEQ
            | MINUSEQ
            | MULTEQ
            | DIVEQ
            | MODEQ
            | LSHIFTEQ
            | RSHIFTEQ ''' #TODO check rest symbol
        non_terminals.append(p.slice)

    def p_Expression1(p):
        ''' Expression1 : Expression2
            | Expression2 Expression1Rest '''
        non_terminals.append(p.slice)

    def p_Expression1Rest(p):
        ''' Expression1Rest : Expression COLON Expression1 ''' #should add QUESTION before Expression
        non_terminals.append(p.slice)

    def p_Expression2(p):
        ''' Expression2 : Expression3
            | Expression3 Expression2Rest '''
        non_terminals.append(p.slice)

    def p_Expression2Rest(p):
        ''' Expression2Rest : InfixOpListExpression
            | INSTANCEOF Type '''
        non_terminals.append(p.slice)

    def p_InfixOpListExpression(p):
        ''' InfixOpListExpression :
            | InfixOpListExpression InfixOp Expression3 '''
        non_terminals.append(p.slice)

    #####################################################################################


    def p_InfixOp(p):
        ''' InfixOp : LOGICAL_OR
            | LOGICAL_AND
            | BITWISE_OR
            | BITWISE_AND
            | BITWISE_XOR
            | EQUALS
            | NOT_EQUAL
            | LST
            | GRT
            | LEQ
            | GEQ
            | L_SHIFT
            | R_SHIFT
            | PLUS
            | MINUS
            | MULT
            | DIVIDE
            | MODULO '''
        non_terminals.append(p.slice)

    def p_Expression3(p):
        ''' Expression3  : PrefixOp Expression3
            | L_PAREN Expression R_PAREN Expression3
            | L_PAREN Type R_PAREN Expression3
            | Primary SelectorList PostfixOpList '''
        non_terminals.append(p.slice)

    def p_SelectorList(p):
        ''' SelectorList :
            | SelectorList Selector '''
        non_terminals.append(p.slice)

    def p_PostfixOpList(p):
        ''' PostfixOpList :
            | PostfixOpList PostfixOp '''
        non_terminals.append(p.slice)

    def p_PrefixOp(p):
        ''' PrefixOp : INCREMENT
            | DECREMENT
            | LOGICAL_NOT
            | BITWISE_NOT
            | PLUS
            | MINUS '''
        non_terminals.append(p.slice)

    def p_PostfixOp(p):
        ''' PostfixOp : INCREMENT
            | DECREMENT '''
        non_terminals.append(p.slice)

    ###########################################################################

    def p_Primary(p):
        ''' Primary : Literal
            | ParExpression
            | THIS
            | THIS Arguments
            | SUPER SuperSuffix
            | NEW Creator
            | NonWildcardTypeArguments ExplicitGenericInvocationSuffix
            | NonWildcardTypeArguments THIS Arguments
            | IdentifierDotList
            | IdentifierDotList IdentifierSuffix
            | PrimType ArrSignList DOT CLASS
            | VOID DOT CLASS '''
        non_terminals.append(p.slice)

    def p_IdentifierDotList(p):
        ''' IdentifierDotList : Identifier
            | IdentifierDotList DOT Identifier '''
        non_terminals.append(p.slice)

    def p_Literal(p):
        ''' Literal : INT_CONSTANT
            | FLOAT_CONSTANT
            | CHAR_CONSTANT
            | STR_CONSTANT
            | NULL ''' # OMITTED BOOLEAN lITERAL
        non_terminals.append(p.slice)

    def p_ParExpression(p):
        ''' ParExpression : L_PAREN Expression R_PAREN '''
        non_terminals.append(p.slice)

    def p_Arguments(p):
        ''' Arguments : L_PAREN R_PAREN
            | L_PAREN ExpressionList R_PAREN '''
        non_terminals.append(p.slice)

    def p_ExpressionList(p):
        ''' ExpressionList : Expression
            | ExpressionList COMMA Expression '''
        non_terminals.append(p.slice)

    def p_SuperSuffix(p):
        ''' SuperSuffix : Arguments
            | DOT Identifier
            | DOT Identifier Arguments '''
        non_terminals.append(p.slice)

    def p_ExplicitGenericInvocationSuffix(p):
        '''  ExplicitGenericInvocationSuffix : SUPER SuperSuffix
            | Identifier Arguments '''
        non_terminals.append(p.slice)

    #################################################################################

    def p_Creator(p):
        ''' Creator : NonWildcardTypeArguments CreatedName ClassCreatorRest
            | CreatedName ClassCreatorRest
            | CreatedName ArrayCreatorRest '''
        non_terminals.append(p.slice)

    def p_CreatedName(p):
        ''' CreatedName : IdentifierTypeArgOrDiamond
            | CreatedName DOT IdentifierTypeArgOrDiamond '''
        non_terminals.append(p.slice)

    def p_IdentifierTypeArgOrDiamond(p):
        ''' IdentifierTypeArgOrDiamond : Identifier TypeArgumentsOrDiamond
            | Identifier '''
        non_terminals.append(p.slice)

    def p_ClassCreatorRest(p):
        ''' ClassCreatorRest : Arguments ClassBody
            | Arguments '''
        non_terminals.append(p.slice)

    def p_ArrayCreatorRest(p):
        ''' ArrayCreatorRest : ''' #TODO
        non_terminals.append(p.slice)

    def p_IdentifierSuffix(p):
        ''' IdentifierSuffix : ArrSignList DOT CLASS
            | Expression
            |
            | Arguments
            | DOT CLASS
            | DOT ExplicitGenericInvocation
            | DOT THIS
            | DOT SUPER Arguments
            | DOT NEW NonWildcardTypeArguments InnerCreator
            | DOT NEW InnerCreator '''
        non_terminals.append(p.slice)

    def p_InnerCreator(p):
        ''' InnerCreator : Identifier ClassCreatorRest
            | Identifier NonWildcardTypeArgumentsOrDiamond ClassCreatorRest '''
        non_terminals.append(p.slice)

    def p_Selector(p):
        ''' Selector : DOT Identifier
            | DOT Identifier Arguments
            | DOT ExplicitGenericInvocation
            | DOT THIS
            | SUPER SuperSuffix
            | DOT NEW InnerCreator
            | DOT NEW NonWildcardTypeArguments InnerCreator
            |
            | Expression '''
        non_terminals.append(p.slice)

    def p_ExplicitGenericInvocation(p):
        '''
        ExplicitGenericInvocation : NonWildcardTypeArguments ExplicitGenericInvocationSuffix
        '''
        non_terminals.append(p.slice)

    ###############################################################################

    def p_EnumBody(p):
        '''
        EnumBody : EnumBody InnerEnumBody
        |
        '''
        non_terminals.append(p.slice)

    def p_InnerEnumBody(p):
        ''' InnerEnumBody : EnumConstants COMMA EnumBodyDeclarations
            | EnumConstants COMMA
            | EnumConstants EnumBodyDeclarations
            | COMMA EnumBodyDeclarations
            | EnumConstants
            | COMMA
            | EnumBodyDeclarations '''
        non_terminals.append(p.slice)


    def p_EnumConstants(p):
        ''' EnumConstants : EnumConstant
            | EnumConstants COMMA EnumConstant '''
        non_terminals.append(p.slice)

    def p_EnumConstant(p):
        ''' EnumConstant : Identifier Arguments ClassBody
            | Identifier Arguments
            | Identifier ClassBody
            | Identifier '''
        non_terminals.append(p.slice)

    def p_EnumBodyDeclarations(p):
        ''' EnumBodyDeclarations : STMT_TERMINATOR
            | EnumBodyDeclarations ClassBodyDeclaration '''
        non_terminals.append(p.slice)

    def p_error(p):
        print("Synatx error in line: ", p.lineno)

    parser = yacc.yacc()
    inputfile = open(sys.argv[1],'r').read()
    inputfile += "\n"
    print(parser.parse(inputfile, debug=0))
    sys.stdout = open("out.html", 'w')

if __name__ == "__main__":
    main()
