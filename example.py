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
        file.write('''
            <html>
            <body>
                <h1 id="sayit" style="text-align: center;">
                    Another thing to say whenever clicked !
                </h1>
                <audio src="{{sayit("en-us","something to say")}}" controls>
                <script type='text/javascript'>
                    document.getElementById('sayit')
                    .addEventListener('click', (e) => {
                        fetch(
                            window.location.origin + 
                            '/gtts/en-us/' + 
                            String(document.getElementById('sayit').innerText)
                        ).then(function (r) {
                            return r.json()
                        }).then(function (j) {
                            let a = document.createElement('AUDIO')
                            a.src = window.location.origin + j.mp3
                            a.play()
                        }).catch(function (e) {
                            console.warn(e)
                        })
                    })
                </script>
            </body>
            </html>
        ''')
    return render_template('index.html')


app.run(debug=True, port=4000)