#packages
import sqlite3
import os
from PIL import Image
from random import shuffle, randint, sample
from colorama import init, Fore

#scripts
from common_functions import comecar_jogo, encerrar_jogo, instrucoes, salvar_jogo

init(autoreset=True)

TODOS = range(0, 78)
MENORES = range(0, 56)
MAIORES = range(0, 22)

LENORMAND = range(1, 36)

def pegar_imagens(numeros, cartas, tarot=False, lenormand=False):
    imagens = []

    if tarot:
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

    if lenormand:
        for numero in numeros:
            path = "./img/cards/lenormand"
            c_id = cartas[numero][0] #id da carta em questão

            for imagem in os.listdir(path):
                nome = os.path.splitext(imagem)

                if int(nome[0][:2]) == int(c_id):
                    img = Image.open("{}/{}" .format(path, imagem)) #se o número no nome do arquivo bater com o valor do id, ele pega essa imagem
                    imagens.append(img)

    return imagens

def montar_mostrar_imagem(imagens, posicoes, copy_template):
    for i in range(len(imagens)):
        copy_template.paste(imagens[i], posicoes[i])

    copy_template.save("./img/jogo.png", "PNG")
    copy_template.show()

def finalizar_jogo(cartas_string):
    salvar_jogo(cartas_string)

    os.remove("./img/jogo.png") #exclui a foto salva pq ela já tá no banco

##

def jogo_personalizado(tarot=False, lenormand=False):
    """Joga um jogo personalizado, com número de cartas e quais Arcanos usar personalizados."""

    connection = comecar_jogo(personalizado=True)

    n_cartas = ""
    while n_cartas == 0 or not n_cartas.isnumeric():
        n_cartas = input("\nDigite o número de cartas que você quer tirar: ")
    n_cartas = int(n_cartas)

    if n_cartas == 1: n = "CARTA"
    else: n = "CARTAS"

    #usando cartas do tarô
    if tarot:
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

    #usando cartas do baralho cigano
    if lenormand:
        cartas = []
        for linha in connection.execute("SELECT nome FROM lenormand"):
            cartas.append(linha[0])
        jogo = "BARALHO CIGANO"

    instrucoes(n_cartas)

    shuffle(cartas)
    print(Fore.CYAN + "\n--> JOGO DE {} {}, USANDO {} <--\n" .format(n_cartas, n, jogo))

    cartas_string = "" #pro banco

    for i in range(n_cartas):
        carta = cartas[0] #pega as primeiras cartas do maço
        cartas.pop(0)

        print(Fore.CYAN + "CASA {}:" .format(i+1) + Fore.RESET + " {}" .format(carta))
        cartas_string += "CASA %s: %s | " %((i+1), carta)

    salvar_jogo(cartas=cartas_string, foto=None)

    encerrar_jogo(connection)

def arcano_espelho(tarot=False, lenormand=False):
    """Método de Arcano Espelho.
    1 Arcano Maior (ou pode usar o baralho todo) que é um espelho energético diário ou semanal de quem tira a carta, e indica como vai ser seu dia/semana e como agir.
    Autoconhecimento diário. Usuário mentaliza se quer saber do dia ou da semana."""

    connection = comecar_jogo(personalizado=True)

    cartas = []

    if tarot:
        resp = 0
        while resp < 1 or resp > 3:
            print("\nEscolha quais cartas você quer usar:\n" + Fore.CYAN + "1- TODOS OS 78 ARCANOS\n" + Fore.MAGENTA + "2- SÓ ARCANOS MAIORES (22)\n" + Fore.YELLOW + "3- SÓ ARCANOS MENORES (56)\n")
            resp = int(input("Digite o número: "))

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

    if lenormand:
        path = "./img/cards/lenormand"
        for linha in connection.execute("SELECT id, nome FROM lenormand"):
            cartas.append(linha)
        n = 36

    instrucoes(1)

    shuffle(cartas)
    indice = randint(0, n-1)
    carta = cartas[indice][1] #nome da carta
    c_id = cartas[indice][0]

    if tarot:
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

    if lenormand:
        for imagem in os.listdir(path):
            nome = os.path.splitext(imagem)

            if int(nome[0][:2]) == int(c_id):
                img = Image.open("{}/{}" .format(path, imagem)) #se o número no nome do arquivo bater com o valor do id, ele pega essa imagem

    print(Fore.GREEN + "\n--> SIM OU NÃO / ESPELHO <--")

    print(Fore.GREEN + "\nSEU ARCANO ESPELHO DE HOJE/SEMANA / SUA RESPOSTA É: " + Fore.RESET + carta)
    cartas_string = carta + " | "

    img.save("./img/jogo.png", "PNG")
    img.show()

    finalizar_jogo(cartas_string)
    
    encerrar_jogo(connection)

