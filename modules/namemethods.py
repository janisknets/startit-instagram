import random

#Funkcija, kas ielādē visus lietotājvārdus 
def loadAllNicknames():
  filepath = 'static/nicknames.bin'
  nicknames=[]
  with open(filepath, mode="r", encoding="utf-8") as fp:
    line = fp.readline()
    cnt = 1
    while line:
      if line!='':
        nextNickname = line.strip()
        nicknames.append(nextNickname)
      line = fp.readline()
      cnt += 1
  fp.close()
  return nicknames

 #Funkcija, kas saskaita, cik kopā nejaušo niku vispār ir
def countNicknames():
    count = 0
    allNicknames = loadAllNicknames()
    for nickname in allNicknames:
        if nickname != '':
            count +=1
    return count

#Funkcija, kas no visu niku saraksta izvēlas vienu netīšu un atgriež to
def generateRandomNickname():
    nicknameCount = countNicknames()
    randomNicknameNumber = random.randint(1,nicknameCount)
    allNicknames = loadAllNicknames()
    randomNickname = allNicknames[randomNicknameNumber-1]
    return randomNickname