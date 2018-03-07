#!/usr/bin/env python
import sys
import ply.lex as lex
import ply.yacc as yacc
import lexer

def main():
    tokens = lexer.Tokens().get_tokens()
    ###########################################################################

    def p_CompileUnit(p):
        ''' CompileUnit : PackageDeclaration ImportDeclarations TypeDeclaration
            | PackageDeclaration TypeDeclaration
            | ImportDeclarations TypeDeclaration
            | ImportDeclarations
            | TypeDeclaration
        '''

    def p_PackageDeclaration(p):
        ''' PackageDeclaration :
            | PACKAGE QualifiedIdentifier STMT_TERMINATOR'''

    def p_ImportDeclarations(p):
        ''' ImportDeclarations : ImportDeclaration
            | ImportDeclarations ImportDeclaration'''

    def p_ImportDeclaration(p):
        '''
        ImportDeclaration : ImportType STMT_TERMINATOR
        '''

    def p_ImportType(p):
        '''
        ImportType : SingleTypeImport
        | TypeOnDemandImport
        '''

    def p_SingleTypeImport(p):
        ''' SingleTypeImport : IMPORT QualifiedIdentifier'''

    def p_TypeOnDemandImport(p):
        ''' TypeOnDemandImport : IMPORT QualifiedIdentifier DOT MULT'''

    def p_TypeDeclaration(p):
        ''' TypeDeclaration : ClassDeclaration'''

    def p_ClassDeclaration(p):
        ''' ClassDeclaration : NormalClassDeclaration
            | EnumDeclaration'''

    def p_NormalClassDeclaration(p):
        ''' NormalClassDeclaration : CLASS IDENTIFIER ClassBody
            | CLASS IDENTIFIER TypeParameters ClassBody
            | CLASS IDENTIFIER TypeParameters EXTENDS TypeList ClassBody
            | CLASS IDENTIFIER EXTENDS TypeList ClassBody'''

    def p_EnumDeclaration(p):
        ''' EnumDeclaration : ENUM IDENTIFIER EnumBody '''

    #####################################################################################

    def p_Identifier(p):
        '''Identifier : IDENTIFIER'''

    def p_QualifiedIdentifier(p):
        '''QualifiedIdentifier : Identifier
            | QualifiedIdentifier DOT Identifier'''

    def p_ArrSignList(p):
        '''ArrSignList :
            | ArrSignList L_SQBR R_SQBR '''

    def p_Types(p):
        '''Types : Type ArrSignList'''

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

    def p_Type(p):
        '''Type : PrimType
            | ReferenceType '''

    def p_ReferenceType(p):
        '''ReferenceType : RefTypeComponent
            | ReferenceType DOT RefTypeComponent '''

    def p_RefTypeComponent(p):
        '''RefTypeComponent : Identifier
            | Identifier TypeArguments '''

    def p_TypeArguments(p):
        ''' TypeArguments : LST TypeArgumentList GRT'''

    def p_TypeArgumentList(p):
        ''' TypeArgumentList : TypeArgument
            | TypeArgumentList COMMA TypeArgument '''

    def p_TypeArgument(p):
        ''' TypeArgument : ReferenceType
            | ''' ## CONFUSION HERE