def conselho(tarot=False, lenormand=False):
    """Método da Carta + Conselho do Dia
    2 cartas que mostram, respectivamente, a Energia geral do dia e o Conselho para o dia (o que fazer ou o que não fazer).
    """

    template = Image.open("./img/templates/2-cartas.png")
    copy_template = template.copy() #copia a img pra não sobrescrever a do template na pasta
    posicoes = [(91, 93), (507, 93)]

    connection, cursor = comecar_jogo()
    cartas = []

    instrucoes(1)

    print(Fore.BLUE + "\n--> CARTA E CONSELHO DO DIA <--\n")

    if lenormand:
        cursor.execute("SELECT id, nome FROM lenormand")
        cartas = cursor.fetchall()
        numeros = sample(LENORMAND, 2)

        imagens = pegar_imagens(numeros, cartas, lenormand=True)

    if tarot:
        cursor.execute("SELECT id, nome FROM cartas")
        cartas = cursor.fetchall()
        numeros = sample(TODOS, 2)

        imagens = pegar_imagens(numeros, cartas, tarot=True)

    cartas_string = ""

    for numero in enumerate(numeros):
        carta = cartas[numero[1]][1]

        if numero[0] == 0: r = "ENERGIA DO DIA"
        else: r = "CONSELHO"
        
        print(Fore.BLUE + "{}:" .format(r) + Fore.RESET + " {}" .format(carta))
        cartas_string += "%s: %s | " %(r, carta)
    
    montar_mostrar_imagem(imagens, posicoes, copy_template)

    finalizar_jogo(cartas_string)

    encerrar_jogo(connection)

def elementos():
    """Método pra ver quais aspectos seus estão desarmonizados.
    4 Arcanos Menores cujos naipes indicam quais aspectos (elementos) de quem tira a carta precisam ser harmonizados novamente.
    Espadas = Mental, Copas = Emocional, Paus = Espiritual, Ouros = Físico"""

    template = Image.open("./img/templates/4-elementos.png")
    copy_template = template.copy() #copia a img pra não sobrescrever a do template na pasta
    posicoes = [(81, 122), (403, 122), (726, 122), (1048, 122)]
    """pos_1 = (81, 122)
    pos_2 = (403, 122)
    pos_3 = (726, 122)
    pos_4 = (1048, 122)"""

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

    cartas_string = ""

    for numero in numeros:
        carta = cartas[numero][1]
        c_id = cartas[numero][0]

        if "Espadas" in carta: cor = Fore.YELLOW
        elif "Copas" in carta: cor = Fore.BLUE
        elif "Paus" in carta: cor = Fore.RED
        else: cor = Fore.GREEN
        print(cor + carta)

        cartas_string += carta + " | "

    montar_mostrar_imagem(imagens, posicoes, copy_template)

    finalizar_jogo(cartas_string)

    encerrar_jogo(connection)

def espiritualidade(tarot=False, lenormand=False): #NÃO TÁ FEITO!!!!!!!!
    """Método da Espiritualidade
    7 cartas que mostram nossa conexão com a espiritualdiade através dos chakras, respectivamente Seres Ínferos, Ancestrais, Você (Alma), Você (Espírito), Mentores, Anjos (Protetores) e Divindade.
    Créditos ao querdiíssimo Wayner Lyra.
    """

