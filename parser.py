# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
from token import *
from lexer import *
from node import *

class Parser(object):
    def __init__(self, lex):
        self.lx = lex

    def parse(self, string):
        self.lx.init(string)
        self.token = self.lx.get_token()
        return self.__brexp()

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
            print "Token ", tk, " was not matched"
            raise SyntaxError

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
        elif tk == Token.AUNIT:
            self.__match(Token.AUNIT)
            return Aunit()
        elif tk == Token.EOF:
            self.__match(Token.EOF)
        else:
            print "unmatched token ", self.token
            raise SyntaxError
