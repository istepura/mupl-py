# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
# -*- coding: utf-8 -*-

class ParserException(Exception):
    def __init__(self, coord):
        self.coord = coord

class InvalidSymbol(ParserException):
    def __init__(self, coord, value):
        ParserException.__init__(self, coord)
        self.parameter = value
    def __str__(self):
        return repr("".join(['Invalid symbol at line : ', self.parameter]))

class StringNotTerminated(ParserException):
    pass

class UnexpectedToken(ParserException):
    def __init__(self, coord, expected, got):
        ParserException.__init__(self, coord)
        self.expected = expected
        self.got = got
