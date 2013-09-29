# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

class LB(object):
    def __repr__(self):
        return "LB()"
class RB(object):
    def __repr__(self):
        return "RB()"

class Number(object):
    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return "Number(%d)" % self.val

class Add(object):
    def __repr__(self):
        return "Add()"

class Int(object):
    def __repr__(self):
        return "Int()"

class Var(object):
    def __repr__(self):
        return "Var()"

class Symbol(object):
    def __init__(self, val):
        self.val = val
    def __repr__(self):
        return "".join(["Symbol(", self.val, ")"])

class Lexer(object):
    keywords = {
            "add" : Add(),
            "var" : Var(),
            "int" : Int()
            }
    def process(self, text):
        '''Extracts lexemes from text'''
        res = []
        if not text:
            return res

        idx = 0
        while idx < len(text):
            if text[idx] == '(':
                res.append(LB())
            elif text[idx] == ')':
                res.append(RB())
            elif text[idx].isdigit():
                start = idx
                while text[idx].isdigit():
                    idx += 1
                idx -=1
                res.append(Number(int(text[start:idx+1])))
            elif text[idx].isalpha():
                start = idx
                while text[idx].isalpha():
                    idx += 1
                val = text[start:idx]
                idx -= 1

                if val in self.keywords:
                    res.append(self.keywords[val])
                else:
                    res.append(Symbol(val))

            else:
                pass
            idx += 1
        return res

def main():
    l = Lexer()
    print l.process("(add (int 3) (int 8))")
    print l.process('''(mlet "f1"
                               (fun "f1" "a" (mlet "x" (var "a") (fun "f2" "z" (add (var "x") (int 1)))))
                               (mlet "f3" (fun "f3" "f" (mlet "x" (int 1729) (call (var "f") (aunit)))) 
                                     (call (var "f3") (call (var "f1") (int 1))))))) ''')
    if __name__ == "__main__":
        main()

