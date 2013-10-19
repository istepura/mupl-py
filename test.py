#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
    def assertEq(self, s1, s2):
        res = self.parseToStr(s1)
        self.assertEqual(res, s2)
    def asserEx(self, ex, s):
        self.assertRaises(ex, self.parseToStr, s)

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
        self.assertRaises(UnexpectedToken, self.parseToStr, "int 3")

    def testBadInt2(self):
        self.assertRaises(UnexpectedToken, self.parseToStr, '(int "3")')

class TestAdd(ParserTest):
    def test1(self):
        s ="(add (int 3) (int 8))"
        res = self.parseToStr(s)
        self.assertEqual(res, "(int 11)")

    def test2(self):
        s = "(add (int 300)    (int    -98)  )"
        res = self.parseToStr(s)
        self.assertEqual(res, "(int 202)")

    def test3(self):
        self.assertEq("(add (add (int 1) (int 2)) (add (int 3) (int 4)))", "(int 10)")

    def test4(self):
        self.assertRaises(ValError, self.parseToStr, "(add (int 3) (aunit))")


class TestIfgreater(ParserTest):
    def test4(self):
        s = '(ifgreater (add (int 0)(int 2)) (add (int 1) (int 0)) (int 3) (int 4))'
        res = self.parseToStr(s)
        self.assertEqual(res, "(int 3)")
    def test1(self):
        self.assertEq("(ifgreater (add (int 0)(int 1)) (add (int 0)(int 2)) (int 3) (int 4))", "(int 4)")
    def test2(self):
        self.assertRaises(ValError, self.parseToStr, '(ifgreater (aunit) (int 2) (int 3) (int 4))')

class TesApair(ParserTest):
    def test1(self):
        s = '(apair (fst (apair (int 1) (int 2)))                 (snd (apair (int 3) (int 4))) )'
        res = self.parseToStr(s)
        self.assertEqual(res, "(apair (int 1) (int 4))")

    def test2(self):
        self.assertEq('(mlet "x" (int 1) (apair (var "x") (var "x")))', '(apair (int 1) (int 1))')

    def test3(self):
        self.assertEq('(fst (apair (int 1) (int 2)))', '(int 1)')

    def test4(self):
        self.assertEq('(mlet "x" (apair (int 1) (int 2)) (fst (var "x")))', '(int 1)')
    
    def test5(self):
        self.assertRaises(ValError, self.parseToStr, '(fst (add (int 1) (int 2)))')
        self.assertRaises(ValError, self.parseToStr, '(snd (add (int 1) (int 2)))')

    def test6(self):
        self.assertEq('(snd (apair (int 1) (int 2)))', '(int 2)')

    def test7(self):
        self.assertEq('(mlet "x" (apair (int 1) (int 2)) (snd (var "x")))', '(int 2)')


class TestIsaunit(ParserTest):
    def test1(self):
        self.assertEq('(isaunit (aunit))', '(int 1)')
    def tes2(self):
        self.assertEq('(mlet "x" (aunit) (isaunit (var "x")))', '(int 0)')
    def test3(self):
        self.assertEq('(isaunit (int 34))', '(int 0)')
    def test4(self):
        self.assertEq('(mlet "x" (int 0) (isaunit (var "x")))', '(int 0)')

class TestVarMlet(ParserTest):
    def test1(self):
        self.assertEq('(mlet "x" (add (int 1) (int 1)) (var "x"))', '(int 2)')
    def test2(self):
        self.assertEq('(mlet "x" (int 1) (var "x"))', '(int 1)')
    def test3(self):
        self.asserEx(UndefinedNameError, '(var "x")')

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

    def test4(self):
        s= '(mlet "fnc"       (fun "f1" "x"             (ifgreater (isaunit (var "x")) (int 0)                        (int 0)                        (add (fst (var "x")) (call (var "f1") (snd (var "x"))))))       (call (var "fnc") (apair (int 1) (apair (int 2) (apair (int 3) (aunit))))))'
        res = self.parseToStr(s)
        self.assertEqual(res, "(int 6)")

    def test5(self):
        self.assertEq('(mlet "double" (fun "double" "x" (add (var "x") (var "x")))                                  (call (var "double") (int 10)))', '(int 20)')

    def test6(self):
        self.assertEq(u'(mlet "range"           (fun "range" "lo"                (fun #f "hi"                     (ifgreater (var "lo") (var "hi") (aunit)                                (apair (var "lo") (call (call (var "range") (add (int 1) (var "lo"))) (var "hi"))))))           (call (call (var "range") (int 5)) (int 8)))', '(apair (int 5) (apair (int 6) (apair (int 7) (apair (int 8) (aunit)))))')
    
    def test7(self):
        self.asserEx(ValError, '(call (int 1) (int 2))')

if __name__ == "__main__":
    unittest.main()
