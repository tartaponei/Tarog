import sqlite3
import os
from PIL import Image
from random import shuffle, randint, sample
from colorama import init, Fore
from common_functions import comecar_jogo, encerrar_jogo, instrucoes

init(autoreset=True)

TODOS = range(0, 78)
MENORES = range(0, 56)
MAIORES = range(0, 22)

##

def jogo_personalizado():
    """Joga um jogo personalizado, com número de cartas e quais Arcanos usar personalizados."""

    connection = comecar_jogo(personalizado=True)

    n_cartas = ""
    while n_cartas == 0 or not n_cartas.isnumeric():
        n_cartas = input("\nDigite o número de cartas que você quer tirar: ")
    n_cartas = int(n_cartas)

    if n_cartas == 1: n = "CARTA"
    else: n = "CARTAS"

    resp = 0
    while resp < 1 or resp > 6:
        print("\nEscolha quais cartas você quer usar:\n" + Fore.CYAN + "1- TODOS OS 78 ARCANOS\n" + Fore.MAGENTA + "2- SÓ ARCANOS MAIORES (22)\n" + Fore.YELLOW + "3- SÓ ARCANOS MENORES (56)\n" + Fore.GREEN + "4- SÓ ARCANOS MENORES NUMERADOS (40)\n" + Fore.RED + "5- SÓ A CORTE (16)\n" + Fore.BLUE + "6- ARCANOS MAIORES + ARCANOS MENORES NUMERADOS (62)")
        resp = int(input("Digite o número: "))

    cartas = []

    if resp == 1: 
        for linha in connection.execute("SELECT nome FROM cartas"):
            cartas.append(linha[0])
        jogo = "TODO O BARALHO"

    elif resp == 2: 
        for linha in connection.execute("SELECT nome FROM cartas INNER JOIN tipos ON tipos.id = cartas.tipo_id WHERE tipos.grandeza = 'maior'"):
            cartas.append(linha[0])
        jogo = "OS 22 ARCANOS MAIORES"

    elif resp == 3: 
        for linha in connection.execute("SELECT nome FROM cartas INNER JOIN tipos ON tipos.id = cartas.tipo_id WHERE tipos.grandeza = 'menor'"):
            cartas.append(linha[0])
        jogo = "OS 56 ARCANOS MENORES"

    elif resp == 4: 
        for linha in connection.execute("SELECT nome FROM cartas INNER JOIN tipos ON tipos.id = cartas.tipo_id WHERE tipos.tipo = 'numerado'"):
            cartas.append(linha[0])
        jogo = "OS 40 ARCANOS MENORES NUMERADOS"

    elif resp == 5: 
        for linha in connection.execute("SELECT nome FROM cartas INNER JOIN tipos ON tipos.id = cartas.tipo_id WHERE tipos.tipo = 'corte'"):
            cartas.append(linha[0])
        jogo = "OS 16 ARCANOS MENORES DA CORTE"

    elif resp == 6: 
        for linha in connection.execute("SELECT nome FROM cartas INNER JOIN tipos ON tipos.id = cartas.tipo_id WHERE tipos.grandeza = 'maior'"):
            cartas.append(linha[0])

        for linha in connection.execute("SELECT nome FROM cartas INNER JOIN tipos ON tipos.id = cartas.tipo_id WHERE tipos.tipo = 'numerado'"):
            cartas.append(linha[0])
        jogo = "22 ARCANOS MAIORES + 40 ARCANOS MENORES NUMERADOS"

    instrucoes(n_cartas)

    shuffle(cartas)
    print(Fore.CYAN + "\n--> JOGO DE {} {}, USANDO {} <--\n" .format(n_cartas, n, jogo))

    for i in range(n_cartas):
        carta = cartas[0] #pega as primeiras cartas do maço
        cartas.pop(0)

        print(Fore.CYAN + "CASA {}:" .format(i+1) + Fore.RESET + " {}" .format(carta))

    encerrar_jogo(connection)

