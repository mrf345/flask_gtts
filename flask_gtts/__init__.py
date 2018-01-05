from flask import url_for
from gtts import gTTS
from os import path, makedirs
from shutil import rmtree
from random import randint
from atexit import register
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


class gtts(object):
    def __init__(self, app=None, temporary=True, tempdir='flask_gtts'):
        """
        initating the extension with the Flask app instance
        @param: app Flask app instance (Default: None)
        @param: temporary to remove stored audio files upon exiting (Default:
        True)
        @param: tempdir relative path to the directory in-which audio files
        will be stored (Default: 'flask_gtts')
        """
        self.app = app
        self.temporary = temporary
        self.rpath = path.join(self.app.static_folder, tempdir)
        self.rrpath = tempdir
        self.flist = {}
        if self.app is not None:
            self.init_app(app)
        else:
            raise(AttributeError("must pass app to gtts(app=)"))
        if not isinstance(tempdir, str):
            raise(TypeError("gtts(tempdir=) takes a string for a static path"))
        elif tempdir.startswith('/'):
            raise(TypeError(
                "gtts(tempdir=) requires relative path not abolute"))
        if not isinstance(temporary, bool):
            raise(TypeError("gtts(temporary=) takes True or False"))
        self.injectem()  # injecting into the template
        if self.temporary:
            register(self.cleanup)  # register audio files removal before exit

    def init_app(self, app):
        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)

    def teardown(self, exception):
        pass

    def injectem(self):
        """ to inject say function as sayit into the template """
        @self.app.context_processor
        def inject_vars():
            return dict(sayit=self.say)

    def say(self, lang='en-us', text='Flask says Hi!'):
        for h, a in {'lang': lang, 'text': text}.items():
            if not isinstance(a, str):  # check if recieving a string
                raise(TypeError("gtts.say(%s) takes string" % h))
        if not path.isdir(self.rpath):  # creating temporary directory
            makedirs(self.rpath, exist_ok=True)
        if (text, lang) not in self.flist.keys():
            s = gTTS(lang=lang, text=text)
            while True:  # making sure audio file name is truely unique
                fname = str(randint(1, 999999)) + '.mp3'
                abp_fname = path.join(self.rpath, fname)
                if not path.isfile(abp_fname):
                    break
            self.flist[(text, lang)] = abp_fname
            s.save(abp_fname)
        else:
            fname = path.basename(self.flist.get((text, lang)))
        # returning ready to use url of the audio file
        return url_for('static', filename=path.join(self.rrpath, fname))

    def cleanup(self):
        """ removing the temporary directory """
        if path.isdir(self.rpath):
            rmtree(self.rpath)
