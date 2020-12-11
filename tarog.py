import random
import functions

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
    print("\n0- Sair\n1 - Arcano Espelho (1 carta)\n2- Jogo Personalizado\n3- Elementos Desarmonizados (4 cartas)\n4- Mandala de 3 (3 cartas)\n5- Mandala de 5 (5 / 6 cartas)\n6- Cruz Celta (10 cartas)\n7- Taça do Amor (7 cartas)\n8- Templo de Afrodite (7 cartas)")
    opcao = int(input("Digite o número: "))

    if opcao == 1:
        functions.arcano_espelho()
    elif opcao == 2:
        functions.jogo_personalizado()
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
    else:
        pass
