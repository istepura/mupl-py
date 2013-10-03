# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
from token import *
from lexer import *

class Parser(object):
    def __init__(self, lex):
        self.lx = lex

    def parse(self, string):
        self.lx.init(string)
        self.token = self.lx.get_token()
        self.__brexp()

    def __brexp(self):
        self.__match(Token.LB)
        self.__expr()
        self.__match(Token.RB)
    
    def __match(self,  tk):
        if self.token[0] == tk:
            print "Matched ", self.token, 
            self.token = self.lx.get_token()
        else: 
            print "Token ", tk, " was not matched"
            raise SyntaxError

    def __expr(self):
        tk = self.token[0]
        if tk == Token.ADD:
            self.__match(Token.ADD)
            self.__brexp()
            self.__brexp()
        elif tk == Token.INT:
            self.__match(Token.INT)
            self.__match(Token.NUMBER)
        elif tk == Token.MLET:
            self.__match(Token.MLET)
            self.__match(Token.STRING)
            self.__brexp()
            self.__brexp()
        elif tk == Token.FUN:
            self.__match(Token.FUN)
            self.__match(Token.STRING)
            self.__match(Token.STRING)
            self.__brexp()
        elif tk == Token.VAR:
            self.__match(Token.VAR)
            self.__match(Token.STRING)
        elif tk == Token.CALL:
            self.__match(Token.CALL)
            self.__brexp()
            self.__brexp()
        elif tk == Token.AUNIT:
            self.__match(Token.AUNIT)
        elif tk == Token.EOF:
            self.__match(Token.EOF)
        else:
            print "unmatched token ", self.token
            raise SyntaxError
