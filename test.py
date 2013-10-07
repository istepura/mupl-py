from lexer import *
from parser import *

def main():
    l = Lexer()
    l.init("(add (int 3) (int 8))")

    s = l.process()

    print s
    lex = Lexer()
    sc = Parser(lex)

    ast = sc.parse("(add (int 3)    (int    8)  )")
    print ast

    s2 = '''(mlet "f1" (fun "f1" "a" (mlet "x" (var "a") (fun "f2" "z" (add (var "x") (int 1)))))
                               (mlet "f3" (fun "f3" "f" (mlet "x" (int 1729) (call (var "f") (aunit))))
                                     (call (var "f3") (call (var "f1") (int 1))))) '''
    print sc.parse(s2)
if __name__ == "__main__":
    main() 
