# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

class Node(object):
    pass

class Add(Node):
    def __init__(self, n1, n2):
        self.n1 = n1
        self.n2 = n2
    def __repr__(self):
        return "Add(%r, %r)" % (self.n1, self.n2)
    def __str__(self):
        return "(add %s %s)" % (self.n1, self.n2)

class Int(Node):
    def __init__(self, n):
        self.n = n
    def __repr__(self):
        return "Int(%r)" % self.n
    def __str__(self):
        return "(int %s)" % str(self.n)

class Number(Node):
    def __init__(self, val):
        self.val = val
    def __repr__(self):
        return "Number(%d)" % self.val
    def __str__(self):
        return str(self.val)

class Mlet(Node):
    def __init__(self, name, n1, n2):
        self.name = name
        self.n1 = n1
        self.n2 = n2
    def __str__(self):
        return "(mlet '%s' %s %s)" % (self.name, self.n1, self.n2)

class Fun(Node):
    def __init__(self, name, argname, n):
        self.name = name
        self.argname = argname
        self.n = n

    def __str__(self):
        return "(fun '%s' '%s' %s)" % (self.name, self.argname, self.n)

class Var(Node):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return '(var "%s")' % self.name

class Call(Node):
    def __init__(self, n1 ,n2):
        self.n1 = n1
        self.n2 = n2

    def __str__(self):
        return '(call %s %s)' % (self.n1, self.n2)

class Aunit(Node):
    def __str__(self):
        return '(aunit)'

