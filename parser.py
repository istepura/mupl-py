# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
from token import *

class Parser(object):
    def parse(self, s):
        self.__brexp(0, s)

    def __brexp(self,i, s):
        i = self.__match(Token.LB, i, s)
        i = self.__expr(i, s)
        i = self.__match(Token.RB, i, s)
        return i
    
    def __match(self,  tk, i, s):
        if s[i][0] == tk:
            print "Matched ", tk, i
            i += 1
            return i
        else: 
            raise SyntaxError

    def __expr(self, i, s):
        tk = s[i][0]
        if tk == Token.ADD:
            i = self.__match(Token.ADD, i, s)
            i = self.__brexp(i, s)
            i = self.__brexp(i, s)
        elif tk == Token.INT:
            i = self.__match(Token.INT, i, s)
            i = self.__match(Token.NUMBER, i, s)
        elif tk == Token.EOF:
            i = self.__match(Token.EOF, i, s)
        else:
            raise SyntaxError
        return i