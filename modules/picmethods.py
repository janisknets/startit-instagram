#Funkcija, kas ielādē visus attēlu nosaukumus vienā sarakstā pictures un atgriež to, lai varētu no tā pēc nosaukumiem ielādēt attēlus html lapā
def loadAllPictures():
  filepath = 'static/pictures.bin'
  pictures=[]
  with open(filepath) as fp:
    line = fp.readline()
    cnt = 1
    while line:
      pictures.append(line.strip())
      line = fp.readline()
      cnt += 1
  fp.close()
  return pictures

#Funkcija, kas pārbauda, vai attēls jau eksistē datnē pictures.bin. Ja eksistē, tad funkcija atgriež True. Ja attēls neeksistē, tad funcija atgriež False
def checkIfPictureExists(pictureName):
  exists = False
  allPictures = loadAllPictures()
  for picture in allPictures:
    if picture == pictureName:
      exists = True
  return exists

#Funkcija, kas pievieno jaunu attēlu datnē pictures.bin
def addNewPicture(pictureName):
  try:
    with open('static/pictures.bin',mode='a') as pictureFile:
      text = '\n'+ pictureName
      pictureFile.write(text)
      pictureFile.close()
  except:
    print('Error')
  finally:
    print("All ok")
  return 0