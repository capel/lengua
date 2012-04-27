import string
import literals
import kinds

class RawSymbol(object):
  def __init__(self, name):
    self._name = name
  def name(self):
    return self._name
  def __repr__(self):
    return self.name()

def is_raw_sym(sym):
  return isinstance(sym, RawSymbol)

def lex(stream):
  l = []
  while len(stream) > 0:
    token = stream.pop()
    if token == '(':
      l.append(lex(stream))
    elif token == ')':
      return l
    else:
      if token.startswith('"') and token.endswith('"'):
        l.append(literals.String(token[1:-1]))
      elif token[0] in string.digits:
        for c in token:
          if c not in string.digits:
            raise SyntaxError("Bad numeric literal" + token)
        l.append(literals.Integer(int(token)))
      else:
        l.append(RawSymbol(token))
  return l

