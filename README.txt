Nicholas Ciotoli 113325368 nciotoli
Adam Lipson 114339915 alipson

decaf_lexer.py is a PLY/lex scanner specification file.
decaf_parser.py is a PLY/yacc scanner specification file.
decaf_checker.py contains the main python function to put together the lexer and parser, take the input from Decaf program files, and perform syntax checking.
decaf_ast.py contains table and class definitions for Decaf's AST
decaf_ast.py contains definitions for evaluating the type constraints and for name resolution