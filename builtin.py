from kinds import parse_kind
import kinds
import symbol
import literals
import syntax
import lex

def int2str(arg):
  return str(arg)

def str2int(arg):
  return int(arg)

def add(v1, v2):
  return v1 + v2;

def subtract(v1, v2):
  return v1 - v2

def ident(v1):
  return v1

def bi_print(arg):
  print ":", arg
  return 0

def cons(car, cdr):
  return literals.Cons(car, cdr)

def car(cons):
  return cons.car

def cdr(cons):
  return cons.cdr

def bi_get():
  print '<<< ',
  return raw_input()

def gt(lhs, rhs):
  return lhs > rhs
def gte(lhs, rhs):
  return lhs >= rhs
def lt(lhs, rhs):
  return lhs < rhs
def lte(lhs, rhs):
  return lhs < rhs
def eq(lhs, rhs):
  return lhs == rhs
def neq(lhs, rhs):
  return lhs != rhs

class bi(object):
  def __init__(self, f, kind):
    self.f = f
    self._kind = kind
  def kind(self):
    return self._kind
  def ret(self):
    return self.kind().ret()
  def resolve(self, kind):
    return self
  def parameterize(self, args):
    return self
  def call(self, args):
    args = [arg.evaluate() for arg in args]
    return self.f(*args)
  def __repr__(self): 
    return str(self._kind) + self.f.__name__
  def evaluate(self):
    return self
  def emitName(self):
    return self.f.__name__
  def emit(self):
    return ""
tmp = {
    '+': bi(add, parse_kind("[#:##]")),
    '-': bi(subtract, parse_kind("[#:##]")),
    '>': bi(gt, parse_kind("[#:##]")),
    '>=': bi(gte, parse_kind("[#:##]")),
    '<': bi(lt, parse_kind("[#:##]")),
    '>=': bi(lte, parse_kind("[#:##]")),
    '==': bi(eq, parse_kind("[#:##]")),
    '!=': bi(neq, parse_kind("[#:##]")),
    'print': bi(bi_print, parse_kind("[^:$]")),
    'gets': bi(bi_get, parse_kind("[$:]")),

    'int->str': bi(int2str, parse_kind("[$:#]")),
    'str->int': bi(str2int, parse_kind("[#:$]")),

    'cons' : bi(cons, parse_kind("[|{0}{1}|:{0}{1}]")),
    'car' : bi(car, parse_kind("[{5}:|{5}{6}|]")),
    'cdr' : bi(cdr, parse_kind("[{6}:|{5}{6}|]")),
    'id' : bi(ident, parse_kind("[{4}:{4}]")),

    'nil': literals.Nil(),
    '#f': literals.Integer(0),
    '#t': literals.Integer(1),
}

global_st = symbol.Table(None)

for k in tmp:
  syntax.define([lex.RawSymbol(k), tmp[k]])

del tmp



