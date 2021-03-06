#packages
import sqlite3
import os
from PIL import Image
from random import shuffle, randint, sample
from colorama import init, Fore

#scripts
from common_functions import comecar_jogo, encerrar_jogo, instrucoes, salvar_jogo

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

    cartas_string = ""

    for i in range(n_cartas):
        carta = cartas[0] #pega as primeiras cartas do maço
        cartas.pop(0)

        print(Fore.CYAN + "CASA {}:" .format(i+1) + Fore.RESET + " {}" .format(carta))
        cartas_string += "CASA %s: %s | " %((i+1), carta)

    salvar_jogo(cartas=cartas_string, foto=None)

    encerrar_jogo(connection)

def mesa_real():
    """Método Mesa Real.
    36 cartas (o baralho inteiro) para uma visão geral da vida da pessoa, levando-se em consideração as casas de acordo com o número das cartas (casa 1 = casa do Cavaleiro, casa 2 = casa do Trevo, etc).
    """

    template = Image.open("./img/templates/mesa-real.png")
    copy_template = template.copy() #copia a img pra não sobrescrever a do template na pasta
    posicoes = [(142, 81), (472, 81), (818, 81), (1154, 81), (1490, 81), (1828, 81), (2165, 81), (2504, 81),
        (142, 641), (472, 641), (818, 641), (1154, 641), (1490, 641), (1828, 641), (2165, 641), (2504, 641),
        (142, 1205), (472, 1205), (818, 1205), (1154, 1205), (1490, 1205), (1828, 1205), (2165, 1205),(2504, 1205),
        (142, 1775), (472, 1775), (818, 1775), (1154, 1775), (1490, 1775), (1828, 1775), (2165, 1775), (2504, 1775),
    (818, 2330), (1154, 2330), (1490, 2330), (1828, 2330)]

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

    cartas_string = ""

    for numero in enumerate(numeros):
        carta = cartas[numero[1]][1]

        print(Fore.GREEN + "CASA {}:" .format(numero[0]+1) + Fore.RESET + " {}" .format(carta))
        cartas_string += "CASA %s: %s | " %((numero[0]+1), carta)

    #montagem da imagem do jogo
    for i in range(len(imagens)):
        if i == TODOS[i]: copy_template.paste(imagens[i], posicoes[i])

    copy_template.save("./img/jogo.png", "PNG")
    copy_template.show()

    #salvamento do jogo
    salvar_jogo(cartas_string)

    os.remove("./img/jogo.png") #exclui a foto salva pq ela já tá no banco

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
    cartas_string = carta

    img.save("./img/jogo.png", "PNG")
    img.show()

    #salvamento do jogo
    salvar_jogo(cartas_string)

    os.remove("./img/jogo.png") #exclui a foto salva pq ela já tá no banco

    encerrar_jogo(connection)

def conselho_dia():
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

    cartas_string = ""

    for numero in enumerate(numeros):
        carta = cartas[numero[1]][1]

        if numero[0] == 0: r = "ENERGIA DO DIA"
        else: r = "CONSELHO"
        
        print(Fore.BLUE + "{}:" .format(r) + Fore.RESET + " {}" .format(carta))
        cartas_string += "%s: %s | " %(r, carta)
    
    #montagem da imagem do jogo
    for i in range(len(imagens)):
        copy_template.paste(imagens[i], posicoes[i])

    copy_template.save("./img/jogo.png", "PNG")
    copy_template.show()

    #salvamento do jogo
    salvar_jogo(cartas_string)

    os.remove("./img/jogo.png") #exclui a foto salva pq ela já tá no banco

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

    cartas_string = ""

    for i, carta in enumerate(cartas_n):
        if len(numeros) == 6:
            if i == 0 or i == 2 or i == 4:
                if i == 0: r = "PASSADO"
                elif i == 2: r = "PRESENTE"
                else: r = "FUTURO"

                if len(numeros) == 6: carta = carta[1] + " + " + cartas_n[i+1][1] #duas cartas por vez

                print(Fore.GREEN + "{}:" .format(r) + Fore.RESET + " {}" .format(carta))
                cartas_string += "%s: %s | " %(r, carta)
        else:
            if i == 0: r = "PASSADO"
            elif i == 1: r = "PRESENTE"
            else: r = "FUTURO"

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

    #salvamento do jogo
    salvar_jogo(cartas_string)

    os.remove("./img/jogo.png") #exclui a foto salva pq ela já tá no banco

    encerrar_jogo(connection)

def cinco_cartas():
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

    #montagem da imagem do jogo
    for i in range(len(imagens)):
        copy_template.paste(imagens[i], posicoes[i])

    copy_template.save("./img/jogo.png", "PNG")
    copy_template.show()

    #salvamento do jogo
    salvar_jogo(cartas_string)

    os.remove("./img/jogo.png") #exclui a foto salva pq ela já tá no banco

    encerrar_jogo(connection)

def sete_cartas():
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
    
    #montagem da imagem do jogo
    for i in range(len(imagens)):
        copy_template.paste(imagens[i], posicoes[i])

    copy_template.save("./img/jogo.png", "PNG")
    copy_template.show()

    #salvamento do jogo
    salvar_jogo(cartas_string)

    os.remove("./img/jogo.png") #exclui a foto salva pq ela já tá no banco

    encerrar_jogo(connection)
