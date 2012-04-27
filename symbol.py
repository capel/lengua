import kinds
import lex
import literals
import copy

_inf_val = 2
def get_id():
  global _inf_val
  _inf_val += 1
  return _inf_val

class Table(object):
  def __init__(self, parent):
    self.st = {}
    self.parent = parent
  def lookup(self, raw_sym):
    if not lex.is_raw_sym(raw_sym):
      raise TypeError("Attempt to lookup non-symbol " + str(raw_sym))
    name = raw_sym.name()
    try: 
      return self.st[name]
    except KeyError:
      if self.parent == None:
        raise KeyError("Symbol " + str(name) + " not found.")
      return self.parent.lookup(raw_sym)

  def define(self, raw_sym, kind, value):
    if not lex.is_raw_sym(raw_sym):
      raise TypeError("Attempt to define non-symbol " + str(raw_sym))
    name = raw_sym.name()
    if name in self.st:
      raise AttributeError("Cannot redefine symbol" + str(raw_sym))
    self.st[name] = Defined(name, kind, value)

  def addParameter(self, raw_sym):
    if not lex.is_raw_sym(raw_sym):
      raise TypeError("Attempt to add non-symbol param " + str(raw_sym))
    name = raw_sym.name()
    if name in self.st:
      raise AttributeError("Adding parameter symbol twice: " + name)
    else:
      p = Parameter(name)
      self.st[name] = p
      return p

class ParameterSlot(object):
  def __init__(self, param, kind):
    self.name = param.name
    self._kind = kind
  def bind(self, value):
    self.value = value
  def kind(self):
    return self._kind
  def __repr__(self):
    try:
      return "SLOT:" + str(self.value)
    except AttributeError:
      return "**" + self.name
  def evaluate(self):
    return self.value
  def emit(self):
    return self.name

class Parameter(object):
  def __init__(self, name):
    self.name = name
    self._kind = kinds.Template("_" + str(get_id()))
  def kind(self):
    return self._kind
  def resolve(self, mapping):
    if self in mapping:
      return mapping[self]
    else:
      return self
  def __repr__(self):
    return '*' + self.name
  def emit(self):
    return self.name

class Defined(object):
  def __init__(self, name, kind, value):
    self.name = name
    self.value = value
    self._kind = kind

  def kind(self):
    return copy.deepcopy(self._kind)
  def __repr__(self):
    return str(self.kind()) + self.name
  def evaluate(self):
    return self.value
  def resolve(self, mapping):
    return self
  def emit(self):
    return "*" + self.name
