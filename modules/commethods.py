from modules import picmethods
import os
#Funkcija, kas meklē visus vienas bildes komentārus pēc bildes nosaukuma
def searchAllComments(picID):
  pictureComments = []
  allComments = []
  filepath = 'static/comments.bin'
  with open(filepath) as fp:
    line = fp.readline()
    cnt = 1
    while line:
      allComments.append(line.strip())
      line = fp.readline()
      cnt += 1
  fp.close()
  for fullInfoLine in allComments:
    temp = fullInfoLine.split(';')
    if temp[0] == picID:
      pictureComments.append(temp[2])
  return pictureComments

#Funkcija, kas saskaita, cik komentāru ir konkrētam attēlam comments.bin un atgriež konkrētu skaitli+1, 
#lai varētu piešķirt ID nākamajam jaunajam komentāram
def generateNextCommID(picID):
  nextID = 0
  allPicComments = searchAllComments(picID)
  for comment in allPicComments:
    if comment != '':
      nextID +=1
  return nextID+1

#Funkcija, kas pēc attēla nosaukuma atrod, cik konkrētam attēlam ir komentāru
def findCommentCount(picName):
  commentCount = 0
  allComments = []
  picID = picmethods.findPictureIdByName(picName)
  filepath = 'static/comments.bin'
  with open(filepath) as fp:
    line = fp.readline()
    cnt = 1
    while line:
      allComments.append(line.strip())
      line = fp.readline()
      cnt += 1
  fp.close()
  for fullInfoLine in allComments:
    temp = fullInfoLine.split(';')
    if temp[0] == picID:
      commentCount += 1
  return commentCount

#Funkcija, kas pievieno konkrētam attēlam jaunu komentāru
def addNewComment(picID,comment):
  nextCommID = 0
  text = ''
  try:
    with open('static/comments.bin',mode='a') as commentFile:
      nextCommID = generateNextCommID(picID)
      text = str(picID) + ';' + str(nextCommID) + ';' + comment + '\n'
      commentFile.write(text)
      commentFile.close()
  except:
    print('Error')
  finally:
    print("All ok")
  return 0

#Funkcija, kas dzeesh konkreetam atteelam konkreetu komentaaru
def deleteComment(picID,comID):
    #picID - bildes identifikators, str
#comID - komentara identifikators, str
  filepath_1 = 'static/comments.bin'
  filepath_2 = 'static/comold.bin'
  os.rename(filepath_1,filepath_2)
  fp1 = open(filepath_1,mode='a')
  fp2 = open(filepath_2,mode='r')
  with fp2:
    line = fp2.readline()
    while line:
      temp = line.split(';')
      if picID==temp[0]:
        if (comID!=temp[1]):
          fp1.write(line)
      else:  
        fp1.write(line)    
      line = fp2.readline()
  fp1.close()
  fp2.close()
  os.remove(filepath_2)
  return print("OK")
#Funkcija, kas pēc attēla ID un komentara satura atgriež komentara ID no comments.bin
def findCommentIdByName(picID,comment_txt):
  comID = 0
  filepath = 'static/comments.bin'
  with open(filepath) as fp:
    line = fp.readline()
    cnt = 1
    while line:
      if line!='':
        fullComInfo = line.strip().split(';')
        if fullComInfo[0] == picID:
          if(fullComInfo[2]==comment_txt):
            comID = fullComInfo[1]
      line = fp.readline()
      cnt += 1
  fp.close()
  return comID
