#scripts
import tarot
import numerology
import lenormand

#packages
import sqlite3
import cfonts
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
3- Numerologia Pelo Tarô
"""

"""
0- Sair
1- Jogo Personalizado
2- Arcano Espelho
3- Elementos Desarmonizados
4- Mandala de 3
5- mandala de 5
6- Cruz Celta
7- Taça do Amor
8- Templo de Afrodite
9- Caráter
10- Peladán
11- 7 Chaves
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

    print(TITLE)
    print(WELCOME_TEXT)

    #print(Fore.MAGENTA + "\n>> BEM-VINDO AO TAROG! <<")

    while opcao1 != 0:
        print("\nEscolha o que deseja fazer:")
        print(Fore.RED + "\n0- Sair" + Fore.CYAN + "\n1- Jogar Tarô" + Fore.GREEN + "\n2- Jogar Baralho Cigano (Lenormand)" + Fore.YELLOW + "\n3- Numerologia Pelo Tarô" + Fore.BLUE + "\n4- Ver Jogos Salvos")
        opcao1 = int(input("\nDigite o número: "))

        if opcao1 == 1: #tarô
            opcao = 1
            while opcao != 0:
                print("\nEscolha um método:")
                print(Fore.RED + "\n0- Voltar\n" + Fore.CYAN + "1 - Jogo Personalizado\n" + Fore.GREEN + "2- Arcano Espelho (1 carta)\n3- Elementos Desarmonizados (4 cartas)\n" + Fore.YELLOW + "4- Mandala de 3 (3 cartas)\n5- Mandala de 5 (6 cartas)\n" + Fore.BLUE + "6- Cruz Celta (10 cartas)\n" + Fore.MAGENTA + "7- Taça do Amor (7 cartas)\n8- Templo de Afrodite (7 cartas)\n" + Fore.GREEN + "9- Caráter (4 cartas)\n" + Fore.YELLOW + "10- Peladán (5 cartas)\n11- 7 Chaves (7 cartas)")
                opcao = int(input("\nDigite o número: "))

                if opcao == 0: opcao1 = 1

                elif opcao == 1:
                    print(Fore.CYAN + "\n-> Joga um jogo personalizado, com número de cartas e quais Arcanos usar personalizados.")
                    a = apres_jogo()

                    if a == 1: tarot.jogo_personalizado()

                elif opcao == 2:
                    print(Fore.GREEN + "\n-> 1 Arcano Maior (ou pode usar o baralho todo) que é um espelho energético diário ou semanal de quem tira a carta,\ne indica como vai ser seu dia/semana e como agir. Autoconhecimento diário.")
                    a = apres_jogo()

                    if a == 1: tarot.arcano_espelho()

                elif opcao == 3:
                    print(Fore.GREEN + "\n-> 4 Arcanos Menores cujos naipes indicam quais aspectos (elementos) \nde quem tira a carta precisam ser harmonizados novamente. \nPara quando não se está sentindo bem, ansioso ou angustiado.")
                    a = apres_jogo()

                    if a == 1: tarot.elementos()

                elif opcao == 4:
                    print(Fore.YELLOW + "\n-> 3 Arcanos que representam, respecitivamente, Passado ou Causa, Presente ou Situação Atual, \ne Futuro ou Consequência. Para perguntas objetivas de sim ou não e bem formuladas.")
                    a = apres_jogo()

                    if a == 1: tarot.mandala_tres()

                elif opcao == 5:
                    print(Fore.YELLOW + "\n-> 6 Arcanos que representam, respecitvamente, Situação Atual, Influência Externa, Oposição,\n Favorecimento, Resultado e Conselho. Para perguntas objetivas e bem formuladas.")
                    a = apres_jogo()

                    if a == 1: tarot.mandala_cinco()

                elif opcao == 6:
                    print(Fore.BLUE + "\n-> 10 Arcanos que representam, respectivamente, Situação Presente, Influência Imediata, \nConsulente Perante o Problema, Determinações do Passado, O Que o Consulente Não Conhece, Influências do Futuro, \nConsulente, Fatores Ambientais, Caminho do Destino, e Resultado Final. \nPara perguntas bem formuladas, mas apresenta mais detalhes.")
                    a = apres_jogo()

                    if a == 1: tarot.cruz_celta()

                elif opcao == 7:
                    print(Fore.MAGENTA + "\n-> 7 Arcanos que representam, respectivamente, Como Está O Relacionamento, Consulente Na Situação, \nParceiro Na Situação, O Que Favorece O Relacionamento, O Que Não Favorece O Relacionamento, Futuro Próximo da Relação, \ne Conselho Final. Para perguntas sobre amor e relacionamentos.")
                    a = apres_jogo()

                    if a == 1: tarot.taca_amor()

                elif opcao == 8:
                    print(Fore.MAGENTA + "\n-> 7 Arcanos que representam, respectivamente, áreas Mental, Sentimental e Física de quem tira as cartas (1, 2, 3), \náreas Mental, Sentimental e Física do(a) parceiro(a) (4, 5, 6) e a Síntese do Relacionamento (Prognóstico). \nPara questões sobre estado e situação de um relacionamento.")
                    a = apres_jogo()

                    if a == 1: tarot.templo_afrodite()

                elif opcao == 9:
                    print(Fore.GREEN + "\n-> 4 Arcanos que representam, respectivamente, a Persona da pessoa em questão (o que ela mostra ser, \na 'máscara'), a Personalidade (o que ela é realmente e não mostra), as Motivações (o que a leva a agir desse jeito) \ne as Intenções (o que ela realmente quer de você). Para saber sobre as intenções de alguém que você talvez desconfie, \nsaber o que ela quer com você.")
                    a = apres_jogo()

                    if a == 1: tarot.carater()

                elif opcao == 10:
                    print(Fore.YELLOW + "\n-> 5 Arcanos que representam, respecitvamente, Positivo, Negativo, Caminho, Resultado e \nSíntese/Consulente. Para perguntas objetivas, bem formuladas e com tempo determinado.")
                    a = apres_jogo()

                    if a == 1: tarot.peladan()

                elif opcao == 11:
                    print(Fore.YELLOW + "\n-> 7 Arcanos para analisar a fundo alguma magia, feitiço ou amarração feita. \nA magia precisa ter sido confirmada através de outro jogo ou método antes deste método.")
                    a = apres_jogo()

                    if a == 1: tarot.sete_chaves()

                else: pass

        elif opcao1 == 2: #lenormand
            opcao = 1
            while opcao != 0:
                print("\nEscolha um método:")
                print(Fore.RED + "\n0- Voltar\n" + Fore.CYAN + "1 - Jogo Personalizado\n" + Fore.GREEN + "2- Mesa Real (36 cartas)\n" + Fore.BLUE + "3- Sim ou Não / Carta do Dia (1 carta)\n4- Carta e Conselho do Dia (2 cartas)" + Fore.YELLOW + "\n5- Passado, Presente e Futuro (3 ou 6 cartas)\n6- Tiragem de 5 Cartas (Solução de Problemas)\n" + Fore.MAGENTA + "7- Tiragem de 7 Cartas (Entendimento do Presente)")
                opcao = int(input("\nDigite o número: "))

                if opcao == 0: opcao1 = 1

                elif opcao == 1:
                    print(Fore.CYAN + "\n-> Joga um jogo personalizado, com número de cartas personalizado.")
                    a = apres_jogo()

                    if a == 1:lenormand.jogo_personalizado()

                elif opcao == 2:
                    print(Fore.GREEN + "\n-> 36 cartas (o baralho inteiro) para uma visão geral da vida da pessoa, levando-se em consideração\n as casas de acordo com o número das cartas (casa 1 = casa do Cavaleiro, casa 2 = casa do Trevo, etc).")
                    a = apres_jogo()

                    if a == 1: lenormand.mesa_real()

                elif opcao == 3:
                    print(Fore.BLUE + "\n-> 1 carta que responde sua pergunta de sim ou não (vide interpretações da carta além da 'tabela' \nde respostas). Ou então 1 carta que representa a energia geral do dia, recomendado verificar de manhã.")
                    a = apres_jogo()

                    if a == 1: lenormand.sim_nao()

                elif opcao == 4:
                    print(Fore.BLUE + "\n-> 2 cartas que mostram, respectivamente, a Energia geral do dia e o Conselho \npara o dia (o que fazer ou o que não fazer).")
                    a = apres_jogo()

                    if a == 1: lenormand.conselho_dia()

                elif opcao == 5:
                    print(Fore.YELLOW + "\n-> 3 ou 6 cartas que mnostram respectivamente influências do Passado, que afetaram diretamente ou \nresultaram no Presente, e qual a tendência do Futuro próximo.")
                    a = apres_jogo()

                    if a == 1: lenormand.pass_pres_fut()

                elif opcao == 6:
                    print(Fore.YELLOW + "\n-> 5 cartas que mostram, respectivamente, como o problema se encontra atualmente, atos do passado que \nresultaram ou influenciaram no presente, tendências do futuro próximo, algo oculto em meio a problema que a pessoa não \nsabe, e a solução/conselho para resolver o problema.")
                    a = apres_jogo()

                    if a == 1: lenormand.cinco_cartas()

                elif opcao == 7:
                    print(Fore.MAGENTA + "\n-> 7 cartas para visão mais profunda da situação atual, que mostram, respectivamente, Passado que \nresultou ou influencou no Presente, Situação no Atual Momento, tendências do Futuro Próximo, Resposta propriamente dita \npara a pergunta, Energias da situação, Esperanças/Medos da pessoa quanto à situação, e Resultado Final da situação.")
                    a = apres_jogo()

                    if a == 1: lenormand.sete_cartas()

                else: pass

        elif opcao1 == 3: #numerologia
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

        elif opcao1 == 4:
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
                    try:
                        jogow = connection.execute("SELECT pergunta, data, hora, mesa, cartas FROM jogos WHERE id = ?", (str(resp)))
                    except:
                        print("Não tem jogo com esse número. Digite outro.\n")
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

    #se a pessoa quiser sair do prog
    print(EXIT_TEXT)

if __name__ == "__main__":
    main()