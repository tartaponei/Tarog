import cards
import sqlite3
from random import choice, shuffle, randint, sample

def comecar_jogo():
    connection = sqlite3.connect("database.db")
    return connection

def encerrar_jogo(connection):
    """Encerramento do jogo, só pra ficar bonito"""
    connection.close()
    input("\nFim do jogo.\nAperte Enter para continuar...")

##

def jogo_personalizado():
    """Joga um jogo personalizado, com número de cartas e quais Arcanos usar personalizados."""

    connection = comecar_jogo()

    n_cartas = int(input("\nDigite o número de cartas que você quer tirar: "))

    if n_cartas == 1: n = "CARTA"
    else: n = "CARTAS"
    
    print("\nEscolha quais cartas você quer usar:\n1- TODOS OS 78 ARCANOS\n2- SÓ ARCANOS MAIORES (22)\n3- SÓ ARCANOS MENORES (56)\n4- SÓ ARCANOS MENORES NUMERADOS (40)\n5- SÓ A CORTE (16)\n6- ARCANOS MAIORES + ARCANOS MENORES NUMERADOS (62)")
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
    print("\n----> JOGO DE {} {}, USANDO {}:\n" .format(n_cartas, n, jogo))

    for i in range(n_cartas):
        carta = cartas[0]
        cartas.pop(0) #exclui a carta tirada do maço

        print("CASA {}: {}" .format(i+1, carta))

    encerrar_jogo(connection)

def arcano_espelho():
    """Método de Arcano Espelho.
    1 Arcano Maior que é um espelho energético diário ou semanal de quem tira a carta, e indica como vai ser seu dia/semana e como agir.
    Autoconhecimento diário. Usuário mentaliza se quer saber do dia ou da semana."""

    connection = comecar_jogo()

    n = str(randint(1, 23))

    for linha in connection.execute("SELECT DISTINCT nome FROM cartas WHERE id = ?", (n,)):
        carta = linha[0]

    print("\nSeu Arcano Espelho de hoje/semana é: ", carta)
    encerrar_jogo(connection)

def elementos():
    """Método pra ver quais aspectos seus estão desarmonizados.
    4 Arcanos Menores cujos naipes indicam quais aspectos (elementos) de quem tira a carta precisam ser harmonizados novamente.
    Espadas = Mental, Copas = Emocional, Paus = Espiritual, Ouros = Físico"""

    connection = comecar_jogo()

    print("\nAs cartas que saíram são (veja os naipes apenas):")

    for linha in connection.execute("SELECT nome FROM cartas INNER JOIN tipos ON tipos.id = cartas.tipo_id WHERE tipos.grandeza = 'menor' ORDER BY RANDOM() LIMIT 4"):
        print(linha[0])

    encerrar_jogo(connection)

def mandala_tres():
    """Método Mandala de 3.
    3 Arcanos que representam, respecitivamente, Passado ou Causa, Presente ou Situação Atual, e Futuro ou Consequência.
    Para perguntas objetivas de sim ou não e bem formuladas."""

    connection = comecar_jogo()

    print("MANDALA DE 3\n")

    for linha in enumerate(connection.execute("SELECT nome FROM cartas ORDER BY RANDOM() LIMIT 3")):
        carta = linha[1][0]

        if linha[0] == 0: r = "Causa"
        elif linha[0] == 1: r = "Situação"
        else: r = "Consequência"

        print("{}: {}" .format(r, carta))

    encerrar_jogo(connection)

def mandala_cinco():
    """Método Manda de 5.
    5 Arcanos que representam, respecitvamente, Situação Atual, Influência Externa, Oposição, Favorecimento e Resultado. Uma 6ª carta pode ser tirada como Mensagem.
    Para perguntas objetivas e bem formuladas."""

    connection = comecar_jogo()

    print("MANDALA DE 5:\n")

    for linha in enumerate(connection.execute("SELECT nome FROM cartas ORDER BY RANDOM() LIMIT 6")):
        if linha[0] < 5:
            carta = linha[1][0]

            if linha[0] == 0: r = "Situação"
            elif linha[0] == 1: r = "Influência Externa"
            elif linha[0] == 2: r = "Oposição"
            elif linha[0] == 3: r = "Favorecimento"
            elif linha[0] == 4: r = "Resultado"

            print("{}: {}" .format(r, carta))

        else:
            resp = ""
            while resp != "não" and resp != "sim":
                resp = input("\nDeseja tirar uma Mensagem? ")

            if resp == "sim":
                msg = linha[1][0]
                print("\nMensagem: ", msg)

    encerrar_jogo(connection)

