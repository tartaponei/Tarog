import random
import functions

"""
1 - Arcano Espelho
2- ELementos Desarmonizados
3- Mandala de 3
4- Mandala de 5
5- Cruz Celta
6- Sair
"""

opcao = 1

while opcao != 6:
    print("\nBem-vindo ao Tarog!\nEscolha um método:")
    print("\n1 - Arcano Espelho\n2- Elementos Desarmonizados\n3- Mandala de 3\n4- Mandala de 5\n5- Cruz Celta\n6- Sair")
    opcao = int(input("Digite o número: "))

    if opcao == 1:
        functions.arcano_espelho()
    elif opcao == 2:
        functions.elementos()
    elif opcao == 3:
        functions.mandala_tres()
    elif opcao == 4:
        functions.mandala_cinco()
    elif opcao == 5:
        functions.cruz_celta()
