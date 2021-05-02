#scripts
import tarot
import numerology
import lenormand
import pythagorean

#packages
import sqlite3
import cfonts
from time import sleep
from PIL import Image
from io import BytesIO
from terminaltables import SingleTable
from colorama import init, Style, Fore

init(autoreset=True)

#variáveis iniciais
TITLE = cfonts.render("-TAROG-", font='block', size=(80, 40), colors=("magenta", "yellow"), background='transparent', align='left', letter_spacing=None, line_height=1, space=True, max_length=0, gradient=None, independent_gradient=False, transition=False)

WELCOME_TEXT = Fore.YELLOW + "======> BEM VINDO! <======"

EXIT_TEXT = cfonts.render("OBRIGADA POR USAR :)", font='chrome', size=(80, 40), colors=("magenta", "magenta", "magenta"), background='transparent', align='left', letter_spacing=None, line_height=1, space=True, max_length=0, gradient=None, independent_gradient=False, transition=False)
"""
0- Sair
1- Jogar Tarô
2- Jogar Baralho Cigano (Lenormand)
3- Ver Jogos Salvos

4- Numerologia Pelo Tarô
5- Numerologia Pitagórica
"""

"""
0- Sair
1- Jogo Personalizado
2- Arcano Espelho / Sim ou Não
3- Carta e Conselho do Dia
4- Elementos Desarmonizados
5- Espiritualidade
6- Estrela (Eu com Eu Mesmo)

7- Mandala de 3
8- Mandala de 5
9- Peladán
10- Cruz Celta
11- Tiragem de 5 Cartas (Solução de Problemas)
12- Tiragem de 7 Cartas (Entendimento do Presente)

13- Templo de Afrodite
14- Taça do Amor

15- Caráter
16- 7 Chaves
"""

"""
0- Sair
1- Jogo Personalizado
2- Mesa Real
3- Sim ou Não / Carta do Dia
4- Carta e Conselho do Dia
5- Passado, Presente e Futuro
6- Tiragem de 5 Cartas (Solução de Problemas)
7- Tiragem de 7 Cartas (Entendimento do Presente)
"""

"""
0- Sair
1- Numerologia Completa
2- Arcano Pessoal (Suas Tendências)
3- Missão de Vida
4- Dons de Outras Vidas
5- Espelho (Primeira Impressão Que Passa)
"""

def escolher_baralho():
    opcao_baralho = 0

    while opcao_baralho != 1 and opcao_baralho != 2:
        print("\nEscolha o baralho:\n" + Fore.YELLOW + "\n1- Tarô\n" + Fore.CYAN + "2- Lenormand (Baralho Cigano)\n")
        opcao_baralho = int(input("Digite o número: "))
    
    return opcao_baralho

def apres_jogo():
    return int(input("\nDigite " + Fore.GREEN + "1 se quiser continuar com este método" + Fore.WHITE + " ou " + Fore.RED + "0 se quiser voltar" + Fore.RESET +": "))

def criar_tabela_jogo():
    open("jogos_db.db", "a") #cria o arquivo caso não tenha

    f_conn = sqlite3.connect("jogos_db.db")
    f_conn.execute('CREATE TABLE IF NOT EXISTS "jogos" ("id" INTEGER NOT NULL, "pergunta" TEXT(300) NOT NULL, "data" TEXT(10) NOT NULL, "hora" TEXT(5) NOT NULL, "cartas" TEXT,"mesa" BLOB, PRIMARY KEY("id" AUTOINCREMENT));')