def arcano_espelho():
    """Método de Arcano Espelho.
    1 Arcano Maior (ou pode usar o baralho todo) que é um espelho energético diário ou semanal de quem tira a carta, e indica como vai ser seu dia/semana e como agir.
    Autoconhecimento diário. Usuário mentaliza se quer saber do dia ou da semana."""

    connection = comecar_jogo(personalizado=True)

    resp = 0
    while resp < 1 or resp > 3:
        print("\nEscolha quais cartas você quer usar:\n" + Fore.CYAN + "1- TODOS OS 78 ARCANOS\n" + Fore.MAGENTA + "2- SÓ ARCANOS MAIORES (22)\n" + Fore.YELLOW + "3- SÓ ARCANOS MENORES (56)\n")
        resp = int(input("Digite o número: "))

    cartas = []

    if resp == 1: 
        for linha in connection.execute("SELECT id, nome FROM cartas"):
            cartas.append(linha)
        n = 78
        path = "./img/cards/tarot"

    elif resp == 2: 
        for linha in connection.execute("SELECT cartas.id, nome FROM cartas INNER JOIN tipos ON tipos.id = cartas.tipo_id WHERE tipos.grandeza = 'maior'"):
            cartas.append(linha)
        n = 22
        path = "./img/cards/tarot/major"

    elif resp == 3: 
        for linha in connection.execute("SELECT id, nome FROM cartas INNER JOIN tipos ON tipos.id = cartas.tipo_id WHERE tipos.grandeza = 'menor'"):
            cartas.append(linha)
        n = 56
        path = "./img/cards/tarot/minor"

    instrucoes(1)

    shuffle(cartas)
    indice = randint(0, n-1)
    carta = cartas[indice][1] #nome da carta
    c_id = cartas[indice][0]

    pasta = ""

    if n == 78: #se forem todos os arcanos, vai ter que ver as duas subpastas
        for _, _, files in os.walk(path):
            for imagem in files:
                if imagem.endswith(".png"):
                    nome = os.path.splitext(imagem)

                    if imagem in os.listdir("./img/cards/tarot/major"): pasta = "major"
                    else: pasta = "minor"

                    if int(nome[0][:2]) == int(c_id)-1: img = Image.open("./img/cards/tarot/{}/{}" .format(pasta, imagem)) #se o número no nome do arquivo bater com o id-1 (pq no banco tá +1), ele pega essa imagem
    else: #se for só os maiores ou só os menores ele vê só as subpastas
        for imagem in os.listdir(path):
            nome = os.path.splitext(imagem)

            if int(nome[0][:2]) == int(c_id)-1: img = Image.open("{}/{}" .format(path, imagem)) #se o número no nome do arquivo bater com o id-1 (pq lá tá +1), ele pega essa imagem

    print(Fore.GREEN + "\n--> ARCANO ESPELHO DO DIA/SEMANA <--")

    print(Fore.GREEN + "\nSEU ARCANO ESPELHO DE HOJE/SEMANA É: " + Fore.RESET + carta)
    img.show()
    
    encerrar_jogo(connection)

