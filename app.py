from flask import Flask, render_template,request,url_for,redirect,flash
import json
import os.path

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
        urlList[request.form['shortname']]={'url':request.form['URL']}
        #add dictionary entries to json file
        with open('urls.json','w') as url_file:
            json.dump(urlList, url_file)

        return render_template('index.html', shortname=request.form['shortname'])
    else:
        return redirect(url_for('homepage'))
