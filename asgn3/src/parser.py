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
	def p_Types(p):
		'''Types : Type | TypeArr'''
	
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
	
	def p_TypeArr(p):
		'''TypeArr : PrimType L_SQBR R_SQBR 
			| TypeArr L_SQBR R_SQBR ''' 
	
	def p_ReferenceType(p):
		'''ReferenceType : RefTypeComponent 
			| ReferenceType DOT RefTypeComponent '''
	
	def p_RefTypeComponent(p):
		'''RefTypeComponent : Identifier 
			| Identifier TypeArguments '''
	
	def p_TypeArguments(p):
		''' TypeArguments : L_SHIFT TypeArgumentList R_SHIFT'''

	def p_TypeArgumentList(p):
		''' TypeArgumentList : TypeArgument 
			| TypeArgumentList COMMA TypeArgument '''
	
	def p_TypeArgument(p):
		''' TypeArgument : ReferenceType
			| QUESTION ...''' ## CONFUSION HERE

################################################################################


