# Nicholas Ciotoli 113325368 nciotoli
# Adam Lipson 114339915 alipson

import ply.yacc as yacc
from decaf_lexer import tokens

start = 'program'

def p_empty(p):
    'empty :'
    pass

def p_program(p):
    """
    program : program class_decl
            | empty
    """
    if p[2]:
        p[0] = p[1] + [p[2]] #program + class_decl
    else:
        p[0] = [] #empty

def p_class_decl(p):
    """
    class_decl : CLASS ID opt_extend LBRACK class_body_decl_mult RBRACK
    opt_extend : LPAREN EXTENDS ID RPAREN
               | empty
    """

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
            | ID"""
    p[0] = p[1]
    
def p_variables(p):
    """variables : variables COMMA variable
                 | variable"""
    if p[2]:
        p[0] = p[1] + [p[2]] #variables
    else:
        p[0] = [p[1]] #variable

def p_variable(p):
    """variable : ID"""
    p[0] = p[1]

def p_method_decl(p):
    """method_decl : modifier type_void ID formals block
                   | modifier type_void ID block
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
    """constructor_decl : modifier ID formals block
                        | modifier ID block"""
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
    """formals : formals COMMA formal_param
               | formal_param"""

def p_formal_param(p):
    """formal_param : type variable"""
    p[0] = (p[1],p[2])

def p_block(p):
    """block : LBRACK stmt_mult RBRACK"""
    p[0] = p[2]

def p_stmt_mult(p):
    """stmt_mult : stmt_mult stmt
                 | empty"""
    if p[2]:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []

def p_stmt(p):
    """
    stmt : IF LPAREN expr RPAREN stmt opt_else_stmt
         | WHILE LPAREN expr RPAREN stmt
         | FOR LPAREN opt_stmt_expr SEMICOLON opt_expr SEMICOLON opt_stmt_expr RPAREN stmt
         | RETURN opt_expr SEMICOLON
         | stmt_expr SEMICOLON
         | BREAK SEMICOLON
         | CONTINUE SEMICOLON
         | block
         | var_decl
         | SEMICOLON
    opt_else_stmt : ELSE stmt
                  | empty
    opt_expr : expr
             | empty
    opt_stmt_expr : stmt_expr
                  | empty
    """   

def p_literal(p):
    """
    literal : INT_CONST
            | FLOAT_CONST
            | STRING_CONST
            | NULL
            | TRUE
            | FALSE
    """
    p[0] = p[1]

def p_primary(p):
    """
    primary : literal
            | THIS
            | SUPER
            | LPAREN expr RPAREN
            | NEW ID LPAREN opt_args RPAREN
            | lhs
            | method_invocation
    opt_args : arguments
             | empty
    """    

def p_arguments(p):
    """
    arguments : arguments COMMA expr
              | expr
    """

def p_lhs(p):
    """
    lhs : field_access
    """

def p_field_access(p):
    """
    field_access : primary DOT ID
                 | ID
    """

def p_method_invocation(p):
    """
    method_invocation : field_access LPAREN opt_args_alt RPAREN
    opt_args_alt : arguments
                 | empty
    """

def p_expr(p):
    """
    expr : primary
         | assign
         | expr arith_op expr
         | expr bool_op expr
         | unary_op expr
    """

def p_assign(p):
    """
    assign : lhs EQUALS expr
           | lhs DOUBLE_PLUS
           | DOUBLE_PLUS lhs
           | lhs DOUBLE_MINUS
           | DOUBLE_MINUS lhs
    """

def p_arith_op(p):
    """
    arith_op : PLUS
             | MINUS
             | TIMES
             | DIVIDE
    """

def p_bool_op(p):
    """
    bool_op : AND
            | OR
            | DOUBLE_EQUALS
            | NOT_EQUAL
            | L_EQ
            | G_EQ
            | LESS
            | GREATER
    """

def p_unary_op(p):
    """
    unary_op : PLUS
             | MINUS
             | NOT
    """

def p_error(p):
    return

yacc.yacc()