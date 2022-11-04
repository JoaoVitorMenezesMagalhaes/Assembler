assembly = 'ASM.txt' #Arquivo de entrada de contem o assembly
destinoBIN = 'BIN.txt' #Arquivo de saída que contem o binário formatado para VHDL

labels = {}


def  converteArroba(line):
  line = defineInstrucao(line)
  line = line.split('@')
  line = bin(int(line[1]))[2:].upper().zfill(9)
  line = ''.join(line)
  return line
 
def converteReg(line):
  line = defineInstrucao(line)
  line = line.split(',')[0]
  line = line.split (' ')[1]
  line = ''.join(line)
  return line

def  converteCifrao(line):
  line = defineInstrucao(line)
  line = line.split('$')
  line = bin(int(line[1]))[2:].upper().zfill(9)
  line = ''.join(line)
  return line

def  converteLabel(line):
  line = line.split('%')[1]
  #tmp = int(labels[label]["pos"])
  #line[1] = bin(int(tmp))[2:].upper().zfill(9)
  #line = ''.join(line)
  return line.replace("\n", "")
        

def identificaComentario(line):
  if '#' in line:
    line = line.split('#')[1]
    return line.replace("\n","")
  else:
    return line.replace("\n","")


def defineInstrucao(line):
  line = line.split('#')
  line = line[0]
  return line.replace("\n","")
    
def identificaLabel(line):
  line = line.split('%')
  label = line[1]
  return label

def trataMnemonico(line):
  line = line.replace("\n", "") #Remove o caracter de final de linha
  line = line.replace("\t", "") #Remove o caracter de tabulacao
  line = line.split(' ')[0]
  line = "".join(line)
  return line

def nomeLabel(line):
  line = line.split(':')
  label = line[0]
  return label


with open(assembly, "r") as f: #Abre o arquivo ASM
  lines = f.readlines() #Verifica a quantidade de linhas
  cont = 0
  contlabel = 0

  for line in lines:
    if ':' in line:
      labels[nomeLabel(line)] = cont-contlabel
      contlabel+=1
    cont+=1

  for line in lines:
    line = line.replace("\n", "")
    if line.startswith('J'):
      if 'JSR' in line:
        label = line.split('%')[1]
        labels[nomeLabel(line)] = "JSR"
      else:
        label = line.split('%')[1]
        type = line.split('%')[0]
        labels[nomeLabel(line)] = type.replace(" ", "")


with open(destinoBIN, "w") as f:  #Abre o destino BIN

  cont = 0 #Cria uma variável para contagem

  for line in lines:         
      
    if not ':' in line:
      if '@' in line:
        l = 'tmp(' + str(cont) + ') := ' + trataMnemonico(line) + ' & ' + converteReg(line) + ' & \"' + converteArroba(line) + '\"; -- ' + identificaComentario(line) + '\n'
        cont+=1

      elif '$' in line:
        l = 'tmp(' + str(cont) + ') := ' + trataMnemonico(line) + ' & ' + converteReg(line) + ' & \"' + converteCifrao(line) + '\"; -- ' + identificaComentario(line) + '\n'
        cont+=1

      elif line.replace("\n", "") == "NOP":
        l = 'tmp(' + str(cont) + ') := ' + line.replace("\n", "") + ' & \"' + bin(0)[2:].zfill(12) + '\"; -- ' + line.replace("\n", "") + '\n'
        cont+=1

      elif line.replace("\n", "") == "RET":
        l = 'tmp(' + str(cont) + ') := ' + line.replace("\n", "") + ' & \"' + bin(0)[2:].zfill(12) + '\"; -- ' + line.replace("\n", "") + '\n'
        cont+=1

      elif '%' in line:
        label = converteLabel(line)
        tmp = int(labels[label])
        l = 'tmp(' + str(cont) + ') := ' + trataMnemonico(line) + ' & \"' + bin(tmp)[2:].zfill(12) + '\"; -- ' + line.replace("\n", "")+ ' ' + str(tmp) + '\n'
        cont+=1

      else:
        l = line
        cont+=1

      f.write(l)