def main():
    criar_tabela_jogo()
    print("\'")

    opcao1 = 1

    print(TITLE) ; sleep(1)
    print(WELCOME_TEXT) ; sleep(1)

    #print(Fore.MAGENTA + "\n>> BEM-VINDO AO TAROG! <<")

    while opcao1 != 0:
        print("\nEscolha o que deseja fazer:")
        print(Fore.RED + "\n0- Sair" + Fore.CYAN + "\n1- Jogar Cartas" + Fore.YELLOW + "\n2- Ver Jogos Salvos" + Fore.BLUE + "\n\n3- Numerologia Pelo Tarô" + Fore.MAGENTA + "\n4- Numerologia Pitagórica")
        opcao1 = int(input("\nDigite o número: "))

        if opcao1 == 1: #tarô ou baralho
            opcao = 1
            while opcao != 0:
                print("\nEscolha um método:")
                print(Fore.RED + "\n0- Voltar\n" + Fore.CYAN + "1 - Jogo Personalizado\n" + Fore.GREEN + "\n2- Arcano Espelho / Sim ou Não (1 carta) \n3- Carta e Conselho do Dia (2 cartas) \n4- Elementos Desarmonizados (4 cartas - Somente com Tarô)\n5- Espiritualidade (7 cartas) \n6- Estrela / Eu Com Eu Mesmo (6 cartas)\n" + Fore.YELLOW + "\n7- Mandala de 3 (3 cartas) \n8- Mandala de 5 (6 cartas) \n9- Peladán (5 cartas) \n10- Cruz Celta (10 cartas)\n11- Tiragem de 5 Cartas (Solução de Problemas) \n12- Tiragem de 7 Cartas (Entendimento do Presente)\n" + Fore.MAGENTA + "\n13- Templo de Afrodite (7 cartas) \n14- Taça do Amor (7 cartas)\n" + Fore.BLUE + "\n15- Caráter (4 cartas) \n16- 7 Chaves (7 cartas)")
                opcao = int(input("\nDigite o número: "))

                if opcao == 0: opcao1 = 1

                elif opcao == 1: #personalizado
                    print(Fore.CYAN + "\n-> Joga um jogo personalizado, com número de cartas e quais Arcanos usar personalizados.")
                    a = apres_jogo()

                    if a == 1:
                        opcao_baralho = escolher_baralho()

                        if opcao_baralho == 1:
                            tarot.jogo_personalizado(tarot=True)
                        elif opcao_baralho == 2:
                            tarot.jogo_personalizado(lenormand=True)

                elif opcao == 2: #espelho
                    print(Fore.GREEN + "\n-> 1 carta que é um espelho energético diário ou semanal de quem tira a carta,\ne indica como vai ser seu dia/semana e como agir, ou então uma resposta \nobjetiva de sim ou não.")
                    a = apres_jogo()

                    if a == 1:
                        opcao_baralho = escolher_baralho()
                            
                        if opcao_baralho == 1:
                            tarot.arcano_espelho(tarot=True)
                        elif opcao_baralho == 2:
                            tarot.arcano_espelho(lenormand=True)

                elif opcao == 3: #carta e conselho
                    print(Fore.GREEN + "\n-> 2 cartas que mostram, respectivamente, a Energia geral do dia e o \nConselho para o dia (o que fazer ou o que não fazer).")
                    a = apres_jogo()

                    if a == 1:
                        opcao_baralho = escolher_baralho()
                            
                        if opcao_baralho == 1:
                            tarot.conselho(tarot=True)
                        elif opcao_baralho == 2:
                            tarot.conselho(lenormand=True)

                elif opcao == 4: #elementos
                    print(Fore.GREEN + "\n-> Método pra ver quais aspectos seus estão desarmonizados. 4 Arcanos Menores cujos naipes \nindicam quais aspectos (elementos) de quem tira a carta precisam ser harmonizados novamente. \nEspadas = Mental, Copas = Emocional, Paus = Espiritual, Ouros = Físico")
                    a = apres_jogo()

                    if a == 1: tarot.elementos()

                elif opcao == 5: #espiritualidade // NÂO FEITO!!!!!
                    print(Fore.YELLOW + "\n-> 7 cartas que mostram nossa conexão com a espiritualdiade através dos chakras. \nCréditos ao querdiíssimo Wayner Lyra.")
                    a = apres_jogo()

                    if a == 1:
                        opcao_baralho = escolher_baralho()
                            
                        if opcao_baralho == 1:
                            tarot.espiritualidade(tarot=True)
                        elif opcao_baralho == 2:
                            tarot.espiritualidade(lenormand=True)

                elif opcao == 7: #mandala de 3
                    print(Fore.YELLOW + "\n-> 3 cartas que podem ser lidas de forma linear, \ncomo Passado - Presente - Futuro ou Causa - Situação - Consequência")
                    a = apres_jogo()

                    if a == 1:
                        opcao_baralho = escolher_baralho()
                            
                        if opcao_baralho == 1:
                            tarot.mandala_tres(tarot=True)
                        elif opcao_baralho == 2:
                            tarot.mandala_tres(lenormand=True)

                elif opcao == 8: #mandala de 5
                    print(Fore.YELLOW + "\n-> 6 Arcanos que representam, respecitvamente, Situação Atual, Influência Externa, Oposição,\n Favorecimento, Resultado e Conselho. Para perguntas objetivas e bem formuladas.")
                    a = apres_jogo()

                    if a == 1:
                        opcao_baralho = escolher_baralho()
                            
                        if opcao_baralho == 1:
                            tarot.mandala_cinco(tarot=True)
                        elif opcao_baralho == 2:
                            tarot.mandala_cinco(lenormand=True)

                elif opcao == 10: #cruz celta
                    print(Fore.YELLOW + "\n-> 10 cartas para uma visão geral da situação. \nPara perguntas bem formuladas, mas apresenta mais detalhes.")
                    a = apres_jogo()

                    if a == 1:
                        opcao_baralho = escolher_baralho()
                            
                        if opcao_baralho == 1:
                            tarot.cruz_celta(tarot=True)
                        elif opcao_baralho == 2:
                            tarot.cruz_celta(lenormand=True)

                elif opcao == 11: #5 cartas
                    print(Fore.YELLOW + "\n-> 5 cartas para resolução de problemas, tal como a \nMandala de 3 com complementos a mais.")
                    a = apres_jogo()

                    if a == 1:
                        opcao_baralho = escolher_baralho()
                            
                        if opcao_baralho == 1:
                            tarot.cinco_cartas(tarot=True)
                        elif opcao_baralho == 2:
                            tarot.cinco_cartas(lenormand=True)

                elif opcao == 12: #7 cartas
                    print(Fore.YELLOW + "\n-> 7 cartas para visão panorâmica de problemas, tal como o \nmétodo de 5 cartas com complementos a mais.")
                    a = apres_jogo()

                    if a == 1:
                        opcao_baralho = escolher_baralho()
                            
                        if opcao_baralho == 1:
                            tarot.sete_cartas(tarot=True)
                        elif opcao_baralho == 2:
                            tarot.sete_cartas(lenormand=True)

                elif opcao == 14: #taça do amor
                    print(Fore.MAGENTA + "\n-> 7 cartas para uma visão geral sobre um relacionamento amoroso.")
                    a = apres_jogo()

                    if a == 1: 
                        opcao_baralho = escolher_baralho()
                            
                        if opcao_baralho == 1:
                            tarot.taca_amor(tarot=True)
                        elif opcao_baralho == 2:
                            tarot.taca_amor(lenormand=True)

                elif opcao == 13: #templo de afrodite
                    print(Fore.MAGENTA + "\n-> 7 Arcanos que representam, respectivamente, áreas Mental, Sentimental e Física de quem tira as cartas (1, 2, 3), \náreas Mental, Sentimental e Física do(a) parceiro(a) (4, 5, 6) e a Síntese do Relacionamento (Prognóstico). \nPara questões sobre estado e situação de um relacionamento.")
                    a = apres_jogo()

                    if a == 1:
                        opcao_baralho = escolher_baralho()
                            
                        if opcao_baralho == 1:
                            tarot.templo_afrodite(tarot=True)
                        elif opcao_baralho == 2:
                            tarot.templo_afrodite(lenormand=True)

                elif opcao == 15: #caráter
                    print(Fore.GREEN + "\n-> 4 Arcanos que representam, respectivamente, a Persona da pessoa em questão (o que ela mostra ser, \na 'máscara'), a Personalidade (o que ela é realmente e não mostra), as Motivações (o que a leva a agir desse jeito) \ne as Intenções (o que ela realmente quer de você). Para saber sobre as intenções de alguém que você talvez desconfie, \nsaber o que ela quer com você.")
                    a = apres_jogo()

                    if a == 1:
                        opcao_baralho = escolher_baralho()
                            
                        if opcao_baralho == 1:
                            tarot.carater(tarot=True)
                        elif opcao_baralho == 2:
                            tarot.carater(lenormand=True)

                elif opcao == 9: #peladan
                    print(Fore.YELLOW + "\n-> 5 Arcanos que representam, respecitvamente, Positivo, Negativo, Caminho, Resultado e \nSíntese/Consulente. Para perguntas objetivas, bem formuladas e com tempo determinado.")
                    a = apres_jogo()

                    if a == 1:
                        opcao_baralho = escolher_baralho()
                            
                        if opcao_baralho == 1:
                            tarot.peladan(tarot=True)
                        elif opcao_baralho == 2:
                            tarot.peladan(lenormand=True)

                elif opcao == 16: #7 chaves
                    print(Fore.YELLOW + "\n-> 7 Arcanos para analisar a fundo alguma magia, feitiço ou amarração feita. \nA magia precisa ter sido confirmada através de outro jogo ou método antes deste método. Créditos ao queridíssimo Wayner Lyra.")
                    a = apres_jogo()

                    if a == 1:
                        opcao_baralho = escolher_baralho()
                            
                        if opcao_baralho == 1:
                            tarot.sete_chaves(tarot=True)
                        elif opcao_baralho == 2:
                            tarot.sete_chaves(lenormand=True)

                elif opcao == 6: #estrela
                    print(Fore.GREEN + "\n-> 6 Arcanos para vermos como estamos, como anda nosso relacionamento com nós mesmos. \nCréditos ao queridíssimo Wayner Lyra.")
                    a = apres_jogo()

                    if a == 1: 
                        opcao_baralho = escolher_baralho()
                            
                        if opcao_baralho == 1:
                            tarot.estrela(tarot=True)
                        elif opcao_baralho == 2:
                            tarot.estrela(lenormand=True)
                
                else: pass

        elif opcao1 == 3: #numerologia pelo tarô
            opcao = 1
            while opcao != 0:
                print("\nEscolha o que deseja ver:")
                print(Fore.RED + "\n0- Voltar\n" + Fore.YELLOW + "1- Numerologia Completa\n" + Fore.GREEN + "2- Arcano Pessoal (Suas Tendências)\n" + Fore.BLUE + "3- Missão de Vida\n" + Fore.CYAN + "4- Dons de Vidas Passadas\n" + Fore.MAGENTA + "5- Espelho (Primeira Impressão Que Passa)")
                opcao = int(input("\nDigite o número: "))

                if opcao == 0: opcao1 = 1
                elif opcao == 1: numerology.num_completa()
                elif opcao == 2: numerology.arcano_pessoal()
                elif opcao == 3: numerology.missao_vida()
                elif opcao == 4: numerology.dons_passados()
                elif opcao == 5: numerology.espelho()
                else: pass

        elif opcao1 == 2: #jogos salvos
            print(Fore.MAGENTA + "\n--> ESSES SÃO OS JOGOS SALVOS:")
            loop = 1

            while loop == 1:
                tabledata = [["NUM", "PERGUNTA", "QUANDO"]]

                connection = sqlite3.connect("jogos_db.db")
                c = connection.cursor()

                for jogo in c.execute("SELECT pergunta, data, hora, id FROM jogos"):
                    #print("%d - \"%s\" | DIA %s, ÀS %s" %(num, jogo[0], jogo[1], jogo[2]))
                    tabledata.append([jogo[3], "\"%s\"" %(jogo[0]), "DIA %s, ÀS %s" %(jogo[1], jogo[2])])

                tabela = SingleTable(tabledata)
                tabela.inner_row_border = True
                tabela.justify_columns = {0: 'right', 1: 'left', 2: 'center'}
                print(tabela.table)

                resp = int(input("\nDigite o " + Fore.GREEN + "número do jogo que quer ver" + Fore.WHITE + ", ou " + Fore.RED + "0 se quiser voltar" + Fore.RESET + ": "))

                if resp != 0:
                    #try:
                    jogow = connection.execute("SELECT pergunta, data, hora, mesa, cartas FROM jogos WHERE id = ?", (str(resp),))
                    #except:
                        #print("Não tem jogo com esse número. Digite outro.\n")
                    jogo = jogow.fetchone()
                        
                    print(Fore.MAGENTA + "\nPERGUNTA:", jogo[0])
                    print(Fore.MAGENTA + "DATA:", jogo[1])
                    print(Fore.MAGENTA + "HORA:", jogo[2])

                    cartas = str(jogo[4])[:-3]
                    cartas = cartas.split(" | ")

                    print(Fore.BLUE + "\n--> JOGO: <--")
                    for carta in cartas:
                        print(carta)

                    if jogo[3]:
                        corrected = [256+x if int(x)<0 else x for x in jogo[3]]

                        img = Image.open(BytesIO(bytes(corrected)))
                        img.show()

                    connection.close()
                    input("\nAperte Enter para voltar para o menu...")
                loop = 0

        elif opcao1 == 4: #numerologia pitagórica
            pythagorean.numerologia()
    #se a pessoa quiser sair do prog
    print(EXIT_TEXT)

if __name__ == "__main__":
    main()