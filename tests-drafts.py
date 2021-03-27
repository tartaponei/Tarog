"""img_data = bytearray(bytes(cartas[indice][1], 'utf-8')) #binário da imagem da carta

#img = Image.frombytes("RGB", (300,518), img_data, "raw")
img = Image.open(io.BytesIO(img_data))

img2 = img.draft(img.mode, (img.width, img.height))
img2.show()"""

import cfonts

cfonts.say("BEM VINDO AO TAROG!", font='chrome', size=(80, 40), colors=("yellow", "yellow", "yellow"), background='transparent', align='left', letter_spacing=1, line_height=1, space=True, max_length=0, gradient=None, independent_gradient=False, transition=False)