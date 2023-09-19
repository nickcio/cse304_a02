# Nicholas Ciotoli 113325368 nciotoli
# Adam Lipson 114339915 alipson

import ply.yacc as yacc
from decaf_lexer import tokens

def p_program(p):
    """program : program class_decl
               | empty"""
    if p[2]:
        p[0] = p[1] + [p[2]] #program + class_decl
    else:
        p[0] = [] #empty

def p_class_decl(p):
    """class_decl : CLASS id '{' class_body_decl_mult '}'
                  | CLASS id '(' EXTENDS id ')' '{' class_body_decl_mult '}'"""
    n = len(p)
    if n == 6:
        p[0] = (p[2], #id
                p[4]) #class body decl mult
    elif n == 10:
        p[0] = (p[2], #class id
                p[5], #ext id
                p[8]) #class body decl mult

def p_class_body_decl_mult(p):
    """class_body_decl_mult : class_body_decl_mult class_body_decl
                            | class_body_decl"""
    if p[2]:
        p[0] = p[1] + [p[2]] #bodies
    else:
        p[0] = [p[1]] #body

def p_class_body_decl(p):
    """class_body_decl : field_decl
                       | method_decl
                       | constructor_decl"""
    p[0] = p[1]
    
def p_field_decl(p):
    """field_decl : modifier var_decl"""
    p[0] = (p[1], #modifier
            p[2]) #var decl

def p_modifier(p):
    """modifier : visibility STATIC
                | visibility
       visibility : PUBLIC
                  | PRIVATE
                  | empty"""
    n = len(p)
    if n == 3:
        p[0] = (p[1],p[2])
    elif n == 2:
        p[0] = (p[1])
    
def p_var_decl(p):
    """var_decl : type variables"""
    p[0] = (p[1], #type
            p[2]) #variables

def p_type(p):
    """type : INT_CONST
            | FLOAT_CONST
            | STRING_CONST
            | id"""
    p[0] = p[1]
    
def p_variables(p):
    """variables : variables variable
                 | variable"""
    if p[2]:
        p[0] = p[1] + [p[2]] #variables
    else:
        p[0] = [p[1]] #variable

def p_variable(p):
    """variable : id"""
    p[0] = p[1]

def p_method_decl(p):
    """method_decl : modifier type_void id formals block
                   | modifier type_void id block
       type_void : type
                 | VOID"""
    n = len(p)
    if n == 6:
        p[0] = (p[1], #modifier
                p[2], #type
                p[3], #id
                p[4], #formals
                p[5]) #block
    elif n == 5:
        p[0] = (p[1], #modifier
                p[2], #type
                p[3], #id
                p[4]) #block

def p_constructor_decl(p):
    """constructor_decl : modifier id formals block
                        | modifier id block"""
    n = len(p)
    if n == 5:
        p[0] = (p[1], #modifier
                p[2], #id
                p[3], #formals
                p[4]) #block
    elif n == 4:
        p[0] = (p[1], #modifier
                p[2], #id
                p[3]) #block
        
def p_formals(p):
    """formals : formals formal_params
               | empty"""
    if p[2]:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []

def p_formal_param(p):
    """formal_param : type variable"""
    p[0] = (p[1],p[2])

def p_block(p):
    """block : '{' stmt_mult '}'"""
    p[0] = p[2]

def p_stmt_mult(p):
    """stmt_mult : stmt_mult stmt
                 | empty"""
    if p[2]:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []

def p_stmt(p):
    """stmt : if_stmt
            | while_stmt
            | for_stmt
            | return_stmt ';'
            | stmt_expr ';'
            | BREAK ';'
            | CONTINUE ';'
            | block
            | var_decl
            | ';'"""
    n = len(p)
    if n == 2:
        p[0] = p[1]
    elif n == 3:
        p[0] = (p[1],
                p[2])    

def p_if_stmt(p):
    """if_stmt : IF '(' expr ')' stmt
               | IF '(' expr ')' stmt ELSE stmt"""
    n = len(p)
    if n == 6:
        p[0] = (p[3],
                p[5])
    elif n == 8:
        p[0] = (p[3],
                p[5],
                p[7])
        
def p_while_stmt(p):
    """while_stmt : WHILE '(' expr ')' stmt"""
    p[0] = (p[3],p[4])

#def p_for_stmt(p):


