from flask import Flask, render_template
from gtts import gTTS
from flask_gtts import gtts
from os import path, mkdir
from shutil import rmtree
from pytest import fixture
from atexit import register
from random import randint
from tempfile import TemporaryFile
from json import loads
from sys import version_info as V


text = 'something to say'
language = 'en-uk'
dirs = ['templates', 'static']

def toCleanUp():
    for d in dirs:
        if path.isdir(d):
            rmtree(d)

register(toCleanUp)

def toMimic(data):
    for d in dirs:
        if not path.isdir(d):
            mkdir(d)
    while True:
        tFile = str(randint(1, 9999999)) + '.html'
        if not path.isfile(tFile):
            break
    with open(path.join(dirs[0], tFile), 'w+') as file:
        file.write(data)
    return tFile


app = Flask(__name__)
eng = None
# eng = gtts(app=app, route=True)

@app.route('/say')
def say():
    return render_template(
        toMimic(
            "{{sayit(lang='%s', text='%s')}}" % (
                language, text
            )
        )
    )

@app.route('/read')
def read():
    return render_template(toMimic("{{read()}}"))


@fixture
def client():
    app.config['TESTING'] = True
    app.config['STATIC_FOLDER'] = 'static'
    app.config['SERVER_NAME'] = 'localhost'
    client = app.test_client()
    yield client

def test_false_app_gtts(client):
    """ test gtts false app input """
    try:
        gtts(app=None)
    except Exception as e1:
        assert type(e1) == AttributeError
    try:
        gtts(app=app, temporary=200)
    except Exception as e2:
        assert type(e2) == TypeError
    try:
        gtts(app=app, tempdir='/')
    except Exception as e4:
        assert type(e4) == TypeError
    try:
        gtts(app=app, tempdir=200)
    except Exception as e3:
        global eng
        eng = gtts(app=app, route=True)
        assert type(e3) == TypeError

def test_template_sayit_mp3(client):
    """ test sayit function in the template returns .mp3 """
    resp = client.get('/say').data
    assert resp.endswith(b'.mp3')
    ret = eng.say(language, text)
    assert ret.endswith('.mp3') 

def test_template_sayit_valid(client):
    """ test validity of mp3 file from template sayit """
    # mp3 = TemporaryFile()
    gTTS(text=text, lang=language).save('static/testing.mp3')
    with open(client.get('/say').data[1:], 'rb') as resp:
        with open('static/testing.mp3', 'rb') as default:
            assert resp.read() == default.read()

def test_dynamic_route_mp3(client):
    """ test dynamic route mp3 response """
    resp = loads(client.get('/gtts/%s/%s' % (
        language, text
    )).data)['mp3']
    assert resp.endswith('.mp3')

def test_template_read_js(client):
    """ test if JS loaded in templated with read """
    resp = client.get('/read').data
    assert b'Flask-gTTS failed to fetch TTS' in resp

def test_read_false_input_after_right(client):
    """ test gtts.read with False route """
    try:
        eng.route = False
        eng.read()
    except Exception as e:
        assert type(e) == AssertionError

def test_false_inputs_say(client):
    """ test false inputs on gtts.say """
    try:
        eng.say(lang=200, text=text)
        eng.say(lang=language, text=200)
    except Exception as e:
        assert type(e) == TypeError

def test_false_inputs_read(client):
    """ test false inputs on gtts.read """
    try:
        eng.read(id=200, mouseover=False)
    except Exception as e:
        assert type(e) == TypeError
    try:
        eng.read(mouseover=200)
    except Exception as e:
        assert type(e) == TypeError

def test_cleanup_before_exit(client):
    """ test cleanup func before exit """
    assert eng.cleanup() == None