def mandala_tres(tarot=False, lenormand=False):
    """Método Mandala de 3.
    3 cartas que podem ser lidas de forma linear, como Passado - Presente - Futuro ou Causa - Situação - Consequência
    Para perguntas objetivas de sim ou não e bem formuladas."""

    template = Image.open("./img/templates/mandala-3.png")
    copy_template = template.copy() #copia a img pra não sobrescrever a do template na pasta
    pos_1 = (56, 53)
    pos_2 = (376, 53)
    pos_3 = (700, 53)

    pos_4 = (84, 383)
    pos_5 = (404, 383)
    pos_6 = (730, 383)

    connection, cursor = comecar_jogo()

    resp = 0
    while resp < 1 or resp > 2:
        print("\nQuantas cartas por casa você quer usar? (1 ou 2):")
        resp = int(input("Digite o número: "))

    if resp == 2: 
        template = Image.open("./img/templates/3-cartas.png")
        copy_template = template.copy()

    instrucoes(3)

    print(Fore.GREEN + "\n--> 3 CARTAS <--\n")

    imagens = []

    #pega as imagens e guarda no vetor (esse método é diferetne dos outros então deixei aqui)
    if lenormand:
        cursor.execute("SELECT id, nome FROM lenormand")
        cartas = cursor.fetchall()
        numeros = sample(LENORMAND, resp*3)
        path = "./img/cards/lenormand"

        for numero in numeros:
            path = "./img/cards/lenormand"
            c_id = cartas[numero][0] #id da carta em questão

            for imagem in os.listdir(path):
                nome = os.path.splitext(imagem)

                if int(nome[0][:2]) == int(c_id)-1:
                    img = Image.open("{}/{}" .format(path, imagem)) #se o número no nome do arquivo bater com o valor do id, ele pega essa imagem
                    imagens.append(img)

    if tarot:
        cursor.execute("SELECT id, nome FROM cartas")
        cartas = cursor.fetchall()
        numeros = sample(range(1, 78), resp*3)
        path = "./img/cards/tarot"

        for numero in numeros:
            path = "./img/cards/tarot"
            c_id = cartas[numero][0] #id da carta em questão

            for _, _, files in os.walk(path):
                    for imagem in files:
                        if imagem.endswith(".png"):
                            nome = os.path.splitext(imagem)

                            if imagem in os.listdir("./img/cards/tarot/major"): pasta = "major"
                            else: pasta = "minor"

                            if int(nome[0][:2]) == int(c_id)-2: 
                                img = Image.open("{}/{}/{}" .format(path, pasta, imagem)) #se o número no nome do arquivo bater com o valor do id-1 (pq lá tá +1), ele pega essa imagem
                                imagens.append(img)

    cartas_n = []
    for numero in numeros:
        for carta in cartas:
            if int(carta[0]) == numero:
                cartas_n.append(carta)

    cartas_string = ""


    for i, carta in enumerate(cartas_n):
        if len(numeros) == 6:
            if i == 0 or i == 2 or i == 4:
                if i == 0: r = "PASSADO/CAUSA"
                elif i == 2: r = "PRESENTE/SITUAÇÃO"
                else: r = "FUTURO/CONSEQUÊNCIA"

                if len(numeros) == 6: carta = carta[1] + " + " + cartas_n[i+1][1] #duas cartas por vez

                print(Fore.GREEN + "{}:" .format(r) + Fore.RESET + " {}" .format(carta))
                cartas_string += "%s: %s | " %(r, carta)
        else:
            if i == 0: r = "PASSADO/CAUSA"
            elif i == 1: r = "PRESENTE/SITUAÇÃO"
            else: r = "FUTURO/CONSEQUÊNCIA"

            print(Fore.GREEN + "{}:" .format(r) + Fore.RESET + " {}" .format(carta[1]))
            cartas_string += "%s: %s | " %(r, carta[1])

    #montagem da imagem do jogo
    if len(numeros) == 3:
        for i in range(len(imagens)):
            if i == 0: copy_template.paste(imagens[i], pos_1)
            elif i == 1: copy_template.paste(imagens[i], pos_2)
            else: copy_template.paste(imagens[i], pos_3)

    else:
        for i in range(len(imagens)):
            if i == 0: copy_template.paste(imagens[i], pos_1)
            elif i == 1: copy_template.paste(imagens[i], pos_4)
            elif i == 2: copy_template.paste(imagens[i], pos_2)
            elif i == 3: copy_template.paste(imagens[i], pos_5)
            elif i == 4: copy_template.paste(imagens[i], pos_3)
            else: copy_template.paste(imagens[i], pos_6)

    copy_template.save("./img/jogo.png", "PNG")
    copy_template.show()

    finalizar_jogo(cartas_string)

    encerrar_jogo(connection)


    """template = Image.open("./img/templates/mandala-3.png")
    copy_template = template.copy() #copia a img pra não sobrescrever a do template na pasta
    posicoes =[(56, 53), (376, 53), (700, 53)]

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

    cartas_string = ""

    for numero in enumerate(numeros):
        carta = cartas[numero[1]][1]

        if numero[0] == 0: r = "CAUSA"
        elif numero[0] == 1: r = "SITUAÇÃO"
        else: r = "CONSEQUÊNCIA"

        print(Fore.YELLOW + "{}:" .format(r) + Fore.RESET + " {}" .format(carta))
        cartas_string += "%s: %s | " %(r, carta)

    #montagem da imagem do jogo
    for i in range(len(imagens)):
        copy_template.paste(imagens[i], posicoes[i])

    copy_template.save("./img/jogo.png", "PNG")
    copy_template.show()

    #salvamento do jogo
    salvar_jogo(cartas_string)

    os.remove("./img/jogo.png") #exclui a foto salva pq ela já tá no banco

    encerrar_jogo(connection)"""

