"""
Flask-gTTS
-------------

A Flask extension to add gTTS Google text to speech, into the template,
it makes adding and configuring multiple text to speech audio files at
a time much easier and less time consuming

"""
from setuptools import setup


setup(
    name='Flask-gTTS',
    version='0.3',
    url='https://github.com/mrf345/flask_gtts/',
    download_url='https://github.com/mrf345/flask_gtts/archive/0.3.tar.gz',
    license='MIT',
    author='Mohamed Feddad',
    author_email='mrf345@gmail.com',
    description='gTTS Google text to speech flask extension',
    long_description=__doc__,
    py_modules=['gtts'],
    packages=['flask_gtts'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'gTTS'
    ],
    keywords=['flask', 'extension', 'google', 'text', 'speech',
              'gTTS', 'TTS', 'text-to-speech'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
