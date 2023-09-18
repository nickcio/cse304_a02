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
    """class_decl : CLASS identifier class_body_decl_temp
                  | CLASS identifier '(' EXTENDS identifier ')' class_body_decl_temp
       class_body_decl_temp : class_body_decl_temp class_body_decl
                            | class_body_decl"""
    n = len(p)
    if n == 4:
        p[0] = (p[2], #id
                p[3]) #class body decl
    elif n == 8:
        p[0] = (p[2], #class id
                p[5], #ext id
                p[7]) #class body decl
        
def p_class_body_decl(p):
    """class_body_decl : field_decl
                       | method_decl
                       | constructor_decl"""
    p[0] = p[1]
    
    
