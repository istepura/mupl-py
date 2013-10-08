# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
from token import *

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

    def __next(self):
        if self.idx < len(self.text):
            self.ch  = self.text[self.idx]
            self.idx += 1
        else:
            self.ch = -1

    def __scan_str(self):
        start = self.idx -2
        while self.ch != '"':
            if self.ch < 0:
                print "string not terminated"
                return
            else:
                self.__next()
        self.__next()
        return self.text[start:self.idx-1]


    def __skipws(self):
        while  self.ch > 0 and self.ch.isspace():
            if self.ch == '\n':
                self.line += 1
            self.__next()

    def __scan_num(self):
        start = self.idx - 1
        while self.ch.isdigit():
            self.__next()
        return self.text[start:self.idx-1]

    def __scan_symbol(self):
        start = self.idx - 1
        while self.ch.isalpha():
            self.__next()
        return self.text[start:self.idx-1]

    def get_token(self):
        self.__skipws()

        if self.ch> 0:
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
            elif self.ch.isdigit():
                tk = Token.NUMBER
                pos = self.line
                val = self.__scan_num()
                if val:
                    return (tk, pos, val)
            elif self.ch == '#':
                if self.__next() == 'f':
                    return (Token.SHARPF, self.line, '#f')
                else:
                    raise BadToken(self.line, '')
            elif self.ch.isalpha():
                val = self.__scan_symbol()

                if val and val in self.keywords:
                    return (self.keywords[val], self.line, '')
                else:
                    raise BadToken(self.line, val)
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