def mandala_cinco(tarot=False, lenormand=False):
    """Método Manda de 5.
    5 Arcanos que representam, respecitvamente, Situação Atual, Influência Externa, Oposição, Favorecimento, Resultado e Conselho.
    Para perguntas objetivas e bem formuladas."""

    template = Image.open("./img/templates/mandala-5.png")
    copy_template = template.copy() #copia a img pra não sobrescrever a do template na pasta
    posicoes = [(545, 603), (545, 64), (545, 1152), (140, 603), (945, 603), (1256, 1357)]

    connection, cursor = comecar_jogo()

    if tarot:
        cursor.execute("SELECT id, nome FROM cartas")
        cartas = cursor.fetchall()
    if lenormand:
        cursor.execute("SELECT id, nome FROM lenormand")
        cartas = cursor.fetchall()

    instrucoes(6)

    if lenormand:
        numeros = sample(LENORMAND, 6)
        imagens = pegar_imagens(numeros, cartas, lenormand=True)

    if tarot:
        numeros = sample(TODOS, 6)
        imagens = pegar_imagens(numeros, cartas, tarot=True)

    print(Fore.YELLOW + "\n--> MANDALA DE 5 <--\n")
    
    cartas_string = ""
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
        cartas_string += "%s: %s | " %(r, carta)

    montar_mostrar_imagem(imagens, posicoes, copy_template)

    finalizar_jogo(cartas_string)

    encerrar_jogo(connection)

def cruz_celta(tarot=False, lenormand=False):
    """Método Cruz Celta.
    10 Arcanos que representam, respectivamente, Situação Presente, Influência Imediata, Consulente Perante o Problema, Determinações do Passado, O Que o Consulente Não Conhece, Influências do Futuro, Consulente, Fatores Ambientais, Caminho do Destino, e Resultado Final.
    Para perguntas bem formuladas, mas apresenta mais detalhes."""

    template = Image.open("./img/templates/cruz-celta.png")
    copy_template = template.copy() #copia a img pra não sobrescrever a do template na pasta
    posicoes = [(630, 977), (525, 1083), (630, 397), (1082, 977), (630, 1557), (172, 977), (1505, 1779), (1505, 1240), (1505, 693), (1505, 143)]

    connection, cursor = comecar_jogo()

    if tarot:
        cursor.execute("SELECT id, nome FROM cartas")
        cartas = cursor.fetchall()
    if lenormand:
        cursor.execute("SELECT id, nome FROM lenormand")
        cartas = cursor.fetchall()

    instrucoes(10)

    imagens = []

    #pega as imagens e guarda no vetor
    if tarot:
        numeros = sample(TODOS, 10)
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
    if lenormand:
        numeros = sample(LENORMAND, 10)
        path = "./img/cards/lenormand"

        for numero in numeros:
            path = "./img/cards/lenormand"
            c_id = cartas[numero][0] #id da carta em questão

            for imagem in os.listdir(path):
                nome = os.path.splitext(imagem)

                if int(nome[0][:2]) == int(c_id):
                    img = Image.open("{}/{}" .format(path, imagem)) #se o número no nome do arquivo bater com o valor do id, ele pega essa imagem
                    imagens.append(img)

    imagens[1] = imagens[1].rotate(90,expand=True) #gira a carta 2

    print(Fore.BLUE + "\n--> CRUZ CELTA <--\n")
    
    cartas_string = ""

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
        cartas_string += "%s: %s | " %(r, carta)

    montar_mostrar_imagem(imagens, posicoes, copy_template)

    finalizar_jogo(cartas_string)

    encerrar_jogo(connection)

