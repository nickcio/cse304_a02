# Nicholas Ciotoli 113325368 nciotoli
# Adam Lipson 114339915 alipson

import ply.lex as lex
TERMINAL_RED_PRINT = '\033[91m'
TERMINAL_CLEAR_PRINT = '\033[0m'

reserved = {
    'boolean': 'BOOLEAN',
    'break': 'BREAK',
    'extends': 'EXTENDS',
    'new': 'NEW',
    'null': 'NULL',
    'super': 'SUPER',
    'this': 'THIS',
    'continue': 'CONTINUE',
    'class': 'CLASS',
    'float': 'FLOAT',
    'for': 'FOR',
    'private': 'PRIVATE',
    'public': 'PUBLIC',
    'void': 'VOID',
    'while': 'WHILE',
    'do': 'DO',
    'else': 'ELSE',
    'if': 'IF',
    'int': 'INT',
    'return': 'RETURN',
    'static': 'STATIC',
    'string': 'STRING'
}

tokens = [
    'DOT',
    'COMMA',
    'INTEGER',
    'PLUS',
    'PLUSPLUS',
    'MINUS',
    'MINUSMINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'LCURLY',
    'RBRACKET',
    'LBRACKET',
    'RCURLY',
    'EQUAL',
    'NOTEQUAL',
    'GREATER',
    'LESS',
    'GREATEREQ',
    'LESSEQ',
    'OR',
    'AND',
    'NOT',
    'TRUE',
    'FALSE',  
    'SETEQUAL',
    'SEMICOLON',
    'STRING_LITERAL',
    'ERROR',  
    'ID'
] + list(reserved.values())

t_COMMA = r'\,'
t_DOT = r'\.'
t_AND = r'\&\&'
t_BOOLEAN = r'boolean'
t_BREAK = r'break'
t_CLASS = r'class'
t_CONTINUE = r'continue'
t_DIVIDE = r'/'
t_DO = r'do'
t_ELSE = r'else'
t_EQUAL = r'\=\='
t_EXTENDS = r'extends'
t_FOR = r'for'
t_GREATER = r'\>'
t_GREATEREQ = r'\>\='
t_IF = r'if'
t_INT = r'int'
t_LBRACKET = r'\['
t_LCURLY = r'\{'
t_LESS = r'\<'
t_LESSEQ = r'\<\='
t_LPAREN = r'\('
t_MINUSMINUS = r'\-\-'
t_MINUS = r'-'
t_NEW = r'new'
t_NOT = r'\!'
t_NOTEQUAL = r'\!\='
t_NULL = r'null'
t_OR = r'\|\|'
t_PLUSPLUS = r'\+\+'
t_PLUS = r'\+'
t_PRIVATE = r'private'
t_PUBLIC = r'public'
t_RBRACKET = r'\]'
t_RCURLY = r'\}'
t_RETURN = r'return'
t_RPAREN = r'\)'
t_SEMICOLON = r'\;'
t_SETEQUAL = r'\='
t_STATIC = r'static'
t_STRING= r'string'
t_SUPER = r'super'
t_THIS = r'this'
t_TIMES = r'\*'
t_VOID = r'void'
t_WHILE = r'while'

t_ignore = ' \t'

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING_LITERAL(t):
    r'"[^"]*"'
    t.value = t.value[1:-1] 
    return t

def t_TRUE(t):
    r'true'
    t.value = True
    return t

def t_FALSE(t):
    r'false'
    t.value = False
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value in reserved:
        t.type = reserved[t.value]  
    else:
        t.type = 'ID'  
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    t.lexer.lexpos += len(t.value)    

def t_COMMENT(t):
    r'(/\*(.|\n)*?\*/)|(//.*)'
    t.lexer.lineno += t.value.count('\n')