

import math
from collections import Counter
import csv

def remove_repetidos(lista):
    l = []
    for i in lista:
        if i not in l:
            l.append(i)
    l.sort()
    return l

def generateDict():
    myDict = {}
    myDict["tempo"] = ['ensolarado','ensolarado','nublado','chuvoso','chuvoso','chuvoso','nublado','ensolarado','ensolarado', 'chuvoso', 'ensolarado','nublado','nublado','chuvoso']
    myDict["temperatura"] = ['quente','quente','quente','amena','fria','fria','fria','amena','fria','amena','amena','amena','quente','amena']
    myDict["umidade"] = ['alta', 'alta', 'alta', 'alta', 'normal', 'normal', 'normal', 'alta', 'normal', 'normal',
                             'normal', 'alta', 'normal', 'alta']
    myDict["ventoso"] = ['falso', 'verdadeiro', 'falso', 'falso', 'falso', 'verdadeiro', 'verdadeiro', 'falso', 'falso', 'falso',
                         'verdadeiro', 'verdadeiro', 'falso', 'verdadeiro']
    myDict["classeyi"] = ['não', 'não', 'sim', 'sim', 'sim', 'não', 'sim', 'não', 'sim',
                         'sim', 'sim', 'sim', 'sim', 'não']
    return myDict
def calcularEntropias(file):

    i =0
    firstEntropia = 0
    final = {}
    returnDictionary = {}
    for index in list(reversed(file.keys())):
        classe = file[index]

        if i == 0:
            firstIndex = index

        total = len(classe)
        #print("index ", index, " : ",total)

        my_list = classe
        my_dict = {i: my_list.count(i) for i in my_list}
        #print(my_dict)

        if i == 0:
            for k, v in my_dict.items():
                #print(k + ": " + str(v))
                firstEntropia -= int(v) / total * math.log2(int(v) / total)

        if i > 0:
            first = file[firstIndex]

            arrayValsAux = {}
            for ind in my_dict:
                arrayVals = list()
                k =0
                for j in my_list:
                    if ind == j:
                        arrayVals.append(first[k])
                    k += 1
                arrayValsAux[ind] = arrayVals

            #{'falso': ['não', 'não', 'sim', 'sim', 'sim', 'não', 'sim', 'não'], 'verdadeiro': ['não', 'não', 'sim', 'sim', 'sim', 'não']}
            #print("arrayvalsaux: ",index," : ",arrayValsAux)
            returnDictionary[index] = arrayValsAux

            entropia = 0

            for key in arrayValsAux.keys():
                my_dict_vals = {i: arrayValsAux[key].count(i) for i in arrayValsAux[key]}  # cair no próximo deste
                valorinterno = 0
                for vi in my_dict_vals:
                    #print( "-",my_dict_vals.get(vi), "/",int(my_dict.get(key)), " * log2(",int(my_dict_vals.get(vi))/int(my_dict.get(key)), ")")
                    valorinterno -= - int(my_dict_vals.get(vi))/int(my_dict.get(key)) * math.log2(int(my_dict_vals.get(vi))/int(my_dict.get(key)))
                entropia += (int(my_dict.get(key)) / total) * valorinterno


            entropiaFinal = float(firstEntropia) + float(entropia)
            #print("entropiatotal =  ", firstEntropia, " - ", entropia)
            #print(entropiaFinal)
            final[index] = entropiaFinal

        i+=1

    return final, returnDictionary

def porIndex(file,index,key,listInds):

    #print("indice da vez: ", index)
    dictFinal = {}
    for k, v in file.items():
        if k != key: #caso não seja o atributo do arquivo que já tenha sido considerado alguma outra vez
            cont = 0
            indices = list()
            #print(k, " : ", v)
            for i in listInds:
                if i == index:
                    indices.append(v[cont])
                cont +=1
            #print("indices: ",indices)
            dictFinal[k] = indices

    return dictFinal

def maiorEntropia(entropia):
    maiorValor = -1
    key = ""
    for etf in entropia:
        if entropia.get(etf) > maiorValor:
            maiorValor = entropia.get(etf)
            key = etf
    return maiorValor, key

def arvoreDecisao(file):

    tree = {}

    #calcular a entropia para o caso da raiz e pegar as folhas (sim, não)
    entropia,leafs = calcularEntropias(file)

    #pegar a maior entropia e a chave que corresponde a esta maior entropia (se é tempo, temperatura, ventoso, etc)
    maior, key = maiorEntropia(entropia)

    #define árvore com a raiz sendo uma tupla (valor 1, e o maior valor da entropia)
    tree[key] = (1, maior)

    #pega os valores do atributo , então lista = [falso, verdadeiro] para o caso do ventoso
    lista = remove_repetidos(file.get(key))

    perindx = {}
    contador = 1.0
    contadorAux = 0.0
    #leafs = {}
    for l in lista:
        perindx = porIndex(file,l,key,file.get(key))
        entropia, leafs = calcularEntropias(perindx)
        maiorAux, keyAux = maiorEntropia(entropia)

        contador += 0.1
        tree[l] = (contador, maiorAux)

        contadorAux += 1
        tree[keyAux] = str(contador)+"."+str(contadorAux)
        tree[str(keyAux)+str(contador)+"."+str(contadorAux)] = leafs.get(keyAux)

        file.pop(keyAux)

    print(tree)

def lerCSV():
    dict = {}
    dictFinal = {}
    with open('dadosBenchmark_validacaoAlgoritmoAD.csv', mode='r') as csv_file:
        line_count = 0
        for row in csv.reader(csv_file, delimiter=';'):
            if line_count == 0:
                numCol = 0
                for r in row:
                    dict[r] = (numCol)
                    dictFinal[r] = []
                    numCol += 1
            else:
                for rr in dict:
                    dictFinal[rr].append(row[dict[rr]])
            line_count += 1
    return dictFinal


if __name__ == '__main__':

    fileXLS = lerCSV()
    arvoreDecisao(fileXLS)