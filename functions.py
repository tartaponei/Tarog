import sqlite3
from random import shuffle, randint, sample
from colorama import init, Style, Fore

init(autoreset=True)

TODOS = range(1, 79)
MENORES = range(1, 57)
MAIORES = range(1, 23)

def comecar_jogo(personalizado=None):
    """Começo do jogo. Abertura da conexão com o banco"""

    connection = sqlite3.connect("database.db")

    if not personalizado:
        cursor = connection.cursor()
        return connection, cursor
    else: return connection

def encerrar_jogo(connection):
    """Encerramento do jogo, fechamento da conexão com o banco."""

    connection.close()
    input("\nFim do jogo.\nAperte Enter para continuar...")

##

def jogo_personalizado():
    """Joga um jogo personalizado, com número de cartas e quais Arcanos usar personalizados."""

    connection = comecar_jogo(personalizado=True)

    n_cartas = int(input("\nDigite o número de cartas que você quer tirar: "))

    if n_cartas == 1: n = "CARTA"
    else: n = "CARTAS"
    
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

    shuffle(cartas)
    print(Fore.CYAN + "\n--> JOGO DE {} {}, USANDO {} <--\n" .format(n_cartas, n, jogo))

    for i in range(n_cartas):
        carta = cartas[0] #pega as primeiras cartas do maço
        cartas.pop(0)

        print(Fore.CYAN + "CASA {}:" .format(i+1) + Fore.RESET + " {}" .format(carta))

    encerrar_jogo(connection)

def arcano_espelho():
    """Método de Arcano Espelho.
    1 Arcano Maior que é um espelho energético diário ou semanal de quem tira a carta, e indica como vai ser seu dia/semana e como agir.
    Autoconhecimento diário. Usuário mentaliza se quer saber do dia ou da semana."""

    connection, cursor = comecar_jogo()

    n = str(randint(1, 23))
    cursor.execute("SELECT DISTINCT nome FROM cartas WHERE id = ?", (n,))
    cartas = cursor.fetchall()
    
    carta = cartas[0][0]

    print(Fore.GREEN + "\nSEU ARCANO ESPELHO DE HOJE/SEMANA É: " + Fore.RESET + carta)
    encerrar_jogo(connection)

def elementos():
    """Método pra ver quais aspectos seus estão desarmonizados.
    4 Arcanos Menores cujos naipes indicam quais aspectos (elementos) de quem tira a carta precisam ser harmonizados novamente.
    Espadas = Mental, Copas = Emocional, Paus = Espiritual, Ouros = Físico"""

    connection, cursor = comecar_jogo()

    print("\nAS CARTAS QUE SAÍRAM SÃO (VEJA OS NAIPES APENAS):")

    numeros = sample(MENORES, 4)

    cursor.execute("SELECT nome FROM cartas INNER JOIN tipos ON tipos.id = cartas.tipo_id WHERE tipos.grandeza = 'menor'")
    cartas = cursor.fetchall()

    for numero in numeros:
        if "Espadas" in cartas[numero][0]: cor = Fore.YELLOW
        elif "Copas" in cartas[numero][0]: cor = Fore.BLUE
        elif "Paus" in cartas[numero][0]: cor = Fore.RED
        else: cor = Fore.GREEN
        print(cor + cartas[numero][0])

    encerrar_jogo(connection)

def mandala_tres():
    """Método Mandala de 3.
    3 Arcanos que representam, respecitivamente, Passado ou Causa, Presente ou Situação Atual, e Futuro ou Consequência.
    Para perguntas objetivas de sim ou não e bem formuladas."""

    connection, cursor = comecar_jogo()

    print(Fore.YELLOW + "\n--> MANDALA DE 3 <--\n")

    cursor.execute("SELECT nome FROM cartas")
    cartas = cursor.fetchall()

    numeros = sample(TODOS, 3)

    for numero in enumerate(numeros):
        carta = cartas[numero[1]][0]

        if numero[0] == 0: r = "CAUSA"
        elif numero[0] == 1: r = "SITUAÇÃO"
        else: r = "CONSEQUÊNCIA"

        print(Fore.YELLOW + "{}:" .format(r) + Fore.RESET + " {}" .format(carta))

    encerrar_jogo(connection)

