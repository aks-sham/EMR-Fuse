from flask import Flask, render_template, send_file, request, redirect
from fileup import app
import pandas as pd
from werkzeug.utils import secure_filename
import os
import urllib.request
import numpy as np

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/contact")
def contact():
    return render_template("contactus.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/developers")
def developers():
    return render_template("developers.html")

@app.route("/upcsv")
def upcsv():
    return render_template("csv.html")

@app.route("/display", methods=("POST", "GET"))
def display():
    df = pd.read_csv(r'C:\Users\aksha\OneDrive\Desktop\project\pp1\md\main.csv')
    a=df.head(501)
    return render_template('Table.html',  tables=[a.to_html()])

@app.route('/download')
def download_file():
	path = r'C:\Users\aksha\OneDrive\Desktop\project\pp1\md\main.csv'
	return send_file(path, as_attachment=True)


@app.route("/uploaded")
def up():
    return render_template("uploaded.html")

@app.route("/wrong-file-type")
def w():
    return render_template("wro.html")



ALLOWED_EXTENSIONS = set(['csv'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/fupload", methods = ['POST'])
def fupload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect('/upcsv')
        file = request.files['file']
        if file.filename == '':
            return redirect('/upcsv')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            fp=os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(fp)

            r=pd.read_csv(fp)
            l=pd.read_csv(r'C:\Users\aksha\OneDrive\Desktop\project\pp1\md\main.csv')
            #print(l.columns)
            ColNames = pd.Index(np.concatenate([l.columns, r.columns])).drop_duplicates()
            df = (l.set_index('id').combine_first(r.set_index('id')).reset_index().reindex(columns=ColNames))
            df.drop_duplicates(subset='id',keep='last', inplace=True)
            #print(sa)
            #print (df)
            #c=l.set_index('id').combine_first(r.set_index('id')).reset_index().drop_duplicates()
            #l=pd.merge(r, l, how='outer', on='id')
            df.to_csv(r'C:\Users\aksha\OneDrive\Desktop\project\pp1\md\main.csv', index = False)
            #print(c)
            #print(l.head())

            return redirect('/uploaded')
        else:
            return redirect('/wrong-file-type')
    

if __name__ == "__main__":
    app.run()