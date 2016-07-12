#!lex/bin/python

import os

from flask import Flask, render_template, request, Response
import flask_assets as assets

from dictionary import Dictionary
from word import Word
from exceptions import LexicallyWebException

app = Flask(__name__)
app.config.from_object('config')

app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSION'] = set(['json'])

asset = assets.Environment(app)
scss = assets.Bundle('scss/main.scss', filters='scss', output='css/main.css')
coffee = assets.Bundle('coffee/main.coffee',
                       filters='coffeescript',
                       output='js/main.js')
asset.register('main_css', scss)
asset.register('main_coffee', coffee)

#  http://stackoverflow.com/a/9511655
extra_dirs = ['templates',]
extra_files = extra_dirs[:]
for extra_dir in extra_dirs:
    for dirname, dirs, files in os.walk(extra_dir):
        for filename in files:
            filename = os.path.join(dirname, filename)
            if os.path.isfile(filename):
                extra_files.append(filename)

d = Dictionary()
try:
    d.load()
except:
    pass


def allowed_file(filename):
    return (
        '.' in filename and
        filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']
    )


@app.route('/')
@app.route('/index')
def index():
    return render_template('layout.html',
                           language=d.language,
                           dictionary=d)


@app.route('/', methods=['POST'])
def modify_data():
    # Text Parameters
    parent = str(request.form['parent']).split(",")
    pos = str(request.form['pos'])
    meaning = str(request.form['meaning'])
    ipa = str(request.form['ipa'])
    notes = str(request.form['notes'])
    language = str(request.form['language'])

    # File
    file_ = request.files.get('file')

    # Confirmation
    submit_value = request.form['submit']

    if submit_value == "Add Word":
        d.add_word(Word(parent, pos, meaning, ipa, notes=notes))
    elif submit_value == "Delete Word":
        d.del_word(ipa)
    elif submit_value == "Save":
        return Response(d.save(),
                        mimetype='application/json',
                        headers={'Content-Disposition':
                                 'attachment;filename=dictionary.json'}
                        )
    elif submit_value == "Load":
        if file_ and allowed_file(file_.filename):
            d.load(file_.stream.read())
    elif submit_value == "Export as HTML":
        return Response(d.export_as_html(d.language))
    elif submit_value == "Change Language":
        d.language = language
    return render_template('layout.html',
                           language=d.language,
                           dictionary=d)


if __name__ == '__main__':
    app.run(debug=True, extra_files=extra_files)
