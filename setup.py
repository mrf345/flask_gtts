from os import path
from setuptools import setup

supported_versions = ["3.7", "3.8", "3.9", "3.10", "3.11", "3.12"]
basedir = path.abspath(path.dirname(__file__))
long_description = ''
requirements = []
requirements_path = path.join(basedir, 'requirements')


with open(path.join(basedir, path.join('flask_gtts', 'about.py'))) as f:
    exec(f.read())

with open(path.join(basedir, 'README.md')) as f:
    long_description += f.read()


if path.isdir(requirements_path):
    with open(path.join(requirements_path, 'main.txt')) as f:
        requirements += [line for line in f.read().split('\n') if line]
else:
    requires_path = path.join(
        path.join(basedir, "Flask_gTTS.egg-info"), "requires.txt"
    )

    with open(requires_path) as f:
        requirements += [line for line in f.read().split("\n") if line]

supported_python_classifiers = [
    "Programming Language :: Python :: {0}".format(v) for v in supported_versions
]

setup(
    name='Flask-gTTS',
    version=__version__,  # noqa
    url='https://github.com/mrf345/flask_gtts/',
    download_url='https://github.com/mrf345/flask_gtts/archive/%s.tar.gz'
    % __version__,  # noqa
    license=__license__,  # noqa
    author=__author__,  # noqa
    author_email=__email__,  # noqa
    description=__doc__,  # noqa
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['flask_gtts'],
    zip_safe=False,
    platforms='any',
    install_requires=requirements,
    package_data={'flask_gtts': ['read.html']},
    keywords=['flask', 'extension', 'google', 'text', 'speech',
              'gTTS', 'TTS', 'text-to-speech'],
    classifiers=[
        *supported_python_classifiers,
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