def taca_amor(tarot=False, lenormand=False):
    """Método A Taça do Amor.
    7 Arcanos que representam, respectivamente, Como Está O Relacionamento, Consulente Na Situação, Parceiro Na Situação, O Que Favorece O Relacionamento, O Que Não Favorece O Relacionamento, Futuro Próximo da Relação, e Conselho Final.
    Para perguntas sobre amor e relacionamentos."""

    template = Image.open("./img/templates/taca-amor.png")
    copy_template = template.copy() #copia a img pra não sobrescrever a do template na pasta
    posicoes = [(699, 1105), (906, 548), (493, 548), (1268, 102), (131, 101), (699, 1650), (699, 2197)]

    connection, cursor = comecar_jogo()

    if tarot:
        cursor.execute("SELECT id, nome FROM cartas")
        cartas = cursor.fetchall()
    if lenormand:
        cursor.execute("SELECT id, nome FROM lenormand")
        cartas = cursor.fetchall()

    instrucoes(7)

    imagens = []

    #pega as imagens e guarda no vetor
    if tarot:
        numeros = sample(TODOS, 7)
        imagens = pegar_imagens(numeros, cartas, tarot=True)
    if lenormand:
        numeros = sample(LENORMAND, 7)
        imagens = pegar_imagens(numeros, cartas, lenormand=True)

    print(Fore.MAGENTA + "\n--> TAÇA DO AMOR <--\n")
    
    cartas_string = ""

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
        cartas_string += "%s: %s | " %(r, carta)

    montar_mostrar_imagem(imagens, posicoes, copy_template)

    finalizar_jogo(cartas_string)

    encerrar_jogo(connection)

def cinco_cartas(tarot=False, lenormand=False):
    """Método para Solução de Problemas
    5 cartas que mostram, respectivamente, como o problema se encontra atualmente, atos do passado que resultaram ou influenciaram no presente, tendências do futuro próximo, algo oculto em meio a problema que a pessoa não sabe, e a solução/conselho para resolver o problema.
    """

    template = Image.open("./img/templates/5-cartas.png")
    copy_template = template.copy() #copia a img pra não sobrescrever a do template na pasta
    posicoes = [(88, 116), (428, 116), (768, 116), (1104, 116), (1441, 116)]

    connection, cursor = comecar_jogo()
    cartas = []

    instrucoes(5)

    print(Fore.YELLOW + "\n--> CINCO CARTAS (SOLUÇÃO DE PROBLEMAS) <--\n")

    if lenormand:
        cursor.execute("SELECT id, nome FROM lenormand")
        cartas = cursor.fetchall()
    if tarot:
        cursor.execute("SELECT id, nome FROM cartas")
        cartas = cursor.fetchall()

    imagens = []

    if lenormand:
        numeros = sample(LENORMAND, 5)
        imagens = pegar_imagens(numeros, cartas, lenormand=True)
    if tarot:
        numeros = sample(TODOS, 5)
        imagens = pegar_imagens(numeros, cartas, tarot=True)

    cartas_string = ""
    for numero in enumerate(numeros):
        carta = cartas[numero[1]][1]

        if numero[0] == 0: r = "PRESENTE"
        elif numero[0] == 1: r = "PASSADO"
        elif numero[0] == 2: r = "FUTURO PRÓXIMO (CARTA CENTRAL)"
        elif numero[0] == 3: r = "OCULTO"
        else: r = "SOLUÇÃO"
        
        print(Fore.YELLOW + "{}:" .format(r) + Fore.RESET + " {}" .format(carta))
        cartas_string += "%s: %s | " %(r, carta)

    montar_mostrar_imagem(imagens, posicoes, copy_template)

    finalizar_jogo(cartas_string)

    encerrar_jogo(connection)

