from kinds import parse_kind, NIL, INT, STRING
import kinds

def resolve_same(old, new):
  if old != new:
    raise TypeError("Attempt to resolve type %r to type %r" % (old, new))

class Nil(object):
  def __init__(self):
    pass
  def kind(self):
    return NIL
  def resolve(self, mapping):
    return self
  def __repr__(self):
    return str(NIL) + "nil"
  def evaluate(self):
    return self
  def emit(self):
    return "0"
  
class String(object):
  def __init__(self, s):
    self.val = s
  def kind(self):
    return STRING
  def resolve(self, mapping):
    return self
  def __repr__(self):
    return '"%s"' % self.val
  def evaluate(self):
    return self.val
  def emit(self):
    return '"%s"' % self.val

class Integer(object):
  def __init__(self, i):
    self.val = i
  def kind(self):
    return INT
  def resolve(self, mapping):
    return self
  def __repr__(self):
    return str(self.val)
  def evaluate(self):
    return self.val
  def emit(self):
    return str(self.val)

class Cons(object):
  def __init__(self, car, cdr):
    self.car = car
    self.cdr = cdr
  def kind(self):
    return Cons(self.car.kind(), self.cdr.kind())
  def resolve(self, mapping):
    return Cons(self.car().parameterize(mapping), self.cdr.parameterize(mapping))
  def __repr__(self):
    return "|%r %r|" % (self.car, self.cdr)
  def evaluate(self):
    return Cons(self.car.evaluate(), self.cdr.evaluate())

class Call(object):
  def __init__(self, func, args):
    self.function = func.evaluate().parameterize([a.kind() for a in args])
    self.args = args
    self._kind = self.function.kind().ret()
  def kind(self):
    return self._kind
  def resolve(self, mapping):
    return Call(self.function.resolve(mapping),
               [arg.resolve(mapping) for arg in self.args])
  def __repr__(self):
    body = ' '.join(str(a) for a in self.args)
    return "(%s %s)" % (str(self.function), body)
  def evaluate(self):
    return self.function.evaluate().call(self.args)
  def emit(self):
    return "%s(%s)" % (self.function.evaluate().emitName(), 
        ', '.join(a.emit() for a in self.args))

