#Funkcija, kas ielādē visus attēlu nosaukumus vienā sarakstā pictures un atgriež to, 
#lai varētu no tā pēc nosaukumiem ielādēt attēlus html lapā
def loadAllPictures():
  filepath = 'static/pictures.bin'
  pictures=[]
  with open(filepath) as fp:
    line = fp.readline()
    cnt = 1
    while line:
      if line!='':
        fullPicInfo = line.strip().split(';')
        pictures.append(fullPicInfo[1])
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

#Funkcija, kas saskaita, cik attēlu ir pictures.bin un atgriež konkrētu skaitli+1, 
#lai varētu piešķirt ID nākamajam jaunajam attēlam
def generateNextPicID():
  nextID = 0
  allPictures = loadAllPictures()
  for picture in allPictures:
    if picture != '':
      nextID +=1
  return nextID+1

#Funkcija, kas pievieno jaunu attēlu datnē pictures.bin
def addNewPicture(pictureName):
  try:
    with open('static/pictures.bin',mode='a') as pictureFile:
      picID = generateNextPicID
      text = picID + ';' + pictureName + '\n'
      pictureFile.write(text)
      pictureFile.close()
  except:
    print('Error')
  finally:
    print("All ok")
  return 0

#Funkcija, kas pēc attēla nosaukuma atgriež attēla ID no pictures.bin
def findPictureIdByName(picName):
  picID = 0
  filepath = 'static/pictures.bin'
  with open(filepath) as fp:
    line = fp.readline()
    cnt = 1
    while line:
      if line!='':
        fullPicInfo = line.strip().split(';')
        if fullPicInfo[1] == picName:
          picID = fullPicInfo[0]
      line = fp.readline()
      cnt += 1
  fp.close()
  return picID