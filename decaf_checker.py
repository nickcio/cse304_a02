# Nicholas Ciotoli 113325368 nciotoli
# Adam Lipson 114339915 alipson

import sys
import ply.lex as lex
import ply.yacc as yacc

import decaf_ast
import decaf_lexer
import decaf_parser


def just_scan(fn=""):
    fn = sys.argv[1] if len(sys.argv) > 1 else ""
    if fn == "":
        print("Missing file name for source program.")
        print("USAGE: python3 decaf_checker.py <decaf_source_file_name>")
        sys.exit()
    import decaf_lexer
    lexer = lex.lex(module = decaf_lexer)#, debug = 1)

    fh = open(fn, 'r')
    source = fh.read()
    lexer.input(source)
    next_token = lexer.token()
    while next_token != None:
        print(next_token)
        next_token = lexer.token()
# end def just_scan()

def just_parse(fn=""):
    print("Parsing...")
    if fn == "":
        print("Missing file name for source program.")
        print("USAGE: python3 decaf_checker.py <decaf_source_file_name>")
        sys.exit()
    lexer = lex.lex(module = decaf_lexer, debug = 0 )
    parser = yacc.yacc(module = decaf_parser, debug = 0)

    fh = open(fn, 'r')
    source = fh.read()
    fh.close()
    result = parser.parse(source, lexer = lexer, debug = 0)
    print(result)
    ast = decaf_ast.writeAST(result)
    # Parsing Successful
    print(ast)

def main():
    fn = sys.argv[1] if len(sys.argv) > 1 else ""
    just_scan(fn) # lexer
    fn = sys.argv[1] if len(sys.argv) > 1 else ""
    just_parse(fn) # parser

if __name__ == "__main__":
    main()
