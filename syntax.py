import kinds
import symbol
import literals
import builtin
import lex

def req_args(num, args):
  if len(args) != num:
    raise TypeError(str(num) + " args expected:" + str(args))

class BoundFunction(object):
  def __init__(self, body, param_slots):
    self.body = body
    self.slots = param_slots
    self.name = "%r_" % symbol.get_id()
  def call(self, args):
    for arg, slot in zip(args, self.slots):
      slot.bind(arg.evaluate())
    return self.body.evaluate()
  def resolve(self, mapping):
    return self

  def kind(self):
    return kinds.Function(self.body.kind(), [slot.kind() for slot in self.slots])
    
  def evaluate(self):
    return self

  def __repr__(self):
    return "((%s) %r)" %  (' '.join([repr(s) for s in self.slots]), self.body)

  def emitName(self):
    return self.kind().mangle() + str(self.name)

  def emit(self):
    return "%s %s(%s) { return %s; }" % (self.kind().ret().typename(), self.emitName(), 
        ', '.join(["%s %s" % (a.kind().typename(), a.emit()) for a in self.slots]),
        self.body.emit())

  def parameterize(self, kinds):
    for slot, kind in zip(self.slots, kinds):
      literals.resolve_same(slot.kind(), kind.kind())
    return self

class Function(object):
  def __init__(self, params, body):
    self.st = symbol.Table(builtin.global_st)
    self.params = [self.st.addParameter(param) for param in params]
    
    self.body = replace(body, self.st)

  def parameterize(self, params):
    mapping = {}
    slots = []
    for param, kind in zip(self.params, params):
      slot = symbol.ParameterSlot(param, kind)
      slots.append(slot)
      mapping[param] = slot
    
    return BoundFunction(self.body.resolve(mapping), slots) 

  def kind(self):
    return kinds.Function(self.body.kind(), [p.kind() for p in self.params])

  def __repr__(self):
    return "*(%r(%s) %r)" % (self.body.kind(), 
                             ' '.join([repr(s) for s in self.params]),
                             self.body)
  def evaluate(self):
    return self

  def emit(self):
    return "FUNC_LITERAL"

def func(args):
  req_args(2, args)
  params = args[0]
  body = args[1]
  return Function(params, body)

# Not a class, since we want to return a lambda + expr eventually
def syntax_let(args):
  req_args(2, args)
  lets = args[0]
  body = args[1]

  syms = []
  bindings = []
  for let in lets:
    syms.append(let[0])
    bindings.append(replace(let[1]))

  return Expr([syntax_lambda((syms, body))] + bindings)

def define(args):
  req_args(2, args)

  raw_sym = args[0]
  expr = replace(args[1], builtin.global_st)

  builtin.global_st.define(raw_sym, expr.kind(), expr.evaluate())
  print expr.emit()

  return literals.Nil()

def syntax_if(args):
  req_args(3, args)
  
  cond = replace(args[0], builtin.global_st)
  a = replace(args[1], builtin.global_st)
  b = replace(args[2], builtin.global_st)
  return If(cond, a, b)

class If(object):
  def __init__(self, cond, a, b):
    literals.resolve_same(kinds.INT, cond)
    self.cond = cond
    self.a = a
    self.b = b
#    if args[1] != args[2]:
#      raise TypeError("Kinds of if branches are not the same: %r / %r" % (args[1], args[2]))
  def kind(self):
    return self.a.kind()
  def __repr__(self):
    return str(self.a.kind()) + "if"
  def emit(self):
    return "(%s) ? (%s) : (%s)" % (self.cond.emit(), self.a.emit(), self.b.emit())
  def evaluate(self):
    if self.cond.evaluate():
      return self.a.evaluate()
    else:
      return self.b.evaluate()

table = {
    'define': define,
    'func': func,
    'if': syntax_if,
}

def replace(token, st):
  if isinstance(token, list):
    if not token:
      raise SyntaxError("Empty () that is not in function literal")
    if lex.is_raw_sym(token[0]):
      head = token[0]
      if head.name() in table:
        return table[head.name()](token[1:])
    return literals.Call(replace(token[0], st), [replace(e, st) for e in token[1:]])
  elif lex.is_raw_sym(token):
    return st.lookup(token)
  else:
    return token
