import os
from PIL import Image

path = "./img/cards/lenormand"

for _, _, files in os.walk(path):
        for imagem in files:
            if imagem.endswith(".png"):
                nome = os.path.splitext(imagem)

                img = Image.open("{}/{}" .format(path, imagem))
                resized = img.resize((300, 518), Image.LANCZOS)
                resized.save("{}/{}" .format(path, imagem))

print("feito")

"""#SOMA DOS VALORES E REDUÇÃO TEOSÓFICA
        soma = 0
        for numero in numeros:
            print(cartas[numero])
            soma += int(cartas[numero][2])
        print(soma)
        while soma > 21:
            soma_s = str(soma)
            soma = int(soma_s[0]) + int(soma_s[1]) #soma os algarismos
        print(soma)

        for linha in connection.execute("SELECT nome FROM cartas INNER JOIN tipos ON tipos.id = cartas.tipo_id WHERE tipos.grandeza = 'maior' AND cartas.valor = ?", [str(soma)]):
            sintese = linha[0]
            numeros.append(10) #um numero aleratorio pra somar 5 na lista"""