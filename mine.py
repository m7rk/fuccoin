import sys

def evaluate(code, input, max_itrs=64):
  bracemap = buildbracemap(code)
  input.reverse()
  output = []

  cells, codeptr, cellptr = [0], 0, 0

  while codeptr < len(code):
    max_itrs -= 1
    if(max_itrs == 0):
        return []
    
    command = code[codeptr]

    if command == ">":
      cellptr += 1
      if cellptr == len(cells): cells.append(0)

    if command == "<":
      cellptr = 0 if cellptr <= 0 else cellptr - 1

    if command == "+":
      cells[cellptr] = cells[cellptr] + 1 if cells[cellptr] < 255 else 0

    if command == "-":
      cells[cellptr] = cells[cellptr] - 1 if cells[cellptr] > 0 else 255

    if command == "[" and cells[cellptr] == 0: codeptr = bracemap[codeptr]
    if command == "]" and cells[cellptr] != 0: codeptr = bracemap[codeptr]
    if command == ".": output.append(cells[cellptr])
    if command == ",": 
      if len(input) > 0:
        cells[cellptr] = input.pop()
      else:
        return []
      
    codeptr += 1
  return output

def buildbracemap(code):
  temp_bracestack, bracemap = [], {}

  for position, command in enumerate(code):
    if command == "[": temp_bracestack.append(position)
    if command == "]":
      start = temp_bracestack.pop()
      bracemap[start] = position
      bracemap[position] = start
  return bracemap

def validBF(code):
  cnt = 0
  # check if parens are matched.
  for v in code:
    if v == '[':
        cnt += 1 
    if v == ']':
        cnt -= 1 
    if cnt < 0:
        return False
  return cnt == 0


def test(prog, constraints):
  for v in constraints:
    if v[1] != evaluate(prog, v[0].copy()):
      return False
  return True

def next(symbhash,curr):
  i = len(curr) - 1
  while i != -1:
    # curr was last in base 8 so we need to carry
    if curr[i] == '-':
      curr[i] = symbhash[curr[i]]
      i -= 1
    else:
      curr[i] = symbhash[curr[i]]
      return curr
    # full carry
  curr.append('.')
  print("searching programs of length " + str(len(curr)))
  sys.stdout.flush()
  return curr

def mine():
  # ur constraints here
  constraints = [
    [ [5,1], [1] ],
    [ [1,6], [7] ],
    [ [1,1], [6] ],
  ]

  # think of it base 8..
  symbhash = {'.' : ',',
    ',' : '[',
    '[' : ']',
    ']' : '<',
    '<' : '>',
    '>' : '+',
    '+' : '-',
    '-' : '.'
  }

  curr = ["."]
  while True:
    # flush console
    if(validBF(curr) and test(curr, constraints)):
      return "".join(curr)
    else:
      curr = next(symbhash,curr)

print(mine())