import sqlite3
import os
from PIL import Image
from random import shuffle, randint, sample
from colorama import init, Fore
from common_functions import comecar_jogo, encerrar_jogo, instrucoes

init(autoreset=True)

TODOS = [*range(0, 36)]

##

def jogo_personalizado():
    """Joga um jogo personalizado, com número de cartas personalizado."""

    connection = comecar_jogo(personalizado=True)

    n_cartas = ""
    while n_cartas == 0 or not n_cartas.isnumeric():
        n_cartas = input("\nDigite o número de cartas que você quer tirar: ")
    n_cartas = int(n_cartas)

    if n_cartas == 1: n = "CARTA"
    else: n = "CARTAS"

    cartas = []

    for linha in connection.execute("SELECT nome FROM lenormand"):
        cartas.append(linha[0])

    instrucoes(n_cartas)

    shuffle(cartas)
    print(Fore.CYAN + "\n--> JOGO DE {} {} <--\n" .format(n_cartas, n))

    for i in range(n_cartas):
        carta = cartas[0] #pega as primeiras cartas do maço
        cartas.pop(0)

        print(Fore.CYAN + "CASA {}:" .format(i+1) + Fore.RESET + " {}" .format(carta))

    encerrar_jogo(connection)

def mesa_real():
    """Método Mesa Real.
    36 cartas (o baralho inteiro) para uma visão geral da vida da pessoa, levando-se em consideração as casas de acordo com o número das cartas (casa 1 = casa do Cavaleiro, casa 2 = casa do Trevo, etc).
    """

    template = Image.open("./img/templates/mesa-real.png")
    copy_template = template.copy() #copia a img pra não sobrescrever a do template na pasta
    pos_1 = (142, 81)
    pos_2 = (472, 81)
    pos_3 = (818, 81)
    pos_4 = (1154, 81)
    pos_5 = (1490, 81)
    pos_6 = (1828, 81)
    pos_7 = (2165, 81)
    pos_8 = (2504, 81)

    pos_9 = (142, 641)
    pos_10 = (472, 641)
    pos_11 = (818, 641)
    pos_12 = (1154, 641)
    pos_13 = (1490, 641)
    pos_14 = (1828, 641)
    pos_15 = (2165, 641)
    pos_16 = (2504, 641)

    pos_17 = (142, 1205)
    pos_18 = (472, 1205)
    pos_19 = (818, 1205)
    pos_20 = (1154, 1205)
    pos_21 = (1490, 1205)
    pos_22 = (1828, 1205)
    pos_23 = (2165, 1205)
    pos_24 = (2504, 1205)

    pos_25 = (142, 1775)
    pos_26 = (472, 1775)
    pos_27 = (818, 1775)
    pos_28 = (1154, 1775)
    pos_29 = (1490, 1775)
    pos_30 = (1828, 1775)
    pos_31 = (2165, 1775)
    pos_32 = (2504, 1775)

    pos_33 = (818, 2330)
    pos_34 = (1154, 2330)
    pos_35 = (1490, 2330)
    pos_36 = (1828, 2330)

    posicoes = [pos_1, pos_2, pos_3, pos_4, pos_5, pos_6, pos_7, pos_8, pos_9, pos_10, pos_11, pos_12, pos_13, pos_14, pos_15, pos_16, pos_17, pos_18, pos_19, pos_20, pos_21, pos_22, pos_23, pos_24, pos_25, pos_26, pos_27, pos_28, pos_29, pos_30, pos_31, pos_32, pos_33, pos_34, pos_35, pos_36]

    connection, cursor = comecar_jogo()

    instrucoes(36)

    print(Fore.GREEN + "\n--> MESA REAL <--\n")

    cursor.execute("SELECT id, nome FROM lenormand")
    cartas = cursor.fetchall()

    numeros = TODOS.copy()
    shuffle(numeros)

    imagens = []

    #pega as imagens e guarda no vetor
    for numero in numeros:
        path = "./img/cards/lenormand"
        c_id = cartas[numero][0] #id da carta em questão

        for imagem in os.listdir(path):
            nome = os.path.splitext(imagem)

            if int(nome[0][:2]) == int(c_id):
                img = Image.open("{}/{}" .format(path, imagem)) #se o número no nome do arquivo bater com o valor do id, ele pega essa imagem
                imagens.append(img)

    for numero in enumerate(numeros):
        carta = cartas[numero[1]][1]

        print(Fore.GREEN + "CASA {}:" .format(numero[0]+1) + Fore.RESET + " {}" .format(carta))

    #montagem da imagem do jogo
    for i in range(len(imagens)):
        if i == TODOS[i]: copy_template.paste(imagens[i], posicoes[i])

    copy_template.show()

    encerrar_jogo(connection)

