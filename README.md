<h1 align='center'>flask_gtts</h1>
<h3 align='center'>A Flask extension to add gTTS (Google text to speech), into the template, it makes adding and configuring multiple text to speech audio files at a time much easier and less time consuming.</h3>

## Install:
#### - With pip
> - `pip install Flask-gTTS` <br />

#### - From the source:
> - `git clone https://github.com/mrf345/flask_gtts.git`<br />
> - `cd flask_gtts` <br />
> - `python setup.py install`

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
> - More complex example:

```jinja
{% block content %}
  <button type='button' onclick='document.getElementById("us").play();'>American</button>
  <button type='button' onclick='document.getElementById("ausi").play();'>Australian</button>
  <button type='button' onclick='document.getElementById("brit").play();'>British</button>
  <audio id='us' src="{{ sayit(lang='en-us', text='Hello from Flask !') }}"></audio>
  <audio id='ausi' src="{{ sayit(lang='en-au', text='Hello from Flask !') }}"></audio>
  <audio id='brit' src="{{ sayit(lang='en-uk', text='Hello from Flask !') }}"></audio>
{% endblock %}
```

## Settings:
> - gtts() options

```python
gtts(app=app,
    temporary=True, # to remove audio files on exit
    tempdir='tempfile', # relative path in-which audio files will be stored
    route=False # opens route on /gtts that takes /language/text as args to return gtts mp3 link
    ) 
```
> - sayit() options

```python
sayit(lang='en-us', # language to convert text to
      text='say hi') # text to be converted`_<br />
```

> _List of supported languages :_

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
> - [gTTS][2c6d97b1]: Python Google text-to-speech

  [2c6d97b1]: https://github.com/pndurette/gTTS "gTTs repo"
