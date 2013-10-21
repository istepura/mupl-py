# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
# -*- coding: utf-8 -*-
from token import *
from lexer import *
from node import *
from exception import *

class Parser(object):
    def __init__(self, lex):
        self.lx = lex

    def parse(self, string):
        self.lx.init(string)
        self.token = self.lx.get_token()
        res = self.__brexp()
        self.__match(Token.EOF)
        return res

    def __brexp(self):
        self.__match(Token.LB)
        node = self.__expr()
        self.__match(Token.RB)
        return node
    
    def __match(self,  tk):
        if self.token[0] == tk:
            val = tokenval(self.token)
            self.token = self.lx.get_token()
            return val
        else: 
       #     print "Token ", tk, " was not matched ", self.token
            raise UnexpectedToken(tokencoord(self.token), tk, self.token[0])

    def __funname(self):
        tk = self.token
        if tk[0] == Token.SHARPF:
            self.__match(tk[0])
        else:
            self.__match(Token.STRING)
        return tokenval(tk)

    def __expr(self):
        tk = self.token[0]
        if tk == Token.ADD:
            self.__match(Token.ADD)
            n1 = self.__brexp()
            n2 = self.__brexp()
            return Add(n1, n2)
        elif tk == Token.INT:
            self.__match(Token.INT)
            val = tokenval(self.token)
            self.__match(Token.NUMBER)
            return Int(val)
        elif tk == Token.IFGRT:
            self.__match(Token.IFGRT)
            n1 = self.__brexp()
            n2 = self.__brexp()
            n3 = self.__brexp()
            n4 = self.__brexp()
            return Ifgreater(n1, n2, n3, n4)
        elif tk == Token.MLET:
            self.__match(Token.MLET)
            val = tokenval(self.token)
            self.__match(Token.STRING)
            n1 = self.__brexp()
            n2 = self.__brexp()
            return Mlet(val, n1, n2)
        elif tk == Token.FUN:
            self.__match(Token.FUN)
            fname = self.__funname()

            argname = tokenval(self.token)
            self.__match(Token.STRING)
            n = self.__brexp()
            return Fun(fname, argname, n)
        elif tk == Token.VAR:
            self.__match(Token.VAR)
            name = self.__match(Token.STRING)
            return Var(name)
        elif tk == Token.CALL:
            self.__match(Token.CALL)
            n1 = self.__brexp()
            n2 = self.__brexp()
            return Call(n1, n2)
        elif tk == Token.APAIR:
            self.__match(Token.APAIR)
            n1 = self.__brexp()
            n2 = self.__brexp()
            return Apair(n1, n2)
        elif tk == Token.FST:
            self.__match(Token.FST)
            n = self.__brexp()
            return Fst(n)
        elif tk == Token.SND:
            self.__match(Token.SND)
            n = self.__brexp()
            return Snd(n)
        elif tk == Token.AUNIT:
            self.__match(Token.AUNIT)
            return Aunit()
        elif tk == Token.ISAUNIT:
            self.__match(Token.ISAUNIT)
            n = self.__brexp()
            return Isaunit(n)
        elif tk == Token.EOF:
            self.__match(Token.EOF)
        else:
            raise UnexpectedToken(tokencoord(self.token), tk, tk)
