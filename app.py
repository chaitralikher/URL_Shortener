from flask import Flask

app=Flask(__name__)
#print(__name__)

@app.route('/')

def homepage():
    return("Hello to first Flask Application")

@app.route('/about/')

def about():
    return("This is a Demo Flask Application created on May 27")