def elementos():
    """Método pra ver quais aspectos seus estão desarmonizados.
    4 Arcanos Menores cujos naipes indicam quais aspectos (elementos) de quem tira a carta precisam ser harmonizados novamente.
    Espadas = Mental, Copas = Emocional, Paus = Espiritual, Ouros = Físico"""

    template = Image.open("./img/templates/4-elementos.png")
    copy_template = template.copy() #copia a img pra não sobrescrever a do template na pasta
    pos_1 = (81, 122)
    pos_2 = (403, 122)
    pos_3 = (726, 122)
    pos_4 = (1048, 122)

    connection, cursor = comecar_jogo()

    numeros = sample(MENORES, 4)

    instrucoes(4, elementos=True)

    cursor.execute("SELECT cartas.id, nome FROM cartas INNER JOIN tipos ON tipos.id = cartas.tipo_id WHERE tipos.grandeza = 'menor'")
    cartas = cursor.fetchall()

    imagens = [] #vetor onde vão ficar as imagens das 4 cartas

    #pega as imagens e guarda no vetor:
    for numero in numeros:
        path = "./img/cards/tarot/minor"
        c_id = cartas[numero][0] #id da carta em questão

        for imagem in os.listdir(path):
            nome = os.path.splitext(imagem)

            if int(nome[0][:2]) == int(c_id)-1:
                img = Image.open("{}/{}" .format(path, imagem)) #se o número no nome do arquivo bater com o valor do id-1 (pq lá tá +1), ele pega essa imagem
                imagens.append(img)
    
    print("\nAS CARTAS QUE SAÍRAM SÃO (VEJA OS NAIPES APENAS):")

    for numero in numeros:
        carta = cartas[numero][1]
        c_id = cartas[numero][0]

        if "Espadas" in carta: cor = Fore.YELLOW
        elif "Copas" in carta: cor = Fore.BLUE
        elif "Paus" in carta: cor = Fore.RED
        else: cor = Fore.GREEN
        print(cor + carta)

    #montagem da imagem do jogo
    for i in range(len(imagens)):
        if i == 0: copy_template.paste(imagens[i], pos_1)
        elif i == 1: copy_template.paste(imagens[i], pos_2)
        elif i == 2: copy_template.paste(imagens[i], pos_3)
        else: copy_template.paste(imagens[i], pos_4)

    copy_template.show()

    encerrar_jogo(connection)

def mandala_tres():
    """Método Mandala de 3.
    3 Arcanos que representam, respecitivamente, Passado ou Causa, Presente ou Situação Atual, e Futuro ou Consequência.
    Para perguntas objetivas de sim ou não e bem formuladas."""

    template = Image.open("./img/templates/mandala-3.png")
    copy_template = template.copy() #copia a img pra não sobrescrever a do template na pasta
    pos_1 = (56, 53)
    pos_2 = (376, 53)
    pos_3 = (700, 53)

    connection, cursor = comecar_jogo()

    cursor.execute("SELECT id, nome FROM cartas")
    cartas = cursor.fetchall()

    instrucoes(3)

    numeros = sample(TODOS, 3)

    imagens = []

    #pega as imagens e guarda no vetor
    for numero in numeros:
        path = "./img/cards/tarot"
        c_id = cartas[numero][0] #id da carta em questão

        for _, _, files in os.walk(path):
                for imagem in files:
                    if imagem.endswith(".png"):
                        nome = os.path.splitext(imagem)

                        if imagem in os.listdir("./img/cards/tarot/major"): pasta = "major"
                        else: pasta = "minor"

                        if int(nome[0][:2]) == int(c_id)-1: 
                            img = Image.open("{}/{}/{}" .format(path, pasta, imagem)) #se o número no nome do arquivo bater com o valor do id-1 (pq lá tá +1), ele pega essa imagem
                            imagens.append(img)

    print(Fore.YELLOW + "\n--> MANDALA DE 3 <--\n")

    for numero in enumerate(numeros):
        carta = cartas[numero[1]][1]

        if numero[0] == 0: r = "CAUSA"
        elif numero[0] == 1: r = "SITUAÇÃO"
        else: r = "CONSEQUÊNCIA"

        print(Fore.YELLOW + "{}:" .format(r) + Fore.RESET + " {}" .format(carta))

    #montagem da imagem do jogo
    for i in range(len(imagens)):
        if i == 0: copy_template.paste(imagens[i], pos_1)
        elif i == 1: copy_template.paste(imagens[i], pos_2)
        else: copy_template.paste(imagens[i], pos_3)

    copy_template.show()

    encerrar_jogo(connection)

