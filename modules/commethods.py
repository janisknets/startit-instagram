#Funkcija, kas meklē visus vienas bildes komentārus pēc bildes nosaukuma
def searchAllComments(picName):
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
    if temp[0] == picName:
      pictureComments.append(temp[1])
  return pictureComments

#Funkcija, kas pievieno konkrētam attēlam jaunu komentāru
def addNewComment(picName,comment):
  try:
    with open('static/comments.bin',mode='a') as commentFile:
      text = '\n'+ picName + ';' + comment
      commentFile.write(text)
      commentFile.close()
  except:
    print('Error')
  finally:
    print("All ok")
  return 0