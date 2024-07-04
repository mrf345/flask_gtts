import os
from importlib import import_module

import pytest
from flask_gtts import gtts, main

from .setup import app, language, text, extension, message

# workaround for py2 vs py3 mock import
unittest = import_module('unittest')
mock = getattr(unittest, 'mock', None) or import_module('mock')


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['STATIC_FOLDER'] = 'static'
    app.config['SERVER_NAME'] = 'localhost'
    extension.files = {}
    app.logger = mock.MagicMock()
    client = app.test_client()
    yield client


def test_gtts_remote_error_handling(client, monkeypatch):
    mock_gtts = mock.MagicMock()
    exception = AttributeError('something went wrong')
    mock_gtts().save.side_effect = exception
    monkeypatch.setattr(main, 'gTTS', mock_gtts)

    resp = client.get('%s/%s/%s' % (extension.route_path, language, text))

    assert resp.status_code == 500
    assert resp.json.get('mp3') == ''
    app.logger.exception.assert_called_once_with(exception)


def test_false_app_gtts(client):
    ''' test gtts false app input. '''
    try:
        gtts(app=None)
    except Exception as e1:
        assert type(e1) is AttributeError

    assert extension.tempdir.endswith('flask_gtts') is True


def test_template_sayit_mp3(client):
    ''' test sayit function in the template returns .mp3 '''
    assert client.get('/say').data.endswith(b'.mp3')
    assert extension.say(language, text).endswith('.mp3')


def test_template_sayit_file_exists(client):
    ''' test validity of mp3 file from template sayit '''
    extension.files = {}
    resp = client.get('/say')
    static_file_relative = resp.data[1:].decode('utf-8')
    static_file_path = os.path.join(extension.tempdir,
                                    os.path.basename(static_file_relative))

    assert os.path.isfile(static_file_path)


def test_dynamic_route_mp3(client):
    ''' test dynamic route mp3 response '''
    json = client.get('%s/%s/%s' % (extension.route_path, language, text)).json

    assert json.get('mp3', '').endswith('.mp3') is True


def test_template_read_js(client):
    ''' test if JS loaded in templated with read '''
    assert b'Flask-gTTS failed to fetch TTS' in client.get('/read').data


def test_route_decorator(client):
    ''' test route decorator response '''
    response = client.get('%s/%s/%s' % (extension.route_path, language, text),
                          headers={'prevent': True})

    assert response.data.decode('utf-8') == message


def test_cleanup_before_exit(client):
    ''' test cleanup func before exit '''
    assert extension.teardown() is None
