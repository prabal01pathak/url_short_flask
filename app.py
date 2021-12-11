#set FLASK_ENV=develpment
from flask import Flask,render_template, request, redirect, url_for, flash
import json
import os.path
from werkzeug.utils import secure_filename



app = Flask(__name__)
app.secret_key = "sldjflsjdfl32ljk43l2"


# home page
@app.route('/')
def home():
    print(dir(json))
    return render_template('home.html')


@app.route("/your-url",methods=['GET','POST'])
def your_url():
    if request.method == "POST":
        urls = {}

        # if key exist then return that it exits 
        if os.path.exists('urls.json'):
            with open("urls.json",'r') as urls_file:
                values = json.load(urls_file)

            if request.form['code'] in values.keys():
                flash('That shortname has already been taken Please Select Another Name.')
                return redirect(url_for("home"))
        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url':request.form['url']}
            print('this')
        else:
            f= request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save(os.path.join(os.getcwd() +'/static/user_files/' + full_name))
            urls[request.form['code']] = {'file':full_name}

        with open("urls.json",'w') as url_file:
            json.dump(urls,url_file)
        # get request data code and send it to form
        return  render_template("your_url.html",code = request.form['code'])
    return redirect(url_for('home'))

@app.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                else:
                    return redirect(url_for('static',filename='user_files/'+urls[code]['file']))
