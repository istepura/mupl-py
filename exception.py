# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
# -*- coding: utf-8 -*-
from token import *

class ParserException(Exception):
    def __init__(self, coord):
        self.coord = coord

class InvalidSymbol(ParserException):
    def __init__(self, coord, value):
        ParserException.__init__(self, coord)
        self.parameter = value
    def __str__(self):
        return "Invalid symbol \"%s\" at line %d" % (self.parameter, self.coord[0])

class StringNotTerminated(ParserException):
    pass

class UnexpectedToken(ParserException):
    keywords = {
            Token.ADD: 'add',
            Token.INT : 'int',
            Token.EOF : 'EOF',
            Token.RB : ')',
            Token.VAR : 'var',
            Token.CALL : 'call',
            Token.MLET : 'mlet',
            Token.FUN : 'fun',
            Token.IFGRT : 'ifgreater',
            Token.APAIR : 'apair',
            Token.FST : 'fst',
            Token.SND : 'snd',
            Token.AUNIT : 'aunit',
            Token.ISAUNIT: 'isaunit',
            Token.LB: '(',
            Token.NUMBER : 'number',
            Token.SHARPF : '#f',
            Token.STRING : 'string'
        }
    def __init__(self, coord, expected, got):
        ParserException.__init__(self, coord)
        self.expected = expected
        self.got = got
    def __str__(self):
        return "Unexpected token \"%s\" at line %d. Expected \"%s\"" % (self.keywords[self.got], self.coord[0], self.keywords[self.expected])