def mandala_cinco():
    """Método Manda de 5.
    5 Arcanos que representam, respecitvamente, Situação Atual, Influência Externa, Oposição, Favorecimento, Resultado e Conselho.
    Para perguntas objetivas e bem formuladas."""

    template = Image.open("./img/templates/mandala-5.png")
    copy_template = template.copy() #copia a img pra não sobrescrever a do template na pasta
    pos_1 = (545, 603)
    pos_2 = (545, 64)
    pos_3 = (545, 1152)
    pos_4 = (140, 603)
    pos_5 = (945, 603)
    pos_6 = (1256, 1357)

    connection, cursor = comecar_jogo()

    cursor.execute("SELECT id, nome FROM cartas")
    cartas = cursor.fetchall()

    instrucoes(6)

    numeros = sample(TODOS, 6)

    imagens = []

    #pega as imagens e guarda no vetor
    for numero in numeros:
        path = "./img/cards/tarot"
        c_id = cartas[numero][0] #id da carta em questão

        for _, _, files in os.walk(path):
                for imagem in files:
                    if imagem.endswith(".png"):
                        nome = os.path.splitext(imagem)

                        if imagem in os.listdir("./img/cards/tarot/major"): pasta = "major"
                        else: pasta = "minor"

                        if int(nome[0][:2]) == int(c_id)-1: 
                            img = Image.open("{}/{}/{}" .format(path, pasta, imagem)) #se o número no nome do arquivo bater com o valor do id-1 (pq lá tá +1), ele pega essa imagem
                            imagens.append(img)

    print(Fore.YELLOW + "\n--> MANDALA DE 5 <--\n")
    
    for numero in enumerate(numeros):
        """if numero[0] < 5:"""
        carta = cartas[numero[1]][1]

        if numero[0] == 0: r = "SITUAÇÃO"
        elif numero[0] == 1: r = "INFLUÊNCIA EXTERNA"
        elif numero[0] == 2: r = "OPOSIÇÃO"
        elif numero[0] == 3: r = "FAVORECIMENTO"
        elif numero[0] == 4: r = "RESULTADO"
        else: r = "CONSELHO/MENSAGEM"

        print(Fore.YELLOW + "{}:" .format(r) + Fore.RESET + " {}" .format(carta))

        """else:
            resp = ""
            while resp != "não" and resp != "sim":
                resp = input("\nDeseja tirar uma Mensagem? ")

            if resp == "sim":
                msg = cartas[numero[1]][0]
                print(Fore.YELLOW + "\nMENSAGEM:" + Fore.RESET + msg)"""

    #montagem da imagem do jogo
    for i in range(len(imagens)):
        if i == 0: copy_template.paste(imagens[i], pos_1)
        elif i == 1: copy_template.paste(imagens[i], pos_2)
        elif i == 2: copy_template.paste(imagens[i], pos_3)
        elif i == 3: copy_template.paste(imagens[i], pos_4)
        elif i == 4: copy_template.paste(imagens[i], pos_5)
        else: copy_template.paste(imagens[i], pos_6)

    copy_template.show()

    encerrar_jogo(connection)

