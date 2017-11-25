# flask_gtts
### A [Flask][1a19dccf] extension to add [gTTS][0de5906d] Google text to speech, into the template, it makes adding and configuring multiple text to speech audio files at a time much easier and less time consuming

  [1a19dccf]: http://flask.pocoo.org/ "Flask website"
  [0de5906d]: https://github.com/pndurette/gTTS "gTTS repo"

## Install it :
#### - With pip
`pip install Flask-gTTS` <br />
#### - or from github
`git clone https://github.com/mrf345/flask_gtts.git`<br />
`python setup.py install`
## Run it :
`from flask import Flask, render_template` <br />
`from flask_gtts import gtts` <br />
`app = Flask(__name__)` <br />
`gtts(app)` <br />
#### inside the template
`{% block content %}` <br />
`<audio src="{{ sayit(text='Hello from Flask !') }}"></audio>`<br />
`{% endblock %}` <br />

#### More detailed example
`{% block content %}` <br />
`<button type='button' onclick='document.getElementById("us").play();'>American</button>`<br />
`<button type='button' onclick='document.getElementById("ausi").play();'>Australian</button>` <br />
`<button type='button' onclick='document.getElementById("brit").play();'>British</button>` <br />
`<audio id='us' src="{{ sayit(lang='en-us', text='Hello from Flask !') }}"></audio>` <br />
`<audio id='ausi' src="{{ sayit(lang='en-au', text='Hello from Flask !') }}"></audio>` <br />
`<audio id='brit' src="{{ sayit(lang='en-uk', text='Hello from Flask !') }}"></audio>`<br />
`{% endblock %}` <br />
#### _Result_
![Datepicker](https://raw.githubusercontent.com/usb-resetter/usb-resetter.github.io/master/images/gtts.png)
##### _ Press them to hear the accent _

## Settings:
#### - gtts() options
#### `gtts(app=app,`<br />
##### _`---> temporary=True, # to remove audio files on exit`_<br />
##### _`---> tempdir='tempfile') # relative path in-which audio files will be stored`_ <br />

#### - sayit() options
#### `sayit(`<br />
##### _`---> lang='en-us', # language to convert text to`_
##### _`---> text='say hi') # text to be converted`_<br />

##### _List of supported languages :_
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
