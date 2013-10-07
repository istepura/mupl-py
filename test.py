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

    print ast.eval({})

    s2 = '''(mlet "f1" (fun "f1" "a" (mlet "x" (var "a") (fun "f2" "z" (add (var "x") (int 1)))))
                               (mlet "f3" (fun "f3" "f" (mlet "x" (int 1729) (call (var "f") (aunit))))
                                     (call (var "f3") (call (var "f1") (int 1))))) '''
    l.init(s2)
    print l.process()

    print sc.parse(s2)

    simplestr = '(call (fun "incr" "x" (add (var "x") (int 1))) (int 42)))'
    ast = sc.parse(simplestr)

    print ast.eval({})
if __name__ == "__main__":
    main() 