def cruz_celta():
    """Método Cruz Celta.
    10 Arcanos que representam, respectivamente, Situação Presente, Influência Imediata, Consulente Perante o Problema, Determinações do Passado, O Que o Consulente Não Conhece, Influências do Futuro, Consulente, Fatores Ambientais, Caminho do Destino, e Resultado Final.
    Para perguntas bem formuladas, mas apresenta mais detalhes."""

    template = Image.open("./img/templates/cruz-celta.png")
    copy_template = template.copy() #copia a img pra não sobrescrever a do template na pasta
    pos_1 = (630, 977)
    pos_2 = (525, 1083)
    pos_3 = (630, 397)
    pos_4 = (1082, 977)
    pos_5 = (630, 1557)
    pos_6 = (172, 977)
    pos_7 = (1505, 1779)
    pos_8 = (1505, 1240)
    pos_9 = (1505, 693)
    pos_10 = (1505, 143)

    connection, cursor = comecar_jogo()

    cursor.execute("SELECT id, nome FROM cartas")
    cartas = cursor.fetchall()

    instrucoes(10)

    numeros = sample(TODOS, 10)

    imagens = []

    #pega as imagens e guarda no vetor
    for numero in numeros:
        path = "./img/cards/tarot"
        c_id = cartas[numero][0] #id da carta em questão

        for _, _, files in os.walk(path):
                for imagem in files:
                    if imagem.endswith(".png"):
                        nome = os.path.splitext(imagem)

                        if imagem in os.listdir("./img/cards/tarot/major"): pasta = "major"
                        else: pasta = "minor"

                        if int(nome[0][:2]) == int(c_id)-1: 
                            img = Image.open("{}/{}/{}" .format(path, pasta, imagem)) #se o número no nome do arquivo bater com o valor do id-1 (pq lá tá +1), ele pega essa imagem
                            imagens.append(img)

    imagens[1] = imagens[1].rotate(90,expand=True) #gira a carta 2

    print(Fore.BLUE + "\n--> CRUZ CELTA <--\n")
    
    for numero in enumerate(numeros):
        carta = cartas[numero[1]][1]

        if numero[0] == 0: r = "SITUAÇÃO (PESSOA OU ATMOSFERA ESPIRITUAL)"
        elif numero[0] == 1: r = "INFLUÊNCIA IMEDIATA"
        elif numero[0] == 2: r = "CONSULENTE PERANTE O PROBLEMA"
        elif numero[0] == 3: r = "PASSADO"
        elif numero[0] == 4: r = "CONSULENTE NÃO SABE"
        elif numero[0] == 5: r = "FUTURO QUE VAI INFLUENCIAR"
        elif numero[0] == 6: r = "REPRESENTAÇÃO DO CONSULENTE"
        elif numero[0] == 7: r = "FATORES AMBIENTAIS (CASA 1)"
        elif numero[0] == 8: r = "CAMINHO PARA O SUCESSO"
        else: r = "RESULTADO FINAL"

        print(Fore.BLUE + "{}:" .format(r) + Fore.RESET + " {}" .format(carta))

    #montagem da imagem do jogo
    for i in range(len(imagens)):
        if i == 0: copy_template.paste(imagens[i], pos_1)
        elif i == 1: copy_template.paste(imagens[i], pos_2)
        elif i == 2: copy_template.paste(imagens[i], pos_3)
        elif i == 3: copy_template.paste(imagens[i], pos_4)
        elif i == 4: copy_template.paste(imagens[i], pos_5)
        elif i == 5: copy_template.paste(imagens[i], pos_6)
        elif i == 6: copy_template.paste(imagens[i], pos_7)
        elif i == 7: copy_template.paste(imagens[i], pos_8)
        elif i == 8: copy_template.paste(imagens[i], pos_9)
        else: copy_template.paste(imagens[i], pos_10)

    copy_template.show()

    encerrar_jogo(connection)

