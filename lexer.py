# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
# -*- coding: utf-8 -*-
from token import *

class InvalidSymbol(Exception):
    def __init__(self, line, value):
        self.parameter = value
        self.line = line
    def __str__(self):
        return repr("".join(["Invalid symbol at line ", str(self.line), ': ', self.parameter]))

class StringNotTerminated(Exception):
    pass

class Lexer(object):
    keywords = {
            'add' : Token.ADD,
            "var" : Token.VAR,
            "int" : Token.INT,
            "call" : Token.CALL,
            "mlet" : Token.MLET,
            "fun" : Token.FUN,
            "ifgreater" : Token.IFGRT,
            "apair" : Token.APAIR,
            "fst" : Token.FST,
            "snd" : Token.SND,
            "aunit" :Token.AUNIT,
            "isaunit" : Token.ISAUNIT
        }
    def init(self, text):
        self.text = text
        self.idx, self.line = 0, 1
        self.__next()
        self.eof = False

    def __next(self):
        if self.idx < len(self.text):
            self.ch  = self.text[self.idx]
            self.idx += 1
        else:
            self.eof = True

    def __scan_str(self):
        start = self.idx -2
        while self.ch != '"':
            if self.eof:
                raise StringNotTerminated
            else:
                self.__next()
        self.__next()
        return self.text[start:self.idx-1]


    def __skipws(self):
        while  not self.eof and self.ch.isspace():
            if self.ch == '\n':
                self.line += 1
            self.__next()

    def __scan_num(self):
        start = self.idx - 1
        while not self.eof and self.ch.isdigit():
            self.__next()
        return self.text[start:self.idx-1]

    def __scan_symbol(self):
        start = self.idx - 1
        while not self.eof and self.ch.isalpha():
            self.__next()
        return self.text[start:self.idx-1]

    def get_token(self):
        self.__skipws()

        if not self.eof:
            if self.ch == '(':
                self.__next()
                return (Token.LB, self.line, '')
            elif self.ch == ')':
                self.__next()
                return (Token.RB, self.line, '')
            elif self.ch == '"':
                self.__next()
                val = self.__scan_str()
                tk = Token.STRING
                pos = self.line
                if val:
                    return (tk, pos, val)
            elif self.ch == '-':
                val = None
                self.__next()
                if self.ch.isdigit():
                    tk = Token.NUMBER
                    pos = self.line
                    val = self.__scan_num()
                if val:
                    return (tk, pos, '-'+val)
                else:
                    raise InvalidSymbol(self.line, '-')
            elif self.ch.isdigit():
                tk = Token.NUMBER
                pos = self.line
                val = self.__scan_num()
                if val:
                    return (tk, pos, val)
            elif self.ch == '#':
                self.__next()
                if self.ch == 'f':
                    self.__next()
                    return (Token.SHARPF, self.line, '#f')
                else:
                    raise InvalidSymbol(self.line, self.ch)
            elif self.ch.isalpha():
                val = self.__scan_symbol()

                if val and val in self.keywords:
                    return (self.keywords[val], self.line, '')
                else:
                    raise InvalidSymbol(self.line, val)
        else :
            return (Token.EOF, self.line, '')

    def process(self):
        '''Extracts lexemes from text'''
        res = []
        tok = self.get_token()
        while tok[0] != Token.EOF:
            res.append(tok)
            tok = self.get_token()

        res.append(tok)
        return res 

def tokenval(token):
    return token[2]
