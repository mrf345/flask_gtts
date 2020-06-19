import os
from functools import wraps
import atexit as at_exit
from shutil import rmtree
from uuid import uuid4
from flask import url_for, jsonify, Markup
from gtts import gTTS

from flask_gtts.constants import PY2


class gtts(object):
    def __init__(self, app=None, temporary=True, tempdir='flask_gtts', route=False,
                 route_path='/gtts', route_decorator=None):
        '''Extension to help in generating Google Text-To-Speech files.

        Parameters
        ----------
        app : Flask Application, optional
            Flask application instance, by default None
        temporary : bool, optional
            Remove the audio files before existing, by default True
        tempdir : str, optional
            Name of the static directory to store audio files in, by default 'flask_gtts'
        route : bool, optional
            Enable endpoint to generate TTS file dynamically, by default False
        route_path : str, optional
            Endpoint route path, by default '/gtts'
        route_decorator : callable, optional
            Decorator to wrap route endpoint, by default None
        '''
        self.temporary = temporary
        self.tempdir = 'flask_gtts' if not tempdir or tempdir.startswith('/') else tempdir
        self.route = route
        self.route_path = route_path
        self.route_decorator = route_decorator
        self.files = {}

        app and self.init_app(app)

    def init_app(self, app):
        '''Lazy load Flask Application.

        Parameters
        ----------
        app : Flask Application
            Flask application instance.
        '''
        self.app = app
        self.tempdir = os.path.join(self.app.static_folder, self.tempdir)
        self.inject()

        if not os.path.isdir(self.tempdir):
            if PY2:
                os.makedirs(self.tempdir)
            else:
                os.makedirs(self.tempdir, exist_ok=True)

        self.route and self.set_route()
        self.temporary and at_exit.register(self.teardown)

    def teardown(self):
        '''Remove the cache directory and its content.'''
        self.files = {}

        os.path.isdir(self.tempdir) and rmtree(self.tempdir)

    def inject(self):
        '''Inject say and read into templates.'''
        @self.app.context_processor
        def inject_vars():
            return dict(sayit=self.say, read=self.read)

    def say(self, lang='en-us', text='Flask says Hi!'):
        '''Generate a TTS audio file.

        Parameters
        ----------
        lang : str, optional
            Language to produce the TTS in, by default 'en-us'
        text : str, optional
            Text to convert into audio, by default 'Flask says Hi!'

        Returns
        -------
        str
            Relative url of the generated TTS audio file.
        '''
        if (text, lang) not in self.files:
            generator = gTTS(text=text) if lang == 'skip' else gTTS(lang=lang, text=text)
            file_name = None
            file_path = None

            while not file_name:
                temp_name = str(uuid4()).replace('-', '') + '.mp3'
                file_path = os.path.join(self.tempdir, temp_name)

                if not os.path.isfile(file_path):
                    break

            self.files[(text, lang)] = file_path
            generator.save(file_path)

        file_name = os.path.basename(self.files.get((text, lang)))
        relative_dir = os.path.basename(self.tempdir)

        with self.app.app_context():
            try:
                return url_for('static',
                               filename=os.path.join(relative_dir, file_name))
            except Exception:
                return ''

    def read(self, id='.toRead', mouseover=False):
        '''Read an HTML element inner text.

        Parameters
        ----------
        id : str, optional
            HTML element css selector, by default '.toRead'
        mouseover : bool, optional
            Read text on `mouseover` event instead of `click`, by default False

        Returns
        -------
        str
            Safe JavaScript to read an HTML element content.
        '''
        if not self.route:
            try:
                self.set_route()
            except Exception:
                pass

        file_path = os.path.join(os.path.dirname(__file__), 'read.html')

        with open(file_path) as html_file:
            return Markup(html_file.read()
                                   .replace('{id}', id)
                                   .replace('{route}', self.route_path)
                                   .replace('{event}', 'mouseover' if mouseover else 'click'))

    def set_route(self):
        ''' Setup a route endpont on `self.route_path/<language>/<text>` '''
        def empty_decorator(function):
            @wraps(function)
            def wrapper(*args, **kwargs):
                return function(*args, **kwargs)
            return wrapper

        decorator = self.route_decorator or empty_decorator

        @self.app.route(self.route_path + '/<language>/<text>')
        @decorator
        def gtts_route(language, text):
            if PY2:
                language = language.encode('utf8')
                text = text.encode('utf8')

            return jsonify(mp3=self.say(language, text)
                                   .replace('%5C', '/'))
