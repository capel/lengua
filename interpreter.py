import sys
from pprint import pprint

import builtin
import lex
import parse
import syntax
import readline
import traceback

def repl():
  base_st = builtin.global_st
  while True:
    try:
      line = raw_input(">>> ")
      stream = parse.parse(line)
      stream.reverse()
      p = lex.lex(stream)
      p = p[0]
      print 'lex', p

      s = syntax.replace(p, base_st)
      print 'syntax', s

      res = s.evaluate()
      print res

      out = open("test.c", "w")


      out.write('#include "builtin.h"\n')
      out.write( "int main() {\n" )
      
      code = s.emit()
      out.write('\treturn ' + str(code) + ';\n}\n')
      out.close()
    except Exception, e:
      traceback.print_exc(file=sys.stdout)


def main():
  if len(sys.argv) < 2:
    repl()

main()
