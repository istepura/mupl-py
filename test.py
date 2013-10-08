import unittest
from lexer import *
from parser import *

class ParserTest(unittest.TestCase):
    def setUp(self):
        self._parser = Parser(Lexer())
    def parseToStr(self, string):
        ast = self._parser.parse(string)
        res = ast.eval({})
        return str(res)

class TestBasic(ParserTest):
    def testPositiveInt(self):
        res = self.parseToStr("(int 3)")
        self.assertEqual(res, '(int 3)')

    def testPositiveLongInt(self):
        s = "(int 12345678903)"
        res = self.parseToStr(s)
        self.assertEqual(res, s)

    def testNegativeInt(self):
        s = "(int -1)"
        res = self.parseToStr(s)
        self.assertEqual(res, s)

    def testLongNegativeInt(self):
        s = "(int -12345678903)"
        res = self.parseToStr(s)
        self.assertEqual(res, s)

    def testAunit(self):
        res = self.parseToStr("(aunit)")
        self.assertEqual(res, "(aunit)")

    def testBadInt(self):
        self.assertRaises(SyntaxError, self.parseToStr, "int 3")

    def testBadInt2(self):
        self.assertRaises(SyntaxError, self.parseToStr, '(int "3")')

class TestAdd(ParserTest):
    def test1(self):
        s ="(add (int 3) (int 8))"
        res = self.parseToStr(s)
        self.assertEqual(res, "(int 11)")

    def test2(self):
        s = "(add (int 300)    (int    -98)  )"
        res = self.parseToStr(s)
        self.assertEqual(res, "(int 202)")


class TestComplex(ParserTest):
    def test1(self):
        s = '''(mlet "f1" (fun "f1" "a" (mlet "x" (var "a") (fun "f2" "z" (add (var "x") (int 1)))))
                      (mlet "f3" (fun "f3" "f" (mlet "x" (int 1729) (call (var "f") (aunit))))
                                     (call (var "f3") (call (var "f1") (int 1))))) '''
        res = self.parseToStr(s)
        self.assertEqual(res, "(int 2)")
    def test2(self):
        s = '(call (fun "incr" "x" (add (var "x") (int 1))) (int 42)))'
        res = self.parseToStr(s)
        self.assertEqual(res, "(int 43)")

    def test3(self):
        s = '(ifgreater (add (int 0)(int 1)) (add (int 0)(int 2)) (int 3) (int 4))'
        res = self.parseToStr(s)
        self.assertEqual(res, "(int 4)")

    def test4(self):
        s = '(ifgreater (add (int 0)(int 2)) (add (int 1) (int 0)) (int 3) (int 4))'
        res = self.parseToStr(s)
        self.assertEqual(res, "(int 3)")

    def test4(self):
        s= '(mlet "fnc"       (fun "f1" "x"             (ifgreater (isaunit (var "x")) (int 0)                        (int 0)                        (add (fst (var "x")) (call (var "f1") (snd (var "x"))))))       (call (var "fnc") (apair (int 1) (apair (int 2) (apair (int 3) (aunit))))))' 
        res = self.parseToStr(s)
        self.assertEqual(res, "(int 6)")

if __name__ == "__main__":
    unittest.main()
