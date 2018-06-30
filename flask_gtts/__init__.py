from flask import url_for, redirect, jsonify, Markup
from gtts import gTTS
from os import path, makedirs
from shutil import rmtree
from datetime import datetime
from atexit import register
from sys import version_info


class gtts(object):
    def __init__(
        self, app=None, temporary=True,
        tempdir='flask_gtts', route=False):
        """
        initiating the extension with the Flask app instance
        @param: app Flask app instance (Default: None)
        @param: temporary to remove stored audio files upon exiting (Default:
        True)
        @param: tempdir relative path to the directory in-which audio files
        will be stored (Default: 'flask_gtts')
        @param: route to produce gtts file from route /gtts/language/text
        (Default: False)
        """
        self.app = app
        self.temporary = temporary
        self.route = route
        self.rpath = path.join(self.app.static_folder, tempdir)
        self.rrpath = tempdir
        self.flist = {}
        self.routeFiles = {}
        if self.app is None:
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
        if self.route:
            self.gTTsRoute()

    def injectem(self):
        """ to inject say function as sayit into the template """
        @self.app.context_processor
        def inject_vars():
            return dict(sayit=self.say, read=self.read)

    def say(self, lang='en-us', text='Flask says Hi!'):
        for h, a in {'lang': lang, 'text': text}.items():
            if not isinstance(a, str):  # check if receiving a string
                raise(TypeError("gtts.say(%s) takes string" % h))
        if not path.isdir(self.rpath):  # creating temporary directory
            makedirs(self.rpath) if version_info.major == 2 else makedirs(
                # makedirs in py2 missing exist_ok
                self.rpath, exist_ok=True
            )
        if (text, lang) not in self.flist.keys():
            s = gTTS(text=text) if lang == 'skip' else gTTS(lang=lang, text=text)
            while True:  # making sure audio file name is truly unique
                fname = str(
                    datetime.utcnow()
                    ).replace('.', ''
                    ).replace('-', ''
                    ).replace(' ', ''
                    ).replace(':', '') + '.mp3'
                abp_fname = path.join(self.rpath, fname)
                if not path.isfile(abp_fname):
                    break
            self.flist[(text, lang)] = abp_fname
            s.save(abp_fname)
        else:
            fname = path.basename(self.flist.get((text, lang)))
        # returning ready to use url of the audio file
        with self.app.app_context():
            return url_for('static', filename=path.join(self.rrpath, fname))

    def read(self, id='.toRead', mouseover=False):
        if not isinstance(id, str):
            raise(TypeError("gtts.say_if(id) takes string"))
        if not isinstance(mouseover, bool):
            raise(TypeError("gtts.say_if(hover) takes True or False"))
        if not self.route:
            # activate route if not already
            self.gTTsRoute()
        return Markup(
            '''
            <script>
            document.addEventListener('DOMContentLoaded', function () {
                ("%s".startsWith('#'
                    ) ? [document.getElementById("%s".slice(1))
                    ] : [].slice.call(document.getElementsByClassName("%s".slice(1)))
                ).forEach(function (i) {
                    i.addEventListener("%s", function () {
                        fetch(
                            window.location.origin + '/gtts/' + 
                            (i.getAttribute('language') || 'skip') +
                            '/' + i.innerText
                        ).then(function (r) { return r.json() })
                        .then(function (j) {
                            var toPlay = document.createElement('AUDIO')
                            toPlay.src = j.mp3
                            toPlay.play()
                        }).catch(function (e) { console.warn(
                            'Flask-gTTS failed to fetch TTS from route'
                        ) })
                    })
                })
            })
            </script>
            ''' % (id, id, id, 'mouseover' if mouseover else 'click')
        )
        
        

    def cleanup(self):
        """ removing the temporary directory """
        if path.isdir(self.rpath):
            rmtree(self.rpath)

    def gTTsRoute(self):
        """ to setup a route on /gtts/lang/text, that cache & returns mp3 file link """
        @self.app.route('/gtts/<language>/<text>')
        def gttsRoute(language, text):
            return jsonify(mp3=self.say(
                language.encode('utf8') if version_info.major == 2 else language,
                text.encode('utf8') if version_info.major == 2 else text
            ).replace('%5C', '/'))