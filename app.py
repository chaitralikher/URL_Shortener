from flask import Flask, render_template,request,url_for,redirect,flash
import json
import os.path
from werkzeug.utils import secure_filename


app=Flask(__name__)
app.secret_key='hiehbcdsjcvs7eyhnm'

#give URL path for the homepage
@app.route('/')

#function definition for homepage returns the html page
def homepage():
    return render_template('home.html')

#give URL path for the actual functionality page
@app.route('/index',methods=['GET','POST'])

#Function definition for index page
def index():
    #checks that it is a valid post request
    if request.method== 'POST':
        #dictionary for saving all website entries
        urlList={}
        #check if a json file exists
        if os.path.exists('urls.json'):
            with open('urls.json') as url_file:
                urlList=json.load(url_file)

        if request.form['shortname'] in urlList.keys():
            flash('That shortened url is already in use. Please select another one')
            return redirect(url_for('homepage'))

        if 'url' in request.form.keys():
            urlList[request.form['shortname']]={'url':request.form['URL']}
        else:
            fd=request.files['file']
            fname=request.form['shortname'] + secure_filename(fd.filename)
            fd.save('/Volumes/chaitrali/ML/URL_Shortener/'+fname)
            urlList[request.form['shortname']]={'file':fname}
        #add dictionary entries to json file
        with open('urls.json','w') as url_file:
            json.dump(urlList, url_file)

        return render_template('index.html', shortname=request.form['shortname'])
    else:
        return redirect(url_for('homepage'))


@app.route('/<string:shortname>')

def redirect_to_url(shortname):
    if os.path.exists('urls.json'):
        with open('urls.json') as url_file:
            urlList=json.load(url_file)
            if shortname in urlList.keys():
                if 'url' in urlList[shortname].keys():
                    return redirect(urlList[shortname]['url'])
