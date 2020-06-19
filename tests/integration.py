import os
from gtts import gTTS
from flask_gtts import gtts
from pytest import fixture

from .setup import app, language, text, eng, message


@fixture
def client():
    app.config['TESTING'] = True
    app.config['STATIC_FOLDER'] = 'static'
    app.config['SERVER_NAME'] = 'localhost'
    client = app.test_client()
    yield client


def test_false_app_gtts(client):
    ''' test gtts false app input. '''
    try:
        gtts(app=None)
    except Exception as e1:
        assert type(e1) == AttributeError
    try:
        gtts(app=app, temporary=200)
    except Exception as e2:
        assert type(e2) == TypeError

    assert gtts(app=app, tempdir='/').tempdir.endswith('flask_gtts') is True


def test_template_sayit_mp3(client):
    ''' test sayit function in the template returns .mp3 '''
    assert client.get('/say').data.endswith(b'.mp3')
    assert eng.say(language, text).endswith('.mp3')


def test_template_sayit_valid(client):
    ''' test validity of mp3 file from template sayit '''
    base_dir = app.static_folder
    file_name = 'testing.mp3'
    file_path = os.path.join(base_dir, file_name)
    static_file_relative = client.get('/say').data[1:].decode('utf-8')
    static_file_path = os.path.join(eng.tempdir,
                                    os.path.basename(static_file_relative))

    gTTS(text=text, lang=language).save(file_path)

    with open(static_file_path, 'rb') as resp:
        with open(file_path, 'rb') as default:
            assert resp.read() == default.read()


def test_dynamic_route_mp3(client):
    ''' test dynamic route mp3 response '''
    json = client.get('%s/%s/%s' % (eng.route_path, language, text)).json

    assert json.get('mp3', '').endswith('.mp3') is True


def test_template_read_js(client):
    ''' test if JS loaded in templated with read '''
    assert b'Flask-gTTS failed to fetch TTS' in client.get('/read').data


def test_route_decorator(client):
    ''' test route decorator response '''
    response = client.get('%s/%s/%s' % (eng.route_path, language, text),
                          headers={'prevent': True})

    assert response.data.decode('utf-8') == message


def test_cleanup_before_exit(client):
    ''' test cleanup func before exit '''
    assert eng.teardown() is None
