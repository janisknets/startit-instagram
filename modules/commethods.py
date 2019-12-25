from modules import picmethods

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
  try:
    with open('static/comments.bin',mode='a') as commentFile:
      nextCommID = generateNextCommID(picID)
      text = picID + ';' + nextCommID + ';' + comment + '\n'
      commentFile.write(text)
      commentFile.close()
  except:
    print('Error')
  finally:
    print("All ok")
  return 0