def cruz_celta():
    """Método Cruz Celta.
    10 Arcanos que representam, respectivamente, Situação Presente, Influência Imediata, Consulente Perante o Problema, Determinações do Passado, O Que o Consulente Não Conhece, Influências do Futuro, Consulente, Fatores Ambientais, Caminho do Destino, e Resultado Final.
    Para perguntas bem formuladas, mas apresenta mais detalhes."""

    connection = comecar_jogo()

    print("\nCRUZ CELTA\n")

    for linha in enumerate(connection.execute("SELECT nome FROM cartas ORDER BY RANDOM() LIMIT 10")):
        carta = linha[1][0]

        if linha[0] == 0: r = "Situação (Pessoa ou atmosfera espiritual)"
        elif linha[0] == 1: r = "Influência Imediata"
        elif linha[0] == 2: r = "Consulente Perante o Problema"
        elif linha[0] == 3: r = "Passado"
        elif linha[0] == 4: r = "Consulente Não Sabe"
        elif linha[0] == 5: r = "Futuro que vai influenciar"
        elif linha[0] == 6: r = "Representação do Consulente"
        elif linha[0] == 7: r = "Fatores Ambientais (Casa 1)"
        elif linha[0] == 8: r = "Caminho para o sucesso"
        else: r = "Resultado Final"

        print("{}: {}" .format(r, carta))

    encerrar_jogo(connection)

def taca_amor():
    """Método A Taça do Amor.
    7 Arcanos que representam, respectivamente, Como Está O Relacionamento, Consulente Na Situação, Parceiro Na Situação, O Que Favorece O Relacionamento, O Que Não Favorece O Relacionamento, Futuro Próximo da Relação, e Conselho Final.
    Para perguntas sobre amor e relacionamentos."""

    connection = comecar_jogo()
    print("\nTAÇA DO AMOR\n")

    for linha in enumerate(connection.execute("SELECT nome FROM cartas ORDER BY RANDOM() LIMIT 7")):
        carta = linha[1][0]

        if linha[0] == 0: r = "Como Está o Relacionamento"
        elif linha[0] == 1: r = "Consulente Nessa Situação"
        elif linha[0] == 2: r = "Parceiro Nessa Situação"
        elif linha[0] == 3: r = "Favorece o Relacionamento"
        elif linha[0] == 4: r = "Não Favorece o Relacionamento"
        elif linha[0] == 5: r = "Futuro Próximo da Relação"
        else: r = "Conselho Final"

        print("{}: {}" .format(r, carta))

    encerrar_jogo(connection)

def templo_afrodite():
    """Método Templo de Afrodite.
    7 Arcanos que representam, respectivamente, áreas Mental, Sentimental e Física de quem tira as cartas (1, 2, 3), áreas Mental, Sentimental e Física do(a) parceiro(a) (4, 5, 6) e a Síntese do Relacionamento (Prognóstico).
    Para questões sobre estado e situação de um relacionamento."""

    connection = comecar_jogo()

    print("\nTEMPLO DE AFRODITE\n")

    for linha in enumerate(connection.execute("SELECT nome FROM cartas ORDER BY RANDOM() LIMIT 7")):
        carta = linha[1][0]

        if linha[0] == 0: r = "VOCÊ:\nO Que Você Pensa Sobre Relacionamento"
        elif linha[0] == 1: r = "O Que Você Sente Pelo(a) Parceiro(a), Seu Coração"
        elif linha[0] == 2: r = "Sua Atração Física Pelo(a) Parceiro(a), Seu Tesão"
        elif linha[0] == 3: r = "\nPARCEIRO(A):\nO Que Ele Pensa Sobre Relacionamento"
        elif linha[0] == 4: r = "O Que Ele(a) Sente Por Você, O Coração Dele"
        elif linha[0] == 5: r = "A Atração Dele(a) Por Você, O Tesão Dele"
        else: r = "\nSíntese, Prognóstico da Relação"

        print("{}: {}" .format(r, carta))

    encerrar_jogo(connection)