def taca_amor():
    """Método A Taça do Amor.
    7 Arcanos que representam, respectivamente, Como Está O Relacionamento, Consulente Na Situação, Parceiro Na Situação, O Que Favorece O Relacionamento, O Que Não Favorece O Relacionamento, Futuro Próximo da Relação, e Conselho Final.
    Para perguntas sobre amor e relacionamentos."""

    template = Image.open("./img/templates/taca-amor.png")
    copy_template = template.copy() #copia a img pra não sobrescrever a do template na pasta
    pos_1 = (699, 1105)
    pos_2 = (906, 548)
    pos_3 = (493, 548)
    pos_4 = (1268, 102)
    pos_5 = (131, 101)
    pos_6 = (699, 1650)
    pos_7 = (699, 2197)

    connection, cursor = comecar_jogo()

    cursor.execute("SELECT id, nome FROM cartas")
    cartas = cursor.fetchall()

    instrucoes(7)

    numeros = sample(TODOS, 7)

    imagens = []

    #pega as imagens e guarda no vetor
    for numero in numeros:
        path = "./img/cards/tarot"
        c_id = cartas[numero][0] #id da carta em questão

        for _, _, files in os.walk(path):
                for imagem in files:
                    if imagem.endswith(".png"):
                        nome = os.path.splitext(imagem)

                        if imagem in os.listdir("./img/cards/tarot/major"): pasta = "major"
                        else: pasta = "minor"

                        if int(nome[0][:2]) == int(c_id)-1: 
                            img = Image.open("{}/{}/{}" .format(path, pasta, imagem)) #se o número no nome do arquivo bater com o valor do id-1 (pq lá tá +1), ele pega essa imagem
                            imagens.append(img)

    print(Fore.MAGENTA + "\n--> TAÇA DO AMOR <--\n")
    
    for numero in enumerate(numeros):
        carta = cartas[numero[1]][1]

        if numero[0] == 0: r = "COMO ESTÁ O RELACIONAMENTO"
        elif numero[0] == 1: r = "CONSULENTE NESSA SITUAÇÃO"
        elif numero[0] == 2: r = "PARCEIRO NESSA SITUAÇÃO"
        elif numero[0] == 3: r = "FAVORECE O RELACIONAMENTO"
        elif numero[0] == 4: r = "NÃO FAVORECE O RELACIONAMENTO"
        elif numero[0] == 5: r = "FUTURO PRÓXIMO DA RELAÇÃO"
        else: r = "CONSELHO FINAL"

        print(Fore.MAGENTA + "{}:" .format(r) + Fore.RESET + " {}" .format(carta))

    #montagem da imagem do jogo
    for i in range(len(imagens)):
        if i == 0: copy_template.paste(imagens[i], pos_1)
        elif i == 1: copy_template.paste(imagens[i], pos_2)
        elif i == 2: copy_template.paste(imagens[i], pos_3)
        elif i == 3: copy_template.paste(imagens[i], pos_4)
        elif i == 4: copy_template.paste(imagens[i], pos_5)
        elif i == 5: copy_template.paste(imagens[i], pos_6)
        else: copy_template.paste(imagens[i], pos_7)

    copy_template.show()

    encerrar_jogo(connection)

