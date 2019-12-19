#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 10:49:59 2019

@author: hsauro, XJiang
"""

try:
    import tesbml as libsbml
except:
    import libsbml

def convertOperator (op):
    if op == 'times':
        return '*' # To make sure there is space between symbols
    if op == 'plus':
        return '+'
    if op == 'minus':
        return '-'
    if op == 'divide':
        return '/'
    if op == 'power':
        return '^'
    if op == 'lt':
        return '<'
    if op == 'gt':
        return '>'
    if op == 'leq':
        return '\\ \\leq \\ '
    if op == 'geq':
        return '\\ \\geq \\ '
    if op == 'and':
        return '\\ \\mathrm{and}\\ '
    if op == 'or':
        return '\\ \\mathrm{or}\\ '
    if op == 'not':
        return '\\ \\mathrm{not}\\ '
    if op == 'eq':
        return '\\ == \\ '
   
   
def isParensOnLeft (ast):
    if (ast.getLeftChild().isOperator() or ast.getLeftChild().isBoolean) and (ast.getLeftChild().getPrecedence() < ast.getPrecedence()):
       return True
    else:
       return False
   
def isParensOnRight (ast):
    if ast.getRightChild().isNumber():
       return False
   
    if ast.getOperatorName () == 'plus' or ast.getOperatorName() == 'times':
       return ast.getRightChild().getPrecedence() < ast.getPrecedence()
    return ast.getRightChild().getPrecedence() <= ast.getPrecedence()
   

def convertToInfix (ast):
    lhs = ''; rhs = ''; frac = False; pwr = False;
    
    if ast.isFunction() :
       if ast.getName() == 'power': #the fix is here
           return '\\left(' + convertToInfix (ast.getLeftChild())+ '\\right)^{'+ convertToInfix(ast.getRightChild())+ '}'
       lhs = '\\' + ast.getName() + '\\left('      
       return lhs + convertToInfix (ast.getLeftChild()) + '\\right)'
       
   
    if ast.isBoolean():
       if ast.getName() == 'True' or ast.getName() == 'False':
          return '\\mathrm{' + ast.getName() + '}'
       else:  
          lhs = convertToInfix (ast.getLeftChild())

       op = ast.getName()
       opStr = convertOperator (op)
       if ast.getRightChild() != None:
          rhs = convertToInfix (ast.getRightChild())
          #if isParensOnRight (ast):
          #   rhs = '\\left(' + rhs + '\\right)'
         
          return lhs + opStr + rhs
       else:
          return opStr + lhs  
       
       
    if ast.isOperator():
       op = ast.getOperatorName(); 
       if op == 'divide':
          frac = True
    
       if op == 'power':
          pwr = True
           
       lhs = convertToInfix (ast.getLeftChild())
       if isParensOnLeft (ast):
          lhs = '\\left(' + lhs + '\\right)'
           
       
       opStr = convertOperator (op)
         
       rhs = convertToInfix (ast.getRightChild())
       if isParensOnRight (ast) and not pwr:  
          rhs = '\\left(' + rhs + '\\right)'  
          #print('2'+ ast.getName())
       if frac:
          return '\\frac{' + lhs + '}{' + rhs + '}'
       else:    
          return lhs + opStr + rhs

    if ast.isNumber():
       if ast.isReal():
          return (str (ast.getReal()))
       else:
          return (str (ast.getInteger()))
    else:
       return '\\mathrm{' + ast.getName() + '}'

     
#r = te.loada("""
#       
#function quadratic(x, a, b, c)
#     a*x^2 + b*x + c
#end
#     
#model testmodel1()    
#     
#     S1 -> S2; k1*k2*S1;
#     
#     at time > 10: k1 = k1 * 2, k2 = 0.2;
#     
#     k1 = 0.1; k2 = 0.2
#     S1 = 0;
#end
#""")
#
#te.saveToFile ('c:\\tmp\\latex.tex', sbmlUtils.sbml2latex(r.getSBML()))
#
#ast = libsbml.parseL3Formula ('a == True')
#if ast == None:
#    print ('Syntax Error in formula')
#else:
#   print (convertToInfix (ast))
#   
#ast = libsbml.parseL3Formula ('a*(b+c)')
#if ast == None:
#    print ('Syntax Error in formula')
#else:
#   print (convertToInfix (ast))