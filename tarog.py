import functions
from colorama import init, Style, Fore

init(autoreset=True)

"""
0- Sair
1 - Arcano Espelho
2- ELementos Desarmonizados
3- Mandala de 3
4- Mandala de 5
5- Cruz Celta
6- Taça do Amor
"""

opcao = 1

print("\nBem-vindo ao Tarog!")

while opcao != 0:
    print("\nEscolha um método:")
    print(Fore.RED + "\n0- Sair\n" + Fore.CYAN + "1 - Jogo Personalizado\n" + Fore.GREEN + "2- Arcano Espelho (1 carta)\n3- Elementos Desarmonizados (4 cartas)\n" + Fore.YELLOW + "4- Mandala de 3 (3 cartas)\n5- Mandala de 5 (5 / 6 cartas)\n" + Fore.BLUE + "6- Cruz Celta (10 cartas)\n" + Fore.MAGENTA + "7- Taça do Amor (7 cartas)\n8- Templo de Afrodite (7 cartas)\n" + Fore.GREEN + "9- Caráter (4 cartas)")
    opcao = int(input("\nDigite o número: "))

    if opcao == 1:
        functions.jogo_personalizado()
    elif opcao == 2:
        functions.arcano_espelho()
    elif opcao == 3:
        functions.elementos()
    elif opcao == 4:
        functions.mandala_tres()
    elif opcao == 5:
        functions.mandala_cinco()
    elif opcao == 6:
        functions.cruz_celta()
    elif opcao == 7:
        functions.taca_amor()
    elif opcao == 8:
        functions.templo_afrodite()
    elif opcao == 9:
        functions.carater()
    else:
        pass
