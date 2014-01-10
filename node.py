# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
# -*- coding: utf-8 -*-
class ValError(Exception):
    def __init__(self, expected, actual):
        self.expected = expected
        self.actual = actual
    def __str__(self):
        return "Expected value of type %s, actual value is %s" % (self.expected, self.actual)
class UndefinedNameError(Exception):
    def __init__(self, val):
        self.val =val
    def __str__(self):
        return "Variable name %s is undefined in current environment" % self.val


class Node(object):
    def eval(self, env):
        pass

class Isaunit(Node):
    def __init__(self, n):
        self.n = n
    def __str__(self):
        return '(isaunit %s)' % self.n
    def eval(self, env):
        e = self.n.eval(env)
        if isinstance(e, Aunit):
            return Int(1)
        else:
            return Int(0)

class Closure(Node):
    """ internal class to faciliate functions calls"""
    def __init__(self, env, expr):
        self.env = env
        self.expr = expr
    def eval(self, env):
        return self

class Add(Node):
    def __init__(self, n1, n2):
        self.n1 = n1
        self.n2 = n2
    def __repr__(self):
        return "Add(%r, %r)" % (self.n1, self.n2)
    def __str__(self):
        return "(add %s %s)" % (self.n1, self.n2)
    def eval(self, env):
        e1 = self.n1.eval(env)
        e2 = self.n2.eval(env)
        if isinstance(e1, Int) and isinstance(e2, Int):
            return Int(int(e1.n) + int(e2.n))
        else:
            bad = e1 if type(e1) != Int else e2
            raise ValError('(int)', bad)

class Int(Node):
    def __init__(self, n):
        self.n = n
    def __repr__(self):
        return "Int(%r)" % self.n
    def __str__(self):
        return "(int %s)" % str(self.n)
    def eval(self, env):
        return self

class Mlet(Node):
    def __init__(self, name, n1, n2):
        self.name = name
        self.n1 = n1
        self.n2 = n2
    def __str__(self):
        return "(mlet '%s' %s %s)" % (self.name, self.n1, self.n2)
    def eval(self, env):
        newenv = env.copy()
        newenv[self.name] = self.n1.eval(env)
        return self.n2.eval(newenv)

class Fun(Node):
    def __init__(self, name, argname, n):
        self.name = name
        self.argname = argname
        self.n = n
    def __str__(self):
        return "(fun '%s' '%s' %s)" % (self.name, self.argname, self.n)
    def eval(self, env):
        return Closure(env, self)

class Var(Node):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return '(var "%s")' % self.name
    def eval(self, env):
        if self.name in env:
            return env[self.name]
        else:
            raise UndefinedNameError(self.name)

class Call(Node):
    def __init__(self, n1 ,n2):
        self.n1 = n1
        self.n2 = n2
    def __str__(self):
        return '(call %s %s)' % (self.n1, self.n2)
    def eval(self, env):
        func = self.n1.eval(env)
        arg = self.n2.eval(env)

        if isinstance(func, Closure):
            fn = func.expr
            newenv = func.env.copy()
            newenv[fn.name] = func
            newenv[fn.argname] = arg
            return fn.n.eval(newenv)
        else:
            raise ValError(Closure, func)

class Aunit(Node):
    def __str__(self):
        return '(aunit)'
    def eval(self, env):
        return self

class Ifgreater(Node):
    def __init__(self, n1, n2, n3, n4):
        self.n1 = n1
        self.n2 = n2
        self.n3 = n3
        self.n4 = n4
    def __str__(self):
        return 'ifgreater %s %s %s %s' % (self.n1, self.n2, self.n3, self.n4)
    def __repr__(self):
        return 'Ifgreater(%r, %r, %r, %r)' % (self.n1, self.n2, self.n3, self.n4)
    def eval(self, env):
        e1 = self.n1.eval(env)
        e2 = self.n2.eval(env)
        if isinstance(e1, Int) and isinstance(e2, Int):
            if int(e1.n) > int(e2.n):
                return self.n3.eval(env)
            else:
                return self.n4.eval(env)
        else:
            bad = e1 if type(e1) != Int else e2
            raise ValError(Int, bad)

class Apair(Node):
    def __init__(self, n1, n2):
        self.n1 = n1
        self.n2 = n2
    def __str__(self):
        return '(apair %s %s)' % (self.n1, self.n2)
    def eval(self, env):
        e1 = self.n1.eval(env)
        e2 = self.n2.eval(env)
        return Apair(e1, e2)

class Fst(Node):
    def __init__(self, n):
        self.n = n
    def __str__(self):
        return '(fst %s)' % self.n
    def eval(self, env):
        e1 = self.n.eval(env)
        if isinstance(e1, Apair):
            return e1.n1
        else:
            raise ValError(Apair, e1)

class Snd(Node):
    def __init__(self, n):
        self.n = n
    def __str__(self):
        return '(snd %s)' % self.n
    def eval(self, env):
        e = self.n.eval(env)
        if isinstance(e, Apair):
            return e.n2
        else:
            raise ValError(Apair, e)


