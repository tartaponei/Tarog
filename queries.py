import sqlite3
#import cards
import os
from PIL import Image

connection = sqlite3.connect("database.db")
#c = connection.cursor()

"""for carta in cards.major:
    print(carta)
    connection.execute("INSERT INTO 'cartas' ('nome', 'tipo_id') VALUES (?, ?)", (carta, '1'))
connection.commit()

for carta in cards.numbered:
    print(carta)
    connection.execute("INSERT INTO 'cartas' ('nome', 'tipo_id') VALUES (?, ?)", (carta, '2'))
connection.commit()

for carta in cards.court:
    print(carta)
    connection.execute("INSERT INTO 'cartas' ('nome', 'tipo_id') VALUES (?, ?)", (carta, '3'))
connection.commit()"""

imgs = []

for img in os.listdir("./img/minor"):
    if img.endswith(".png"):
        nome, ext = os.path.splitext(img)
        with open("./img/minor/{}" .format(img), "rb") as file:
            img_data = file.read()
            img_id = int(nome[:2]) #pega os dois primeiros char do nome (id)
            item = [img_id, img_data]
            imgs.append(item)

for img in imgs:
    i_id = str(img[0]+1)
    data = img[1]
    print(i_id)
    print(len(data))

    connection.execute("UPDATE 'cartas' SET imagem = ? WHERE id = ?", (data, i_id))
    connection.commit()