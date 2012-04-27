import string

def parse(stream):
  l = []
  token = []
  in_token = False
  in_string = False

  for c in stream:
    if c is '(' or c is ')':
      if (in_string):
        token.append(c)
        continue
      if (in_token):
        l.append(''.join(token));
        in_token = False
      l.append(c)
    elif c in string.whitespace:
      if in_string:
        l.append(c)
      elif in_token:
        l.append(''.join(token))
        in_token = False
      else:
        continue
    elif c is '"':
      if in_string:
        token.append(c)
        l.append(''.join(token))
        in_string = False
      else:
        token = ['"']
        in_string = True
    else:
      if in_string or in_token:
        token.append(c);
      else:
        in_token = True
        token = [c]

  if in_token or in_string:
    l.append(''.join(token))
  return l

