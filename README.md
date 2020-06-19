<h1 align='center'>Flask-gTTS</h1>
<p align='center'>
    <a href='https://travis-ci.com/mrf345/flask_gtts'>
        <img src='https://travis-ci.com/mrf345/flask_gtts.svg?branch=master' alt='Build Status' />
    </a>
    <a href='https://github.com/mrf345/flask_gtts/releases'>
        <img src='https://img.shields.io/github/v/tag/mrf345/flask_gtts' alt='Latest Release' />
    </a>
    <a href='https://coveralls.io/github/mrf345/flask_gtts?branch=master'>
        <img src='https://coveralls.io/repos/github/mrf345/flask_gtts/badge.svg?branch=master' alt='Coverage Status' />
    </a>
    <a href='https://www.python.org/dev/peps/pep-0008/'>
        <img src='https://img.shields.io/badge/code%20style-PEP8-orange.svg' alt='Code Style' />
    </a>
</p>
<h3 align='center'>A Flask extension to add support for Google Text-To-Speech (TTS).</h3>

## Install:
#### - With pip
- `pip install Flask-gTTS` <br />

#### - From the source:
- `git clone https://github.com/mrf345/flask_gtts.git`<br />
- `cd flask_gtts` <br />
- `python setup.py install`

## Setup:

#### - Inside the Flask app:
```python
from flask import Flask, render_template
from flask_gtts import gtts
app = Flask(__name__)
gtts(app)
```

#### - Inside the jinja template:
```jinja
{% block content %}
  <audio src="{{ sayit(text='Hello from Flask !')}}"></audio>
{% endblock %}
```

#### - Dynamic read TTS example:
```jinja
<head>
  {{ read(id='.readIt') }}
</head>
<body>
  <h1 class='readIt'>Say something</h1>
  <h1 class='readIT' language='it'>qualcosa da dire</h1>
</body>
```

#### - Dynamic route example:
```python
from flask import Flask
from flask_gtts import gtts

# If we want to allow only logged in users for example.
from flask_login import login_required

app = Flask(__name__)
gtts(app,
     route=True,
     route_decorator=login_required,
     route_path='/gtts')
```

And now you can test the endpoint by accessing `http://localhost:5000/gtts/en-us/some text to test`. It will return `JSON` response:

```json
{
    "mp3": "Generated audio file path."
}
```

## Settings:
- **`gtts()`** options:

```python
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
```

- **`sayit()`** options:

```python
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
```

- **`read()`** options:
```python
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
```

- **List of supported languages**:

`
    'af' : 'Afrikaans'
    'sq' : 'Albanian'
    'ar' : 'Arabic'
    'hy' : 'Armenian'
    'bn' : 'Bengali'
    'ca' : 'Catalan'
    'zh' : 'Chinese'
    'zh-cn' : 'Chinese (Mandarin/China)'
    'zh-tw' : 'Chinese (Mandarin/Taiwan)'
    'zh-yue' : 'Chinese (Cantonese)'
    'hr' : 'Croatian'
    'cs' : 'Czech'
    'da' : 'Danish'
    'nl' : 'Dutch'
    'en' : 'English'
    'en-au' : 'English (Australia)'
    'en-uk' : 'English (United Kingdom)'
    'en-us' : 'English (United States)'
    'eo' : 'Esperanto'
    'fi' : 'Finnish'
    'fr' : 'French'
    'de' : 'German'
    'el' : 'Greek'
    'hi' : 'Hindi'
    'hu' : 'Hungarian'
    'is' : 'Icelandic'
    'id' : 'Indonesian'
    'it' : 'Italian'
    'ja' : 'Japanese'
    'km' : 'Khmer (Cambodian)'
    'ko' : 'Korean'
    'la' : 'Latin'
    'lv' : 'Latvian'
    'mk' : 'Macedonian'
    'no' : 'Norwegian'
    'pl' : 'Polish'
    'pt' : 'Portuguese'
    'ro' : 'Romanian'
    'ru' : 'Russian'
    'sr' : 'Serbian'
    'si' : 'Sinhala'
    'sk' : 'Slovak'
    'es' : 'Spanish'
    'es-es' : 'Spanish (Spain)'
    'es-us' : 'Spanish (United States)'
    'sw' : 'Swahili'
    'sv' : 'Swedish'
    'ta' : 'Tamil'
    'th' : 'Thai'
    'tr' : 'Turkish'
    'uk' : 'Ukrainian'
    'vi' : 'Vietnamese'
    'cy' : 'Welsh'
`

## Credit:
- [gTTS][2c6d97b1]: Python Google text-to-speech

  [2c6d97b1]: https://github.com/pndurette/gTTS "gTTs repo"
