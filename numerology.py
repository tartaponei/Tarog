import sqlite3
from colorama import init, Fore

init(autoreset=True)

MAIORES = range(0, 22)

def comecar_jogo(personalizado=None):
    """Começo do jogo. Abertura da conexão com o banco"""

    connection = sqlite3.connect("database.db")
    return connection

def encerrar_jogo(connection):
    """Encerramento do jogo, fechamento da conexão com o banco."""

    connection.close()
    input("\nFim do jogo.\nAperte Enter para continuar...")

##

def reducao_teosofica(soma):
    """
    Faz redução teosófica (soma os algarismos).
    """
    soma_s = str(soma)
    soma = 0

    for algarismo in soma_s:
        soma += int(algarismo)

    return soma

def checar_nome():
    """
    Faz o somatório dos valores das letras do nome.
    """

    nome = input("\nDigite seu nome completo (atenção para escrever tudo corretamente): ")
    nome = nome.lower() #coloca tudo minúsculo
    soma = 0

    for letra in nome:
        if letra == "a" or letra == "i" or letra == "q" or letra == "j" or letra == "y": soma += 1
        elif letra == "b" or letra == "k" or letra == "r" or letra == "\'" or letra == "à" or letra == "ì" or letra == "ä" or letra == "ï": soma += 2
        elif letra == "c" or letra == "g" or letra == "l" or letra == "s" or letra == "á" or letra == "í": soma += 3
        elif letra == "d" or letra == "m" or letra == "t": soma += 4
        elif letra == "e" or letra == "h" or letra == "n": soma += 5
        elif letra == "u" or letra == "v" or letra == "w" or letra == "x" or letra == "ç": soma += 6
        elif letra == "o" or letra == "z" or letra == "é": soma += 7
        elif letra == "f" or letra == "p" or letra == "ú" or letra == "â" or letra == "î" or letra == "å": soma += 8
        elif letra == "ó": soma += 9
        elif letra == "è" or letra == "ë": soma += 5*2
        elif letra == "ò" or letra == "ö" or letra == "ô": soma += 7*2
        elif letra == "ù" or letra == "ü": soma += 6*2
        elif letra == "ê": soma += 5+7
        elif letra == "û": soma += 6+7

    while soma > 22:
        soma = reducao_teosofica(soma)
        
    return soma

def checar_data(get_dia=None):
    ano = input("\nDigite o ANO que você nasceu (AAAA): ")
    mes = input("Digite o número do MÊS que você nasceu (ex.: se for Março, digite 3): ")
    dia = input("Digite agora o DIA do nascimento: ")

    data = dia + mes + ano
    soma = 0

    for algarismo in data:
        soma += int(algarismo)

    while soma > 22:
        soma = reducao_teosofica(soma)
    
    if get_dia: return soma, dia
    else: return soma

##

def arcano_pessoal(n_nome=None, conn=None):
    if n_nome and conn: 
        num = str(n_nome) #se já tiver calculado
        connection = conn
    else:
        print(Fore.GREEN + "\n--> ARCANO PESSOAL (SUAS TENDÊNCIAS) <--")
        num = checar_nome() #se não tiver
        connection = comecar_jogo()

    if num == 22: #se for O louco
        num = 0

    for linha in connection.execute("SELECT nome FROM cartas INNER JOIN tipos ON tipos.id = cartas.tipo_id WHERE tipos.grandeza = 'maior' AND cartas.valor = ?", [str(num)]):
        carta = linha[0]

    print(Fore.GREEN + "\nARCANO PESSOAL (SUAS TENDÊNCIAS): " + Fore.RESET + carta)
    
    if not n_nome: encerrar_jogo(connection)

def missao_vida(n_data=None, conn=None):
    if n_data and conn:
        num = str(n_data) #se já tiver calculado
        connection = conn
    else:
        print(Fore.BLUE + "\n--> MISSÃO DE VIDA <--\n")
        num = checar_data() #se não tiver
        connection = comecar_jogo()

    if num == 22: #se for O louco
        num = 0

    connection = comecar_jogo()

    for linha in connection.execute("SELECT nome FROM cartas INNER JOIN tipos ON tipos.id = cartas.tipo_id WHERE tipos.grandeza = 'maior' AND cartas.valor = ?", [str(num)]):
        carta = linha[0]

    print(Fore.BLUE + "MISSÃO DE VIDA: " + Fore.RESET + carta)
    
    if not n_data: encerrar_jogo(connection)

def dons_passados(n_nome=None, n_data=None, conn=None):
    if n_nome and n_data and conn:
        num_missao = str(n_nome) + str(n_data) #se já tiver calculado
        connection = conn
    else:
        print(Fore.CYAN + "\n--> DONS DE VIDAS PASSADAS <--\n")
        num_missao = str(checar_nome()) + str(checar_data()) #se não tiver
        connection = comecar_jogo()

    soma = 0

    for algarismo in num_missao:
        soma += int(algarismo)

    connection = comecar_jogo()
    
    for linha in connection.execute("SELECT nome FROM cartas INNER JOIN tipos ON tipos.id = cartas.tipo_id WHERE tipos.grandeza = 'maior' AND cartas.valor = ?", [str(soma)]):
        carta = linha[0]

    print(Fore.CYAN + "DONS DE VIDAS PASSADAS: " + Fore.RESET + carta)
    
    if not n_nome and not n_data: encerrar_jogo(connection)

def espelho(n_dia=None, conn=None):
    if n_dia and conn:
        num = str(n_dia) #se já tiver calculado
        connection = conn
    else:
        print(Fore.MAGENTA + "\n--> ESPELHO (PRIMEIRA IMPRESSÃO QUE AS PESSOAS TÊM DE VOCÊ) <--\n")
        num = input("\nDigite o dia do seu nascimento (ex.: se nasceu em 12/03/2002, digite 12): ")
        connection = comecar_jogo()

    while int(num) > 22:
        num = reducao_teosofica(num)

    connection = comecar_jogo()
    
    for linha in connection.execute("SELECT nome FROM cartas INNER JOIN tipos ON tipos.id = cartas.tipo_id WHERE tipos.grandeza = 'maior' AND cartas.valor = ?", [str(num)]):
        carta = linha[0]

    print(Fore.MAGENTA + "ESPELHO (PRIMEIRA IMPRESSÃO QUE AS PESSOAS TÊM DE VOCÊ): " + Fore.RESET + carta)
    
    if not n_dia: encerrar_jogo(connection)
    
def num_completa():
    connection = comecar_jogo()

    num_nome = checar_nome()
    num_data, dia = checar_data(get_dia=True)

    arcano_pessoal(n_nome=num_nome, conn=connection)
    missao_vida(n_data=num_data, conn=connection)
    dons_passados(n_nome=num_nome, n_data=num_data, conn=connection)
    espelho(n_dia=dia, conn=connection)

    encerrar_jogo(connection)