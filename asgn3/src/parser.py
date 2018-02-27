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
			| QUESTION ...''' ## CONFUSION HERE

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
		''' Modifier: STATIC
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






























