# Nicholas Ciotoli 113325368 nciotoli
# Adam Lipson 114339915 alipson

import ply.lex as lex

reserved_words_upper = ['BOOLEAN', 'BREAK', 'CONTINUE', 'CLASS', 'DO', 'ELSE',
                  'EXTENDS', 'FALSE', 'FLOAT', 'FOR', 'IF', 'INT',
                  'NEW', 'NULL', 'PRIVATE', 'PUBLIC', 'RETURN', 'STATIC',
                  'SUPER', 'THIS', 'TRUE', 'VOID', 'WHILE']
reserved_words = {}
for word in reserved_words_upper:
    reserved_words[word.lower()] = word



tokens = tuple([
    'INT_CONST',
    'FLOAT_CONST',
    'STRING_CONST',
    'ID',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'DOUBLE_PLUS',
    'DOUBLE_MINUS',
    'AND',
    'OR',
    'DOUBLE_EQUALS',
    'NOT_EQUAL',
    'L_EQ',
    'G_EQ',
    'LBRACK',
    'RBRACK',
    'SEMICOLON',
    'DOT',
    'COMMA',
    'EQUALS',
    'LESS',
    'GREATER',
    'NOT'
] + reserved_words_upper)

t_DOUBLE_PLUS = r'\+\+'
t_DOUBLE_MINUS = r'--'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_AND = r'&&'
t_OR = r'\|\|'
t_DOUBLE_EQUALS = r'=='
t_NOT_EQUAL = r'!='
t_L_EQ = r'<='
t_G_EQ = r'>='
t_LBRACK = r'{'
t_RBRACK = r'}'
t_SEMICOLON = r';'
t_DOT = r'\.'
t_COMMA = r','
t_EQUALS = r'='
t_LESS = r'<'
t_GREATER = r'>'
t_NOT = r'!'

def t_COMMENT(t):
    r'(/[*][^*]*[*]+([^/*][^*]*[*]+)*/)|(//[^\n]*)'
    linecount = t.value.count('\n')
    if linecount: t.lexer.lineno += linecount
    pass

def t_FLOAT_CONST(t):
    r'(\d+.\d+([eE][+-]?\d+)?)|(\d+[eE][+-]?\d+)'
    t.value = float(t.value)
    return t

def t_INT_CONST(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING_CONST(t):
    r'"[^"]*"'
    #t.value = str(t.value[1:-1])
    t.value = str(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    if t.value in reserved_words.keys():
        t.type = reserved_words[t.value]
    else:
        t.type = 'ID'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += 1

t_ignore  = ' \t'

def t_error(t):
    print(f'Scanning Error: Illegal character {t.value[0]} at line number {t.lexer.lineno}')
    t.lexer.skip(1)

lexer = lex.lex()