def templo_afrodite():
    """Método Templo de Afrodite.
    7 Arcanos que representam, respectivamente, áreas Mental, Sentimental e Física de quem tira as cartas (1, 2, 3), áreas Mental, Sentimental e Física do(a) parceiro(a) (4, 5, 6) e a Síntese do Relacionamento (Prognóstico).
    Para questões sobre estado e situação de um relacionamento."""

    template = Image.open("./img/templates/templo-afrodite.png")
    copy_template = template.copy() #copia a img pra não sobrescrever a do template na pasta
    pos_1 = (133, 63)
    pos_2 = (133, 604)
    pos_3 = (133, 1150)
    pos_4 = (958, 63)
    pos_5 = (958, 604)
    pos_6 = (958, 1150)
    pos_7 = (547, 604)

    connection, cursor = comecar_jogo()

    cursor.execute("SELECT id, nome FROM cartas")
    cartas = cursor.fetchall()

    instrucoes(7)

    numeros = sample(TODOS, 7)

    imagens = []

    #pega as imagens e guarda no vetor
    for numero in numeros:
        path = "./img/cards/tarot"
        c_id = cartas[numero][0] #id da carta em questão

        for _, _, files in os.walk(path):
                for imagem in files:
                    if imagem.endswith(".png"):
                        nome = os.path.splitext(imagem)

                        if imagem in os.listdir("./img/cards/tarot/major"): pasta = "major"
                        else: pasta = "minor"

                        if int(nome[0][:2]) == int(c_id)-1: 
                            img = Image.open("{}/{}/{}" .format(path, pasta, imagem)) #se o número no nome do arquivo bater com o valor do id-1 (pq lá tá +1), ele pega essa imagem
                            imagens.append(img)

    print(Fore.MAGENTA + "\n--> TEMPLO DE AFRODITE <--\n")
    
    for numero in enumerate(numeros):
        carta = cartas[numero[1]][1]

        if numero[0] == 0: r = Fore.YELLOW + "VOCÊ:" + Fore.MAGENTA + "\nO QUE VOCÊ PENSA SOBRE O RELACIONAMENTO"
        elif numero[0] == 1: r = "O QUE VOCÊ SENTE PELO(A) PARCEIRO(A), SEU CORAÇÃO"
        elif numero[0] == 2: r = "SUA ATRAÇÃO FÍSICA PELO(A) PARCEIRO(A), SEU TESÃO"
        elif numero[0] == 3: r = Fore.YELLOW + "\nPARCEIRO(A):" + Fore.MAGENTA + "\nO QUE ELE PENSA SOBRE O RELACIONAMENTO"
        elif numero[0] == 4: r = "O QUE ELE(A) SENTE POR VOCÊ, O CORAÇÃO DELE(A)"
        elif numero[0] == 5: r = "A ATRAÇÃO DELE(A) POR VOCÊ, O TESÃO DELE(A)"
        else: r = "\nSÍNTESE, PROGNÓSTICO DA RELAÇÃO"

        print(Fore.MAGENTA + "{}:" .format(r) + Fore.RESET + " {}" .format(carta))

    #montagem da imagem do jogo
    for i in range(len(imagens)):
        if i == 0: copy_template.paste(imagens[i], pos_1)
        elif i == 1: copy_template.paste(imagens[i], pos_2)
        elif i == 2: copy_template.paste(imagens[i], pos_3)
        elif i == 3: copy_template.paste(imagens[i], pos_4)
        elif i == 4: copy_template.paste(imagens[i], pos_5)
        elif i == 5: copy_template.paste(imagens[i], pos_6)
        else: copy_template.paste(imagens[i], pos_7)

    copy_template.show()

    encerrar_jogo(connection)

def carater():
    """Método do Caráter
    4 Arcanos que representam, respectivamente, a Persona da pessoa em questão (o que ela mostra ser, a "máscara"), a Personalidade (o que ela é realmente e não mostra), as Motivações (o que a leva a agir desse jeito) e as Intenções (o que ela realmente quer de você).
    Para saber sobre as intenções de alguém que você talvez desconfie, saber o que ela quer com você."""

    template = Image.open("./img/templates/carater.png")
    copy_template = template.copy() #copia a img pra não sobrescrever a do template na pasta
    pos_1 = (94, 100)
    pos_2 = (94, 712)
    pos_3 = (539, 100)
    pos_4 = (539, 712)

    connection, cursor = comecar_jogo()

    cursor.execute("SELECT id, nome FROM cartas")
    cartas = cursor.fetchall()

    instrucoes(4)

    numeros = sample(TODOS, 4)

    imagens = []

    #pega as imagens e guarda no vetor
    for numero in numeros:
        path = "./img/cards/tarot"
        c_id = cartas[numero][0] #id da carta em questão

        for _, _, files in os.walk(path):
                for imagem in files:
                    if imagem.endswith(".png"):
                        nome = os.path.splitext(imagem)

                        if imagem in os.listdir("./img/cards/tarot/major"): pasta = "major"
                        else: pasta = "minor"

                        if int(nome[0][:2]) == int(c_id)-1: 
                            img = Image.open("{}/{}/{}" .format(path, pasta, imagem)) #se o número no nome do arquivo bater com o valor do id-1 (pq lá tá +1), ele pega essa imagem
                            imagens.append(img)

    print(Fore.GREEN + "\n--> MÉTODO DO CARÁTER <--\n")
    
    for numero in enumerate(numeros):
        carta = cartas[numero[1]][1]

        if numero[0] == 0: r = "PERSONA, O QUE A PESSOA MOSTRA SER E É VISÍVEL"
        elif numero[0] == 1: r = "PERSONALIDADE, O QUE ELA ESCONDE E NÃO É VISÍVEL"
        elif numero[0] == 2: r = "MOTIVAÇÕES DELA, O QUE LEVA ELA A AGIR ASSIM"
        else: r = "INTENÇÕES DELA, O QUE ELA QUER DE VOCÊ"

        print(Fore.GREEN + "{}:" .format(r) + Fore.RESET + " {}" .format(carta))

    #montagem da imagem do jogo
    for i in range(len(imagens)):
        if i == 0: copy_template.paste(imagens[i], pos_1)
        elif i == 1: copy_template.paste(imagens[i], pos_2)
        elif i == 2: copy_template.paste(imagens[i], pos_3)
        else: copy_template.paste(imagens[i], pos_4)

    copy_template.show()

    encerrar_jogo(connection)