def sete_cartas(tarot=False, lenormand=False):
    """Método para Entendimento do Presente
    7 cartas para visão mais profunda da situação atual, que mostram, respectivamente, Passado que resultou ou influencou no Presente, Situação no Atual Momento, tendências do Futuro Próximo, Resposta propriamente dita para a pergunta, Energias da situação, Esperanças/Medos da pessoa quanto à situação, e Resultado Final da situação.
    """

    template = Image.open("./img/templates/7-cartas.png")
    copy_template = template.copy() #copia a img pra não sobrescrever a do template na pasta
    posicoes = [(70, 748), (381, 447), (694, 310), (1006, 104), (1321, 310), (1633, 467), (1943, 748)]

    connection, cursor = comecar_jogo()
    cartas = []

    instrucoes(7)

    print(Fore.YELLOW + "\n--> SETE CARTAS (VISÃO MAIS PROFUNDA DA SITUAÇÃO) <--\n")

    if lenormand:
        numeros = sample(LENORMAND, 7)
        cursor.execute("SELECT id, nome FROM lenormand")
        cartas = cursor.fetchall()
    if tarot:
        numeros = sample(TODOS, 7)
        cursor.execute("SELECT id, nome FROM cartas")
        cartas = cursor.fetchall()

    if lenormand: imagens = pegar_imagens(numeros, cartas, lenormand=True)
    if tarot: imagens = pegar_imagens(numeros, cartas, tarot=True)

    cartas_string = ""

    for numero in enumerate(numeros):
        carta = cartas[numero[1]][1]

        if numero[0] == 0: r = "PASSADO"
        elif numero[0] == 1: r = "PRESENTE"
        elif numero[0] == 2: r = "FUTURO PRÓXIMO"
        elif numero[0] == 3: r = "RESPOSTA (CARTA CENTRAL)"
        elif numero[0] == 4: r = "ENERGIAS"
        elif numero[0] == 5: r = "MEDOS E ESPERANÇAS"
        else: r = "RESULTADO FINAL"
        
        print(Fore.YELLOW + "{}:" .format(r) + Fore.RESET + " {}" .format(carta))
        cartas_string += "%s: %s | " %(r, carta)
    
    montar_mostrar_imagem(imagens, posicoes, copy_template)

    finalizar_jogo(cartas_string)

    encerrar_jogo(connection)

def templo_afrodite(tarot=False, lenormand=False):
    """Método Templo de Afrodite.
    7 Arcanos que representam, respectivamente, áreas Mental, Sentimental e Física de quem tira as cartas (1, 2, 3), áreas Mental, Sentimental e Física do(a) parceiro(a) (4, 5, 6) e a Síntese do Relacionamento (Prognóstico).
    Para questões sobre estado e situação de um relacionamento."""

    template = Image.open("./img/templates/templo-afrodite.png")
    copy_template = template.copy() #copia a img pra não sobrescrever a do template na pasta
    posicoes = [(133, 63), (133, 604), (133, 1150), (958, 63), (958, 604), (958, 1150), (547, 604)]

    connection, cursor = comecar_jogo()

    if tarot:
        cursor.execute("SELECT id, nome FROM cartas")
        cartas = cursor.fetchall()
    if lenormand:
        cursor.execute("SELECT id, nome FROM lenormand")
        cartas = cursor.fetchall()

    instrucoes(7)

    if tarot:
        numeros = sample(TODOS, 7)
        imagens = pegar_imagens(numeros, cartas, tarot=True)
    if lenormand:
        numeros = sample(LENORMAND, 7)
        imagens = pegar_imagens(numeros, cartas, lenormand=True)

    print(Fore.MAGENTA + "\n--> TEMPLO DE AFRODITE <--\n")
    
    cartas_string = ""

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
        cartas_string += "%s: %s | " %(r, carta)

    montar_mostrar_imagem(imagens, posicoes, copy_template)

    finalizar_jogo(cartas_string)

    encerrar_jogo(connection)

