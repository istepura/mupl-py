# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
class BadToken(Exception):
    def __init__(self, line, value):
        self.parameter = value
        self.line = line
    def __str__(self):
        return repr("".join(["Bad token at line ", str(self.line), ': ', self.parameter]))

class Token(object):
    LB = 0
    RB = 1
    NUMBER = 2
    STRING = 3
    INT = 4
    ADD = 5
    VAR = 6
    FUN = 7
    SHARPF = 8
    IFGRT = 9
    CALL = 10
    MLET = 11
    APAIR = 12
    FST = 13
    SND = 14
    AUNIT = 15
    ISAUNIT = 16
    EOF = 666
 