def peladan():
    """Método Peladán.
    5 Arcanos que representam, respecitvamente, Positivo, Negativo, Caminho, Resultado e Síntese/Consulente.
    Para perguntas objetivas, bem formuladas e com tempo determinado."""

    template = Image.open("./img/templates/peladan.png")
    copy_template = template.copy() #copia a img pra não sobrescrever a do template na pasta
    pos_5 = (444, 591)
    pos_3 = (444, 61)
    pos_4 = (444, 1127)
    pos_1 = (46, 591)
    pos_2 = (835, 591)

    connection, cursor = comecar_jogo()

    cursor.execute("SELECT id, nome FROM cartas")
    cartas = cursor.fetchall()

    numeros = sample(TODOS, 5) #pega 5

    instrucoes(5)

    imagens = []

    #pega as imagens e guarda no vetor
    for numero in numeros:
        path = "./img/cards/tarot"
        c_id = cartas[numero][0] #id da carta em questão

        for _, _, files in os.walk(path):
                for imagem in files:
                    if imagem.endswith(".png"):
                        nome = os.path.splitext(imagem)

                        if imagem in os.listdir("./img/cards/tarot/major"): pasta = "major"
                        else: pasta = "minor"

                        if int(nome[0][:2]) == int(c_id)-1: 
                            img = Image.open("{}/{}/{}" .format(path, pasta, imagem)) #se o número no nome do arquivo bater com o valor do id-1 (pq lá tá +1), ele pega essa imagem
                            imagens.append(img)
    
    print(Fore.YELLOW + "\n--> PELADÁN <--\n")

    for numero in enumerate(numeros):
        carta = cartas[numero[1]][1]

        if numero[0] == 0: r = "POSITIVO, O QUE ESTÁ A FAVOR"
        elif numero[0] == 1: r = "NEGATIVO, O QUE ESTÁ CONTRA"
        elif numero[0] == 2: r = "CAMINHO, COMO CONCILIAR OS DOIS ANTERIORES"
        elif numero[0] == 3: r = "RESULTADO"
        else: r = "COMO O CONSULENTE ESTÁ DIANTE DA SITUAÇÃO"

        print(Fore.YELLOW + "{}:" .format(r) + Fore.RESET + " {}" .format(carta))

        #montagem da imagem do jogo
    for i in range(len(imagens)):
        if i == 0: copy_template.paste(imagens[i], pos_1)
        elif i == 1: copy_template.paste(imagens[i], pos_2)
        elif i == 2: copy_template.paste(imagens[i], pos_3)
        elif i == 3: copy_template.paste(imagens[i], pos_4)
        else: copy_template.paste(imagens[i], pos_5)

    copy_template.show()

    encerrar_jogo(connection)