################################################################################

    def p_NonWildcardTypeArguments(p):
        ''' NonWildcardTypeArguments : LST TypeList GRT '''

    def p_TypeList(p):
        ''' TypeList : ReferenceType
            | TypeList COMMA ReferenceType '''

    def p_TypeArgumentsOrDiamond(p):
        ''' TypeArgumentsOrDiamond : LST GRT
            | TypeArguments '''

    def p_NonWildcardTypeArgumentsOrDiamond(p):
        ''' NonWildcardTypeArgumentsOrDiamond : LST GRT
            | NonWildcardTypeArguments '''

    def p_TypeParameters(p):
        ''' TypeParameters : LST TypeParameterList GRT '''

    def p_TypeParameterList(p):
        ''' TypeParameterList : TypeParameter
            | TypeParameterList COMMA TypeParameter '''

    def p_TypeParameter(p):
        ''' TypeParameter : Identifier
            | Identifier EXTENDS Bound '''
    def p_Bound(p):
        ''' Bound : ReferenceType
            | Bound BITWISE_AND ReferenceType '''

    ##################################################################################

    def p_Modifier(p):
        ''' Modifier : STATIC
            | ABSTRACT
            | FINAL '''

    ##################################################################################

    def p_ClassBody(p):
        ''' ClassBody : BLOCK_OPENER ClassBodyDeclaration BLOCK_CLOSER '''

    def p_ClassBodyDeclaration(p):
        ''' ClassBodyDeclaration : STMT_TERMINATOR
            | STATIC Block
            | Block
            | ModifierList MemberDeclaration '''

    def p_ModifierList(p):
        ''' ModifierList : Modifier
            | ModifierList Modifier '''

    def p_MemberDeclaration(p):
        ''' MemberDeclaration : MethodOrFieldDeclaration
            | VOID Identifier VoidMethodDeclaratorRest
            | Identifier ConstructorDeclaratorRest
            | GenericMethodOrConstructorDecl
            | ClassDeclaration
        '''

    def p_MethodOrFieldDeclaration(p):
        ''' MethodOrFieldDeclaration : Type Identifier MethodOrFieldRest '''

    def p_MethodOrFieldRest(p):
        ''' MethodOrFieldRest : FieldDeclaration STMT_TERMINATOR
            | MethodDeclaratorRest '''

    def p_FieldDeclaration(p):
        ''' FieldDeclaration : VariableDeclaratorRest VariableDeclaratorList '''

    def p_VariableDeclaratorList(p):
        ''' VariableDeclaratorList : VariableDeclarator
            | VariableDeclaratorList COMMA VariableDeclarator '''

    def p_MethodDeclaratorRest(p):
        ''' MethodDeclaratorRest : FormalParameters ArrSignList STMT_TERMINATOR
            | FormalParameters ArrSignList THROWS QualifiedIdentifierList STMT_TERMINATOR
            | FormalParameters ArrSignList Block
            | FormalParameters ArrSignList THROWS QualifiedIdentifierList Block '''

    def p_ConstructorDeclaratorRest(p):
        ''' ConstructorDeclaratorRest : FormalParameters Block
            | FormalParameters THROWS QualifiedIdentifierList Block '''

    def p_VoidMethodDeclaratorRest(p):
        ''' VoidMethodDeclaratorRest : FormalParameters STMT_TERMINATOR
            | FormalParameters THROWS QualifiedIdentifierList STMT_TERMINATOR
            | FormalParameters Block
            | FormalParameters THROWS QualifiedIdentifierList Block '''

    def p_GenericMethodOrConstructorDecl(p):
        ''' GenericMethodOrConstructorDecl : TypeParameters GenericMethodOrConstructorRest'''

    def p_GenericMethodOrConstructorRest(p):
        ''' GenericMethodOrConstructorRest : Type Identifier MethodDeclaratorRest
            | VOID Identifier MethodDeclaratorRest
            | Identifier ConstructorDeclaratorRest '''

    def p_QualifiedIdentifierList(p):
        '''
        QualifiedIdentifierList : QualifiedIdentifier
        | QualifiedIdentifier COMMA QualifiedIdentifierList
        '''

    ###########################################################################################

    def p_ConstantDeclaratorsRest(p):
        ''' ConstantDeclaratorsRest : ConstantDeclaratorRest ConstantDeclaratorList'''

    def p_ConstantDeclaratorList(p):
        ''' ConstantDeclaratorList :
            | ConstantDeclaratorList COMMA ConstantDeclarator '''

    def p_ConstantDeclaratorRest(p):
        ''' ConstantDeclaratorRest : ArrSignList ASSIGN VariableInitializer'''

    def p_ConstantDeclarator(p):
        ''' ConstantDeclarator : Identifier ConstantDeclaratorRest'''

