import json
import boto3
import random

def evaluate(code, input):
  code     = cleanup(list(code))
  bracemap = buildbracemap(code)
  input.reverse()
  output = []

  cells, codeptr, cellptr = [0], 0, 0

  while codeptr < len(code):
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
    if command == ",": cells[cellptr] = input.pop()
      
    codeptr += 1
  return output

def cleanup(code):
  return ''.join(filter(lambda x: x in ['.', ',', '[', ']', '<', '>', '+', '-'], code))

def buildbracemap(code):
  temp_bracestack, bracemap = [], {}

  for position, command in enumerate(code):
    if command == "[": temp_bracestack.append(position)
    if command == "]":
      start = temp_bracestack.pop()
      bracemap[start] = position
      bracemap[position] = start
  return bracemap

def makechallenge():
  chall = []
  for i in range(random.randint(2,3)):
    c = [[random.randint(0,8)],[random.randint(0,8)]]
    if(random.randint(0,1) == 0):
      c[0].append(random.randint(0,8))
    else:
      c[1].append(random.randint(0,8))

    chall.append(c)
    
  json_object = json.dumps(chall)
  with open("/tmp/c.json", "w") as outfile:
    outfile.write(json_object)
  s3 = boto3.resource(service_name = 's3')
  s3.meta.client.upload_file(Filename = '/tmp/c.json', Bucket = 'fuccoin', Key = 'block.json')
    
def award(name):
  s3 = boto3.client('s3')
  data = s3.get_object(Bucket='fuccoin', Key='wallet.json')
  names = json.loads(data['Body'].read())
  entry = False
  itr = 0
  for v in names:
    if(name == v[0]):
      names[itr] = [v[0],v[1]+1]
      entry = True
    itr += 1
  if(entry == False):
    names.append([name,1])
  print(names)
  
  json_object = json.dumps(names)
  with open("/tmp/n.json", "w") as outfile:
    outfile.write(json_object)
    
  s3 = boto3.resource(service_name = 's3')
  s3.meta.client.upload_file(Filename = '/tmp/n.json', Bucket = 'fuccoin', Key = 'wallet.json')
  
def mint(name):
  award(name)
  makechallenge()


def lambda_handler(event, context):
  # Get current 
  s3 = boto3.client('s3')
  data = s3.get_object(Bucket='fuccoin', Key='block.json')
  tests = json.loads(data['Body'].read())
  for v in tests:
    print("testing:" + str(v[0]))
    res = evaluate(event["queryStringParameters"]['bf'],v[0])
    print("got:" + str(res))
    if(res != v[1]):
      exit()
  mint(event["queryStringParameters"]['name'])
    
  return {
      'statusCode': 200,
      'body': json.dumps('Nice Coin Bro!')
  }
