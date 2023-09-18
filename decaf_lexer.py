import ply.lex as lex

reserved_words = ['BOOLEAN', 'BREAK', 'CONTINUE', 'CLASS', 'DO', 'ELSE',
                  'EXTENDS', 'FALSE', 'FOR', 'IF', 'INT',
                  'NEW', 'NULL', 'PRIVATE', 'PUBLIC', 'RETURN', 'STATIC',
                  'SUPER', 'THIS', 'TRUE', 'VOID', 'WHILE']
reserved_words = list(map(str.lower,reserved_words))

tokens = tuple([
    'COMMENT',
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
])

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_COMMENT(t):
    r'(\/\*(.|\n)+\*\/)|(\/\/.*)'

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
    r'[a-zA-Z][a-zA-Z_\d]*'
    if str(t.value) not in reserved_words:
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
  "HELLO\n GOODBYE"
  //G = E
  for
'''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)