##########################################################################################

    def p_FormalParameters(p):
        ''' FormalParameters : L_PAREN R_PAREN
            | L_PAREN FormalParameterDecls R_PAREN '''

    def p_FormalParameterDecls(p):
        ''' FormalParameterDecls : VariableModifierList Type FormalParameterDeclsRest '''

    def p_VariableModifierList(p):
        ''' VariableModifierList :
            | VariableModifierList VariableModifier '''

    def p_VariableModifier(p):
        '''
        VariableModifier : FINAL
        '''

    def p_FormalParameterDeclsRest(p):
        ''' FormalParameterDeclsRest : VariableDeclaratorId COMMA FormalParameterDecls
            | VariableDeclaratorId
            | DOT DOT DOT VariableDeclaratorId ''' #TODO what is this!!!

    def p_VariableDeclaratorId(p):
        '''VariableDeclaratorId : Identifier ArrSignList '''

    def p_VariableDeclarators(p):
        ''' VariableDeclarators : VariableDeclarator
            | VariableDeclarators COMMA VariableDeclarator '''

    def p_VariableDeclarator(p):
        ''' VariableDeclarator : Identifier VariableDeclaratorRest'''

    def p_VariableDeclaratorRest(p):
        ''' VariableDeclaratorRest : ArrSignList
            | ArrSignList ASSIGN VariableInitializer '''

    def p_VariableInitializer(p):
        ''' VariableInitializer : ArrayInitializer
            | Expression '''

    def p_ArrayInitializer(p):
        ''' ArrayInitializer : '''      #TODO

    #########################################################################

    def p_Block(p):
        ''' Block : BLOCK_OPENER BlockStatements BLOCK_CLOSER '''

    def p_BlockStatements(p):
        ''' BlockStatements :
            | BlockStatements BlockStatement '''

    def p_BlockStatement(p):
        ''' BlockStatement : LocalVariableDeclarationStatement
            | ClassDeclaration
            | Statement
            | Identifier COLON Statement ''' #TODO Check COLON token in lexer

    def p_LocalVariableDeclarationStatement(p):
        '''LocalVariableDeclarationStatement : VariableModifierList Type VariableDeclarators STMT_TERMINATOR '''

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
            | RETURN Identifier STMT_TERMINATOR
            | THROW Expression STMT_TERMINATOR
            | TRY Block Catches
            | TRY Block FINALLY
            | TRY Block Catches FINALLY '''

    def p_StatementExpression(p):
        ''' StatementExpression : Expression '''

    ###############################################################################

    def p_Catches(p):
        ''' Catches : CatchClause
            | Catches CatchClause '''

    def p_CatchClause(p):
        ''' CatchClause : CATCH L_PAREN VariableModifierList CatchType Identifier R_PAREN Block '''

    def p_CatchType(p):
        ''' CatchType : QualifiedIdentifier
            | CatchType  QualifiedIdentifier '''

    def p_Finally(p):
        ''' Finally : FINALLY Block '''

    #################################################################################

    def p_SwitchBlockStatementGroups(p):
        ''' SwitchBlockStatementGroups :
            | SwitchBlockStatementGroups SwitchBlockStatementGroup '''

    def p_SwitchBlockStatementGroup(p):
        ''' SwitchBlockStatementGroup : SwitchLabels BlockStatements '''

    def p_SwitchLabels(p):
        ''' SwitchLabels : SwitchLabel
            | SwitchLabels SwitchLabel '''

    def p_SwitchLabel(p):
        ''' SwitchLabel : CASE Expression COLON
            | CASE EnumConstantName COLON
            | DEFAULT COLON  ''' #TODO CheckToken

    def p_EnumConstantName(p):
        ''' EnumConstantName : Identifier '''

    def p_ForControl(p):
        ''' ForControl : ForVarControl
            | ForInit STMT_TERMINATOR STMT_TERMINATOR
            | ForInit STMT_TERMINATOR Expression STMT_TERMINATOR ForUpdate
            | ForInit STMT_TERMINATOR STMT_TERMINATOR ForUpdate
            | ForInit STMT_TERMINATOR Expression STMT_TERMINATOR '''

    def p_ForVarControl(p):
        ''' ForVarControl : VariableModifierList Type VariableDeclaratorId ForVarControlRest '''

    def p_ForVarControlRest(p):
        ''' ForVarControlRest : ForVariableDeclaratorRest STMT_TERMINATOR STMT_TERMINATOR
            | ForVariableDeclaratorRest STMT_TERMINATOR Expression STMT_TERMINATOR ForUpdate
            | ForVariableDeclaratorRest STMT_TERMINATOR STMT_TERMINATOR ForUpdate
            | ForVariableDeclaratorRest STMT_TERMINATOR Expression STMT_TERMINATOR
            | COLON Expression '''
    def p_ForVariableDeclaratorRest(p):
        ''' ForVariableDeclaratorRest : ASSIGN VariableInitializer
            |
            | ForVariableDeclaratorRest COMMA VariableDeclarator '''

    def p_ForInit(p):
        ''' ForInit : StatementExpression
            | ForInit COMMA StatementExpression '''

    def p_ForUpdate(p):
        ''' ForUpdate : StatementExpression
            | ForInit COMMA StatementExpression '''

    ###############################################################################################

    def p_Expression(p):
        ''' Expression : Expression1
            | Expression1 AssignmentOperator Expression1 '''
            # | LambdaExpression '''

    # def p_LambdaExpression(p):
        # ''' LambdaExpression : LambdaParameters LAMBDA_TOKEN LambdaBody'''

    # def p_LambdaParameters(p):
        # ''' LambdaParameters : Identifier
            # | L_PAREN R_PAREN
            # | L_PAREN FormalParameters R_PAREN
            # | L_PAREN QualifieIdentifierList R_PAREN '''

    # def p_LambdaBody(p):
        # ''' LambdaBody : Expression
            # | Block '''

    def p_AssignmentOperator(p):
        ''' AssignmentOperator : ASSIGN
            | PLUSEQ
            | MINUSEQ
            | MULTEQ
            | DIVEQ
            | MODEQ
            | LSHIFTEQ
            | RSHIFTEQ ''' #TODO check rest symbol

    def p_Expression1(p):
        ''' Expression1 : Expression2
            | Expression2 Expression1Rest '''

    def p_Expression1Rest(p):
        ''' Expression1Rest : Expression COLON Expression1 ''' #should add QUESTION before Expression

    def p_Expression2(p):
        ''' Expression2 : Expression3
            | Expression3 Expression2Rest '''

    def p_Expression2Rest(p):
        ''' Expression2Rest : InfixOpListExpression
            | INSTANCEOF Type '''

    def p_InfixOpListExpression(p):
        ''' InfixOpListExpression :
            | InfixOpListExpression InfixOp Expression3 '''

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

    def p_Expression3(p):
        ''' Expression3  : PrefixOp Expression3
            | L_PAREN Expression R_PAREN Expression3
            | L_PAREN Type R_PAREN Expression3
            | Primary SelectorList PostfixOpList '''

    def p_SelectorList(p):
        ''' SelectorList :
            | SelectorList Selector '''

    def p_PostfixOpList(p):
        ''' PostfixOpList :
            | PostfixOpList PostfixOp '''

    def p_PrefixOp(p):
        ''' PrefixOp : INCREMENT
            | DECREMENT
            | LOGICAL_NOT
            | BITWISE_NOT
            | PLUS
            | MINUS '''

    def p_PostfixOp(p):
        ''' PostfixOp : INCREMENT
            | DECREMENT '''

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

    def p_IdentifierDotList(p):
        ''' IdentifierDotList : Identifier
            | IdentifierDotList DOT Identifier '''

    def p_Literal(p):
        ''' Literal : INT_CONSTANT
            | FLOAT_CONSTANT
            | CHAR_CONSTANT
            | STR_CONSTANT
            | NULL ''' # OMITTED BOOLEAN lITERAL

    def p_ParExpression(p):
        ''' ParExpression : L_PAREN Expression R_PAREN '''

    def p_Arguments(p):
        ''' Arguments : L_PAREN R_PAREN
            | L_PAREN ExpressionList R_PAREN '''

    def p_ExpressionList(p):
        ''' ExpressionList : Expression
            | ExpressionList COMMA Expression '''

    def p_SuperSuffix(p):
        ''' SuperSuffix : Arguments
            | DOT Identifier
            | DOT Identifier Arguments '''

    def p_ExplicitGenericInvocationSuffix(p):
        '''  ExplicitGenericInvocationSuffix : SUPER SuperSuffix
            | Identifier Arguments '''

    #################################################################################

    def p_Creator(p):
        ''' Creator : NonWildcardTypeArguments CreatedName ClassCreatorRest
            | CreatedName ClassCreatorRest
            | CreatedName ArrayCreatorRest '''

    def p_CreatedName(p):
        ''' CreatedName : IdentifierTypeArgOrDiamond
            | CreatedName DOT IdentifierTypeArgOrDiamond '''

    def p_IdentifierTypeArgOrDiamond(p):
        ''' IdentifierTypeArgOrDiamond : Identifier TypeArgumentsOrDiamond
            | Identifier '''

    def p_ClassCreatorRest(p):
        ''' ClassCreatorRest : Arguments ClassBody
            | Arguments '''

    def p_ArrayCreatorRest(p):
        ''' ArrayCreatorRest : ''' #TODO

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

    def p_InnerCreator(p):
        ''' InnerCreator : Identifier ClassCreatorRest
            | Identifier NonWildcardTypeArgumentsOrDiamond ClassCreatorRest '''

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

    def p_ExplicitGenericInvocation(p):
        '''
        ExplicitGenericInvocation : NonWildcardTypeArguments ExplicitGenericInvocationSuffix
        '''

    ###############################################################################

    def p_EnumBody(p):
        '''
        EnumBody : EnumBody InnerEnumBody
        |
        '''

    def p_InnerEnumBody(p):
        ''' InnerEnumBody : EnumConstants COMMA EnumBodyDeclarations
            | EnumConstants COMMA
            | EnumConstants EnumBodyDeclarations
            | COMMA EnumBodyDeclarations
            | EnumConstants
            | COMMA
            | EnumBodyDeclarations '''


    def p_EnumConstants(p):
        ''' EnumConstants : EnumConstant
            | EnumConstants COMMA EnumConstant '''

    def p_EnumConstant(p):
        ''' EnumConstant : Identifier Arguments ClassBody
            | Identifier Arguments
            | Identifier ClassBody
            | Identifier '''

    def p_EnumBodyDeclarations(p):
        ''' EnumBodyDeclarations : STMT_TERMINATOR
            | EnumBodyDeclarations ClassBodyDeclaration '''

    def p_error(p):
            print("Syntax Error in Input!!")

    parser = yacc.yacc()
    inputfile = open("../test/Video.java",'r').read()
    inputfile += "\n"
    print(parser.parse(inputfile, debug=1))

if __name__ == "__main__":
    main()
