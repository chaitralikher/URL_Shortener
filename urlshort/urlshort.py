from flask import Blueprint, render_template,request,url_for,redirect,flash, abort,session,jsonify
import json
import os.path
from werkzeug.utils import secure_filename


bp = Blueprint('urlshort',__name__)

#give URL path for the homepage
@bp.route('/')

#function definition for homepage returns the html page
def homepage():
    return render_template('home.html',codes=session.keys())

#give URL path for the actual functionality page
@bp.route('/index', methods=['GET','POST'])

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
            return redirect(url_for('urlshort.homepage'))

        if 'url' in request.form.keys():
            urlList[request.form['shortname']]={'url':request.form['url']}
        else:
            fd=request.files['file']
            fname=request.form['shortname'] + secure_filename(fd.filename)
            fd.save('/Volumes/chaitrali/ML/URL_Shortener/urlshort/static/user_files/'+fname)
            urlList[request.form['shortname']]={'file':fname}

        #add dictionary entries to json file
        with open('urls.json','w') as url_file:
            json.dump(urlList, url_file)
            session[request.form['shortname']]= True #can be set to timestamp too
        return render_template('index.html', shortname=request.form['shortname'])
    else:
        return redirect(url_for('urlshort.homepage'))


@bp.route('/<string:shortname>')
def redirect_to_url(shortname):
    if os.path.exists('urls.json'):
        with open('urls.json') as url_file:
            urlList=json.load(url_file)
            if shortname in urlList.keys():
                if 'url' in urlList[shortname].keys():
                    return redirect(urlList[shortname]['url'])
                else:
                    return redirect(url_for('static', filename='user_files/'+urlList[shortname]['file']))
    return abort(404)

@bp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'),404

@bp.route('/session')
def session_api():
    return jsonify(list(session.keys()))
