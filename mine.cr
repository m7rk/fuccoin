def evaluate(code : Array(String), input : Array(Int32))
  max_itrs = 64
  bracemap = buildbracemap(code)
  input.reverse!
  output = [] of Int32
  cells, codeptr, cellptr = [0], 0, 0

  while codeptr < code.size
    max_itrs -= 1
    if (max_itrs == 0)
      return [] of String
    end

    command = code[codeptr]

    if command == ">"
      cellptr += 1
      if cellptr == cells.size
        cells << 0
      end
    end

    if command == "<"
      if cellptr <= 0
        cellptr = 0 
      else
        cellptr -= 1
      end
    end

    if command == "+"
      if cells[cellptr] < 255
        cells[cellptr] = cells[cellptr] + 1 
      else
        cells[cellptr] = 0
      end
    end

    if command == "-"
      if cells[cellptr] > 0
        cells[cellptr] = cells[cellptr] - 1 
      else
        cells[cellptr] = 255
      end
    end

    if (command == "[" && cells[cellptr] == 0)
      codeptr = bracemap[codeptr]
    end

    if (command == "]" && cells[cellptr] != 0)
      codeptr = bracemap[codeptr]
    end

    if command == "."
      output << cells[cellptr]
    end

    if command == ","
      if (input.size > 0)
        cells[cellptr] = input.pop
      else
        return [] of String
      end
    end
    codeptr += 1
  end
  return output
end

def validBF(code : Array(String))
  cnt = 0
  # check if parens are matched.
  code.each do |v|
    cnt += 1 if v == "["
    cnt -= 1 if v == "]"
    return false if cnt < 0
  end
  return cnt == 0
end

def buildbracemap(code : Array(String))
  temp_bracestack, bracemap = [] of Int32, {} of Int32 => Int32
  code.each_with_index do |command, position|
    if command == "["
      temp_bracestack.push(position)
    end
    if command == "]"
      start = temp_bracestack.pop
      bracemap[start] = position
      bracemap[position] = start
    end
  end
  return bracemap
end

def test(prog : Array(String), constraints : Array(Array(Array(Int32))))
  constraints.each do |v|
    return false if v[1] != evaluate(prog, v[0].clone)
  end
  return true
end

def nex(symbhash : Hash(String,String) , curr : Array(String)) : Array(String)
  i = curr.size - 1
  while i != -1
    # curr was last in base 8 so we need to carry
    if curr[i] == "-"
      curr[i] = symbhash[curr[i]]
      i -= 1
    else
      curr[i] = symbhash[curr[i]]
      return curr
    end
  end
  curr << "."
  puts("searching programs of length " +  curr.size.to_s)
  return curr
end

def mine()
  # ur constraints here
  constraints = [
    [ [7], [0] ],
    [ [0], [3] ],
  ]

  # think of it base 8..
  symbhash = {"." => ",",
    "," => "[",
    "[" => "]",
    "]" => "<",
    "<" => ">",
    ">" => "+",
    "+" => "-",
    "-" => "."
  }

  curr = ["."]
  while true
    # flush console
    if validBF(curr) && test(curr, constraints)
      return curr.reduce(""){|a,b| a + b}
    else
      curr = nex(symbhash,curr)
    end
  end
end
print(mine())