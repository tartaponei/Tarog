#packages
import sqlite3
import re
from colorama import init, Fore

init(autoreset=True)

MESTRES = (11, 22, 33, 44, 55, 66, 77, 88, 99)
ALGARISMOS = (1, 2, 3, 4, 5, 6, 7, 8, 9)
VOGAIS = ("a", "e", "i", "o", "u")

def desejo_instintivo(primeiro_nome):
    for i, letra in enumerate(primeiro_nome):
        if letra in VOGAIS:
            instintivo = verificar_todas_letras(letra)
            break
        elif letra == "w" and sons_w[i] == "u":
            instintivo = 3
            break

    return instintivo

def carma(nome_completo):
    presentes = []
    ausentes = []

    for letra in nome_completo:
        valor = verificar_todas_letras(letra)
        presentes.append(valor)

    for algarismo in ALGARISMOS:
        if algarismo not in presentes:
            ausentes.append(algarismo)

    print("NÚMEROS DE CARMA: ", end="")
    for num in ausentes:
        if num == ausentes[-1]: print(num)
        else: print("%d, " %num, end="")

def tendencias_ocultas(nome):
    algarismos_nome = []
    repetidos = []

    contagem = {}
    for nomee in nome:
        contagem.clear()
        algarismos_nome.clear()

        for letra in nomee:
            valor = verificar_todas_letras(letra)
            algarismos_nome.append(valor)

        contagem = {i:algarismos_nome.count(i) for i in algarismos_nome}

        for algarismo in contagem:
            if contagem.get(algarismo) > 3:
                repetidos.append(algarismo)

    if len(repetidos) > 0:
        for num in repetidos:
            if len(repetidos) > 1:
                if num == repetidos[-1]: print(num)
                else: print("%d, " %num, end="")
            else:
                print(num)
                break
        
    if len(repetidos) == 0: print("Nenhum")

###############

def num_destino(dia, mes, ano):
    valor = 0

    for alg in dia:
        valor += int(alg)
    for alg in mes:
        valor += int(alg)
    for alg in ano:
        valor += int(alg)

    valor = reducao_teosofica(valor)

    return valor

###############

def verificar_todas_letras(nome):
    valor = 0

    for letra in nome:
        if letra == "a" or letra == "j" or letra == "s": valor += 1
        elif letra == "b" or letra == "k" or letra == "t": valor += 2
        elif letra == "c" or letra == "l" or letra == "u": valor += 3
        elif letra == "d" or letra == "m" or letra == "v": valor += 4
        elif letra == "e" or letra == "n" or letra == "w": valor += 5
        elif letra == "f" or letra == "o" or letra == "x": valor += 6
        elif letra == "g" or letra == "p" or letra == "y": valor += 7
        elif letra == "h" or letra == "q" or letra == "z": valor += 8
        elif letra == "i" or letra == "r": valor += 9

    valor = reducao_teosofica(valor)
    return valor

def verificar_vogais(nome, sons_w):
    valor = 0

    contagem_w = 0
    for letra in nome:
        if letra == "a": valor += 1
        elif letra == "e": valor += 5
        elif letra == "i" or letra == "y": valor += 9
        elif letra == "o": valor += 6
        elif letra == "u": valor += 3
        elif letra == "w":
            contagem_w += 1

            if sons_w[contagem_w-1] == "u": valor += 3
    
    valor = reducao_teosofica(valor)
    return valor

def verificar_consoantes(nome, sons_w):
    valor = 0

    contagem_w = 0
    for letra in nome:
        if letra == "j" or letra == "s": valor += 1
        elif letra == "b" or letra == "k" or letra == "t": valor += 2
        elif letra == "c" or letra == "l": valor += 3
        elif letra == "d" or letra == "m" or letra == "v": valor += 4
        elif letra == "n": valor += 5
        elif letra == "f" or letra == "x": valor += 6
        elif letra == "g" or letra == "p": valor += 7
        elif letra == "h" or letra == "q" or letra == "z": valor += 8
        elif letra == "r": valor += 9
        elif letra == "w":
            contagem_w += 1

            if sons_w[contagem_w-1] == "v": valor += 4

    valor = reducao_teosofica(valor)
    return valor

def reducao_teosofica(num):
    while num not in ALGARISMOS:
        if num not in MESTRES:
            alg = 0
            for algarismo in str(num):
                alg += int(algarismo)
            
            num = alg
        else:
            break

    return num

##############################

def numerologia():
    print(Fore.MAGENTA + "\n>> NUMEROLOGIA PITAGÓRICA <<\n")

    data = ""

    #nome
    nome = input("Digite seu nome completo SEM ACENTOS: ")

    nome = nome.lower() #coloca tudo minúsculo
    nome = nome.split(" ") #separa o nome

    nome_completo = ""
    for a in nome:
        nome_completo += a

    resp = 0
    while resp > 2 or resp < 1:
        resp = int(input("\nDigite 1 se o primeiro nome for simples e 2 se for composto: "))

    #separação de nome e sobrenome
    if resp == 1: 
        primeiro_nome = nome[0]

        ultimo_nome = ""
        for i in range(len(nome)):
            if i != 0:
                ultimo_nome += nome[i]
    elif resp == 2: 
        primeiro_nome = nome[0] + nome[1]

        ultimo_nome = ""
        for i in range(len(nome)):
            if i > 1:
                ultimo_nome += nome[i]

    #verificação de w
    sons_w = []

    contagem = 0
    for w in nome_completo:
        if w == "w":
            contagem += 1
            resp = " "

            while resp != "v" and resp != "u":
                resp = input("\nO %d° W no nome tem som de U ou de V? Digite U ou V: " %(contagem))
                resp = resp.lower()
            
            sons_w.append(resp) #coloca o som na lista
    print("\n")

    #data
    while not re.match("[0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9]", data):
        data = input("Digite sua data de nascimento no formato DD/MM/AAAA: ")
    
    dia = data[:2]
    mes = data[3:5]
    ano = data[6:10]

    #cálculo dos números:

    #número de expressão
    expressao = verificar_todas_letras(nome_completo)
    print("\nNÚMERO DE EXPRESSÃO:", expressao)

    #número de motivação
    motivacao = verificar_vogais(nome_completo, sons_w)
    print("NÚMERO DE MOTIVAÇÃO:", motivacao)

    #número de impressão
    impressao = verificar_consoantes(nome_completo, sons_w)
    print("NÚMERO DE IMPRESSÃO/PERSONALIDADE:", impressao)

    #número-chave
    chave = verificar_todas_letras(primeiro_nome)
    print("NÚMERO-CHAVE:", chave)

    #pedra angular
    angular = verificar_todas_letras(primeiro_nome[0])
    print("PEDRA ANGULAR/FUNDAMENTAL:", angular)

    #desejo instintivo
    instintivo = desejo_instintivo(primeiro_nome)
    print("DESEJO INSTINTIVO:", instintivo)

    #números do carma
    carma(nome_completo)

    #tendências ocultas
    print("TENDÊNCIAS OCULTAS: ", end="")
    tendencias_ocultas(nome)
    
    ##################################

    #número de destino
    destino = num_destino(dia, mes, ano)
    print("NÚMERO DE DESTINO:", destino)

    input("\nFim do jogo.\nAperte Enter para continuar...")