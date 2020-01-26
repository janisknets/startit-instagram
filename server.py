from flask import Flask
from flask import request
from flask import url_for, json, jsonify, request
from flask import render_template, make_response
import os
from modules import picmethods, commethods
app = Flask(__name__)

@app.route('/',methods = ['POST', 'GET'])
def root():
  #Attēli ir linki uz pixabay attēliem; attēlu saraksts atrodas static/pictures.bin
  #Ja tiek pievienots jauns attēls
  if request.method == 'POST':
    newPicture = request.form['newPicture']
    pictureExistsAlready = picmethods.checkIfPictureExists(newPicture)
    if pictureExistsAlready:
      print('Duplicate picture error.')
    else:
      picmethods.addNewPicture(newPicture)
    pictures = picmethods.loadAllPictures()
    return render_template("bildes.html", pictures=pictures)
  #Ja lapa tiek vienkārši ielādēta
  else:
    lietotajs = ""
    #Skatāmies, vai eksistē cepums ar nosaukumu "lietotajs"
    #Ja neeksistē, uztaisām cepumu uz 24 stundām un ieliekam lietotājvārdu "Nezināms" (anonymous)
    if not request.cookies.get('lietotajs'):
        res = make_response('Uzstadam lietotajvardu')
        res.set_cookie('lietotajs', 'Nezināms', max_age=60*60*24)
        lietotajs = 'Nezināms'
    #Ja cepums jau eksistē, nolasām un ieliekam mainīgajā lietotajs
    else:
        res = make_response('Lietotajvards ir {}'.format(request.cookies.get('lietotajs')))
        lietotajs = request.cookies.get('lietotajs')

    #Ielādējam visus attēlus un izsaucam šablonu, padodot attēlu sarakstu, komentāru sarakstu un lietotājvārdu
    pictures = picmethods.loadAllPictures()
    return render_template("bildes.html", pictures=pictures,comments=commethods.findCommentCount,lietotajs=lietotajs)

@app.route('/bildes',methods = ['POST', 'GET'])
def visasBildes():
  #Ja tiek pievienots jauns attēls
  if request.method == 'POST':
    newPicture = request.form['newPicture']
    pictureExistsAlready = picmethods.checkIfPictureExists(newPicture)
    if pictureExistsAlready:
      print('Duplicate picture error.')
    else:
      picmethods.addNewPicture(newPicture)
    pictures = picmethods.loadAllPictures()
    return render_template("bildes.html", pictures=pictures)
  #Ja lapa tiek vienkārši ielādēta
  else:
    pictures = picmethods.loadAllPictures()
    return render_template("bildes.html", pictures=pictures)

@app.route('/bilde',methods = ['POST', 'GET'])
def bilde():
  pictureName = request.args.get('picture')
  pictureID = picmethods.findPictureIdByName(pictureName)
  #Ja tiek pievienots jauns komentārs no formas
  if request.method == 'POST':
    comments = commethods.searchAllComments(pictureID)
    newComment = request.form['newComment']
    commethods.addNewComment(pictureID,newComment)
    return render_template(
    "bilde.html", picture = pictureName,comm = comments)
  #Ja lapa tiek vienkārši ielādēta
  else:
    comments = commethods.searchAllComments(pictureID)
    return render_template(
    "bilde.html", picture = pictureName,comm = comments
  )

@app.route('/komentari/<komentaraID>')
def komentars(komentaraID):
  atrastaisKomentars = ""
  try:
    fp = open('komentari.txt')
    line = fp.readline()
    cnt = 0
    while line:
      print("cnt: {}, komentaraID: {}".format(cnt, komentaraID))
      if cnt == int(komentaraID):
        print("Line {}: {}".format(cnt, line.strip()))
        atrastaisKomentars = line
      line = fp.readline()
      cnt += 1
  finally:
    fp.close()
  return render_template('komentars.html', komentars = atrastaisKomentars)

@app.route('/mainit',methods = ['POST', 'GET'])
#Dzeesh, maina pret citu komentaru
def del_komentars():
  pictureID = "2"  # jaasanejem no lapas
  oldComID = "1"   # jasanjem no lapas, ja "", tad dzesh visus vildes komentarus
  newComment = "Rs viens pats"  # jasanjem no lapas, ja "xxx", tad ar sho nomaina veco, ja "", tad dzesh esosho komentaru
  commethods.deleteComment(pictureID,oldComID,newComment)
  return "OK"

@app.route('/chats/lasi')
def ielasit_chatu():
  chata_rindas = []
  with open('chats.txt','r', encoding='UTF-8') as f:
    for rinda in f:
      chata_rindas.append(rinda)
  return jsonify({'chats':chata_rindas})

@app.route('/chats/suuti', methods = ['POST'])
def suuti_zinju():
  dati = request.json
  with open('chats.txt', 'a', newline='', encoding='UTF-8') as f:
    f.write(dati['chats'] + '\n')
    return ielasit_chatu()

@app.route('/health')
def health():
  return "OK"

if __name__ == '__main__':
  app.run()
