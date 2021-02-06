"""img_data = bytearray(bytes(cartas[indice][1], 'utf-8')) #binário da imagem da carta

#img = Image.frombytes("RGB", (300,518), img_data, "raw")
img = Image.open(io.BytesIO(img_data))

img2 = img.draft(img.mode, (img.width, img.height))
img2.show()"""