def carater(tarot=False, lenormand=False):
    """Método do Caráter
    4 Arcanos que representam, respectivamente, a Persona da pessoa em questão (o que ela mostra ser, a "máscara"), a Personalidade (o que ela é realmente e não mostra), as Motivações (o que a leva a agir desse jeito) e as Intenções (o que ela realmente quer de você).
    Para saber sobre as intenções de alguém que você talvez desconfie, saber o que ela quer com você."""

    template = Image.open("./img/templates/carater.png")
    copy_template = template.copy() #copia a img pra não sobrescrever a do template na pasta
    posicoes = [(94, 100), (94, 712), (539, 100), (539, 712)]

    connection, cursor = comecar_jogo()

    if tarot:
        cursor.execute("SELECT id, nome FROM cartas")
        cartas = cursor.fetchall()
    if lenormand:
        cursor.execute("SELECT id, nome FROM lenormand")
        cartas = cursor.fetchall()

    instrucoes(4)

    if tarot:
        numeros = sample(TODOS, 4)
        imagens = pegar_imagens(numeros, cartas, tarot=True)
    if lenormand:
        numeros = sample(LENORMAND, 4)
        imagens = pegar_imagens(numeros, cartas, lenormand=True)

    print(Fore.GREEN + "\n--> MÉTODO DO CARÁTER <--\n")
    
    cartas_string = ""

    for numero in enumerate(numeros):
        carta = cartas[numero[1]][1]

        if numero[0] == 0: r = "PERSONA, O QUE A PESSOA MOSTRA SER E É VISÍVEL"
        elif numero[0] == 1: r = "PERSONALIDADE, O QUE ELA ESCONDE E NÃO É VISÍVEL"
        elif numero[0] == 2: r = "MOTIVAÇÕES DELA, O QUE LEVA ELA A AGIR ASSIM"
        else: r = "INTENÇÕES DELA, O QUE ELA QUER DE VOCÊ"

        print(Fore.GREEN + "{}:" .format(r) + Fore.RESET + " {}" .format(carta))
        cartas_string += "%s: %s | " %(r, carta)

    montar_mostrar_imagem(imagens, posicoes, copy_template)

    finalizar_jogo(cartas_string)

    encerrar_jogo(connection)

def peladan(tarot=False, lenormand=False):
    """Método Peladán.
    5 Arcanos que representam, respecitvamente, Positivo, Negativo, Caminho, Resultado e Síntese/Consulente.
    Para perguntas objetivas, bem formuladas e com tempo determinado."""

    template = Image.open("./img/templates/peladan.png")
    copy_template = template.copy() #copia a img pra não sobrescrever a do template na pasta
    posicoes = [(46, 591), (835, 591), (444, 61), (444, 1127), (444, 591)]

    connection, cursor = comecar_jogo()

    instrucoes(5)

    if tarot:
        numeros = sample(TODOS, 5)
        cursor.execute("SELECT id, nome FROM cartas")
        cartas = cursor.fetchall()

        imagens = pegar_imagens(numeros, cartas, tarot=True)

    if lenormand:
        numeros = sample(LENORMAND, 5)
        cursor.execute("SELECT id, nome FROM lenormand")
        cartas = cursor.fetchall()

        imagens = pegar_imagens(numeros, cartas, lenormand=True)
    
    print(Fore.YELLOW + "\n--> PELADÁN <--\n")

    cartas_string = ""

    for numero in enumerate(numeros):
        carta = cartas[numero[1]][1]

        if numero[0] == 0: r = "POSITIVO, O QUE ESTÁ A FAVOR"
        elif numero[0] == 1: r = "NEGATIVO, O QUE ESTÁ CONTRA"
        elif numero[0] == 2: r = "CAMINHO, COMO CONCILIAR OS DOIS ANTERIORES"
        elif numero[0] == 3: r = "RESULTADO"
        else: r = "COMO O CONSULENTE ESTÁ DIANTE DA SITUAÇÃO"

        print(Fore.YELLOW + "{}:" .format(r) + Fore.RESET + " {}" .format(carta))
        cartas_string += "%s: %s | " %(r, carta)

    montar_mostrar_imagem(imagens, posicoes, copy_template)

    finalizar_jogo(cartas_string)

    encerrar_jogo(connection)

