import sys
# arq1 = arquivo de base
# arq2 = seu arquivo
arq1 = sys.argv[1]
arq2 = sys.argv[2]
lista_arq1 = []
lista_arq2 = []
cont = 0
n_linha = 0

with open(arq1, 'r') as arq1: 
    for linha in arq1:
        lista_arq1.append([x for x in linha])
with open(arq2, 'r') as arq2: 
    for linha in arq2:
        lista_arq2.append([x for x in linha])

for x in range(len(lista_arq1)):
    n_linha +=1

    if(lista_arq1[x] == lista_arq2[x]):
        print(lista_arq1[x],"(A Linha",n_linha,"é idêntica nos dois arquivos)")
        cont +=1
    else:
        print(lista_arq1[x],lista_arq2[x],"(A linha",n_linha, "está diferente nos dois arquivos)")

print("O seu arquivo está",(cont/257)*100,"% semelhante ao arquivo base", )