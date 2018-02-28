#!/usr/bin/env python
import sys
import ply.lex as lex
import ply.yacc as yacc
import lexer

def main():
	tokens = lexer.Tokens()._get_tokens()
	def p_Identifier(p):
		'''Identifier : IDENTIFIER'''
	
	def p_QualifiedIdentifier(p):
		'''QualifiedIdentifier : Identifier
			| QualifiedIdentifier DOT Identifier'''  
	###########################################################################

	def p_CompileUnit(p):
		''' CompileUnit : PackageDeclaration
			| ImportDeclarations SEMICOLON
			| TypeDeclaration SEMICOLON'''
	
	def p_PackageDeclaration(p):
		''' PackageDeclaration : 
			| PACKAGE QualifiedIdentifier SEMICOLON'''
	
	def p_ImportDeclarations(p):
		''' ImportDeclarations : ImportDeclaration
			| ImportDeclarations ImportDeclaration'''
	
	def p_ImportDeclaration(p):
		''' ImportDeclartion : SingleTypeImport
			| TypeOnDemandImport'''
	
	def p_SingleTypeImport(p):
		''' SingleTypeImport : IMPORT QualifiedIdentifier'''
	
	def p_TypeOnDemandImport(p):
		''' TypeOnDemandImport : IMPORT QualifiedIdentifier DOT MULT'''
	
	def p_TypeDeclartion(p):
		''' TypeDeclaration : ModifiedClassDeclaration SEMICOLON'''
	
	def p_ModifiedClassDeclaration(p):
		''' ModifiedClassDeclaration : Modifiers ClassDeclaration 
			| ClassDeclaration'''
	def p_ClassDeclaration(p):
		''' ClassDeclaration : NormalClassDeclaration
			| EnumDeclaration'''

	def p_NormalClassDeclaration(p):
		''' NormalClassDeclaration : CLASS IDENTIFIER ClassBody
			| CLASS IDENTIFIER TypeParameters ClassBody
			| CLASS IDENTIFIER TypeParameters EXTENDS Typelist ClassBody
			| CLASS IDENTIFIER Extends TypeList ClassBody'''
	
	def p_EnumDeclaration(p):
		''' EnumDeclaration : ENUM IDENTIFIER EnumBody '''

#####################################################################################
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
		''' TypeArguments : LST TypeArgumentList GST'''

	def p_TypeArgumentList(p):
		''' TypeArgumentList : TypeArgument 
			| TypeArgumentList COMMA TypeArgument '''
	
	def p_TypeArgument(p):
		''' TypeArgument : ReferenceType
			| ''' ## CONFUSION HERE

