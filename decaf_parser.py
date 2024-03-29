# Nicholas Ciotoli 113325368 nciotoli
# Adam Lipson 114339915 alipson

import ply.yacc as yacc
from decaf_lexer import *

start = 'program'

precedence = (
    ('left','EQUALS'), #lowest
    ('left','OR'),
    ('left','AND'),
    ('left','DOUBLE_EQUALS','NOT_EQUAL'),
    ('nonassoc','LESS','GREATER','L_EQ','G_EQ'),
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('right','NOT'), #highest
)

def p_empty(p):
    'empty :'
    pass

def p_program(p):
    """
    program : program class_decl
            | empty
    """

def p_class_decl(p):
    """
    class_decl : CLASS ID opt_extend LBRACK class_body_decl_mult RBRACK
    opt_extend : EXTENDS ID
               | empty
    """

def p_class_body_decl_mult(p):
    """
    class_body_decl_mult : class_body_decl_mult class_body_decl
                         | class_body_decl
    """

def p_class_body_decl(p):
    """
    class_body_decl : field_decl
                    | method_decl
                    | constructor_decl
    """
    
def p_field_decl(p):
    """
    field_decl : modifier var_decl
    """

def p_modifier(p):
    """
    modifier : visibility opt_static
    visibility : PUBLIC
               | PRIVATE
               | empty
    opt_static : STATIC
               | empty
    """
    
def p_var_decl(p):
    """
    var_decl : type variables SEMICOLON
    """

def p_type(p):
    """
    type : INT
         | FLOAT
         | BOOLEAN
         | ID
    """
    
def p_variables(p):
    """
    variables : variables COMMA variable
              | variable
    """

def p_variable(p):
    """
    variable : ID
    """

def p_method_decl(p):
    """
    method_decl : modifier type ID LPAREN opt_formals RPAREN block
                | modifier VOID ID LPAREN opt_formals RPAREN block
    opt_formals : formals
                | empty
    """

def p_constructor_decl(p):
    """
    constructor_decl : modifier ID LPAREN opt_formals_alt RPAREN block
    opt_formals_alt : formals
                    | empty
    """
        
def p_formals(p):
    """
    formals : formals COMMA formal_param
            | formal_param
    """

def p_formal_param(p):
    """
    formal_param : type variable
    """

def p_block(p):
    """
    block : LBRACK stmt_mult RBRACK
    """

def p_stmt_mult(p):
    """
    stmt_mult : stmt_mult stmt
              | empty
    """

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

def p_stmt_expr(p):
    """
    stmt_expr : assign
              | method_invocation
    """

def p_error(p):
    if p:
        line_start = p.lexer.lexdata.rfind('\n', 0, p.lexpos) + 1
        column = (p.lexpos - line_start)
        print(f'Parsing Error: Unexpected Token \'{p.value}\' of type \'{p.type}\' at line number {p.lexer.lineno} and column {column}')
    else: 
        print(f'Unexpected Parsing Error')
    exit()

parser = yacc.yacc()

