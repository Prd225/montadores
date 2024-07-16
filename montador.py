#Pedro Barreto de Souza         CB01
import sys

op={ 
    'add':'8', #dois regs   
    'shr':'9', #dois regs
    'shl':'a', #dois regs
    'not':'b', #dois regs
    'and':'c', #dois regs 
    'or':'d', #dois regs
    'xor':'e', #dois regs
    'cmp':'f', #dois regs
    'ld':'0', #dois regs
    'st':'1', #dois regs
    'data':'2', #regB & adress
    'jmpr':'3', #regB
    'jmp':'4', #adress
    'jcond':'5', #condição & adress
    'clf':'6' #nada
}
regs = {'r0':'00','r1':'01','r2':'10','r3':'11'} #registradores
jcaez = {'c': 8, 'a': 4, 'e': 2, 'z': 1} #jump condicional
I_O = {'in': '0', 'out': '1', 'data':'0', 'addr':'1'} #Instrucoes de Input e Output

def output_file(memory, path, lista_operacoes): #constroi o arquivo de saida
    f = open(path,'w')
    f.write("v3.0 hex words addressed\n")
    a = 0
    while(a < len(lista_operacoes)):
        f.write(f"{a:02x}: {lista_operacoes[a]}")
        f.write("\n")
        a += 1
    
    for i in range(a,len(memory)):
        f.write(f"{i:02x}: {memory[i]}")
        f.write("\n")
    f.close()

def tranforma_registradores(ra,rb): #concatena os valores de registrador
    r = ra+rb
    r = str(hex(int(r,2))[2:])
    return r

def arquivo_entrada(path): #cria a lista das linhas do programa com cada palavra separada
    f = open(path,'r')
    linhas  =[line.rstrip('\n') for line in f] #pega o arquivo e tira os \n
    f.close()
    linhas = [i.lower() for i in linhas] #transforma todos os caracteres em minusculo
    linhas = [i for i in linhas if i] #apaga todas os espaços vazios
    linhas = [[y for x in item.split() for y in x.split(',') if y] for item in linhas] #divide em palavras sem as virgulas e espaços
    return linhas

def verifica_base(string): #Verifica em qual base está os endereços
    try:
        numero = int(string, base = 0 )
    except ValueError:
        numero = int(string,10)
    if(numero <= 15):
        return '0' + hex(numero)[2:]
    else:
        return hex(numero)[2:]

def jump_condicional(string): #Constroí os valores do jump condicional
    valor = [jcaez[string[i]] for i in range(1, len(string))]
    valor = sum(valor)
    return str(hex(valor)[2:])

def traduzir(arquivo): #Cria o arquivo com os valores hexadecimais para cada linha
    lista_op = list()
    for i in range(len(arquivo)):
        if(arquivo[i][0] == 'clf'):
            lista_op.append(op[arquivo[i][0]] + '0')
        elif(arquivo[i][0] == 'jmp'):
            lista_op.append(op[arquivo[i][0]] + '0')
            lista_op.append(verifica_base(arquivo[i][1]))
        elif(arquivo[i][0] == 'data'):
            lista_op.append(op[arquivo[i][0]] + tranforma_registradores('00',regs[arquivo[i][1]]))
            lista_op.append(verifica_base(arquivo[i][2]))
        elif(arquivo[i][0] == 'jmpr'):
            lista_op.append(op[arquivo[i][0]] + tranforma_registradores('00', regs[arquivo[i][1]]))
        elif(arquivo[i][0] in op):
            lista_op.append(op[arquivo[i][0]] + tranforma_registradores(regs[arquivo[i][1]],regs[arquivo[i][2]]))
        elif('j' in arquivo[i][0]):
            lista_op.append(op['jcond'] + jump_condicional(arquivo[i][0]))
            lista_op.append(verifica_base(arquivo[i][1]))
        elif(arquivo[i][0] in I_O):
            lista_op.append('7' + tranforma_registradores((I_O[arquivo[i][0]] + I_O[arquivo[i][1]]),regs[arquivo[i][2]]))
        else:
            print(f"\nErro na Leitura\t'{arquivo[i][0]}'\tlinha:{(i+1)}")
            break
    return lista_op
#Parte Principal "Main"
memory = ['00' for _ in range(256)]
arquivo_input = sys.argv[1]
arquivo_output = sys.argv[2]
arquivo_core = arquivo_entrada(arquivo_input)
lista_saida = traduzir(arquivo_core)
if lista_saida:
    output_file(memory,arquivo_output,lista_saida)
else:
    print("Erro Geral no Codigo")