################################################################################

	def p_NonWildCardTypeArguments(p):
		''' NonWildCardTypeArguments : LST TypeList GST '''

	def p_TypeList(p):
		''' TypeList : ReferenceType
			| TypeList COMMA ReferenceType '''

	def p_TypeArgumentsOrDiamond(p):
		''' TYpeArgumentsOrDiamond : LST GST
			| TypeArguments '''

	def p_NonWildCardTypeArgumentsOrDiamond(p):
		''' NonWildCardTypeArgumentsOrDiamond : LST GST
			| NonWildCardTypeArguments '''

	def p_TypeParameters(p):
		''' TypeParameters : LST TypeParameterList GST '''

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

	def p_ClassBody(p):   ##TODO check
		''' ClassBody : 
			| ClassBody BLOCK_OPENER ClassBodyDeclarataion BLOCK_CLOSER '''

	def p_ClassBodyDeclaration(p):
		''' ClassBodyDeclaration : SEMICOLON
			| STATIC Block
			| Block
			| ModifierList MemberDeclaration '''

	def p_ModifierList(p):
		''' ModifierList : Modifier 
			| ModifierList Modifier '''

	def p_MemberDeclaration(p):
		''' MemberDeclaration : MethodOrFieldDecl
			| VOID Identifier VoidMethodDeclaratorRest
			| Identifier ConstructorDeclaratorRest
			| GenericMethodOrConstructorDecl
			| ClassDeclaration
		'''

	def p_MethodOrFieldDeclaration(p):
		''' MethodOrFoeldDeclaration : Type Identifier MethodOrFieldRest '''

	def p_MethodOrFieldRest(p):
		''' MethodOrFieldRest : FieldDeclarationRest SEMICOLON	
			| MethodDeclaratorRest '''

	def p_FieldDeclaration(p):
		''' FieldDeclaration : VariableDeclaratorRest VariableDeclaratorList '''

	def p_VariableDeclaratorList(p):
		''' VariableDeclaratorList : VariableDeclarator
			| VariableDeclaratorList COMMA VariableDeclarator '''

	def p_MethodDeclaratorRest(p):
		''' MethodDeclaratorRest : FormalParameters ArrSignList SEMICOLON
			| FormalParameters ArrSignList THROWS QualifiedIdentifierList SEMICOLON
			| FormalParameters ArrSignList Block
			| FormalParameters ArrSignList THROWS QualifiedIdentifierList Block '''
	
	def p_ConstructorDeclaratorRest(p):
		''' ConstructorDeclaratorRest : FormalParameters Block
			| FormalParameters THROWS QualifiedIdentifierList Block '''

	def p_VoidMethodDeclaratorRest(p):
		''' VoidMethodDeclaratorRest : FormalParameters SEMICOLON
			| FormalParameters THROWS QualifiedIdentifierList SEMICOLON
			| FormalParameters Block
			| FormalParameters THROWS QualifiedIdentifierList Block '''

	def p_GenericMethodOrConstructorDecl(p):
		''' GenericMethodOrConstructorDecl : TypeParameters GenericMethodOrConstructorRest'''

	def p_GenericMethodOrConstructorRest(p):
		''' GenericMethodOrConstructorRest : Type Identifier MethodDeclaratorRest
			| VOID Identifier MethodDeclaratorRest
			| Identifier ConstructorDeclaratorRest '''

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
		''' VariableModifier : FINAL
			| ANNOTATION ''' #TODO remove annotation

	def p_FormalParameterDeclsRest(p):
		''' FormalParameterDeclsRest : VariableDeclaratorId COMMA FormalParameterDecls
			| VariableDeclaratorId
			| DOT DOT DOT VariableDeeclaratorId ''' #TODO what is this!!!

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
		'''LocalVariableDeclarationStatement : VariableModifierList Type VariableDeclarators SEMICOLON '''

	def p_Statement(p):
		''' Statement : Block
			| SEMICOLON
			|
			| Identifier COLON Statement
			| StatementExpression SEMICOLON
			| IF ParExpression Statement
			| IF ParExpression Statement ELSE Statement
			| ASSERT Expression SEMICOLON
			| ASSERT Expression COLON Expression SEMICOLON
			| SWITCH ParExpression BLOCK_OPENER SwitchBlockStatementGroups BLOCK_CLOSER
			| WHILE ParExpression Statement
			| DO Statement WHILE ParExpression SEMICOLON
			| FOR L_PAREN ForControl R_PAREN Statement
			| BREAK SEMICOLON
			| BREAK Identifier SEMICOLON
			| Continue SEMICOLON
			| Continue Identifier SEMICOLON
			| RETURN SEMICOLON
			| RETURN Identifier SEMICOLON
			| THROW Expression SEMICOLON
			| TRY BLOCK Catches
			| TRY BLOCK FINALLY
			| TRY BLOCK Catches FINALLY '''

	def p_StatementExpression(p):
		''' StatementExpression : Expression '''
	
	###############################################################################
	
	def p_Catches(p):
		''' Catches : CatchClause
			| Catches CatchClause '''
	
	def p_CatchClause(p):
		''' CatchClause : catch L_PAREN VariableModifierList CatchType Identifier R_PAREN Block '''

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
			| ForInit SEMICOLON SEMICOLON
			| ForInit SEMICOLON Expression SEMICOLON ForUpdate
			| ForInit SEMICOLON SEMICOLON ForUpdate
			| ForInit SEMICOLON Expression SEMICOLON '''

	def p_ForVarControl(p):
		''' ForVarControl : VariableModifierList Type VariableDeclaratorId ForVarControlRest '''

	def p_ForVarControlRest(p):
		''' ForVarControlRest : ForVariableDeclaratorRest SEMICOLON SEMICOLON
			| ForVariableDeclaratorRest SEMICOLON Expression SEMICOLON ForUpdate
			| ForVariableDeclaratorRest SEMICOLON SEMICOLON ForUpdate
			| ForVariableDeclaratorRest SEMICOLON Expression SEMICOLON 
			| COLON Expression '''
	def p_ForVariableDeclaratorRest(p):
		''' ForVariableDeclaratorRest : ASSIGN VariableIntializer
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
			| Expression1 AssignmentOperator Expression1 
			| LambdaExpression '''
	def p_LambdaExpression(p):
		''' LambdaExpression : LambdaParameters MINUS GST LambdaBody'''

	def _LambdaParameters(p):
		''' LambdaParameters : Identifier
			| L_PAREN R_PAREN 
			| L_PAREN FormalParameters R_PAREN
			| L_PAREN QualifieIdentifierList R_PAREN '''

	def p_LambdaBody(p):
		''' LambdaBody : Expression
			| Block '''

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
			| EExpression2 Expression1Rest '''

	def p_Expression1Rest(p):
		''' Expression1Rest : QUESTION Expression COLON Expression1 '''

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
			| GST
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
			| BasicType MultArrSign DOT CLASS
			| VOID DOT CLASS '''
	
	def p_IdentifierDotList(p):
		''' IdentifierDotList : Identifier
			| IdentifierDotList DOT Identifier '''

	def p_Literal(p):
		''' Literal : IntegerLiteral
			| FloatingPointLiteral
			| CharacterLiteral
			| StringLiteral
			| BooleanLiteral
			| NullLiteral '''

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
		''' Creator : NonWildCardTypeArguments CreatedName ClassCreatorRest
			| CreatedName ClassCreatorRest
			| CreatorName ArrayCreatorRest '''

	def p_CreatedName(p):
		''' CreatedName : IdentifierTypeArgOrDiamond
			| CreatedName DOT IdentifierTypeArgOrDiamond '''
	def p_IdentifierTypeArgOrDiamond(p):
		''' IdentifierTypeArgOrDiamond : Identifier TypeArgumentsOrDiamond
			| Identifier '''
	
	def p_ClassCreatorRest(p):
		''' ClassCreatorRest : Arguments Classbody
			| Arguments '''

	def p_ArrayCreatorRest(p):
		''' ArrayCreatorRest : ''' #TODO

	def p_IdentifierSuffix(p):
		''' IdentifierSuffix : MultArrSign DOT CLASS
			| Expression
			|
			| Arguments
			| DOT CLASS
			| DOT ExplicitGenericInvocation
			| DOT THIS
			| DOT SUPER Arguments
			| DOT NEW NonWildCardArguments InnerCreator
			| DOT NEW InnerCreator '''

	def p_InnerCreator(p):
		''' InnerCreator : Identifier ClassCreatorRest 
			| Identifier NonWildCardTypeArgumentsOrDiamond ClassCreatorRest '''

	def p_Selector(p):
		''' Selector : DOT Identifier
			| DOT Identifier Arguments
			| DOT ExplicitGenericInvocation
			| DOT THIS
			| SUPER SuperSuffix
			| DOT NEW InnerCreator
			| DOT NEW NonWildCardTypeArguments Innercreator
			|
			| Expression '''

	###############################################################################

	def p_EnumBody(p):
		''' EnunmBody : 
			| EnumBody InnerEnumBody '''

	def p_InnerEnumBody(p):  #TODO confusion
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
		''' EnumBodyDeclarations : SEMICOLON
			| EnumBodyDeclarations ClassBodyDeclaration '''

	yacc.yacc()
	inputfile = open(sys.argv[1],'r').read()
	print(yacc.parse(inputfile))
	
if __name__ == "__main__":
	main()