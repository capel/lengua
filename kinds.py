def colors(s):
  try:
    return {
      '#': '\033[94m#\033[0m',
      '?': '\033[92m?\033[0m',
      '^': '\033[92m^\033[0m',
      '%': '\033[93m%\033[0m',
      '$': '\033[91m$\033[0m',
      ':': '\033[95m:\033[0m',
      '|': '\033[95m|\033[0m',
      '{': '\033[92m{\033[0m',
      '}': '\033[92m}\033[0m',
    }[str(s)]
  except KeyError:
    if isinstance(s, int):
      return '\033[93m{%d}\033[0m' % s
    return str(s)

def mangle(s):
  try:
    return {
      '#': "N",
      '?': "U",
      '^': "M",
      '%': "P",
      '$': "S",
      ':': "R",
      '|': "C",
      '[': "F",
      ']': "F",
      '{': "!!!!",
      '}': "!!!!",
    }[str(s)]
  except KeyError:
    return str(s)

def typename(s):
  try:
    return {
      '#': "int",
      '^': "int",
      '$': "char*",
    }[str(s)]
  except KeyError:
    return str(s)

def map_same(old, new):
  if old != new:
    raise TypeError("Attempt to map concrete type %r to type %r" % (old, new))

class Simple(object):
  def __init__(self, ret):
    self.ret = ret
  def map(self, mapping, kind):
    map_same(self, kind)
  def resolve(self, mapping):
    return self
  def kind(self):
    return self
  def __eq__(self, other):
    if other == None:
      return False
    return self.ret == other.kind().ret
  def __ne__(self, other):
    return not self == other
  def __repr__(self):
    return colors(self.ret)
  def mangle(self):
    return mangle(self.ret)
  def typename(self):
    return typename(self.ret)
  def __hash__(self):
    return hash(self.ret)

class Template(Simple):
  def __init__(self, template):
    self.template = template

  def kind(self):
    return self.template

  def resolve(self, mapping):
    if self.template in mapping:
      return mapping[self.template]
    else:
      return self

  def map(self, mapping, kind):
    mapping[self.template] = kind

  def __eq__(self, other):
    return type(other) == Template and self.template == other.template
  def __repr__(self):
    return colors('{') + str(self.template) + colors('}')
  def __hash__(self):
    return hash(self.template)

class Function(Simple):
  def __init__(self, ret, params):
    self._ret = ret
    self._params = params

  def kind(self):
    return self

  def ret(self):
    return self._ret
  def params(self):
    return self._params

  def __eq__(self, other):
    return  type(other) == Function and \
        self.ret() == other.ret() and self.params() == other.params()
  def __repr__(self):
    p = ''.join([colors(k) for k in self.params()])
    return '[' + str(self.ret()) + colors(":") + p +']'
  def mangle(self):
    p = ''.join([k.mangle() for k in self.params()])
    return mangle("[") + self.ret().mangle() + mangle(":") + p + mangle(']')
  def typename(self):
    p = ', '.join([k.typename() for k in self.params()])
    return "(*" + self.ret().typename()+ ")(" + p + ')'

  def __hash__(self):
    return hash(self.ret()) ^ hash(self.params())

  def resolve(self, mapping):
    self._ret = self.ret().resolve(mapping)
    self._params = [param.resolve(mapping) for param in self.params()]
    return self

class Call(Simple):
  def __init__(self, function, args):
    mapping = {}
    for arg, param in zip(args, function.kind().params()):
      param.map(mapping, arg)

    f = function.kind().resolve(mapping)
    self._ret = f.ret()
    self._args = args


  def __eq__(self, other):
    return self.kind() == other.kind()
  def __repr__(self):
    p = ''.join([colors(k) for k in self.args()])
    return '(' + str(self.kind()) + colors(":") + p +')'
    
  def kind(self):
    return self._ret.kind()
  def args(self):
    return self._args

class Cons(Simple):
  def __init__(self, car, cdr):
    self._car = car
    self._cdr = cdr
  def car(self):
    return self._car
  def cdr(self):
    return self._cdr

  def resolve(self, mapping):
    self._car = self.car().resolve(mapping)
    self._cdr = self.cdr().resolve(mapping)
    return self

  def __eq__(self, o):
    return type(o) == Cons and self.car() == o.car() and self.cdr() == o.cdr()
  def __hash__(self):
    return hash(self.car()) ^ hash(self.cdr())
  def __repr__(self):
    return colors('|') + ''.join((str(self.car()), str(self.cdr()))) + colors('|')

sigils = {
    '#': Simple,
    '$': Simple,
    '^': Simple,
}

def parse_kind(string):
  def lex(stream):
    token = stream.pop()
  
    if token in sigils:
      return sigils[token](token)

    if token == ':':
      return None
    
    if token == '{':
      tmp = []
      try:
        token = stream.pop()
        while token != '}':
          tmp.append(token)
          token = stream.pop()
        return Template(''.join(tmp))
      except IndexError:
        raise SyntaxError("Unmatched '{' at end of stream")

    if token == '|':
      try:
        c = Cons(lex(stream), lex(stream))
        end = stream.pop()
        if end != '|':
          raise SyntaxError("Unmatched '|'; expected '|', got " + end)
        return c
      except IndexError:
        raise SyntaxError("Unmatched '|' at end of stream")

    if token == '[':
      ret = lex(stream)
      c = stream.pop()
      if c != ':':
        raise SyntaxError("Malformed function. Expected :, got " + c)
      tmp = []
      try:
        while stream[-1] != ']':
          tmp.append(lex(stream))
        stream.pop()
        return Function(ret, tmp)
      except IndexError:
        raise SyntaxError("Unmatched '[' at end of stream")

  stream = list(reversed(string))
  return lex(stream)

STRING = parse_kind('$')
INT = parse_kind('#')
NIL = parse_kind('^')

