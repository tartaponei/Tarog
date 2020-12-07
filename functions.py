import cards
from random import choice

def arcano_espelho():
    carta = choice(cards.major) #pega um arcano maior aleatório

    print("\nSeu Arcano Espelho de hoje é: ", carta)

def elementos():
    cartas = cards.numbered[0:]
    print("\nAs cartas que saíram são (veja os naipes apenas):")

    for i in range(4):
        carta = choice(cartas)
        cartas.remove(carta)
        print(carta)

def mandala_tres():
    cartas = cards.cards[0:]
    print("\n")

    for i in range(3):
        carta = choice(cartas)
        cartas.remove(carta)

        if i == 0: r = "Causa"
        elif i == 1: r = "Situação"
        else: r = "Consequência"

        print("{}: {}" .format(r, carta))

def mandala_cinco():
    cartas = cards.cards[0:]
    print("\n")

    for i in range(5):
        carta = choice(cartas)
        cartas.remove(carta)

        if i == 0: r = "Situação"
        elif i == 1: r = "Influência Externa"
        elif i == 2: r = "Oposição"
        elif i == 3: r = "Favorecimento"
        else: r = "Resultado"

        print("{}: {}" .format(r, carta))

    resp = input("\nDeseja tirar uma Mensagem? ")

    if resp == "sim":
        msg = choice(cartas)
        print("\nMensagem: ", msg)

def cruz_celta():
    cartas = cards.cards[0:]
    print("\n")

    for i in range(10):
        carta = choice(cartas)
        cartas.remove(carta)

        if i == 0: r = "Situação (Pessoa ou atmosfera espiritual)"
        elif i == 1: r = "Influência Imediata"
        elif i == 2: r = "Consulente Perante o Problema"
        elif i == 3: r = "Passado"
        elif i == 4: r = "Consulente Não Sabe"
        elif i == 5: r = "Futuro que vai influenciar"
        elif i == 6: r = "Representação do Consulente"
        elif i == 7: r = "Fatores Ambientais (Casa 1)"
        elif i == 8: r = "Caminho para o sucesso"
        else: r = "Resultado Final"

        print("{}: {}" .format(r, carta))