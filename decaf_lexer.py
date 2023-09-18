import ply.lex as lex

reserved_words = ['BOOLEAN', 'BREAK', 'CONTINUE', 'CLASS', 'DO', 'ELSE',
                  'EXTENDS', 'FALSE', 'FOR', 'IF', 'INT',
                  'NEW', 'NULL', 'PRIVATE', 'PUBLIC', 'RETURN', 'STATIC',
                  'SUPER', 'THIS', 'TRUE', 'VOID', 'WHILE']
#rsv = list(map(lambda x:x.replace('-','_'),reserved_words))

tokens = tuple([
    'INTEGER',
    'FLOAT',
    'STRING',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
] + reserved_words)

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_FLOAT(t):
    r'(\d+.\d+([eE][+-]?\d+)?)|(\d+[eE][+-]?\d+)'
    t.value = float(t.value)
    return t

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'"[^"]*"'
    t.value = str(t.value[1:-1])
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += 1

t_ignore  = ' \t'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

# Test it out
data = '''
3 + 4.1e-10 * 10
  + -20 *2
  "HELLO\nGOODBYE"
'''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)