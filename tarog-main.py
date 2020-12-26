import tarot
import numerology
from colorama import init, Style, Fore

init(autoreset=True)

"""
0- Sair
1- Jogar Tarô
2- Numerologia Pelo Tarô
"""

"""
0- Sair
1 - Jogo Personalizado
2- Arcano Espelho
3- Elementos Desarmonizados
4- Mandala de 3
5- mandala de 5
6- Cruz Celta
7- Taça do Amor
8- Templo de Afrodite
9- Caráter
10- Peladán
"""

"""
0- Sair
1- Numerologia Completa
2- Arcano Pessoal (Suas Tendências)
3- Missão de Vida
4- Dons de Outras Vidas
5- Espelho (Primeira Impressão Que Passa)
"""

print("\'")

opcao = 1

print("\nBem-vindo ao Tarog!")

while opcao != 0:
    print("\nEscolha o que deseja fazer:")
    print(Fore.RED + "\n0- Sair" + Fore.CYAN + "\n1- Jogar Tarô\n" + Fore.YELLOW + "2- Numerologia Pelo Tarô")
    opcao = int(input("\nDigite o número: "))

    if opcao == 1:
        while opcao != 0:
            print("\nEscolha um método:")
            print(Fore.RED + "\n0- Sair\n" + Fore.CYAN + "1 - Jogo Personalizado\n" + Fore.GREEN + "2- Arcano Espelho (1 carta)\n3- Elementos Desarmonizados (4 cartas)\n" + Fore.YELLOW + "4- Mandala de 3 (3 cartas)\n5- Mandala de 5 (5 / 6 cartas)\n" + Fore.BLUE + "6- Cruz Celta (10 cartas)\n" + Fore.MAGENTA + "7- Taça do Amor (7 cartas)\n8- Templo de Afrodite (7 cartas)\n" + Fore.GREEN + "9- Caráter (4 cartas)\n" + Fore.YELLOW + "10- Peladán (5 cartas)")
            opcao = int(input("\nDigite o número: "))

            if opcao == 1: tarot.jogo_personalizado()
            elif opcao == 2: tarot.arcano_espelho()
            elif opcao == 3: tarot.elementos()
            elif opcao == 4: tarot.mandala_tres()
            elif opcao == 5: tarot.mandala_cinco()
            elif opcao == 6: tarot.cruz_celta()
            elif opcao == 7: tarot.taca_amor()
            elif opcao == 8: tarot.templo_afrodite()
            elif opcao == 9: tarot.carater()
            elif opcao == 10: tarot.peladan()
            else: pass
    else:
        while opcao != 0:
            print("\nEscolha o que deseja ver:")
            print(Fore.RED + "\n0- Sair\n" + Fore.YELLOW + "1- Numerologia Completa\n" + Fore.GREEN + "2- Arcano Pessoal (Suas Tendências)\n" + Fore.BLUE + "3- Missão de Vida\n" + Fore.CYAN + "4- Dons de Vidas Passadas\n" + Fore.MAGENTA + "5- Espelho (Primeira Impressão Que Passa)")
            opcao = int(input("\nDigite o número: "))

            if opcao == 1: numerology.num_completa()
            elif opcao == 2: numerology.arcano_pessoal()
            elif opcao == 3: numerology.missao_vida()
            elif opcao == 4: numerology.dons_passados()
            elif opcao == 5: numerology.espelho()
            else: pass