def sim_nao():
    """Método de Sim e Não / Carta do Dia
    1 carta que responde sua pergunta de sim ou não (vide interpretações da carta além da "tabela" de respostas). Ou então 1 carta que representa a energia geral do dia, recomendado verificar de manhã.
    """
    connection = comecar_jogo(personalizado=True)
    cartas = []

    instrucoes(1)

    print(Fore.GREEN + "\n--> SIM OU NÃO / CARTA DO DIA <--\n")

    for linha in connection.execute("SELECT id, nome FROM lenormand"):
        cartas.append(linha)

    indice = randint(0, 35)
    carta = cartas[indice][1] #nome da carta aleatória que saiu
    c_id = cartas[indice][0]

    #pega a imagem
    path = "./img/cards/lenormand"

    for imagem in os.listdir(path):
        nome = os.path.splitext(imagem)

        if int(nome[0][:2]) == int(c_id):
            img = Image.open("{}/{}" .format(path, imagem)) #se o número no nome do arquivo bater com o valor do id, ele pega essa imagem

    print(Fore.GREEN + "SUA RESPOSTA OU CARTA DO DIA É:" + Fore.RESET + " {}" .format(carta))
    img.show()

    encerrar_jogo(connection)

def conselho_dia():
    """Método da Carta + Conselho do Dia
    2 cartas que mostram, respectivamente, a Energia geral do dia e o Conselho para o dia (o que fazer ou o que não fazer).
    """

    template = Image.open("./img/templates/2-cartas.png")
    copy_template = template.copy() #copia a img pra não sobrescrever a do template na pasta
    pos_1 = (91, 93)
    pos_2 = (507, 93)

    connection, cursor = comecar_jogo()
    cartas = []

    instrucoes(1)

    print(Fore.BLUE + "\n--> CARTA E CONSELHO DO DIA <--\n")

    cursor.execute("SELECT id, nome FROM lenormand")
    cartas = cursor.fetchall()

    numeros = sample(range(1, 36), 2)

    #pega a imagem
    path = "./img/cards/lenormand"

    imagens = []

    for numero in numeros:
        path = "./img/cards/lenormand"
        c_id = cartas[numero][0] #id da carta em questão

        for imagem in os.listdir(path):
            nome = os.path.splitext(imagem)

            if int(nome[0][:2]) == int(c_id):
                img = Image.open("{}/{}" .format(path, imagem)) #se o número no nome do arquivo bater com o valor do id, ele pega essa imagem
                imagens.append(img)

    for numero in enumerate(numeros):
        carta = cartas[numero[1]][1]

        if numero[0] == 0: r = "ENERGIA DO DIA"
        else: r = "CONSELHO"
        
        print(Fore.BLUE + "{}:" .format(r) + Fore.RESET + " {}" .format(carta))
    
    #montagem da imagem do jogo
    for i in range(len(imagens)):
        if i == 0: copy_template.paste(imagens[i], pos_1)
        else: copy_template.paste(imagens[i], pos_2)

    copy_template.show()

    encerrar_jogo(connection)

def pass_pres_fut():
    """Método Passado, Presente e Futuro.
    3 cartas que mnostram respectivamente influências do Passado que afetaram diretamente ou resultaram no Presente e qual a tendência do Futuro próximo.
    """

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

    print(Fore.GREEN + "\n--> PASSADO, PRESENTE, FUTURO <--\n")

    cursor.execute("SELECT id, nome FROM lenormand")
    cartas = cursor.fetchall()

    numeros = sample(range(1, 36), (resp*3)) #pega a quantidade de cartas que a pessoa digitou

    cartas_n = []
    for numero in numeros:
        for carta in cartas:
            if int(carta[0]) == numero:
                cartas_n.append(carta)

    imagens = []

    #pega as imagens e guarda no vetor
    for carta in cartas_n:
        path = "./img/cards/lenormand"
        c_id = carta[0] #id da carta em questão

        for imagem in os.listdir(path):
            nome = os.path.splitext(imagem)

            if int(nome[0][:2]) == int(c_id):
                img = Image.open("{}/{}" .format(path, imagem)) #se o número no nome do arquivo bater com o valor do id, ele pega essa imagem
                imagens.append(img)

    for i, carta in enumerate(cartas_n):
        if len(numeros) == 6:
            if i == 0 or i == 2 or i == 4:
                if i == 0: r = "PASSADO"
                elif i == 2: r = "PRESENTE"
                else: r = "FUTURO"

                if len(numeros) == 6: carta = carta[1] + " + " + cartas_n[i+1][1] #duas cartas por vez

                print(Fore.GREEN + "{}:" .format(r) + Fore.RESET + " {}" .format(carta))
        else:
            if i == 0: r = "PASSADO"
            elif i == 1: r = "PRESENTE"
            else: r = "FUTURO"

            print(Fore.GREEN + "{}:" .format(r) + Fore.RESET + " {}" .format(carta[1]))

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

    copy_template.show()

    encerrar_jogo(connection)

