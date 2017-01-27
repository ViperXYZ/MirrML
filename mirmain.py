import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory,make_response
from werkzeug.utils import secure_filename
from pprint import pprint
from pymongo import MongoClient
import ast
from datetime import datetime
from time import gmtime, strftime
import json
from clarifai import rest
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
import operator

# run these lines to access the Mirror Mirror application
os.environ["CLARIFAI_APP_ID"] = "fXM043GazV7t45lQSFQpw3Jj8NIuRWO4PEVNtzBS"
os.environ["CLARIFAI_APP_SECRET"] = "mKsHrQ7CKaHXROyeNfZlaDNZ61W2BH3jjIJ9NJ_7"

# initializing clarify app
cApp = ClarifaiApp()
model = cApp.models.get('Style-Categorizer')

client = MongoClient('localhost',27017)
db = client.MirrorMirror
user_images = db.user_Images
users = db.app_users

UPLOAD_FOLDER = 'static/users/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

catToNum = {"Casual" : 0, "Business" : 2, "Evening" : 1}

#Initiallizing Flask App
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results')
def results():
    username = request.cookies.get('userID')
    #path = os.path.join(app.config['UPLOAD_FOLDER'], username)
    #file_list = [path+"/"+file for file in os.listdir(path)]


    sorted_styles = getStyleList(username)


    i = 0
    for style in sorted_styles:
        sorted_styles[i] = (style[0],round(style[1] * 100, 2))
        i += 1

    topStyle = sorted_styles[0][0]

    matchedUsers = findMatches(username, topStyle)

    matchedUserPhotoes = []

    for un in matchedUsers:
        matchedUserPhotoes.append(findTopImage(un))

    print(sorted_styles)

    ret = [1,645,678,90,"hello world", sorted_styles, str(matchedUsers), str(matchedUserPhotoes)]

    dataToReturn = [sorted_styles, matchedUsers, matchedUserPhotoes]

    return render_template('result.html',result = dataToReturn)


def getStyleList(username):
    styles = {'Casual': 0, 'Business': 0, 'Evening': 0}


    count = 0

    queryResults = user_images.find({"username": username})
    for r in queryResults:



        casualList = r['clarifai_data']['outputs'][0]['data']['concepts']
        businessList = r['clarifai_data']['outputs'][0]['data']['concepts']
        eveningList = r['clarifai_data']['outputs'][0]['data']['concepts']


        for obj in r['clarifai_data']['outputs'][0]['data']['concepts']:
            if obj['id']=='Casual':
                styles['Casual'] += obj['value']
            if obj['id']=='Business':
                styles['Business'] += obj['value']
            if obj['id']=='evening':
                styles['Evening'] += obj['value']
       


        #styles['Casual'] += casualAmount
        
        
        
        #r['clarifai_data']['outputs'][0]['data']['concepts'][catToNum["Casual"]]['value']
        #styles['Business'] += BusinessAmount #r['clarifai_data']['outputs'][0]['data']['concepts'][catToNum["Business"]]['value']
        #styles['Evening'] += EveningAmount#r['clarifai_data']['outputs'][0]['data']['concepts'][catToNum["Evening"]]['value']
        count += 1

    if count > 0:
        styles['Casual'] = styles['Casual']/count
        styles['Business'] = styles['Business']/count
        styles['Evening'] = styles['Evening']/count



    #x = {1: 2, 3: 4, 4: 3, 2: 1, 0: 0}
    sorted_styles = sorted(styles.items(), key=operator.itemgetter(1), reverse=True)

    topStyle = sorted_styles[0][0]

    

    print("TOP STYLE::: " + topStyle)

    #updateResult = users.update()

    userUpdate = {"username" : username, "Top Style" : topStyle}

    updateResult = users.update({"username" : username},userUpdate, upsert = True)

    return sorted_styles
    
def findMatches(username, topStyle):
    queryResult = users.find({"username" : {'$ne' : username}, "Top Style" : topStyle})

    matches = []

    #used to limit number of results, as the build in querry limit seems to break the querry....
    limit = 3
    count = 0

    for r in queryResult:
        print(r)
        matches.append(r["username"])
        count += 1
        if count >= limit:
            break

    return matches

def findTopImage(username):
    topStyle = users.find_one({"username" : username})['Top Style']

    #print(['clarifai_data']['outputs'][0]['data']['concepts'][catToNum[topStyle]]['value'])

    images = list(user_images.find({"username": username}))

    topScore = 0

    topImagePath = None

    for i in images:
        if i['clarifai_data']['outputs'][0]['data']['concepts'][catToNum[topStyle]]['value'] > topScore:
            topImagePath = i['filepath']

    return topImagePath


@app.route('/upload', methods=['POST','GET'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            now = datetime.now()
            username = request.cookies.get('userID')
            print(username)
            filename = os.path.join(app.config['UPLOAD_FOLDER'], username)
            filename = os.path.join(app.config['UPLOAD_FOLDER']+username, "%s.%s" % (now.strftime("%Y-%m-%d-%H-%M-%S-%f"), file.filename.rsplit('.', 1)[1]))
            print(app.config['UPLOAD_FOLDER']+username)
            file.save(filename)


            #image = ClImage(url='https://samples.clarifai.com/metro-north.jpg')
            image = ClImage(file_obj=open(filename, 'rb'))
            pred = model.predict([image])


            user_images.insert_one(
                {
                    "username": username,
                    "filepath": filename,
                    "clarifai_data": pred       
                }
            )
            print(pred)

            return jsonify({"success":True})
    elif(request.method == 'GET'):
        return render_template("upload.html")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/login', methods=['POST','GET'])
def my_form_post():
    if(request.method == 'POST'):
        username = str(request.form['username']).strip()
        print(username)
        if((username!= "") and (not(os.path.isdir("static/users/" + username + "/")))):
            os.makedirs("static/users/" + username + "/")
            resp = make_response(render_template('upload.html'))
            resp.set_cookie('userID',username)
            return resp
        elif((username!= "") and (os.path.isdir("static/users/" + username + "/"))):
            resp = make_response(render_template('upload.html'))
            resp.set_cookie('userID',username)
            return resp
        else:
            return "<h1>Please enter a Username!!</h1>"
            
    else:
        return redirect("/")


if __name__ == '__main__':
    app.run(
        host = "localhost",
        port = 5000
    )

