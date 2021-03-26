import sqlite3
import os
import io
from PIL import Image
from datetime import date, datetime
from random import shuffle, randint, sample
from colorama import init, Fore

hoje = date.today()

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

def instrucoes(cartas, elementos=False):
    if elementos:
        instrucao = "\nAs cartas serão mostradas na ordem em que foram tiradas do baralho.\nO significado das cartas não será mostrado.\nO que importa neste método é ver os naipes das cartas que saíram:\n\n" + Fore.YELLOW + "Espadas = Área Mental = Ar" + Fore.BLUE + "\nCopas = Área Emocional = Água\n" + Fore.RED + "Paus = Área Espiritual = Fogo\n" + Fore.GREEN + "Ouros = Área Física = Terra\n\n" + Fore.CYAN + "Os naipes que saírem mostram seus aspectos que precisam de atenção a mais, \natente-se a eles e reflita o melhor jeito de harmonizá-los de volta. \nA recomendação é reconexão com seus respectivos elementos representativos, mas procure as soluções com você mesmo.\n\nAntes de continuar, respire fundo algumas vezes, e conecte-se com sua concepção de luz.\nConcentre-se por alguns instantes em pedir para ver quais aspectos seus precisam ser harmonizados e evite sentimentos e pensamentos negativos.\nLembre-se que sua intuição aqui também é importante.\nAs cartas serão embaralhadas assim que você continuar daqui.\nQue neste jogo somente a verdade te seja mostrada."
    elif cartas > 1:
        instrucao = "\nAs cartas serão mostradas de acordo com sua posição no jogo.\nO significado das cartas não será mostrado.\nExercite sua capacidade de olhar cada detalhe das cartas e tirar o significado dos símbolos e desenhos ali mostrados, \nsem se prender em palavras chave e clichês.\nAtente-se a cada posição para saber se a carta está negativa ou positiva, e atente-se também ao contexto do conjunto das cartas e sempre tenha em mente sua pergunta.\n\nAntes de continuar, respire fundo algumas vezes, e conecte-se com sua concepção de luz.\nConcentre-se na pergunta por alguns instantes e evite sentimentos e pensamentos negativos.\nLembre-se que sua intuição aqui também é importante.\nAs cartas serão embaralhadas assim que você continuar daqui.\nQue neste jogo somente a verdade te seja mostrada."
    else:
        instrucao = "\nO significado da carta não será mostrado.\nExercite sua capacidade de olhar cada detalhe da carta e tirar a mensagem dela dos símbolos e desenhos ali mostrados, \nsem se prender em palavras chave e clichês, e sempre tenha em mente sua pergunta ou objetivo.\n\nAntes de continuar, respire fundo algumas vezes, e conecte-se com sua concepção de luz.\nConcentre-se na pergunta ou no contexto (seu dia, semana, etc) por alguns instantes e evite sentimentos e pensamentos negativos.\nLembre-se que sua intuição aqui também é importante.\nAs cartas serão embaralhadas assim que você continuar daqui.\nQue neste jogo somente a verdade te seja mostrada."

    print(Fore.MAGENTA + "\n>> LEIA ANTES DE PROSSEGUIR <<")
    print(Fore.CYAN + instrucao)

    input("\nAperte Enter para continuar...")

def salvar_jogo(cartas, foto=True):
    connection = sqlite3.connect("jogos_db.db")
    print("\nDeseja salvar o jogo feito?")
    s = int(input("\nDigite " + Fore.GREEN + "1 se sim" + Fore.WHITE + " ou " + Fore.RED + "0 se não" + Fore.RESET +": "))

    if s == 1:
        pergunta = input(Fore.GREEN + "\nQual foi a pergunta feita?\n--> " + Fore.RESET)
        data = hoje.strftime("%d-%m-%y")
        hora = datetime.now()
        hora = hora.strftime("%H:%M")
        if foto:
            mesa = convertToBinaryData("./img/jogo.png")
        else:
            mesa = None

        try:
            connection.execute("INSERT INTO 'jogos' ('pergunta', 'data', 'hora', 'mesa', 'cartas') VALUES (?, ?, ?, ?, ?)", (pergunta, str(data), str(hora), mesa, cartas))
            connection.commit()
        except Exception as e:
            print("Erro: ", e)
        else:
            print(Fore.YELLOW + "\n--> Jogo salvo! <--")
    connection.close()

# TRATAMENTO DE FOTOS

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

"""def image_to_byte_array(image:Image):
  imgByteArr = io.BytesIO()
  image.save(imgByteArr, format=image.format)
  imgByteArr = imgByteArr.getvalue()
  return imgByteArr"""

