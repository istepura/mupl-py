# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
class BadToken(Exception):
    def __init__(self, line, value):
        self.parameter = value
        self.line = line
    def __str__(self):
        return repr("".join(["Bad token at line ", str(self.line), ': ', self.parameter]))
class Token:
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

    def __next(self):
        if self.idx < len(self.text):
            ch = self.text[self.idx]
            self.idx += 1
            return ch
        else:
            return -1

    def __scan_str(self):
        start = self.idx -1
        ch = self.__next()
        while ch != '"':
            if ch < 0:
                print "string not terminated"
                return
            else:
                ch = self.__next()
        return self.text[start:self.idx]

    def __skipws(self):
        ch = self.__next()
        while  ch > 0 and ch.isspace():
            if ch == '\n':
                self.line += 1
            ch = self.__next()
        return ch

    def __scan_num(self):
        start = self.idx - 1
        ch = self.__next()
        while ch.isdigit():
            ch = self.__next()
        return self.text[start:self.idx-1]

    def __scan_symbol(self):
        start = self.idx - 1
        ch = self.__next()
        while ch.isalpha():
            ch = self.__next()
        return self.text[start:self.idx-1]

    def __get_token(self):
        ch = self.__skipws()

        if ch> 0:
            if ch == '(':
                return (Token.LB, self.line, '')
            elif ch == ')':
                return (Token.RB, self.line, '')
            elif ch == '"':
                tk = Token.STRING
                pos = self.line
                val = self.__scan_str()
                if val:
                    return (tk, pos, val)
            elif ch.isdigit():
                tk = Token.NUMBER
                pos = self.line
                val = self.__scan_num()
                if val:
                    return (tk, pos, val)
            elif ch == '#':
                if self.__next() == 'f':
                    return (Token.SHARPF, self.line, '')
                else:
                    raise BadToken(self.line, '')
            elif ch.isalpha():
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
        tok = self.__get_token()
        while tok[0] != Token.EOF:
            res.append(tok)
            tok = self.__get_token()

        res.append(tok)
        return res

def main():
    l = Lexer()
    l.init("(add (int 3) (int 8))")
    print l.process()

    l.init('''(mlet "f1" (fun "f1" "a" (mlet "x" (var "a") (fun "f2" "z" (add (var "x") (int 1)))))
                               (mlet "f3" (fun "f3" "f" (mlet "x" (int 1729) (call (var "f") (aunit))))
                                     (call (var "f3") (call (var "f1") (int 1))))) ''')
    print l.process()

if __name__ == "__main__":
    main()