def cinco_cartas():
    """Método para Solução de Problemas
    5 cartas que mostram, respectivamente, como o problema se encontra atualmente, atos do passado que resultaram ou influenciaram no presente, tendências do futuro próximo, algo oculto em meio a problema que a pessoa não sabe, e a solução/conselho para resolver o problema.
    """

    template = Image.open("./img/templates/5-cartas.png")
    copy_template = template.copy() #copia a img pra não sobrescrever a do template na pasta
    pos_1 = (88, 116)
    pos_2 = (428, 116)
    pos_3 = (768, 116)
    pos_4 = (1104, 116)
    pos_5 = (1441, 116)

    connection, cursor = comecar_jogo()
    cartas = []

    instrucoes(5)

    print(Fore.YELLOW + "\n--> CINCO CARTAS (SOLUÇÃO DE PROBLEMAS) <--\n")

    cursor.execute("SELECT id, nome FROM lenormand")
    cartas = cursor.fetchall()

    numeros = sample(range(1, 36), 5)

    #pega a imagem
    path = "./img/cards/lenormand"

    imagens = []

    for numero in numeros:
        path = "./img/cards/lenormand"
        c_id = cartas[numero][0] #id da carta em questão

        for imagem in os.listdir(path):
            nome = os.path.splitext(imagem)

            if int(nome[0][:2]) == int(c_id):
                img = Image.open("{}/{}" .format(path, imagem)) #se o número no nome do arquivo bater com o valor do id, ele pega essa imagem
                imagens.append(img)

    for numero in enumerate(numeros):
        carta = cartas[numero[1]][1]

        if numero[0] == 0: r = "PRESENTE"
        elif numero[0] == 1: r = "PASSADO"
        elif numero[0] == 2: r = "FUTURO PRÓXIMO (CARTA CENTRAL)"
        elif numero[0] == 3: r = "OCULTO"
        else: r = "SOLUÇÃO"
        
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

def sete_cartas():
    """Método para Entendimento do Presente
    7 cartas para visão mais profunda da situação atual, que mostram, respectivamente, Passado que resultou ou influencou no Presente, Situação no Atual Momento, tendências do Futuro Próximo, Resposta propriamente dita para a pergunta, Energias da situação, Esperanças/Medos da pessoa quanto à situação, e Resultado Final da situação.
    """

    template = Image.open("./img/templates/7-cartas.png")
    copy_template = template.copy() #copia a img pra não sobrescrever a do template na pasta
    pos_1 = (70, 748)
    pos_2 = (381, 447)
    pos_3 = (694, 310)
    pos_4 = (1006, 104)
    pos_5 = (1321, 310)
    pos_6 = (1633, 467)
    pos_7 = (1943, 748)

    connection, cursor = comecar_jogo()
    cartas = []

    instrucoes(7)

    print(Fore.YELLOW + "\n--> SETE CARTAS (VISÃO MAIS PROFUNDA DA SITUAÇÃO) <--\n")

    cursor.execute("SELECT id, nome FROM lenormand")
    cartas = cursor.fetchall()

    numeros = sample(range(1, 36), 7)

    #pega a imagem
    path = "./img/cards/lenormand"

    imagens = []

    for numero in numeros:
        path = "./img/cards/lenormand"
        c_id = cartas[numero][0] #id da carta em questão

        for imagem in os.listdir(path):
            nome = os.path.splitext(imagem)

            if int(nome[0][:2]) == int(c_id):
                img = Image.open("{}/{}" .format(path, imagem)) #se o número no nome do arquivo bater com o valor do id, ele pega essa imagem
                imagens.append(img)

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
