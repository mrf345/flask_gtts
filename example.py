from flask import Flask, render_template
from flask_gtts import gtts
from atexit import register
from os import remove, rmdir, mkdir, path

app = Flask(__name__, template_folder='.')
gtts(app, route=True)

def cleanUp():
    try:
        remove('index.html')
    except Exception:
        pass

register(cleanUp)

@app.route('/')
def root():
    with open('index.html', 'w+') as file:
        file.write('<html><body><audio src="{{sayit("en-us","something to say")}}" controls></body></html>')
    return render_template('index.html')


app.run(debug=True, port=4000)