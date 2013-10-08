from lexer import *
from parser import *

def main():
    l = Lexer()
    l.init("(add (int 3) (int 8))")

    s = l.process()

    lex = Lexer()
    sc = Parser(lex)

    ast = sc.parse("(add (int 3)    (int    8)  )")
    print ast

    print ast.eval({})

    s2 = '''(mlet "f1" (fun "f1" "a" (mlet "x" (var "a") (fun "f2" "z" (add (var "x") (int 1)))))
                      (mlet "f3" (fun "f3" "f" (mlet "x" (int 1729) (call (var "f") (aunit))))
                                     (call (var "f3") (call (var "f1") (int 1))))) '''
    l.init(s2)

    ast = sc.parse(s2)
    print ast
    print ast.eval({})

    simplestr = '(call (fun "incr" "x" (add (var "x") (int 1))) (int 42)))'
    ast = sc.parse(simplestr)
    print ast.eval({})

    s = '(ifgreater (add (int 0)(int 1)) (add (int 0)(int 2)) (int 3) (int 4))'
    ast = sc.parse(s)
    print ast.eval({})

    s = '(ifgreater (add (int 0)(int 2)) (add (int 1) (int 0)) (int 3) (int 4))'
    ast = sc.parse(s)
    print ast.eval({})

    s= '(mlet "fnc"       (fun "f1" "x"             (ifgreater (isaunit (var "x")) (int 0)                        (int 0)                        (add (fst (var "x")) (call (var "f1") (snd (var "x"))))))       (call (var "fnc") (apair (int 1) (apair (int 2) (apair (int 3) (aunit))))))' 

    ast = sc.parse(s)
    print ast
    print ast.eval({})
if __name__ == "__main__":
    main() 