def mandala_cinco():
    """Método Manda de 5.
    5 Arcanos que representam, respecitvamente, Situação Atual, Influência Externa, Oposição, Favorecimento e Resultado. Uma 6ª carta pode ser tirada como Mensagem.
    Para perguntas objetivas e bem formuladas."""

    connection, cursor = comecar_jogo()

    print(Fore.YELLOW + "\n--> MANDALA DE 5 <--\n")

    cursor.execute("SELECT nome FROM cartas")
    cartas = cursor.fetchall()

    numeros = sample(TODOS, 6)

    for numero in enumerate(numeros):
        if numero[0] < 5:
            carta = cartas[numero[1]][0]

            if numero[0] == 0: r = "SITUAÇÃO"
            elif numero[0] == 1: r = "INFLUÊNCIA EXTERNA"
            elif numero[0] == 2: r = "OPOSIÇÃO"
            elif numero[0] == 3: r = "FAVORECIMENTO"
            elif numero[0] == 4: r = "RESULTADO"

            print(Fore.YELLOW + "{}:" .format(r) + Fore.RESET + " {}" .format(carta))

        else:
            resp = ""
            while resp != "não" and resp != "sim":
                resp = input("\nDeseja tirar uma Mensagem? ")

            if resp == "sim":
                msg = cartas[numero[1]][0]
                print(Fore.YELLOW + "\nMENSAGEM:" + Fore.RESET + msg)

    encerrar_jogo(connection)

def cruz_celta():
    """Método Cruz Celta.
    10 Arcanos que representam, respectivamente, Situação Presente, Influência Imediata, Consulente Perante o Problema, Determinações do Passado, O Que o Consulente Não Conhece, Influências do Futuro, Consulente, Fatores Ambientais, Caminho do Destino, e Resultado Final.
    Para perguntas bem formuladas, mas apresenta mais detalhes."""

    connection, cursor = comecar_jogo()

    print(Fore.BLUE + "\n--> CRUZ CELTA <--\n")

    cursor.execute("SELECT nome FROM cartas")
    cartas = cursor.fetchall()

    numeros = sample(TODOS, 10)

    for numero in enumerate(numeros):
        carta = cartas[numero[1]][0]

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

    encerrar_jogo(connection)

def taca_amor():
    """Método A Taça do Amor.
    7 Arcanos que representam, respectivamente, Como Está O Relacionamento, Consulente Na Situação, Parceiro Na Situação, O Que Favorece O Relacionamento, O Que Não Favorece O Relacionamento, Futuro Próximo da Relação, e Conselho Final.
    Para perguntas sobre amor e relacionamentos."""

    connection, cursor = comecar_jogo()

    print(Fore.MAGENTA + "\n--> TAÇA DO AMOR <--\n")

    cursor.execute("SELECT nome FROM cartas")
    cartas = cursor.fetchall()

    numeros = sample(TODOS, 7)

    for numero in enumerate(numeros):
        carta = cartas[numero[1]][0]

        if numero[0] == 0: r = "COMO ESTÁ O RELACIONAMENTO"
        elif numero[0] == 1: r = "CONSULENTE NESSA SITUAÇÃO"
        elif numero[0] == 2: r = "PARCEIRO NESSA SITUAÇÃO"
        elif numero[0] == 3: r = "FAVORECE O RELACIONAMENTO"
        elif numero[0] == 4: r = "NÃO FAVORECE O RELACIONAMENTO"
        elif numero[0] == 5: r = "FUTURO PRÓXIMO DA RELAÇÃO"
        else: r = "CONSELHO FINAL"

        print(Fore.MAGENTA + "{}:" .format(r) + Fore.RESET + " {}" .format(carta))

    encerrar_jogo(connection)

def templo_afrodite():
    """Método Templo de Afrodite.
    7 Arcanos que representam, respectivamente, áreas Mental, Sentimental e Física de quem tira as cartas (1, 2, 3), áreas Mental, Sentimental e Física do(a) parceiro(a) (4, 5, 6) e a Síntese do Relacionamento (Prognóstico).
    Para questões sobre estado e situação de um relacionamento."""

    connection, cursor = comecar_jogo()

    print(Fore.MAGENTA + "\n--> TEMPLO DE AFRODITE <--\n")

    cursor.execute("SELECT nome FROM cartas")
    cartas = cursor.fetchall()

    numeros = sample(TODOS, 7)

    for numero in enumerate(numeros):
        carta = cartas[numero[1]][0]

        if numero[0] == 0: r = Fore.YELLOW + "VOCÊ:" + Fore.MAGENTA + "\nO QUE VOCÊ PENSA SOBRE O RELACIONAMENTO"
        elif numero[0] == 1: r = "O QUE VOCÊ SENTE PELO(A) PARCEIRO(A), SEU CORAÇÃO"
        elif numero[0] == 2: r = "SUA ATRAÇÃO FÍSICA PELO(A) PARCEIRO(A), SEU TESÃO"
        elif numero[0] == 3: r = Fore.YELLOW + "\nPARCEIRO(A):" + Fore.MAGENTA + "\nO QUE ELE PENSA SOBRE O RELACIONAMENTO"
        elif numero[0] == 4: r = "O QUE ELE(A) SENTE POR VOCÊ, O CORAÇÃO DELE(A)"
        elif numero[0] == 5: r = "A ATRAÇÃO DELE(A) POR VOCÊ, O TESÃO DELE(A)"
        else: r = "\nSÍNTESE, PROGNÓSTICO DA RELAÇÃO"

        print(Fore.MAGENTA + "{}:" .format(r) + Fore.RESET + " {}" .format(carta))

    encerrar_jogo(connection)