from functools import wraps
from flask import Flask, render_template, request

from flask_gtts import gtts
from .mockers import mock_template


app = Flask(__name__)
message = 'You are not allowed!'


def prevent_header(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if request.headers.get('prevent'):
            return message

        return function(*args, **kwargs)

    return wrapper


eng = gtts(app, route=True, route_decorator=prevent_header)
text = 'something to say'
language = 'en-uk'


@app.route('/say')
def say():
    return render_template(mock_template(
        "{{sayit(lang='%s', text='%s')}}" % (language,
                                             text)))


@app.route('/read')
def read():
    return render_template(mock_template("{{read()}}"))