def sete_chaves(tarot=False, lenormand=False):
    """Método das 7 Chaves.
    7 Arcanos para analisar a fundo alguma magia, feitiço ou amarração feita. 
    A magia precisa ter sido confirmada através de outro jogo ou método antes deste método.
    Créditos ao queridíssimo Wayner Lyra."""

    template = Image.open("./img/templates/7-chaves.png")
    copy_template = template.copy() #copia a img pra não sobrescrever a do template na pasta
    posicoes = [(789, 76), (137, 604), (465, 604), (1119, 604), (1441, 604), (789, 1133), (789, 1666)]

    connection, cursor = comecar_jogo()

    if tarot:
        numeros = sample(TODOS, 7)
        cursor.execute("SELECT id, nome FROM cartas")
        cartas = cursor.fetchall()
    if lenormand:
        numeros = sample(LENORMAND, 7)
        cursor.execute("SELECT id, nome FROM lenormand")
        cartas = cursor.fetchall()

    instrucoes(7)

    if tarot: imagens = pegar_imagens(numeros, cartas, tarot=True)
    if lenormand: imagens = pegar_imagens(numeros, cartas, lenormand=True)
    
    print(Fore.YELLOW + "\n--> 7 CHAVES <--\n")

    cartas_string = ""

    for numero in enumerate(numeros):
        carta = cartas[numero[1]][1]

        if numero[0] == 0: r = "INTENÇÃO DO FEITIÇO"
        elif numero[0] == 1: r = "FALANGE QUE AJUDA NO FEITIÇO"
        elif numero[0] == 2: r = "INTENSIDADE DO FEITIÇO"
        elif numero[0] == 3: r = "O ANTIFEITIÇO"
        elif numero[0] == 4: r = "O QUE FAZER ATÉ QUE SE RESOLVA"
        elif numero[0] == 5: r = "ÁREA DA VIDA AFETADA"
        else: r = "COMO RESOLVER (CONSELHO)"

        print(Fore.YELLOW + "{}:" .format(r) + Fore.RESET + " {}" .format(carta))
        cartas_string += "%s: %s | " %(r, carta)

    montar_mostrar_imagem(imagens, posicoes, copy_template)

    finalizar_jogo(cartas_string)

    encerrar_jogo(connection)

def estrela(tarot=False, lenormand=False):
    """Método da Estrela
    6 cartas que mostram respectivamente Você Hoje, Estudos e Vida Social, Vida Afetiva e Família, Espiritualidade e Defesa Energética, Dinheiro e Trabalho e o Caminho/Conselho.
    Para saber como estamos com nós mesmos. 
    Créditos ao queridíssimo Wayner Lyra.
    """
    template = Image.open("./img/templates/estrela.png")
    copy_template = template.copy() #copia a img pra não sobrescrever a do template na pasta
    posicoes = [(562, 876), (152, 501), (152, 1212), (958, 1212), (958, 501), (562, 98)]

    connection, cursor = comecar_jogo()

    instrucoes(6)

    if tarot:
        cursor.execute("SELECT id, nome FROM cartas")
        cartas = cursor.fetchall()

        numeros = sample(TODOS, 6) #pega 6

        imagens = pegar_imagens(numeros, cartas, tarot=True)

    if lenormand:
        cursor.execute("SELECT id, nome FROM lenormand")
        cartas = cursor.fetchall()

        numeros = sample(LENORMAND, 6) #pega 6

        imagens = pegar_imagens(numeros, cartas, lenormand=True)
    
    print(Fore.GREEN + "\n--> ESTRELA <--\n")

    cartas_string = ""

    for numero in enumerate(numeros):
        carta = cartas[numero[1]][1]

        if numero[0] == 0: r = "VOCÊ HOJE"
        elif numero[0] == 1: r = "ESTUDOS / VIDA SOCIAL"
        elif numero[0] == 2: r = "VIDA AFETIVA / FAMÍLIA"
        elif numero[0] == 3: r = "ESPIRITUALIDADE / DEFESAS"
        elif numero[0] == 4: r = "DINHEIRO / TRABALHO"
        else: r = "CAMINHO / CONSELHO"

        print(Fore.GREEN + "{}:" .format(r) + Fore.RESET + " {}" .format(carta))
        cartas_string += "%s: %s | " %(r, carta)

    #montagem da imagem do jogo
    montar_mostrar_imagem(imagens, posicoes, copy_template)

    finalizar_jogo(cartas_string)

    encerrar_jogo(connection)
    